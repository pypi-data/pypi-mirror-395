"""Iterative methods: Newton-like solvers, including solving ln(x) = target."""
import sympy as sp
from .logs_phi import ln

def newton_solve(expr, var='x', start=1.0, iterations=5):
    var = sp.Symbol(str(var))
    expr = sp.sympify(expr)
    f = sp.lambdify(var, expr, 'sympy')
    fprime_expr = sp.diff(expr, var)
    fprime = sp.lambdify(var, fprime_expr, 'sympy')
    x = sp.sympify(start)
    for _ in range(iterations):
        fx = f(x)
        fpx = fprime(x)
        if fpx == 0:
            break
        x = x - fx/fpx
    return sp.N(x)

def solve_ln_equals(target, start=1.0, iterations=5):
    x = sp.Symbol('x')
    expr = ln(x) - target
    return newton_solve(expr, var=x, start=start, iterations=iterations)

__all__ = ['newton_solve', 'solve_ln_equals']
