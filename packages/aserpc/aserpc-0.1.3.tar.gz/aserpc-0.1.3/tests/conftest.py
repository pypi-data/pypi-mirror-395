"""Pytest fixtures for aserpc testing.

Design principles:
- Explicit: every component is a visible fixture parameter
- Inspectable: access logs, state, metrics from fixtures
- Simple: clean API, no hidden magic

Usage:
    def test_energy(broker, lj_worker, remote_lj_calculator, water):
        atoms = water.copy()
        atoms.calc = remote_lj_calculator
        energy = atoms.get_potential_energy()

        # Inspect worker logs if needed
        assert "error" not in lj_worker.get_logs()
"""

import asyncio
import logging
import shutil
import threading
import time
import uuid
from collections.abc import Callable, Generator
from dataclasses import dataclass, field
from io import StringIO
from pathlib import Path

import pytest
from ase import Atoms
from ase.build import molecule
from ase.calculators.lj import LennardJones

from aserpc import Broker, RemoteCalculator, Worker


# =============================================================================
# Logging capture handler
# =============================================================================


class StringIOHandler(logging.Handler):
    """Handler that writes to a StringIO buffer."""

    def __init__(self, buffer: StringIO):
        super().__init__()
        self.buffer = buffer

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        self.buffer.write(msg + "\n")


# =============================================================================
# Broker fixture
# =============================================================================


@dataclass
class BrokerFixture:
    """Test broker with accessible state and logs."""

    frontend: str
    backend: str
    logs: StringIO = field(default_factory=StringIO)
    _broker: Broker | None = field(default=None, repr=False)
    _thread: threading.Thread | None = field(default=None, repr=False)
    _loop: asyncio.AbstractEventLoop | None = field(default=None, repr=False)

    def start(self, worker_timeout: float = 1.0) -> None:
        """Start broker in background thread."""
        self._broker = Broker(
            frontend=self.frontend,
            backend=self.backend,
            worker_timeout=worker_timeout,  # Short timeout for tests
        )

        # Setup logging to capture to StringIO
        handler = StringIOHandler(self.logs)
        handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
        broker_logger = logging.getLogger("aserpc.broker")
        broker_logger.addHandler(handler)
        broker_logger.setLevel(logging.DEBUG)

        def run_broker():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            try:
                self._loop.run_until_complete(self._broker.run())
            except Exception as e:
                self.logs.write(f"ERROR: Broker crashed: {e}\n")

        self._thread = threading.Thread(target=run_broker, daemon=True)
        self._thread.start()

        # Wait for broker to be ready (sockets bound)
        time.sleep(0.1)

    def stop(self) -> None:
        """Stop broker and cleanup."""
        if self._broker:
            self._broker.stop()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)

    @property
    def is_running(self) -> bool:
        """Check if broker is running."""
        return self._thread is not None and self._thread.is_alive()

    def get_logs(self) -> str:
        """Get broker logs as string."""
        return self.logs.getvalue()


@pytest.fixture
def broker() -> Generator[BrokerFixture, None, None]:
    """Broker fixture with accessible logs.

    Uses short IPC paths to stay within ZMQ's 107-char path limit.

    Usage:
        def test_something(broker):
            print(broker.frontend)  # IPC address
            print(broker.get_logs())  # Inspect logs
    """
    # Use short path to avoid ZMQ's IPC path length limits (107 chars on Unix)
    short_id = uuid.uuid4().hex[:8]
    ipc_dir = f"/tmp/aserpc-{short_id}"
    Path(ipc_dir).mkdir(parents=True, exist_ok=True)

    frontend = f"ipc://{ipc_dir}/f.ipc"
    backend = f"ipc://{ipc_dir}/b.ipc"

    b = BrokerFixture(frontend=frontend, backend=backend)
    b.start()

    yield b

    b.stop()

    # Cleanup IPC directory
    shutil.rmtree(ipc_dir, ignore_errors=True)


# =============================================================================
# Worker fixtures
# =============================================================================


