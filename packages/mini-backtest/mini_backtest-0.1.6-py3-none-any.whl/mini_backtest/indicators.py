"""
Technical indicators module - similar to finlab's data module.
Provides flexible indicator calculations with pandas-like API.
"""

import pandas as pd
import numpy as np
from typing import Union, Optional


class IndicatorSeries(pd.Series):
    """Enhanced Series with indicator methods."""

    @property
    def _constructor(self):
        return IndicatorSeries

    @property
    def _constructor_expanddim(self):
        return IndicatorDataFrame

    def average(self, window: int) -> 'IndicatorSeries':
        """Simple moving average - finlab-style API."""
        return IndicatorSeries(self.rolling(window=window).mean(), index=self.index, name=self.name)

    def ema(self, window: int) -> 'IndicatorSeries':
        """Exponential moving average."""
        return IndicatorSeries(self.ewm(span=window).mean(), index=self.index, name=self.name)

    def std(self, window: int) -> 'IndicatorSeries':
        """Rolling standard deviation."""
        return IndicatorSeries(self.rolling(window=window).std(), index=self.index, name=self.name)

    def max(self, window: int) -> 'IndicatorSeries':
        """Rolling maximum."""
        return IndicatorSeries(self.rolling(window=window).max(), index=self.index, name=self.name)

    def min(self, window: int) -> 'IndicatorSeries':
        """Rolling minimum."""
        return IndicatorSeries(self.rolling(window=window).min(), index=self.index, name=self.name)

    def rank(self, ascending: bool = True) -> 'IndicatorSeries':
        """Cross-sectional rank (for single series, just return normalized)."""
        return IndicatorSeries(self.rank(ascending=ascending), index=self.index, name=self.name)


class IndicatorDataFrame(pd.DataFrame):
    """Enhanced DataFrame with indicator methods - similar to finlab data."""

    @property
    def _constructor(self):
        return IndicatorDataFrame

    @property
    def _constructor_sliced(self):
        return IndicatorSeries

    def average(self, window: int) -> 'IndicatorDataFrame':
        """Simple moving average for each column."""
        return IndicatorDataFrame(self.rolling(window=window).mean(),
                                 index=self.index, columns=self.columns)

    def ema(self, window: int) -> 'IndicatorDataFrame':
        """Exponential moving average for each column."""
        return IndicatorDataFrame(self.ewm(span=window).mean(),
                                 index=self.index, columns=self.columns)

    def std(self, window: int) -> 'IndicatorDataFrame':
        """Rolling standard deviation for each column."""
        return IndicatorDataFrame(self.rolling(window=window).std(),
                                 index=self.index, columns=self.columns)

    def max(self, window: int) -> 'IndicatorDataFrame':
        """Rolling maximum for each column."""
        return IndicatorDataFrame(self.rolling(window=window).max(),
                                 index=self.index, columns=self.columns)

    def min(self, window: int) -> 'IndicatorDataFrame':
        """Rolling minimum for each column."""
        return IndicatorDataFrame(self.rolling(window=window).min(),
                                 index=self.index, columns=self.columns)

    def rank(self, axis: int = 1, ascending: bool = True) -> 'IndicatorDataFrame':
        """Cross-sectional ranking."""
        return IndicatorDataFrame(self.rank(axis=axis, ascending=ascending),
                                 index=self.index, columns=self.columns)

    def quantile(self, q: float, axis: int = 1) -> 'IndicatorSeries':
        """Cross-sectional quantile."""
        result = self.quantile(q, axis=axis)
        return IndicatorSeries(result, index=self.index, name=f'quantile_{q}')

    def top(self, n: int, axis: int = 1) -> 'IndicatorDataFrame':
        """Select top N values cross-sectionally."""
        def select_top_n(row):
            return row.nlargest(n)

        if axis == 1:
            result = self.apply(lambda row: row.where(row.isin(row.nlargest(n))), axis=1)
        else:
            result = self.apply(lambda col: col.where(col.isin(col.nlargest(n))), axis=0)

        return IndicatorDataFrame(result, index=self.index, columns=self.columns)

    def bottom(self, n: int, axis: int = 1) -> 'IndicatorDataFrame':
        """Select bottom N values cross-sectionally."""
        if axis == 1:
            result = self.apply(lambda row: row.where(row.isin(row.nsmallest(n))), axis=1)
        else:
            result = self.apply(lambda col: col.where(col.isin(col.nsmallest(n))), axis=0)

        return IndicatorDataFrame(result, index=self.index, columns=self.columns)


def create_indicator_data(df: pd.DataFrame) -> IndicatorDataFrame:
    """Convert regular DataFrame to IndicatorDataFrame."""
    return IndicatorDataFrame(df, index=df.index, columns=df.columns)


def bollinger_bands(price: Union[IndicatorDataFrame, IndicatorSeries],
                   window: int = 20, std_dev: float = 2) -> dict:
    """Calculate Bollinger Bands."""
    ma = price.average(window)
    std = price.std(window)

    return {
        'middle': ma,
        'upper': ma + (std * std_dev),
        'lower': ma - (std * std_dev),
        'width': (ma + (std * std_dev)) - (ma - (std * std_dev)),
        'percent_b': (price - (ma - (std * std_dev))) / ((ma + (std * std_dev)) - (ma - (std * std_dev)))
    }


def rsi(price: Union[IndicatorDataFrame, IndicatorSeries], window: int = 14) -> Union[IndicatorDataFrame, IndicatorSeries]:
    """Relative Strength Index."""
    delta = price.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi_result = 100 - (100 / (1 + rs))

    if isinstance(price, IndicatorSeries):
        return IndicatorSeries(rsi_result, index=price.index, name=f'rsi_{window}')
    else:
        return IndicatorDataFrame(rsi_result, index=price.index, columns=price.columns)


def macd(price: Union[IndicatorDataFrame, IndicatorSeries],
         fast: int = 12, slow: int = 26, signal: int = 9) -> dict:
    """MACD indicator."""
    ema_fast = price.ema(fast)
    ema_slow = price.ema(slow)
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ema(signal)
    histogram = macd_line - signal_line

    return {
        'macd': macd_line,
        'signal': signal_line,
        'histogram': histogram
    }


def stochastic(high: Union[IndicatorDataFrame, IndicatorSeries],
               low: Union[IndicatorDataFrame, IndicatorSeries],
               close: Union[IndicatorDataFrame, IndicatorSeries],
               k_window: int = 14, d_window: int = 3) -> dict:
    """Stochastic oscillator."""
    lowest_low = low.rolling(window=k_window).min()
    highest_high = high.rolling(window=k_window).max()

    k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
    d_percent = k_percent.rolling(window=d_window).mean()

    return {
        'k': k_percent,
        'd': d_percent
    }