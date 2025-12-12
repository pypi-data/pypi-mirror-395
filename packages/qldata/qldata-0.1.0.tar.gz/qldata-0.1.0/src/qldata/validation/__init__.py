"""Convenient, stable validation exports."""

from typing import Any

import pandas as pd

from qldata.validation.checks import validate_bars
from qldata.validation.checks.price import check_price_continuity, check_price_range
from qldata.validation.checks.timestamp import (
    check_chronological_order,
    check_duplicates,
    check_future_dates,
)
from qldata.validation.checks.volume import check_volume_range, check_zero_volume
from qldata.validation.core import Severity, ValidationIssue, ValidationReport, Validator
from qldata.validation.reports import (
    export_to_csv,
    export_to_html,
    export_to_json,
    generate_summary,
    print_summary,
)


def validate_and_report(
    data: pd.DataFrame,
    validator: Validator,
    path: str | None = None,
    format: str = "json",
) -> tuple[pd.DataFrame, ValidationReport]:
    """Validate data and optionally export a report."""
    cleaned, report = validator.validate_and_fix(data)
    if path:
        fmt = format.lower()
        if fmt == "json":
            export_to_json(report, path)
        elif fmt == "csv":
            export_to_csv(report, path)
        elif fmt == "html":
            export_to_html(report, path)
        else:
            raise ValueError(f"Unsupported format: {format}")
    return cleaned, report


__all__ = [
    "Validator",
    "ValidationIssue",
    "ValidationReport",
    "Severity",
    # Checks
    "validate_bars",
    "check_price_range",
    "check_price_continuity",
    "check_volume_range",
    "check_zero_volume",
    "check_chronological_order",
    "check_future_dates",
    "check_duplicates",
    # Reports
    "generate_summary",
    "print_summary",
    "export_to_json",
    "export_to_csv",
    "export_to_html",
    "validate_and_report",
]
