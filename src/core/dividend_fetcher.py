"""
Upcoming Dividends Fetcher Module (Indian Stock Market - NSE).
"""

import re
import datetime
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from .base_fetcher import BaseFetcher


class DividendFetcher(BaseFetcher):
    """
    Client for fetching upcoming dividend data and CMPs from NSE India.
    """

    BASE_URL = "https://www.nseindia.com"
    CORPORATE_ACTIONS_URL = "https://www.nseindia.com/api/corporates-corporateActions"

    def __init__(self, timeout: int = 15):
        super().__init__(timeout=timeout)
        self.session.headers.update({
            "Referer": "https://www.nseindia.com/companies-listing/corporate-filings-actions"
        })

    def fetch_cmp(self, symbol: str) -> Optional[float]:
        """Fetch Current Market Price (CMP) for an NSE symbol."""
        clean_sym = symbol.strip().upper()
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{clean_sym}.NS?interval=1d"
            res = self.safe_get(url)
            if res and res.status_code == 200:
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
        """
        Fetch upcoming corporate dividends and compute dividend yield metrics.

        Returns DataFrame with columns:
          stock, dividentex date, CMP, Divident per share, divident per 1L
        """
        self.init_nse_session(self.BASE_URL)

        today = datetime.date.today()
        from_date_str = from_date if from_date else today.strftime("%d-%m-%Y")
        to_date_str = to_date if to_date else (today + datetime.timedelta(days=days_ahead)).strftime("%d-%m-%Y")

        params = {
            "index": "equities",
            "from_date": from_date_str,
            "to_date": to_date_str
        }

        res = self.safe_get(self.CORPORATE_ACTIONS_URL, params=params)
        if not res:
            return pd.DataFrame()

        try:
            raw_data = res.json()
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

            # Fetch CMP & calculate Dividend per 1L
            symbols = df["stock"].tolist()
            cmp_dict = self.fetch_cmp_batch(symbols)
            df["CMP"] = df["stock"].map(cmp_dict)

            # Formula: 100000 / cmp * dividend
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
            print(f"[Error] Failed to parse upcoming dividends: {e}")
            return pd.DataFrame()
