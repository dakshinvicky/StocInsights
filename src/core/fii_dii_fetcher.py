"""
Indian Market FII & DII Holding Changes & Daily Activity Fetcher.
"""

from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from bs4 import BeautifulSoup
from .base_fetcher import BaseFetcher


class FIIDIIFetcher(BaseFetcher):
    """
    Client to fetch institutional investment data (FII/DII) and stock CMPs for the Indian stock market.
    """

    NSE_BASE_URL = "https://www.nseindia.com"
    NSE_FIIDII_URL = "https://www.nseindia.com/api/fiidiiTradeReact"

    SLUG_MAP = {
        "M&M": "mahindra-and-mahindra",
        "L&T": "larsen-and-toubro",
        "BAJFINANCE": "bajaj-finance",
        "BAJAJFINSV": "bajaj-finserv",
        "TATAMOTORS": "tata-motors",
        "TATASTEEL": "tata-steel",
        "COALINDIA": "coal-india",
        "ADANIPORTS": "adani-ports-and-special-economic-zone",
        "ADANIENT": "adani-enterprises",
        "ASIANPAINT": "asian-paints",
        "ULTRACEMCO": "ultratech-cement",
        "JSWSTEEL": "jsw-steel",
        "HINDUNILVR": "hindustan-unilever",
        "POWERGRID": "power-grid-corporation-of-india",
        "KOTAKBANK": "kotak-mahindra-bank"
    }

    def __init__(self, timeout: int = 10):
        super().__init__(timeout=timeout)
        self.session.headers.update({
            "Referer": "https://www.nseindia.com/reports/fii-dii"
        })

    def fetch_daily_fii_dii(self) -> pd.DataFrame:
        """Fetch live daily FII and DII net market buy/sell figures in Cash Market (in Rs Crores)."""
        self.init_nse_session(self.NSE_BASE_URL)
        res = self.safe_get(self.NSE_FIIDII_URL)
        if not res:
            return pd.DataFrame()

        try:
            data = res.json()
            if isinstance(data, list):
                records = []
                for item in data:
                    buy_val = float(item.get("buyValue", 0))
                    sell_val = float(item.get("sellValue", 0))
                    net_val = float(item.get("netValue", 0))
                    net_str = f"+{net_val:,.2f}" if net_val > 0 else f"{net_val:,.2f}"

                    records.append({
                        "Category": item.get("category", "").strip(),
                        "Date": item.get("date", "").strip(),
                        "Buy Value (Rs Cr)": f"{buy_val:,.2f}",
                        "Sell Value (Rs Cr)": f"{sell_val:,.2f}",
                        "Net Value (Rs Cr)": net_str,
                    })
                return pd.DataFrame(records)
        except Exception as e:
            print(f"[Error] Failed to parse daily FII/DII JSON: {e}")

        return pd.DataFrame()

    def fetch_cmp(self, symbol: str) -> Optional[float]:
        """Fetch Current Market Price (CMP) for an NSE ticker symbol."""
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

    def fetch_stock_shareholding(self, symbol: str) -> Dict[str, Any]:
        """Fetch historical quarterly shareholding pattern and recent FII / DII holding changes for a stock."""
        clean_symbol = symbol.strip().upper()
        slug = self.SLUG_MAP.get(clean_symbol, clean_symbol.lower().replace('&', 'and').replace('_', '-'))

        urls_to_try = [
            f"https://www.screener.in/company/{slug}/consolidated/",
            f"https://www.screener.in/company/{slug}/"
        ]

        for url in urls_to_try:
            try:
                res = self.safe_get(url)
                if res and res.status_code == 200:
                    soup = BeautifulSoup(res.text, "html.parser")
                    sh_section = soup.find("section", id="shareholding")
                    if sh_section:
                        table = sh_section.find("table")
                        if table:
                            rows = table.find_all("tr")
                            quarters = [th.text.strip() for th in rows[0].find_all(["th", "td"])][1:]

                            category_data = {}
                            for row in rows[1:]:
                                cols = [td.text.strip() for td in row.find_all(["th", "td"])]
                                if cols:
                                    cat_name = cols[0].replace("\xa0+", "").replace("+", "").strip()
                                    category_data[cat_name] = cols[1:]

                            if quarters:
                                last_q = quarters[-1]
                                prev_q = quarters[-2] if len(quarters) > 1 else last_q

                                fii_vals = category_data.get("FIIs", [])
                                dii_vals = category_data.get("DIIs", [])
                                promoter_vals = category_data.get("Promoters", [])
                                public_vals = category_data.get("Public", [])

                                fii_curr = float(fii_vals[-1].replace("%", "")) if fii_vals and fii_vals[-1] else 0.0
                                fii_prev = float(fii_vals[-2].replace("%", "")) if len(fii_vals) > 1 and fii_vals[-2] else fii_curr
                                fii_change = round(fii_curr - fii_prev, 2)

                                dii_curr = float(dii_vals[-1].replace("%", "")) if dii_vals and dii_vals[-1] else 0.0
                                dii_prev = float(dii_vals[-2].replace("%", "")) if len(dii_vals) > 1 and dii_vals[-2] else dii_curr
                                dii_change = round(dii_curr - dii_prev, 2)

                                return {
                                    "Stock": clean_symbol,
                                    "Latest Quarter": last_q,
                                    "Prev Quarter": prev_q,
                                    "FII (%)": fii_curr,
                                    "FII Prev (%)": fii_prev,
                                    "FII QoQ Change (%)": fii_change,
                                    "DII (%)": dii_curr,
                                    "DII Prev (%)": dii_prev,
                                    "DII QoQ Change (%)": dii_change,
                                    "Promoter (%)": float(promoter_vals[-1].replace("%", "")) if promoter_vals and promoter_vals[-1] else 0.0,
                                    "Public (%)": float(public_vals[-1].replace("%", "")) if public_vals and public_vals[-1] else 0.0
                                }
            except Exception:
                continue

        return {
            "Stock": clean_symbol,
            "Latest Quarter": "N/A",
            "Prev Quarter": "N/A",
            "FII (%)": None,
            "FII Prev (%)": None,
            "FII QoQ Change (%)": None,
            "DII (%)": None,
            "DII Prev (%)": None,
            "DII QoQ Change (%)": None,
            "Promoter (%)": None,
            "Public (%)": None
        }

    def fetch_stocks_shareholding_batch(self, symbols: List[str], max_workers: int = 15) -> pd.DataFrame:
        """Fetch FII/DII historical holding changes and CMPs for a list of stocks concurrently."""
        clean_symbols = list(set([s.strip().upper() for s in symbols if s.strip()]))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            cmp_futures = executor.map(self.fetch_cmp, clean_symbols)
            sh_futures = executor.map(self.fetch_stock_shareholding, clean_symbols)

            cmp_dict = dict(zip(clean_symbols, list(cmp_futures)))
            sh_records = list(sh_futures)

        df = pd.DataFrame(sh_records)
        if not df.empty:
            df["CMP"] = df["Stock"].map(cmp_dict)
        return df
