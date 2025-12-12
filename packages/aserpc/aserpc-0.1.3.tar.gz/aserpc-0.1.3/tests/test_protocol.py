"""Tests for aserpc protocol layer."""

import numpy as np
import numpy.testing as npt
import pytest
from ase import Atoms
from ase.build import bulk, molecule

from aserpc.protocol import (
    pack_request,
    pack_response,
    unpack_request,
    unpack_response,
    get_request_info,
)


# =============================================================================
# Request roundtrip tests
# =============================================================================


def test_request_roundtrip_water():
    """Request roundtrip preserves water molecule."""
    atoms = molecule("H2O")
    properties = ["energy", "forces"]

    data = pack_request(atoms, properties)
    atoms_out, props_out = unpack_request(data)

    assert len(atoms_out) == len(atoms)
    npt.assert_array_equal(atoms_out.numbers, atoms.numbers)
    npt.assert_allclose(atoms_out.positions, atoms.positions)
    npt.assert_allclose(atoms_out.cell, atoms.cell)
    npt.assert_array_equal(atoms_out.pbc, atoms.pbc)
    assert props_out == properties


def test_request_roundtrip_bulk():
    """Request roundtrip preserves bulk structure with PBC."""
    atoms = bulk("Cu", cubic=True) * (2, 2, 2)
    atoms.pbc = [True, True, True]
    properties = ["energy", "forces", "stress"]

    data = pack_request(atoms, properties)
    atoms_out, props_out = unpack_request(data)

    assert len(atoms_out) == len(atoms)
    npt.assert_array_equal(atoms_out.numbers, atoms.numbers)
    npt.assert_allclose(atoms_out.positions, atoms.positions)
    npt.assert_allclose(atoms_out.cell, atoms.cell)
    npt.assert_array_equal(atoms_out.pbc, atoms.pbc)
    assert props_out == properties


def test_request_roundtrip_empty_properties():
    """Request with empty properties list."""
    atoms = molecule("H2")
    properties = []

    data = pack_request(atoms, properties)
    atoms_out, props_out = unpack_request(data)

    assert props_out == []


def test_request_roundtrip_single_atom():
    """Request with single atom."""
    atoms = Atoms("H", positions=[[0, 0, 0]])
    properties = ["energy"]

    data = pack_request(atoms, properties)
    atoms_out, props_out = unpack_request(data)

    assert len(atoms_out) == 1
    assert atoms_out.symbols[0] == "H"


# =============================================================================
# Response roundtrip tests
# =============================================================================


def test_response_roundtrip_energy():
    """Response roundtrip preserves energy."""
    results = {"energy": -42.5}

    data = pack_response(results)
    results_out = unpack_response(data)

    assert results_out["energy"] == pytest.approx(-42.5)


def test_response_roundtrip_forces():
    """Response roundtrip preserves forces array."""
    forces = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
    results = {"energy": -10.0, "forces": forces}

    data = pack_response(results)
    results_out = unpack_response(data, n_atoms=3)

    assert results_out["energy"] == pytest.approx(-10.0)
    npt.assert_allclose(results_out["forces"], forces)
    assert results_out["forces"].shape == (3, 3)


def test_response_roundtrip_stress():
    """Response roundtrip preserves stress tensor."""
    stress = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    results = {"stress": stress}

    data = pack_response(results)
    results_out = unpack_response(data)

    npt.assert_allclose(results_out["stress"], stress)


def test_response_roundtrip_all_properties():
    """Response with all common properties."""
    n_atoms = 5
    results = {
        "energy": -123.456,
        "forces": np.random.randn(n_atoms, 3),
        "stress": np.random.randn(6),
    }

    data = pack_response(results)
    results_out = unpack_response(data, n_atoms=n_atoms)

    assert results_out["energy"] == pytest.approx(results["energy"])
    npt.assert_allclose(results_out["forces"], results["forces"])
    npt.assert_allclose(results_out["stress"], results["stress"])


# =============================================================================
# Error handling tests
# =============================================================================


