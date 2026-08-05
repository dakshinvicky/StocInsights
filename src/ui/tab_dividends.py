"""
Tab 2 UI Component: Upcoming Corporate Dividends & Yield Calculator.
Matches 1-to-1 with port 8000 Pro Terminal card styling.
"""

import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
import pandas as pd
from src.core.dividend_fetcher import DividendFetcher


@st.cache_data(ttl=300)
def load_upcoming_dividends(days_ahead, symbol):
    fetcher = DividendFetcher()
    return fetcher.fetch_upcoming_dividends(days_ahead=days_ahead, symbol=symbol if symbol else None)


def render_tab_dividends():
    col_days, col_sym = st.columns([6, 6])
    with col_days:
        days_ahead = st.slider("Lookahead Horizon (Days):", min_value=7, max_value=90, value=30, step=7)
    with col_sym:
        search_sym = st.text_input("Filter Ticker Symbol (Optional, e.g. SBIN):")

    with st.spinner("Fetching upcoming corporate dividend announcements from NSE..."):
        df_div = load_upcoming_dividends(days_ahead=days_ahead, symbol=search_sym)

    count_div = len(df_div) if not df_div.empty else 0
    max_div_val = df_div["Divident per share"].max() if not df_div.empty and "Divident per share" in df_div.columns else 0.0

    # Capital Allocation Selector for Calculator
    st.markdown("""
    <div style="background: rgba(18, 25, 41, 0.75); border: 1px solid #1e293b; border-left: 4px solid #f59e0b; padding: 1.25rem; border-radius: 14px; margin-bottom: 1.5rem;">
        <h4 style="color: #f8fafc; font-weight: 700; margin: 0 0 0.25rem 0;">🧮 Interactive Dividend Yield Earnings Calculator</h4>
        <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">Simulate estimated dividend cash returns based on your capital allocation</p>
    </div>
    """, unsafe_allow_html=True)

    c_input, c_preset = st.columns([6, 6])
    with c_input:
        investment_amount = st.number_input(
            "Capital Allocation Amount (₹):",
            min_value=5000,
            max_value=10000000,
            value=100000,
            step=10000
        )
    with c_preset:
        st.write("Quick Capital Presets:")
        p_col1, p_col2, p_col3, p_col4 = st.columns(4)
        if p_col1.button("₹50K"): investment_amount = 50000
        if p_col2.button("₹1 Lakh"): investment_amount = 100000
        if p_col3.button("₹5 Lakhs"): investment_amount = 500000
        if p_col4.button("₹10 Lakhs"): investment_amount = 1000000

    max_calc_val = 0.0
    if not df_div.empty and "CMP" in df_div.columns and "Divident per share" in df_div.columns:
        def custom_div_calc(row):
            cmp_val = row["CMP"]
            div_val = row["Divident per share"]
            if pd.notnull(cmp_val) and pd.notnull(div_val) and cmp_val > 0:
                return round((investment_amount / cmp_val) * div_val, 2)
            return None
        
        calc_col_name = f"Est. Cash Return (per ₹{investment_amount:,})"
        df_div[calc_col_name] = df_div.apply(custom_div_calc, axis=1)
        if calc_col_name in df_div.columns:
            max_calc_val = df_div[calc_col_name].max() or 0.0

    # Metric Cards (Matching Port 8000 1-to-1)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
        <div class="pro-metric-card border-amber">
            <div class="metric-head-st"><span>UPCOMING DIVIDEND ACTIONS</span> 📅</div>
            <div class="metric-val-st text-amber">{count_div}</div>
            <div style="font-size: 0.8rem; color: #94a3b8;">Corporate Announcements</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="pro-metric-card border-cyan">
            <div class="metric-head-st"><span>MAX DIVIDEND PAYOUT</span> 💰</div>
            <div class="metric-val-st text-cyan">₹ {max_div_val:,.2f}</div>
            <div style="font-size: 0.8rem; color: #94a3b8;">Highest Dividend Per Share</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="pro-metric-card border-emerald">
            <div class="metric-head-st"><span>MAX ESTIMATED EARNING</span> 🐷</div>
            <div class="metric-val-st text-emerald">₹ {max_calc_val:,.2f}</div>
            <div style="font-size: 0.8rem; color: #94a3b8;">Based on ₹{investment_amount:,.0f} capital</div>
        </div>
        """, unsafe_allow_html=True)

    # Section: Dividend Schedule Table
    st.markdown("""
    <div style="margin-top: 1rem; margin-bottom: 0.75rem;">
        <h3 style="color: #f8fafc; font-weight: 700; margin: 0; font-size: 1.2rem;">💰 Corporate Dividend Schedule</h3>
        <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">Ex-Dividend dates, declared payout per share, CMP, and calculated income</p>
    </div>
    """, unsafe_allow_html=True)

    if not df_div.empty:
        st.dataframe(df_div, use_container_width=True)
        csv_div = df_div.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Dividend Schedule (CSV)", csv_div, "upcoming_dividends.csv", "text/csv")
    else:
        st.warning(f"No upcoming dividends found in next {days_ahead} days.")
