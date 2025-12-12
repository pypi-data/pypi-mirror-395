"""
Unit tests for data generators
"""

import unittest
from structured_data_generator.core.generators import (
    USER_TEMPLATE, ECOM_TEMPLATE, generate_from_template
)


class TestGenerators(unittest.TestCase):
    
    def test_user_template_generation(self):
        """Test USER_TEMPLATE generates data correctly"""
        result = generate_from_template(
            USER_TEMPLATE, 
            ["Personal Info"], 
            count=10, 
            seed=42
        )
        self.assertEqual(len(result), 10)
        self.assertIn("Full Name", result.columns)
    
    def test_ecom_template_generation(self):
        """Test ECOM_TEMPLATE generates data correctly"""
        result = generate_from_template(
            ECOM_TEMPLATE, 
            ["Order Info"], 
            count=5, 
            seed=42
        )
        self.assertEqual(len(result), 5)
        self.assertIn("Order ID", result.columns)


if __name__ == '__main__':
    unittest.main()
