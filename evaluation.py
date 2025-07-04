"""
This module evaluates the performance of the pairs trading strategy.

Includes:
- Portfolio equity curve plotting
- Z-score and signal visualization
- Sharpe ratio calculation
- Summary statistics
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple


def evaluate_results(df: pd.DataFrame, pair: Tuple[str, str]) -> None:
    """
    Plots performance and prints evaluation metrics for a trading pair.

    Args:
        df (pd.DataFrame): DataFrame with PortfolioValue, Position, ZScore, etc.
        pair (Tuple[str, str]): Tuple of traded tickers (A, B).
    """
    ticker_a, ticker_b = pair
    _, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    # equity curve
    axs[0].plot(df["PortfolioValue"], label="Portfolio Value", color="navy")
    axs[0].set_title(f"Equity Curve: {ticker_a} / {ticker_b}")
    axs[0].set_ylabel("Portfolio Value ($)")
    axs[0].legend()
    axs[0].grid(True)

    # z-score plot
    axs[1].plot(df["ZScore"], color="darkgreen", label="Z-Score")
    axs[1].axhline(2, linestyle="--", color="red", alpha=0.6)
    axs[1].axhline(-2, linestyle="--", color="red", alpha=0.6)
    axs[1].axhline(0, linestyle="--", color="gray", alpha=0.3)
    axs[1].set_ylabel("Z-Score")
    axs[1].set_title("Spread Z-Score and Entry Points")
    axs[1].legend()
    axs[1].grid(True)

    # position plot
    axs[2].plot(df["Position"], drawstyle="steps-post", color="purple")
    axs[2].set_ylabel("Position")
    axs[2].set_title("Position Over Time")
    axs[2].set_xlabel("Date")
    axs[2].grid(True)

    plt.tight_layout()
    plt.show()

    # final stats
    sharpe = calculate_sharpe(df["PnL"])
    max_dd = calculate_max_drawdown(df["PortfolioValue"])
    total_return = (df["PortfolioValue"].iloc[-1] / df["PortfolioValue"].iloc[0]) - 1

    print(f"Performance Summary for {ticker_a} / {ticker_b}")
    print(f"Final Portfolio Value: ${df['PortfolioValue'].iloc[-1]:,.2f}")
    print(f"Total Return: {total_return:.2%}")
    print(f"Sharpe Ratio: {sharpe:.2f}")
    print(f"Max Drawdown: {max_dd:.2%}")


def calculate_sharpe(returns: pd.Series, risk_free_rate: float = 0.0) -> float:
    """
    Calculates annualized Sharpe ratio.

    Args:
        returns (pd.Series): Daily returns or PnL stream.
        risk_free_rate (float): Daily risk-free rate (default 0.0).

    Returns:
        float: Sharpe ratio (annualized).
    """
    if returns.std() == 0:
        return 0.0
    excess_returns = returns - risk_free_rate
    return (np.sqrt(252) * excess_returns.mean()) / excess_returns.std()


def calculate_max_drawdown(portfolio: pd.Series) -> float:
    """
    Calculates maximum drawdown of a portfolio.

    Args:
        portfolio (pd.Series): Portfolio value over time.

    Returns:
        float: Max drawdown as a negative percentage.
    """
    cumulative_max = portfolio.cummax()
    drawdown = (portfolio - cumulative_max) / cumulative_max
    return drawdown.min()