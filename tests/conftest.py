"""
Pytest configuration and shared fixtures.
"""

import pytest
import pandas as pd


@pytest.fixture
def sample_daily_df():
    return pd.DataFrame([
        {
            "Category": "FII/FPI *",
            "Date": "05-Aug-2026",
            "Buy Value (Rs Cr)": "12,500.00",
            "Sell Value (Rs Cr)": "10,200.00",
            "Net Value (Rs Cr)": "+2,300.00"
        },
        {
            "Category": "DII **",
            "Date": "05-Aug-2026",
            "Buy Value (Rs Cr)": "8,100.00",
            "Sell Value (Rs Cr)": "9,000.00",
            "Net Value (Rs Cr)": "-900.00"
        }
    ])


@pytest.fixture
def sample_dividend_df():
    return pd.DataFrame([
        {
            "stock": "SBIN",
            "dividentex date": "15-Aug-2026",
            "CMP": 800.0,
            "Divident per share": 13.7,
            "divident per 1L": 1712.5
        }
    ])
