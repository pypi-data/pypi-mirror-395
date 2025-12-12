import unittest
import sys
sys.path.insert(0, '..')

from brliant_calc import complex_ops

class TestComplexOperations(unittest.TestCase):
    
    def test_complex_add(self):
        result = complex_ops.add("1+2j", "3+4j")
        self.assertEqual(result, (4+6j))
    
    def test_complex_sub(self):
        result = complex_ops.sub("5+6j", "2+3j")
        self.assertEqual(result, (3+3j))
    
    def test_complex_mul(self):
        result = complex_ops.mul("2+3j", "1-1j")
        self.assertEqual(result, (5+1j))
    
    def test_complex_div(self):
        result = complex_ops.div("4+2j", "1+1j")
        self.assertEqual(result, (3-1j))
    
    def test_magnitude(self):
        result = complex_ops.mag("3+4j")
        self.assertAlmostEqual(result, 5.0, places=10)
    
    def test_phase(self):
        result = complex_ops.phase("1+1j")
        self.assertAlmostEqual(result, 0.7853981633974483, places=10)

if __name__ == '__main__':
    unittest.main()
