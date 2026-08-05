"""
Unified CLI & Application Entrypoint for StockIns8 Framework.
"""

import sys
import argparse
import subprocess
from src.core.fii_dii_fetcher import FIIDIIFetcher
from src.core.dividend_fetcher import DividendFetcher
from src.utils.formatters import format_dataframe_changes
from src.utils.exporter import export_json_data


def run_cli_fii_dii(args):
    fetcher = FIIDIIFetcher()
    if args.daily:
        print("\n[StockIns8] Daily FII / DII Market Activity (Cash Market)\n")
        df = fetcher.fetch_daily_fii_dii()
        if not df.empty:
            print(df.to_string(index=False))
        else:
            print("No daily activity data found.")
    elif args.stocks:
        symbols = [s.strip() for s in args.stocks.split(",") if s.strip()]
        print(f"\n[StockIns8] Shareholding Changes for {len(symbols)} stocks\n")
        df = fetcher.fetch_stocks_shareholding_batch(symbols)
        if not df.empty:
            print(format_dataframe_changes(df).to_string(index=False))
    else:
        print("Please specify --daily or --stocks 'RELIANCE,TCS'")


def run_cli_dividends(args):
    fetcher = DividendFetcher()
    print(f"\n[StockIns8] Upcoming Dividends (Next {args.days} days)\n")
    df = fetcher.fetch_upcoming_dividends(days_ahead=args.days, symbol=args.symbol)
    if not df.empty:
        print(df.to_string(index=False))
    else:
        print("No upcoming dividends found.")


def main():
    parser = argparse.ArgumentParser(description="StockIns8 Financial Intelligence Framework CLI")
    subparsers = parser.add_subparsers(dest="command", help="Sub-command to execute")

    # CLI sub-command
    cli_parser = subparsers.add_parser("cli", help="Run in Command Line Mode")
    cli_parser.add_argument("--daily", action="store_true", help="Fetch daily FII/DII net market flows")
    cli_parser.add_argument("--stocks", type=str, help="Comma-separated stock symbols")
    cli_parser.add_argument("--dividends", action="store_true", help="Fetch upcoming dividends")
    cli_parser.add_argument("--days", type=int, default=30, help="Lookahead days for dividends")
    cli_parser.add_argument("--symbol", type=str, help="Filter dividend stock symbol")

    # UI sub-command
    subparsers.add_parser("ui", help="Launch Streamlit Web Dashboard")

    # Data Generator sub-command
    subparsers.add_parser("generate", help="Generate static JSON files for GitHub Pages")

    args = parser.parse_args()

    if args.command == "cli":
        if args.dividends:
            run_cli_dividends(args)
        else:
            run_cli_fii_dii(args)
    elif args.command == "ui":
        print("Launching StockIns8 Streamlit Web App...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "src/ui/app.py"])
    elif args.command == "generate":
        export_json_data("data")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
