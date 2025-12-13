import unittest
import sys
import numpy as np
sys.path.insert(0, '..')

from brliant_calc import vectors

class TestVectorOperations(unittest.TestCase):
    
    def test_dot_product(self):
        result = vectors.dot_product([1, 2, 3], [4, 5, 6])
        self.assertEqual(result, 32)
    
    def test_cross_product(self):
        result = vectors.cross_product([1, 0, 0], [0, 1, 0])
        expected = [0, 0, 1]
        np.testing.assert_array_equal(result, expected)
    
    def test_magnitude(self):
        result = vectors.magnitude([3, 4])
        self.assertAlmostEqual(result, 5.0, places=10)
    
    def test_normalize(self):
        result = vectors.normalize([3, 4])
        expected = [0.6, 0.8]
        np.testing.assert_array_almost_equal(result, expected, decimal=10)
    
    def test_angle_between(self):
        result = vectors.angle_between([1, 0], [0, 1])
        self.assertAlmostEqual(result, 90.0, places=10)

if __name__ == '__main__':
    unittest.main()
