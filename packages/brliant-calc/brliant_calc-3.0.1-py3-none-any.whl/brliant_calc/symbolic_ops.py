import sympy

def simplify(expr_str):
    return sympy.simplify(expr_str)

def diff(expr_str, var="x"):
    return sympy.diff(expr_str, var)

def integrate(expr_str, var="x"):
    return sympy.integrate(expr_str, var)

def solve(expr_str, var="x"):

    return sympy.solve(expr_str, var)

def expand(expr_str):
    return sympy.expand(expr_str)

def factor(expr_str):
    return sympy.factor(expr_str)
