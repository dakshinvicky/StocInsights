"""
StockIns8 Web Application Main Entrypoint.
Direct Application Loading with Live On-Demand Data Synchronization.
"""

import sys
import os
from datetime import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from src.ui.tab_fii_dii import render_tab_fii_dii
from src.ui.tab_dividends import render_tab_dividends
from src.utils.exporter import export_json_data

st.set_page_config(
    page_title="StockIns8 Pro Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State for Last Sync Timestamp
if "last_sync_time" not in st.session_state:
    st.session_state["last_sync_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")

# Global CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif !important;
    }
    
    .stApp {
        background-color: #090d16 !important;
        color: #f8fafc !important;
    }

    /* Top Ticker Bar */
    .ticker-bar-st {
        background: #050810;
        border-bottom: 1px solid #1e293b;
        padding: 0.5rem 1rem;
        margin: -4rem -5rem 1.5rem -5rem;
        display: flex;
        gap: 2rem;
        font-size: 0.825rem;
        font-family: 'JetBrains Mono', monospace;
        color: #94a3b8;
        white-space: nowrap;
        overflow-x: auto;
    }
    .ticker-item {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Main Header */
    .main-header-st {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(18, 25, 41, 0.85);
        backdrop-filter: blur(16px);
        border: 1px solid #1e293b;
        padding: 1.25rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    .brand-section-st {
        display: flex;
        align-items: center;
        gap: 1.25rem;
    }
    .brand-logo-st {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        color: #ffffff;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
    }
    .brand-title-st {
        font-size: 1.5rem;
        font-weight: 800;
        color: #f8fafc;
        letter-spacing: -0.03em;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .brand-title-st span { color: #38bdf8; }
    .pro-tag-st {
        font-size: 0.65rem;
        font-weight: 700;
        background: rgba(56, 189, 248, 0.12);
        color: #38bdf8;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        letter-spacing: 0.05em;
    }
    .brand-sub-st {
        font-size: 0.875rem;
        color: #94a3b8;
    }

    /* Metric Cards Custom HTML/CSS */
    .pro-metric-card {
        background: rgba(18, 25, 41, 0.75);
        backdrop-filter: blur(16px);
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        margin-bottom: 1rem;
    }
    .border-cyan { border-top: 3px solid #38bdf8; }
    .border-purple { border-top: 3px solid #a855f7; }
    .border-emerald { border-top: 3px solid #10b981; }
    .border-amber { border-top: 3px solid #f59e0b; }

    .metric-head-st {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
        color: #94a3b8;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
    }
    .metric-val-st {
        font-size: 1.85rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.03em;
        margin-bottom: 0.25rem;
    }
    .text-emerald { color: #10b981 !important; }
    .text-rose { color: #f43f5e !important; }
    .text-amber { color: #f59e0b !important; }
    .text-cyan { color: #38bdf8 !important; }

    /* Streamlit Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        margin-bottom: 1.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(18, 25, 41, 0.75) !important;
        border: 1px solid #1e293b !important;
        color: #94a3b8 !important;
        padding: 0.85rem 1.5rem !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
    }
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.25) !important;
    }

    .stDataFrame {
        border-radius: 12px;
        border: 1px solid #1e293b;
        overflow: hidden;
    }

    .sync-badge-st {
        font-size: 0.8rem;
        color: #94a3b8;
        background: #0d1322;
        padding: 0.4rem 0.85rem;
        border-radius: 20px;
        border: 1px solid #1e293b;
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: 1px solid #38bdf8 !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.3) !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# Direct Application Layout
st.markdown("""
<div class="ticker-bar-st">
    <div class="ticker-item">📈 <strong>NSE NIFTY 50</strong> 24,650.00 <span style="color:#10b981">+0.45%</span></div>
    <div class="ticker-item">🏛️ <strong>FII CASH FLOW</strong> Live StockIns8 Session</div>
    <div class="ticker-item">🏛️ <strong>DII CASH FLOW</strong> Live StockIns8 Session</div>
    <div class="ticker-item">💰 <strong>CORPORATE ACTIONS</strong> Active Scanner</div>
</div>
""", unsafe_allow_html=True)

col_h1, col_h2 = st.columns([7, 5])
with col_h1:
    st.markdown(f"""
    <div class="main-header-st">
        <div class="brand-section-st">
            <div class="brand-logo-st">📈</div>
            <div>
                <div class="brand-title-st">StockIns8 <span>PRO</span> <span class="pro-tag-st">TERMINAL</span></div>
                <div class="brand-sub-st">Institutional Flow Tracker & Dividend Yield Intelligence</div>
            </div>
        </div>
        <div style="display: flex; gap: 1rem; align-items: center;">
            <div class="sync-badge-st">🔄 Synced: {st.session_state['last_sync_time']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_h2:
    if st.button("⚡ LIVE SYNC & RELOAD DATA", key="btn_sync_all", use_container_width=True):
        with st.spinner("Scraping live NSE market data & re-generating static JSON files..."):
            export_json_data("data")
            st.cache_data.clear()
            st.session_state["last_sync_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
        st.toast(f"⚡ Synced live data at {st.session_state['last_sync_time']}!", icon="🚀")
        st.rerun()

tab1, tab2 = st.tabs(["🏛️ FII & DII Institutional Activity", "💰 Upcoming Corporate Dividends"])

with tab1:
    render_tab_fii_dii()

with tab2:
    render_tab_dividends()
