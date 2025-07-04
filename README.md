# Pairs Trading Strategy

A quantitative trading system that identifies statistically related stock pairs, and trades their spread using a mean-reversion strategy.

## Strategy Overview

This project identifies pairs of stocks that are:

- Highly correlated using Pearson correlation
- Statistically cointegrated using the Engle-Granger cointegration test

Once identified, the spread between the two stocks is tracked over time:

- A Z-score is computed using a rolling window (default: 60 days)
- A trade is entered when the Z-score exceeds a threshold (e.g. ±2), indicating a divergence
- The position is exited when the spread mean-reverts (Z-score returns within ±0.5)

Trades are executed as:

- Long the underpriced asset
- Short the overpriced asset

This allows the strategy to profit when the price relationship converges again.

## Output

- Equity curve of the portfolio  
- Z-score plot showing entry/exit points  
- Position chart  
- Final stats:
  
  - Total return
  - Sharpe ratio
  - Max drawdown

## How to Run

```bash
git clone https://github.com/sarihammad/pairs-trading-strategy.git
cd pairs-trading-strategy

pip install -r requirements.txt

python main.py
