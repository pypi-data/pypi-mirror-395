"""Built-in calculator providers for aserpc."""


def get_calculators() -> dict[str, dict]:
    """Return available ASE built-in calculators.

    This is a provider function for the aserpc.calculator_providers entry point.
    Returns metadata dicts with factory paths (no imports needed).
    """
    return {
        "LJ": {"factory": "ase.calculators.lj:LennardJones"},
        "EMT": {"factory": "ase.calculators.emt:EMT"},
    }
