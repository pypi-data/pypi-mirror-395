"""Basic arithmetic ideas: repeated addition as multiplication, etc."""
import sympy as sp

def repeated_addition(base, times):
    base = sp.sympify(base)
    times = int(times)
    return sum(base for _ in range(times))

def square(n):
    n = sp.sympify(n)
    return n**2

def cube(n):
    n = sp.sympify(n)
    return n**3

__all__ = ['repeated_addition', 'square', 'cube']
