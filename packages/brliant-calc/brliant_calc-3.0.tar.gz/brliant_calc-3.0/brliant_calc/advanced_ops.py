import numpy as np
import math
from functools import lru_cache

def nth(number, n):
    if n == 0:
        return "n cannot be zero."
    return np.power(number, 1 / n)

def exp(x):
    return np.exp(x)

def pow(base, exponent):
    return np.power(base, exponent)

def log(value):
    if value <= 0:
        return "logarithm is undefined for non-positive values."
    return np.log(value)

def log10(value):
    if value <= 0:
        return "logarithm is undefined for non-positive values."
    return np.log10(value)

def log2(value):
    if value <= 0:
        return "logarithm is undefined for non-positive values."
    return np.log2(value)

@lru_cache(maxsize=128)
def fact(n):
    if isinstance(n, float) and n.is_integer():
        n = int(n)
    if not isinstance(n, int) or n < 0:
        return "factorial is only defined for non-negative integers."
    return math.factorial(n)

def sin(x):
    return np.sin(x)

def cos(x):
    return np.cos(x)

def tan(x):
    return np.tan(x)

def arcsin(x):
    return np.arcsin(x)

def arccos(x):
    return np.arccos(x)

def arctan(x):
    return np.arctan(x)

def sinh(x):
    return np.sinh(x)

def cosh(x):
    return np.cosh(x)

def tanh(x):
    return np.tanh(x)

def arcsinh(x):
    return np.arcsinh(x)

def arccosh(x):
    return np.arccosh(x)

def arctanh(x):
    return np.arctanh(x)

def sqrt(x):
    return np.sqrt(x)

def abs(x):
    return np.abs(x)

def floor(x):
    return np.floor(x)

def ceil(x):
    return np.ceil(x)

def round(x, decimals=0):
    return np.round(x, decimals)

def trunc(x):
    return np.trunc(x)

def sign(x):
    return np.sign(x)

def mean(*args):
    return np.mean(args)

def median(*args):
    return np.median(args)

def std(*args):
    return np.std(args)

def var(*args):
    return np.var(args)

def min(*args):
    return np.min(args)

def max(*args):
    return np.max(args)

def sum(*args):
    return np.sum(args)

def prod(*args):
    return np.prod(args)

def convolve(signal, kernel):
    return np.convolve(signal, kernel, mode='full')
