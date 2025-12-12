"""Very simple acceleration modelling inspired by the engine / rpm example."""
import sympy as sp

def acceleration_expression(c_drag='c', L_friction='L'):
    x = sp.Symbol('x')
    c = sp.Symbol(str(c_drag))
    L = sp.Symbol(str(L_friction))
    expr = sp.diff(2*x* (x**2), x) + c + L
    return sp.simplify(expr)

__all__ = ['acceleration_expression']
