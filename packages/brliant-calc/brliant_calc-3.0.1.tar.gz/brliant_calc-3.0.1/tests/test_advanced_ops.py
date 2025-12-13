import unittest
import sys
import numpy as np
sys.path.insert(0, '..')

from brliant_calc import advanced_ops

class TestAdvancedOperations(unittest.TestCase):
    
    def test_trigonometric(self):
        self.assertAlmostEqual(advanced_ops.sin(0), 0, places=10)
        self.assertAlmostEqual(advanced_ops.cos(0), 1, places=10)
        self.assertAlmostEqual(advanced_ops.tan(0), 0, places=10)
        self.assertAlmostEqual(advanced_ops.sin(np.pi/2), 1, places=10)
    
    def test_inverse_trig(self):
        self.assertAlmostEqual(advanced_ops.arcsin(0.5), np.pi/6, places=10)
        self.assertAlmostEqual(advanced_ops.arccos(0.5), np.pi/3, places=10)
        self.assertAlmostEqual(advanced_ops.arctan(1), np.pi/4, places=10)
    
    def test_hyperbolic(self):
        self.assertAlmostEqual(advanced_ops.sinh(0), 0, places=10)
        self.assertAlmostEqual(advanced_ops.cosh(0), 1, places=10)
        self.assertAlmostEqual(advanced_ops.tanh(0), 0, places=10)
    
    def test_logarithms(self):
        self.assertAlmostEqual(advanced_ops.log(np.e), 1, places=10)
        self.assertAlmostEqual(advanced_ops.log10(100), 2, places=10)
        self.assertAlmostEqual(advanced_ops.log2(8), 3, places=10)
    
    def test_exponentials(self):
        self.assertAlmostEqual(advanced_ops.exp(0), 1, places=10)
        self.assertAlmostEqual(advanced_ops.exp(1), np.e, places=10)
        self.assertEqual(advanced_ops.pow(2, 3), 8)
        self.assertAlmostEqual(advanced_ops.sqrt(16), 4, places=10)
    
    def test_rounding(self):
        self.assertEqual(advanced_ops.floor(3.7), 3)
        self.assertEqual(advanced_ops.ceil(3.2), 4)
        self.assertAlmostEqual(advanced_ops.round(3.14159, 2), 3.14, places=2)
        self.assertEqual(advanced_ops.trunc(3.9), 3)
        self.assertEqual(advanced_ops.sign(-42), -1)
        self.assertEqual(advanced_ops.sign(42), 1)
    
    def test_statistics(self):
        data = [1, 2, 3, 4, 5]
        self.assertEqual(advanced_ops.mean(*data), 3.0)
        self.assertEqual(advanced_ops.median(*data), 3.0)
        self.assertEqual(advanced_ops.min(*data), 1)
        self.assertEqual(advanced_ops.max(*data), 5)
        self.assertEqual(advanced_ops.sum(*data), 15)
    
    def test_factorial(self):
        self.assertEqual(advanced_ops.fact(5), 120)
        self.assertEqual(advanced_ops.fact(0), 1)
        self.assertEqual(advanced_ops.fact(3), 6)
    
    def test_absolute(self):
        self.assertEqual(advanced_ops.abs(-5), 5)
        self.assertEqual(advanced_ops.abs(5), 5)
        self.assertEqual(advanced_ops.abs(0), 0)

if __name__ == '__main__':
    unittest.main()
