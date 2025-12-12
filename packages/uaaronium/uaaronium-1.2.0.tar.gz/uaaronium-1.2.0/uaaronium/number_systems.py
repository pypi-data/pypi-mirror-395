"""Custom number systems: binary, ternary, quaternary, quinary."""
import sympy as sp

def to_base(n, base):
    n = int(n)
    base = int(base)
    if n == 0:
        return [0]
    digits = []
    while n > 0:
        digits.append(n % base)
        n //= base
    return digits[::-1]

def from_base(digits, base):
    base = int(base)
    value = 0
    for d in digits:
        value = value*base + int(d)
    return value

def binary(n): return to_base(n, 2)
def ternary(n): return to_base(n, 3)
def quaternary(n): return to_base(n, 4)
def quinary(n): return to_base(n, 5)

__all__ = ['to_base', 'from_base', 'binary', 'ternary', 'quaternary', 'quinary']
