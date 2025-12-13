from currency_converter import CurrencyConverter

def convert_currency(from_curr, to_curr, amount):
    c = CurrencyConverter()
    return c.convert(amount, from_curr, to_curr)