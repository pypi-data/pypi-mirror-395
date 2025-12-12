"""Worker - serves a single calculator type.

Key features:
- Runs calculator in ThreadPoolExecutor (keeps async loop free for heartbeats)
- Sends BUSY messages while computing long calculations
- Self-terminates after idle timeout
"""

import asyncio
import logging
import signal
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field

import zmq
import zmq.asyncio
from ase.calculators.calculator import Calculator

from aserpc.constants import (
    BUSY,
    DISCONNECT,
    HEARTBEAT_INTERVAL,
    IPC_BACKEND,
    IDLE_TIMEOUT,
    READY,
    RESPONSE,
    SHUTDOWN,
)
from aserpc.protocol import pack_response, unpack_request

log = logging.getLogger(__name__)


@dataclass
class Worker:
    """Calculator worker that connects to a broker.

    Attributes:
        name: Calculator name (must match what clients request)
        calculator_factory: Callable that returns a Calculator instance
        broker: ZMQ address of broker backend
        idle_timeout: Seconds of idle time before self-termination
        heartbeat_interval: Seconds between heartbeat/busy messages
    """

    name: str
    calculator_factory: Callable[[], Calculator]
    broker: str = IPC_BACKEND
    idle_timeout: float = IDLE_TIMEOUT
    heartbeat_interval: float = HEARTBEAT_INTERVAL

    # Internal state
    _ctx: zmq.asyncio.Context | None = field(default=None, init=False, repr=False)
    _socket: zmq.asyncio.Socket | None = field(default=None, init=False, repr=False)
    _calculator: Calculator | None = field(default=None, init=False, repr=False)
    _executor: ThreadPoolExecutor | None = field(default=None, init=False, repr=False)
    _running: bool = field(default=False, init=False, repr=False)
    _stop_event: asyncio.Event | None = field(default=None, init=False, repr=False)
    _last_activity: float = field(default=0.0, init=False, repr=False)
    _requests_handled: int = field(default=0, init=False, repr=False)

    @property
    def requests_handled(self) -> int:
        """Number of requests this worker has processed."""
        return self._requests_handled

    async def run(self) -> None:
        """Run the worker (blocking)."""
        self._setup_signal_handlers()

        self._ctx = zmq.asyncio.Context()
        self._socket = self._ctx.socket(zmq.DEALER)
        self._socket.connect(self.broker)
        self._stop_event = asyncio.Event()

        self._executor = ThreadPoolExecutor(max_workers=1)
        self._calculator = self.calculator_factory()
        self._running = True
        self._last_activity = time.time()

        log.info(f"Worker '{self.name}' started, connected to {self.broker}")

        # Send READY
        await self._send_ready()

        try:
            await self._main_loop()
        finally:
            # Send DISCONNECT to broker before cleanup
            await self._send_disconnect()
            self._cleanup()

    def stop(self) -> None:
        """Signal the worker to stop."""
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

        # Signal handlers only work in the main thread
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
            # Windows doesn't support add_signal_handler
            # ValueError can occur if called from wrong thread
            pass

    def _cleanup(self) -> None:
        """Clean up resources."""
        if self._executor:
            self._executor.shutdown(wait=False)
        if self._socket:
            self._socket.close(linger=0)
        if self._ctx:
            self._ctx.term()
        log.info(
            f"Worker '{self.name}' stopped after handling {self._requests_handled} requests"
        )

    async def _main_loop(self) -> None:
        """Main worker loop."""
        assert self._socket is not None  # Initialized in run()
        poller = zmq.asyncio.Poller()
        poller.register(self._socket, zmq.POLLIN)

        while self._running:
            # Check idle timeout
            idle_time = time.time() - self._last_activity
            if idle_time > self.idle_timeout:
                log.info(f"Idle timeout ({self.idle_timeout}s), shutting down")
                break

            # Poll with heartbeat timeout
            events = await poller.poll(timeout=int(self.heartbeat_interval * 1000))

            if events:
                msg = await self._socket.recv_multipart()
                await self._handle_message(msg)
            else:
                # No message - send READY (acts as heartbeat + re-registration)
                # Using READY instead of HEARTBEAT ensures re-registration after broker restart
                await self._send_ready()

    async def _handle_message(self, msg: list[bytes]) -> None:
        """Handle incoming message from broker."""
        # Message format: [empty, msg_type_or_client_id, ...]
        if len(msg) < 2:
            log.warning(f"Invalid message: {msg}")
            return

        # Check if it's a control message (SHUTDOWN)
        if len(msg) == 2 and msg[1] == SHUTDOWN:
            log.info("Received SHUTDOWN command")
            self._running = False
            return

        # Otherwise it's a request: [empty, client_id, request_data]
        if len(msg) >= 3:
            client_id = msg[1]
            request_data = msg[2]
            await self._process_request(client_id, request_data)

    async def _process_request(self, client_id: bytes, request_data: bytes) -> None:
        """Process a calculation request with heartbeats."""
        self._last_activity = time.time()

        log.debug(f"Processing request from {client_id.hex()[:8]}")

        # Run calculation in thread pool
        loop = asyncio.get_running_loop()
        compute_task = loop.run_in_executor(
            self._executor,
            self._compute_sync,
            request_data,
        )

        # Wait for completion, sending BUSY only if it takes long
        # First wait without BUSY (fast path for quick calculations)
        try:
            response_data = await asyncio.wait_for(
                asyncio.shield(compute_task),
                timeout=self.heartbeat_interval,
            )
        except asyncio.TimeoutError:
            # Computation is taking long - enter BUSY loop
            while not compute_task.done():
                await self._send_busy()
                try:
                    response_data = await asyncio.wait_for(
                        asyncio.shield(compute_task),
                        timeout=self.heartbeat_interval,
                    )
                    break
                except asyncio.TimeoutError:
                    continue
            else:
                response_data = compute_task.result()

        # Send response
        await self._send_response(client_id, response_data)

        self._requests_handled += 1
        self._last_activity = time.time()

        # Signal ready for next request
        await self._send_ready()

    def _compute_sync(self, request_data: bytes) -> bytes:
        """Synchronous calculation (runs in thread pool)."""
        assert self._calculator is not None  # Initialized in run()
        try:
            atoms, properties = unpack_request(request_data)
            atoms.calc = self._calculator

            results = {}
            for prop in properties:
                if prop == "energy":
                    results["energy"] = atoms.get_potential_energy()
                elif prop == "forces":
                    results["forces"] = atoms.get_forces()
                elif prop == "stress":
                    results["stress"] = atoms.get_stress()
                else:
                    # Try generic property access
                    try:
                        results[prop] = atoms.calc.results.get(prop)
                    except Exception:
                        pass

            return pack_response(results=results)

        except Exception as e:
            log.exception(f"Calculation failed: {e}")
            return pack_response(error=str(e))

    async def _send_ready(self) -> None:
        """Send READY message to broker."""
        assert self._socket is not None
        await self._socket.send_multipart([b"", READY, self.name.encode()])

    async def _send_busy(self) -> None:
        """Send BUSY message to broker."""
        assert self._socket is not None
        await self._socket.send_multipart([b"", BUSY, self.name.encode()])

    async def _send_response(self, client_id: bytes, response_data: bytes) -> None:
        """Send response back through broker."""
        assert self._socket is not None
        await self._socket.send_multipart([b"", RESPONSE, client_id, response_data])

    async def _send_disconnect(self) -> None:
        """Send DISCONNECT message to broker (deregister before shutdown)."""
        if self._socket is None:
            return
        try:
            await self._socket.send_multipart([b"", DISCONNECT, self.name.encode()])
            log.debug(f"Sent DISCONNECT for '{self.name}'")
        except Exception as e:
            log.warning(f"Failed to send DISCONNECT: {e}")
