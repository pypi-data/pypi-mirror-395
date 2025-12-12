import unittest
from cc_toolkit import greet, calculate

class TestCCToolkit(unittest.TestCase):
    def test_greet(self):
        """Test the greet function"""
        result = greet("World")
        self.assertEqual(result, "Hello, World! Welcome to cc_toolkit.")
        
        result = greet("Alice")
        self.assertEqual(result, "Hello, Alice! Welcome to cc_toolkit.")
    
    def test_calculate_add(self):
        """Test addition operation"""
        result = calculate(5, 3, "add")
        self.assertEqual(result, 8)
    
    def test_calculate_subtract(self):
        """Test subtraction operation"""
        result = calculate(5, 3, "subtract")
        self.assertEqual(result, 2)
    
    def test_calculate_multiply(self):
        """Test multiplication operation"""
        result = calculate(5, 3, "multiply")
        self.assertEqual(result, 15)
    
    def test_calculate_divide(self):
        """Test division operation"""
        result = calculate(6, 3, "divide")
        self.assertEqual(result, 2)
        
        # Test division by zero
        with self.assertRaises(ZeroDivisionError):
            calculate(5, 0, "divide")
    
    def test_calculate_invalid_operation(self):
        """Test invalid operation"""
        with self.assertRaises(ValueError):
            calculate(5, 3, "invalid_operation")

if __name__ == "__main__":
    unittest.main()
