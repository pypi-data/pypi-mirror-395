"""Base validator class."""

from collections.abc import Callable

import pandas as pd

from qldata.common.logger import get_logger
from qldata.validation.core.reporter import Severity, ValidationReport

logger = get_logger(__name__)


class Validator:
    """Base validator for running validation rules on data.

    Example:
        >>> validator = Validator()
        >>> validator.add_rule(check_positive_prices, "positive_prices")
        >>> report = validator.validate(data)
        >>> print(report.summary())
    """

    def __init__(self) -> None:
        """Initialize validator."""
        self._rules: list[tuple[str, Callable]] = []

    def add_rule(
        self,
        rule: Callable[[pd.DataFrame, ValidationReport], pd.DataFrame],
        name: str,
    ) -> "Validator":
        """Add a validation rule.

        Args:
            rule: Validation function that takes (data, report) and returns cleaned data
            name: Rule name for reporting

        Returns:
            Self for method chaining
        """
        self._rules.append((name, rule))
        return self

    def validate(self, data: pd.DataFrame) -> ValidationReport:
        """Run all validation rules and generate report.

        Args:
            data: DataFrame to validate

        Returns:
            ValidationReport with issues found
        """
        report = ValidationReport(
            total_rows=len(data),
            valid_rows=len(data),
        )

        # Run each rule
        for rule_name, rule_func in self._rules:
            try:
                logger.debug(f"Running validation rule: {rule_name}")
                rule_func(data, report)
            except Exception as e:
                logger.error(f"Validation rule '{rule_name}' failed: {e}", exc_info=True)
                report.add_issue(Severity.CRITICAL, rule_name, f"Rule execution failed: {e}")

        return report

    def validate_and_fix(self, data: pd.DataFrame) -> tuple[pd.DataFrame, ValidationReport]:
        """Run validation and return cleaned data.

        Args:
            data: DataFrame to validate

        Returns:
            Tuple of (cleaned_data, report)
        """
        report = ValidationReport(
            total_rows=len(data),
            valid_rows=len(data),
        )

        cleaned = data.copy()

        # Run each rule and fix issues
        for rule_name, rule_func in self._rules:
            try:
                logger.debug(f"Running validation rule with fixes: {rule_name}")
                cleaned = rule_func(cleaned, report)
            except Exception as e:
                logger.error(f"Validation rule '{rule_name}' failed during fix: {e}", exc_info=True)
                report.add_issue(Severity.CRITICAL, rule_name, f"Rule execution failed: {e}")

        report.valid_rows = len(cleaned)
        removed_rows = len(data) - len(cleaned)
        if removed_rows > 0:
            logger.info(f"Validation removed {removed_rows} invalid rows")

        return cleaned, report
