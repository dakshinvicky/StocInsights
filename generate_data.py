"""
Data Generator for StockIns8 Static Web Dashboard (GitHub Pages)

Fetches:
1. Daily FII/DII net market activity & stock shareholding data.
2. Upcoming corporate dividends data.

Exports structured JSON files to `data/` directory using clean JSON sanitation.
"""

import sys
import os

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.utils.exporter import export_json_data


def main():
    print("Generating fresh market data for StockIns8 GitHub Pages...")
    export_json_data("data")
    print("Data generation complete!")


if __name__ == "__main__":
    main()
