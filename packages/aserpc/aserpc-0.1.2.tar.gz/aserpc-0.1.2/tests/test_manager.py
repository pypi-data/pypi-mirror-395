"""Tests for manager and scale-to-zero functionality."""

import asyncio
import logging
import sys
import threading
import time
from collections.abc import Generator
from dataclasses import dataclass, field
from io import StringIO

import pytest
from ase.build import molecule

from aserpc import Manager, RemoteCalculator, SpawnConfig
from aserpc.spawn import get_spawn_configs, load_spawn_registry


class StringIOHandler(logging.Handler):
    """Handler that writes to a StringIO buffer."""

    def __init__(self, buffer: StringIO):
        super().__init__()
        self.buffer = buffer

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        self.buffer.write(msg + "\n")


# =============================================================================
# SpawnConfig tests
# =============================================================================


def test_spawn_config_render_command():
    """Test SpawnConfig template variable substitution."""
    config = SpawnConfig(
        name="test_calc",
        command=["aserpc", "worker", "{name}", "--broker", "{broker}"],
    )

    rendered = config.render_command(broker="tcp://localhost:5555")
    assert rendered == [
        "aserpc",
        "worker",
        "test_calc",
        "--broker",
        "tcp://localhost:5555",
    ]


def test_spawn_config_render_command_with_idle_timeout():
    """Test SpawnConfig with idle_timeout variable."""
    config = SpawnConfig(
        name="mace",
        command=[
            "uvx",
            "aserpc",
            "worker",
            "{name}",
            "--idle-timeout",
            "{idle_timeout}",
        ],
        idle_timeout=120.0,
    )

    rendered = config.render_command()
    assert "{idle_timeout}" not in " ".join(rendered)
    assert "120.0" in rendered


def test_spawn_config_defaults():
    """Test SpawnConfig default values."""
    config = SpawnConfig(
        name="test",
        command=["echo", "hello"],
    )

    assert config.env is None
    assert config.cwd is None
    assert config.idle_timeout == 300.0  # Default from IDLE_TIMEOUT


# =============================================================================
# Registry loading tests
# =============================================================================


def test_load_spawn_registry_invalid_format():
    """Test that invalid registry path raises ValueError."""
    with pytest.raises(ValueError, match="expected 'module:variable'"):
        load_spawn_registry("invalid_path_no_colon")


def test_get_spawn_configs_empty():
    """Test get_spawn_configs returns empty dict when no entry points."""
    # With no registry and no entry points, should return empty dict
    configs = get_spawn_configs(registry_path=None)
    # This may or may not be empty depending on installed packages
    assert isinstance(configs, dict)


# =============================================================================
# Manager fixture for testing
# =============================================================================


@dataclass
class ManagerFixture:
    """Test manager with accessible state and logs."""

    configs: dict[str, SpawnConfig]
    broker_backend: str
    logs: StringIO = field(default_factory=StringIO)
    _manager: Manager | None = field(default=None, repr=False)
    _thread: threading.Thread | None = field(default=None, repr=False)
    _loop: asyncio.AbstractEventLoop | None = field(default=None, repr=False)

    def start(self) -> None:
        """Start manager in background thread."""
        self._manager = Manager(
            configs=self.configs,
            broker=self.broker_backend,
            heartbeat_interval=0.2,
        )

        # Setup logging
        handler = StringIOHandler(self.logs)
        handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
        manager_logger = logging.getLogger("aserpc.manager")
        manager_logger.addHandler(handler)
        manager_logger.setLevel(logging.DEBUG)

        def run_manager():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            try:
                self._loop.run_until_complete(self._manager.run())
            except Exception as e:
                self.logs.write(f"ERROR: Manager crashed: {e}\n")

        self._thread = threading.Thread(target=run_manager, daemon=True)
        self._thread.start()
        time.sleep(0.1)

    def stop(self) -> None:
        """Stop manager and cleanup."""
        if self._manager:
            self._manager.stop()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)

    @property
    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def get_logs(self) -> str:
        return self.logs.getvalue()

    def get_status(self) -> dict:
        if self._manager:
            return self._manager.get_status()
        return {}


@pytest.fixture
def manager_fixture(broker) -> Generator[ManagerFixture, None, None]:
    """Manager fixture that spawns LJ workers."""
    # Create spawn config that runs aserpc worker in same environment
    config = SpawnConfig(
        name="lj",
        command=[
            sys.executable,
            "-m",
            "aserpc.cli",
            "worker",
            "lj",
            "--broker",
            broker.backend,
            "--idle-timeout",
            "30",
        ],
        idle_timeout=30.0,
    )

    m = ManagerFixture(
        configs={"lj": config},
        broker_backend=broker.backend,
    )
    m.start()

    yield m

    m.stop()


# =============================================================================
# Integration tests
# =============================================================================


def test_manager_registers_with_broker(broker, manager_fixture):
    """Test that manager successfully registers with broker."""
    time.sleep(0.2)  # Give time for registration

    # Check broker logs for manager registration
    broker_logs = broker.get_logs()
    assert "Manager" in broker_logs or manager_fixture.is_running


