"""
Configuration file for the Pairs Trading Strategy.
Defines tickers, date ranges, signal thresholds, and model parameters.
"""

# ticker universe (S&P 100 sample)
TICKERS = [
    "MSFT", "AAPL", "GOOGL", "AMZN", "META",
    "NVDA", "TSLA", "JPM", "V", "MA"
]

# backtest period 
START_DATE = "2020-01-01"
END_DATE = "2024-12-31"

# z-score window
Z_SCORE_WINDOW = 60  # days

# entry/exit thresholds
ENTRY_THRESHOLD = 2.0
EXIT_THRESHOLD = 0.5

# statistical filters
MIN_CORRELATION = 0.85       # pearson correlation threshold
MAX_COINTEGRATION_PVAL = 0.05  # p-value for engle-granger test

# capital
INITIAL_CAPITAL = 1_000_000