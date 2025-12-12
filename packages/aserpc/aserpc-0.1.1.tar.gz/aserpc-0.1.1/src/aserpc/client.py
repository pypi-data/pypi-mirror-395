"""Client - ASE-compatible RemoteCalculator.

Usage:
    from aserpc import RemoteCalculator
    from ase.build import bulk

    calc = RemoteCalculator("lj")
    atoms = bulk("Cu")
    atoms.calc = calc
    energy = atoms.get_potential_energy()
"""

import logging

import msgspec
import zmq
from ase.calculators.calculator import Calculator, all_changes

from aserpc.constants import (
    CLIENT_TIMEOUT_MS,
    ERROR,
    IPC_FRONTEND,
    LIST,
    REQUEST,
    RESPONSE,
    STATUS,
    WORKER_SHUTDOWN,
)
from aserpc.protocol import pack_request, unpack_response

log = logging.getLogger(__name__)


class RemoteCalculator(Calculator):
    """ASE Calculator that delegates to remote workers.

    Args:
        calc_name: Calculator name (must match a registered worker)
        broker: ZMQ address of broker frontend
        timeout: Request timeout in milliseconds
        check_broker: If True, verify broker is reachable on init (default: True)

    Raises:
        ConnectionError: If broker is not reachable and check_broker is True

    Note:
        This class is NOT thread-safe. Each thread should create its own
        RemoteCalculator instance. For concurrent calculations, use separate
        instances or external synchronization.
    """

    implemented_properties = ["energy", "forces", "stress"]

    def __init__(
        self,
        calc_name: str,
        broker: str = IPC_FRONTEND,
        timeout: int = CLIENT_TIMEOUT_MS,
        check_broker: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.calc_name = calc_name
        self.broker = broker
        self.timeout = timeout

        self._ctx: zmq.Context | None = None
        self._socket: zmq.Socket | None = None

        if check_broker:
            self._verify_broker()

    def _ensure_connected(self) -> None:
        """Ensure socket is connected (lazy initialization)."""
        if self._socket is None:
            self._ctx = zmq.Context()
            self._socket = self._ctx.socket(zmq.REQ)
            self._socket.setsockopt(zmq.RCVTIMEO, self.timeout)
            self._socket.setsockopt(zmq.SNDTIMEO, self.timeout)
            self._socket.setsockopt(zmq.LINGER, 0)
            self._socket.connect(self.broker)

    def _reset_socket(self) -> None:
        """Reset socket after error (REQ socket can get stuck)."""
        if self._socket:
            self._socket.close(linger=0)
        if self._ctx is None:
            self._ctx = zmq.Context()
        self._socket = self._ctx.socket(zmq.REQ)
        self._socket.setsockopt(zmq.RCVTIMEO, self.timeout)
        self._socket.setsockopt(zmq.SNDTIMEO, self.timeout)
        self._socket.setsockopt(zmq.LINGER, 0)
        self._socket.connect(self.broker)

    def _verify_broker(self, timeout_ms: int = 2000) -> None:
        """Verify broker is reachable by sending a LIST request.

        Args:
            timeout_ms: Timeout for the check in milliseconds

        Raises:
            ConnectionError: If broker is not reachable
        """
        ctx = zmq.Context()
        sock = ctx.socket(zmq.REQ)
        sock.setsockopt(zmq.RCVTIMEO, timeout_ms)
        sock.setsockopt(zmq.SNDTIMEO, timeout_ms)
        sock.setsockopt(zmq.LINGER, 0)
        sock.connect(self.broker)

        try:
            sock.send_multipart([LIST])
            msg = sock.recv_multipart()
            if len(msg) < 2 or msg[0] != RESPONSE:
                raise ConnectionError(f"Invalid response from broker: {msg}")
        except zmq.Again:
            raise ConnectionError(
                f"Broker not reachable at {self.broker} (timeout: {timeout_ms}ms)"
            )
        finally:
            sock.close(linger=0)
            ctx.term()

    def calculate(
        self,
        atoms=None,
        properties=None,
        system_changes=all_changes,
    ) -> None:
        """Perform calculation via remote worker."""
        if properties is None:
            properties = self.implemented_properties

        # Standard ASE calculator setup
        Calculator.calculate(self, atoms, properties, system_changes)

        self._ensure_connected()

        # Pack and send request
        request_data = pack_request(atoms, properties)

        try:
            self._socket.send_multipart(
                [REQUEST, self.calc_name.encode(), request_data]
            )
        except zmq.Again:
            self._reset_socket()
            raise TimeoutError(f"Send timeout ({self.timeout}ms)")

        # Receive response
        try:
            msg = self._socket.recv_multipart()
        except zmq.Again:
            self._reset_socket()
            raise TimeoutError(f"Receive timeout ({self.timeout}ms)")

        # Parse response
        if len(msg) < 2:
            raise RuntimeError(f"Invalid response: {msg}")

        msg_type, response_data = msg[0], msg[1]

        if msg_type == ERROR:
            # Error response
            results = unpack_response(response_data, n_atoms=len(atoms))
            # unpack_response raises RuntimeError for errors
        elif msg_type == RESPONSE:
            # Success response
            results = unpack_response(response_data, n_atoms=len(atoms))
        else:
            raise RuntimeError(f"Unexpected response type: {msg_type}")

        # Store results
        self.results = results

    def __del__(self) -> None:
        """Clean up socket on deletion."""
        if hasattr(self, "_socket") and self._socket:
            self._socket.close(linger=0)
        if hasattr(self, "_ctx") and self._ctx:
            self._ctx.term()


# =============================================================================
# Helper functions
# =============================================================================


def list_calculators(broker: str = IPC_FRONTEND, timeout: int = 5000) -> dict[str, int]:
    """List available calculators and their worker counts.

    Args:
        broker: ZMQ address of broker frontend
        timeout: Timeout in milliseconds

    Returns:
        Dict mapping calculator names to worker counts
    """
    ctx = zmq.Context()
    sock = ctx.socket(zmq.REQ)
    sock.setsockopt(zmq.RCVTIMEO, timeout)
    sock.setsockopt(zmq.SNDTIMEO, timeout)
    sock.setsockopt(zmq.LINGER, 0)
    sock.connect(broker)

    try:
        sock.send_multipart([LIST])
        msg = sock.recv_multipart()

        if len(msg) >= 2 and msg[0] == RESPONSE:
            return msgspec.msgpack.decode(msg[1])
        else:
            raise RuntimeError(f"Unexpected response: {msg}")
    except zmq.Again:
        raise TimeoutError(f"Timeout ({timeout}ms)")
    finally:
        sock.close(linger=0)
        ctx.term()


def broker_status(broker: str = IPC_FRONTEND, timeout: int = 5000) -> dict:
    """Get broker status.

    Args:
        broker: ZMQ address of broker frontend
        timeout: Timeout in milliseconds

    Returns:
        Status dict with worker and queue information
    """
    ctx = zmq.Context()
    sock = ctx.socket(zmq.REQ)
    sock.setsockopt(zmq.RCVTIMEO, timeout)
    sock.setsockopt(zmq.SNDTIMEO, timeout)
    sock.setsockopt(zmq.LINGER, 0)
    sock.connect(broker)

    try:
        sock.send_multipart([STATUS])
        msg = sock.recv_multipart()

        if len(msg) >= 2 and msg[0] == RESPONSE:
            return msgspec.msgpack.decode(msg[1])
        else:
            raise RuntimeError(f"Unexpected response: {msg}")
    except zmq.Again:
        raise TimeoutError(f"Timeout ({timeout}ms)")
    finally:
        sock.close(linger=0)
        ctx.term()


def shutdown_workers(
    calc_name: str,
    broker: str = IPC_FRONTEND,
    timeout: int = 5000,
) -> int:
    """Shutdown workers for a specific calculator.

    Args:
        calc_name: Calculator name
        broker: ZMQ address of broker frontend
        timeout: Timeout in milliseconds

    Returns:
        Number of workers shutdown
    """
    ctx = zmq.Context()
    sock = ctx.socket(zmq.REQ)
    sock.setsockopt(zmq.RCVTIMEO, timeout)
    sock.setsockopt(zmq.SNDTIMEO, timeout)
    sock.setsockopt(zmq.LINGER, 0)
    sock.connect(broker)

    try:
        sock.send_multipart([WORKER_SHUTDOWN, calc_name.encode()])
        msg = sock.recv_multipart()

        if len(msg) >= 2 and msg[0] == RESPONSE:
            result = msgspec.msgpack.decode(msg[1])
            return result.get("shutdown_count", 0)
        else:
            raise RuntimeError(f"Unexpected response: {msg}")
    except zmq.Again:
        raise TimeoutError(f"Timeout ({timeout}ms)")
    finally:
        sock.close(linger=0)
        ctx.term()
