import numpy as np
import pandas as pd

# ==== Configuration System Tests ====


def test_report_with_specific_checks():
    """Test that report runs only specified checks"""
    df = pd.DataFrame({"a": [1, np.nan, 3], "b": [1, 2, 2]})

    # Only run missing check
    report = df.lint.report(checks_to_run=["missing"])
    assert "Missing Values" in report
    assert "Duplicate" not in report


def test_report_with_multiple_specific_checks():
    """Test running multiple specific checks"""
    df = pd.DataFrame({"a": [1, np.nan, 3, 3], "b": [1, 2, 4, 4]})

    report = df.lint.report(checks_to_run=["missing", "duplicates"])
    assert "Missing Values" in report
    assert "Duplicate" in report


def test_report_with_invalid_check_name():
    """Test that invalid check names raise ValueError"""
    df = pd.DataFrame({"a": [1, 2, 3]})

    try:
        df.lint.report(checks_to_run=["invalid_check"])
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Invalid check(s)" in str(e)


def test_report_with_custom_thresholds():
    """Test that custom thresholds are applied"""
    df = pd.DataFrame({"a": [1, 2, 3, 100]})

    # Default threshold
    report_default = df.lint.report(checks_to_run=["outliers"])
    assert "Outliers" in report_default

    # Higher threshold - should find no outliers
    report_high = df.lint.report(checks_to_run=["outliers"], outlier_threshold=5.0)
    assert "No issues found" in report_high


def test_report_with_all_keyword():
    """Test that 'all' runs all checks"""
    df = pd.DataFrame({"a": [1, 2, 3]})

    report = df.lint.report(checks_to_run="all")
    assert "LintData Quality Report" in report
