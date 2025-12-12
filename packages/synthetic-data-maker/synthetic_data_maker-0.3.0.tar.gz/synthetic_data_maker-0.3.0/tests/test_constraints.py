"""
Unit tests for constraints module
"""

import unittest
from structured_data_generator.core.constraints import (
    enforce_range, ensure_uniqueness, apply_correlation
)


class TestConstraints(unittest.TestCase):
    
    def test_enforce_range(self):
        """Test range enforcement"""
        self.assertEqual(enforce_range(5, 0, 10), 5)
        self.assertEqual(enforce_range(-5, 0, 10), 0)
        self.assertEqual(enforce_range(15, 0, 10), 10)
    
    def test_ensure_uniqueness(self):
        """Test uniqueness enforcement"""
        data = [1, 2, 2, 3, 3, 3, 4]
        result = ensure_uniqueness(data)
        self.assertEqual(result, [1, 2, 3, 4])


if __name__ == '__main__':
    unittest.main()
