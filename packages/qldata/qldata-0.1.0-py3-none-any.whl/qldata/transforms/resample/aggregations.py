"""OHLCV aggregation functions."""

from typing import Any

import pandas as pd


def aggregate_ohlcv(ticks: pd.DataFrame) -> dict[str, Any]:
    """Aggregate ticks into OHLCV values.

    Args:
        ticks: DataFrame with tick data (must have 'price' and 'volume' columns)

    Returns:
        Dictionary with OHLCV values

    Example:
        >>> ticks = pd.DataFrame({'price': [100, 101, 99, 102], 'volume': [1000, 2000, 1500, 1000]})
        >>> ohlcv = aggregate_ohlcv(ticks)
        >>> ohlcv['open'], ohlcv['high'], ohlcv['low'], ohlcv['close']
        (100, 102, 99, 102)
    """
    if ticks.empty:
        return {
            "open": None,
            "high": None,
            "low": None,
            "close": None,
            "volume": 0,
        }

    return {
        "open": ticks["price"].iloc[0],
        "high": ticks["price"].max(),
        "low": ticks["price"].min(),
        "close": ticks["price"].iloc[-1],
        "volume": ticks["volume"].sum(),
    }


def aggregate_vwap(ticks: pd.DataFrame) -> float:
    """Calculate volume-weighted average price.

    Args:
        ticks: DataFrame with tick data (must have 'price' and 'volume' columns)

    Returns:
        VWAP value

    Example:
        >>> ticks = pd.DataFrame({'price': [100, 101, 99], 'volume': [1000, 2000, 1500]})
        >>> vwap = aggregate_vwap(ticks)
        >>> round(vwap, 2)
        100.11
    """
    if ticks.empty or ticks["volume"].sum() == 0:
        return 0.0

    return float((ticks["price"] * ticks["volume"]).sum() / ticks["volume"].sum())


def aggregate_bars(bars: pd.DataFrame) -> dict[str, Any]:
    """Aggregate multiple bars into a single bar.

    Used for resampling bars to higher timeframes.

    Args:
        bars: DataFrame with OHLCV bar data

    Returns:
        Dictionary with aggregated OHLCV values
    """
    if bars.empty:
        return {
            "open": None,
            "high": None,
            "low": None,
            "close": None,
            "volume": 0,
        }

    return {
        "open": bars["open"].iloc[0],
        "high": bars["high"].max(),
        "low": bars["low"].min(),
        "close": bars["close"].iloc[-1],
        "volume": bars["volume"].sum(),
    }
