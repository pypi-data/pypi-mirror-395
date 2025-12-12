"""Manager - infrastructure worker for scale-to-zero worker management.

The Manager is a special worker that:
- Connects to the broker like a regular worker
- Receives SPAWN_REQUEST messages when clients request unavailable calculators
- Spawns worker processes on demand
- Monitors spawned processes for health
"""

import asyncio
import logging
import signal
import subprocess
import time
from dataclasses import dataclass, field

import zmq
import zmq.asyncio

from aserpc.constants import (
    HEARTBEAT_INTERVAL,
    IPC_BACKEND,
    MANAGER_HEARTBEAT,
    MANAGER_READY,
    MESSAGE_NAMES,
    SHUTDOWN,
    SPAWN_REQUEST,
    SPAWN_RESPONSE,
)
from aserpc.spawn import SpawnConfig

log = logging.getLogger(__name__)


@dataclass
class SpawnedProcess:
    """Tracks a spawned worker process."""

    process: subprocess.Popen
    calc_name: str
    started_at: float
    command: list[str]


@dataclass
class Manager:
    """Infrastructure manager that spawns workers on demand.

    Attributes:
        configs: Dictionary mapping calculator names to spawn configurations
        broker: ZMQ address of broker backend
        heartbeat_interval: Seconds between heartbeat checks
    """

    configs: dict[str, SpawnConfig]
    broker: str = IPC_BACKEND
    heartbeat_interval: float = HEARTBEAT_INTERVAL

    # Internal state
    _ctx: zmq.asyncio.Context | None = field(default=None, init=False, repr=False)
    _socket: zmq.asyncio.Socket | None = field(default=None, init=False, repr=False)
    _running: bool = field(default=False, init=False, repr=False)
    _stop_event: asyncio.Event | None = field(default=None, init=False, repr=False)
    _processes: dict[str, list[SpawnedProcess]] = field(
        default_factory=dict, init=False, repr=False
    )
    _spawn_counts: dict[str, int] = field(default_factory=dict, init=False, repr=False)

    async def run(self) -> None:
        """Run the manager (blocking)."""
        self._setup_signal_handlers()

        self._ctx = zmq.asyncio.Context()
        self._socket = self._ctx.socket(zmq.DEALER)
        self._socket.connect(self.broker)
        self._stop_event = asyncio.Event()
        self._running = True

        log.info(
            f"Manager started with {len(self.configs)} spawn configs, "
            f"connected to {self.broker}"
        )
        for name in self.configs:
            log.info(f"  - {name}: {' '.join(self.configs[name].command)}")

        # Send MANAGER_READY
        await self._send_manager_ready()

        try:
            await asyncio.gather(
                self._main_loop(),
                self._monitor_processes(),
                self._send_heartbeats(),
            )
        finally:
            await self._shutdown_all_processes()
            self._cleanup()

    def stop(self) -> None:
        """Signal the manager to stop."""
        self._running = False
        if self._stop_event and not self._stop_event.is_set():
            try:
                loop = asyncio.get_running_loop()
                loop.call_soon_threadsafe(self._stop_event.set)
            except RuntimeError:
                self._stop_event.set()

    def _setup_signal_handlers(self) -> None:
        """Setup graceful shutdown on SIGTERM/SIGINT."""
        import threading

        if threading.current_thread() is not threading.main_thread():
            return

        loop = asyncio.get_running_loop()

        def handler(sig: int) -> None:
            log.info(f"Received signal {sig}, shutting down...")
            self._running = False

        try:
            loop.add_signal_handler(signal.SIGTERM, lambda: handler(signal.SIGTERM))
            loop.add_signal_handler(signal.SIGINT, lambda: handler(signal.SIGINT))
        except (NotImplementedError, ValueError):
            pass

    def _cleanup(self) -> None:
        """Clean up resources."""
        if self._socket:
            self._socket.close(linger=0)
        if self._ctx:
            self._ctx.term()
        log.info(f"Manager stopped, total spawns: {sum(self._spawn_counts.values())}")

    async def _main_loop(self) -> None:
        """Main manager loop."""
        assert self._socket is not None
        poller = zmq.asyncio.Poller()
        poller.register(self._socket, zmq.POLLIN)

        while self._running:
            # Poll with heartbeat timeout
            events = await poller.poll(timeout=int(self.heartbeat_interval * 1000))

            if events:
                msg = await self._socket.recv_multipart()
                await self._handle_message(msg)

    async def _handle_message(self, msg: list[bytes]) -> None:
        """Handle incoming message from broker."""
        # Message format: [empty, msg_type, ...]
        if len(msg) < 2:
            log.warning(f"Invalid message: {msg}")
            return

        msg_type = msg[1]
        log.debug(f"Received {MESSAGE_NAMES.get(msg_type, msg_type.hex())}")

        if msg_type == SHUTDOWN:
            log.info("Received SHUTDOWN command")
            self._running = False
        elif msg_type == SPAWN_REQUEST:
            if len(msg) >= 3:
                calc_name = msg[2].decode()
                await self._handle_spawn_request(calc_name)
            else:
                log.warning("SPAWN_REQUEST missing calculator name")
        else:
            log.warning(f"Unknown message type: {msg_type.hex()}")

    async def _handle_spawn_request(self, calc_name: str) -> None:
        """Handle a spawn request from the broker."""
        log.info(f"Spawn request for calculator '{calc_name}'")

        if calc_name not in self.configs:
            log.warning(f"No spawn config for calculator '{calc_name}'")
            await self._send_spawn_response(calc_name, success=False, error="No config")
            return

        success = await self._spawn_worker(calc_name)
        await self._send_spawn_response(calc_name, success=success)

    async def _spawn_worker(self, calc_name: str) -> bool:
        """Spawn a worker for the given calculator.

        Returns:
            True if spawn was successful, False otherwise
        """
        config = self.configs[calc_name]
        command = config.render_command(broker=self.broker)

        log.info(f"Spawning worker for '{calc_name}': {' '.join(command)}")

        try:
            # Build environment
            env = None
            if config.env:
                import os

                env = os.environ.copy()
                env.update(config.env)

            # Spawn the process
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=config.cwd,
                env=env,
                start_new_session=True,  # Prevent signals from propagating
            )

            # Track the process
            spawned = SpawnedProcess(
                process=process,
                calc_name=calc_name,
                started_at=time.time(),
                command=command,
            )
            if calc_name not in self._processes:
                self._processes[calc_name] = []
            self._processes[calc_name].append(spawned)

            # Update spawn count
            self._spawn_counts[calc_name] = self._spawn_counts.get(calc_name, 0) + 1

            log.info(f"Spawned worker PID {process.pid} for '{calc_name}'")
            return True

        except Exception as e:
            log.exception(f"Failed to spawn worker for '{calc_name}': {e}")
            return False

    async def _monitor_processes(self) -> None:
        """Periodically check for dead processes and clean up."""
        while self._running:
            await asyncio.sleep(self.heartbeat_interval)

            for calc_name, processes in list(self._processes.items()):
                alive = []
                for spawned in processes:
                    retcode = spawned.process.poll()
                    if retcode is None:
                        # Still running
                        alive.append(spawned)
                    else:
                        # Process exited
                        uptime = time.time() - spawned.started_at
                        if retcode == 0:
                            log.info(
                                f"Worker PID {spawned.process.pid} for '{calc_name}' "
                                f"exited normally after {uptime:.1f}s"
                            )
                        else:
                            log.warning(
                                f"Worker PID {spawned.process.pid} for '{calc_name}' "
                                f"exited with code {retcode} after {uptime:.1f}s"
                            )

                if alive:
                    self._processes[calc_name] = alive
                else:
                    del self._processes[calc_name]

    async def _shutdown_all_processes(self) -> None:
        """Gracefully shutdown all spawned processes."""
        if not self._processes:
            return

        log.info("Shutting down all spawned workers...")

        for calc_name, processes in self._processes.items():
            for spawned in processes:
                if spawned.process.poll() is None:
                    log.info(f"Terminating worker PID {spawned.process.pid}")
                    spawned.process.terminate()

        # Wait a bit for graceful shutdown
        await asyncio.sleep(2.0)

        # Force kill any remaining
        for calc_name, processes in self._processes.items():
            for spawned in processes:
                if spawned.process.poll() is None:
                    log.warning(f"Force killing worker PID {spawned.process.pid}")
                    spawned.process.kill()

        self._processes.clear()

    async def _send_heartbeats(self) -> None:
        """Periodically send heartbeats to broker."""
        while self._running:
            await asyncio.sleep(self.heartbeat_interval)
            if self._running and self._socket:
                await self._socket.send_multipart([b"", MANAGER_HEARTBEAT])
                log.debug("Sent MANAGER_HEARTBEAT")

    async def _send_manager_ready(self) -> None:
        """Send MANAGER_READY message to broker."""
        assert self._socket is not None
        # Include list of available calculators
        calc_names = ",".join(self.configs.keys())
        await self._socket.send_multipart([b"", MANAGER_READY, calc_names.encode()])
        log.debug("Sent MANAGER_READY")

    async def _send_spawn_response(
        self, calc_name: str, success: bool, error: str | None = None
    ) -> None:
        """Send SPAWN_RESPONSE message to broker."""
        assert self._socket is not None
        status = b"ok" if success else b"error"
        error_msg = (error or "").encode() if not success else b""
        await self._socket.send_multipart(
            [b"", SPAWN_RESPONSE, calc_name.encode(), status, error_msg]
        )
        log.debug(f"Sent SPAWN_RESPONSE for '{calc_name}': {status.decode()}")

    def get_status(self) -> dict:
        """Get manager status for debugging/monitoring."""
        return {
            "running": self._running,
            "configs": list(self.configs.keys()),
            "spawn_counts": dict(self._spawn_counts),
            "active_processes": {
                name: len(procs) for name, procs in self._processes.items()
            },
        }
