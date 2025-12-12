"""Helpers for geometric series like the 1.111... constructions."""
import sympy as sp

def geometric_sum(a, r, n):
    a = sp.sympify(a)
    r = sp.sympify(r)
    n = sp.sympify(n)
    if r == 1:
        return a*n
    return a*(1 - r**n)/(1 - r)

def infinite_geometric(a, r):
    a = sp.sympify(a)
    r = sp.sympify(r)
    return a/(1 - r)

__all__ = ['geometric_sum', 'infinite_geometric']
