from __future__ import annotations

from typing import Tuple

import numpy as np
import pandas as pd
from scipy import stats


def _ensure_dataframe(x: pd.Series | pd.DataFrame) -> pd.DataFrame:
    if isinstance(x, pd.Series):
        return x.to_frame()
    return x


def compute_cagr(
    prices: pd.Series | pd.DataFrame,
    periods_per_year: int = 252,
) -> pd.Series:
    """Compute CAGR for each column of a price/equity DataFrame.

    Returns a Series indexed by column name with CAGR as a float in [−1, inf).
    """
    df = _ensure_dataframe(prices).dropna(how="all")
    if df.shape[0] < 2:
        return pd.Series({c: np.nan for c in df.columns})

    def _cagr(col: pd.Series) -> float:
        col = col.dropna()
        if len(col) < 2:
            return np.nan
        start, end = float(col.iloc[0]), float(col.iloc[-1])
        years = (len(col) - 1) / periods_per_year
        if years <= 0 or start <= 0:
            return np.nan
        return (end / start) ** (1.0 / years) - 1.0

    return df.apply(_cagr, axis=0)


def compute_max_drawdown(prices: pd.Series | pd.DataFrame) -> pd.Series:
    """Compute max drawdown magnitude for each column of a price/equity DataFrame.

    Returns positive magnitudes (e.g., 0.35 means -35% at worst).
    """
    df = _ensure_dataframe(prices).dropna(how="all")
    if df.shape[0] < 1:
        return pd.Series({c: np.nan for c in df.columns})

    def _mdd(col: pd.Series) -> float:
        col = col.dropna().astype(float)
        if len(col) == 0:
            return np.nan
        running_max = col.cummax()
        drawdown = col / running_max - 1.0
        return float((-drawdown.min()))  # positive magnitude

    return df.apply(_mdd, axis=0)


def compute_volatility(
    prices: pd.Series | pd.DataFrame,
    periods_per_year: int = 252
) -> pd.Series:
    """Compute annualized volatility for each column."""
    df = _ensure_dataframe(prices).dropna(how="all")
    if df.shape[0] < 2:
        return pd.Series({c: np.nan for c in df.columns})

    def _volatility(col: pd.Series) -> float:
        col = col.dropna()
        if len(col) < 2:
            return np.nan
        returns = col.pct_change().dropna()
        if len(returns) < 2:
            return np.nan
        return float(returns.std() * np.sqrt(periods_per_year))

    return df.apply(_volatility, axis=0)


def compute_sharpe_ratio(
    prices: pd.Series | pd.DataFrame,
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252
) -> pd.Series:
    """Compute Sharpe ratio for each column."""
    df = _ensure_dataframe(prices).dropna(how="all")
    if df.shape[0] < 2:
        return pd.Series({c: np.nan for c in df.columns})

    def _sharpe(col: pd.Series) -> float:
        col = col.dropna()
        if len(col) < 2:
            return np.nan
        returns = col.pct_change().dropna()
        if len(returns) < 2:
            return np.nan

        excess_return = returns.mean() * periods_per_year - risk_free_rate
        volatility = returns.std() * np.sqrt(periods_per_year)

        if volatility == 0:
            return np.nan
        return float(excess_return / volatility)

    return df.apply(_sharpe, axis=0)


def compute_sortino_ratio(
    prices: pd.Series | pd.DataFrame,
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252
) -> pd.Series:
    """Compute Sortino ratio for each column."""
    df = _ensure_dataframe(prices).dropna(how="all")
    if df.shape[0] < 2:
        return pd.Series({c: np.nan for c in df.columns})

    def _sortino(col: pd.Series) -> float:
        col = col.dropna()
        if len(col) < 2:
            return np.nan
        returns = col.pct_change().dropna()
        if len(returns) < 2:
            return np.nan

        excess_return = returns.mean() * periods_per_year - risk_free_rate
        downside_returns = returns[returns < 0]
        if len(downside_returns) == 0:
            return np.inf if excess_return > 0 else np.nan

        downside_deviation = downside_returns.std() * np.sqrt(periods_per_year)
        if downside_deviation == 0:
            return np.nan
        return float(excess_return / downside_deviation)

    return df.apply(_sortino, axis=0)


