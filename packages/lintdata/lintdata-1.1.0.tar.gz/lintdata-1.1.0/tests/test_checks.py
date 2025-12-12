"""
Tests for the individual check functions in checks.py
"""

from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from lintdata import checks


def test_check_missing_values_clean():
    """Test that a DataFrame with no missing values returns an empty list."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    warnings = checks.check_missing_values(df)
    assert warnings == []


def test_check_missing_values_one_column_missing():
    """Test detection and correct reporting for one missing value."""
    df = pd.DataFrame({"a": [1, 2, np.nan], "b": ["x", "y", "z"]})
    warnings = checks.check_missing_values(df)

    assert len(warnings) == 1
    # Check the content of the warning string
    assert "Column 'a'" in warnings[0]
    assert "1 missing" in warnings[0]
    assert "(33.3%)" in warnings[0]


def test_check_missing_values_multiple_columns_missing():
    """Test detection and reporting for multiple columns."""
    df = pd.DataFrame({"a": [1, np.nan, np.nan, 4], "b": ["w", "x", "y", "z"], "c": [np.nan, 2, 3, 4]})
    warnings = checks.check_missing_values(df)

    assert len(warnings) == 2
    # Check warning for 'a'
    assert "Column 'a'" in warnings[0]
    assert "2 missing" in warnings[0]
    assert "(50.0%)" in warnings[0]
    # Check warning for 'c'
    assert "Column 'c'" in warnings[1]
    assert "1 missing" in warnings[1]
    assert "(25.0%)" in warnings[1]


def test_check_missing_values_all_missing():
    """Test a column that is entirely missing values."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": [np.nan, np.nan, np.nan]})
    warnings = checks.check_missing_values(df)

    assert len(warnings) == 1
    assert "Column 'b'" in warnings[0]
    assert "3 missing" in warnings[0]
    assert "(100.0%)" in warnings[0]


# ==== Tests for check_duplicate_rows ====


