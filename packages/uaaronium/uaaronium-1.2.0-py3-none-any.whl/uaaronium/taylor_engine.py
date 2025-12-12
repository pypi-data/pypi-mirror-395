import sympy as sp

def taylor_series(expr, var, about=0, order=5):
    var = sp.Symbol(str(var))
    series = sp.series(expr, var, about, order)
    return series.removeO()

def maclaurin_exp(x, order=5):
    x_sym = sp.Symbol('x')
    series = taylor_series(sp.exp(x_sym), x_sym, 0, order)
    return series.subs(x_sym, x)

def maclaurin_ln1px(x, order=5):
    x_sym = sp.Symbol('x')
    series = taylor_series(sp.log(1 + x_sym), x_sym, 0, order)
    return series.subs(x_sym, x)

__all__ = ['taylor_series', 'maclaurin_exp', 'maclaurin_ln1px']
