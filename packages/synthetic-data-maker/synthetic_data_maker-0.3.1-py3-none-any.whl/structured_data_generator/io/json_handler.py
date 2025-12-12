"""
JSON read/write operations
"""

import pandas as pd
import json


def save_to_json(dataframe, filename, orient='records', indent=4):
    """Save DataFrame to JSON file"""
    if not filename.endswith('.json'):
        filename += '.json'
    dataframe.to_json(filename, orient=orient, indent=indent)
    return filename


def load_from_json(filename):
    """Load DataFrame from JSON file"""
    return pd.read_json(filename)
