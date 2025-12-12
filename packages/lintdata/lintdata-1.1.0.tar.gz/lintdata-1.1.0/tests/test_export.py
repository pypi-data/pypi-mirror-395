import csv
import json
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

# ==== JSON Export Tests ====


def test_json_export_generation():
    """Test that JSON export generates valid JSON."""
    df = pd.DataFrame({"a": [1, np.nan, 3], "b": [1, 2, 2]})

    json_report = df.lint.report(report_format="json")

    # Should be valid JSON
    data = json.loads(json_report)

    # Check structure
    assert "shape" in data
    assert "issue_count" in data
    assert "issues" in data
    assert data["shape"] == [3, 2]
    assert data["issue_count"] > 0


def test_json_export_clean_data():
    """Test JSON export with clean data."""
    df = pd.DataFrame(
        {
            "id": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10],
            "category": [
                "A",
                "B",
                "C",
                "A",
                "B",
                "C",
                "A",
                "B",
                "C",
                "A",
                "B",
                "C",
                "A",
                "B",
                "C",
                "A",
                "B",
                "C",
                "A",
                "B",
            ],
            "value": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        }
    )

    json_report = df.lint.report(report_format="json")
    data = json.loads(json_report)

    assert data["issue_count"] == 0
    assert data["issues"] == []


def test_json_export_save_to_file():
    """Test saving JSON report to file."""
    df = pd.DataFrame({"a": [1, np.nan, 3]})

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "report.json"

        # Generate and save
        result = df.lint.report(report_format="json", output=str(output_path))

        # Check file exists
        assert output_path.exists()

        # Check file content is valid JSON
        with open(output_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert "shape" in data
        assert "issues" in data

        # Check return value matches file content
        assert result == json.dumps(data, indent=2)


def test_json_export_issue_structure():
    """Test that JSON issues have correct structure."""
    df = pd.DataFrame({"a": [1, np.nan, 3], "b": [" x", "y", "z"]})

    json_report = df.lint.report(report_format="json", checks_to_run=["missing", "whitespace"])
    data = json.loads(json_report)

    # Check each issue has required fields
    for issue in data["issues"]:
        assert "check" in issue
        assert "column" in issue
        assert "severity" in issue
        assert "message" in issue

        # Severity should be valid
        assert issue["severity"] in ["high", "medium", "low"]


def test_json_export_specific_checks():
    """Test JSON export with specific checks only."""
    df = pd.DataFrame({"a": [1, np.nan, 3], "b": [1, 2, 2]})

    json_report = df.lint.report(report_format="json", checks_to_run=["missing"])
    data = json.loads(json_report)

    # Should only have missing values issues
    assert all("Missing Values" in issue["check"] for issue in data["issues"])


# ==== CSV Export Tests ====


def test_csv_export_generation():
    """Test that CSV export generates valid CSV."""
    df = pd.DataFrame({"a": [1, np.nan, 3], "b": [1, 2, 2]})

    csv_report = df.lint.report(report_format="csv")

    # Should have header
    assert "check,column,severity,message" in csv_report

    # Should have data rows
    lines = csv_report.strip().split("\n")
    assert len(lines) > 1  # Header + at least one issue


def test_csv_export_clean_data():
    """Test CSV export with clean data."""
    df = pd.DataFrame(
        {
            "id": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10],
            "category": [
                "A",
                "B",
                "C",
                "A",
                "B",
                "C",
                "A",
                "B",
                "C",
                "A",
                "B",
                "C",
                "A",
                "B",
                "C",
                "A",
                "B",
                "C",
                "A",
                "B",
            ],
            "value": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        }
    )

    csv_report = df.lint.report(report_format="csv")

    # Should only have header
    lines = csv_report.strip().split("\n")
    assert len(lines) == 1  # Just header
    assert "check,column,severity,message" in csv_report


def test_csv_export_save_to_file():
    """Test saving CSV report to file."""
    df = pd.DataFrame({"a": [1, np.nan, 3]})

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "issues.csv"

        # Generate and save
        result = df.lint.report(report_format="csv", output=str(output_path))

        # Check file exists
        assert output_path.exists()

        # Check file content is valid CSV
        with open(output_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) > 0
        assert "check" in rows[0]
        assert "column" in rows[0]

        # Check return value matches file content
        with open(output_path, "r", encoding="utf-8") as f:
            file_content = f.read()

        assert result.replace("\r\n", "\n").strip() == file_content.replace("\r\n", "\n").strip()


