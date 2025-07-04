"""
Main orchestration file for the Pairs Trading Strategy.
This script coordinates the workflow: fetch data, find pairs, simulate trades, and evaluate performance.
"""

from data_loader import fetch_price_data
from pair_selection import find_cointegrated_pairs
from trade_engine import generate_trade_signals, run_backtest
from evaluation import evaluate_results
import config

# universe and parameters
TICKERS = [
    "MSFT", "AAPL", "GOOGL", "AMZN", "META",
    "NVDA", "TSLA", "JPM", "V", "MA"
]

START_DATE = "2020-01-01"
END_DATE = "2024-12-31"


def main():
    print("Fetching price data...")
    price_df = fetch_price_data(config.TICKERS, config.START_DATE, config.END_DATE)

    print("Identifying cointegrated pairs...")
    pairs = find_cointegrated_pairs(
        price_df,
        min_corr=config.MIN_CORRELATION,
        max_pval=config.MAX_COINTEGRATION_PVAL
    )
    if not pairs:
        print("No suitable pairs found. Exiting.")
        return

    for pair in pairs:
        print(f"Trading pair: {pair[0]} / {pair[1]}")
        spread_df, z_scores = generate_trade_signals(
            price_df[pair[0]],
            price_df[pair[1]], 
            window=config.Z_SCORE_WINDOW
        )
        results = run_backtest(
            spread_df,
            z_scores,
            entry_threshold=config.ENTRY_THRESHOLD,
            exit_threshold=config.EXIT_THRESHOLD,
            initial_capital=config.INITIAL_CAPITAL
        )
        evaluate_results(results, pair)


if __name__ == "__main__":
    main()
