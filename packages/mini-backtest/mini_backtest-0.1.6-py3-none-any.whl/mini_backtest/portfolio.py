from __future__ import annotations

import pandas as pd


def calc_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Compute simple close-to-close returns from a price DataFrame.

    Assumes `prices` indexed by date, columns are symbols.
    """
    returns = prices.sort_index().astype(float).pct_change()
    returns = returns.fillna(0.0)
    return returns


def portfolio_returns(
    prices: pd.DataFrame,
    weights: pd.DataFrame,
    *,
    exec_mode: str = "close_next_day",
) -> pd.Series:
    """Compute portfolio daily returns from prices and target weights.

    - exec_mode="close_next_day": use weights shifted by 1 day (T+1 holdings)
    - exec_mode="close_same_day": use today's weights with today's return (T+0)
    """
    rets = calc_returns(prices)
    w_aligned = (
        weights.reindex(index=rets.index, columns=rets.columns, fill_value=0.0)
        .astype(float)
    )
    if exec_mode == "close_next_day":
        w_use = w_aligned.shift(1).fillna(0.0)
    elif exec_mode == "close_same_day":
        w_use = w_aligned.fillna(0.0)
    else:
        raise ValueError(f"Unsupported exec_mode: {exec_mode}")
    return (w_use * rets).sum(axis=1)


def turnover_cost(
    weights: pd.DataFrame,
    *,
    fee_ratio: float = 0.0,
    tax_ratio: float = 0.0,
) -> pd.Series:
    """Estimate transaction costs per day from weight turnover.

    - fee_ratio applies to buys + sells
    - tax_ratio applies to sells only (e.g., TW stock transaction tax)
    """
    w = weights.astype(float)
    w_prev = w.shift(1).fillna(0.0)
    dw = w - w_prev
    buys = dw.clip(lower=0.0).sum(axis=1)
    sells = (-dw.clip(upper=0.0)).sum(axis=1)
    return fee_ratio * (buys + sells) + tax_ratio * sells


def equity_curve_from_weights(
    prices: pd.DataFrame,
    weights: pd.DataFrame,
    start_value: float = 1.0,
    *,
    exec_mode: str = "close_next_day",
    fee_ratio: float = 0.0,
    tax_ratio: float = 0.0,
) -> pd.Series:
    """Compute portfolio equity curve from prices and target weights.

    - Uses `exec_mode` to align weights (T+1 by default) and applies turnover costs.
    - Returns a Series named 'PORT'.
    """
    rets = calc_returns(prices)
    w_aligned = weights.reindex(index=rets.index, columns=rets.columns, fill_value=0.0).astype(float)
    port_rets = portfolio_returns(prices, w_aligned, exec_mode=exec_mode)
    costs = turnover_cost(w_aligned, fee_ratio=fee_ratio, tax_ratio=tax_ratio)
    equity = (1.0 + port_rets - costs).cumprod() * float(start_value)
    equity.name = "PORT"
    return equity
