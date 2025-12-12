"""Centralized OHLCV validation rules."""

from dataclasses import dataclass
from typing import Iterable


@dataclass
class OHLCVRules:
    """Single source of truth for OHLC relationships and positivity checks."""

    allow_zero_volume: bool = True
    min_price: float = 0.0
    max_price: float = float("inf")

    def _prices_positive(self, prices: Iterable[float]) -> bool:
        return all(self.min_price < p < self.max_price for p in prices)

    def validate_all(self, o: float, h: float, l: float, c: float) -> tuple[bool, list[str]]:
        """Run all validation rules and return (is_valid, errors)."""
        errors: list[str] = []

        if not self._prices_positive((o, h, l, c)):
            errors.append("Prices must be positive and within configured bounds")

        if h < l:
            errors.append(f"High ({h}) must be >= low ({l})")

        if h < o or h < c:
            errors.append(f"High ({h}) must be >= open ({o}) and close ({c})")

        if l > o or l > c:
            errors.append(f"Low ({l}) must be <= open ({o}) and close ({c})")

        return len(errors) == 0, errors


__all__ = ["OHLCVRules"]
