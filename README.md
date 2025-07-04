# Pairs Trading Strategy

A modular quantitative trading system that identifies statistically related stock pairs and trades their spread using a mean-reversion strategy.

## Strategy Overview

This project identifies pairs of stocks that are:

- **Highly correlated**
- **Statistically cointegrated**

It then monitors the **spread** between those stocks:

- Enters a trade when the spread deviates significantly (Z-score > ±2)
- Exits when the spread mean-reverts (Z-score < ±0.5)

Trades are executed by taking **long/short positions** on the pair to capture the convergence.

## Example Output

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