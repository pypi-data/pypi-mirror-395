import unittest
import sys
sys.path.insert(0, '..')

class TestSecurityFeatures(unittest.TestCase):
    
    def test_ast_parser_blocks_imports(self):
        from brliant_calc import plotting
        
        malicious_expr = "__import__('os').system('calc')"
        result = plotting.plot(malicious_expr, "0,10")
        self.assertIn("Error", result)
    
    def test_ast_parser_blocks_exec(self):
        from brliant_calc import plotting
        
        malicious_expr = "exec('print(1)')"
        result = plotting.plot(malicious_expr, "0,10")
        self.assertIn("Error", result)
    
    def test_ast_parser_blocks_eval(self):
        from brliant_calc import plotting
        
        malicious_expr = "eval('1+1')"
        result = plotting.plot(malicious_expr, "0,10")
        self.assertIn("Error", result)
    
    def test_ast_parser_allows_safe_math(self):
        from brliant_calc import plotting
        
        safe_expr = "sin(x) + cos(x)"
        result = plotting.plot(safe_expr, "0,10")
        self.assertEqual(result, "Plot displayed.")

if __name__ == '__main__':
    unittest.main()
