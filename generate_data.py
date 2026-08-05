"""
Data Generator for GitHub Pages Static Dashboard

Fetches:
1. Daily FII/DII net market activity & stock shareholding data.
2. Upcoming corporate dividends data.

Exports structured JSON files to `data/` directory for consumption by index.html.
"""

import os
import json
import pandas as pd
from fii_dii_fetcher import FIIDIIFetcher
from indian_stock_fetcher import IndianStockFetcher


def generate_all_data():
    os.makedirs("data", exist_ok=True)
    print("Generating data for static Web App...")

    # 1. Fetch Daily FII / DII activity
    fii_dii_fetcher = FIIDIIFetcher()
    print("Fetching Daily FII / DII data...")
    df_daily = fii_dii_fetcher.fetch_daily_fii_dii()
    
    daily_records = df_daily.to_dict(orient="records") if not df_daily.empty else []

    # 2. Fetch Stock Shareholding Data
    sample_stocks = [
        "RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN", "BHARTIARTL", "ITC",
        "AXISBANK", "MARUTI", "M&M", "POWERGRID", "ONGC", "NTPC", "TITAN", "SUNPHARMA",
        "TATAMOTORS", "TATASTEEL", "COALINDIA", "ASIANPAINT", "ULTRACEMCO", "JSWSTEEL"
    ]
    print(f"Fetching FII/DII shareholding for {len(sample_stocks)} stocks...")
    df_stocks = fii_dii_fetcher.fetch_stocks_shareholding_batch(sample_stocks)
    stock_records = df_stocks.to_dict(orient="records") if not df_stocks.empty else []

    fii_dii_data = {
        "updated_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S IST"),
        "daily": daily_records,
        "stocks": stock_records
    }

    with open("data/fii_dii.json", "w", encoding="utf-8") as f:
        json.dump(fii_dii_data, f, indent=2)
    print("Saved data/fii_dii.json")

    # 3. Fetch Upcoming Dividends
    div_fetcher = IndianStockFetcher()
    print("Fetching upcoming dividends...")
    df_div = div_fetcher.fetch_upcoming_dividends(days_ahead=60)
    div_records = df_div.to_dict(orient="records") if not df_div.empty else []

    dividends_data = {
        "updated_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S IST"),
        "dividends": div_records
    }

    with open("data/dividends.json", "w", encoding="utf-8") as f:
        json.dump(dividends_data, f, indent=2)
    print("Saved data/dividends.json")

    print("Data generation complete!")


if __name__ == "__main__":
    generate_all_data()
