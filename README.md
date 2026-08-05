# 📈 StockIns8 - Financial Intelligence Platform

A production-grade Python framework and dual-interface Web Platform for tracking Indian Stock Market (NSE) financial metrics:
1. **FII & DII Institutional Activity**: Live daily net buying/selling market flows (in ₹ Crores) and stock-wise quarterly QoQ shareholding changes (FII % and DII %).
2. **Upcoming Corporate Dividends**: Live corporate dividend announcements from NSE India, Current Market Prices (CMP from Yahoo Finance), and an interactive **Dividend Yield Earnings Calculator** per custom investment amount (e.g. ₹1,00,000).

Supports both a live **Streamlit Web Application** (hosted on Streamlit Community Cloud or locally) and an automated static **GitHub Pages Web Dashboard** powered by GitHub Actions.

---

## 🏛️ System Design & Architecture

```
+---------------------------------------------------------------------------------------------------+
|                                       USER INTERFACES                                             |
|                                                                                                   |
|   +---------------------------------------+       +-------------------------------------------+   |
|   | StockIns8 Streamlit App (src/ui/app.py)|       | StockIns8 GitHub Pages (src/web/index.html|   |
|   | - Live Dynamic Scraping (NSE/Yahoo)   |       | - Static JSON Consumption                 |   |
|   | - Interactive Stock Filter & Calculator|       | - Search, Sort, Filter, Calculator (JS)  |   |
|   +---------------------------------------+       +-------------------------------------------+   |
+--------------------------------------------+------------------------------------------------------+
                                             |
                                             v
+---------------------------------------------------------------------------------------------------+
|                                       CORE FRAMEWORK (src/)                                       |
|                                                                                                   |
|   +-----------------------------------+        +----------------------------------------------+   |
|   | FIIDIIFetcher                     |        | DividendFetcher                              |   |
|   | (src/core/fii_dii_fetcher.py)     |        | (src/core/dividend_fetcher.py)               |   |
|   | - Daily Net Flow Parsing          |        | - Corporate Action Extraction                |   |
|   | - Screener QoQ Scraper            |        | - Dividend Yield Math Engine                 |   |
|   +-----------------------------------+        +----------------------------------------------+   |
|                     \                            /                                                |
|                      \                          /                                                 |
|                       v                        v                                                  |
|         +-------------------------------------------------------------+                           |
|         | BaseFetcher (src/core/base_fetcher.py)                      |                           |
|         | - Connection Pooling & Custom User-Agent Headers             |                           |
|         | - Automatic Session Cookie Acquisition (NSE Homepage)       |                           |
|         +-------------------------------------------------------------+                           |
+---------------------------------------------------------------------------------------------------+
```

---

## 🔒 Security Gate Authentication

Both StockIns8 web applications include Security Gate Passcode protection:
- **Default Secret Passcode**: `STOCKINS8` (or `STOC2026`)
- **Customizable**: Set via `APP_SECRET_CODE` environment variable or Streamlit Secrets.

---

## ⚡ Quick Start & Installation

### Prerequisites
- Python 3.9+
- `pip`

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run StockIns8 Streamlit Web Application
```bash
python main.py ui
```
*or*
```bash
streamlit run app.py
```

### Step 3: Run via Command Line Interface (CLI)

Fetch daily FII/DII activity:
```bash
python main.py cli --daily
```

Fetch shareholding changes for custom stocks:
```bash
python main.py cli --stocks RELIANCE,TCS,INFY,SBIN
```

Fetch upcoming corporate dividends:
```bash
python main.py cli --dividends --days 30
```

---

## 🧪 Running Unit Tests

To execute the test suite:

```bash
pytest
```

---

## 📜 License

MIT License. Created for analytical and research purposes.