def compute_calmar_ratio(
    prices: pd.Series | pd.DataFrame,
    periods_per_year: int = 252
) -> pd.Series:
    """Compute Calmar ratio (CAGR / Max Drawdown)."""
    cagr = compute_cagr(prices, periods_per_year)
    mdd = compute_max_drawdown(prices)

    calmar = cagr / mdd
    calmar = calmar.replace([np.inf, -np.inf], np.nan)
    return calmar


def compute_average_drawdown(prices: pd.Series | pd.DataFrame) -> pd.Series:
    """Compute average drawdown magnitude."""
    df = _ensure_dataframe(prices).dropna(how="all")
    if df.shape[0] < 1:
        return pd.Series({c: np.nan for c in df.columns})

    def _avg_dd(col: pd.Series) -> float:
        col = col.dropna().astype(float)
        if len(col) == 0:
            return np.nan
        running_max = col.cummax()
        drawdown = col / running_max - 1.0
        # Only consider negative drawdowns
        negative_dd = drawdown[drawdown < 0]
        if len(negative_dd) == 0:
            return 0.0
        return float(-negative_dd.mean())  # positive magnitude

    return df.apply(_avg_dd, axis=0)


def compute_average_drawdown_days(prices: pd.Series | pd.DataFrame) -> pd.Series:
    """Compute average duration of drawdown periods in days."""
    df = _ensure_dataframe(prices).dropna(how="all")
    if df.shape[0] < 1:
        return pd.Series({c: np.nan for c in df.columns})

    def _avg_dd_days(col: pd.Series) -> float:
        col = col.dropna().astype(float)
        if len(col) == 0:
            return np.nan
        running_max = col.cummax()
        drawdown = col / running_max - 1.0

        # Find drawdown periods
        is_in_drawdown = drawdown < 0
        if not is_in_drawdown.any():
            return 0.0

        # Group consecutive drawdown periods
        groups = (is_in_drawdown != is_in_drawdown.shift()).cumsum()
        drawdown_periods = []

        for group in groups.unique():
            group_data = is_in_drawdown[groups == group]
            if group_data.iloc[0]:  # This is a drawdown period
                drawdown_periods.append(len(group_data))

        if not drawdown_periods:
            return 0.0
        return float(np.mean(drawdown_periods))

    return df.apply(_avg_dd_days, axis=0)


def compute_value_at_risk(
    prices: pd.Series | pd.DataFrame,
    confidence_level: float = 0.05
) -> pd.Series:
    """Compute Value at Risk (VaR) for daily returns."""
    df = _ensure_dataframe(prices).dropna(how="all")
    if df.shape[0] < 2:
        return pd.Series({c: np.nan for c in df.columns})

    def _var(col: pd.Series) -> float:
        col = col.dropna()
        if len(col) < 2:
            return np.nan
        returns = col.pct_change().dropna()
        if len(returns) < 2:
            return np.nan
        return float(np.percentile(returns, confidence_level * 100))

    return df.apply(_var, axis=0)


def compute_conditional_value_at_risk(
    prices: pd.Series | pd.DataFrame,
    confidence_level: float = 0.05
) -> pd.Series:
    """Compute Conditional Value at Risk (CVaR) for daily returns."""
    df = _ensure_dataframe(prices).dropna(how="all")
    if df.shape[0] < 2:
        return pd.Series({c: np.nan for c in df.columns})

    def _cvar(col: pd.Series) -> float:
        col = col.dropna()
        if len(col) < 2:
            return np.nan
        returns = col.pct_change().dropna()
        if len(returns) < 2:
            return np.nan
        var = np.percentile(returns, confidence_level * 100)
        tail_returns = returns[returns <= var]
        if len(tail_returns) == 0:
            return var
        return float(tail_returns.mean())

    return df.apply(_cvar, axis=0)