def test_csv_export_structure():
    """Test that CSV has correct column structure."""
    df = pd.DataFrame({"a": [1, np.nan, 3], "b": [" x", "y", "z"]})

    csv_report = df.lint.report(report_format="csv", checks_to_run=["missing", "whitespace"])

    from io import StringIO

    reader = csv.DictReader(StringIO(csv_report))
    rows = list(reader)

    # Check columns
    assert reader.fieldnames == ["check", "column", "severity", "message"]

    # Check each row has values
    for row in rows:
        assert row["check"] != ""
        assert row["severity"] in ["high", "medium", "low"]
        assert row["message"] != ""


def test_csv_export_specific_checks():
    """Test CSV export with specific checks only."""
    df = pd.DataFrame({"a": [1, np.nan, 3], "b": [1, 2, 2]})

    csv_report = df.lint.report(report_format="csv", checks_to_run=["missing"])

    from io import StringIO

    reader = csv.DictReader(StringIO(csv_report))
    rows = list(reader)

    # Should only have missing values issues
    assert all("Missing Values" in row["check"] for row in rows)


# ==== return_dict Tests ====


def test_return_dict_basic():
    """Test return_dict returns structured dictionary."""
    df = pd.DataFrame({"a": [1, np.nan, 3]})

    data = df.lint.report(return_dict=True)

    assert isinstance(data, dict)
    assert "shape" in data
    assert "issue_count" in data
    assert "issues" in data


def test_return_dict_structure():
    """Test return_dict structure matches JSON."""
    df = pd.DataFrame({"a": [1, np.nan, 3]})

    # Get both formats
    dict_data = df.lint.report(return_dict=True)
    json_str = df.lint.report(report_format="json")
    json_data = json.loads(json_str)

    # Should be identical
    assert dict_data == json_data


def test_return_dict_with_checks():
    """Test return_dict with specific checks."""
    df = pd.DataFrame({"a": [1, np.nan, 3], "b": [1, 2, 2]})

    data = df.lint.report(return_dict=True, checks_to_run=["missing"])

    assert len(data["issues"]) == 1
    assert "Missing Values" in data["issues"][0]["check"]


def test_return_dict_clean_data():
    """Test return_dict with clean data."""
    df = pd.DataFrame(
        {
            "id": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10],
            "category": [
                "A",
                "B",
                "C",
                "A",
                "B",
                "C",
                "A",
                "B",
                "C",
                "A",
                "B",
                "C",
                "A",
                "B",
                "C",
                "A",
                "B",
                "C",
                "A",
                "B",
            ],
            "value": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        }
    )

    data = df.lint.report(return_dict=True)

    assert data["issue_count"] == 0
    assert data["issues"] == []


# ==== Format Validation Tests ====


def test_invalid_format_raises_error():
    """Test that invalid format raises ValueError."""
    df = pd.DataFrame({"a": [1, 2, 3]})

    try:
        df.lint.report(report_format="xml")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Invalid format" in str(e)
        assert "xml" in str(e)


def test_all_formats_work():
    """Test that all valid formats work."""
    df = pd.DataFrame({"a": [1, np.nan, 3]})

    # Text
    text = df.lint.report(report_format="text")
    assert "LintData Quality Report" in text

    # HTML
    html = df.lint.report(report_format="html")
    assert "<!DOCTYPE html>" in html

    # JSON
    json_str = df.lint.report(report_format="json")
    data = json.loads(json_str)
    assert "issues" in data

    # CSV
    csv_str = df.lint.report(report_format="csv")
    assert "check,column,severity,message" in csv_str


# ==== Empty DataFrame Tests ====


def test_json_export_empty_dataframe():
    """Test JSON export with empty DataFrame."""
    df = pd.DataFrame()

    json_report = df.lint.report(report_format="json")
    data = json.loads(json_report)

    assert data["shape"] == [0, 0]
    assert data["issue_count"] == 0
    assert data["issues"] == []


def test_csv_export_empty_dataframe():
    """Test CSV export with empty DataFrame."""
    df = pd.DataFrame()

    csv_report = df.lint.report(report_format="csv")

    # Should have header
    assert "check,column,severity,message" in csv_report

    # Should have no data rows
    lines = csv_report.strip().split("\n")
    assert len(lines) == 1


def test_return_dict_empty_dataframe():
    """Test return_dict with empty DataFrame."""
    df = pd.DataFrame()

    data = df.lint.report(return_dict=True)

    assert data["shape"] == [0, 0]
    assert data["issue_count"] == 0
    assert data["issues"] == []
