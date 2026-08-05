"""
Streamlit Web Application Main Entrypoint.
Includes Passcode Security Gate Authentication.
"""

import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from src.ui.tab_fii_dii import render_tab_fii_dii
from src.ui.tab_dividends import render_tab_dividends

# Configurable secret passcode (defaults to STOC2026 or environment variable)
DEFAULT_SECRET_CODE = os.environ.get("APP_SECRET_CODE", "STOC2026")

st.set_page_config(
    page_title="Indian Market Intelligence | Pro Terminal",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

    /* Security Gate Login Box */
    .login-container {
        max-width: 440px;
        margin: 4rem auto;
        background: rgba(18, 25, 41, 0.9);
        backdrop-filter: blur(20px);
        border: 1px solid #1e293b;
        border-top: 4px solid #38bdf8;
        padding: 2.5rem 2rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
        text-align: center;
    }

    .login-icon {
        width: 64px;
        height: 64px;
        background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        color: #ffffff;
        margin: 0 auto 1.5rem auto;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
    }

    .login-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 0.4rem;
        letter-spacing: -0.02em;
    }

    .login-sub {
        font-size: 0.875rem;
        color: #94a3b8;
        margin-bottom: 1.5rem;
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
</style>
""", unsafe_allow_html=True)

# Session state initialization for authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Security Gate Screen if unauthenticated
if not st.session_state["authenticated"]:
    st.markdown("""
    <div class="login-container">
        <div class="login-icon">🔒</div>
        <div class="login-title">TERMINAL SECURITY GATE</div>
        <div class="login-sub">Authorized access only. Enter secret passcode to unlock terminal.</div>
    </div>
    """, unsafe_allow_html=True)

    col_l1, col_l2, col_l3 = st.columns([3, 4, 3])
    with col_l2:
        passcode_input = st.text_input("Secret Access Passcode:", type="password", key="pass_input", placeholder="Enter secret code...")
        if st.button("🔓 Unlock Terminal", use_container_width=True):
            if passcode_input and passcode_input.strip() == DEFAULT_SECRET_CODE:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ Invalid secret passcode! Access denied.")

    st.markdown("""
    <div style="text-align: center; font-size: 0.8rem; color: #64748b; margin-top: 2rem;">
        Default Secret Code: <code>STOC2026</code> (Configurable via APP_SECRET_CODE env variable)
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Authenticated Terminal Layout
st.markdown("""
<div class="ticker-bar-st">
    <div class="ticker-item">📈 <strong>NSE NIFTY 50</strong> 24,650.00 <span style="color:#10b981">+0.45%</span></div>
    <div class="ticker-item">🏛️ <strong>FII CASH FLOW</strong> Live Streamlit Session</div>
    <div class="ticker-item">🏛️ <strong>DII CASH FLOW</strong> Live Streamlit Session</div>
    <div class="ticker-item">💰 <strong>CORPORATE ACTIONS</strong> Active Scanner</div>
</div>
""", unsafe_allow_html=True)

col_h1, col_h2 = st.columns([10, 2])
with col_h1:
    st.markdown("""
    <div class="main-header-st">
        <div class="brand-section-st">
            <div class="brand-logo-st">📈</div>
            <div>
                <div class="brand-title-st">MARKET<span>INTEL</span> <span class="pro-tag-st">PRO TERMINAL</span></div>
                <div class="brand-sub-st">Institutional Flow Tracker & Dividend Yield Intelligence</div>
            </div>
        </div>
        <div style="display: flex; gap: 1rem; align-items: center;">
            <div class="status-indicator-st">🟢 NSE Market Live</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_h2:
    if st.button("🔒 Lock Terminal", key="btn_logout"):
        st.session_state["authenticated"] = False
        st.rerun()

tab1, tab2 = st.tabs(["🏛️ FII & DII Institutional Activity", "💰 Upcoming Corporate Dividends"])

with tab1:
    render_tab_fii_dii()

with tab2:
    render_tab_dividends()
