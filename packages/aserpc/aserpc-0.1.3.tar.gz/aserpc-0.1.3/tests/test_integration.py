"""Integration tests for aserpc.

These tests define the expected API and behavior.
All components are explicit fixture parameters - no hidden magic.
"""

import time

import numpy as np
import numpy.testing as npt
import pytest
from ase import Atoms
from ase.calculators.calculator import Calculator, all_changes
from ase.calculators.lj import LennardJones

from conftest import BrokerFixture, WorkerFixture


# =============================================================================
# Basic usage - single worker
# =============================================================================


def test_remote_energy(
    broker: BrokerFixture,
    lj_worker: WorkerFixture,
    remote_lj_calculator,
    water: Atoms,
) -> None:
    """Basic energy calculation with remote LJ."""
    atoms = water.copy()
    atoms.calc = remote_lj_calculator
    energy = atoms.get_potential_energy()

    assert isinstance(energy, float)
    assert lj_worker.requests_handled == 1


def test_remote_matches_local(
    broker: BrokerFixture,
    lj_worker: WorkerFixture,
    remote_lj_calculator,
    water: Atoms,
) -> None:
    """Remote calculation matches local calculation."""
    # Local
    local = water.copy()
    local.calc = LennardJones()
    local_energy = local.get_potential_energy()
    local_forces = local.get_forces()

    # Remote
    remote = water.copy()
    remote.calc = remote_lj_calculator
    remote_energy = remote.get_potential_energy()
    remote_forces = remote.get_forces()

    # Compare
    assert np.isclose(remote_energy, local_energy)
    npt.assert_allclose(remote_forces, local_forces)


# =============================================================================
# Long-running calculations - worker timeout handling
# =============================================================================


class SlowCalculator(Calculator):
    """Calculator that sleeps during calculation to simulate slow computation."""

    implemented_properties = ["energy", "forces"]

    def __init__(self, delay: float = 2.0, **kwargs):
        super().__init__(**kwargs)
        self.delay = delay

    def calculate(self, atoms=None, properties=["energy"], system_changes=all_changes):
        super().calculate(atoms, properties, system_changes)
        # Simulate slow computation
        time.sleep(self.delay)
        # Return simple results
        self.results = {
            "energy": 0.0,
            "forces": np.zeros((len(self.atoms), 3)),
        }


def test_long_running_calculation_not_timed_out(water: Atoms) -> None:
    """Worker sending BUSY messages should not be timed out during long calculations.

    This test verifies that:
    1. Worker sends BUSY messages during computation (not HEARTBEAT)
    2. Broker doesn't timeout the worker even though computation > worker_timeout
    3. Calculation completes successfully
    """
    import shutil
    import uuid
    from pathlib import Path

    from aserpc import RemoteCalculator

    # Setup unique IPC paths
    short_id = uuid.uuid4().hex[:8]
    ipc_dir = f"/tmp/aserpc-{short_id}"
    Path(ipc_dir).mkdir(parents=True, exist_ok=True)
    frontend = f"ipc://{ipc_dir}/f.ipc"
    backend = f"ipc://{ipc_dir}/b.ipc"

    try:
        # Start broker with SHORT timeout (0.5s)
        broker = BrokerFixture(frontend=frontend, backend=backend)
        broker.start(worker_timeout=0.5)

        # Start worker with slow calculator (1.5s delay)
        # This is 3x the worker_timeout, so without BUSY messages it would timeout
        worker = WorkerFixture(
            name="slow",
            broker_backend=backend,
            calculator_factory=lambda: SlowCalculator(delay=1.5),
        )
        worker.start()
        time.sleep(0.1)  # Let worker register

        # Do a calculation - this should NOT timeout
        calc = RemoteCalculator(
            calc_name="slow", broker=frontend, timeout=10000, check_broker=False
        )
        atoms = water.copy()
        atoms.calc = calc
        energy = atoms.get_potential_energy()

        # Should complete successfully despite long computation
        assert isinstance(energy, float)
        assert worker.requests_handled == 1

        # Check logs show BUSY messages were sent (not worker timeout)
        broker_logs = broker.get_logs()
        assert "BUSY" in broker_logs, "Worker should send BUSY during long computation"
        assert "timed out" not in broker_logs.lower(), "Worker should NOT be timed out"

        # Cleanup
        worker.stop()
        broker.stop()

    finally:
        shutil.rmtree(ipc_dir, ignore_errors=True)


# =============================================================================
# Multiple workers - use factory
# =============================================================================


