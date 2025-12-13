import math


def add(*args):
    return math.fsum(args)

def sub(*args):
    if not args:
        return 0
    return args[0] - math.fsum(args[1:])

def mul(*args):
    return math.prod(args)

def div(*args):
    if not args:
        return "error: no arguments provided"
    if 0 in args[1:]:  
        return "cannot divide by zero."
    
    total = args[0]
    for i in args[1:]:
        total /= i
    return total

def mod(dividend, divisor):
    if divisor == 0:
        return "cannot divide by zero."
    return math.fmod(dividend, divisor)