"""
CLI for generating dataset profiles
"""

import sys
import pandas as pd
from structured_data_generator.profiling.profiler import generate_profile, print_profile


def main():
    if len(sys.argv) < 2:
        print("Usage: python profile_dataset.py <filename.csv|filename.json>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(filename)
        elif filename.endswith('.json'):
            df = pd.read_json(filename)
        else:
            print("Error: File must be CSV or JSON")
            sys.exit(1)
        
        profile = generate_profile(df)
        print_profile(profile)
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
