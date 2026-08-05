"""
Formatting utilities for DataFrames and numbers.
"""

import pandas as pd


def format_dataframe_changes(df: pd.DataFrame) -> pd.DataFrame:
    """Format numeric QoQ changes with explicit + and - signs for visual clarity."""
    df_formatted = df.copy()
    if "FII QoQ Change (%)" in df_formatted.columns:
        df_formatted["FII QoQ Change (%)"] = df_formatted["FII QoQ Change (%)"].apply(
            lambda x: f"+{x:.2f}%" if pd.notnull(x) and x > 0 else (f"{x:.2f}%" if pd.notnull(x) else "N/A")
        )
    if "DII QoQ Change (%)" in df_formatted.columns:
        df_formatted["DII QoQ Change (%)"] = df_formatted["DII QoQ Change (%)"].apply(
            lambda x: f"+{x:.2f}%" if pd.notnull(x) and x > 0 else (f"{x:.2f}%" if pd.notnull(x) else "N/A")
        )
    return df_formatted


def format_currency(val: float, prefix: str = "₹ ") -> str:
    """Format float into INR currency string with commas."""
    if val is None or pd.isna(val):
        return "N/A"
    sign = "+" if val > 0 else ""
    return f"{prefix}{sign}{val:,.2f}"
