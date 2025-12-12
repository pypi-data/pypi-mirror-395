import unittest
import sys
sys.path.insert(0, '..')

from brliant_calc import basic_ops

class TestBasicOperations(unittest.TestCase):
    
    def test_add(self):
        self.assertEqual(basic_ops.add(5, 10), 15)
        self.assertEqual(basic_ops.add(1, 2, 3, 4), 10)
        self.assertEqual(basic_ops.add(-5, 5), 0)
    
    def test_sub(self):
        self.assertEqual(basic_ops.sub(10, 5), 5)
        self.assertEqual(basic_ops.sub(100, 50, 25), 25)
        self.assertEqual(basic_ops.sub(0, 10), -10)
    
    def test_mul(self):
        self.assertEqual(basic_ops.mul(5, 10), 50)
        self.assertEqual(basic_ops.mul(2, 3, 4), 24)
        self.assertEqual(basic_ops.mul(-2, 3), -6)
    
    def test_div(self):
        self.assertEqual(basic_ops.div(10, 2), 5)
        self.assertEqual(basic_ops.div(100, 4, 5), 5)
        self.assertAlmostEqual(basic_ops.div(1, 3), 0.333333, places=5)
    
    def test_mod(self):
        self.assertEqual(basic_ops.mod(10, 3), 1)
        self.assertEqual(basic_ops.mod(100, 7), 2)
        self.assertEqual(basic_ops.mod(10, 5), 0)

if __name__ == '__main__':
    unittest.main()
