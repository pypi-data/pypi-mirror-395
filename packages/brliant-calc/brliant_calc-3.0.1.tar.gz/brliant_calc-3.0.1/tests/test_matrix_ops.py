import unittest
import sys
import numpy as np
sys.path.insert(0, '..')

from brliant_calc import matrix_ops

class TestMatrixOperations(unittest.TestCase):
    
    def test_matrix_mul(self):
        m1 = "[[1,2],[3,4]]"
        m2 = "[[5,6],[7,8]]"
        result = matrix_ops.mul(m1, m2)
        expected = np.array([[19, 22], [43, 50]])
        np.testing.assert_array_equal(result, expected)
    
    def test_determinant(self):
        m = "[[1,2],[3,4]]"
        result = matrix_ops.det(m)
        self.assertAlmostEqual(result, -2.0, places=10)
    
    def test_transpose(self):
        m = "[[1,2,3],[4,5,6]]"
        result = matrix_ops.transpose(m)
        expected = np.array([[1, 4], [2, 5], [3, 6]])
        np.testing.assert_array_equal(result, expected)
    
    def test_rank(self):
        m = "[[1,2],[2,4]]"
        result = matrix_ops.rank(m)
        self.assertEqual(result, 1)
    
    def test_inverse(self):
        m = "[[1,2],[3,4]]"
        result = matrix_ops.inv(m)
        m_array = np.array([[1, 2], [3, 4]])
        product = np.dot(m_array, result)
        expected_identity = np.eye(2)
        np.testing.assert_array_almost_equal(product, expected_identity, decimal=10)

if __name__ == '__main__':
    unittest.main()
