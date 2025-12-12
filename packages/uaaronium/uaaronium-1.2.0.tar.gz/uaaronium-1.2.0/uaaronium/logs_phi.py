"""Logarithms, exponentials and the phi / ln 5 / log10(41.5) region."""
import sympy as sp

phi = (1 + sp.sqrt(5))/2

def ln(x):
    return sp.log(sp.sympify(x))

def log10(x):
    x = sp.sympify(x)
    return sp.log(x, 10)

def log_base(x, base):
    x = sp.sympify(x)
    base = sp.sympify(base)
    return sp.log(x) / sp.log(base)

def phi_region_triplet():
    return {
        "ln5": ln(5),
        "phi": phi,
        "log10_41_5": log10(41.5)
    }

__all__ = ['phi', 'ln', 'log10', 'log_base', 'phi_region_triplet']
