"""
Upcoming Dividends Fetcher (Indian Stock Market - NSE) (Legacy Script)

NOTE: This is a legacy standalone experiment script preserved for reference only.
It is NOT executed or used by the main application framework.
Core functionality is maintained in `src/core/dividend_fetcher.py`.
"""

import os
import re
import argparse
import datetime
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor
import requests
import pandas as pd


class IndianStockFetcher:
    """
    Client for fetching upcoming dividend data and CMPs from NSE India.
    """
    
    BASE_URL = "https://www.nseindia.com"
    CORPORATE_ACTIONS_URL = "https://www.nseindia.com/api/corporates-corporateActions"
    
    DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/125.0.0.0 Safari/537.36"
        ),
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/companies-listing/corporate-filings-actions",
    }

    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)
        self._cookies_initialized = False

    def _init_session_cookies(self):
        """Acquires required session cookies from NSE homepage."""
        if not self._cookies_initialized:
            try:
                self.session.get(self.BASE_URL, timeout=self.timeout)
                self._cookies_initialized = True
            except Exception as err:
                print(f"[Warning] Failed to initialize NSE session cookies: {err}")

    def fetch_cmp(self, symbol: str) -> Optional[float]:
        """Fetch Current Market Price (CMP) for an NSE symbol."""
        clean_sym = symbol.strip().upper()
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{clean_sym}.NS?interval=1d"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                meta = res.json()["chart"]["result"][0]["meta"]
                return meta.get("regularMarketPrice")
        except Exception:
            pass
        return None

    def fetch_cmp_batch(self, symbols: List[str], max_workers: int = 15) -> Dict[str, Optional[float]]:
        """Fetch CMPs for multiple symbols concurrently."""
        unique_symbols = list(set(symbols))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self.fetch_cmp, unique_symbols))
        return dict(zip(unique_symbols, results))

    def fetch_upcoming_dividends(
        self,
        days_ahead: int = 30,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        symbol: Optional[str] = None
    ) -> pd.DataFrame:
        """Fetch upcoming corporate dividends and compute dividend yield metrics."""
        self._init_session_cookies()
        
        today = datetime.date.today()
        from_date_str = from_date if from_date else today.strftime("%d-%m-%Y")
        to_date_str = to_date if to_date else (today + datetime.timedelta(days=days_ahead)).strftime("%d-%m-%Y")

        params = {
            "index": "equities",
            "from_date": from_date_str,
            "to_date": to_date_str
        }

        try:
            resp = self.session.get(self.CORPORATE_ACTIONS_URL, params=params, timeout=self.timeout)
            resp.raise_for_status()
            raw_data = resp.json()

            if not isinstance(raw_data, list):
                return pd.DataFrame()

            dividend_records = []
            amount_pattern = r'(?:Rs\.?|Re\.?)\s*([\d\.]+)'

            for item in raw_data:
                subject = item.get("subject", "")
                if "dividend" in subject.lower():
                    matches = re.findall(amount_pattern, subject, re.IGNORECASE)
                    amounts = [float(m) for m in matches] if matches else []
                    div_per_share = sum(amounts) if amounts else None

                    dividend_records.append({
                        "stock": item.get("symbol", "").strip(),
                        "dividentex date": item.get("exDate", "").strip(),
                        "Divident per share": div_per_share,
                    })

            df = pd.DataFrame(dividend_records)
            if df.empty:
                return df

            if symbol:
                df = df[df["stock"].str.upper() == symbol.upper().strip()]
                if df.empty:
                    return df

            symbols = df["stock"].tolist()
            cmp_dict = self.fetch_cmp_batch(symbols)
            df["CMP"] = df["stock"].map(cmp_dict)

            def calc_div_1l(row):
                cmp_val = row["CMP"]
                div_val = row["Divident per share"]
                if pd.notnull(cmp_val) and pd.notnull(div_val) and cmp_val > 0:
                    return round((100000 / cmp_val) * div_val, 2)
                return None

            df["divident per 1L"] = df.apply(calc_div_1l, axis=1)

            cols = ["stock", "dividentex date", "CMP", "Divident per share", "divident per 1L"]
            return df[[c for c in cols if c in df.columns]]

        except Exception as e:
            print(f"[Error] Failed to fetch dividends: {e}")
            return pd.DataFrame()


if __name__ == "__main__":
    print("[Experiment Script] This is an unexecuted legacy reference file.")
