import tempfile
from pathlib import Path

import numpy as np
import pandas as pd


def test_html_report_generation():
    """Test that HTML report generates valid HTML."""
    df = pd.DataFrame({"a": [1, np.nan, 3], "b": [1, 2, 2]})

    html_report = df.lint.report(report_format="html")

    # Check HTML structure
    assert "<!DOCTYPE html>" in html_report
    assert "<html" in html_report
    assert "</html>" in html_report
    assert "LintData Quality Report" in html_report
    assert "Missing Values" in html_report


def test_html_report_clean_data():
    """Test HTML report with clean data (no issues)."""
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
            "value": [
                10,
                20,
                30,
                40,
                50,
                60,
                70,
                80,
                90,
                100,
                10,
                20,
                30,
                40,
                50,
                60,
                70,
                80,
                90,
                100,
            ],
        }
    )

    html_report = df.lint.report(report_format="html")

    assert "No issues found" in html_report
    assert "DataFrame looks good" in html_report


def test_html_report_save_to_file():
    """Test saving HTML report to file."""
    df = pd.DataFrame({"a": [1, np.nan, 3]})

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "report.html"

        # Generate and save
        result = df.lint.report(report_format="html", output=str(output_path))

        # Check file exists
        assert output_path.exists()

        # Check file content
        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()

        assert "<!DOCTYPE html>" in content
        assert "LintData Quality Report" in content
        assert "Missing Values" in content

        # Check return value matches file content
        assert result == content


def test_html_report_metadata():
    """Test that HTML report includes DataFrame metadata."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]})

    html_report = df.lint.report(report_format="html")

    # Check shape is displayed
    assert "3" in html_report  # 3 rows or 3 columns
    assert "Rows" in html_report
    assert "Columns" in html_report


def test_html_report_multiple_issues():
    """Test HTML report with multiple issues."""
    df = pd.DataFrame(
        {
            "a": [1, np.nan, 3, 3],  # Missing value + duplicates
            "b": [" x", "y", "z", "z"],  # Whitespace
            "c": [1, "two", 3, 3],  # Mixed types
        }
    )

    html_report = df.lint.report(report_format="html")

    # Check all issues are present
    assert "Missing Values" in html_report
    assert "Duplicate" in html_report
    assert "Whitespace" in html_report
    assert "Mixed Types" in html_report

    # Check issue count
    assert ">4<" in html_report or "4</div>" in html_report


def test_html_report_specific_checks():
    """Test HTML report with specific checks only."""
    df = pd.DataFrame({"a": [1, np.nan, 3], "b": [1, 2, 2]})

    html_report = df.lint.report(report_format="html", checks_to_run=["missing"])

    # Only missing values should be reported
    assert "Missing Values" in html_report
    # Duplicates should not be in report
    assert "Duplicate" not in html_report


def test_html_report_empty_dataframe():
    """Test HTML report with empty DataFrame."""
    df = pd.DataFrame()

    html_report = df.lint.report(report_format="html")

    assert "<!DOCTYPE html>" in html_report
    assert "LintData Quality Report" in html_report
    # Should handle empty DataFrame gracefully


def test_html_report_has_styling():
    """Test that HTML report includes CSS styling."""
    df = pd.DataFrame({"a": [1, 2, 3]})

    html_report = df.lint.report(report_format="html")

    # Check for CSS
    assert "<style>" in html_report
    assert "</style>" in html_report
    assert "background" in html_report
    assert "color" in html_report


def test_text_format_still_works():
    """Test that text format (default) still works correctly."""
    df = pd.DataFrame({"a": [1, np.nan, 3]})

    # Default format should be text
    text_report = df.lint.report()

    assert "--- LintData Quality Report ---" in text_report
    assert "[Missing Values]" in text_report
    assert "<!DOCTYPE html>" not in text_report


def test_invalid_format_raises_error():
    """Test that invalid format raises ValueError."""
    df = pd.DataFrame({"a": [1, 2, 3]})

    try:
        df.lint.report(report_format="pdf")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Invalid format" in str(e)
        assert "pdf" in str(e)


def test_html_report_severity_levels():
    """Test that HTML report includes severity styling."""
    df = pd.DataFrame(
        {
            "a": [1, np.nan, 3],  # High severity (missing values)
            "b": [1, 2, 100],  # Medium severity (outliers)
            "c": ["x", "x", "x"],  # Low severity (constant)
        }
    )

    html_report = df.lint.report(report_format="html")

    assert 'class="warning' in html_report


def test_html_report_escapes_special_chars():
    """Test that HTML report properly escapes special characters."""
    # This is important for security (XSS prevention)
    df = pd.DataFrame({"<script>": [1, 2, 3]})

    html_report = df.lint.report(report_format="html")

    assert "&lt;script&gt;" in html_report


def test_html_report_with_custom_thresholds():
    """Test HTML report with custom check thresholds."""
    df = pd.DataFrame({"a": [1, 2, 3, 100]})

    html_report = df.lint.report(report_format="html", checks_to_run=["outliers"], outlier_threshold=5.0)

    # With high threshold, should find no outliers
    assert "No issues found" in html_report
