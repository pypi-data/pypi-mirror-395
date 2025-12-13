Mini Backtest
==============

A lightweight, pandas‑first toolkit for quick backtesting experiments. It focuses on the essentials: generating reproducible sample OHLCV data, transforming data into analysis‑friendly shapes, and computing core performance metrics such as CAGR and Maximum Drawdown. The API is intentionally small, composable, and easy to integrate with your own research code.

Features
--------

- Simple, pandas‑centric API for inputs and outputs.
- Deterministic sample data generation for demos and tests.
- Core metrics: CAGR and Maximum Drawdown.
- Minimal `Backtester` wrapper that computes metrics from close‑price DataFrames.

Installation
------------

```
pip install mini_backtest
```

Quick Start
-----------

```python
from mini_backtest import load_sample_prices, Backtester

# Load a reproducible wide close‑price DataFrame (index=date, columns=symbol)
prices = load_sample_prices(n_symbols=10, start="2020-01-01", end="2022-12-31", seed=42)

# Compute per‑symbol metrics
res = Backtester(prices).run()
print(res.head())
```

API Overview
------------

- `mini_backtest.data`
  - `load_sample_dataset(n_symbols=10, start="2020-01-01", end="2022-12-31", seed=42) -> pd.DataFrame`
    - Returns a reproducible tidy OHLCV DataFrame without writing to disk.
  - `load_sample_prices(n_symbols=10, start="2020-01-01", end="2022-12-31", seed=42) -> pd.DataFrame`
    - Returns a reproducible wide close-price DataFrame.
  - `generate_sample_data(file_path, symbols=None, start="2020-01-01", end="2022-12-31", seed=42) -> Path`
    - Writes the simulated dataset to a JSON file for offline use.
  - `load_data(file_path) -> pd.DataFrame`
    - Loads the JSON dataset into a tidy DataFrame with columns: `date, symbol, open, high, low, close, volume`.
  - `pivot_close(df) -> pd.DataFrame`
    - Pivots the tidy data to a wide close‑price DataFrame (index = date, columns = symbols).

- `mini_backtest.metrics`
  - `compute_cagr(prices, periods_per_year=252) -> pd.Series`
  - `compute_max_drawdown(prices) -> pd.Series`
  - `compute_metrics(prices, periods_per_year=252) -> pd.DataFrame`

- `mini_backtest.portfolio`
  - `calc_returns(prices) -> pd.DataFrame`
    - Converts a wide price DataFrame into single-period simple returns (date-sorted).
  - `equity_curve_from_weights(prices, weights, start_value=1.0) -> pd.Series`
    - Computes a portfolio equity curve using previous-day weights to avoid lookahead.

- `mini_backtest.backtester`
  - `Backtester(prices: pd.DataFrame, periods_per_year: int = 252)`
  - `Backtester.run() -> pd.DataFrame`

Design Notes
------------

- This project is intentionally minimal and metric‑oriented. It does not attempt to be an event‑driven engine or a full execution simulator.
- Inputs and outputs are pandas DataFrames to maximize composability with your own research pipeline.

Requirements
------------

- Python 3.8+
- `pandas>=1.4`, `numpy>=1.22`

Testing (optional)
------------------

If you clone the repository and want to run the tests:

```
pytest -q
```

Versioning
----------

This package follows semantic versioning for public APIs exposed in `mini_backtest`.

Security & Privacy
------------------

The published distribution includes only the `mini_backtest` package and this README. It does not ship any credentials, local configuration, or example datasets.

More Examples
-------------

The following examples demonstrate how to use `mini_backtest` to run simple backtests and both write results to a file and print them. These examples require no external data; a reproducible OHLCV sample is generated on demand with a fixed random seed.

Example 1: Equal-weight Buy & Hold
----------------------------------

```python
from pathlib import Path
import numpy as np
import pandas as pd
from mini_backtest import load_sample_prices, Backtester
from mini_backtest.portfolio import equity_curve_from_weights

# 1) Load reproducible sample prices (wide DataFrame)
prices = load_sample_prices(seed=42)

# 2) Build equal-weight portfolio weights
n = prices.shape[1]
weights = pd.DataFrame(
    np.full_like(prices, fill_value=1.0 / n, dtype=float),
    index=prices.index,
    columns=prices.columns,
)

# 3) Compute equity using previous-day weights (no lookahead)
equity = equity_curve_from_weights(prices, weights, start_value=1.0)

# 4) Compute portfolio-level metrics (CAGR / Max Drawdown)
bt = Backtester(prices=equity.to_frame())
metrics = bt.run()

# 5) Write to file + print
out_path = Path('examples/output_buy_and_hold.json')
out_path.parent.mkdir(parents=True, exist_ok=True)
metrics.reset_index().to_json(out_path, orient='records')
print('Saved:', out_path)
print(metrics)
```

Example 2: Moving Average Crossover (SMA 20/50)
-----------------------------------------------

```python
from pathlib import Path
import numpy as np
from mini_backtest import load_sample_prices, Backtester
from mini_backtest.portfolio import equity_curve_from_weights

short, long = 20, 50
prices = load_sample_prices(seed=42)

sma_s = prices.rolling(short, min_periods=1).mean()
sma_l = prices.rolling(long, min_periods=1).mean()
long_mask = (sma_s > sma_l).astype(float)
denom = long_mask.sum(axis=1).replace(0, np.nan)
weights = long_mask.div(denom, axis=0).fillna(0.0)  # Equal-weight among symbols with active signal

equity = equity_curve_from_weights(prices, weights, start_value=1.0)
metrics = Backtester(prices=equity.to_frame()).run()

out_path = Path('examples/output_ma_crossover.json')
out_path.parent.mkdir(parents=True, exist_ok=True)
metrics.reset_index().to_json(out_path, orient='records')
print('Saved:', out_path)
print(metrics)
```

Example 3: Momentum Timing (Top 30% equal-weight)
-------------------------------------------------

```python
from pathlib import Path
import numpy as np
from mini_backtest import load_sample_prices, Backtester
from mini_backtest.portfolio import equity_curve_from_weights

lookback, top_pct = 20, 0.7  # Rank by past 20-day return; select percentile >= 0.7
prices = load_sample_prices(seed=42)

momentum = prices.pct_change(lookback)
ranks = momentum.rank(axis=1, pct=True)
long_mask = (ranks >= top_pct).astype(float)
denom = long_mask.sum(axis=1).replace(0, np.nan)
weights = long_mask.div(denom, axis=0).fillna(0.0)

equity = equity_curve_from_weights(prices, weights, start_value=1.0)
metrics = Backtester(prices=equity.to_frame()).run()

out_path = Path('examples/output_momentum_top30.json')
out_path.parent.mkdir(parents=True, exist_ok=True)
metrics.reset_index().to_json(out_path, orient='records')
print('Saved:', out_path)
print(metrics)
```

Notes
-----

- Examples use `load_sample_prices()` to create in-memory, reproducible sample data; results are written to the `examples/` directory.
- You can also run the included scripts directly (see more strategies in `examples/`):
  - `python examples/buy_and_hold.py`
  - `python examples/ma_crossover.py`
  - `python examples/momentum_top30.py`
