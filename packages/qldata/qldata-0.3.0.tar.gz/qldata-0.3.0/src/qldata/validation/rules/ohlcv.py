"""Centralized OHLCV validation rules."""

from collections.abc import Iterable
from dataclasses import dataclass


@dataclass
class OHLCVRules:
    """Single source of truth for OHLC relationships and positivity checks."""

    allow_zero_volume: bool = True
    min_price: float = 0.0
    max_price: float = float("inf")

    def _prices_positive(self, prices: Iterable[float]) -> bool:
        return all(self.min_price < p < self.max_price for p in prices)

    def validate_all(self, o: float, h: float, low: float, c: float) -> tuple[bool, list[str]]:
        """Run all validation rules and return (is_valid, errors)."""
        errors: list[str] = []

        if not self._prices_positive((o, h, low, c)):
            errors.append("Prices must be positive and within configured bounds")

        if h < low:
            errors.append(f"High ({h}) must be >= low ({low})")

        if h < o or h < c:
            errors.append(f"High ({h}) must be >= open ({o}) and close ({c})")

        if low > o or low > c:
            errors.append(f"Low ({low}) must be <= open ({o}) and close ({c})")

        return len(errors) == 0, errors


__all__ = ["OHLCVRules"]