def compute_alpha_beta(
    prices: pd.Series | pd.DataFrame,
    benchmark: pd.Series,
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252
) -> Tuple[pd.Series, pd.Series]:
    """Compute alpha and beta versus benchmark."""
    df = _ensure_dataframe(prices).dropna(how="all")
    if df.shape[0] < 2 or len(benchmark) < 2:
        return (
            pd.Series({c: np.nan for c in df.columns}),
            pd.Series({c: np.nan for c in df.columns})
        )

    # Align benchmark with price data
    benchmark = benchmark.reindex(df.index).dropna()
    benchmark_returns = benchmark.pct_change().dropna()

    def _alpha_beta(col: pd.Series) -> Tuple[float, float]:
        col = col.dropna()
        if len(col) < 2:
            return np.nan, np.nan
        returns = col.pct_change().dropna()
        if len(returns) < 2:
            return np.nan, np.nan

        # Align returns with benchmark returns
        aligned_returns = returns.reindex(benchmark_returns.index).dropna()
        aligned_benchmark = benchmark_returns.reindex(aligned_returns.index).dropna()

        if len(aligned_returns) < 2 or len(aligned_benchmark) < 2:
            return np.nan, np.nan

        # Calculate beta using linear regression
        slope, intercept, _, _, _ = stats.linregress(aligned_benchmark, aligned_returns)
        beta = slope

        # Calculate alpha
        portfolio_return = aligned_returns.mean() * periods_per_year
        benchmark_return = aligned_benchmark.mean() * periods_per_year
        alpha = portfolio_return - risk_free_rate - beta * (benchmark_return - risk_free_rate)

        return float(alpha), float(beta)

    results = df.apply(lambda col: _alpha_beta(col), axis=0)
    alphas = pd.Series({col: result[0] for col, result in results.items()})
    betas = pd.Series({col: result[1] for col, result in results.items()})

    return alphas, betas


def compute_tail_ratio(
    prices: pd.Series | pd.DataFrame,
    periods: int = 252
) -> pd.Series:
    """Compute tail ratio (95th percentile return / 5th percentile return)."""
    df = _ensure_dataframe(prices).dropna(how="all")
    if df.shape[0] < 2:
        return pd.Series({c: np.nan for c in df.columns})

    def _tail_ratio(col: pd.Series) -> float:
        col = col.dropna()
        if len(col) < 2:
            return np.nan
        returns = col.pct_change().dropna()
        if len(returns) < 2:
            return np.nan

        p95 = np.percentile(returns, 95)
        p5 = np.percentile(returns, 5)

        if p5 == 0:
            return np.nan
        return float(abs(p95 / p5))

    return df.apply(_tail_ratio, axis=0)


def compute_win_rate(
    prices: pd.Series | pd.DataFrame
) -> pd.Series:
    """Compute win rate (percentage of positive returns)."""
    df = _ensure_dataframe(prices).dropna(how="all")
    if df.shape[0] < 2:
        return pd.Series({c: np.nan for c in df.columns})

    def _win_rate(col: pd.Series) -> float:
        col = col.dropna()
        if len(col) < 2:
            return np.nan
        returns = col.pct_change().dropna()
        if len(returns) == 0:
            return np.nan
        return float((returns > 0).mean())

    return df.apply(_win_rate, axis=0)


def compute_expectancy(
    prices: pd.Series | pd.DataFrame
) -> pd.Series:
    """Compute expectancy (average return per period)."""
    df = _ensure_dataframe(prices).dropna(how="all")
    if df.shape[0] < 2:
        return pd.Series({c: np.nan for c in df.columns})

    def _expectancy(col: pd.Series) -> float:
        col = col.dropna()
        if len(col) < 2:
            return np.nan
        returns = col.pct_change().dropna()
        if len(returns) == 0:
            return np.nan
        return float(returns.mean())

    return df.apply(_expectancy, axis=0)


