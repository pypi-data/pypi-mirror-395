from fractions import Fraction
from decimal import Decimal, getcontext

def add_fraction(f1, f2):
    return Fraction(f1) + Fraction(f2)

def sub_fraction(f1, f2):
    return Fraction(f1) - Fraction(f2)

def mul_fraction(f1, f2):
    return Fraction(f1) * Fraction(f2)

def div_fraction(f1, f2):
    return Fraction(f1) / Fraction(f2)

def add_decimal(d1, d2, precision=28):
    getcontext().prec = int(precision)
    return Decimal(d1) + Decimal(d2)

def sub_decimal(d1, d2, precision=28):
    getcontext().prec = int(precision)
    return Decimal(d1) - Decimal(d2)

def mul_decimal(d1, d2, precision=28):
    getcontext().prec = int(precision)
    return Decimal(d1) * Decimal(d2)

def div_decimal(d1, d2, precision=28):
    getcontext().prec = int(precision)
    return Decimal(d1) / Decimal(d2)
