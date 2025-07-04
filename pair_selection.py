"""
This module identifies statistically valid trading pairs
using Pearson correlation and the Engle-Granger cointegration test.
"""

import pandas as pd
from statsmodels.tsa.stattools import coint
from itertools import combinations
from typing import List, Tuple


def find_cointegrated_pairs(
    price_df: pd.DataFrame,
    min_corr: float = 0.85,
    max_pval: float = 0.05
) -> List[Tuple[str, str]]:
    """
    Identifies cointegrated pairs from a price DataFrame.

    Args:
        price_df (pd.DataFrame): DataFrame of adjusted close prices.
        min_corr (float): Minimum Pearson correlation to consider a pair.
        max_pval (float): Maximum p-value from coint test to accept cointegration.

    Returns:
        List[Tuple[str, str]]: List of selected (ticker_A, ticker_B) pairs.
    """
    selected_pairs = []
    tickers = price_df.columns.tolist()

    for (ticker_a, ticker_b) in combinations(tickers, 2):
        series_a = price_df[ticker_a]
        series_b = price_df[ticker_b]

        # filter out pairs with missing data
        if series_a.isnull().any() or series_b.isnull().any():
            continue

        corr = series_a.corr(series_b)
        if corr < min_corr:
            continue

        _, pval, _ = coint(series_a, series_b)
        if pval < max_pval:
            selected_pairs.append((ticker_a, ticker_b))

    return selected_pairs