def compute_mae_mfe(
    prices: pd.Series | pd.DataFrame
) -> Tuple[pd.Series, pd.Series]:
    """Compute Maximum Adverse Excursion (MAE) and Maximum Favorable Excursion (MFE)."""
    df = _ensure_dataframe(prices).dropna(how="all")
    if df.shape[0] < 1:
        return (
            pd.Series({c: np.nan for c in df.columns}),
            pd.Series({c: np.nan for c in df.columns})
        )

    def _mae_mfe(col: pd.Series) -> Tuple[float, float]:
        col = col.dropna().astype(float)
        if len(col) == 0:
            return np.nan, np.nan

        # Calculate running returns from start
        start_price = col.iloc[0]
        returns = col / start_price - 1.0

        mae = float(returns.min())  # Most negative return
        mfe = float(returns.max())  # Most positive return

        return mae, mfe

    results = df.apply(lambda col: _mae_mfe(col), axis=0)
    mae = pd.Series({col: result[0] for col, result in results.items()})
    mfe = pd.Series({col: result[1] for col, result in results.items()})

    return mae, mfe


def compute_trade_based_metrics_from_log(trade_log: list, fee_ratio: float = 0.001425, tax_ratio: float = 0.003) -> dict:
    """Compute trade-based metrics from trade log (ENTRY/EXIT pairs)."""
    if not trade_log:
        return {
            'winRate': np.nan,
            'expectancy': np.nan,
            'mae': np.nan,
            'mfe': np.nan
        }

    # Group trades by symbol and calculate returns for complete ENTRY->EXIT pairs
    trades_by_symbol = {}
    for trade in trade_log:
        symbol = trade['symbol']
        if symbol not in trades_by_symbol:
            trades_by_symbol[symbol] = []
        trades_by_symbol[symbol].append(trade)

    completed_trades = []
    total_cost = fee_ratio + tax_ratio

    for symbol, trades in trades_by_symbol.items():
        i = 0
        while i < len(trades) - 1:
            if trades[i]['action'] == 'ENTRY' and i + 1 < len(trades) and trades[i + 1]['action'] == 'EXIT':
                entry_price = trades[i]['price']
                exit_price = trades[i + 1]['price']
                # Calculate return after transaction costs
                raw_return = (exit_price / entry_price) - 1.0
                net_return = raw_return - total_cost
                completed_trades.append(net_return)
                i += 2  # Skip both trades
            else:
                i += 1

    if not completed_trades:
        return {
            'winRate': np.nan,
            'expectancy': np.nan,
            'mae': np.nan,
            'mfe': np.nan
        }

    # Calculate metrics
    winning_trades = [r for r in completed_trades if r > 0]
    win_rate = len(winning_trades) / len(completed_trades)
    expectancy = sum(completed_trades) / len(completed_trades)
    mae = min(completed_trades) if completed_trades else 0
    mfe = max(completed_trades) if completed_trades else 0

    return {
        'winRate': float(win_rate),
        'expectancy': float(expectancy),
        'mae': float(mae),
        'mfe': float(mfe)
    }


def compute_trade_based_metrics(
    prices: pd.Series | pd.DataFrame,
    is_buy_and_hold: bool = True
) -> dict:
    """Compute trade-based metrics for buy-and-hold strategy."""
    df = _ensure_dataframe(prices).dropna(how="all")
    if df.shape[0] < 2:
        return {
            'winRate': np.nan,
            'expectancy': np.nan,
            'mae': np.nan,
            'mfe': np.nan
        }

    col = df.iloc[:, 0]  # Take first column
    col = col.dropna().astype(float)
    if len(col) < 2:
        return {
            'winRate': np.nan,
            'expectancy': np.nan,
            'mae': np.nan,
            'mfe': np.nan
        }

    if is_buy_and_hold:
        # For buy-and-hold, treat as single trade
        start_price = col.iloc[0]
        end_price = col.iloc[-1]
        total_return = (end_price / start_price) - 1.0

        # Calculate MAE/MFE as running min/max from start
        running_returns = col / start_price - 1.0
        mae = float(running_returns.min())
        mfe = float(running_returns.max())

        return {
            'winRate': 1.0 if total_return > 0 else 0.0,  # Single trade win/loss
            'expectancy': float(total_return),  # Total return for single trade
            'mae': mae,
            'mfe': mfe
        }
    else:
        # For regular trading, use daily returns
        returns = col.pct_change().dropna()
        if len(returns) == 0:
            return {
                'winRate': np.nan,
                'expectancy': np.nan,
                'mae': np.nan,
                'mfe': np.nan
            }

        win_rate = float((returns > 0).mean())
        expectancy = float(returns.mean())

        # MAE/MFE from cumulative perspective
        running_returns = col / col.iloc[0] - 1.0
        mae = float(running_returns.min())
        mfe = float(running_returns.max())

        return {
            'winRate': win_rate,
            'expectancy': expectancy,
            'mae': mae,
            'mfe': mfe
        }


