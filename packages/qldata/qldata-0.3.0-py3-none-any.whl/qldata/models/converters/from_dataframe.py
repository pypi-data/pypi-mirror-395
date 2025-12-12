"""DataFrame to model converters."""

from decimal import Decimal

import pandas as pd

from qldata.models.bar import Bar
from qldata.models.quote import Quote
from qldata.models.tick import Tick


def dataframe_to_ticks(df: pd.DataFrame, symbol: str) -> list[Tick]:
    """Convert DataFrame to list of Tick objects.

    Args:
        df: DataFrame with tick data
        symbol: Symbol ticker

    Returns:
        List of Tick instances
    """
    ticks = []
    for timestamp, row in df.iterrows():
        tick = Tick(
            timestamp=pd.to_datetime(timestamp).to_pydatetime(),
            symbol=symbol,
            price=Decimal(str(row["price"])),
            volume=Decimal(str(row["volume"])),
            bid=Decimal(str(row["bid"])) if pd.notna(row.get("bid")) else None,
            ask=Decimal(str(row["ask"])) if pd.notna(row.get("ask")) else None,
        )
        ticks.append(tick)

    return ticks


def dataframe_to_bars(df: pd.DataFrame, symbol: str) -> list[Bar]:
    """Convert DataFrame to list of Bar objects.

    Args:
        df: DataFrame with OHLCV data
        symbol: Symbol ticker

    Returns:
        List of Bar instances
    """
    bars = []
    for timestamp, row in df.iterrows():
        bar = Bar(
            timestamp=pd.to_datetime(timestamp).to_pydatetime(),
            symbol=symbol,
            open=Decimal(str(row["open"])),
            high=Decimal(str(row["high"])),
            low=Decimal(str(row["low"])),
            close=Decimal(str(row["close"])),
            volume=Decimal(str(row["volume"])),
        )
        bars.append(bar)

    return bars


def dataframe_to_quotes(df: pd.DataFrame, symbol: str) -> list[Quote]:
    """Convert DataFrame to list of Quote objects.

    Args:
        df: DataFrame with quote data
        symbol: Symbol ticker

    Returns:
        List of Quote instances
    """
    quotes = []
    for timestamp, row in df.iterrows():
        quote = Quote(
            timestamp=pd.to_datetime(timestamp).to_pydatetime(),
            symbol=symbol,
            bid=Decimal(str(row["bid"])),
            ask=Decimal(str(row["ask"])),
            bid_size=Decimal(str(row["bid_size"])) if pd.notna(row.get("bid_size")) else None,
            ask_size=Decimal(str(row["ask_size"])) if pd.notna(row.get("ask_size")) else None,
        )
        quotes.append(quote)

    return quotes
