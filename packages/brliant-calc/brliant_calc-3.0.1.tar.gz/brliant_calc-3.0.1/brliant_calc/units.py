def length(value, from_unit, to_unit):
    factors = {
        'm': 1.0,
        'km': 1000.0,
        'cm': 0.01,
        'mm': 0.001,
        'miles': 1609.344,
        'feet': 0.3048
    }
    
    if from_unit not in factors or to_unit not in factors:
        return f"Error: Supported length units are {', '.join(factors.keys())}"
    

    meters = value * factors[from_unit]

    return meters / factors[to_unit]

def mass(value, from_unit, to_unit):
    factors = {
        'g': 0.001,
        'kg': 1.0,
        'lb': 0.45359237,
        'oz': 0.028349523125
    }
    
    if from_unit not in factors or to_unit not in factors:
        return f"Error: Supported mass units are {', '.join(factors.keys())}"
    
    kg = value * factors[from_unit]
    return kg / factors[to_unit]

def temperature(value, from_unit, to_unit):

    if from_unit == 'C':
        c = value
    elif from_unit == 'F':
        c = (value - 32) * 5/9
    elif from_unit == 'K':
        c = value - 273.15
    else:
        return "Error: Supported temperature units are C, F, K"
  
    if to_unit == 'C':
        return c
    elif to_unit == 'F':
        return (c * 9/5) + 32
    elif to_unit == 'K':
        return c + 273.15
    else:
        return "Error: Supported temperature units are C, F, K"

def time(value, from_unit, to_unit):
    factors = {
        's': 1.0,
        'min': 60.0,
        'hr': 3600.0
    }
    
    if from_unit not in factors or to_unit not in factors:
        return f"Error: Supported time units are {', '.join(factors.keys())}"
    
    seconds = value * factors[from_unit]
    return seconds / factors[to_unit]

def speed(value, from_unit, to_unit):
    factors = {
        'm/s': 1.0,
        'km/h': 1/3.6, 
        'mph': 0.44704
    }
    
    if from_unit not in factors or to_unit not in factors:
        return f"Error: Supported speed units are {', '.join(factors.keys())}"
    
    ms = value * factors[from_unit]
    return ms / factors[to_unit]
