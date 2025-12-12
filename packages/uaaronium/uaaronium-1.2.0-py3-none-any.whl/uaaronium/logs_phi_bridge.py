"""Golden-region bridge: relate ln(5), φ, sqrt(e) and log10(41.5)."""
import sympy as sp
from .logs_phi import phi, ln, log10

def golden_region_constants():
    return {
        "phi": phi,
        "ln5": ln(5),
        "sqrt_e": sp.sqrt(sp.E),
        "exp_half": sp.exp(sp.Rational(1, 2)),
        "log10_41_5": log10(41.5),
    }

def is_golden_region(value, threshold=0.05):
    val = float(sp.N(value))
    phi_val = float(sp.N(phi))
    return abs(val - phi_val) <= threshold * phi_val

__all__ = ['golden_region_constants', 'is_golden_region']
