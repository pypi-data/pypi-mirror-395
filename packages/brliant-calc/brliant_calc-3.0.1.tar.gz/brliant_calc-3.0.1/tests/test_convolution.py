import unittest
import sys
sys.path.insert(0, '..')

from brliant_calc.advanced_ops import convolve

class TestConvolution(unittest.TestCase):
    
    def test_basic_convolution(self):
        signal = [1, 2, 3]
        kernel = [0.5, 0.5]
        result = convolve(signal, kernel)
        expected = [0.5, 1.5, 2.5, 1.5]
        self.assertEqual(list(result), expected)
    
    def test_convolution_with_zeros(self):
        signal = [1, 0, 1]
        kernel = [1, 1]
        result = convolve(signal, kernel)
        expected = [1, 1, 1, 1]
        self.assertEqual(list(result), expected)

if __name__ == '__main__':
    unittest.main()
