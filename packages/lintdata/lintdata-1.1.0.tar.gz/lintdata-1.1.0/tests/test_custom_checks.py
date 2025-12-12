"""
Tests for the custom check API framework.
"""

import pandas as pd


def test_register_custom_check():
    """Test registering a custom check function."""
    df = pd.DataFrame({"email": ["test@example.com", "invalid-email", "another@test.com"]})

    def check_email_format(df):
        warnings = []
        for col in df.select_dtypes(include="object").columns:
            if "email" in col.lower():
                # Simple check for @ symbol
                invalid = df[~df[col].str.contains("@", na=False)]
                if len(invalid) > 0:
                    warnings.append(f"[Email] Column '{col}': {len(invalid)} invalid email(s)")
        return warnings

    # Register the check
    df.lint.register_check(check_email_format)

    # Verify it's registered
    assert "check_email_format" in df.lint.list_custom_checks()

    # Run report and verify custom check is executed
    report = df.lint.report()
    assert "Email" in report


def test_register_custom_check_with_name():
    """Test registering a custom check with a custom name."""
    df = pd.DataFrame({"value": [1, 2, 3]})

    def my_check(df):
        return ["[Custom] Test warning"]

    df.lint.register_check(my_check, name="my_custom_check")

    assert "my_custom_check" in df.lint.list_custom_checks()
    assert "my_check" not in df.lint.list_custom_checks()


def test_unregister_custom_check():
    """Test unregistering a custom check."""
    df = pd.DataFrame({"value": [1, 2, 3]})

    def my_check(df):
        return []

    df.lint.register_check(my_check)
    assert "my_check" in df.lint.list_custom_checks()

    df.lint.unregister_check("my_check")
    assert "my_check" not in df.lint.list_custom_checks()


def test_register_duplicate_check_raises_error():
    """Test that registering duplicate check name raises error."""
    df = pd.DataFrame({"value": [1, 2, 3]})

    def my_check(df):
        return []

    df.lint.register_check(my_check)

    try:
        df.lint.register_check(my_check)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "already registered" in str(e)


def test_unregister_nonexistent_check_raises_error():
    """Test that unregistering non-existent check raises error."""
    df = pd.DataFrame({"value": [1, 2, 3]})

    try:
        df.lint.unregister_check("nonexistent")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "not registered" in str(e)


def test_register_non_callable_raises_error():
    """Test that registering non-callable raises error."""
    df = pd.DataFrame({"value": [1, 2, 3]})

    try:
        df.lint.register_check("not a function")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "must be a callable" in str(e)


def test_custom_check_with_parameters():
    """Test custom check that accepts additional parameters."""
    df = pd.DataFrame({"price": [10, 20, 30, 1000]})

    def check_price_range(df, max_price=100):
        warnings = []
        if "price" in df.columns:
            over_max = df[df["price"] > max_price]
            if len(over_max) > 0:
                warnings.append(f"[Price] {len(over_max)} value(s) exceed max price of {max_price}")
        return warnings

    # Use lambda to bind parameters
    df.lint.register_check(lambda d: check_price_range(d, max_price=50))

    report = df.lint.report()
    assert "Price" in report
    assert "exceed max price of 50" in report


def test_custom_check_error_handling():
    """Test that custom check errors are caught and reported."""
    df = pd.DataFrame({"value": [1, 2, 3]})

    def broken_check(df):
        raise ValueError("Something went wrong")

    df.lint.register_check(broken_check)

    report = df.lint.report()
    assert "Custom Check Error" in report
    assert "broken_check" in report
    assert "Something went wrong" in report


def test_custom_check_returns_non_list():
    """Test that custom check returning non-list is handled."""
    df = pd.DataFrame({"value": [1, 2, 3]})

    def bad_check(df):
        return "not a list"

    df.lint.register_check(bad_check)

    report = df.lint.report()
    assert "Custom Check Error" in report
    assert "did not return a list" in report


def test_multiple_custom_checks():
    """Test registering and running multiple custom checks."""
    df = pd.DataFrame({"email": ["test@example.com"], "phone": ["123-456-7890"]})

    def check_email(df):
        return ["[Email] Custom email check"]

    def check_phone(df):
        return ["[Phone] Custom phone check"]

    df.lint.register_check(check_email)
    df.lint.register_check(check_phone)

    assert len(df.lint.list_custom_checks()) == 2

    report = df.lint.report()
    assert "Email" in report
    assert "Phone" in report


def test_custom_checks_work_with_built_in_checks():
    """Test that custom checks run alongside built-in checks."""
    df = pd.DataFrame({"value": [1, 2, None]})

    def custom_check(df):
        return ["[Custom] This is a custom warning"]

    df.lint.register_check(custom_check)

    report = df.lint.report()

    # Should have both built-in missing values check and custom check
    assert "Missing Values" in report
    assert "Custom" in report


def test_list_custom_checks_empty():
    """Test listing custom checks when none are registered."""
    df = pd.DataFrame({"value": [1, 2, 3]})

    assert df.lint.list_custom_checks() == []


def test_custom_check_with_empty_dataframe():
    """Test custom check with empty DataFrame."""
    df = pd.DataFrame()

    def custom_check(df):
        if df.empty:
            return []
        return ["[Custom] Warning"]

    df.lint.register_check(custom_check)

    report = df.lint.report()
    # Should not crash, report should indicate empty DataFrame
    assert "empty" in report.lower()
