import unittest
import sys
sys.path.insert(0, '..')

from brliant_calc.precision_ops import add_fraction, mul_decimal

class TestPrecisionOperations(unittest.TestCase):
    
    def test_fraction_add(self):
        result = add_fraction("1/3", "1/6")
        self.assertEqual(str(result), "1/2")
    
    def test_fraction_sub(self):
        from brliant_calc.precision_ops import sub_fraction
        result = sub_fraction("1/2", "1/4")
        self.assertEqual(str(result), "1/4")
    
    def test_fraction_mul(self):
        from brliant_calc.precision_ops import mul_fraction
        result = mul_fraction("2/3", "3/4")
        self.assertEqual(str(result), "1/2")
    
    def test_decimal_precision(self):
        from brliant_calc.precision_ops import div_decimal
        result = div_decimal("1", "3", precision=50)
        self.assertTrue(str(result).startswith("0.33333333333333333333333333333333"))

if __name__ == '__main__':
    unittest.main()
