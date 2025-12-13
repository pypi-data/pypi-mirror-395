import unittest
import sys
import matplotlib
matplotlib.use('Agg')
sys.path.insert(0, '..')

from brliant_calc import plotting

class TestPlotting(unittest.TestCase):
    
    def test_simple_plot(self):
        result = plotting.plot("sin(x)", "0,6.28")
        self.assertEqual(result, "Plot displayed.")
    
    def test_nested_expression(self):
        result = plotting.plot("sin(x**2 + pi)", "0,10")
        self.assertEqual(result, "Plot displayed.")
    
    def test_with_variables(self):
        user_vars = {"a": 2.0, "b": 3.14}
        result = plotting.plot("sin(a*x + b)", "0,10", user_vars)
        self.assertEqual(result, "Plot displayed.")
    
    def test_polynomial(self):
        result = plotting.plot("x**3 - 2*x**2 + x", "0,5")
        self.assertEqual(result, "Plot displayed.")
    
    def test_exponential(self):
        result = plotting.plot("exp(-x)", "0,5")
        self.assertEqual(result, "Plot displayed.")
    
    def test_combined_functions(self):
        result = plotting.plot("exp(-x) * cos(2*pi*x)", "0,5")
        self.assertEqual(result, "Plot displayed.")

if __name__ == '__main__':
    unittest.main()
