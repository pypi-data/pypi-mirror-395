"""
Signal generation utilities - provides building blocks for strategy construction.
"""

import pandas as pd
import numpy as np
from typing import Union, Optional, Callable, Any

from .indicators import IndicatorDataFrame, IndicatorSeries


class SignalBuilder:
    """Helper for building complex trading signals."""

    def __init__(self):
        self.signals = {}
        self.conditions = {}

    def add_signal(self, name: str, condition: Union[pd.DataFrame, pd.Series]) -> 'SignalBuilder':
        """Add a named signal condition."""
        self.signals[name] = condition
        return self

    def combine_and(self, *signal_names) -> Union[pd.DataFrame, pd.Series]:
        """Combine multiple signals with AND logic."""
        if not signal_names:
            raise ValueError("Must provide at least one signal name")

        result = self.signals[signal_names[0]]
        for name in signal_names[1:]:
            result = result & self.signals[name]
        return result

    def combine_or(self, *signal_names) -> Union[pd.DataFrame, pd.Series]:
        """Combine multiple signals with OR logic."""
        if not signal_names:
            raise ValueError("Must provide at least one signal name")

        result = self.signals[signal_names[0]]
        for name in signal_names[1:]:
            result = result | self.signals[name]
        return result

    def negate(self, signal_name: str) -> Union[pd.DataFrame, pd.Series]:
        """Negate a signal."""
        return ~self.signals[signal_name]


# Common signal patterns
def price_above_ma(price: Union[IndicatorDataFrame, IndicatorSeries],
                   window: int) -> Union[IndicatorDataFrame, IndicatorSeries]:
    """Price above moving average signal."""
    ma = price.average(window)
    return price > ma


def price_below_ma(price: Union[IndicatorDataFrame, IndicatorSeries],
                   window: int) -> Union[IndicatorDataFrame, IndicatorSeries]:
    """Price below moving average signal."""
    ma = price.average(window)
    return price < ma


def ma_crossover_up(price: Union[IndicatorDataFrame, IndicatorSeries],
                    fast_window: int, slow_window: int) -> Union[IndicatorDataFrame, IndicatorSeries]:
    """Moving average crossover upward signal."""
    ma_fast = price.average(fast_window)
    ma_slow = price.average(slow_window)

    # Current fast > slow AND previous fast <= slow
    current_cross = ma_fast > ma_slow
    previous_cross = ma_fast.shift(1) <= ma_slow.shift(1)

    return current_cross & previous_cross


def ma_crossover_down(price: Union[IndicatorDataFrame, IndicatorSeries],
                      fast_window: int, slow_window: int) -> Union[IndicatorDataFrame, IndicatorSeries]:
    """Moving average crossover downward signal."""
    ma_fast = price.average(fast_window)
    ma_slow = price.average(slow_window)

    # Current fast < slow AND previous fast >= slow
    current_cross = ma_fast < ma_slow
    previous_cross = ma_fast.shift(1) >= ma_slow.shift(1)

    return current_cross & previous_cross


def volume_spike(volume: Union[IndicatorDataFrame, IndicatorSeries],
                 multiplier: float = 1.5,
                 window: Optional[int] = None) -> Union[IndicatorDataFrame, IndicatorSeries]:
    """Volume spike signal."""
    if window is None:
        # Compare to previous day
        return volume > (volume.shift(1) * multiplier)
    else:
        # Compare to rolling average
        avg_volume = volume.average(window)
        return volume > (avg_volume * multiplier)


def volume_above_threshold(volume: Union[IndicatorDataFrame, IndicatorSeries],
                          threshold: float) -> Union[IndicatorDataFrame, IndicatorSeries]:
    """Volume above absolute threshold."""
    return volume > threshold


def price_momentum(price: Union[IndicatorDataFrame, IndicatorSeries],
                   window: int) -> Union[IndicatorDataFrame, IndicatorSeries]:
    """Price momentum signal (current price vs N days ago)."""
    return price > price.shift(window)


def consecutive_up_days(price: Union[IndicatorDataFrame, IndicatorSeries],
                       count: int) -> Union[IndicatorDataFrame, IndicatorSeries]:
    """N consecutive up days signal."""
    daily_change = price > price.shift(1)
    return daily_change.rolling(window=count).sum() >= count


