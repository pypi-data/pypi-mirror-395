import sympy as sp

def nth_root(x, n):
    x = sp.sympify(x)
    n = sp.sympify(n)
    return x**(1/n)

def root_of_ten(n=9):
    n = sp.sympify(n)
    return sp.Integer(10)**(sp.Rational(1, n))

def evaluate_root(x, n, precision=20):
    x = sp.sympify(x)
    n = sp.sympify(n)
    return sp.N(x**(1/n), precision)

__all__ = ['nth_root', 'root_of_ten', 'evaluate_root']
