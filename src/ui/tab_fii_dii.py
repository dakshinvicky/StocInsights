"""
Tab 1 UI Component: FII & DII Institutional Activity.
Matches 1-to-1 with port 8000 Pro Terminal card styling.
"""

import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
import pandas as pd
from src.core.fii_dii_fetcher import FIIDIIFetcher
from src.utils.formatters import format_dataframe_changes


@st.cache_data(ttl=300)
def load_daily_fii_dii():
    fetcher = FIIDIIFetcher()
    return fetcher.fetch_daily_fii_dii()


@st.cache_data(ttl=600)
def load_stock_shareholding(symbols):
    fetcher = FIIDIIFetcher()
    return fetcher.fetch_stocks_shareholding_batch(symbols)


def render_tab_fii_dii():
    with st.spinner("Fetching live daily FII / DII activity from NSE India..."):
        df_daily = load_daily_fii_dii()

    fii_net = 0.0
    dii_net = 0.0

    if not df_daily.empty:
        for _, row in df_daily.iterrows():
            cat = str(row.get("Category", "")).upper()
            val_str = str(row.get("Net Value (Rs Cr)", "")).replace(",", "").replace("+", "")
            try:
                val = float(val_str)
                if "FII" in cat or "FPI" in cat:
                    fii_net = val
                elif "DII" in cat:
                    dii_net = val
            except ValueError:
                pass

    total_flow = fii_net + dii_net

    # Render Pro Metric Cards (Matching Port 8000 1-to-1)
    m1, m2, m3 = st.columns(3)
    with m1:
        fii_color = "text-emerald" if fii_net >= 0 else "text-rose"
        fii_str = f"+{fii_net:,.2f}" if fii_net > 0 else f"{fii_net:,.2f}"
        st.markdown(f"""
        <div class="pro-metric-card border-cyan">
            <div class="metric-head-st"><span>FII / FPI NET FLOW</span> 🌐</div>
            <div class="metric-val-st {fii_color}">₹ {fii_str} Cr</div>
            <div style="font-size: 0.8rem; color: #94a3b8;">{"🟢 Net Buyers" if fii_net >= 0 else "🔴 Net Sellers"} • Cash Market Net</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        dii_color = "text-emerald" if dii_net >= 0 else "text-rose"
        dii_str = f"+{dii_net:,.2f}" if dii_net > 0 else f"{dii_net:,.2f}"
        st.markdown(f"""
        <div class="pro-metric-card border-purple">
            <div class="metric-head-st"><span>DII NET FLOW</span> 🏛️</div>
            <div class="metric-val-st {dii_color}">₹ {dii_str} Cr</div>
            <div style="font-size: 0.8rem; color: #94a3b8;">{"🟢 Net Buyers" if dii_net >= 0 else "🔴 Net Sellers"} • Cash Market Net</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        total_color = "text-emerald" if total_flow >= 0 else "text-rose"
        total_str = f"+{total_flow:,.2f}" if total_flow > 0 else f"{total_flow:,.2f}"
        sentiment = "🔥 Strongly Bullish" if total_flow > 1000 else ("🟢 Mildly Bullish" if total_flow >= 0 else "🔴 Bearish Flow")
        st.markdown(f"""
        <div class="pro-metric-card border-emerald">
            <div class="metric-head-st"><span>COMBINED INSTITUTIONAL NET</span> ⚖️</div>
            <div class="metric-val-st {total_color}">₹ {total_str} Cr</div>
            <div style="font-size: 0.8rem; color: #10b981; font-weight: 700;">{sentiment}</div>
        </div>
        """, unsafe_allow_html=True)

    # Section 1: Daily Activity Table
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem; margin-bottom: 0.75rem;">
        <div>
            <h3 style="color: #f8fafc; font-weight: 700; margin: 0; font-size: 1.2rem;">📅 Daily Institutional Cash Market Activity</h3>
            <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">Live daily net buying & selling totals published by NSE India</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not df_daily.empty:
        st.dataframe(df_daily, use_container_width=True)
        csv_daily = df_daily.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Daily Data (CSV)", csv_daily, "daily_fii_dii.csv", "text/csv")
    else:
        st.error("Failed to load daily FII/DII data from NSE India.")

    st.markdown("---")

    # Section 2: Quarterly Stock Shareholding Changes
    st.markdown("""
    <div style="margin-bottom: 0.75rem;">
        <h3 style="color: #f8fafc; font-weight: 700; margin: 0; font-size: 1.2rem;">📊 Quarterly Stock Shareholding Changes (FII & DII)</h3>
        <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">Quarter-over-Quarter holding variations and live Current Market Prices (CMP)</p>
    </div>
    """, unsafe_allow_html=True)

    default_stocks = [
        "RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN", "BHARTIARTL", "ITC",
        "AXISBANK", "MARUTI", "M&M", "POWERGRID", "ONGC", "NTPC", "TITAN", "SUNPHARMA"
    ]

    selected_symbols = st.multiselect(
        "Select or Add NSE Tickers to Inspect:",
        options=default_stocks + ["HCLTECH", "WIPRO", "LT", "BAJFINANCE", "ADANIENT", "ADANIPORTS"],
        default=default_stocks[:10]
    )

    custom_ticker = st.text_input("Add Custom Ticker Symbol (e.g. IRCTC, BEL):")
    if custom_ticker:
        clean_custom = custom_ticker.strip().upper()
        if clean_custom not in selected_symbols:
            selected_symbols.append(clean_custom)

    if selected_symbols:
        with st.spinner(f"Fetching shareholding changes for {len(selected_symbols)} stocks..."):
            df_stocks = load_stock_shareholding(tuple(selected_symbols))

        if not df_stocks.empty:
            cols_order = ["Stock", "CMP", "Latest Quarter", "Prev Quarter", "FII (%)", "FII Prev (%)", "FII QoQ Change (%)", "DII (%)", "DII Prev (%)", "DII QoQ Change (%)"]
            existing_cols = [c for c in cols_order if c in df_stocks.columns]
            df_formatted = format_dataframe_changes(df_stocks[existing_cols])

            sub1, sub2, sub3 = st.tabs(["📋 All Selected Stocks", "🟢 FII Buyers", "🔴 FII Sellers"])
            with sub1:
                st.dataframe(df_formatted, use_container_width=True)
            with sub2:
                if "FII QoQ Change (%)" in df_stocks.columns:
                    fii_pos = df_stocks[df_stocks["FII QoQ Change (%)"] > 0].sort_values(by="FII QoQ Change (%)", ascending=False)
                    st.dataframe(format_dataframe_changes(fii_pos[existing_cols]), use_container_width=True)
            with sub3:
                if "FII QoQ Change (%)" in df_stocks.columns:
                    fii_neg = df_stocks[df_stocks["FII QoQ Change (%)"] < 0].sort_values(by="FII QoQ Change (%)", ascending=True)
                    st.dataframe(format_dataframe_changes(fii_neg[existing_cols]), use_container_width=True)

            csv_stocks = df_stocks.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Shareholding Data (CSV)", csv_stocks, "stock_shareholding.csv", "text/csv")
