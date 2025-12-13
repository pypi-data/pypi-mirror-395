"""A minimal, extensible backtesting toolkit.

Current scope:
- Data utilities (load/generate sample OHLCV data)
- Core metrics: CAGR and Max Drawdown
- Simple Backtester wrapper producing metrics from price DataFrames

Design goals:
- Inputs and outputs are pandas DataFrames where practical
- Modular functions for maintainability and future expansion
"""

from .data import (
    generate_sample_data,
    load_data,
    pivot_close,
    load_sample_dataset,
    load_sample_prices,
)
from .metrics import compute_cagr, compute_max_drawdown, compute_metrics, compute_comprehensive_metrics
from .backtester import Backtester

# High-level simple interfaces
from .simple import buy_and_hold, volume_momentum, compare_strategies, quick_backtest_buy_hold, quick_backtest_volume, quick_compare

# Flexible finlab-like interfaces
from .data_loader import get, set_universe, get_data_provider, DataProvider
from .simulator import sim, BacktestResult, PositionBuilder
from .indicators import IndicatorDataFrame, IndicatorSeries, create_indicator_data
from . import signals

# Legacy strategy builder (deprecated in favor of flexible approach)
from .strategy import StrategyBuilder, simple_volume_strategy, run_strategy_and_save

__all__ = [
    # Simple data utilities
    "generate_sample_data",
    "load_data",
    "pivot_close",
    "load_sample_dataset",
    "load_sample_prices",

    # Core metrics
    "compute_cagr",
    "compute_max_drawdown",
    "compute_metrics",
    "compute_comprehensive_metrics",

    # Legacy backtester
    "Backtester",

    # Simple one-liner interfaces
    "buy_and_hold",
    "volume_momentum",
    "compare_strategies",
    "quick_backtest_buy_hold",
    "quick_backtest_volume",
    "quick_compare",

    # Flexible finlab-like interfaces
    "get",              # data.get() equivalent
    "set_universe",     # data.set_universe() equivalent
    "get_data_provider",
    "DataProvider",
    "sim",              # backtest.sim() equivalent
    "BacktestResult",
    "PositionBuilder",
    "IndicatorDataFrame",
    "IndicatorSeries",
    "create_indicator_data",
    "signals",          # Signal building module

    # Legacy (use flexible approach instead)
    "StrategyBuilder",
    "simple_volume_strategy",
    "run_strategy_and_save",
]
