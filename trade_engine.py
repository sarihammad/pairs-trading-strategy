"""
This module implements the trade logic for a pairs trading strategy.

Includes:
- Spread and z-score calculation
- Signal generation based on z-score thresholds
- Basic PnL simulation with long/short spread positions
"""

import pandas as pd
from typing import Tuple


def generate_trade_signals(
    series_a: pd.Series,
    series_b: pd.Series,
    window: int = 60
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Computes spread and rolling z-score between two price series.

    Args:
        series_a (pd.Series): First asset's price series (e.g., A).
        series_b (pd.Series): Second asset's price series (e.g., B).
        window (int): Rolling window to compute z-score.

    Returns:
        Tuple:
            - pd.DataFrame: DataFrame containing spread, positions, PnL, etc.
            - pd.Series: Z-score series
    """
    hedge_ratio = series_a.cov(series_b) / series_b.var()
    spread = series_a - hedge_ratio * series_b

    spread_mean = spread.rolling(window=window).mean()
    spread_std = spread.rolling(window=window).std()
    z_score = (spread - spread_mean) / spread_std

    df = pd.DataFrame({
        "Price_A": series_a,
        "Price_B": series_b,
        "Spread": spread,
        "ZScore": z_score
    })

    return df.dropna(), z_score.dropna()


def run_backtest(
    df: pd.DataFrame,
    z_scores: pd.Series,
    entry_threshold: float = 2.0,
    exit_threshold: float = 0.5,
    initial_capital: float = 1_000_000
) -> pd.DataFrame:
    """
    Runs a simple backtest for pairs trading with mean reversion signals.

    Args:
        df (pd.DataFrame): Spread + price data.
        z_scores (pd.Series): Z-score of the spread.
        entry_threshold (float): Z-score to trigger trade entry.
        exit_threshold (float): Z-score to exit trade.
        initial_capital (float): Starting cash for simulation.

    Returns:
        pd.DataFrame: DataFrame with position info, daily PnL, and portfolio value.
    """
    df = df.copy()
    df["Position"] = 0  # 1 = long spread, -1 = short spread, 0 = no position

    # signal generation
    for i in range(1, len(df)):
        if df["Position"].iloc[i - 1] == 0:
            if df["ZScore"].iloc[i] > entry_threshold:
                df.at[df.index[i], "Position"] = -1
            elif df["ZScore"].iloc[i] < -entry_threshold:
                df.at[df.index[i], "Position"] = 1
        else:
            if abs(df["ZScore"].iloc[i]) < exit_threshold:
                df.at[df.index[i], "Position"] = 0
            else:
                df.at[df.index[i], "Position"] = df["Position"].iloc[i - 1]

    # forward fill positions
    df["Position"] = df["Position"].ffill().fillna(0)

    # daily pnl based on change in spread
    df["Spread_Return"] = df["Spread"].diff()
    df["PnL"] = df["Spread_Return"] * df["Position"]
    df["CumulativePnL"] = df["PnL"].cumsum()
    df["PortfolioValue"] = initial_capital + df["CumulativePnL"]

    return df