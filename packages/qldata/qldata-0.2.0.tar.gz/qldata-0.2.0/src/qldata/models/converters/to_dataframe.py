"""Model to DataFrame converters."""

import pandas as pd

from qldata.models.bar import Bar
from qldata.models.quote import Quote
from qldata.models.tick import Tick


def ticks_to_dataframe(ticks: list[Tick]) -> pd.DataFrame:
    """Convert list of Tick objects to DataFrame.

    Args:
        ticks: List of Tick instances

    Returns:
        DataFrame with tick data, indexed by timestamp
    """
    if not ticks:
        return pd.DataFrame(
            columns=["timestamp", "symbol", "price", "volume", "bid", "ask"]
        ).set_index("timestamp")

    data = {
        "timestamp": [t.timestamp for t in ticks],
        "symbol": [t.symbol for t in ticks],
        "price": [float(t.price) for t in ticks],
        "volume": [float(t.volume) for t in ticks],
        "bid": [float(t.bid) if t.bid is not None else None for t in ticks],
        "ask": [float(t.ask) if t.ask is not None else None for t in ticks],
    }

    df = pd.DataFrame(data)
    df.set_index("timestamp", inplace=True)
    return df


def bars_to_dataframe(bars: list[Bar]) -> pd.DataFrame:
    """Convert list of Bar objects to DataFrame.

    Args:
        bars: List of Bar instances

    Returns:
        DataFrame with OHLCV data, indexed by timestamp
    """
    if not bars:
        return pd.DataFrame(
            columns=["timestamp", "symbol", "open", "high", "low", "close", "volume"]
        ).set_index("timestamp")

    data = {
        "timestamp": [b.timestamp for b in bars],
        "symbol": [b.symbol for b in bars],
        "open": [float(b.open) for b in bars],
        "high": [float(b.high) for b in bars],
        "low": [float(b.low) for b in bars],
        "close": [float(b.close) for b in bars],
        "volume": [float(b.volume) for b in bars],
    }

    df = pd.DataFrame(data)
    df.set_index("timestamp", inplace=True)
    return df


def quotes_to_dataframe(quotes: list[Quote]) -> pd.DataFrame:
    """Convert list of Quote objects to DataFrame.

    Args:
        quotes: List of Quote instances

    Returns:
        DataFrame with quote data, indexed by timestamp
    """
    if not quotes:
        return pd.DataFrame(
            columns=["timestamp", "symbol", "bid", "ask", "bid_size", "ask_size"]
        ).set_index("timestamp")

    data = {
        "timestamp": [q.timestamp for q in quotes],
        "symbol": [q.symbol for q in quotes],
        "bid": [float(q.bid) for q in quotes],
        "ask": [float(q.ask) for q in quotes],
        "bid_size": [float(q.bid_size) if q.bid_size is not None else None for q in quotes],
        "ask_size": [float(q.ask_size) if q.ask_size is not None else None for q in quotes],
    }

    df = pd.DataFrame(data)
    df.set_index("timestamp", inplace=True)
    return df