def compute_comprehensive_metrics(
    prices: pd.DataFrame,
    benchmark: pd.Series = None,
    periods_per_year: int = 252,
    risk_free_rate: float = 0.0,
    trade_log: list = None
) -> dict:
    """Compute comprehensive metrics matching finlab output structure."""

    # Basic metrics
    cagr = compute_cagr(prices, periods_per_year)
    mdd = compute_max_drawdown(prices)
    volatility = compute_volatility(prices, periods_per_year)

    # Ratios
    sharpe = compute_sharpe_ratio(prices, risk_free_rate, periods_per_year)
    sortino = compute_sortino_ratio(prices, risk_free_rate, periods_per_year)
    calmar = compute_calmar_ratio(prices, periods_per_year)
    tail_ratio = compute_tail_ratio(prices)
    omega = compute_omega_ratio(prices, risk_free_rate, periods_per_year)
    recovery = compute_recovery_factor(prices, periods_per_year)

    # Risk metrics
    avg_dd = compute_average_drawdown(prices)
    avg_dd_days = compute_average_drawdown_days(prices)
    var = compute_value_at_risk(prices)
    cvar = compute_conditional_value_at_risk(prices)
    ulcer = compute_ulcer_index(prices, periods_per_year)

    # Distribution metrics
    skewness = compute_skewness(prices)
    kurtosis = compute_kurtosis(prices)

    # Performance metrics - use trade log if available, otherwise price-based
    if trade_log:
        trade_metrics = compute_trade_based_metrics_from_log(trade_log)
    else:
        trade_metrics = compute_trade_based_metrics(prices, is_buy_and_hold=True)
    win_rate_val = trade_metrics['winRate']
    expectancy_val = trade_metrics['expectancy']
    mae_val = trade_metrics['mae']
    mfe_val = trade_metrics['mfe']

    # Alpha/Beta if benchmark provided
    alpha, beta = None, None
    if benchmark is not None:
        alpha, beta = compute_alpha_beta(prices, benchmark, risk_free_rate, periods_per_year)

    # Count metrics (for portfolio)
    weights_df = (prices > 0).astype(float)  # Assume binary holdings for simplicity
    n_stocks = weights_df.sum(axis=1)
    avg_n_stock = float(n_stocks.mean()) if len(n_stocks) > 0 else 0.0
    max_n_stock = int(n_stocks.max()) if len(n_stocks) > 0 else 0

    # Organize like finlab output
    metrics = {}

    # For single column (PORT)
    col = prices.columns[0] if len(prices.columns) == 1 else 'PORT'

    metrics['profitability'] = {
        'annualReturn': float(cagr.iloc[0]) if len(cagr) > 0 else np.nan,
        'alpha': float(alpha.iloc[0]) if alpha is not None and len(alpha) > 0 else 0.0,
        'beta': float(beta.iloc[0]) if beta is not None and len(beta) > 0 else 1.0,
        'avgNStock': avg_n_stock,
        'maxNStock': max_n_stock
    }

    metrics['risk'] = {
        'maxDrawdown': float(-mdd.iloc[0]) if len(mdd) > 0 else np.nan,  # Negative for consistency
        'avgDrawdown': float(-avg_dd.iloc[0]) if len(avg_dd) > 0 else np.nan,
        'avgDrawdownDays': float(avg_dd_days.iloc[0]) if len(avg_dd_days) > 0 else np.nan,
        'valueAtRisk': float(var.iloc[0]) if len(var) > 0 else np.nan,
        'cvalueAtRisk': float(cvar.iloc[0]) if len(cvar) > 0 else np.nan,
        'ulcerIndex': float(ulcer.iloc[0]) if len(ulcer) > 0 else np.nan,
        'skewness': float(skewness.iloc[0]) if len(skewness) > 0 else np.nan,
        'kurtosis': float(kurtosis.iloc[0]) if len(kurtosis) > 0 else np.nan
    }

    metrics['ratio'] = {
        'sharpeRatio': float(sharpe.iloc[0]) if len(sharpe) > 0 else np.nan,
        'sortinoRatio': float(sortino.iloc[0]) if len(sortino) > 0 else np.nan,
        'calmarRatio': float(calmar.iloc[0]) if len(calmar) > 0 else np.nan,
        'omegaRatio': float(omega.iloc[0]) if len(omega) > 0 else np.nan,
        'recoveryFactor': float(recovery.iloc[0]) if len(recovery) > 0 else np.nan,
        'volatility': float(volatility.iloc[0]) if len(volatility) > 0 else np.nan,
        'profitFactor': 0,  # Placeholder - would need trade-by-trade data
        'tailRatio': float(tail_ratio.iloc[0]) if len(tail_ratio) > 0 else np.nan
    }

    metrics['winrate'] = {
        'winRate': win_rate_val,
        'm12WinRate': None,  # Not implemented
        'expectancy': expectancy_val,
        'mae': mae_val,
        'mfe': mfe_val
    }

    metrics['liquidity'] = {
        'capacity': 0,  # Not applicable for simple framework
        'disposalStockRatio': 0.0,
        'warningStockRatio': 0.0,
        'fullDeliveryStockRatio': 0.0,
        'buyHigh': 0.0,
        'sellLow': 0.0
    }

    return metrics


