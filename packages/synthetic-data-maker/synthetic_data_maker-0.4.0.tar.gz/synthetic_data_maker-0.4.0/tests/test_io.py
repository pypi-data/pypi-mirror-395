"""
Unit tests for I/O handlers
"""

import unittest
import pandas as pd
import os
from structured_data_generator.io.csv_handler import save_to_csv, load_from_csv
from structured_data_generator.io.json_handler import save_to_json, load_from_json


class TestIO(unittest.TestCase):
    
    def setUp(self):
        """Create test data"""
        self.test_df = pd.DataFrame({
            'name': ['Alice', 'Bob'],
            'age': [25, 30]
        })
    
    def tearDown(self):
        """Clean up test files"""
        for file in ['test.csv', 'test.json']:
            if os.path.exists(file):
                os.remove(file)
    
    def test_csv_save_load(self):
        """Test CSV save and load"""
        save_to_csv(self.test_df, 'test.csv')
        loaded = load_from_csv('test.csv')
        self.assertEqual(len(loaded), 2)
    
    def test_json_save_load(self):
        """Test JSON save and load"""
        save_to_json(self.test_df, 'test.json')
        loaded = load_from_json('test.json')
        self.assertEqual(len(loaded), 2)


if __name__ == '__main__':
    unittest.main()
