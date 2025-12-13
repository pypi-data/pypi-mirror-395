"""
Data loading module - similar to finlab's data module.
Provides flexible data access with familiar API.
"""

import json
import pandas as pd
import numpy as np
from typing import List, Optional, Union, Dict, Any
from pathlib import Path

from .indicators import IndicatorDataFrame, create_indicator_data


class DataProvider:
    """Data provider similar to finlab's data interface."""

    def __init__(self, data_file: str = 'data.json'):
        """Initialize data provider with JSON data file."""
        self.data_file = data_file
        self._cache = {}
        self._load_data()

    def _load_data(self):
        """Load data from JSON file."""
        with open(self.data_file, 'r', encoding='utf-8') as f:
            payload = json.load(f)

        # Convert to DataFrames with proper types
        self._raw_data = {}
        for key, matrix in payload.items():
            # Skip metadata fields
            if key in ['period', 'warmup', 'symbols']:
                continue

            # Only process matrix data (dict with index, columns, data)
            if isinstance(matrix, dict) and 'index' in matrix and 'columns' in matrix and 'data' in matrix:
                df = self._df_from_matrix(matrix)
                if key in ['volume', '成交股數']:
                    df = df.astype(float)
                elif key in ['close', 'high', 'low', 'open', '收盤價', '最高價', '最低價', '開盤價']:
                    df = df.astype(float)
                self._raw_data[key] = df

    def _df_from_matrix(self, obj: dict) -> pd.DataFrame:
        """Convert JSON matrix format to DataFrame."""
        idx = pd.DatetimeIndex(pd.to_datetime(obj["index"]))
        cols = obj["columns"]
        data = obj["data"]
        return pd.DataFrame(data, index=idx, columns=cols)

    def get(self, field: str, symbols: Optional[List[str]] = None) -> IndicatorDataFrame:
        """
        Get data field similar to finlab's data.get() API.

        Args:
            field: Data field name (e.g., 'close', 'volume', 'price:收盤價')
            symbols: Optional list of symbols to filter

        Returns:
            IndicatorDataFrame with requested data
        """
        # Handle finlab-style field names
        field_mapping = {
            'price:收盤價': 'close',
            'price:開盤價': 'open',
            'price:最高價': 'high',
            'price:最低價': 'low',
            'price:成交股數': 'volume',
            '收盤價': 'close',
            '開盤價': 'open',
            '最高價': 'high',
            '最低價': 'low',
            '成交股數': 'volume'
        }

        actual_field = field_mapping.get(field, field)

        if actual_field not in self._raw_data:
            available_fields = list(self._raw_data.keys())
            raise KeyError(f"Field '{field}' not found. Available fields: {available_fields}")

        df = self._raw_data[actual_field].copy()

        # Filter symbols if requested
        if symbols:
            missing_symbols = [s for s in symbols if s not in df.columns]
            if missing_symbols:
                print(f"Warning: Symbols not found: {missing_symbols}")
            available_symbols = [s for s in symbols if s in df.columns]
            if available_symbols:
                df = df[available_symbols]
            else:
                raise ValueError("No valid symbols found")

        return create_indicator_data(df)

    def set_universe(self, symbols: Optional[List[str]] = None, market: Optional[str] = None):
        """Set trading universe (for compatibility with finlab API)."""
        if market:
            print(f"Market filter '{market}' noted but not implemented in mini-backtest")
        if symbols:
            self._universe = symbols
        else:
            # Get all available symbols
            if 'close' in self._raw_data:
                self._universe = list(self._raw_data['close'].columns)
            else:
                self._universe = []

    @property
    def universe(self) -> List[str]:
        """Get current universe."""
        return getattr(self, '_universe', list(self._raw_data.get('close', pd.DataFrame()).columns))

    def list_fields(self) -> List[str]:
        """List available data fields."""
        return list(self._raw_data.keys())

    def date_range(self) -> tuple:
        """Get available date range."""
        if 'close' in self._raw_data:
            dates = self._raw_data['close'].index
            return (dates.min(), dates.max())
        return (None, None)

    def info(self):
        """Print data information."""
        print("=== Data Information ===")
        print(f"Data file: {self.data_file}")
        print(f"Available fields: {self.list_fields()}")
        print(f"Date range: {self.date_range()}")
        print(f"Universe: {len(self.universe)} symbols")
        if self.universe:
            print(f"Sample symbols: {self.universe[:5]}{'...' if len(self.universe) > 5 else ''}")


# Global data instance for easy access
_default_data_provider = None


def get_data_provider(data_file: str = 'data.json') -> DataProvider:
    """Get or create default data provider."""
    global _default_data_provider
    if _default_data_provider is None:
        _default_data_provider = DataProvider(data_file)
    return _default_data_provider


def get(field: str, symbols: Optional[List[str]] = None) -> IndicatorDataFrame:
    """Global get function similar to finlab's data.get()."""
    return get_data_provider().get(field, symbols)


def set_universe(symbols: Optional[List[str]] = None, market: Optional[str] = None):
    """Global set_universe function."""
    get_data_provider().set_universe(symbols, market)