"""Schema detection helpers for financial DataFrames."""

from dataclasses import dataclass

import pandas as pd


@dataclass
class DataFrameSchema:
    """Detected OHLCV schema for a DataFrame."""

    open: str | None = None
    high: str | None = None
    low: str | None = None
    close: str | None = None
    volume: str | None = None

    @classmethod
    def detect(cls, df: pd.DataFrame) -> "DataFrameSchema":
        """Auto-detect OHLCV columns (case-insensitive)."""
        cols_lower = {col.lower(): col for col in df.columns}
        return cls(
            open=cols_lower.get("open"),
            high=cols_lower.get("high"),
            low=cols_lower.get("low"),
            close=cols_lower.get("close"),
            volume=cols_lower.get("volume"),
        )

    @property
    def has_ohlcv(self) -> bool:
        return all([self.open, self.high, self.low, self.close, self.volume])

    @property
    def has_ohlc(self) -> bool:
        return all([self.open, self.high, self.low, self.close])

    @property
    def price_columns(self) -> list[str]:
        return [col for col in [self.open, self.high, self.low, self.close] if col]

    def to_dict(self) -> dict[str, str | None]:
        return {
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
        }


__all__ = ["DataFrameSchema"]
