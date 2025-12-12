"""Price validation checks."""

import pandas as pd

from qldata.common.dataframe.schema import DataFrameSchema
from qldata.common.dataframe.timestamps import TimestampOps
from qldata.validation.core import Severity, ValidationReport
from qldata.validation.rules.ohlcv import OHLCVRules


def _apply_ohlcv_rules(
    cleaned: pd.DataFrame, schema: DataFrameSchema, rules: OHLCVRules
) -> pd.DataFrame:
    """Vectorized application of OHLCV rules."""
    if not schema.has_ohlc:
        return cleaned

    o_col, h_col, l_col, c_col = schema.open, schema.high, schema.low, schema.close
    assert o_col and h_col and l_col and c_col  # narrow for mypy

    # Price bounds
    for col in (o_col, h_col, l_col, c_col):
        cleaned = cleaned[(cleaned[col] > rules.min_price) & (cleaned[col] < rules.max_price)]

    # OHLC relationships
    cleaned = cleaned[cleaned[h_col] >= cleaned[l_col]]
    cleaned = cleaned[cleaned[h_col] >= cleaned[o_col]]
    cleaned = cleaned[cleaned[h_col] >= cleaned[c_col]]
    cleaned = cleaned[cleaned[l_col] <= cleaned[o_col]]
    cleaned = cleaned[cleaned[l_col] <= cleaned[c_col]]

    # Volume (if present)
    if schema.volume and schema.volume in cleaned.columns and not rules.allow_zero_volume:
        cleaned = cleaned[cleaned[schema.volume] > 0]
    elif schema.volume and schema.volume in cleaned.columns:
        cleaned = cleaned[cleaned[schema.volume] >= 0]

    return cleaned


def validate_bars(data: pd.DataFrame) -> pd.DataFrame:
    """Run validation checks on bar data.

    Applies OHLCV validation rules including:
    - Price bounds validation (removes prices outside min/max thresholds)
    - OHLC relationship checks (high >= low, high >= open/close, low <= open/close)
    - Volume non-negativity (removes negative or optionally zero volume)
    - Chronological ordering (sorts by timestamp)
    - Duplicate timestamp removal (keeps last occurrence)

    Args:
        data: DataFrame with OHLCV columns (open, high, low, close, volume)

    Returns:
        Cleaned DataFrame with invalid rows removed and data sorted chronologically
    """
    cleaned = data.copy()
    schema = DataFrameSchema.detect(cleaned)
    rules = OHLCVRules()

    cleaned = _apply_ohlcv_rules(cleaned, schema, rules)

    # Ensure chronological order and drop duplicates
    cleaned = TimestampOps.sort_by_timestamp(cleaned)
    cleaned = TimestampOps.remove_duplicate_timestamps(cleaned, keep="last")
    return cleaned


def check_price_range(
    data: pd.DataFrame,
    report: ValidationReport,
    min_price: float = 0.01,
    max_price: float = 1000000.0,
) -> pd.DataFrame:
    """Check if prices are within reasonable range.

    Args:
        data: DataFrame with price data
        report: ValidationReport to add issues to
        min_price: Minimum reasonable price
        max_price: Maximum reasonable price

    Returns:
        DataFrame with out-of-range prices removed
    """
    cleaned = data.copy()

    price_cols = ["open", "high", "low", "close"]
    for col in price_cols:
        if col not in cleaned.columns:
            continue

        # Find out of range
        too_low = cleaned[col] < min_price
        too_high = cleaned[col] > max_price

        if too_low.any():
            report.add_issue(
                Severity.ERROR,
                "price_range",
                f"{too_low.sum()} rows with {col} < {min_price}",
                suggestion="Check if prices are in correct units",
            )

        if too_high.any():
            report.add_issue(
                Severity.ERROR,
                "price_range",
                f"{too_high.sum()} rows with {col} > {max_price}",
                suggestion="Check for data errors or splits",
            )

        # Remove out of range
        cleaned = cleaned[(cleaned[col] >= min_price) & (cleaned[col] <= max_price)]

    return cleaned


def check_price_continuity(
    data: pd.DataFrame,
    report: ValidationReport,
    max_change_percent: float = 20.0,
) -> pd.DataFrame:
    """Check for unrealistic price jumps.

    Args:
        data: DataFrame with price data
        report: ValidationReport to add issues to
        max_change_percent: Maximum allowed price change percentage

    Returns:
        DataFrame (unchanged, but issues reported)
    """
    if "close" not in data.columns or len(data) < 2:
        return data

    # Calculate price changes
    close_prices = data["close"]
    pct_change = close_prices.pct_change().abs() * 100

    # Find large jumps
    large_jumps = pct_change > max_change_percent

    if large_jumps.any():
        num_jumps = large_jumps.sum()
        max_jump = pct_change.max()

        report.add_issue(
            Severity.WARNING,
            "price_continuity",
            f"{num_jumps} price jumps > {max_change_percent}% (max: {max_jump:.1f}%)",
            suggestion="Check for splits, data errors, or halts",
        )

    return data
