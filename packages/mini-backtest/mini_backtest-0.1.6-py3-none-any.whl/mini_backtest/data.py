from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

import numpy as np
import pandas as pd


DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "data.json"


@dataclass
class SymbolSpec:
    symbol: str
    drift: float = 0.0002  # daily drift
    vol: float = 0.01  # daily volatility


def _simulate_ohlcv(
    dates: Iterable[pd.Timestamp],
    start_price: float,
    drift: float,
    vol: float,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Simulate a simple geometric random walk OHLCV series.

    - prices follow: P_t = P_{t-1} * exp((mu - 0.5*sigma^2) + sigma*Z)
    - OHLC generated from close with small ranges
    - volume simulated with mild noise around a base
    """
    dates = list(pd.to_datetime(list(dates)))
    n = len(dates)
    if n == 0:
        return pd.DataFrame(columns=["date", "open", "high", "low", "close", "volume"])  # pragma: no cover

    log_ret = rng.normal(loc=drift - 0.5 * vol * vol, scale=vol, size=n)
    close = start_price * np.exp(np.cumsum(log_ret))

    # Derive OHLC from close with small intraday ranges
    spread = np.maximum(close * 0.002, 0.01)  # 0.2% spread
    open_ = close * (1 + rng.normal(0, 0.0005, size=n))
    high = np.maximum.reduce([open_, close]) + rng.uniform(0, spread)
    low = np.minimum.reduce([open_, close]) - rng.uniform(0, spread)

    base_vol = 1_000_000
    volume = (base_vol * (1 + rng.normal(0, 0.1, size=n)) * (close / close[0]) ** -0.3).astype(int)

    df = pd.DataFrame(
        {
            "date": dates,
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
        }
    )
    # Ensure monotonic increasing time index
    df = df.sort_values("date").reset_index(drop=True)
    return df


def _default_symbol_specs(n: int = 10) -> List[SymbolSpec]:
    return [
        SymbolSpec(symbol=f"STK{i+1:02d}", drift=0.00015 + 0.00002 * i, vol=0.012 - 0.0005 * i)
        for i in range(n)
    ]


def generate_sample_data(
    file_path: Path | str = DATA_FILE,
    symbols: List[SymbolSpec] | None = None,
    start: str = "2020-01-01",
    end: str = "2022-12-31",
    seed: int = 42,
) -> Path:
    """Generate a reproducible JSON dataset with OHLCV for 10 symbols.

    The JSON is an array of objects: {date, symbol, open, high, low, close, volume}.
    """
    file_path = Path(file_path)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if symbols is None:
        symbols = _default_symbol_specs(10)

    rng = np.random.default_rng(seed)
    dates = pd.bdate_range(start=start, end=end, freq="C")  # business days

    records = []
    for spec in symbols:
        start_price = float(50 + 10 * rng.uniform())
        ohlcv = _simulate_ohlcv(dates, start_price, spec.drift, spec.vol, rng)
        ohlcv.insert(1, "symbol", spec.symbol)
        records.extend(ohlcv.to_dict(orient="records"))

    with file_path.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2, default=str)

    return file_path


def load_data(file_path: Path | str = DATA_FILE) -> pd.DataFrame:
    """Load the JSON dataset into a tidy pandas DataFrame.

    Returns columns: date, symbol, open, high, low, close, volume.
    """
    file_path = Path(file_path)
    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    # Normalize dtypes
    df["date"] = pd.to_datetime(df["date"], utc=False)
    numeric_cols = ["open", "high", "low", "close", "volume"]
    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c])
    # Sort for consistency
    df = df.sort_values(["symbol", "date"]).reset_index(drop=True)
    return df


def load_sample_dataset(
    *,
    n_symbols: int = 10,
    start: str = "2020-01-01",
    end: str = "2022-12-31",
    seed: int = 42,
) -> pd.DataFrame:
    """Return a reproducible tidy OHLCV DataFrame without writing to disk.

    Columns: date, symbol, open, high, low, close, volume.
    """
    symbols = _default_symbol_specs(n_symbols)
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range(start=start, end=end, freq="C")

    frames = []
    for spec in symbols:
        start_price = float(50 + 10 * rng.uniform())
        ohlcv = _simulate_ohlcv(dates, start_price, spec.drift, spec.vol, rng)
        ohlcv.insert(1, "symbol", spec.symbol)
        frames.append(ohlcv)

    df = pd.concat(frames, ignore_index=True)
    # Normalize dtypes and sort for consistency
    df["date"] = pd.to_datetime(df["date"], utc=False)
    numeric_cols = ["open", "high", "low", "close", "volume"]
    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c])
    df = df.sort_values(["symbol", "date"]).reset_index(drop=True)
    return df


def load_sample_prices(
    *,
    n_symbols: int = 10,
    start: str = "2020-01-01",
    end: str = "2022-12-31",
    seed: int = 42,
) -> pd.DataFrame:
    """Return a reproducible wide close-price DataFrame without writing to disk.

    Index: date, Columns: symbols, Values: close.
    """
    df = load_sample_dataset(n_symbols=n_symbols, start=start, end=end, seed=seed)
    return pivot_close(df)


def pivot_close(df: pd.DataFrame) -> pd.DataFrame:
    """Pivot a tidy OHLCV DataFrame to a wide close-price DataFrame.

    - Index: date (sorted)
    - Columns: symbols
    - Values: close
    """
    wide = df.pivot(index="date", columns="symbol", values="close").sort_index()
    # Ensure float dtype for numeric operations downstream
    wide = wide.astype(float)
    return wide
