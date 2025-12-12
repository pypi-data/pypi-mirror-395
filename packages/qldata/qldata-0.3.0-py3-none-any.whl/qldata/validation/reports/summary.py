"""Summary validation report."""

from qldata.validation.core import ValidationReport


def generate_summary(report: ValidationReport) -> dict:
    """Generate summary statistics from validation report.

    Args:
        report: ValidationReport

    Returns:
        Dictionary with summary statistics
    """
    # Count by severity
    severity_counts: dict[str, int] = {
        "info": 0,
        "warning": 0,
        "error": 0,
        "critical": 0,
    }

    for issue in report.issues:
        severity_counts[issue.severity.value] += 1

    # Group by rule
    rule_counts: dict[str, int] = {}
    for issue in report.issues:
        rule_counts[issue.rule_name] = rule_counts.get(issue.rule_name, 0) + 1

    return {
        "total_rows": report.total_rows,
        "valid_rows": report.valid_rows,
        "invalid_rows": report.invalid_rows,
        "pass_rate": (report.valid_rows / report.total_rows * 100) if report.total_rows > 0 else 0,
        "total_issues": len(report.issues),
        "by_severity": severity_counts,
        "by_rule": rule_counts,
        "has_errors": report.has_errors,
        "has_warnings": report.has_warnings,
    }


def print_summary(report: ValidationReport) -> None:
    """Print human-readable summary.

    Args:
        report: ValidationReport
    """
    summary = generate_summary(report)

    print(report.summary())
    print()

    if summary["by_rule"]:
        print("Issues by rule:")
        for rule_name, count in sorted(summary["by_rule"].items(), key=lambda x: -x[1]):
            print(f"  {rule_name}: {count}")