def test_multiple_workers_load_balancing(
    broker: BrokerFixture,
    lj_worker_factory,
    remote_lj_calculator,
    molecules_batch: list[Atoms],
) -> None:
    """Requests are distributed across multiple workers."""
    # Create 3 workers explicitly
    w1 = lj_worker_factory()
    w2 = lj_worker_factory()
    w3 = lj_worker_factory()

    # Calculate all molecules
    for atoms in molecules_batch:
        atoms = atoms.copy()
        atoms.calc = remote_lj_calculator
        atoms.get_potential_energy()

    # Verify load was distributed (each worker handled some requests)
    total_handled = w1.requests_handled + w2.requests_handled + w3.requests_handled
    assert total_handled == len(molecules_batch)

    # Can inspect logs of each worker
    for w in [w1, w2, w3]:
        assert "error" not in w.get_logs().lower()


def test_worker_logs_accessible(
    broker: BrokerFixture,
    lj_worker: WorkerFixture,
    remote_lj_calculator,
    water: Atoms,
) -> None:
    """Worker logs are accessible for debugging."""
    atoms = water.copy()
    atoms.calc = remote_lj_calculator
    atoms.get_potential_energy()

    # Worker logs should exist (may be empty if DEBUG level not set)
    logs = lj_worker.get_logs()
    # Just verify we can access logs - content depends on log level
    assert isinstance(logs, str)


# =============================================================================
# Parametrized tests
# =============================================================================


def test_g2_molecules(
    broker: BrokerFixture,
    lj_worker: WorkerFixture,
    remote_lj_calculator,
    g2_molecule: Atoms,
) -> None:
    """Energy calculation works for all g2 molecules."""
    atoms = g2_molecule.copy()
    atoms.calc = remote_lj_calculator
    energy = atoms.get_potential_energy()

    assert isinstance(energy, float)
    assert np.isfinite(energy)


# =============================================================================
# Error handling
# =============================================================================


def test_no_workers_raises(
    broker: BrokerFixture,
    remote_lj_calculator,  # No lj_worker!
    water: Atoms,
) -> None:
    """Request without workers raises clear error."""
    atoms = water.copy()
    atoms.calc = remote_lj_calculator

    with pytest.raises(RuntimeError, match="[Nn]o.*worker"):
        atoms.get_potential_energy()


def test_retry_on_worker_failure(
    broker: BrokerFixture,
    lj_worker_factory,
    water: Atoms,
) -> None:
    """RemoteCalculator retries when worker fails mid-calculation."""
    from aserpc import RemoteCalculator

    # Start a worker
    worker1 = lj_worker_factory()
    time.sleep(0.1)

    # Create calculator with retries=1 (1 initial attempt + 1 retry = 2 total)
    calc = RemoteCalculator(
        calc_name="lj",
        broker=broker.frontend,
        timeout=5000,
        check_broker=False,
        retries=1,
    )
    atoms = water.copy()
    atoms.calc = calc

    # First calculation succeeds
    energy1 = atoms.get_potential_energy()
    assert isinstance(energy1, float)
    assert worker1.requests_handled == 1

    # Kill the worker to simulate failure
    worker1.stop()
    time.sleep(0.2)

    # Start a new worker
    lj_worker_factory()
    time.sleep(0.1)

    # Second calculation should retry and succeed with new worker
    atoms2 = water.copy()
    atoms2.calc = calc
    energy2 = atoms2.get_potential_energy()
    assert isinstance(energy2, float)
    assert np.isclose(energy1, energy2)


def test_retry_exhausted_raises(
    broker: BrokerFixture,
    water: Atoms,
) -> None:
    """RemoteCalculator raises after all retries exhausted."""
    from aserpc import RemoteCalculator

    # No workers available
    calc = RemoteCalculator(
        calc_name="lj",
        broker=broker.frontend,
        timeout=1000,  # Short timeout
        check_broker=False,
        retries=1,  # 1 initial + 1 retry = 2 total attempts
    )
    atoms = water.copy()
    atoms.calc = calc

    # Should fail after 2 total attempts
    with pytest.raises(RuntimeError, match="[Nn]o.*worker"):
        atoms.get_potential_energy()


