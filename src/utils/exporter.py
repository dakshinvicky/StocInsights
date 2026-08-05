"""
Data Exporter Engine for StockIns8 Static Site (GitHub Pages).
Purges old JSON files and ensures 100% valid JSON compliance.
"""

import os
import json
import numpy as np
import pandas as pd
from src.core.fii_dii_fetcher import FIIDIIFetcher
from src.core.dividend_fetcher import DividendFetcher


def clean_records_for_json(df: pd.DataFrame) -> list:
    """Converts a DataFrame to JSON-safe dictionary records (replaces NaN/Inf with None)."""
    if df.empty:
        return []
    
    cleaned_df = df.replace([np.nan, np.inf, -np.inf], None)
    records = cleaned_df.to_dict(orient="records")
    
    for record in records:
        for k, v in record.items():
            if isinstance(v, float) and (np.isnan(v) or np.isinf(v)):
                record[k] = None
    return records


def export_json_data(output_dir: str = "data") -> bool:
    """Purge old data, fetch fresh live data and export static JSON files."""
    try:
        os.makedirs(output_dir, exist_ok=True)
        print(f"[Exporter] Purging old datasets in '{output_dir}'...")

        # Completely delete existing JSON files to guarantee clean creation
        fii_file = os.path.join(output_dir, "fii_dii.json")
        div_file = os.path.join(output_dir, "dividends.json")

        if os.path.exists(fii_file):
            os.remove(fii_file)
            print(f"[Exporter] Deleted old {fii_file}")

        if os.path.exists(div_file):
            os.remove(div_file)
            print(f"[Exporter] Deleted old {div_file}")

        print(f"[Exporter] Generating fresh static datasets in '{output_dir}'...")

        # 1. Daily FII/DII & Stock Shareholding
        fii_dii_client = FIIDIIFetcher()
        df_daily = fii_dii_client.fetch_daily_fii_dii()
        daily_records = clean_records_for_json(df_daily)

        sample_stocks = [
            "RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN", "BHARTIARTL", "ITC",
            "AXISBANK", "MARUTI", "M&M", "POWERGRID", "ONGC", "NTPC", "TITAN", "SUNPHARMA"
        ]
        df_stocks = fii_dii_client.fetch_stocks_shareholding_batch(sample_stocks)
        stock_records = clean_records_for_json(df_stocks)

        fii_dii_data = {
            "updated_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S IST"),
            "daily": daily_records,
            "stocks": stock_records
        }

        with open(fii_file, "w", encoding="utf-8") as f:
            json.dump(fii_dii_data, f, indent=2)

        # 2. Upcoming Dividends
        div_client = DividendFetcher()
        df_div = div_client.fetch_upcoming_dividends(days_ahead=60)
        div_records = clean_records_for_json(df_div)

        dividends_data = {
            "updated_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S IST"),
            "dividends": div_records
        }

        with open(div_file, "w", encoding="utf-8") as f:
            json.dump(dividends_data, f, indent=2)

        print("[Exporter] Successfully purged old files & exported fresh JSON data/fii_dii.json and data/dividends.json")
        return True

    except Exception as e:
        print(f"[Exporter Error] Failed to export data: {e}")
        return False
