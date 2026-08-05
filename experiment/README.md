# 🧪 Experiment / Sandbox Folder

This directory contains early prototype standalone scripts:
- `fii_dii_fetcher.py`: Early prototype script for fetching FII/DII data.
- `indian_stock_fetcher.py`: Early prototype script for fetching dividend actions.

> [!WARNING]
> **IMPORTANT ARCHITECTURAL NOTE:**
> These files are preserved for historical reference **only**. They are **NOT** executed, imported, or called by any component of the production framework. All active, production-grade logic is located inside the `src/` directory package (`src/core/fii_dii_fetcher.py` and `src/core/dividend_fetcher.py`).