def test_calculator_error_propagated(broker: BrokerFixture) -> None:
    """Calculator errors are propagated to client with original message."""
    from ase import Atoms
    from ase.calculators.emt import EMT

    from aserpc import RemoteCalculator

    # Start EMT worker
    worker = WorkerFixture(
        name="emt",
        broker_backend=broker.backend,
        calculator_factory=EMT,
    )
    worker.start()
    time.sleep(0.1)

    # Create atoms with unsupported element (e.g., Uranium)
    # EMT only supports: H, C, N, O, Al, Ni, Cu, Pd, Ag, Pt, Au
    atoms = Atoms("U", positions=[[0, 0, 0]])

    calc = RemoteCalculator(
        calc_name="emt", broker=broker.frontend, timeout=5000, check_broker=False
    )
    atoms.calc = calc

    # Should raise RuntimeError with the original calculator error message
    # EMT raises: "No EMT-potential for U"
    with pytest.raises(RuntimeError, match="No EMT-potential for U"):
        atoms.get_potential_energy()

    worker.stop()


def test_worker_deregistration(
    broker: BrokerFixture,
    lj_worker_factory,
    water: Atoms,
) -> None:
    """Worker properly deregisters from broker on shutdown."""
    import time

    from aserpc.client import list_calculators, RemoteCalculator

    # Start a worker
    worker = lj_worker_factory()

    # Give broker time to register
    time.sleep(0.1)

    # Verify calculator is available
    calcs = list_calculators(broker.frontend)
    assert "lj" in calcs
    assert calcs["lj"] == 1

    # Do a calculation to verify it works
    calc = RemoteCalculator(
        calc_name="lj", broker=broker.frontend, timeout=5000, check_broker=False
    )
    atoms = water.copy()
    atoms.calc = calc
    energy = atoms.get_potential_energy()
    assert isinstance(energy, float)

    # Stop the worker
    worker.stop()

    # Give broker time to process DISCONNECT
    time.sleep(0.2)

    # Verify calculator is no longer available
    calcs = list_calculators(broker.frontend)
    assert "lj" not in calcs or calcs.get("lj", 0) == 0

    # Trying to calculate should fail
    calc2 = RemoteCalculator(
        calc_name="lj", broker=broker.frontend, timeout=5000, check_broker=False
    )
    atoms2 = water.copy()
    atoms2.calc = calc2

    with pytest.raises(RuntimeError, match="[Nn]o.*worker"):
        atoms2.get_potential_energy()


def test_remote_calculator_no_broker_raises() -> None:
    """RemoteCalculator raises ConnectionError if broker not running."""
    from aserpc.client import RemoteCalculator

    # Use a random IPC path that definitely doesn't exist
    fake_broker = "ipc:///tmp/aserpc-nonexistent-12345/frontend.ipc"

    with pytest.raises(ConnectionError, match="[Bb]roker not reachable"):
        RemoteCalculator(calc_name="lj", broker=fake_broker, check_broker=True)


def test_broker_returns_error_message(
    broker: BrokerFixture,
    remote_lj_calculator,
    water: Atoms,
) -> None:
    """Broker returns clear error message when no workers available."""
    atoms = water.copy()
    atoms.calc = remote_lj_calculator

    with pytest.raises(RuntimeError) as exc_info:
        atoms.get_potential_energy()

    # Error message should be informative
    assert "lj" in str(exc_info.value).lower()
    assert "worker" in str(exc_info.value).lower()


# =============================================================================
# Fixture smoke tests (run now)
# =============================================================================


def test_broker_fixture(broker: BrokerFixture) -> None:
    """Broker fixture provides IPC addresses."""
    assert broker.frontend.startswith("ipc://")
    assert broker.backend.startswith("ipc://")


def test_worker_fixture(broker: BrokerFixture, lj_worker: WorkerFixture) -> None:
    """Worker fixture connects to broker."""
    assert lj_worker.name == "lj"
    assert lj_worker.broker_backend == broker.backend


def test_worker_factory(broker: BrokerFixture, lj_worker_factory) -> None:
    """Worker factory creates multiple workers."""
    w1 = lj_worker_factory()
    w2 = lj_worker_factory()

    assert w1.name == "lj"
    assert w2.name == "lj"
    assert w1 is not w2


def test_water_fixture(water: Atoms) -> None:
    """Water fixture provides valid atoms."""
    assert len(water) == 3
    assert set(water.symbols) == {"O", "H"}


def test_local_lj(water: Atoms) -> None:
    """Local LJ works (sanity check)."""
    atoms = water.copy()
    atoms.calc = LennardJones()
    energy = atoms.get_potential_energy()
    assert isinstance(energy, float)


# =============================================================================
# CLI direct factory tests
# =============================================================================


