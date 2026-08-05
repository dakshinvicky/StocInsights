"""
Base HTTP Fetcher module.
Handles session management, cookie acquisition, and HTTP request headers.
"""

from typing import Optional, Dict, Any
import requests


class BaseFetcher:
    """
    Abstract Base Class for HTTP scraping clients targeting NSE India and Yahoo Finance.
    """

    DEFAULT_USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    )

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.DEFAULT_USER_AGENT,
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
        })
        self._cookies_initialized = False

    def init_nse_session(self, base_url: str = "https://www.nseindia.com"):
        """Acquires required session cookies from NSE homepage."""
        if not self._cookies_initialized:
            try:
                self.session.get(base_url, timeout=self.timeout)
                self._cookies_initialized = True
            except Exception as err:
                print(f"[Warning] Failed to initialize NSE session cookies: {err}")

    def safe_get(self, url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Optional[requests.Response]:
        """Performs a safe HTTP GET request with exception handling."""
        try:
            req_headers = self.session.headers.copy()
            if headers:
                req_headers.update(headers)
            response = self.session.get(url, params=params, headers=req_headers, timeout=self.timeout)
            response.raise_for_status()
            return response
        except Exception as e:
            print(f"[Error] HTTP GET failed for {url}: {e}")
            return None