def test_response_error():
    """Error response raises RuntimeError."""
    data = pack_response(error="Calculator failed: division by zero")

    with pytest.raises(RuntimeError, match="division by zero"):
        unpack_response(data)


def test_response_error_empty_message():
    """Error response with empty message."""
    data = pack_response(error="")

    with pytest.raises(RuntimeError):
        unpack_response(data)


# =============================================================================
# Utility function tests
# =============================================================================


def test_get_request_info():
    """get_request_info extracts metadata."""
    atoms = molecule("CH4")
    properties = ["energy", "forces"]

    data = pack_request(atoms, properties)
    info = get_request_info(data)

    assert info["n_atoms"] == 5
    assert info["properties"] == ["energy", "forces"]
    assert info["version"] == 1


# =============================================================================
# Edge cases
# =============================================================================


def test_large_system():
    """Protocol handles large systems."""
    # 1000 atoms
    atoms = bulk("Cu", cubic=True) * (10, 10, 10)
    properties = ["energy", "forces", "stress"]

    data = pack_request(atoms, properties)
    atoms_out, props_out = unpack_request(data)

    assert len(atoms_out) == len(atoms)
    npt.assert_allclose(atoms_out.positions, atoms.positions)


def test_non_orthogonal_cell():
    """Protocol handles non-orthogonal cells."""
    atoms = bulk("Cu", "fcc", a=3.6)
    properties = ["energy"]

    data = pack_request(atoms, properties)
    atoms_out, _ = unpack_request(data)

    npt.assert_allclose(atoms_out.cell, atoms.cell)


def test_mixed_pbc():
    """Protocol handles mixed periodic boundaries."""
    atoms = molecule("H2O")
    atoms.cell = [10, 10, 10]
    atoms.pbc = [True, True, False]  # Slab geometry

    data = pack_request(atoms, ["energy"])
    atoms_out, _ = unpack_request(data)

    npt.assert_array_equal(atoms_out.pbc, [True, True, False])


# =============================================================================
# Benchmarks (run with pytest --benchmark-only)
# =============================================================================


@pytest.fixture
def small_atoms():
    """Small molecule for benchmarks."""
    return molecule("H2O")


@pytest.fixture
def medium_atoms():
    """Medium system for benchmarks."""
    return bulk("Cu", cubic=True) * (3, 3, 3)  # 108 atoms


@pytest.fixture
def large_atoms():
    """Large system for benchmarks."""
    return bulk("Cu", cubic=True) * (10, 10, 10)  # 4000 atoms


def test_bench_pack_request_small(benchmark, small_atoms):
    """Benchmark pack_request for small system."""
    benchmark(pack_request, small_atoms, ["energy", "forces"])


def test_bench_pack_request_medium(benchmark, medium_atoms):
    """Benchmark pack_request for medium system."""
    benchmark(pack_request, medium_atoms, ["energy", "forces"])


def test_bench_pack_request_large(benchmark, large_atoms):
    """Benchmark pack_request for large system."""
    benchmark(pack_request, large_atoms, ["energy", "forces"])


def test_bench_unpack_request_small(benchmark, small_atoms):
    """Benchmark unpack_request for small system."""
    data = pack_request(small_atoms, ["energy", "forces"])
    benchmark(unpack_request, data)


def test_bench_unpack_request_large(benchmark, large_atoms):
    """Benchmark unpack_request for large system."""
    data = pack_request(large_atoms, ["energy", "forces"])
    benchmark(unpack_request, data)


def test_bench_roundtrip_small(benchmark, small_atoms):
    """Benchmark full roundtrip for small system."""

    def roundtrip():
        data = pack_request(small_atoms, ["energy", "forces"])
        return unpack_request(data)

    benchmark(roundtrip)


def test_bench_roundtrip_large(benchmark, large_atoms):
    """Benchmark full roundtrip for large system."""

    def roundtrip():
        data = pack_request(large_atoms, ["energy", "forces"])
        return unpack_request(data)

    benchmark(roundtrip)
