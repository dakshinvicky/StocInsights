# 📈 Indian Market Financial Intelligence Framework

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
|   | Streamlit Web App (src/ui/app.py)     |       | GitHub Pages Dashboard (src/web/index.html|   |
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
                                             |
                                             v
+---------------------------------------------------------------------------------------------------+
|                                   EXPORT & UTILITIES LAYER                                        |
|                                                                                                   |
|   +-----------------------------------+        +----------------------------------------------+   |
|   | Formatters (src/utils/formatters.py)|       | Exporter Engine (src/utils/exporter.py)     |   |
|   | - QoQ Change formatting (+1.50%)  |        | - Generates data/fii_dii.json                |   |
|   | - Currency formatting (₹ 2,300 Cr)|        | - Generates data/dividends.json              |   |
|   +-----------------------------------+        +----------------------------------------------+   |
+---------------------------------------------------------------------------------------------------+
```

---

## 📁 Project Structure & File Map

```
AG_E/
├── .github/
│   └── workflows/
│       └── deploy.yml            # GitHub Actions CI/CD pipeline for GitHub Pages
├── data/                         # Exported static JSON datasets for GitHub Pages
│   ├── fii_dii.json              # Daily FII/DII flow & stock shareholding data
│   └── dividends.json            # Upcoming corporate dividends data
├── experiment/                   # ⚠️ LEGACY EXPERIMENT SANDBOX (Ignored by framework)
│   ├── README.md                 # Sandbox documentation
│   ├── fii_dii_fetcher.py        # Original standalone prototype script (Unexecuted)
│   └── indian_stock_fetcher.py   # Original standalone prototype script (Unexecuted)
├── src/                          # Core Production Package Framework
│   ├── __init__.py
│   ├── core/                     # Scraping & Business Logic Layer
│   │   ├── __init__.py
│   │   ├── base_fetcher.py       # Connection pooling & session base class
│   │   ├── fii_dii_fetcher.py    # FII/DII net flows & shareholding scraper
│   │   └── dividend_fetcher.py   # Corporate actions & dividend yield scraper
│   ├── utils/                    # Formatting & Exporter Utilities
│   │   ├── __init__.py
│   │   ├── formatters.py         # Currency & QoQ formatting helpers
│   │   └── exporter.py            # Static JSON/CSV exporter
│   ├── ui/                       # Streamlit Application Presentation Layer
│   │   ├── __init__.py
│   │   ├── app.py                # Main Streamlit Dashboard entrypoint
│   │   ├── tab_fii_dii.py        # Tab 1 Component: FII/DII Activity
│   │   └── tab_dividends.py      # Tab 2 Component: Upcoming Dividends
│   └── web/                      # GitHub Pages Static Web App Assets
│       ├── index.html            # Main HTML5 Dashboard
│       ├── styles.css            # Dark mode glassmorphism styles
│       └── app.js                # Dynamic JS (Search, Filter, Sort, Calculator)
├── tests/                        # Pytest Test Suite
│   ├── __init__.py
│   ├── conftest.py               # Shared test fixtures & mocks
│   ├── test_fii_dii_fetcher.py   # Unit tests for FII/DII scraper
│   ├── test_dividend_fetcher.py  # Unit tests for Dividend scraper
│   └── test_exporter.py          # Unit tests for static exporter
├── app.py                        # Shortcut entrypoint for Streamlit Cloud
├── generate_data.py              # CLI entrypoint for static JSON generation
├── main.py                       # Unified CLI & Application Controller
├── pyproject.toml                 # PyPA package configuration
├── requirements.txt              # Required dependencies
└── README.md                     # Comprehensive system documentation
```

> [!WARNING]
> **Experiments Folder Note**: The `experiment/` directory contains original prototype scripts (`fii_dii_fetcher.py` and `indian_stock_fetcher.py`). These scripts are preserved for historical reference **only** and are **ignored/never executed** by the production application.

---

## ⚡ Installation & Quick Start

### Prerequisites
- Python 3.9+
- `pip`

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```
*(Optional: Install in editable mode via `pip install -e .`)*

---

## 🚀 Running the Application

### Option A: Launch Streamlit Web App (Local Server)
```bash
python main.py ui
```
*or*
```bash
streamlit run app.py
```
App will open in your browser at `http://localhost:8501`.

### Option B: Command Line Interface (CLI)

1. **Daily FII / DII Net Market Activity**:
   ```bash
   python main.py cli --daily
   ```

2. **Quarterly Shareholding Changes for Custom Tickers**:
   ```bash
   python main.py cli --stocks RELIANCE,TCS,INFY,HDFCBANK,SBIN
   ```

3. **Upcoming Corporate Dividends**:
   ```bash
   python main.py cli --dividends --days 30
   ```

### Option C: Data Exporter (Static Site Generator)
Generate JSON files in `data/` for static hosting:
```bash
python main.py generate
```

---

## 🌐 Deploying to GitHub Pages

GitHub Pages is a static hosting platform. Because it cannot execute Python backends, the repository includes a complete automated CI/CD pipeline using **GitHub Actions**.

### How it Works:
1. **GitHub Action Workflow** (`.github/workflows/deploy.yml`) runs on a scheduled cron trigger (daily at 01:00 AM UTC / 06:30 AM IST) or whenever code is pushed to `main`/`master`.
2. The workflow executes `generate_data.py`, which calls `export_json_data()`.
3. It fetches fresh data from NSE/Yahoo, updates `data/fii_dii.json` and `data/dividends.json`, and commits them to the `gh-pages` branch.
4. `src/web/index.html` loads the pre-rendered JSON files seamlessly with zero CORS issues!

### One-Time Setup Instructions:
1. Push your repository to GitHub.
2. Go to **Settings** -> **Pages**.
3. Under **Source**, select **Deploy from a branch**.
4. Choose Branch: `gh-pages`, Folder: `/ (root)`. Click **Save**.
5. Your dashboard will be live at `https://<your-username>.github.io/<repo-name>/`.

---

## ☁️ Deploying to Streamlit Community Cloud

To host the live interactive Python application for free:

1. Push your repository to GitHub.
2. Sign in to [Streamlit Community Cloud](https://streamlit.io/cloud).
3. Click **New App**, select your GitHub repository, branch `main`, and set **Main file path** to `app.py` (or `src/ui/app.py`).
4. Click **Deploy**.

---

## 🧪 Testing Suite

Run the `pytest` test suite:
```bash
pytest
```
*Sample Test Output:*
```
============================= test session starts =============================
collected 5 items

tests/test_dividend_fetcher.py ..                                        [ 40%]
tests/test_exporter.py .                                                 [ 60%]
tests/test_fii_dii_fetcher.py ..                                         [100%]

============================= 5 passed in 25.12s ==============================
```

---

## 📚 API Reference

### `FIIDIIFetcher` (`src.core.fii_dii_fetcher`)
- `fetch_daily_fii_dii() -> pd.DataFrame`: Returns daily FII/DII Net Buy/Sell figures in Cash Market.
- `fetch_cmp(symbol: str) -> Optional[float]`: Returns live Current Market Price from Yahoo Finance.
- `fetch_stock_shareholding(symbol: str) -> Dict[str, Any]`: Returns quarterly shareholding percentages (FII %, DII %, Promoter %, Public %) and QoQ changes.
- `fetch_stocks_shareholding_batch(symbols: List[str]) -> pd.DataFrame`: Concurrently fetches shareholding changes for multiple stocks using thread pools.

### `DividendFetcher` (`src.core.dividend_fetcher`)
- `fetch_upcoming_dividends(days_ahead: int, symbol: Optional[str]) -> pd.DataFrame`: Returns upcoming dividend dates, dividend per share, CMP, and estimated dividend return per ₹1,00,000 invested.

---

## 📜 License
MIT License. Created for analytical and research purposes.
