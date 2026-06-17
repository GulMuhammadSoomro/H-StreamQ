"""
generate_demo_subset.py
-----------------------
Generates the H-StreamQ demonstration subset from a locally obtained
MIMIC-IV v3.1 labevents.csv file.

IMPORTANT: MIMIC-IV data cannot be redistributed publicly.
You must obtain credentialed access via PhysioNet:
https://physionet.org/content/mimiciv/

Usage:
    python generate_demo_subset.py --input /path/to/labevents.csv --output data/demo_subset.csv

The script selects records from 10 fixed hospital admission IDs
(listed in config/hadm_ids.txt) and saves them as the 1,996-row
local test subset. The main notebook then samples 200 records
from this subset using seed 42.
"""

import argparse
import os
import pandas as pd

# Fixed hospital admission IDs for reproducibility
# These were selected randomly with seed 0 from the full MIMIC-IV labevents
FIXED_HADM_IDS_FILE = os.path.join(os.path.dirname(__file__), 'config', 'hadm_ids.txt')

def load_hadm_ids(filepath):
    with open(filepath, 'r') as f:
        return [int(line.strip()) for line in f if line.strip()]

def generate_subset(input_path, output_path, hadm_ids):
    print(f"Loading labevents from: {input_path}")
    df = pd.read_csv(input_path, low_memory=False)
    print(f"Full labevents shape: {df.shape}")

    subset = df[df['hadm_id'].isin(hadm_ids)].copy()
    print(f"Subset shape (fixed hadm_ids): {subset.shape}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    subset.to_csv(output_path, index=False)
    print(f"Saved subset to: {output_path}")
    return subset

def main():
    parser = argparse.ArgumentParser(description='Generate H-StreamQ MIMIC-IV demonstration subset')
    parser.add_argument('--input', required=True, help='Path to MIMIC-IV v3.1 labevents.csv')
    parser.add_argument('--output', default='data/demo_subset.csv', help='Output path for subset')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise FileNotFoundError(f"Input file not found: {args.input}\n"
                                f"Please obtain MIMIC-IV v3.1 from PhysioNet: "
                                f"https://physionet.org/content/mimiciv/")

    hadm_ids = load_hadm_ids(FIXED_HADM_IDS_FILE)
    print(f"Using {len(hadm_ids)} fixed hospital admission IDs")
    generate_subset(args.input, args.output, hadm_ids)
    print("Done. Run H_StreamQ_Pipeline.ipynb to reproduce the demonstration.")

if __name__ == '__main__':
    main()