def test_cli_load_factory_direct():
    """Test load_factory with direct module:callable syntax."""
    from aserpc.cli import load_factory

    # Load LennardJones directly
    factory = load_factory("ase.calculators.lj:LennardJones")
    calc = factory()
    assert calc.__class__.__name__ == "LennardJones"


def test_cli_load_factory_invalid():
    """Test load_factory with invalid paths."""
    from aserpc.cli import load_factory
    import pytest

    # Missing colon
    with pytest.raises(ValueError, match="expected 'module:name'"):
        load_factory("ase.calculators.lj.LennardJones")

    # Non-existent module
    with pytest.raises(ModuleNotFoundError):
        load_factory("nonexistent.module:Factory")

    # Non-existent attribute
    with pytest.raises(AttributeError):
        load_factory("ase.calculators.lj:NonExistentClass")


def test_cli_is_direct_factory_detection():
    """Test detection of direct module:callable vs name lookup."""
    # These should be detected as direct factory paths
    direct_paths = [
        "mace.calculators:mace_mp",
        "ase.calculators.lj:LennardJones",
        "my.package.submodule:CalculatorClass",
    ]

    # These should be detected as name lookups
    name_lookups = [
        "lj",
        "mace_mp",
        "my_calculator",
        "registry:CALCS",  # Registry path, not direct factory (no dot before colon)
    ]

    for path in direct_paths:
        is_direct = ":" in path and "." in path.split(":")[0]
        assert is_direct, f"Expected {path} to be detected as direct factory"

    for name in name_lookups:
        is_direct = ":" in name and "." in name.split(":")[0]
        assert not is_direct, f"Expected {name} to be detected as name lookup"


def test_cli_direct_factory_name_extraction():
    """Test name extraction from direct factory path."""
    test_cases = [
        ("mace.calculators:mace_mp", "mace_mp"),
        ("ase.calculators.lj:LennardJones", "LennardJones"),
        ("my.module:MyCalc", "MyCalc"),
    ]

    for path, expected_name in test_cases:
        extracted = path.rsplit(":", 1)[1]
        assert extracted == expected_name


# =============================================================================
# Broker restart tests
# =============================================================================


def test_worker_reconnects_after_broker_restart(water: Atoms) -> None:
    """Worker should re-register with broker after broker restart."""
    import shutil
    import time
    import uuid
    from pathlib import Path

    from aserpc import RemoteCalculator
    from aserpc.client import list_calculators

    from conftest import BrokerFixture, WorkerFixture

    # Setup unique IPC paths
    short_id = uuid.uuid4().hex[:8]
    ipc_dir = f"/tmp/aserpc-{short_id}"
    Path(ipc_dir).mkdir(parents=True, exist_ok=True)
    frontend = f"ipc://{ipc_dir}/f.ipc"
    backend = f"ipc://{ipc_dir}/b.ipc"

    try:
        # Start broker
        broker1 = BrokerFixture(frontend=frontend, backend=backend)
        broker1.start()

        # Start worker
        worker = WorkerFixture(
            name="lj",
            broker_backend=backend,
            calculator_factory=LennardJones,
        )
        worker.start()
        time.sleep(0.2)

        # Verify worker is registered
        calcs = list_calculators(frontend)
        assert "lj" in calcs, f"Worker not registered initially: {calcs}"
        assert calcs["lj"] == 1

        # Do a calculation to verify it works
        calc = RemoteCalculator(
            calc_name="lj", broker=frontend, timeout=5000, check_broker=False
        )
        atoms = water.copy()
        atoms.calc = calc
        energy1 = atoms.get_potential_energy()
        assert isinstance(energy1, float)

        # Stop broker (simulating crash/restart)
        broker1.stop()
        time.sleep(0.3)

        # Start new broker on same address
        broker2 = BrokerFixture(frontend=frontend, backend=backend)
        broker2.start()
        time.sleep(0.5)  # Give worker time to reconnect

        # Worker should have re-registered
        calcs = list_calculators(frontend)
        assert "lj" in calcs, f"Worker not re-registered after broker restart: {calcs}"
        assert calcs["lj"] == 1

        # Do another calculation to verify it still works
        calc2 = RemoteCalculator(
            calc_name="lj", broker=frontend, timeout=5000, check_broker=False
        )
        atoms2 = water.copy()
        atoms2.calc = calc2
        energy2 = atoms2.get_potential_energy()
        assert isinstance(energy2, float)
        assert np.isclose(energy1, energy2)

        # Cleanup
        worker.stop()
        broker2.stop()

    finally:
        shutil.rmtree(ipc_dir, ignore_errors=True)
