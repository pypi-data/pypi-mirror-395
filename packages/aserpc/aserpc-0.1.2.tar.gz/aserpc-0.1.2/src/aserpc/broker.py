"""Broker - routes requests between clients and workers.

Architecture:
    Frontend (ROUTER) <-- clients send requests
        |
        v
      Broker (async event loop)
        |
        v
    Backend (ROUTER) <-- workers connect
"""

import asyncio
import logging
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from pathlib import Path

import msgspec
import zmq
import zmq.asyncio

from aserpc.constants import (
    BUSY,
    DISCONNECT,
    ERROR,
    HEARTBEAT,
    IPC_BACKEND,
    IPC_FRONTEND,
    LIST,
    MANAGER_HEARTBEAT,
    MANAGER_READY,
    MESSAGE_NAMES,
    READY,
    REQUEST,
    REQUEST_QUEUE_TIMEOUT,
    RESPONSE,
    SHUTDOWN,
    SPAWN_REQUEST,
    SPAWN_RESPONSE,
    STATUS,
    WORKER_SHUTDOWN,
    WORKER_TIMEOUT,
)
from aserpc.protocol import pack_response

log = logging.getLogger(__name__)


@dataclass
class WorkerState:
    """Tracks state of a connected worker."""

    worker_id: bytes
    calc_name: str
    last_seen: float
    busy: bool = False


@dataclass
class PendingRequest:
    """A queued client request waiting for a worker."""

    client_id: bytes
    request_data: bytes
    timestamp: float


