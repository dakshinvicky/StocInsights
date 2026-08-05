"""
Unit tests for FIIDIIFetcher.
"""

from src.core.fii_dii_fetcher import FIIDIIFetcher
from src.utils.formatters import format_dataframe_changes


def test_fii_dii_fetcher_instantiation():
    fetcher = FIIDIIFetcher(timeout=5)
    assert fetcher.timeout == 5
    assert "User-Agent" in fetcher.session.headers


def test_format_dataframe_changes(sample_daily_df):
    sample_daily_df["FII QoQ Change (%)"] = [1.5, -0.8]
    formatted = format_dataframe_changes(sample_daily_df)
    assert formatted["FII QoQ Change (%)"].iloc[0] == "+1.50%"
    assert formatted["FII QoQ Change (%)"].iloc[1] == "-0.80%"
