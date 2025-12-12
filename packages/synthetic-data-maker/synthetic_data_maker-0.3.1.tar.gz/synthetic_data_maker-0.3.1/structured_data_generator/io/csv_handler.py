"""
CSV read/write operations
"""

import pandas as pd


def save_to_csv(dataframe, filename):
    """Save DataFrame to CSV file"""
    if not filename.endswith('.csv'):
        filename += '.csv'
    dataframe.to_csv(filename, index=False)
    return filename


def load_from_csv(filename):
    """Load DataFrame from CSV file"""
    return pd.read_csv(filename)
