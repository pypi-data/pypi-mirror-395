"""Volume validation checks."""

import pandas as pd

from qldata.validation.core import Severity, ValidationReport


def check_volume_range(
    data: pd.DataFrame,
    report: ValidationReport,
    min_volume: float = 0,
    max_volume: float = 1e12,
) -> pd.DataFrame:
    """Check if volumes are within reasonable range.

    Args:
        data: DataFrame with volume data
        report: ValidationReport to add issues to
        min_volume: Minimum reasonable volume
        max_volume: Maximum reasonable volume

    Returns:
        DataFrame with out-of-range volumes removed
    """
    if "volume" not in data.columns:
        return data

    cleaned = data.copy()

    # Find out of range
    too_low = cleaned["volume"] < min_volume
    too_high = cleaned["volume"] > max_volume

    if too_low.any():
        report.add_issue(
            Severity.ERROR,
            "volume_range",
            f"{too_low.sum()} rows with volume < {min_volume}",
        )

    if too_high.any():
        report.add_issue(
            Severity.WARNING,
            "volume_range",
            f"{too_high.sum()} rows with volume > {max_volume}",
            suggestion="Check for unusual trading activity",
        )

    # Remove out of range
    cleaned = cleaned[(cleaned["volume"] >= min_volume) & (cleaned["volume"] <= max_volume)]

    return cleaned


def check_zero_volume(
    data: pd.DataFrame,
    report: ValidationReport,
) -> pd.DataFrame:
    """Check for zero-volume bars.

    Args:
        data: DataFrame with volume data
        report: ValidationReport to add issues to

    Returns:
        DataFrame (unchanged)
    """
    if "volume" not in data.columns:
        return data

    zero_vol = data["volume"] == 0

    if zero_vol.any():
        count = zero_vol.sum()
        pct = (count / len(data)) * 100

        report.add_issue(
            Severity.INFO,
            "zero_volume",
            f"{count} bars ({pct:.1f}%) with zero volume",
            suggestion="Normal for some securities, but verify data source",
        )

    return data
