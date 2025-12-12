"""Golden ratio region and the golden sample / golden mistake expressions."""
import sympy as sp
from .logs_phi import phi, ln

def golden_ratio():
    return phi

def golden_sample(lambda_value=0):
    lam = sp.sympify(lambda_value)
    pi = sp.pi
    result = (sp.Rational(4,3) * pi * ln(41.5)) * (pi * ln(58.5)) + lam
    return sp.simplify(result)

def golden_mistake(lambda_value=0):
    return golden_sample(lambda_value=lambda_value)

__all__ = ['golden_ratio', 'golden_sample', 'golden_mistake']
