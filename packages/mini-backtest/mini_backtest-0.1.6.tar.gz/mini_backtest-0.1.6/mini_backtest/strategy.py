"""
Strategy building utilities for mini-backtest framework.
Provides simple interfaces for common trading strategy patterns.
"""

import json
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Callable, Any

from .portfolio import equity_curve_from_weights
from .metrics import compute_comprehensive_metrics


class StrategyBuilder:
    """Simple strategy builder with comprehensive logging and debugging."""

    def __init__(self, data_file: str = 'data.json'):
        """Initialize with market data from JSON file."""
        with open(data_file, 'r', encoding='utf-8') as f:
            payload = json.load(f)

        self.close = self._df_from_matrix(payload["close"]).astype(float)
        self.volume = self._df_from_matrix(payload["volume"]).astype(float)
        self.trade_log = []

    def _df_from_matrix(self, obj: dict) -> pd.DataFrame:
        """Convert JSON matrix format to DataFrame."""
        idx = pd.DatetimeIndex(pd.to_datetime(obj["index"]))
        cols = obj["columns"]
        data = obj["data"]
        return pd.DataFrame(data, index=idx, columns=cols)

    def filter_symbols(self, symbols: List[str]) -> 'StrategyBuilder':
        """Filter to specific symbols."""
        self.close = self.close[symbols]
        self.volume = self.volume[symbols]
        return self

    def volume_spike_strategy(
        self,
        symbols: List[str],
        start_date: str,
        end_date: str,
        vol_multiple: float = 1.2,
        volume_min: float = 1_000_000,
        ma_periods: Tuple[int, int, int] = (5, 10, 20),
        max_positions: int = 1
    ) -> Dict[str, Any]:
        """
        Simple volume spike + moving average strategy.

        Entry: Volume spike + MA trend up
        Exit: Price below MA10 or MA trend down
        """

        # Filter data and period
        close = self.close[symbols]
        volume = self.volume[symbols]

        # Calculate indicators
        ma5 = close.rolling(window=ma_periods[0]).mean()
        ma10 = close.rolling(window=ma_periods[1]).mean()
        ma20 = close.rolling(window=ma_periods[2]).mean()
        prev_volume = volume.shift(1)

        # Entry/exit conditions
        entry_cond = (
            (volume >= prev_volume * vol_multiple) &
            (volume >= volume_min) &
            (ma5 > ma10) & (ma10 > ma20)
        )

        exit_cond = (
            (ma5 < ma10) | (ma10 < ma20) | (close < ma10)
        )

        # Filter to strategy period
        period_mask = (close.index >= start_date) & (close.index <= end_date)
        close_period = close.loc[period_mask]
        volume_period = volume.loc[period_mask]
        entry_period = entry_cond.loc[period_mask]
        exit_period = exit_cond.loc[period_mask]
        ma5_period = ma5.loc[period_mask]
        ma10_period = ma10.loc[period_mask]
        ma20_period = ma20.loc[period_mask]
        prev_vol_period = prev_volume.loc[period_mask]

        # Build positions with logging
        positions, trade_log = self._build_positions_with_log(
            close_period, volume_period, entry_period, exit_period,
            ma5_period, ma10_period, ma20_period, prev_vol_period,
            vol_multiple, volume_min, max_positions
        )

        # Calculate returns
        weights = positions.astype(float)
        equity = equity_curve_from_weights(
            prices=close_period,
            weights=weights,
            exec_mode='close_same_day',
            fee_ratio=0.001425,
            tax_ratio=0.003
        )

        # Compute metrics
        metrics = compute_comprehensive_metrics(
            prices=equity.to_frame('PORT'),
            benchmark=None,
            periods_per_year=252,
            risk_free_rate=0.0
        )

        return {
            'positions': positions,
            'equity': equity,
            'metrics': metrics,
            'trade_log': trade_log,
            'strategy_params': {
                'symbols': symbols,
                'period': {'start': start_date, 'end': end_date},
                'vol_multiple': vol_multiple,
                'volume_min': volume_min,
                'ma_periods': ma_periods,
                'max_positions': max_positions
            }
        }

    def _build_positions_with_log(self, close_df, volume_df, entry_cond, exit_cond,
                                  ma5_df, ma10_df, ma20_df, prev_vol_df,
                                  vol_multiple, volume_min, max_positions):
        """Build positions with detailed trade logging."""
        dates = close_df.index
        symbols = list(close_df.columns)
        held = set()
        positions = pd.DataFrame(False, index=dates, columns=symbols)
        trade_log = []

        for t in dates:
            try:
                current_close = close_df.loc[t]
                current_volume = volume_df.loc[t]
                prev_volume = prev_vol_df.loc[t] if t in prev_vol_df.index else pd.Series(dtype=float)
                ma5_val = ma5_df.loc[t] if t in ma5_df.index else pd.Series(dtype=float)
                ma10_val = ma10_df.loc[t] if t in ma10_df.index else pd.Series(dtype=float)
                ma20_val = ma20_df.loc[t] if t in ma20_df.index else pd.Series(dtype=float)

                ex = exit_cond.loc[t] if t in exit_cond.index else pd.Series(False, index=symbols)
                ent = entry_cond.loc[t] if t in entry_cond.index else pd.Series(False, index=symbols)

                # Process exits first
                for symbol in list(held):
                    if bool(ex.get(symbol, False)):
                        held.discard(symbol)
                        trade_log.append({
                            'date': str(t.date()),
                            'action': 'EXIT',
                            'symbol': symbol,
                            'price': float(current_close[symbol]),
                            'volume': float(current_volume[symbol]),
                            'prev_volume': float(prev_volume.get(symbol, 0)) if not pd.isna(prev_volume.get(symbol, np.nan)) else None,
                            'ma5': float(ma5_val.get(symbol, 0)) if not pd.isna(ma5_val.get(symbol, np.nan)) else None,
                            'ma10': float(ma10_val.get(symbol, 0)) if not pd.isna(ma10_val.get(symbol, np.nan)) else None,
                            'ma20': float(ma20_val.get(symbol, 0)) if not pd.isna(ma20_val.get(symbol, np.nan)) else None,
                            'reason': 'exit_signal_triggered'
                        })

                # Process entries
                for symbol in symbols:
                    if symbol not in held and len(held) < max_positions and bool(ent.get(symbol, False)):
                        vol_spike = (current_volume[symbol] >= prev_volume.get(symbol, 0) * vol_multiple
                                   if not pd.isna(prev_volume.get(symbol, np.nan)) else False)
                        vol_min_check = current_volume[symbol] >= volume_min
                        ma_trend = (ma5_val.get(symbol, 0) > ma10_val.get(symbol, 0) and
                                  ma10_val.get(symbol, 0) > ma20_val.get(symbol, 0))

                        held.add(symbol)
                        trade_log.append({
                            'date': str(t.date()),
                            'action': 'ENTRY',
                            'symbol': symbol,
                            'price': float(current_close[symbol]),
                            'volume': float(current_volume[symbol]),
                            'prev_volume': float(prev_volume.get(symbol, 0)) if not pd.isna(prev_volume.get(symbol, np.nan)) else None,
                            'ma5': float(ma5_val.get(symbol, 0)) if not pd.isna(ma5_val.get(symbol, np.nan)) else None,
                            'ma10': float(ma10_val.get(symbol, 0)) if not pd.isna(ma10_val.get(symbol, np.nan)) else None,
                            'ma20': float(ma20_val.get(symbol, 0)) if not pd.isna(ma20_val.get(symbol, np.nan)) else None,
                            'vol_spike': bool(vol_spike),
                            'vol_min_check': bool(vol_min_check),
                            'ma_trend': bool(ma_trend)
                        })

                # Set current positions
                if held:
                    positions.loc[t, list(held)] = True

            except (KeyError, IndexError):
                continue

        return positions, trade_log

    def create_finlab_output(self, result: Dict[str, Any], strategy_name: str) -> Dict[str, Any]:
        """Create finlab-compatible output format."""
        params = result['strategy_params']

        # Create timestamps
        start_ts = pd.Timestamp(f"{params['period']['start']} 00:00:00+00:00").timestamp()
        end_ts = pd.Timestamp(f"{params['period']['end']} 00:00:00+00:00").timestamp()

        backtest_info = {
            "startDate": start_ts,
            "endDate": end_ts,
            "version": "mini-1.0.0",
            "feeRatio": 0.001425,
            "taxRatio": 0.003,
            "tradeAt": "close",
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

        return {
            'strategy_name': strategy_name,
            'trade_at_price': 'close',
            'trail_stop': None,
            'period': params['period'],
            'metrics': {
                'backtest': backtest_info,
                'profitability': result['metrics']['profitability'],
                'risk': result['metrics']['risk'],
                'ratio': result['metrics']['ratio'],
                'winrate': result['metrics']['winrate'],
                'liquidity': result['metrics']['liquidity']
            }
        }

    def save_results(self, result: Dict[str, Any], strategy_name: str,
                     output_file: str, trade_log_file: str = None):
        """Save strategy results to files."""
        # Save main output
        finlab_output = self.create_finlab_output(result, strategy_name)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(finlab_output, f, ensure_ascii=False, indent=2)

        # Save trade log
        if trade_log_file:
            with open(trade_log_file, 'w', encoding='utf-8') as f:
                json.dump(result['trade_log'], f, ensure_ascii=False, indent=2)

        # Print summary
        metrics = result['metrics']
        print(f"=== {strategy_name} Results ===")
        print(f"Annual Return: {metrics['profitability']['annualReturn']:.4f}")
        print(f"Max Drawdown: {metrics['risk']['maxDrawdown']:.4f}")
        print(f"Sharpe Ratio: {metrics['ratio']['sharpeRatio']:.4f}")
        print(f"Win Rate: {metrics['winrate']['winRate']:.4f}")
        print(f"Total signals: {len(result['trade_log'])}")
        print(f"Results saved to: {output_file}")
        if trade_log_file:
            print(f"Trade log saved to: {trade_log_file}")


def simple_volume_strategy(symbols: List[str], start_date: str, end_date: str,
                          vol_multiple: float = 1.2, volume_min: float = 1_000_000) -> Dict[str, Any]:
    """
    Ultra-simple interface for volume spike strategy.

    Args:
        symbols: List of stock symbols
        start_date: Start date string 'YYYY-MM-DD'
        end_date: End date string 'YYYY-MM-DD'
        vol_multiple: Volume spike threshold (default 1.2x)
        volume_min: Minimum volume threshold

    Returns:
        Complete strategy results with metrics and trade log
    """
    builder = StrategyBuilder()
    return builder.volume_spike_strategy(
        symbols=symbols,
        start_date=start_date,
        end_date=end_date,
        vol_multiple=vol_multiple,
        volume_min=volume_min
    )


def run_strategy_and_save(symbols: List[str], start_date: str, end_date: str,
                         strategy_name: str, output_file: str,
                         vol_multiple: float = 1.2, volume_min: float = 1_000_000):
    """
    Complete one-liner strategy execution and save.

    Args:
        symbols: List of stock symbols
        start_date: Start date 'YYYY-MM-DD'
        end_date: End date 'YYYY-MM-DD'
        strategy_name: Name for the strategy
        output_file: Output JSON file name
        vol_multiple: Volume spike threshold
        volume_min: Minimum volume threshold
    """
    builder = StrategyBuilder()
    result = builder.volume_spike_strategy(
        symbols=symbols,
        start_date=start_date,
        end_date=end_date,
        vol_multiple=vol_multiple,
        volume_min=volume_min
    )

    trade_log_file = output_file.replace('.json', '-trade-log.json')
    builder.save_results(result, strategy_name, output_file, trade_log_file)

    return result