def test_check_duplicate_rows_no_duplicates():
    """No duplicate rows present."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    warnings = checks.check_duplicate_rows(df)
    assert warnings == []


def test_check_duplicate_rows_detects_duplicates():
    """Core functionality: detects duplicate rows."""
    df = pd.DataFrame(
        {
            "id": [1, 2, 2],
            "name": ["Alice", "Bob", "Bob"],
        }
    )
    warnings = checks.check_duplicate_rows(df)
    assert len(warnings) == 1
    assert "1 duplicate row(s)" in warnings[0] or "1 duplicate" in warnings[0]
    assert "index: 2" in warnings[0]


def test_check_duplicate_rows_empty_dataframe():
    """Edge case: empty DataFrame should return no warnings."""
    df = pd.DataFrame(columns=["a", "b"])
    warnings = checks.check_duplicate_rows(df)
    assert warnings == []


def test_check_duplicate_rows_all_duplicates():
    """All rows are duplicates except the first one."""
    df = pd.DataFrame(
        {
            "id": [1, 1, 1],
            "name": ["Alice", "Alice", "Alice"],
        }
    )
    warnings = checks.check_duplicate_rows(df)
    assert len(warnings) == 1
    assert "2 duplicate row(s)" in warnings[0] or "2 duplicates" in warnings[0]
    assert "index: 1, 2" in warnings[0]


def test_check_duplicate_rows_multiple_duplicates_sets():
    """Multiple sets of duplicate rows."""
    df = pd.DataFrame(
        {
            "id": [1, 2, 2, 3, 3, 3],
            "name": ["Alice", "Bob", "Bob", "Charlie", "Charlie", "Charlie"],
        }
    )
    warnings = checks.check_duplicate_rows(df)
    assert len(warnings) == 1
    assert "3 duplicate row(s)" in warnings[0] or "3 duplicates" in warnings[0]
    assert "index: 2, 4, 5" in warnings[0]


# ==== Mixed Type Tests ====


def test_check_mixed_types_no_mixed_types():
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    warnings = checks.check_mixed_types(df)
    assert warnings == []


def test_check_mixed_types_detects_mixed():
    df = pd.DataFrame(
        {
            "price": [10, "20", 30],
        }
    )
    warnings = checks.check_mixed_types(df)
    assert len(warnings) == 1
    assert "Column 'price'" in warnings[0]
    assert "int" in warnings[0] or "int64" in warnings[0]
    assert "str" in warnings[0] or "object" in warnings[0]


def test_check_mixed_types_empty_dataframe():
    df = pd.DataFrame()
    warnings = checks.check_mixed_types(df)
    assert warnings == []


def test_check_mixed_types_with_nan():
    df = pd.DataFrame(
        {
            "value": [1, 2, np.nan, "text"],
        }
    )
    warnings = checks.check_mixed_types(df)
    assert len(warnings) == 1
    assert "Column 'value'" in warnings[0]
    assert "int" in warnings[0] or "int64" in warnings[0]
    assert "str" in warnings[0] or "object" in warnings[0]


def test_check_mixed_types_multiple_columns():
    df = pd.DataFrame(
        {
            "col1": [1, 2, 3],
            "col2": [1.0, "2.0", 3.0],
            "col3": ["a", "b", "c"],
            "col4": [True, False, "True"],
        }
    )
    warnings = checks.check_mixed_types(df)
    assert len(warnings) == 2
    assert any("Column 'col2'" in warning for warning in warnings)
    assert any("Column 'col4'" in warning for warning in warnings)


# ==== Whitespace Tests ====


def test_check_whitespace_no_whitespace():
    df = pd.DataFrame({"a": ["x", "y", "z"], "b": ["foo", "bar", "baz"]})
    warnings = checks.check_whitespace(df)
    assert warnings == []


def test_check_whitespace_detects_leading():
    df = pd.DataFrame({"a": [" x", "y", "z"]})
    warnings = checks.check_whitespace(df)
    assert len(warnings) == 1
    assert "Column 'a'" in warnings[0]
    assert "1 value(s)" in warnings[0]


def test_check_whitespace_detects_trailing():
    df = pd.DataFrame({"a": ["x ", "y", "z"]})
    warnings = checks.check_whitespace(df)
    assert len(warnings) == 1
    assert "Column 'a'" in warnings[0]
    assert "1 value(s)" in warnings[0]


def test_check_whitespace_detects_both():
    df = pd.DataFrame({"a": [" x ", "y", "z"]})
    warnings = checks.check_whitespace(df)
    assert len(warnings) == 1
    assert "Column 'a'" in warnings[0]
    assert "1 value(s)" in warnings[0]


def test_check_whitespace_multiple_columns():
    df = pd.DataFrame(
        {
            "a": [" x", "y", "z"],
            "b": ["foo", " bar", "baz "],
        }
    )
    warnings = checks.check_whitespace(df)
    assert len(warnings) == 2
    assert any("Column 'a'" in warning for warning in warnings)
    assert any("Column 'b'" in warning for warning in warnings)


def test_check_whitespace_empty_dataframe():
    df = pd.DataFrame()
    warnings = checks.check_whitespace(df)
    assert warnings == []


def test_check_whitespace_non_string_column():
    df = pd.DataFrame({"a": [1, 2, 3]})
    warnings = checks.check_whitespace(df)
    assert warnings == []


def test_check_whitespace_nan_values():
    df = pd.DataFrame({"a": [" x", np.nan, "z "]})
    warnings = checks.check_whitespace(df)
    assert len(warnings) == 1
    assert "Column 'a'" in warnings[0]
    assert "2 value(s)" in warnings[0]


# === Check Constant Columns Tests ====


def test_check_constant_columns_no_constants():
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    warnings = checks.check_constant_columns(df)
    assert warnings == []


def test_check_constant_columns_detects_constants():
    df = pd.DataFrame({"a": ["x", "x", "x"]})
    warnings = checks.check_constant_columns(df)
    assert len(warnings) == 1
    assert "Column 'a'" in warnings[0]
    assert "only one unique value: 'x'" in warnings[0]


def test_check_constant_columns_numeric_constants():
    df = pd.DataFrame({"a": [3.14, 3.14, 3.14], "b": [1, 2, 3]})
    warnings = checks.check_constant_columns(df)
    assert len(warnings) == 1
    assert "Column 'a'" in warnings[0]
    assert "only one unique value: 3.14" in warnings[0]


def test_check_constant_columns_empty_dataframe():
    df = pd.DataFrame()
    warnings = checks.check_constant_columns(df)
    assert warnings == []


def test_check_constant_columns_single_row():
    df = pd.DataFrame({"a": [42]})
    warnings = checks.check_constant_columns(df)
    assert len(warnings) == 1


def test_check_constant_columns_with_nan():
    df = pd.DataFrame({"a": [np.nan, np.nan, np.nan]})
    warnings = checks.check_constant_columns(df)
    assert len(warnings) == 1
    assert "Column 'a'" in warnings[0]


def test_check_constant_columns_mixed_with_nan_and_constant():
    df = pd.DataFrame({"a": [5, 5, np.nan, 5]})
    warnings = checks.check_constant_columns(df)
    assert len(warnings) == 1
    assert "Column 'a'" in warnings[0]
    assert "only one unique value: 5" in warnings[0]


def test_check_constant_columns_multiple_constants():
    df = pd.DataFrame({"a": ["constant", "constant", "constant"], "b": [42, 42, 42], "c": [1, 2, 3]})
    warnings = checks.check_constant_columns(df)
    assert len(warnings) == 2
    assert any("Column 'a'" in warning for warning in warnings)
    assert any("Column 'b'" in warning for warning in warnings)


def test_check_constant_columns_boolean_constant():
    df = pd.DataFrame({"a": [True, True, True, True]})
    warnings = checks.check_constant_columns(df)
    assert len(warnings) == 1
    assert "Column 'a'" in warnings[0]
    assert "only one unique value: True" in warnings[0]


# ==== Unique Columns Test ====


def test_check_unique_columns_detects_uniques():
    df = pd.DataFrame({"a": [1, 2, 3, 4, 5]})
    warnings = checks.check_unique_columns(df)
    assert len(warnings) == 1
    assert "Column 'a'" in warnings[0]
    assert "100.0% unique" in warnings[0]


def test_check_unique_columns_custom_threshold():
    df = pd.DataFrame(
        {
            "a": [1, 2, 3, 4, 5, 5, 5, 5, 5, 5],
            "b": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
        }
    )
    warnings = checks.check_unique_columns(df)
    assert len(warnings) == 1
    assert "Column 'b'" in warnings[0]

    warnings_low = checks.check_unique_columns(df, threshold=0.4)
    assert len(warnings_low) == 2


def test_check_unique_columns_empty_dataframe():
    df = pd.DataFrame()
    warnings = checks.check_unique_columns(df)
    assert warnings == []


def test_check_unique_columns_with_nan():
    df = pd.DataFrame({"a": [1, 2, 3, np.nan, np.nan]})
    warnings = checks.check_unique_columns(df)
    assert len(warnings) == 1
    assert "Column 'a'" in warnings[0]
    assert "100.0% unique" in warnings[0]


def test_check_unique_columns_single_row():
    df = pd.DataFrame({"a": [42]})
    warnings = checks.check_unique_columns(df)
    assert len(warnings) == 1
    assert "Column 'a'" in warnings[0]


def test_check_unique_columns_all_nan():
    df = pd.DataFrame({"a": [np.nan, np.nan, np.nan], "b": [1, 2, 3]})
    warnings = checks.check_unique_columns(df)
    assert len(warnings) == 1
    assert "Column 'b'" in warnings[0]


def test_check_unique_columns_multiple_unique_columns():
    df = pd.DataFrame({"a": [1, 2, 3, 4], "b": ["x", "y", "z", "w"], "c": [1, 1, 1, 1]})
    warnings = checks.check_unique_columns(df)
    assert len(warnings) == 2
    assert any("Column 'a'" in warning for warning in warnings)
    assert any("Column 'b'" in warning for warning in warnings)


# ==== Outliers Tests ====


def test_check_outliers_no_outliers():
    df = pd.DataFrame({"a": [10, 12, 11, 13, 12], "b": [20, 22, 21, 19, 20]})
    warnings = checks.check_outliers(df)
    assert warnings == []


def test_check_outliers_with_outliers():
    df = pd.DataFrame({"a": [10, 12, 11, 13, 100], "b": [20, 22, 21, 19, 20]})
    warnings = checks.check_outliers(df)
    assert len(warnings) == 1
    assert "Column 'a'" in warnings[0]
    assert "potential outlier(s)" in warnings[0]


def test_check_outliers_empty_dataframe():
    df = pd.DataFrame()
    warnings = checks.check_outliers(df)
    assert warnings == []


def test_check_outliers_custom_threshold():
    df = pd.DataFrame({"a": [10, 15, 20, 25, 30, 35, 150], "b": [10, 20, 30, 40, 50, 80, 110]})
    warnings = checks.check_outliers(df)
    assert len(warnings) == 1
    assert "Column 'a'" in warnings[0]
    warnings_low = checks.check_outliers(df, threshold=0.9)
    assert len(warnings_low) == 2
    assert "Column 'a'" in warnings_low[0]
    assert "potential outlier(s)" in warnings_low[0]
    assert "Column 'b'" in warnings_low[1]
    assert "potential outlier(s)" in warnings_low[1]


# ==== Missing Patterns Tests ====


def test_check_missing_patterns_no_pattern():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    warnings = checks.check_missing_patterns(df)
    assert warnings == []


def test_check_missing_patterns_detects_pattern():
    df = pd.DataFrame(
        {
            "income": [50000, np.nan, 60000, np.nan],
            "job": ["Engineer", np.nan, "Doctor", np.nan],
            "age": [25, 26, 27, 28],
        }
    )

    warnings = checks.check_missing_patterns(df)
    assert len(warnings) == 1
    assert "income" in warnings[0]
    assert "job" in warnings[0]
    assert "identical missing rows" in warnings[0].lower()


def test_check_missing_patterns_empty_dataframe():
    df = pd.DataFrame()
    warnings = checks.check_missing_patterns(df)
    assert warnings == []


# ==== Case Consistency Tests ====


def test_check_case_consistency_no_issues():
    df = pd.DataFrame({"a": ["Apple", "Banana", "Cherry"], "b": ["Dog", "Elephant", "Frog"]})
    warnings = checks.check_case_consistency(df)
    assert warnings == []


def test_check_case_consistency_detects_issues():
    df = pd.DataFrame({"category": ["apple", "APPLE", "Apple", "Banana"]})
    warnings = checks.check_case_consistency(df)
    assert len(warnings) == 1
    assert "category" in warnings[0]
    assert "mixed case" in warnings[0].lower()


def test_check_case_consistency_empty_dataframe():
    df = pd.DataFrame()
    warnings = checks.check_case_consistency(df)
    assert warnings == []


def test_check_case_consistency_multiple_columns():
    df = pd.DataFrame({"fruit": ["apple", "APPLE", "Apple", "Banana"], "animal": ["dog", "Dog", "DOG", "cat"]})
    warnings = checks.check_case_consistency(df)
    assert len(warnings) == 2
    assert any("fruit" in warning for warning in warnings)
    assert any("animal" in warning for warning in warnings)


# ==== Cardinality Tests ====


def test_check_cardinality_no_issues():
    df = pd.DataFrame({"a": [1, 2, 3, 4, 5], "b": ["x", "y", "z", "w", "v"]})
    warnings = checks.check_cardinality(df)
    assert warnings == []


def test_check_cardinality_detects_high_cardinality():
    df = pd.DataFrame({"a": list(range(100)), "b": ["x", "y", "z", "w", "v"] * 20})
    warnings = checks.check_cardinality(df)
    assert len(warnings) == 1
    assert "Column 'a'" in warnings[0]
    assert "High Cardinality" in warnings[0]
    assert "100.0% unique" in warnings[0]
    assert "100 unique values" in warnings[0]


def test_check_cardinality_low_cardinality():
    df = pd.DataFrame({"status": ["active"] * 100})
    warnings = checks.check_cardinality(df)
    assert len(warnings) == 1
    assert "Low Cardinality" in warnings[0]
    assert "1 unique value" in warnings[0]
    assert "status" in warnings[0]


def test_check_cardinality_empty_dataframe():
    df = pd.DataFrame()
    warnings = checks.check_cardinality(df)
    assert warnings == []


def test_check_cardinality_multiple_columns():
    df = pd.DataFrame({"high_card": list(range(100)), "low_card": ["A"] * 100, "medium_card": ["A", "B"] * 50})
    warnings = checks.check_cardinality(df)
    assert len(warnings) == 2
    assert any("high_card" in warning for warning in warnings if "High Cardinality" in warning)
    assert any("low_card" in warning for warning in warnings if "Low Cardinality" in warning)


def test_check_cardinality_custom_thresholds():
    df = pd.DataFrame({"a": list(range(30)), "b": ["x", "y", "z"] * 10})
    warnings = checks.check_cardinality(df, high_threshold=25, low_threshold=2)
    assert len(warnings) == 1
    assert "Column 'a'" in warnings[0]
    assert "High Cardinality" in warnings[0]

    warnings_low = checks.check_cardinality(df, high_threshold=40, low_threshold=4)
    assert len(warnings_low) == 1
    assert "Column 'b'" in warnings_low[0]
    assert "Low Cardinality" in warnings_low[0]


def test_check_cardinality_all_nan_values():
    df = pd.DataFrame({"a": [np.nan] * 10})
    warnings = checks.check_cardinality(df)
    assert warnings == []


# ==== Skewness Tests ====


def test_check_skewness_no_skewness():
    np.random.seed(42)
    df = pd.DataFrame({"a": np.random.normal(50, 10, 1000)})
    warnings = checks.check_skewness(df)
    assert warnings == []


def test_check_skewness_detects_right_skewness():
    df = pd.DataFrame({"a": [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 100]})
    warnings = checks.check_skewness(df)
    assert len(warnings) == 1
    assert "Column 'a'" in warnings[0]
    assert "right-skewed" in warnings[0].lower()


def test_check_skewness_detects_left_skewness():
    df = pd.DataFrame({"a": [100, 95, 90, 85, 80, 75, 70, 10]})
    warnings = checks.check_skewness(df)
    assert len(warnings) == 1
    assert "Column 'a'" in warnings[0]
    assert "left-skewed" in warnings[0].lower()


def test_check_skewness_empty_dataframe():
    df = pd.DataFrame()
    warnings = checks.check_skewness(df)
    assert warnings == []


def test_check_skewness_with_nan():
    df = pd.DataFrame({"a": [1, 2, 3, 4, 5, np.nan, np.nan, 100]})
    warnings = checks.check_skewness(df)
    assert len(warnings) == 1
    assert "Column 'a'" in warnings[0]
    assert "right-skewed" in warnings[0].lower()


def test_check_skewness_with_custom_thresholds():
    df = pd.DataFrame({"a": [1, 2, 3, 4, 5, 6, 7, 8, 9, 20]})

    warnings_high = checks.check_skewness(df, threshold=2.0)
    assert warnings_high == []

    warnings_low = checks.check_skewness(df, threshold=0.5)
    assert len(warnings_low) == 1
    assert "Column 'a'" in warnings_low[0]
    assert "right-skewed" in warnings_low[0].lower()


# ==== Duplicate columns tests ====


def test_check_duplicate_columns_no_duplicates():
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    warnings = checks.check_duplicate_columns(df)
    assert warnings == []


def test_check_duplicate_columns_detects_duplicates():
    df = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "name_dup": ["Alice", "Bob", "Charlie"],
        }
    )
    warnings = checks.check_duplicate_columns(df)
    assert len(warnings) == 1
    assert "Columns 'name' and 'name_dup'" in warnings[0]
    assert "are identical" in warnings[0]


def test_check_duplicate_columns_empty_dataframe():
    df = pd.DataFrame()
    warnings = checks.check_duplicate_columns(df)
    assert warnings == []


def test_check_duplicate_columns_multiple_duplicates():
    df = pd.DataFrame(
        {
            "col1": [1, 2, 3],
            "col2": ["a", "b", "c"],
            "col1_dup": [1, 2, 3],
            "col2_dup": ["a", "b", "c"],
        }
    )
    warnings = checks.check_duplicate_columns(df)
    assert len(warnings) == 2
    assert any("Columns 'col1' and 'col1_dup'" in warning for warning in warnings)
    assert any("Columns 'col2' and 'col2_dup'" in warning for warning in warnings)


def test_check_duplicate_columns_duplicates_with_different_dtypes():
    df = pd.DataFrame(
        {
            "col1": [1, 2, 3],
            "col2": [1.0, 2.0, 3.0],
        }
    )
    warnings = checks.check_duplicate_columns(df)
    assert warnings == []


# ==== Data Type Consistency Tests ====


def test_check_data_type_consistency_no_issues():
    df = pd.DataFrame(
        {
            "age": [25, 30, 22],
            "salary": [50000.0, 60000.0, 55000.0],
        }
    )
    warnings = checks.check_data_type_consistency(df)
    assert warnings == []


def test_check_data_type_consistency_detects_numeric_issues():
    df = pd.DataFrame(
        {
            "price": [10, "20", 30],
        }
    )
    warnings = checks.check_data_type_consistency(df)
    assert len(warnings) == 1
    assert "Column 'price'" in warnings[0]
    assert "numeric type" in warnings[0].lower()


def test_check_data_type_consistency_detects_datetime_issues():
    df = pd.DataFrame(
        {
            "start_date": ["2020-01-01", "2020-02-01", "not_a_date"],
        }
    )
    warnings = checks.check_data_type_consistency(df)
    assert len(warnings) == 1
    assert "Column 'start_date'" in warnings[0]
    assert "datetime type" in warnings[0].lower()


def test_check_data_type_consistency_detects_boolean_issues():
    df = pd.DataFrame(
        {
            "is_active": ["yes", "no", "no", "yes"],
        }
    )
    warnings = checks.check_data_type_consistency(df)
    assert len(warnings) == 1
    assert "Column 'is_active'" in warnings[0]
    assert "boolean type" in warnings[0].lower()


def test_check_data_type_consistency_empty_dataframe():
    df = pd.DataFrame()
    warnings = checks.check_data_type_consistency(df)
    assert warnings == []


def test_check_data_type_consistency_multiple_issues():
    df = pd.DataFrame(
        {
            "price": [10, "20", 30],
            "start_date": ["2020-01-01", "2020-02-01", "not_a_date"],
            "is_active": ["yes", "no", "no"],
        }
    )
    warnings = checks.check_data_type_consistency(df)
    assert len(warnings) == 3
    assert any("Column 'price'" in warning for warning in warnings)
    assert any("Column 'start_date'" in warning for warning in warnings)
    assert any("Column 'is_active'" in warning for warning in warnings)


def test_check_data_type_consistency_with_nan():
    df = pd.DataFrame(
        {
            "price": [10, np.nan, 30],
            "start_date": ["2020-01-01", np.nan, "not_a_date"],
            "is_active": [True, False, np.nan],
        }
    )
    warnings = checks.check_data_type_consistency(df)
    assert len(warnings) == 2
    assert any("Column 'start_date'" in warning for warning in warnings)
    assert any("Column 'is_active'" in warning for warning in warnings)


# ==== Negative Value Check ====


def test_check_negative_values_no_negatives():
    df = pd.DataFrame({"age": [25, 30, 35], "price": [10.0, 20.0, 30.0]})
    warnings = checks.check_negative_values(df)
    assert warnings == []


def test_check_negative_values_detects_negatives():
    df = pd.DataFrame({"age": [25, -5, 30], "balance": [100, 200, 300]})
    warnings = checks.check_negative_values(df)
    assert len(warnings) == 1
    assert "Column 'age'" in warnings[0]
    assert "1 negative value(s)" in warnings[0]


def test_check_negative_values_specific_columns():
    df = pd.DataFrame({"age": [25, -5, 30], "balance": [100, -50, 200]})
    warnings = checks.check_negative_values(df, columns=["age"])
    assert len(warnings) == 1
    assert "Column 'age'" in warnings[0]
    assert "balance" not in str(warnings)


def test_check_negative_values_empty_dataframe():
    df = pd.DataFrame()
    warnings = checks.check_negative_values(df)
    assert warnings == []


def test_check_negative_values_with_nan():
    df = pd.DataFrame({"age": [25, -5, np.nan, 30]})
    warnings = checks.check_negative_values(df)
    assert len(warnings) == 1
    assert "Column 'age'" in warnings[0]
    assert "1 negative value(s)" in warnings[0]


def test_check_negative_values_multiple_columns():
    df = pd.DataFrame({"age": [25, -5, 30], "balance": [100, -50, 200], "score": [-10, -20, -30]})
    warnings = checks.check_negative_values(df)
    assert len(warnings) == 3
    assert any("age" in warning for warning in warnings)
    assert any("balance" in warning for warning in warnings)
    assert any("score" in warning for warning in warnings)


def test_check_negative_values_non_numeric_columns():
    df = pd.DataFrame({"name": ["Alice", "Bob", "Charlie"], "age": [25, 30, 35]})
    warnings = checks.check_negative_values(df)
    assert warnings == []


# ==== Rare Categories Tests ====


def test_check_rare_categories_no_rare():
    df = pd.DataFrame({"category": ["A", "B", "C"] * 30})
    warnings = checks.check_rare_categories(df)
    assert warnings == []


def test_check_rare_categories_detects_rare():
    df = pd.DataFrame({"category": ["A"] * 98 + ["B", "C"]})
    warnings = checks.check_rare_categories(df, threshold=0.02)
    assert len(warnings) == 1
    assert "Column 'category'" in warnings[0]
    assert "2 categories" in warnings[0]
    assert "<2.0%" in warnings[0]


def test_check_rare_categories_empty_dataframe():
    df = pd.DataFrame()
    warnings = checks.check_rare_categories(df)
    assert warnings == []


def test_check_rare_categories_custom_threshold():
    df = pd.DataFrame({"category": ["A"] * 90 + ["B"] * 5 + ["C"] * 5})
    warnings_1 = checks.check_rare_categories(df, threshold=0.01)
    assert warnings_1 == []

    warnings_2 = checks.check_rare_categories(df, threshold=0.06)
    assert len(warnings_2) == 1
    assert "2 categories" in warnings_2[0]


def test_check_rare_categories_with_nan():
    df = pd.DataFrame({"category": ["A"] * 95 + ["B"] * 3 + [np.nan, np.nan]})
    warnings = checks.check_rare_categories(df, threshold=0.05)
    assert len(warnings) == 1
    assert "1 categories" in warnings[0]


def test_check_rare_categories_multiple_columns():
    df = pd.DataFrame({"cat1": ["A"] * 98 + ["B", "C"], "cat2": ["X"] * 99 + ["Y"]})
    warnings = checks.check_rare_categories(df, threshold=0.015)
    assert len(warnings) == 2
    assert any("cat1" in warning for warning in warnings)
    assert any("cat2" in warning for warning in warnings)


def test_check_rare_categories_invalid_threshold():
    df = pd.DataFrame({"category": ["A", "B", "C"]})
    try:
        checks.check_rare_categories(df, threshold=1.5)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


# ==== Date Format Consistency Tests ====


def test_check_date_format_consistency_no_dates():
    df = pd.DataFrame({"name": ["Alice", "Bob", "Charlie"]})
    warnings = checks.check_date_format_consistency(df)
    assert warnings == []


def test_check_date_format_consistency_consistent_format():
    df = pd.DataFrame({"date": ["2020-01-01", "2020-02-01", "2020-03-01"]})
    warnings = checks.check_date_format_consistency(df)
    assert warnings == []


def test_check_date_format_consistency_detects_mixed():
    df = pd.DataFrame({"date": ["2020-01-01", "01/02/2020", "2020-03-01"]})
    warnings = checks.check_date_format_consistency(df)
    assert len(warnings) == 1
    assert "Column 'date'" in warnings[0]
    assert "inconsistent date formats" in warnings[0]


def test_check_date_format_consistency_empty_dataframe():
    df = pd.DataFrame()
    warnings = checks.check_date_format_consistency(df)
    assert warnings == []


def test_check_date_format_consistency_no_date_column_names():
    df = pd.DataFrame({"value": ["2020-01-01", "01/02/2020", "2020-03-01"]})
    warnings = checks.check_date_format_consistency(df)
    assert warnings == []


def test_check_date_format_consistency_with_nan():
    df = pd.DataFrame({"date": ["2020-01-01", np.nan, "01/02/2020", "2020-03-01"]})
    warnings = checks.check_date_format_consistency(df)
    assert len(warnings) == 1
    assert "Column 'date'" in warnings[0]


def test_check_date_format_consistency_multiple_date_columns():
    df = pd.DataFrame(
        {"start_date": ["2020-01-01", "01/02/2020"], "end_date": ["2020-03-01", "2020-04-01"], "value": [1, 2]}
    )
    warnings = checks.check_date_format_consistency(df)
    assert len(warnings) == 1
    assert "start_date" in warnings[0]


def test_check_date_format_consistency_with_time():
    df = pd.DataFrame({"timestamp": ["2020-01-01", "01/02/2020 10:30", "2020-03-01"]})
    warnings = checks.check_date_format_consistency(df)
    assert len(warnings) == 1
    assert "timestamp" in warnings[0]


# ==== String Length Outliers Tests ====


def test_check_string_length_outliers_no_outliers():
    df = pd.DataFrame({"name": ["Alice", "Bob", "Charlie", "David"]})
    warnings = checks.check_string_length_outliers(df)
    assert warnings == []


def test_check_string_length_outliers_detects_outliers():
    df = pd.DataFrame({"email": ["a@b.com", "test@example.com", "x" * 100 + "@example.com"]})
    warnings = checks.check_string_length_outliers(df)
    assert len(warnings) == 1
    assert "Column 'email'" in warnings[0]
    assert "unusual length" in warnings[0]


def test_check_string_length_outliers_empty_dataframe():
    df = pd.DataFrame()
    warnings = checks.check_string_length_outliers(df)
    assert warnings == []


def test_check_string_length_outliers_too_few_values():
    df = pd.DataFrame({"name": ["A", "B"]})
    warnings = checks.check_string_length_outliers(df)
    assert warnings == []


def test_check_string_length_outliers_custom_threshold():
    df = pd.DataFrame({"name": ["Alice", "Bob", "Charlie", "x" * 20]})
    warnings_high = checks.check_string_length_outliers(df, threshold=5.0)
    assert warnings_high == []

    warnings_low = checks.check_string_length_outliers(df, threshold=2.0)
    assert len(warnings_low) == 1


def test_check_string_length_outliers_with_nan():
    df = pd.DataFrame({"email": ["a@b.com", np.nan, "test@example.com", "x" * 100 + "@example.com"]})
    warnings = checks.check_string_length_outliers(df)
    assert len(warnings) == 1
    assert "Column 'email'" in warnings[0]


def test_check_string_length_outliers_constant_length():
    df = pd.DataFrame({"code": ["ABC", "DEF", "GHI", "JKL"]})
    warnings = checks.check_string_length_outliers(df)
    assert warnings == []


def test_check_string_length_outliers_multiple_columns():
    df = pd.DataFrame(
        {"email": ["a@b.com", "test@example.com", "x" * 100 + "@example.com"], "name": ["A", "Bob", "x" * 50]}
    )
    warnings = checks.check_string_length_outliers(df)
    assert len(warnings) == 2
    assert any("email" in warning for warning in warnings)
    assert any("name" in warning for warning in warnings)


def test_check_string_length_outliers_invalid_threshold():
    df = pd.DataFrame({"name": ["Alice", "Bob", "Charlie"]})
    try:
        checks.check_string_length_outliers(df, threshold=-1.0)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


# ==== Zero Inflation Tests ====


def test_check_zero_inflation_no_zeros():
    """No zero inflation in clean data."""
    df = pd.DataFrame({"sales": [100, 200, 300, 400]})
    warnings = checks.check_zero_inflation(df)
    assert warnings == []


def test_check_zero_inflation_detects_inflation():
    """Detects columns with excessive zeros."""
    df = pd.DataFrame({"purchases": [0, 0, 0, 0, 0, 100, 200]})
    warnings = checks.check_zero_inflation(df, threshold=0.5)
    assert len(warnings) == 1
    assert "Column 'purchases'" in warnings[0]
    assert "71.4%" in warnings[0] or "71%" in warnings[0]
    assert "zero" in warnings[0].lower()


def test_check_zero_inflation_custom_threshold():
    """Custom threshold works correctly."""
    df = pd.DataFrame({"col1": [0, 0, 0, 1, 2, 3, 4, 5, 6, 7]})

    # 30% zeros - should not trigger with 0.5 threshold
    warnings_high = checks.check_zero_inflation(df, threshold=0.5)
    assert warnings_high == []

    # Should trigger with 0.2 threshold
    warnings_low = checks.check_zero_inflation(df, threshold=0.2)
    assert len(warnings_low) == 1
    assert "Column 'col1'" in warnings_low[0]


def test_check_zero_inflation_empty_dataframe():
    """Empty DataFrame returns no warnings."""
    df = pd.DataFrame()
    warnings = checks.check_zero_inflation(df)
    assert warnings == []


def test_check_zero_inflation_with_nan():
    """NaN values are ignored in calculation."""
    df = pd.DataFrame({"values": [0, 0, 0, np.nan, np.nan, 1, 2]})
    warnings = checks.check_zero_inflation(df, threshold=0.5)
    assert len(warnings) == 1
    assert "60.0%" in warnings[0] or "60%" in warnings[0]  # 3 zeros out of 5 non-null


def test_check_zero_inflation_non_numeric():
    """Non-numeric columns are ignored."""
    df = pd.DataFrame({"text": ["zero", "zero", "one"]})
    warnings = checks.check_zero_inflation(df)
    assert warnings == []


def test_check_zero_inflation_multiple_columns():
    """Multiple columns with zero inflation."""
    df = pd.DataFrame({"col1": [0, 0, 0, 0, 0, 1], "col2": [1, 2, 3, 4, 5, 6], "col3": [0, 0, 0, 0, 1, 2]})
    warnings = checks.check_zero_inflation(df, threshold=0.5)
    assert len(warnings) == 2
    assert any("col1" in w for w in warnings)
    assert any("col3" in w for w in warnings)


def test_check_zero_inflation_invalid_threshold():
    """Invalid threshold raises ValueError."""
    df = pd.DataFrame({"col": [0, 1, 2]})

    try:
        checks.check_zero_inflation(df, threshold=1.5)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "between 0 and 1" in str(e).lower()


# ==== Future Dates Tests ====


def test_check_future_dates_no_future():
    """No future dates in clean data."""
    past_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    df = pd.DataFrame({"birth_date": pd.to_datetime([past_date, "1990-01-01", "1985-06-15"])})
    warnings = checks.check_future_dates(df)
    assert warnings == []


def test_check_future_dates_detects_future():
    """Detects future dates."""
    future_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    df = pd.DataFrame({"event_date": pd.to_datetime(["1990-01-01", future_date, "1985-06-15"])})
    warnings = checks.check_future_dates(df)
    assert len(warnings) == 1
    assert "Column 'event_date'" in warnings[0]
    assert "1 date(s) in the future" in warnings[0]


def test_check_future_dates_string_dates():
    """Handles string date columns."""
    future_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    df = pd.DataFrame({"date": ["1990-01-01", future_date, "1985-06-15"]})
    warnings = checks.check_future_dates(df)
    assert len(warnings) == 1
    assert "Column 'date'" in warnings[0]


def test_check_future_dates_specific_columns():
    """Only checks specified columns."""
    future_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    df = pd.DataFrame(
        {"date1": pd.to_datetime(["1990-01-01", future_date]), "date2": pd.to_datetime(["2000-01-01", future_date])}
    )
    warnings = checks.check_future_dates(df, columns=["date1"])
    assert len(warnings) == 1
    assert "date1" in warnings[0]
    assert "date2" not in str(warnings)


def test_check_future_dates_custom_reference():
    """Custom reference date works correctly."""
    df = pd.DataFrame({"date": pd.to_datetime(["2020-01-01", "2022-01-01", "2025-01-01"])})
    warnings = checks.check_future_dates(df, reference_date="2021-01-01")
    assert len(warnings) == 1
    assert "2 date(s) in the future" in warnings[0]


def test_check_future_dates_empty_dataframe():
    """Empty DataFrame returns no warnings."""
    df = pd.DataFrame()
    warnings = checks.check_future_dates(df)
    assert warnings == []


def test_check_future_dates_with_nan():
    """NaN values are ignored."""
    future_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    df = pd.DataFrame({"date": pd.to_datetime(["1990-01-01", np.nan, future_date])})  # type: ignore
    warnings = checks.check_future_dates(df)
    assert len(warnings) == 1
    assert "1 date(s) in the future" in warnings[0]


def test_check_future_dates_invalid_reference():
    """Invalid reference date raises ValueError."""
    df = pd.DataFrame({"date": pd.to_datetime(["1990-01-01"])})

    try:
        checks.check_future_dates(df, reference_date="not-a-date")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "ISO format" in str(e)


def test_check_future_dates_multiple_columns():
    """Multiple columns with future dates."""
    future_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    df = pd.DataFrame(
        {
            "start_date": pd.to_datetime(["1990-01-01", future_date]),
            "end_date": pd.to_datetime(["2000-01-01", future_date]),
            "value": [1, 2],
        }
    )
    warnings = checks.check_future_dates(df)
    assert len(warnings) == 2
    assert any("start_date" in w for w in warnings)
    assert any("end_date" in w for w in warnings)


# ==== Special Characters Tests ====


def test_check_special_characters_clean_data():
    """No special characters in clean data."""
    df = pd.DataFrame({"name": ["Alice", "Bob", "Charlie"]})
    warnings = checks.check_special_characters(df)
    assert warnings == []


def test_check_special_characters_detects_encoding_issues():
    """Detects encoding artifacts."""
    df = pd.DataFrame({"text": ["Normal text", "Bobâ„¢", "Aliceâ€¢"]})
    warnings = checks.check_special_characters(df)
    assert len(warnings) == 1
    assert "Column 'text'" in warnings[0]
    assert "special characters" in warnings[0].lower()


def test_check_special_characters_non_ascii():
    """Detects non-ASCII characters."""
    df = pd.DataFrame({"name": ["Alice", "Café", "Naïve", "José"]})
    warnings = checks.check_special_characters(df, threshold=0.1)
    assert len(warnings) == 1
    assert "Column 'name'" in warnings[0]


def test_check_special_characters_custom_threshold():
    """Custom threshold works correctly."""
    df = pd.DataFrame({"text": ["Normal"] * 9 + ["Specialâ„¢"]})

    # 10% special - should not trigger with 0.2 threshold
    warnings_high = checks.check_special_characters(df, threshold=0.2)
    assert warnings_high == []

    # Should trigger with 0.05 threshold
    warnings_low = checks.check_special_characters(df, threshold=0.05)
    assert len(warnings_low) == 1


def test_check_special_characters_empty_dataframe():
    """Empty DataFrame returns no warnings."""
    df = pd.DataFrame()
    warnings = checks.check_special_characters(df)
    assert warnings == []


def test_check_special_characters_numeric_columns():
    """Numeric columns are ignored."""
    df = pd.DataFrame({"numbers": [1, 2, 3, 4]})
    warnings = checks.check_special_characters(df)
    assert warnings == []


def test_check_special_characters_with_nan():
    """NaN values are ignored."""
    df = pd.DataFrame({"text": ["Normal", "Bobâ„¢", np.nan, "Alice"]})
    warnings = checks.check_special_characters(df, threshold=0.2)
    assert len(warnings) == 1
    assert "33.3%" in warnings[0] or "33%" in warnings[0]  # 1 out of 3 non-null


def test_check_special_characters_control_chars():
    """Detects control characters."""
    df = pd.DataFrame({"text": ["Normal", "With\x00null", "With\x1fcontrol"]})
    warnings = checks.check_special_characters(df, threshold=0.1)
    assert len(warnings) == 1
    assert "Column 'text'" in warnings[0]


def test_check_special_characters_multiple_columns():
    """Multiple columns with special characters."""
    df = pd.DataFrame(
        {
            "col1": ["Normal", "Specialâ„¢", "Moreâ€¢"],
            "col2": ["Clean", "Text", "Here"],
            "col3": ["Café", "Naïve", "José"],
        }
    )
    warnings = checks.check_special_characters(df, threshold=0.1)
    assert len(warnings) == 2
    assert any("col1" in w for w in warnings)
    assert any("col3" in w for w in warnings)


def test_check_special_characters_invalid_threshold():
    """Invalid threshold raises ValueError."""
    df = pd.DataFrame({"text": ["Normal"]})

    try:
        checks.check_special_characters(df, threshold=1.5)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "between 0 and 1" in str(e).lower()


# ==== Date Range Anomalies Tests ====


def test_check_date_range_anomalies_normal_range():
    """Dates within reasonable range should pass."""
    df = pd.DataFrame({"order_date": pd.to_datetime(["2020-01-01", "2020-06-01", "2020-12-31"])})
    warnings = checks.check_date_range_anomalies(df)
    assert warnings == []


def test_check_date_range_anomalies_detects_wide_range():
    """Detects suspiciously wide date ranges."""
    df = pd.DataFrame({"birth_date": pd.to_datetime(["1900-01-01", "2020-01-01", "2099-12-31"])})
    warnings = checks.check_date_range_anomalies(df)
    assert len(warnings) == 1
    assert "Column 'birth_date'" in warnings[0]
    assert "wide range" in warnings[0].lower() or "anomalies" in warnings[0].lower()


def test_check_date_range_anomalies_string_dates():
    """Handles string date columns."""
    df = pd.DataFrame({"date": ["1970-01-01", "2020-01-01", "2099-01-01"]})
    warnings = checks.check_date_range_anomalies(df)
    assert len(warnings) == 1
    assert "Column 'date'" in warnings[0]


def test_check_date_range_anomalies_custom_threshold():
    """Custom threshold works correctly."""
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2000-01-01", "2030-01-01"])  # 30 years
        }
    )

    # 30 years should be fine with default 50-year threshold
    warnings_default = checks.check_date_range_anomalies(df)
    assert warnings_default == []

    # Should trigger with 20-year threshold
    warnings_custom = checks.check_date_range_anomalies(df, threshold_years=20)
    assert len(warnings_custom) == 1


def test_check_date_range_anomalies_empty_dataframe():
    """Empty DataFrame returns no warnings."""
    df = pd.DataFrame()
    warnings = checks.check_date_range_anomalies(df)
    assert warnings == []


def test_check_date_range_anomalies_with_nan():
    """NaN values are ignored."""
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(["1970-01-01", np.nan, "2099-01-01"])  # type: ignore
        }
    )
    warnings = checks.check_date_range_anomalies(df)
    assert len(warnings) == 1
    assert "Column 'date'" in warnings[0]


def test_check_date_range_anomalies_specific_columns():
    """Only checks specified columns."""
    df = pd.DataFrame(
        {"date1": pd.to_datetime(["1970-01-01", "2099-01-01"]), "date2": pd.to_datetime(["2020-01-01", "2021-01-01"])}
    )
    warnings = checks.check_date_range_anomalies(df, columns=["date1"])
    assert len(warnings) == 1
    assert "date1" in warnings[0]
    assert "date2" not in str(warnings)


def test_check_date_range_anomalies_single_date():
    """Single date value (no range) should pass."""
    df = pd.DataFrame({"date": pd.to_datetime(["2020-01-01", "2020-01-01", "2020-01-01"])})
    warnings = checks.check_date_range_anomalies(df)
    assert warnings == []


def test_check_date_range_anomalies_multiple_columns():
    """Multiple columns with anomalies."""
    df = pd.DataFrame(
        {
            "start_date": pd.to_datetime(["1900-01-01", "2099-01-01"]),
            "end_date": pd.to_datetime(["1970-01-01", "2100-01-01"]),
            "normal_date": pd.to_datetime(["2020-01-01", "2021-01-01"]),
        }
    )
    warnings = checks.check_date_range_anomalies(df)
    assert len(warnings) == 2
    assert any("start_date" in w for w in warnings)
    assert any("end_date" in w for w in warnings)


def test_check_date_range_anomalies_non_datetime_ignored():
    """Non-datetime columns are ignored."""
    df = pd.DataFrame({"text": ["not", "a", "date"], "number": [1, 2, 3]})
    warnings = checks.check_date_range_anomalies(df)
    assert warnings == []


# ==== Performance Tests ====


def test_performance_large_dataframe():
    """Verify checks work on large DataFrames (basic smoke test)."""
    # Create a reasonably large DataFrame (10K rows)
    np.random.seed(42)
    df = pd.DataFrame(
        {
            "id": range(10000),
            "value": np.random.randn(10000),
            "category": np.random.choice(["A", "B", "C"], 10000),
            "text": ["test_" + str(i) for i in range(10000)],
        }
    )

    # Should complete without errors
    warnings = checks.check_missing_values(df)
    assert isinstance(warnings, list)

    warnings = checks.check_duplicate_rows(df)
    assert isinstance(warnings, list)

    warnings = checks.check_outliers(df)
    assert isinstance(warnings, list)


def test_performance_wide_dataframe():
    """Verify checks work on wide DataFrames (many columns)."""
    # Create DataFrame with many columns
    df = pd.DataFrame({f"col_{i}": [1, 2, 3, 4, 5] for i in range(100)})

    # Should complete without errors
    warnings = checks.check_constant_columns(df)
    assert isinstance(warnings, list)

    warnings = checks.check_duplicate_columns(df)
    assert isinstance(warnings, list)


def test_performance_all_null_columns():
    """Verify optimised handling of all-null columns."""
    df = pd.DataFrame({"all_null": [np.nan] * 1000, "normal": list(range(1000))})

    # Should handle efficiently without processing all-null column
    warnings = checks.check_mixed_types(df)
    assert warnings == []

    warnings = checks.check_whitespace(df)
    assert warnings == []

    warnings = checks.check_outliers(df)
    assert warnings == []


# ==== Correlation Warnings Tests ====


def test_check_correlation_warnings_no_correlation():
    """No correlation in independent columns."""
    np.random.seed(42)
    df = pd.DataFrame({"a": np.random.randn(100), "b": np.random.randn(100), "c": np.random.randn(100)})
    warnings = checks.check_correlation_warnings(df)
    assert warnings == []


def test_check_correlation_warnings_detects_high_correlation():
    """Detects highly correlated columns."""
    df = pd.DataFrame(
        {
            "height_cm": [170, 180, 175, 165, 185],
            "height_inches": [66.9, 70.9, 68.9, 65.0, 72.8],  # ~99% correlated
        }
    )
    warnings = checks.check_correlation_warnings(df, threshold=0.95)
    assert len(warnings) == 1
    assert "height_cm" in warnings[0]
    assert "height_inches" in warnings[0]
    assert "correlated" in warnings[0].lower()


def test_check_correlation_warnings_perfect_correlation():
    """Detects perfectly correlated columns."""
    df = pd.DataFrame(
        {
            "a": [1, 2, 3, 4, 5],
            "b": [2, 4, 6, 8, 10],  # Perfect correlation (b = 2*a) or (b = c*2 - 8)
            "c": [5, 6, 7, 8, 9],  # Perfect correlation (c = a + 4) or (c = b/2 + 4)
        }
    )
    warnings = checks.check_correlation_warnings(df, threshold=0.95)
    assert len(warnings) == 3
    assert "'a'" in warnings[0]
    assert "'b'" in warnings[0]
    assert "100.0%" in warnings[0]


def test_check_correlation_warnings_custom_threshold():
    """Custom threshold works correctly."""
    df = pd.DataFrame(
        {
            "a": [1, 2, 3, 4, 5],
            "b": [1.2, 2.1, 2.5, 3.9, 5.2],  # ~97% correlated
        }
    )

    # High threshold - should not trigger with 0.99
    warnings_high = checks.check_correlation_warnings(df, threshold=0.99)
    assert warnings_high == []

    # Low threshold - should trigger with 0.90
    warnings_low = checks.check_correlation_warnings(df, threshold=0.90)
    assert len(warnings_low) >= 1


def test_check_correlation_warnings_empty_dataframe():
    """Empty DataFrame returns no warnings."""
    df = pd.DataFrame()
    warnings = checks.check_correlation_warnings(df)
    assert warnings == []


def test_check_correlation_warnings_single_numeric_column():
    """Single numeric column returns no warnings."""
    df = pd.DataFrame({"a": [1, 2, 3, 4, 5]})
    warnings = checks.check_correlation_warnings(df)
    assert warnings == []


def test_check_correlation_warnings_no_numeric_columns():
    """Non-numeric columns are ignored."""
    df = pd.DataFrame({"name": ["Alice", "Bob", "Charlie"], "category": ["A", "B", "C"]})
    warnings = checks.check_correlation_warnings(df)
    assert warnings == []


def test_check_correlation_warnings_with_nan():
    """NaN values are handled correctly."""
    df = pd.DataFrame({"a": [1, 2, np.nan, 4, 5], "b": [2, 4, np.nan, 8, 10]})
    warnings = checks.check_correlation_warnings(df, threshold=0.95)
    assert len(warnings) == 1
    assert "'a'" in warnings[0]
    assert "'b'" in warnings[0]


def test_check_correlation_warnings_negative_correlation():
    """Detects negative correlation (absolute value used)."""
    df = pd.DataFrame(
        {
            "a": [1, 2, 3, 4, 5],
            "b": [-2, -4, -6, -8, -10],  # Perfect negative correlation
        }
    )
    warnings = checks.check_correlation_warnings(df, threshold=0.95)
    assert len(warnings) == 1
    assert "'a'" in warnings[0]
    assert "'b'" in warnings[0]
    assert "100.0%" in warnings[0]


def test_check_correlation_warnings_multiple_pairs():
    """Detects multiple correlated pairs."""
    df = pd.DataFrame(
        {
            "a": [1, 2, 3, 4, 5],
            "b": [2, 4, 6, 8, 10],  # Correlated with a
            "c": [10, 20, 30, 40, 50],  # Also correlated with a and b
            "d": [100, 101, 102, 103, 104],  # Not correlated
        }
    )
    warnings = checks.check_correlation_warnings(df, threshold=0.95)
    # Should find a-b, a-c, b-c correlations
    assert len(warnings) >= 2


def test_check_correlation_warnings_invalid_threshold_low():
    """Invalid threshold (too low) raises ValueError."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    try:
        checks.check_correlation_warnings(df, threshold=0)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "between 0 and 1" in str(e).lower()


