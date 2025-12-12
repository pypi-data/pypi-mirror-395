"""
Generate dataset profiles and summary statistics
"""

import pandas as pd


def generate_profile(dataframe):
    """Generate comprehensive profile of dataset"""
    profile = {
        'shape': dataframe.shape,
        'columns': list(dataframe.columns),
        'dtypes': dataframe.dtypes.to_dict(),
        'missing_values': dataframe.isnull().sum().to_dict(),
        'memory_usage': dataframe.memory_usage(deep=True).sum(),
    }
    
    # Add numeric column statistics
    numeric_cols = dataframe.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        profile['numeric_stats'] = dataframe[numeric_cols].describe().to_dict()
    
    return profile


def print_profile(profile):
    """Print dataset profile in readable format"""
    print(f"\nDataset Profile:")
    print(f"Shape: {profile['shape'][0]} rows × {profile['shape'][1]} columns")
    print(f"Memory Usage: {profile['memory_usage'] / 1024:.2f} KB")
    print(f"\nColumns: {', '.join(profile['columns'])}")
    
    missing = {k: v for k, v in profile['missing_values'].items() if v > 0}
    if missing:
        print(f"\nMissing Values: {missing}")
    else:
        print("\nNo missing values")
