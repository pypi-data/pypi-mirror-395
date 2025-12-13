"""
Ultra-simple one-liner interfaces for common strategies.
"""

import json
import pandas as pd
import numpy as np
from typing import List

from .strategy import StrategyBuilder
from .portfolio import equity_curve_from_weights
from .metrics import compute_comprehensive_metrics


def buy_and_hold(symbols: List[str], start_date: str, end_date: str,
                 output_file: str = None, strategy_name: str = '買入持有策略'):
    """
    Ultra-simple buy and hold strategy.

    Args:
        symbols: List of symbols to hold
        start_date: Start date 'YYYY-MM-DD'
        end_date: End date 'YYYY-MM-DD'
        output_file: Optional output file name
        strategy_name: Strategy display name

    Returns:
        Results dictionary
    """
    builder = StrategyBuilder()

    # Get data and filter
    close = builder.close[symbols]
    period_mask = (close.index >= start_date) & (close.index <= end_date)
    close_period = close.loc[period_mask]

    # Always hold all symbols
    positions = pd.DataFrame(True, index=close_period.index, columns=close_period.columns)
    weights = positions.astype(float)

    # Calculate equity
    equity = equity_curve_from_weights(
        prices=close_period,
        weights=weights,
        exec_mode='close_same_day',
        fee_ratio=0.001425,
        tax_ratio=0.003
    )

    # Get metrics
    metrics = compute_comprehensive_metrics(
        prices=equity.to_frame('PORT'),
        periods_per_year=252,
        risk_free_rate=0.0
    )

    # Create result
    result = {
        'positions': positions,
        'equity': equity,
        'metrics': metrics,
        'trade_log': [],
        'strategy_params': {
            'symbols': symbols,
            'period': {'start': start_date, 'end': end_date},
            'type': 'buy_and_hold'
        }
    }

    # Save if requested
    if output_file:
        builder.save_results(result, strategy_name, output_file)

    return result


def volume_momentum(symbols: List[str], start_date: str, end_date: str,
                   vol_multiple: float = 1.2, volume_min: float = 1_000_000,
                   output_file: str = None, strategy_name: str = '價量動能策略'):
    """
    Ultra-simple volume momentum strategy.

    Args:
        symbols: List of symbols
        start_date: Start date 'YYYY-MM-DD'
        end_date: End date 'YYYY-MM-DD'
        vol_multiple: Volume spike threshold
        volume_min: Minimum volume
        output_file: Optional output file
        strategy_name: Strategy display name

    Returns:
        Results dictionary
    """
    builder = StrategyBuilder()
    result = builder.volume_spike_strategy(
        symbols=symbols,
        start_date=start_date,
        end_date=end_date,
        vol_multiple=vol_multiple,
        volume_min=volume_min
    )

    if output_file:
        builder.save_results(result, strategy_name, output_file)

    return result


def compare_strategies(strategies: List[dict], comparison_file: str = None):
    """
    Compare multiple strategy results.

    Args:
        strategies: List of strategy result dictionaries
        comparison_file: Optional file to save comparison

    Returns:
        Comparison DataFrame
    """
    comparison_data = []

    for i, strategy in enumerate(strategies):
        metrics = strategy['metrics']
        params = strategy.get('strategy_params', {})

        name = params.get('type', f'Strategy_{i+1}')
        if 'symbols' in params:
            name += f"_{'-'.join(params['symbols'])}"

        comparison_data.append({
            'Strategy': name,
            'Annual_Return': metrics['profitability']['annualReturn'],
            'Max_Drawdown': metrics['risk']['maxDrawdown'],
            'Sharpe_Ratio': metrics['ratio']['sharpeRatio'],
            'Volatility': metrics['ratio']['volatility'],
            'Win_Rate': metrics['winrate']['winRate'],
            'Total_Signals': len(strategy.get('trade_log', [])),
            'Symbols': ','.join(params.get('symbols', [])),
            'Period': f"{params.get('period', {}).get('start', '')}-{params.get('period', {}).get('end', '')}"
        })

    comparison_df = pd.DataFrame(comparison_data)

    if comparison_file:
        comparison_df.to_csv(comparison_file, index=False)
        print(f"Comparison saved to: {comparison_file}")

    # Print comparison
    print("\n=== STRATEGY COMPARISON ===")
    print(comparison_df.round(4))

    return comparison_df


# Ultra-simple one-liner functions
def quick_backtest_buy_hold(symbol: str, start: str, end: str):
    """One-liner buy and hold backtest."""
    return buy_and_hold([symbol], start, end)


def quick_backtest_volume(symbol: str, start: str, end: str, vol_mult: float = 1.2):
    """One-liner volume strategy backtest."""
    return volume_momentum([symbol], start, end, vol_mult)


def quick_compare(symbol: str, start: str, end: str):
    """Quick comparison between buy-hold and volume strategy."""
    bh = buy_and_hold([symbol], start, end)
    vol = volume_momentum([symbol], start, end)
    return compare_strategies([bh, vol])