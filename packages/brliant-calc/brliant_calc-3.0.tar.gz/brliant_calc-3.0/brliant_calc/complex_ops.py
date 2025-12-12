import cmath

def parse_complex(c_str):
    try:
        return complex(c_str.replace("i", "j"))
    except ValueError:
        raise ValueError(f"Invalid complex number format: {c_str}")

def add(c1, c2):
    return parse_complex(c1) + parse_complex(c2)

def sub(c1, c2):
    return parse_complex(c1) - parse_complex(c2)

def mul(c1, c2):
    return parse_complex(c1) * parse_complex(c2)

def div(c1, c2):
    return parse_complex(c1) / parse_complex(c2)

def mag(c):
    return abs(parse_complex(c))

def phase(c):
    return cmath.phase(parse_complex(c))

def polar(c):
    r, phi = cmath.polar(parse_complex(c))
    return f"r={r}, phi={phi}"

def rect(r, phi):
    return cmath.rect(float(r), float(phi))
