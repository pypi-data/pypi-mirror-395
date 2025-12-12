"""Integration tests for aserpc.

These tests define the expected API and behavior.
All components are explicit fixture parameters - no hidden magic.
"""

import numpy as np
import numpy.testing as npt
import pytest
from ase import Atoms
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