def test_check_correlation_warnings_invalid_threshold_high():
    """Invalid threshold (too high) raises ValueError."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    try:
        checks.check_correlation_warnings(df, threshold=1.5)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "between 0 and 1" in str(e).lower()


def test_check_correlation_warnings_constant_columns():
    """Constant columns (no variance) are handled."""
    df = pd.DataFrame({"const1": [5, 5, 5, 5], "const2": [10, 10, 10, 10], "varying": [1, 2, 3, 4]})
    warnings = checks.check_correlation_warnings(df)
    # Correlation with constant columns is NaN, should not cause issues
    assert isinstance(warnings, list)


def test_check_correlation_warnings_mixed_types():
    """Mixed numeric and non-numeric columns work correctly."""
    df = pd.DataFrame(
        {
            "height_cm": [170, 180, 175],
            "height_inches": [66.9, 70.9, 68.9],
            "name": ["Alice", "Bob", "Charlie"],
            "category": ["A", "B", "C"],
        }
    )
    warnings = checks.check_correlation_warnings(df, threshold=0.95)
    assert len(warnings) == 1
    assert "height_cm" in warnings[0]
    assert "height_inches" in warnings[0]


"""Tests for referential integrity check."""


def test_basic_referential_integrity():
    """Test basic foreign key validation."""
    # Parent table
    users = pd.DataFrame({"user_id": [1, 2, 3, 4, 5]})

    # Child table - all valid references
    orders = pd.DataFrame({"order_id": [101, 102, 103], "user_id": [1, 2, 3]})

    warnings = checks.check_referential_integrity(orders, {"user_id": users})
    assert len(warnings) == 0


def test_missing_foreign_keys():
    """Test detection of missing foreign key values."""
    users = pd.DataFrame({"user_id": [1, 2, 3]})
    orders = pd.DataFrame(
        {"order_id": [101, 102, 103, 104], "user_id": [1, 2, 5, 9]}  # 5 and 9 don't exist
    )

    warnings = checks.check_referential_integrity(orders, {"user_id": users})
    assert len(warnings) == 1
    assert "user_id" in warnings[0]
    assert "2 values not found" in warnings[0] or "2 missing references" in warnings[0]


def test_multiple_foreign_keys():
    """Test validation across multiple foreign key relationships."""
    users = pd.DataFrame({"user_id": [1, 2, 3]})
    products = pd.DataFrame({"product_id": [10, 20, 30]})

    orders = pd.DataFrame(
        {
            "order_id": [101, 102, 103],
            "user_id": [1, 2, 5],  # 5 missing
            "product_id": [10, 99, 30],  # 99 missing
        }
    )

    warnings = checks.check_referential_integrity(orders, {"user_id": users, "product_id": products})

    assert len(warnings) == 2
    assert any("user_id" in w for w in warnings)
    assert any("product_id" in w for w in warnings)


def test_all_valid_references():
    """Test when all foreign keys are valid."""
    departments = pd.DataFrame({"dept_id": [1, 2, 3]})
    employees = pd.DataFrame(
        {"emp_id": [101, 102, 103], "dept_id": [1, 2, 3]}  # All valid
    )

    warnings = checks.check_referential_integrity(employees, {"dept_id": departments})
    assert len(warnings) == 0


def test_empty_child_dataframe():
    """Test with empty child DataFrame."""
    users = pd.DataFrame({"user_id": [1, 2, 3]})
    orders = pd.DataFrame({"order_id": [], "user_id": []})

    warnings = checks.check_referential_integrity(orders, {"user_id": users})
    assert len(warnings) == 0


def test_empty_parent_dataframe():
    """Test with empty parent DataFrame."""
    users = pd.DataFrame({"user_id": []})
    orders = pd.DataFrame({"order_id": [101, 102], "user_id": [1, 2]})

    warnings = checks.check_referential_integrity(orders, {"user_id": users})
    assert len(warnings) == 1
    assert "user_id" in warnings[0]
    assert "2" in warnings[0]


def test_nan_values_in_foreign_key():
    """Test handling of NaN values in foreign key column."""
    users = pd.DataFrame({"user_id": [1, 2, 3]})
    orders = pd.DataFrame({"order_id": [101, 102, 103], "user_id": [1, float("nan"), 5]})

    warnings = checks.check_referential_integrity(orders, {"user_id": users})
    # NaN should be excluded from validation (common in SQL - nullable FKs)
    assert len(warnings) == 1
    assert "1 value" in warnings[0] or "1 missing" in warnings[0]  # Only value 5


def test_custom_reference_column_name():
    """Test when parent table has different column name."""
    # Parent table has 'id' column
    users = pd.DataFrame({"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"]})

    # Child table references it as 'user_id'
    orders = pd.DataFrame({"order_id": [101, 102], "user_id": [1, 5]})

    # Pass parent column explicitly
    warnings = checks.check_referential_integrity(orders, {"user_id": (users, "id")})
    assert len(warnings) == 1
    assert "user_id" in warnings[0]


def test_no_foreign_keys_specified():
    """Test with empty foreign_keys dictionary."""
    orders = pd.DataFrame({"order_id": [101, 102], "user_id": [1, 2]})

    warnings = checks.check_referential_integrity(orders, {})
    assert len(warnings) == 0


def test_nonexistent_foreign_key_column():
    """Test when specified foreign key column doesn't exist in child DataFrame."""
    users = pd.DataFrame({"user_id": [1, 2, 3]})
    orders = pd.DataFrame({"order_id": [101, 102]})  # No user_id column

    # Check if KeyError is raised
    try:
        checks.check_referential_integrity(orders, {"user_id": users})
        assert False, "Should have raised KeyError"
    except KeyError as e:
        assert "user_id" in str(e)


def test_large_dataset_performance():
    """Test performance with larger datasets."""
    users = pd.DataFrame({"user_id": range(10000)})
    orders = pd.DataFrame(
        {
            "order_id": range(5000),
            "user_id": [i % 10000 if i < 4990 else 99999 for i in range(5000)],
        }
    )

    warnings = checks.check_referential_integrity(orders, {"user_id": users})
    assert len(warnings) == 1
    assert "1 values not found" in warnings[0] or "1 missing" in warnings[0]
