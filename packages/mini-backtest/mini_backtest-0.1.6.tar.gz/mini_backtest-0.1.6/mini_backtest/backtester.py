from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pandas as pd

from .metrics import compute_metrics


@dataclass
class Backtester:
    """Minimal backtester that produces metrics from price DataFrames.

    Usage:
        bt = Backtester(prices)
        results = bt.run()

    Inputs and outputs are pandas DataFrames to keep the API simple and composable.
    """

    prices: pd.DataFrame
    periods_per_year: int = 252

    def run(self) -> pd.DataFrame:
        """Compute metrics (CAGR, Max Drawdown) per column/symbol.

        Returns a DataFrame with index as symbol, columns [cagr, max_drawdown].
        """
        return compute_metrics(self.prices, periods_per_year=self.periods_per_year)

