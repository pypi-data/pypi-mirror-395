"""
Backtesting simulator similar to finlab's backtest.sim() but more flexible.
"""

import json
import pandas as pd
import numpy as np
from typing import Union, Optional, Dict, List, Any, Callable
from pathlib import Path

from .portfolio import equity_curve_from_weights
from .metrics import compute_comprehensive_metrics
from .indicators import IndicatorDataFrame


class BacktestResult:
    """Container for backtest results with finlab-compatible interface."""

    def __init__(self, positions: pd.DataFrame, prices: pd.DataFrame,
                 metrics: Dict[str, Any], trade_log: List[Dict[str, Any]],
                 simulation_params: Dict[str, Any]):
        self.positions = positions
        self.prices = prices
        self.metrics = metrics
        self._trade_log = trade_log
        self.simulation_params = simulation_params

        # Calculate equity curve
        weights = positions.astype(float)
        self.equity_curve = equity_curve_from_weights(
            prices=prices,
            weights=weights,
            exec_mode=simulation_params.get('exec_mode', 'close_same_day'),
            fee_ratio=simulation_params.get('fee_ratio', 0.001425),
            tax_ratio=simulation_params.get('tax_ratio', 0.003)
        )

    @property
    def trade_log(self):
        """Get trade log."""
        return self._trade_log

    @trade_log.setter
    def trade_log(self, value):
        """Set trade log and recompute metrics."""
        self._trade_log = value
        self._recompute_metrics_with_trade_log()

    def _recompute_metrics_with_trade_log(self):
        """Recompute metrics using trade log for accurate win rate."""
        if self._trade_log:
            self.metrics = compute_comprehensive_metrics(
                prices=self.equity_curve.to_frame('PORT'),
                benchmark=None,
                periods_per_year=252,
                risk_free_rate=0.0,
                trade_log=self._trade_log
            )

    def get_metrics(self, stats_=None) -> Dict[str, Any]:
        """Get metrics in finlab-compatible format."""
        return self.metrics

    def display(self):
        """Display backtest summary."""
        print(f"=== {self.simulation_params.get('name', 'Backtest')} Results ===")
        print(f"Period: {self.simulation_params.get('start_date')} to {self.simulation_params.get('end_date')}")
        print(f"Annual Return: {self.metrics['profitability']['annualReturn']:.4f}")
        print(f"Max Drawdown: {self.metrics['risk']['maxDrawdown']:.4f}")
        print(f"Sharpe Ratio: {self.metrics['ratio']['sharpeRatio']:.4f}")
        print(f"Win Rate: {self.metrics['winrate']['winRate']:.4f}")
        print(f"Total Signals: {len(self.trade_log)}")

    def save(self, output_file: str, trade_log_file: Optional[str] = None):
        """Save results to files."""
        # Create finlab-compatible output
        start_date = self.simulation_params.get('start_date', '')
        end_date = self.simulation_params.get('end_date', '')

        start_ts = pd.Timestamp(f"{start_date} 00:00:00+00:00").timestamp() if start_date else 0
        end_ts = pd.Timestamp(f"{end_date} 00:00:00+00:00").timestamp() if end_date else 0

        backtest_info = {
            "startDate": start_ts,
            "endDate": end_ts,
            "version": "mini-1.0.0",
            "feeRatio": self.simulation_params.get('fee_ratio', 0.001425),
            "taxRatio": self.simulation_params.get('tax_ratio', 0.003),
            "tradeAt": self.simulation_params.get('trade_at_price', 'close'),
            "market": "tw_stock",
            "freq": "1d",
            "expired": None,
            "updateDate": None,
            "nextTradingDate": None,
            "currentRebalanceDate": None,
            "nextRebalanceDate": None,
            "livePerformanceStart": None,
            "stopLoss": 1,
            "takeProfit": None,
            "trailStop": None
        }

        output = {
            'strategy_name': self.simulation_params.get('name', 'Strategy'),
            'trade_at_price': self.simulation_params.get('trade_at_price', 'close'),
            'trail_stop': None,
            'period': {'start': start_date, 'end': end_date},
            'metrics': {
                'backtest': backtest_info,
                'profitability': self.metrics['profitability'],
                'risk': self.metrics['risk'],
                'ratio': self.metrics['ratio'],
                'winrate': self.metrics['winrate'],
                'liquidity': self.metrics['liquidity']
            }
        }

        # Save main output
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        # Save trade log if requested
        if trade_log_file:
            with open(trade_log_file, 'w', encoding='utf-8') as f:
                json.dump(self.trade_log, f, ensure_ascii=False, indent=2)

        print(f"Results saved to: {output_file}")
        if trade_log_file:
            print(f"Trade log saved to: {trade_log_file}")


