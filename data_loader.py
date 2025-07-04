"""
This module handles data fetching for pairs trading.
It retrieves historical adjusted close prices for a list of tickers using yfinance.
"""

import yfinance as yf
import pandas as pd
from typing import List


def fetch_price_data(tickers: List[str], start: str, end: str) -> pd.DataFrame:
    """
    Fetches adjusted close prices for a list of tickers.

    Args:
        tickers (List[str]): List of stock tickers (e.g., ['AAPL', 'MSFT']).
        start (str): Start date (YYYY-MM-DD).
        end (str): End date (YYYY-MM-DD).

    Returns:
        pd.DataFrame: DataFrame with date index and tickers as columns.
    """
    data = yf.download(tickers, start=start, end=end, auto_adjust=True)["Close"]
    if isinstance(data, pd.Series):
        data = data.to_frame()
    return data.dropna(how="all")