def consecutive_down_days(price: Union[IndicatorDataFrame, IndicatorSeries],
                         count: int) -> Union[IndicatorDataFrame, IndicatorSeries]:
    """N consecutive down days signal."""
    daily_change = price < price.shift(1)
    return daily_change.rolling(window=count).sum() >= count


def bollinger_breakout_up(price: Union[IndicatorDataFrame, IndicatorSeries],
                         window: int = 20, std_dev: float = 2) -> Union[IndicatorDataFrame, IndicatorSeries]:
    """Price breaks above upper Bollinger band."""
    from .indicators import bollinger_bands
    bb = bollinger_bands(price, window, std_dev)
    return price > bb['upper']


def bollinger_breakout_down(price: Union[IndicatorDataFrame, IndicatorSeries],
                           window: int = 20, std_dev: float = 2) -> Union[IndicatorDataFrame, IndicatorSeries]:
    """Price breaks below lower Bollinger band."""
    from .indicators import bollinger_bands
    bb = bollinger_bands(price, window, std_dev)
    return price < bb['lower']


def rsi_overbought(price: Union[IndicatorDataFrame, IndicatorSeries],
                   window: int = 14, threshold: float = 70) -> Union[IndicatorDataFrame, IndicatorSeries]:
    """RSI overbought signal."""
    from .indicators import rsi
    rsi_val = rsi(price, window)
    return rsi_val > threshold


def rsi_oversold(price: Union[IndicatorDataFrame, IndicatorSeries],
                 window: int = 14, threshold: float = 30) -> Union[IndicatorDataFrame, IndicatorSeries]:
    """RSI oversold signal."""
    from .indicators import rsi
    rsi_val = rsi(price, window)
    return rsi_val < threshold


# Advanced signal combinations
def golden_cross(price: Union[IndicatorDataFrame, IndicatorSeries]) -> Union[IndicatorDataFrame, IndicatorSeries]:
    """Classic golden cross: 50-day MA crosses above 200-day MA."""
    return ma_crossover_up(price, 50, 200)


def death_cross(price: Union[IndicatorDataFrame, IndicatorSeries]) -> Union[IndicatorDataFrame, IndicatorSeries]:
    """Classic death cross: 50-day MA crosses below 200-day MA."""
    return ma_crossover_down(price, 50, 200)


def breakout_with_volume(price: Union[IndicatorDataFrame, IndicatorSeries],
                        volume: Union[IndicatorDataFrame, IndicatorSeries],
                        price_window: int = 20,
                        volume_multiplier: float = 1.5) -> Union[IndicatorDataFrame, IndicatorSeries]:
    """Price breakout confirmed by volume spike."""
    price_high = price.max(price_window)
    price_breakout = price > price_high.shift(1)
    vol_spike = volume_spike(volume, volume_multiplier)

    return price_breakout & vol_spike


def trend_following_entry(price: Union[IndicatorDataFrame, IndicatorSeries],
                         volume: Union[IndicatorDataFrame, IndicatorSeries],
                         ma_short: int = 5, ma_medium: int = 10, ma_long: int = 20,
                         volume_multiplier: float = 1.2,
                         volume_min: float = 1000000) -> Union[IndicatorDataFrame, IndicatorSeries]:
    """Complex trend-following entry signal."""
    # Moving average trend
    ma5 = price.average(ma_short)
    ma10 = price.average(ma_medium)
    ma20 = price.average(ma_long)
    ma_trend = (ma5 > ma10) & (ma10 > ma20)

    # Volume conditions
    vol_spike = volume_spike(volume, volume_multiplier)
    vol_min = volume_above_threshold(volume, volume_min)

    return ma_trend & vol_spike & vol_min


def trend_following_exit(price: Union[IndicatorDataFrame, IndicatorSeries],
                        ma_short: int = 5, ma_medium: int = 10, ma_long: int = 20) -> Union[IndicatorDataFrame, IndicatorSeries]:
    """Complex trend-following exit signal."""
    ma5 = price.average(ma_short)
    ma10 = price.average(ma_medium)
    ma20 = price.average(ma_long)

    # Exit if trend breaks
    trend_break = (ma5 < ma10) | (ma10 < ma20)
    price_below_ma = price < ma10

    return trend_break | price_below_ma