"""Differentiation helpers."""
import sympy as sp

def differentiate(expr, var='x'):
    var = sp.Symbol(str(var))
    expr = sp.sympify(expr)
    return sp.diff(expr, var)

def partial_fx(expr, x='x', y='y'):
    x = sp.Symbol(str(x))
    y = sp.Symbol(str(y))
    expr = sp.sympify(expr)
    return sp.diff(expr, x)

def partial_fy(expr, x='x', y='y'):
    x = sp.Symbol(str(x))
    y = sp.Symbol(str(y))
    expr = sp.sympify(expr)
    return sp.diff(expr, y)

__all__ = ['differentiate', 'partial_fx', 'partial_fy']