def compute_omega_ratio(
    prices: pd.Series | pd.DataFrame,
    threshold: float = 0.0,
    periods_per_year: int = 252
) -> pd.Series:
    """Compute Omega ratio (probability-weighted gains over losses)."""
    df = _ensure_dataframe(prices).dropna(how="all")
    if df.shape[0] < 2:
        return pd.Series({c: np.nan for c in df.columns})

    def _omega(col: pd.Series) -> float:
        col = col.dropna()
        if len(col) < 2:
            return np.nan
        returns = col.pct_change().dropna()
        if len(returns) < 2:
            return np.nan

        # Annualize threshold
        threshold_daily = threshold / periods_per_year
        excess = returns - threshold_daily

        gains = excess[excess > 0].sum()
        losses = -excess[excess < 0].sum()

        if losses == 0:
            return np.inf if gains > 0 else np.nan
        return float(gains / losses)

    return df.apply(_omega, axis=0)


def compute_skewness(prices: pd.Series | pd.DataFrame) -> pd.Series:
    """Compute skewness of returns distribution."""
    df = _ensure_dataframe(prices).dropna(how="all")
    if df.shape[0] < 2:
        return pd.Series({c: np.nan for c in df.columns})

    def _skew(col: pd.Series) -> float:
        col = col.dropna()
        if len(col) < 2:
            return np.nan
        returns = col.pct_change().dropna()
        if len(returns) < 3:
            return np.nan
        return float(returns.skew())

    return df.apply(_skew, axis=0)


def compute_kurtosis(prices: pd.Series | pd.DataFrame) -> pd.Series:
    """Compute kurtosis of returns distribution (excess kurtosis)."""
    df = _ensure_dataframe(prices).dropna(how="all")
    if df.shape[0] < 2:
        return pd.Series({c: np.nan for c in df.columns})

    def _kurt(col: pd.Series) -> float:
        col = col.dropna()
        if len(col) < 2:
            return np.nan
        returns = col.pct_change().dropna()
        if len(returns) < 4:
            return np.nan
        return float(returns.kurtosis())  # pandas uses excess kurtosis by default

    return df.apply(_kurt, axis=0)