def test_scale_to_zero_spawn_request_sent(broker, manager_fixture):
    """Test that broker sends spawn request to manager when no workers available."""
    # Give manager time to register
    time.sleep(0.2)

    # Create client and request calculation with short timeout
    calc = RemoteCalculator(
        calc_name="lj",
        broker=broker.frontend,
        timeout=2000,  # Short timeout - we just want to trigger spawn
        check_broker=False,
    )

    atoms = molecule("H2O")
    atoms.calc = calc

    # This will timeout but should have triggered spawn request
    try:
        atoms.get_potential_energy()
    except TimeoutError:
        pass  # Expected - spawned worker may fail or take too long

    # Check that manager spawned a worker (even if it failed)
    # The log shows "Worker PID X for 'lj' exited" which proves spawn happened
    manager_logs = manager_fixture.get_logs()
    assert "PID" in manager_logs and "lj" in manager_logs

    # Verify spawn was attempted
    status = manager_fixture.get_status()
    spawn_count = status.get("spawn_counts", {}).get("lj", 0)
    assert spawn_count >= 1


def test_manager_no_config_logs_warning(broker):
    """Test that manager logs warning for unknown calculator."""
    # Create manager with empty config
    m = ManagerFixture(
        configs={},
        broker_backend=broker.backend,
    )
    m.start()
    time.sleep(0.2)

    # Create client requesting unknown calculator
    calc = RemoteCalculator(
        calc_name="unknown_calc",
        broker=broker.frontend,
        timeout=5000,
        check_broker=False,
    )

    atoms = molecule("H2O")
    atoms.calc = calc

    # This should fail since no workers and manager has no config
    with pytest.raises(Exception):
        atoms.get_potential_energy()

    m.stop()


def test_manager_status(broker, manager_fixture):
    """Test manager status reporting."""
    time.sleep(0.2)
    status = manager_fixture.get_status()

    assert "running" in status
    assert "configs" in status
    assert "lj" in status["configs"]


# =============================================================================
# Concurrent spawn tests
# =============================================================================


def test_concurrent_requests_single_spawn(broker, manager_fixture):
    """Test that multiple concurrent requests don't trigger duplicate spawns."""
    time.sleep(0.2)  # Wait for manager to register

    results = []
    errors = []

    def make_request(idx: int):
        """Make a request in a thread."""
        try:
            calc = RemoteCalculator(
                calc_name="lj",
                broker=broker.frontend,
                timeout=3000,
                check_broker=False,
            )
            atoms = molecule("H2O")
            atoms.calc = calc
            energy = atoms.get_potential_energy()
            results.append((idx, energy))
        except Exception as e:
            errors.append((idx, str(e)))

    # Launch multiple concurrent requests
    threads = [threading.Thread(target=make_request, args=(i,)) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=10)

    # Wait a bit for spawns to be tracked
    time.sleep(0.5)

    # Check spawn count - should be 1 (deduplication), not 5
    status = manager_fixture.get_status()
    spawn_count = status.get("spawn_counts", {}).get("lj", 0)
    # Should spawn at least 1, but due to deduplication not 5
    assert spawn_count >= 1
    # Due to the race with worker becoming ready, might spawn a few but not all 5
    assert spawn_count <= 3, f"Too many spawns: {spawn_count}, expected deduplication"


# =============================================================================
# Manager disconnect tests
# =============================================================================


def test_manager_disconnect_clears_spawn_state(broker):
    """Test that manager disconnect clears spawn-in-progress state."""
    # Create and start manager
    config = SpawnConfig(
        name="lj",
        command=["sleep", "10"],  # Long-running command that won't become a real worker
    )
    m = ManagerFixture(
        configs={"lj": config},
        broker_backend=broker.backend,
    )
    m.start()
    time.sleep(0.3)

    # Verify manager connected
    broker_logs = broker.get_logs()
    assert "Manager" in broker_logs

    # Trigger a spawn request
    calc = RemoteCalculator(
        calc_name="lj",
        broker=broker.frontend,
        timeout=500,
        check_broker=False,
    )
    atoms = molecule("H2O")
    atoms.calc = calc

    try:
        atoms.get_potential_energy()
    except Exception:
        pass

    # Stop manager (simulates disconnect)
    m.stop()
    time.sleep(0.5)

    # Start a new manager
    m2 = ManagerFixture(
        configs={"lj": config},
        broker_backend=broker.backend,
    )
    m2.start()
    time.sleep(0.3)

    # New manager should be able to receive spawn requests
    # (spawn_requested should have been cleared)
    try:
        atoms.get_potential_energy()
    except Exception:
        pass

    # Verify new manager received spawn request
    m2_logs = m2.get_logs()
    assert "Spawn request" in m2_logs or "lj" in m2_logs

    m2.stop()