class PositionBuilder:
    """Helper for building position DataFrames from signals."""

    def __init__(self, universe: List[str], date_range: pd.DatetimeIndex):
        self.universe = universe
        self.date_range = date_range
        self.positions = pd.DataFrame(0.0, index=date_range, columns=universe)
        self.held = set()
        self.trade_log = []

    def apply_signals(self, entry_signals: pd.DataFrame, exit_signals: pd.DataFrame,
                     max_positions: int = 1, ranking: Optional[pd.DataFrame] = None,
                     position_size: Union[float, pd.DataFrame] = 1.0,
                     debug_data: Optional[Dict[str, pd.DataFrame]] = None) -> pd.DataFrame:
        """
        Apply entry/exit signals to build position DataFrame.

        Args:
            entry_signals: Boolean DataFrame for entry conditions
            exit_signals: Boolean DataFrame for exit conditions
            max_positions: Maximum number of positions to hold
            ranking: Optional ranking for position selection
            position_size: Position sizing (1.0 = equal weight)
            debug_data: Additional data for trade logging

        Returns:
            Position DataFrame
        """
        for date in self.date_range:
            try:
                # Get current signals
                current_entry = entry_signals.loc[date] if date in entry_signals.index else pd.Series(False, index=self.universe)
                current_exit = exit_signals.loc[date] if date in exit_signals.index else pd.Series(False, index=self.universe)

                # Process exits first
                exit_symbols = [s for s in self.held if current_exit.get(s, False)]
                exited_today = set()
                for symbol in exit_symbols:
                    self.held.discard(symbol)
                    exited_today.add(symbol)
                    self._log_trade(date, symbol, 'EXIT', debug_data)

                # Process entries (prevent same-day re-entry)
                capacity = max_positions - len(self.held)
                if capacity > 0:
                    # Get entry candidates (exclude symbols that exited today)
                    entry_candidates = [s for s in self.universe
                                      if current_entry.get(s, False) and s not in self.held and s not in exited_today]

                    # Apply ranking if provided
                    if ranking is not None and len(entry_candidates) > 0:
                        if date in ranking.index:
                            rank_scores = ranking.loc[date]
                            # Sort by ranking (descending by default)
                            entry_candidates.sort(key=lambda x: rank_scores.get(x, -np.inf), reverse=True)

                    # Select up to capacity
                    selected = entry_candidates[:capacity]
                    for symbol in selected:
                        self.held.add(symbol)
                        self._log_trade(date, symbol, 'ENTRY', debug_data)

                # Set current positions
                for symbol in self.universe:
                    if symbol in self.held:
                        size = position_size
                        if isinstance(position_size, pd.DataFrame) and date in position_size.index:
                            size = position_size.loc[date, symbol] if symbol in position_size.columns else 1.0
                        self.positions.loc[date, symbol] = float(size)
                    else:
                        self.positions.loc[date, symbol] = 0.0

            except (KeyError, IndexError):
                continue

        return self.positions

    def _log_trade(self, date: pd.Timestamp, symbol: str, action: str,
                   debug_data: Optional[Dict[str, pd.DataFrame]] = None):
        """Log trade with debug information."""
        log_entry = {
            'date': str(date.date()),
            'action': action,
            'symbol': symbol
        }

        # Add debug data if provided
        if debug_data:
            for key, df in debug_data.items():
                if date in df.index and symbol in df.columns:
                    value = df.loc[date, symbol]
                    if pd.notna(value):
                        log_entry[key] = float(value)

        self.trade_log.append(log_entry)


def sim(positions: Union[pd.DataFrame, IndicatorDataFrame],
        trade_at_price: str = 'close',
        name: str = 'Strategy',
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fee_ratio: float = 0.001425,
        tax_ratio: float = 0.003,
        benchmark: Optional[str] = None,
        **kwargs) -> BacktestResult:
    """
    Main simulation function similar to finlab's backtest.sim().

    Args:
        positions: Position DataFrame (boolean or weights)
        trade_at_price: Price type for execution ('close', 'open', etc.)
        name: Strategy name
        start_date: Start date for evaluation
        end_date: End date for evaluation
        fee_ratio: Transaction fee ratio
        tax_ratio: Tax ratio
        benchmark: Benchmark symbol (optional)
        **kwargs: Additional parameters

    Returns:
        BacktestResult object
    """
    from .data_loader import get_data_provider

    # Get price data
    data_provider = get_data_provider()
    if trade_at_price == 'close':
        prices = data_provider.get('close', list(positions.columns))
    else:
        prices = data_provider.get(f'price:{trade_at_price}', list(positions.columns))

    # Align positions with price data
    common_index = positions.index.intersection(prices.index)
    positions_aligned = positions.loc[common_index]
    prices_aligned = prices.loc[common_index]

    # Filter by date range if specified
    if start_date or end_date:
        if start_date:
            mask = positions_aligned.index >= start_date
            positions_aligned = positions_aligned.loc[mask]
            prices_aligned = prices_aligned.loc[mask]
        if end_date:
            mask = positions_aligned.index <= end_date
            positions_aligned = positions_aligned.loc[mask]
            prices_aligned = prices_aligned.loc[mask]

    # Convert to weights
    weights = positions_aligned.astype(float)

    # Calculate equity curve
    equity_curve = equity_curve_from_weights(
        prices=prices_aligned,
        weights=weights,
        exec_mode='close_same_day',
        fee_ratio=fee_ratio,
        tax_ratio=tax_ratio
    )

    # Compute metrics
    benchmark_series = None
    if benchmark:
        try:
            benchmark_data = data_provider.get('close', [benchmark])
            benchmark_series = benchmark_data[benchmark].loc[equity_curve.index]
        except:
            print(f"Warning: Could not load benchmark {benchmark}")

    metrics = compute_comprehensive_metrics(
        prices=equity_curve.to_frame('PORT'),
        benchmark=benchmark_series,
        periods_per_year=252,
        risk_free_rate=0.0
    )

    # Simulation parameters
    sim_params = {
        'name': name,
        'start_date': start_date or str(positions_aligned.index.min().date()),
        'end_date': end_date or str(positions_aligned.index.max().date()),
        'trade_at_price': trade_at_price,
        'fee_ratio': fee_ratio,
        'tax_ratio': tax_ratio,
        'exec_mode': 'close_same_day'
    }

    return BacktestResult(
        positions=positions_aligned,
        prices=prices_aligned,
        metrics=metrics,
        trade_log=[],  # Empty for basic sim - use build_strategy for detailed logging
        simulation_params=sim_params
    )