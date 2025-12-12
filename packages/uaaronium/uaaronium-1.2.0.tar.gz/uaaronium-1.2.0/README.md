# Uaaronium v1.2

Uaaronium is a Python mathematics engine based on Aaron Craig Sinanan's book.

It encodes:
- custom number systems (binary / ternary / quaternary / quinary)
- roots and 9th-root-of-10 style thinking
- logarithms and the phi / ln(5) / log10(41.5) golden region
- Taylor & Maclaurin series
- differentiation and partial differentiation
- geometric series like 1.111...
- golden sample and golden mistake expressions
- Newton-style iterative solvers
- a simple acceleration expression model
- a golden-region bridge that links ln(5), φ, sqrt(e) and log10(41.5)
  as members of the same numerical neighbourhood.

Example:

```python
import uaaronium as ua
from sympy import sqrt, E

print(ua.root_of_ten(9))
print(ua.phi_region_triplet())
print(ua.golden_region_constants())
print(ua.is_golden_region(sqrt(E)))
print(ua.golden_sample(0))
```
