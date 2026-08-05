"""
Unit tests for DividendFetcher.
"""

from src.core.dividend_fetcher import DividendFetcher


def test_dividend_fetcher_instantiation():
    fetcher = DividendFetcher(timeout=5)
    assert fetcher.timeout == 5


def test_dividend_1l_calculation(sample_dividend_df):
    row = sample_dividend_df.iloc[0]
    cmp = row["CMP"]
    div = row["Divident per share"]
    earned = round((100000 / cmp) * div, 2)
    assert earned == 1712.5
