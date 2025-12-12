"""Wire protocol for aserpc.

Uses msgspec.Struct with array_like=True for maximum performance:
- No field names on wire (compact encoding)
- Zero-copy where possible
- Type validation at decode time
"""

from typing import Any

import msgspec
import numpy as np
from ase import Atoms

from aserpc.constants import PROTOCOL_VERSION


# =============================================================================
# Wire format structs (msgspec.Struct for performance)
# =============================================================================


class Request(msgspec.Struct, array_like=True, frozen=True):
    """Calculator request on the wire.

    Fields are encoded as an array (no field names) for compactness.
    All numpy arrays are serialized as raw bytes.
    """

    v: int  # Protocol version
    numbers: bytes  # Atomic numbers as int32
    positions: bytes  # Positions as float64 Nx3
    cell: bytes  # Unit cell as float64 3x3
    pbc: bytes  # Periodic boundaries as bool[3]
    properties: tuple[str, ...]  # Properties to compute


class Response(msgspec.Struct, array_like=True, frozen=True):
    """Calculator response on the wire.

    Results dict contains:
    - energy: float
    - forces: bytes (float64 Nx3)
    - stress: bytes (float64 6)
    - ... any other calculator properties
    """

    v: int  # Protocol version
    success: bool
    results: dict[str, Any]  # Calculator results
    error: str | None = None  # Error message if success=False


# =============================================================================
# Reusable encoder/decoder instances (create once, reuse)
# =============================================================================

_encoder = msgspec.msgpack.Encoder()
_request_decoder = msgspec.msgpack.Decoder(Request)
_response_decoder = msgspec.msgpack.Decoder(Response)


# =============================================================================
# Pack/unpack functions
# =============================================================================


def pack_request(atoms: Atoms, properties: list[str]) -> bytes:
    """Pack Atoms and properties into wire format.

    Args:
        atoms: ASE Atoms object
        properties: List of properties to compute (e.g., ["energy", "forces"])

    Returns:
        Msgpack-encoded bytes
    """
    request = Request(
        v=PROTOCOL_VERSION,
        numbers=np.asarray(atoms.numbers, dtype=np.int32).tobytes(),
        positions=np.asarray(atoms.positions, dtype=np.float64).tobytes(),
        cell=np.asarray(atoms.cell, dtype=np.float64).tobytes(),
        pbc=np.asarray(atoms.pbc, dtype=np.bool_).tobytes(),
        properties=tuple(properties),
    )
    return _encoder.encode(request)


def unpack_request(data: bytes) -> tuple[Atoms, list[str]]:
    """Unpack wire format into Atoms and properties.

    Args:
        data: Msgpack-encoded request bytes

    Returns:
        Tuple of (Atoms, properties list)
    """
    request = _request_decoder.decode(data)

    if request.v != PROTOCOL_VERSION:
        raise ValueError(
            f"Protocol version mismatch: got {request.v}, expected {PROTOCOL_VERSION}"
        )

    # Reconstruct numpy arrays from bytes (zero-copy where possible)
    numbers = np.frombuffer(request.numbers, dtype=np.int32)
    n_atoms = len(numbers)

    positions = np.frombuffer(request.positions, dtype=np.float64).reshape(n_atoms, 3)
    cell = np.frombuffer(request.cell, dtype=np.float64).reshape(3, 3)
    pbc = np.frombuffer(request.pbc, dtype=np.bool_)

    # Create Atoms object
    atoms = Atoms(
        numbers=numbers.copy(),  # Copy to make writable
        positions=positions.copy(),
        cell=cell.copy(),
        pbc=pbc.copy(),
    )

    return atoms, list(request.properties)


def pack_response(
    results: dict[str, Any] | None = None,
    error: str | None = None,
) -> bytes:
    """Pack calculator results or error into wire format.

    Args:
        results: Calculator results dict (energy, forces, stress, etc.)
        error: Error message if calculation failed

    Returns:
        Msgpack-encoded bytes
    """
    if error is not None:
        response = Response(
            v=PROTOCOL_VERSION,
            success=False,
            results={},
            error=error,
        )
    else:
        # Convert numpy types to Python natives or bytes
        packed_results = {}
        for key, value in (results or {}).items():
            if isinstance(value, np.ndarray):
                packed_results[key] = value.astype(np.float64).tobytes()
            elif isinstance(value, (np.floating, np.integer)):
                # Convert numpy scalars to Python natives
                packed_results[key] = value.item()
            else:
                packed_results[key] = value

        response = Response(
            v=PROTOCOL_VERSION,
            success=True,
            results=packed_results,
            error=None,
        )

    return _encoder.encode(response)


def unpack_response(data: bytes, n_atoms: int | None = None) -> dict[str, Any]:
    """Unpack wire format into results dict.

    Args:
        data: Msgpack-encoded response bytes
        n_atoms: Number of atoms (needed to reshape forces array)

    Returns:
        Results dict with numpy arrays reconstructed

    Raises:
        RuntimeError: If response indicates an error
    """
    response = _response_decoder.decode(data)

    if response.v != PROTOCOL_VERSION:
        raise ValueError(
            f"Protocol version mismatch: got {response.v}, expected {PROTOCOL_VERSION}"
        )

    if not response.success:
        raise RuntimeError(response.error or "Unknown error")

    # Reconstruct numpy arrays from bytes
    results = {}
    for key, value in response.results.items():
        if isinstance(value, bytes):
            arr = np.frombuffer(value, dtype=np.float64)
            # Reshape based on key
            if key == "forces" and n_atoms is not None:
                arr = arr.reshape(n_atoms, 3).copy()
            elif key == "stress":
                arr = arr.copy()  # Already 1D (6,)
            else:
                arr = arr.copy()
            results[key] = arr
        else:
            results[key] = value

    return results


# =============================================================================
# Utility functions
# =============================================================================


def get_request_info(data: bytes) -> dict[str, Any]:
    """Extract metadata from request without full decode.

    Useful for logging/debugging.
    """
    request = _request_decoder.decode(data)
    numbers = np.frombuffer(request.numbers, dtype=np.int32)
    return {
        "version": request.v,
        "n_atoms": len(numbers),
        "properties": list(request.properties),
    }