def compute_information_ratio(
    prices: pd.Series | pd.DataFrame,
    benchmark: pd.Series,
    periods_per_year: int = 252
) -> pd.Series:
    """Compute Information Ratio (active return / tracking error)."""
    df = _ensure_dataframe(prices).dropna(how="all")
    if df.shape[0] < 2 or len(benchmark) < 2:
        return pd.Series({c: np.nan for c in df.columns})

    # Align benchmark with price data
    benchmark = benchmark.reindex(df.index).dropna()
    benchmark_returns = benchmark.pct_change().dropna()

    def _ir(col: pd.Series) -> float:
        col = col.dropna()
        if len(col) < 2:
            return np.nan
        returns = col.pct_change().dropna()
        if len(returns) < 2:
            return np.nan

        # Align returns with benchmark
        aligned_returns = returns.reindex(benchmark_returns.index).dropna()
        aligned_benchmark = benchmark_returns.reindex(aligned_returns.index).dropna()

        if len(aligned_returns) < 2:
            return np.nan

        # Active returns
        active_returns = aligned_returns - aligned_benchmark

        # Tracking error (standard deviation of active returns)
        tracking_error = active_returns.std() * np.sqrt(periods_per_year)

        if tracking_error == 0:
            return np.nan

        # Annualized active return
        active_return = active_returns.mean() * periods_per_year

        return float(active_return / tracking_error)

    return df.apply(_ir, axis=0)


def compute_ulcer_index(
    prices: pd.Series | pd.DataFrame,
    periods_per_year: int = 252
) -> pd.Series:
    """Compute Ulcer Index (RMS of drawdowns as measure of downside risk)."""
    df = _ensure_dataframe(prices).dropna(how="all")
    if df.shape[0] < 1:
        return pd.Series({c: np.nan for c in df.columns})

    def _ulcer(col: pd.Series) -> float:
        col = col.dropna().astype(float)
        if len(col) == 0:
            return np.nan
        running_max = col.cummax()
        drawdown_pct = (col / running_max - 1.0) * 100  # in percentage
        # RMS of drawdowns
        squared_dd = drawdown_pct ** 2
        ulcer = np.sqrt(squared_dd.mean())
        return float(ulcer)

    return df.apply(_ulcer, axis=0)


def compute_recovery_factor(
    prices: pd.Series | pd.DataFrame,
    periods_per_year: int = 252
) -> pd.Series:
    """Compute Recovery Factor (total return / max drawdown)."""
    df = _ensure_dataframe(prices).dropna(how="all")
    if df.shape[0] < 2:
        return pd.Series({c: np.nan for c in df.columns})

    def _recovery(col: pd.Series) -> float:
        col = col.dropna()
        if len(col) < 2:
            return np.nan

        total_return = (col.iloc[-1] / col.iloc[0]) - 1.0

        # Calculate max drawdown
        running_max = col.cummax()
        drawdown = col / running_max - 1.0
        max_dd = -drawdown.min()  # positive magnitude

        if max_dd == 0:
            return np.inf if total_return > 0 else np.nan

        return float(total_return / max_dd)

    return df.apply(_recovery, axis=0)


def compute_metrics(
    prices: pd.DataFrame,
    periods_per_year: int = 252,
    benchmark: pd.Series = None,
    risk_free_rate: float = 0.0,
    comprehensive: bool = False
) -> pd.DataFrame | dict:
    """Compute metrics from a close-price/equity DataFrame.

    Input: wide DataFrame with index as datetime and columns as symbols.
    Output: DataFrame with index as symbols and columns [cagr, max_drawdown]
            or comprehensive dict if comprehensive=True.
    """
    if comprehensive:
        return compute_comprehensive_metrics(prices, benchmark, periods_per_year, risk_free_rate)

    cagr = compute_cagr(prices, periods_per_year)
    mdd = compute_max_drawdown(prices)
    out = pd.DataFrame({"cagr": cagr, "max_drawdown": mdd})
    out.index.name = "symbol"
    return out

