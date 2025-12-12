"""Second partial derivatives and Taylor-like multivariable thinking."""
import sympy as sp

def second_partials(expr, x='x', y='y'):
    x = sp.Symbol(str(x))
    y = sp.Symbol(str(y))
    expr = sp.sympify(expr)
    f_xx = sp.diff(expr, x, 2)
    f_yy = sp.diff(expr, y, 2)
    f_xy = sp.diff(expr, x, y)
    return {'f_xx': f_xx, 'f_yy': f_yy, 'f_xy': f_xy}

__all__ = ['second_partials']
