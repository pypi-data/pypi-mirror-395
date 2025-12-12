"""Validation framework and report."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class Severity(Enum):
    """Validation issue severity levels."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationIssue:
    """Represents a single validation issue."""

    severity: Severity
    rule_name: str
    message: str
    timestamp: datetime | None = None
    row_index: int | None = None
    column: str | None = None
    value: Any = None
    suggestion: str | None = None


@dataclass
class ValidationReport:
    """Report containing all validation results."""

    total_rows: int
    valid_rows: int
    issues: list[ValidationIssue] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def invalid_rows(self) -> int:
        """Get number of invalid rows."""
        return self.total_rows - self.valid_rows

    @property
    def has_errors(self) -> bool:
        """Check if report has any errors."""
        return any(issue.severity in (Severity.ERROR, Severity.CRITICAL) for issue in self.issues)

    @property
    def has_warnings(self) -> bool:
        """Check if report has any warnings."""
        return any(issue.severity == Severity.WARNING for issue in self.issues)

    def summary(self) -> str:
        """Get summary of validation report.

        Returns:
            String summary
        """
        lines = [
            "Validation Report",
            "=" * 50,
            f"Total rows: {self.total_rows}",
            f"Valid rows: {self.valid_rows}",
            f"Invalid rows: {self.invalid_rows}",
            "",
            "Issues by severity:",
        ]

        # Count by severity
        severity_counts: dict[Severity, int] = {}
        for issue in self.issues:
            severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1

        for severity in Severity:
            count = severity_counts.get(severity, 0)
            lines.append(f"  {severity.value.upper()}: {count}")

        return "\n".join(lines)

    def add_issue(self, severity: Severity, rule_name: str, message: str, **kwargs: Any) -> None:
        """Add an issue to the report.

        Args:
            severity: Issue severity
            rule_name: Name of validation rule
            message: Issue description
            **kwargs: Additional issue attributes
        """
        issue = ValidationIssue(severity=severity, rule_name=rule_name, message=message, **kwargs)
        self.issues.append(issue)