@dataclass
class WorkerFixture:
    """Test worker with accessible state and logs."""

    name: str
    broker_backend: str
    calculator_factory: Callable
    logs: StringIO = field(default_factory=StringIO)
    _worker: Worker | None = field(default=None, repr=False)
    _thread: threading.Thread | None = field(default=None, repr=False)
    _loop: asyncio.AbstractEventLoop | None = field(default=None, repr=False)

    def start(self) -> None:
        """Start worker in background thread."""
        self._worker = Worker(
            name=self.name,
            calculator_factory=self.calculator_factory,
            broker=self.broker_backend,
            idle_timeout=300.0,  # Long timeout for tests
            heartbeat_interval=0.2,  # Short for fast test teardown
        )

        # Setup logging to capture to StringIO
        handler = StringIOHandler(self.logs)
        handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
        worker_logger = logging.getLogger("aserpc.worker")
        worker_logger.addHandler(handler)
        worker_logger.setLevel(logging.DEBUG)

        def run_worker():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            try:
                self._loop.run_until_complete(self._worker.run())
            except Exception as e:
                self.logs.write(f"ERROR: Worker crashed: {e}\n")

        self._thread = threading.Thread(target=run_worker, daemon=True)
        self._thread.start()

        # Wait for worker to connect and register
        time.sleep(0.1)

    def stop(self) -> None:
        """Stop worker and cleanup."""
        if self._worker:
            self._worker.stop()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)

    @property
    def is_running(self) -> bool:
        """Check if worker is running."""
        return self._thread is not None and self._thread.is_alive()

    def get_logs(self) -> str:
        """Get worker logs as string."""
        return self.logs.getvalue()

    @property
    def requests_handled(self) -> int:
        """Number of requests this worker has handled."""
        if self._worker:
            return self._worker.requests_handled
        return 0


@pytest.fixture
def lj_worker(broker: BrokerFixture) -> Generator[WorkerFixture, None, None]:
    """LJ worker fixture with accessible logs.

    Usage:
        def test_something(broker, lj_worker):
            # ... do calculations ...
            print(lj_worker.get_logs())
            print(lj_worker.requests_handled)
    """
    w = WorkerFixture(
        name="lj",
        broker_backend=broker.backend,
        calculator_factory=LennardJones,
    )
    w.start()

    yield w

    w.stop()


@pytest.fixture
def lj_worker_factory(
    broker: BrokerFixture,
) -> Generator[Callable[[], WorkerFixture], None, None]:
    """Factory to create multiple LJ workers.

    Usage:
        def test_load_balancing(broker, lj_worker_factory):
            w1 = lj_worker_factory()
            w2 = lj_worker_factory()
            w3 = lj_worker_factory()
            # ... test with multiple workers ...
    """
    workers: list[WorkerFixture] = []

    def create_worker() -> WorkerFixture:
        w = WorkerFixture(
            name="lj",
            broker_backend=broker.backend,
            calculator_factory=LennardJones,
        )
        w.start()
        workers.append(w)
        return w

    yield create_worker

    for w in workers:
        w.stop()


# =============================================================================
# Calculator fixtures
# =============================================================================


@pytest.fixture
def remote_lj_calculator(broker: BrokerFixture) -> RemoteCalculator:
    """Remote LJ calculator connected to broker.

    Note: Requires lj_worker fixture for actual calculations.

    Usage:
        def test_energy(broker, lj_worker, remote_lj_calculator, water):
            atoms = water.copy()
            atoms.calc = remote_lj_calculator
            energy = atoms.get_potential_energy()
    """
    # check_broker=False to avoid extra roundtrip in tests (broker is guaranteed running)
    return RemoteCalculator(
        calc_name="lj", broker=broker.frontend, timeout=10000, check_broker=False
    )


@pytest.fixture
def remote_calculator_factory(
    broker: BrokerFixture,
) -> Callable[[str], RemoteCalculator]:
    """Factory for creating RemoteCalculator instances.

    Usage:
        def test_multiple_calcs(broker, lj_worker, emt_worker, remote_calculator_factory):
            lj_calc = remote_calculator_factory("lj")
            emt_calc = remote_calculator_factory("emt")
    """

    def factory(calc_name: str) -> RemoteCalculator:
        # check_broker=False to avoid extra roundtrip in tests
        return RemoteCalculator(
            calc_name=calc_name,
            broker=broker.frontend,
            timeout=10000,
            check_broker=False,
        )

    return factory


# =============================================================================
# Test atoms fixtures
# =============================================================================


@pytest.fixture
def water() -> Atoms:
    """Water molecule."""
    return molecule("H2O")


@pytest.fixture
def ethanol() -> Atoms:
    """Ethanol molecule."""
    return molecule("CH3CH2OH")


@pytest.fixture
def methane() -> Atoms:
    """Methane molecule."""
    return molecule("CH4")


G2_MOLECULES = ["H2", "H2O", "NH3", "CH4", "CO", "CO2", "O2", "N2"]


@pytest.fixture(params=G2_MOLECULES, ids=G2_MOLECULES)
def g2_molecule(request: pytest.FixtureRequest) -> Atoms:
    """Parametrized fixture with g2 molecules."""
    return molecule(request.param)


@pytest.fixture
def molecules_batch() -> list[Atoms]:
    """Batch of molecules for throughput testing."""
    return [molecule(name) for name in G2_MOLECULES]