@dataclass
class Broker:
    """Message broker for routing calculator requests.

    Attributes:
        frontend: ZMQ address for client connections
        backend: ZMQ address for worker connections
        worker_timeout: Seconds before considering worker dead
        request_queue_timeout: Seconds before queued request expires
    """

    frontend: str = IPC_FRONTEND
    backend: str = IPC_BACKEND
    worker_timeout: float = WORKER_TIMEOUT
    request_queue_timeout: float = REQUEST_QUEUE_TIMEOUT

    # Internal state (initialized in run())
    _ctx: zmq.asyncio.Context | None = field(default=None, init=False, repr=False)
    _frontend_sock: zmq.asyncio.Socket | None = field(
        default=None, init=False, repr=False
    )
    _backend_sock: zmq.asyncio.Socket | None = field(
        default=None, init=False, repr=False
    )
    _running: bool = field(default=False, init=False, repr=False)
    _stop_event: asyncio.Event | None = field(default=None, init=False, repr=False)

    # Worker tracking: {worker_id: WorkerState}
    _workers: dict[bytes, WorkerState] = field(
        default_factory=dict, init=False, repr=False
    )

    # Per-calculator idle worker queues: {calc_name: deque[worker_id]}
    _idle_workers: dict[str, deque[bytes]] = field(
        default_factory=lambda: defaultdict(deque), init=False, repr=False
    )

    # Pending requests: {calc_name: deque[PendingRequest]}
    _pending: dict[str, deque[PendingRequest]] = field(
        default_factory=lambda: defaultdict(deque), init=False, repr=False
    )

    # Request routing: {worker_id: client_id} for in-flight requests
    _in_flight: dict[bytes, bytes] = field(default_factory=dict, init=False, repr=False)

    # Manager tracking for scale-to-zero
    _manager_id: bytes | None = field(default=None, init=False, repr=False)
    _manager_last_seen: float = field(default=0.0, init=False, repr=False)
    _spawn_requested: set[str] = field(default_factory=set, init=False, repr=False)

    async def run(self) -> None:
        """Run the broker (blocking)."""
        self._ensure_ipc_dir()
        self._ctx = zmq.asyncio.Context()
        self._stop_event = asyncio.Event()

        self._frontend_sock = self._ctx.socket(zmq.ROUTER)
        self._backend_sock = self._ctx.socket(zmq.ROUTER)

        self._frontend_sock.bind(self.frontend)
        self._backend_sock.bind(self.backend)

        log.info(f"Broker started: frontend={self.frontend}, backend={self.backend}")

        self._running = True

        try:
            await asyncio.gather(
                self._main_loop(),
                self._monitor_workers(),
                self._expire_pending_requests(),
            )
        finally:
            self._cleanup()

    async def _main_loop(self) -> None:
        """Main loop using single poller for both sockets (low latency)."""
        poller = zmq.asyncio.Poller()
        poller.register(self._frontend_sock, zmq.POLLIN)
        poller.register(self._backend_sock, zmq.POLLIN)

        while self._running:
            # Poll both sockets with short timeout
            events = dict(await poller.poll(timeout=100))  # 100ms

            if self._frontend_sock in events:
                msg = await self._frontend_sock.recv_multipart()
                await self._process_frontend_message(msg)

            if self._backend_sock in events:
                msg = await self._backend_sock.recv_multipart()
                await self._process_backend_message(msg)

    def stop(self) -> None:
        """Signal the broker to stop."""
        self._running = False
        # Thread-safe way to set the event if stop() is called from another thread
        if self._stop_event and not self._stop_event.is_set():
            try:
                loop = asyncio.get_running_loop()
                loop.call_soon_threadsafe(self._stop_event.set)
            except RuntimeError:
                # No running loop in this thread, try to set directly
                # (works if called from the broker's own thread)
                self._stop_event.set()

    async def _sleep_interruptible(self, duration: float) -> bool:
        """Sleep for duration but wake early if stop is signaled.

        Returns True if woke due to stop signal, False if timed out.
        """
        try:
            await asyncio.wait_for(self._stop_event.wait(), timeout=duration)
            return True  # Stop was signaled
        except asyncio.TimeoutError:
            return False  # Normal timeout

    def _ensure_ipc_dir(self) -> None:
        """Ensure IPC socket directory exists."""
        for addr in [self.frontend, self.backend]:
            if addr.startswith("ipc://"):
                path = Path(addr.replace("ipc://", ""))
                path.parent.mkdir(parents=True, exist_ok=True)

    def _cleanup(self) -> None:
        """Clean up sockets, context, and IPC files."""
        if self._frontend_sock:
            self._frontend_sock.close(linger=0)
        if self._backend_sock:
            self._backend_sock.close(linger=0)
        if self._ctx:
            self._ctx.term()

        # Clean up IPC socket files
        ipc_dirs: set[Path] = set()
        for addr in [self.frontend, self.backend]:
            if addr.startswith("ipc://"):
                ipc_path = Path(addr.replace("ipc://", ""))
                ipc_dirs.add(ipc_path.parent)
                try:
                    ipc_path.unlink(missing_ok=True)
                except OSError:
                    pass  # Ignore errors during cleanup

        # Remove IPC directory if empty
        for ipc_dir in ipc_dirs:
            try:
                ipc_dir.rmdir()  # Only removes if empty
            except OSError:
                pass  # Directory not empty or other error

        log.info("Broker stopped")

    # =========================================================================
    # Frontend handling (clients)
    # =========================================================================

    async def _process_frontend_message(self, msg: list[bytes]) -> None:
        """Process a message from a client."""
        # Message format: [client_id, empty, msg_type, ...]
        if len(msg) < 3:
            log.warning(f"Invalid frontend message: {msg}")
            return

        client_id, _, msg_type = msg[0], msg[1], msg[2]
        log.debug(
            f"Frontend: {MESSAGE_NAMES.get(msg_type, msg_type)} from {client_id.hex()[:8]}"
        )

        if msg_type == REQUEST:
            await self._handle_request(client_id, msg)
        elif msg_type == LIST:
            await self._handle_list(client_id)
        elif msg_type == STATUS:
            await self._handle_status(client_id)
        elif msg_type == SHUTDOWN:
            await self._handle_shutdown()
        elif msg_type == WORKER_SHUTDOWN:
            await self._handle_worker_shutdown(client_id, msg)
        else:
            log.warning(f"Unknown frontend message type: {msg_type}")

    async def _handle_request(self, client_id: bytes, msg: list[bytes]) -> None:
        """Route a calculation request to a worker."""
        # Message: [client_id, empty, REQUEST, calc_name, request_data]
        if len(msg) < 5:
            await self._send_error(client_id, "Invalid request format")
            return

        calc_name = msg[3].decode()
        request_data = msg[4]

        # Find an idle worker for this calculator
        worker_id = self._pop_idle_worker(calc_name)

        if worker_id:
            # Route to worker
            await self._route_to_worker(worker_id, client_id, calc_name, request_data)
        elif self._has_workers_for(calc_name):
            # Workers exist but all busy - queue request
            self._queue_request(client_id, calc_name, request_data)
            log.debug(
                f"Queued request for {calc_name}, queue depth: {len(self._pending[calc_name])}"
            )
        else:
            # No workers registered for this calculator
            if self._manager_id is not None:
                # Manager available - queue request and request spawn
                self._queue_request(client_id, calc_name, request_data)
                if calc_name not in self._spawn_requested:
                    await self._request_spawn(calc_name)
                log.debug(
                    f"Queued request for {calc_name} (spawn requested), "
                    f"queue depth: {len(self._pending[calc_name])}"
                )
            else:
                # No manager - immediate error
                await self._send_error(
                    client_id, f"No workers available for calculator '{calc_name}'"
                )

    async def _route_to_worker(
        self,
        worker_id: bytes,
        client_id: bytes,
        calc_name: str,
        request_data: bytes,
    ) -> None:
        """Send request to a specific worker."""
        # Track in-flight request
        self._in_flight[worker_id] = client_id

        # Mark worker as busy
        if worker_id in self._workers:
            self._workers[worker_id].busy = True

        # Send to worker: [worker_id, empty, client_id, request_data]
        await self._backend_sock.send_multipart(
            [
                worker_id,
                b"",
                client_id,
                request_data,
            ]
        )

        log.debug(f"Routed request to worker {worker_id.hex()[:8]} for {calc_name}")

    async def _handle_list(self, client_id: bytes) -> None:
        """Return list of available calculators."""
        # Count workers per calculator
        calc_counts = {}
        for worker in self._workers.values():
            calc_counts[worker.calc_name] = calc_counts.get(worker.calc_name, 0) + 1

        data = msgspec.msgpack.encode(calc_counts)
        await self._frontend_sock.send_multipart([client_id, b"", RESPONSE, data])

    async def _handle_status(self, client_id: bytes) -> None:
        """Return broker status."""
        status = {
            "workers": {
                calc: {
                    "total": sum(
                        1 for w in self._workers.values() if w.calc_name == calc
                    ),
                    "idle": len(self._idle_workers[calc]),
                    "busy": sum(
                        1
                        for w in self._workers.values()
                        if w.calc_name == calc and w.busy
                    ),
                }
                for calc in set(w.calc_name for w in self._workers.values())
            },
            "pending_requests": {
                calc: len(queue) for calc, queue in self._pending.items() if queue
            },
        }

        data = msgspec.msgpack.encode(status)
        await self._frontend_sock.send_multipart([client_id, b"", RESPONSE, data])

    async def _handle_shutdown(self) -> None:
        """Shutdown the broker."""
        log.info("Shutdown requested")

        # Send shutdown to all workers
        for worker_id in list(self._workers.keys()):
            await self._backend_sock.send_multipart([worker_id, b"", SHUTDOWN])

        self._running = False

    async def _handle_worker_shutdown(self, client_id: bytes, msg: list[bytes]) -> None:
        """Shutdown workers for a specific calculator."""
        if len(msg) < 4:
            await self._send_error(client_id, "Missing calculator name")
            return

        calc_name = msg[3].decode()
        count = 0

        for worker_id, state in list(self._workers.items()):
            if state.calc_name == calc_name:
                await self._backend_sock.send_multipart([worker_id, b"", SHUTDOWN])
                count += 1

        data = msgspec.msgpack.encode({"shutdown_count": count})
        await self._frontend_sock.send_multipart([client_id, b"", RESPONSE, data])

    async def _send_error(self, client_id: bytes, error_msg: str) -> None:
        """Send error response to client."""
        data = pack_response(error=error_msg)
        await self._frontend_sock.send_multipart([client_id, b"", ERROR, data])

    # =========================================================================
    # Backend handling (workers)
    # =========================================================================

    async def _process_backend_message(self, msg: list[bytes]) -> None:
        """Process a message from a worker."""
        # Message format: [worker_id, empty, msg_type, ...]
        if len(msg) < 3:
            log.warning(f"Invalid backend message: {msg}")
            return

        worker_id, _, msg_type = msg[0], msg[1], msg[2]
        log.debug(
            f"Backend: {MESSAGE_NAMES.get(msg_type, msg_type)} from {worker_id.hex()[:8]}"
        )

        if msg_type == READY:
            await self._handle_worker_ready(worker_id, msg)
        elif msg_type == HEARTBEAT:
            self._handle_worker_heartbeat(worker_id)
        elif msg_type == BUSY:
            self._handle_worker_busy(worker_id)
        elif msg_type == RESPONSE:
            await self._handle_worker_response(worker_id, msg)
        elif msg_type == DISCONNECT:
            await self._handle_worker_disconnect(worker_id, msg)
        elif msg_type == MANAGER_READY:
            await self._handle_manager_ready(worker_id, msg)
        elif msg_type == MANAGER_HEARTBEAT:
            self._handle_manager_heartbeat(worker_id)
        elif msg_type == SPAWN_RESPONSE:
            await self._handle_spawn_response(worker_id, msg)
        else:
            log.warning(f"Unknown backend message type: {msg_type}")

    async def _handle_worker_ready(self, worker_id: bytes, msg: list[bytes]) -> None:
        """Register a new/returning worker."""
        if len(msg) < 4:
            log.warning("READY message missing calculator name")
            return

        calc_name = msg[3].decode()
        now = time.time()

        # Clear spawn request flag since a worker is now available
        self._spawn_requested.discard(calc_name)

        # Register or update worker
        if worker_id not in self._workers:
            self._workers[worker_id] = WorkerState(
                worker_id=worker_id,
                calc_name=calc_name,
                last_seen=now,
            )
            log.info(f"Worker {worker_id.hex()[:8]} registered for '{calc_name}'")
        else:
            self._workers[worker_id].last_seen = now
            self._workers[worker_id].busy = False

        # Check for pending requests
        if self._pending[calc_name]:
            pending = self._pending[calc_name].popleft()
            await self._route_to_worker(
                worker_id,
                pending.client_id,
                calc_name,
                pending.request_data,
            )
        else:
            # Add to idle queue
            self._add_idle_worker(calc_name, worker_id)

    def _handle_worker_heartbeat(self, worker_id: bytes) -> None:
        """Update worker last-seen time."""
        if worker_id in self._workers:
            self._workers[worker_id].last_seen = time.time()

    def _handle_worker_busy(self, worker_id: bytes) -> None:
        """Worker is busy but alive."""
        if worker_id in self._workers:
            self._workers[worker_id].last_seen = time.time()
            self._workers[worker_id].busy = True

    async def _handle_worker_disconnect(
        self, worker_id: bytes, msg: list[bytes]
    ) -> None:
        """Handle worker graceful disconnect."""
        if worker_id not in self._workers:
            return

        state = self._workers.pop(worker_id)
        log.info(f"Worker {worker_id.hex()[:8]} disconnected (calc={state.calc_name})")

        # Remove from idle queue
        queue = self._idle_workers.get(state.calc_name)
        if queue and worker_id in queue:
            queue.remove(worker_id)

        # Handle any in-flight request (shouldn't happen on graceful disconnect)
        client_id = self._in_flight.pop(worker_id, None)
        if client_id:
            log.warning("Worker disconnected with in-flight request")
            await self._send_error(client_id, "Worker disconnected during calculation")

    async def _handle_worker_response(self, worker_id: bytes, msg: list[bytes]) -> None:
        """Forward response to client, mark worker idle."""
        if len(msg) < 5:
            log.warning("RESPONSE message missing data")
            return

        # Message: [worker_id, empty, RESPONSE, client_id, response_data]
        client_id = msg[3]
        response_data = msg[4]

        # Forward to client
        await self._frontend_sock.send_multipart(
            [client_id, b"", RESPONSE, response_data]
        )

        # Remove from in-flight
        self._in_flight.pop(worker_id, None)

        # Mark worker as ready
        if worker_id in self._workers:
            state = self._workers[worker_id]
            state.last_seen = time.time()
            state.busy = False

            # Check for pending requests
            if self._pending[state.calc_name]:
                pending = self._pending[state.calc_name].popleft()
                await self._route_to_worker(
                    worker_id,
                    pending.client_id,
                    state.calc_name,
                    pending.request_data,
                )
            else:
                self._add_idle_worker(state.calc_name, worker_id)

    # =========================================================================
    # Worker queue management
    # =========================================================================

    def _add_idle_worker(self, calc_name: str, worker_id: bytes) -> None:
        """Add worker to idle queue (LRU: append to end)."""
        queue = self._idle_workers[calc_name]
        if worker_id not in queue:
            queue.append(worker_id)

    def _pop_idle_worker(self, calc_name: str) -> bytes | None:
        """Pop least-recently-used worker from idle queue."""
        queue = self._idle_workers.get(calc_name)
        if not queue:
            return None

        while queue:
            worker_id = queue.popleft()
            # Verify worker is still registered and not dead
            if worker_id in self._workers:
                return worker_id

        return None

    def _has_workers_for(self, calc_name: str) -> bool:
        """Check if any workers are registered for this calculator."""
        return any(w.calc_name == calc_name for w in self._workers.values())

    def _queue_request(
        self, client_id: bytes, calc_name: str, request_data: bytes
    ) -> None:
        """Queue a request for when a worker becomes available."""
        self._pending[calc_name].append(
            PendingRequest(
                client_id=client_id,
                request_data=request_data,
                timestamp=time.time(),
            )
        )

    # =========================================================================
    # Background tasks
    # =========================================================================

    async def _monitor_workers(self) -> None:
        """Periodically check for dead workers and manager."""
        while self._running:
            if await self._sleep_interruptible(self.worker_timeout / 2):
                break  # Stop signaled

            now = time.time()
            dead_workers = []

            for worker_id, state in list(self._workers.items()):
                if now - state.last_seen > self.worker_timeout:
                    dead_workers.append(worker_id)

            for worker_id in dead_workers:
                state = self._workers.pop(worker_id)
                log.warning(
                    f"Worker {worker_id.hex()[:8]} timed out (calc={state.calc_name})"
                )

                # Remove from idle queue
                queue = self._idle_workers.get(state.calc_name)
                if queue and worker_id in queue:
                    queue.remove(worker_id)

                # Handle in-flight request
                client_id = self._in_flight.pop(worker_id, None)
                if client_id:
                    # Re-queue or error
                    log.warning(
                        "Worker died with in-flight request, sending error to client"
                    )
                    await self._send_error(client_id, "Worker died during calculation")

            # Check manager liveness
            if self._manager_id is not None:
                if now - self._manager_last_seen > self.worker_timeout:
                    log.warning(
                        f"Manager {self._manager_id.hex()[:8]} timed out, "
                        "clearing manager state"
                    )
                    self._manager_id = None
                    self._manager_last_seen = 0.0
                    self._spawn_requested.clear()

    async def _expire_pending_requests(self) -> None:
        """Periodically expire old pending requests."""
        while self._running:
            if await self._sleep_interruptible(5.0):
                break  # Stop signaled

            now = time.time()

            for calc_name, queue in list(self._pending.items()):
                while queue:
                    oldest = queue[0]
                    if now - oldest.timestamp > self.request_queue_timeout:
                        expired = queue.popleft()
                        log.warning(f"Request expired for {calc_name}")
                        await self._send_error(
                            expired.client_id,
                            f"Request timed out waiting for '{calc_name}' worker",
                        )
                    else:
                        break

    # =========================================================================
    # Manager handling (scale-to-zero)
    # =========================================================================

    async def _handle_manager_ready(self, manager_id: bytes, msg: list[bytes]) -> None:
        """Register infrastructure manager."""
        if self._manager_id is not None and self._manager_id != manager_id:
            log.warning(
                f"Replacing existing manager {self._manager_id.hex()[:8]} "
                f"with {manager_id.hex()[:8]}"
            )
            # Clear spawn state from old manager
            self._spawn_requested.clear()

        self._manager_id = manager_id
        self._manager_last_seen = time.time()

        # Parse available calculators if provided
        calc_names = ""
        if len(msg) >= 4:
            calc_names = msg[3].decode()

        log.info(
            f"Manager {manager_id.hex()[:8]} connected "
            f"(calculators: {calc_names or 'none'})"
        )

    def _handle_manager_heartbeat(self, manager_id: bytes) -> None:
        """Update manager last-seen time."""
        if manager_id == self._manager_id:
            self._manager_last_seen = time.time()

    async def _handle_spawn_response(self, manager_id: bytes, msg: list[bytes]) -> None:
        """Handle spawn response from manager."""
        if len(msg) < 5:
            log.warning("SPAWN_RESPONSE missing fields")
            return

        calc_name = msg[3].decode()
        status = msg[4].decode()

        if status == "ok":
            log.debug(f"Spawn succeeded for '{calc_name}'")
        else:
            error_msg = msg[5].decode() if len(msg) > 5 else "unknown"
            log.warning(f"Spawn failed for '{calc_name}': {error_msg}")
            # Clear spawn requested flag so we can retry
            self._spawn_requested.discard(calc_name)
            # Fail all pending requests immediately instead of waiting for timeout
            await self._expire_pending_for_calc(
                calc_name, f"Failed to spawn worker: {error_msg}"
            )

    async def _request_spawn(self, calc_name: str) -> None:
        """Ask manager to spawn a worker."""
        if self._manager_id is None:
            return

        self._spawn_requested.add(calc_name)
        await self._backend_sock.send_multipart(
            [self._manager_id, b"", SPAWN_REQUEST, calc_name.encode()]
        )
        log.info(f"Requested spawn for calculator '{calc_name}'")

    async def _expire_pending_for_calc(self, calc_name: str, error_msg: str) -> None:
        """Expire all pending requests for a calculator with an error."""
        queue = self._pending.get(calc_name)
        if not queue:
            return

        count = len(queue)
        while queue:
            pending = queue.popleft()
            await self._send_error(pending.client_id, error_msg)

        log.warning(
            f"Expired {count} pending request(s) for '{calc_name}': {error_msg}"
        )