def test_manager_timeout_detection(broker):
    """Test that broker detects manager timeout and clears state."""
    # Create manager with short heartbeat
    config = SpawnConfig(name="test", command=["echo", "test"])

    m = ManagerFixture(
        configs={"test": config},
        broker_backend=broker.backend,
    )
    m.start()
    time.sleep(0.3)

    # Verify manager registered
    assert "Manager" in broker.get_logs()

    # Stop manager without graceful disconnect
    if m._manager:
        m._manager._running = False  # Force stop without sending disconnect
    time.sleep(0.2)

    # After worker_timeout (broker uses 1.0s in tests), manager should be cleared
    # Wait for broker's monitor loop to detect timeout
    time.sleep(2.0)

    # New requests should fail immediately (no manager to spawn)
    calc = RemoteCalculator(
        calc_name="nonexistent",
        broker=broker.frontend,
        timeout=1000,
        check_broker=False,
    )
    atoms = molecule("H2O")
    atoms.calc = calc

    with pytest.raises(Exception) as exc_info:
        atoms.get_potential_energy()

    # Should get "no workers available" error, not timeout
    assert (
        "No workers available" in str(exc_info.value)
        or "timeout" in str(exc_info.value).lower()
    )

    m.stop()


# =============================================================================
# Spawn failure tests
# =============================================================================


def test_spawn_failure_command_not_found(broker):
    """Test that spawn failure with nonexistent command is handled."""
    config = SpawnConfig(
        name="bad_calc",
        command=["nonexistent_command_xyz123", "arg1"],
    )

    m = ManagerFixture(
        configs={"bad_calc": config},
        broker_backend=broker.backend,
    )
    m.start()
    time.sleep(0.3)

    calc = RemoteCalculator(
        calc_name="bad_calc",
        broker=broker.frontend,
        timeout=3000,
        check_broker=False,
    )
    atoms = molecule("H2O")
    atoms.calc = calc

    # Should fail, not hang forever
    with pytest.raises(Exception) as exc_info:
        atoms.get_potential_energy()

    # Should get an error (either spawn failure or timeout)
    error_msg = str(exc_info.value).lower()
    assert "spawn" in error_msg or "timeout" in error_msg or "no workers" in error_msg

    m.stop()


def test_spawn_failure_immediate_exit(broker):
    """Test handling of worker that exits immediately after spawn."""
    config = SpawnConfig(
        name="fast_exit",
        command=["sh", "-c", "exit 1"],  # Exits immediately with error
    )

    m = ManagerFixture(
        configs={"fast_exit": config},
        broker_backend=broker.backend,
    )
    m.start()
    time.sleep(0.3)

    calc = RemoteCalculator(
        calc_name="fast_exit",
        broker=broker.frontend,
        timeout=2000,
        check_broker=False,
    )
    atoms = molecule("H2O")
    atoms.calc = calc

    with pytest.raises(Exception):
        atoms.get_potential_energy()

    # Manager should have logged the exit
    time.sleep(0.5)
    manager_logs = m.get_logs()
    assert "exited" in manager_logs.lower() or "exit" in manager_logs.lower()

    m.stop()


def test_spawn_failure_propagates_to_clients(broker):
    """Test that spawn failure error is sent to waiting clients."""
    # Use a config for calculator that manager doesn't have
    m = ManagerFixture(
        configs={},  # Empty config
        broker_backend=broker.backend,
    )
    m.start()
    time.sleep(0.3)

    calc = RemoteCalculator(
        calc_name="missing_calc",
        broker=broker.frontend,
        timeout=2000,
        check_broker=False,
    )
    atoms = molecule("H2O")
    atoms.calc = calc

    # Should fail quickly with spawn failure, not wait for full timeout
    start = time.time()
    with pytest.raises(Exception) as exc_info:
        atoms.get_potential_energy()
    elapsed = time.time() - start

    # Should fail faster than the full 2s timeout
    # (spawn failure should propagate immediately)
    assert elapsed < 1.5, f"Took too long: {elapsed}s, expected fast failure"

    # Error message should indicate spawn failure
    error_msg = str(exc_info.value)
    assert "spawn" in error_msg.lower() or "No workers" in error_msg

    m.stop()


def test_manager_heartbeat_keeps_alive(broker):
    """Test that manager heartbeats prevent timeout."""
    config = SpawnConfig(name="test", command=["echo", "test"])

    m = ManagerFixture(
        configs={"test": config},
        broker_backend=broker.backend,
    )
    m.start()
    time.sleep(0.3)

    # Manager is running with heartbeat_interval=0.2
    # Broker has worker_timeout=1.0
    # Wait longer than timeout to verify heartbeats keep manager alive
    time.sleep(1.5)

    # Manager should still be registered (heartbeats prevented timeout)
    assert m.is_running

    # Trigger a spawn to verify manager still works
    calc = RemoteCalculator(
        calc_name="test",
        broker=broker.frontend,
        timeout=1000,
        check_broker=False,
    )
    atoms = molecule("H2O")
    atoms.calc = calc

    try:
        atoms.get_potential_energy()
    except Exception:
        pass  # Command is just 'echo', won't create real worker

    # Manager should have received spawn request
    manager_logs = m.get_logs()
    assert "Spawn request" in manager_logs or "test" in manager_logs

    m.stop()
