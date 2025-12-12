"""
Unit tests for profiler module
"""

import unittest
import pandas as pd
from structured_data_generator.profiling.profiler import generate_profile


class TestProfiler(unittest.TestCase):
    
    def test_generate_profile(self):
        """Test profile generation"""
        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'score': [85.5, 90.0, 88.5]
        })
        
        profile = generate_profile(df)
        
        self.assertEqual(profile['shape'], (3, 3))
        self.assertEqual(len(profile['columns']), 3)
        self.assertIn('numeric_stats', profile)


if __name__ == '__main__':
    unittest.main()
