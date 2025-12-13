import pint

ureg = pint.UnitRegistry()

def evaluate_dim(expression):
    try:
        result = ureg(expression)
        return f"{result}"
    except Exception as e:
        return f"Error evaluating dimensional expression: {e}"

def convert_dim(value, from_unit, to_unit):
    try:
        quantity = ureg.Quantity(float(value), from_unit)
        result = quantity.to(to_unit)
        return f"{result}"
    except Exception as e:
        return f"Error converting units: {e}"
