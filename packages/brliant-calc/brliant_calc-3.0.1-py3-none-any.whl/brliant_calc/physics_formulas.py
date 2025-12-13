def force(m, a):
    return m * a

def kinetic_energy(m, v):
    return 0.5 * m * (v ** 2)

def potential_energy(m, h, g=9.8):
    return m * g * h

def ohms_law(i, r):
    return i * r

def work(f, d):
    return f * d

def speed(d, t):
    if t == 0:
        return "Error: Time cannot be zero."
    return d / t

def acceleration(dv, t):
    if t == 0:
        return "Error: Time cannot be zero."
    return dv / t
