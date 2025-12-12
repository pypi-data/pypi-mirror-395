"""Export validation reports to various formats."""

import json
from pathlib import Path

import pandas as pd

from qldata.validation.core import ValidationReport


def export_to_json(report: ValidationReport, filepath: str | Path) -> None:
    """Export validation report to JSON.

    Args:
        report: ValidationReport
        filepath: Output file path
    """
    data = {
        "total_rows": report.total_rows,
        "valid_rows": report.valid_rows,
        "invalid_rows": report.invalid_rows,
        "metadata": report.metadata,
        "issues": [
            {
                "severity": issue.severity.value,
                "rule_name": issue.rule_name,
                "message": issue.message,
                "timestamp": issue.timestamp.isoformat() if issue.timestamp else None,
                "row_index": issue.row_index,
                "column": issue.column,
                "value": str(issue.value) if issue.value is not None else None,
                "suggestion": issue.suggestion,
            }
            for issue in report.issues
        ],
    }

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def export_to_csv(report: ValidationReport, filepath: str | Path) -> None:
    """Export validation issues to CSV.

    Args:
        report: ValidationReport
        filepath: Output file path
    """
    if not report.issues:
        # Create empty DataFrame
        df = pd.DataFrame(columns=["severity", "rule_name", "message", "suggestion"])
    else:
        df = pd.DataFrame(
            [
                {
                    "severity": issue.severity.value,
                    "rule_name": issue.rule_name,
                    "message": issue.message,
                    "timestamp": issue.timestamp,
                    "row_index": issue.row_index,
                    "column": issue.column,
                    "value": issue.value,
                    "suggestion": issue.suggestion,
                }
                for issue in report.issues
            ]
        )

    df.to_csv(filepath, index=False)


def export_to_html(report: ValidationReport, filepath: str | Path) -> None:
    """Export validation report to HTML.

    Args:
        report: ValidationReport
        filepath: Output file path
    """
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Validation Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .summary {{ background: #f5f5f5; padding: 15px; border-radius: 5px; }}
        .issues {{ margin-top: 20px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        .error {{ color: red; }}
        .warning {{ color: orange; }}
        .info {{ color: blue; }}
    </style>
</head>
<body>
    <h1>Validation Report</h1>
    <div class="summary">
        <p><strong>Total rows:</strong> {report.total_rows}</p>
        <p><strong>Valid rows:</strong> {report.valid_rows}</p>
        <p><strong>Invalid rows:</strong> {report.invalid_rows}</p>
        <p><strong>Total issues:</strong> {len(report.issues)}</p>
    </div>

    <div class="issues">
        <h2>Issues</h2>
        <table>
            <tr>
                <th>Severity</th>
                <th>Rule</th>
                <th>Message</th>
                <th>Suggestion</th>
            </tr>
    """

    for issue in report.issues:
        severity_class = issue.severity.value
        html += f"""
            <tr>
                <td class="{severity_class}">{issue.severity.value.upper()}</td>
                <td>{issue.rule_name}</td>
                <td>{issue.message}</td>
                <td>{issue.suggestion or '-'}</td>
            </tr>
        """

    html += """
        </table>
    </div>
</body>
</html>
    """

    with open(filepath, "w") as f:
        f.write(html)
