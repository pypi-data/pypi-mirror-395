from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd


def check_missing_values(df: pd.DataFrame) -> List[str]:
    """Check for missing values in the DataFrame

    Args:
        df (pd.DataFrame): The pandas DataFrame to check

    Returns:
        List[str]: A list of warning messages describing missing values found.

    Example:
        ```py
        >>> df = pd.DataFrame({'a': [1, 2, None], 'b': ['x', 'y', 'z']})
        >>> warnings = check_missing_values(df)
        >>> print(warnings[0])

        [Missing Values] Column 'a': 1 missing values (33.3%)
        ```
    """
    warnings: List[str] = []
    missing_info = df.isna().sum()
    missing_cols = missing_info[missing_info > 0]

    if not missing_cols.empty:
        total_rows = len(df)
        for col, count in missing_cols.items():
            percent = (count / total_rows) * 100
            warnings.append(f"[Missing Values] Column '{col}': {count} missing values ({percent:.1f}%)")

    return warnings


def check_duplicate_rows(df: pd.DataFrame) -> List[str]:
    """Check for duplicate rows in the DataFrame

    A row is considered a duplicate if all its values match another row in the
    DataFrame. The first occurrence is not counted as a duplicate. Indices start at 0.


    Args:
        df (pd.DataFrame): The pandas DataFrame to check.

    Returns:
        List[str]: A list of warning messages for duplicate rows with specific indices.

    Example:
        ```py
        >>> df = pd.DataFrame({'a': [1, 2, 2], 'b': ['x', 'y', 'y']})
        >>> warnings = check_duplicate_rows(df)
        >>> print(warnings[0])

        [Duplicate Rows] Found 1 duplicate row(s) at index: 2
        ```
    """
    warnings: List[str] = []

    if df.empty:
        return warnings

    duplicate_mask = df.duplicated(keep="first")

    if not duplicate_mask.any():
        return warnings

    duplicate_indices = df.index[duplicate_mask].tolist()

    if len(duplicate_indices) > 0:
        indices_str = ", ".join(map(str, duplicate_indices))
        warnings.append(f"[Duplicate Rows] Found {len(duplicate_indices)} duplicate row(s) at index: {indices_str}")

    return warnings


def check_mixed_types(df: pd.DataFrame) -> List[str]:
    """Check for columns containing mixed data types.

    Detects columns where values have different Python types (e.g., integers
    mixed with strings). Reports the specific types found and their proportions.

    Args:
        df (pd.DataFrame): The pandas DataFrame to check.

    Returns:
        List[str]: A list of warning messages for mixed data types found with specific
                    type breakdowns.

    Example:
        ```py
        >>> df = pd.DataFrame({'a': [1, 'two', 3], 'b': [1.0, 2.0, 3.0]})
        >>> warnings = check_mixed_types(df)
        >>> print(warnings[0])

        [Mixed Types] Column 'a' has mixed types: int (66%), str (33%)
        ```
    """
    warnings: List[str] = []
    if df.empty:
        return warnings

    for col in df.columns:
        if df[col].isna().all():
            continue

        non_null_values = df[col].dropna()

        if len(non_null_values) == 0:
            continue

        type_series = non_null_values.apply(type)  # type: ignore
        type_counts = type_series.value_counts().to_dict()

        type_counts = {t.__name__: count for t, count in type_counts.items()}

        if len(type_counts) > 1:
            total = len(non_null_values)

            sorted_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)

            type_breakdown = ", ".join(
                [f"{type_name} ({count / total * 100:.0f}%)" for type_name, count in sorted_types]
            )

            warnings.append(f"[Mixed Types] Column '{col}' has mixed types: {type_breakdown}")

    return warnings


def check_whitespace(df: pd.DataFrame) -> List[str]:
    """Detects string values that have leading or trailing spaces,
    which can cause issues in data analysis and matching operations.

    Args:
        df (pd.DataFrame): The pandas DataFrame to check.

    Returns:
        List[str]: A list of warning messages for columns with leading or
                    trailing whitespace.

    Example:
        ```py
        >>> df = pd.DataFrame({'a': [' x', 'y ', ' z ']})
        >>> warnings = check_whitespace(df)
        >>> print(warnings[0])

        [Whitespace] Column 'a' has 3 value(s) with leading or trailing whitespace.
        ```
    """
    warnings: List[str] = []

    if df.empty:
        return warnings

    string_columns = df.select_dtypes(include=["object"]).columns

    for col in string_columns:
        if df[col].isna().all():
            continue

        non_null_values = df[col].dropna()

        has_whitespace = non_null_values.astype(str).str.len() != non_null_values.astype(str).str.strip().str.len()
        whitespace_count = has_whitespace.sum()

        if whitespace_count > 0:
            warnings.append(
                f"[Whitespace] Column '{col}' has {whitespace_count} value(s) with leading or trailing whitespace."
            )
    return warnings


def check_constant_columns(df: pd.DataFrame) -> List[str]:
    """Check for columns where all values are the same (zero variance).

    Identifies columns with only one unique value (excluding NaN), which are often
    redundant for analysin/modelling.

    Args:
        df (pd.DataFrame): The pandas DataFrame to check.

    Returns:
        List[str]: A list of warning messages for constant columns found.

    Example:
        ```py
        >>> df = pd.DataFrame({'a': [1, 1, 1]})
        >>> warnings = check_constant_columns(df)
        >>> print(warnings[0])

        [Constant Column] Column 'a' has only one unique value: 1.
        ```
    """
    warnings: List[str] = []

    if df.empty:
        return warnings

    for col in df.columns:
        unique_values = df[col].dropna().unique()

        if len(unique_values) == 0:
            warnings.append(f"[Constant Column] Column '{col}' contains only missing values.")

        elif len(unique_values) == 1:
            constant_value = unique_values[0]

            display_value = f"'{constant_value}'" if isinstance(constant_value, str) else str(constant_value)

            warnings.append(f"[Constant Column] Column '{col}' has only one unique value: {display_value}.")
    return warnings


def check_unique_columns(df: pd.DataFrame, threshold: Optional[float] = 0.95) -> List[str]:
    """Check for columns with a high proportion of unique values.

    Args:
        df (pd.DataFrame): The pandas DataFrame to check.
        threshold (float, optional): The unique value proportion threshold.
                                        Defaults to 0.95.

    Returns:
        List[str]: A list of warning messages for columns exceeding
                    the unique value threshold.

    Example:
        ```py
        >>> df = pd.DataFrame({'a': [1, 2, 3, 4, 5]})
        >>> warnings = check_unique_columns(df, threshold=0.8)
        >>> print(warnings[0])

        [Unique Column] Column 'a' is 100.0% unique
        ```
    """
    warnings: List[str] = []

    if threshold:
        if not (0 < threshold <= 1):
            raise ValueError("Uniqueness threshold must be between 0 and 1.")
    else:
        threshold = 0.95

    if df.empty:
        return warnings

    for col in df.columns:
        non_null_values = df[col].dropna()

        if len(non_null_values) == 0:
            continue

        num_unique = non_null_values.nunique()
        total_non_null = len(non_null_values)
        unique_ratio = num_unique / total_non_null

        if unique_ratio >= threshold:
            percent = unique_ratio * 100
            warnings.append(f"[Unique Column] Column '{col}' is {percent:.1f}% unique")

    return warnings


def check_outliers(df: pd.DataFrame, method: Optional[str] = "iqr", threshold: Optional[float] = 1.5) -> List[str]:
    """Check for outliers using different methods.

    Provides a threshold value that sets trigger for outliers. Currently
    supports IQR method.

    Args:
        df (pd.DataFrame): The pandas DataFrame to check.
        method (Optional[str], optional): The outlier detection method to use.
                                            Defaults to "iqr".
        threshold (Optional[float], optional): The threshold for detecting outliers.
                                                Defaults to 1.5.

    Raises:
        ValueError (Method): If the method is not supported.
        ValueError (Threshold): If the threshold is not a positive number.

    Returns:
        List[str]: A list of warning messages for columns with detected outliers.
    Example:
        ```py
        >>> df = pd.DataFrame({'a': [1, 2, 3, 100, 5]})
        >>> warnings = check_outliers(df)
        >>> print(warnings[0])

        [Outliers] Column 'a': 1 potential outlier(s) detected (iqr method).
        ```
    """
    warnings: List[str] = []

    if method and method.lower() != "iqr":
        raise ValueError("Currently, only 'iqr' method is supported for outlier detection.")

    if threshold:
        if threshold <= 0:
            raise ValueError("Threshold must be a positive number.")
    else:
        threshold = 1.5

    if df.empty:
        return warnings

    numeric_columns = df.select_dtypes(include=[np.number]).columns

    for col in numeric_columns:
        if df[col].isna().all():
            continue

        non_null_values = df[col].dropna()

        if len(non_null_values) == 0:
            continue

        q1, q3 = non_null_values.quantile([0.25, 0.75])
        iqr = q3 - q1

        if iqr == 0:
            continue

        lower_bound = q1 - threshold * iqr
        upper_bound = q3 + threshold * iqr

        outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
        outlier_count = outlier_mask.sum()

        if outlier_count > 0:
            warnings.append(
                f"[Outliers] Column '{col}': {outlier_count} potential outlier(s) detected ({method} method)."
            )

    return warnings


def check_missing_patterns(df: pd.DataFrame, threshold: float = 0.9) -> List[str]:
    """Detects patterns in missing data across columns.

    Identifies when multiple columns have missing values in the same rows,
    which may indicate systematic missingness (e.g., related fields that are
    filled out together or not at all.)

    Args:
        df (pd.DataFrame): The pandas DataFrame to check.
        threshold (float, optional): The threshold for detecting missing patterns.
                                        Defaults to 0.9.

    Returns:
        List[str]: A list of warning messages for columns with detected missing patterns.

    Example:
        ```py
        >>> df = pd.DataFrame({'age': [25, None, 30, None], 'income': [50000, None, 60000, None]})
        >>> warnings = check_missing_patterns(df, threshold=0.8)
        >>> print(warnings[0])

        [Missing Patterns] Columns 'age' and 'income' identical missing rows (likely related).
        ```
    """
    warnings: List[str] = []

    if df.empty:
        return warnings

    cols_with_missing = df.columns[df.isna().any()].tolist()

    if len(cols_with_missing) < 2:
        return warnings

    checked_pairs = set()

    for i, col1 in enumerate(cols_with_missing):
        for col2 in cols_with_missing[i + 1 :]:
            pair_key = tuple(sorted([col1, col2]))
            if pair_key in checked_pairs:
                continue
            checked_pairs.add(pair_key)

            missing_col1 = df[col1].isna()
            missing_col2 = df[col2].isna()

            both_missing = (missing_col1 & missing_col2).sum()

            total_missing_col1 = missing_col1.sum()
            total_missing_col2 = missing_col2.sum()

            if total_missing_col1 == 0 or total_missing_col2 == 0:
                continue

            overlap_ratio1 = both_missing / total_missing_col1
            overlap_ratio2 = both_missing / total_missing_col2

            if overlap_ratio1 >= threshold and overlap_ratio2 >= threshold:
                warnings.append(
                    f"[Missing Patterns] Columns '{col1}' and '{col2}' identical missing rows (likely related)"
                )
    return warnings


def check_case_consistency(df: pd.DataFrame, min_unique: int = 2) -> List[str]:
    """Check for inconsistent casing in string columns.

    Detects columns where the same logical value appears with different casing (e.g., "Active", "active", "ACTIVE"). This is common
    in categorical data and can cause issues in analysis and grouping operations.

    Args:
        df (pd.DataFrame): The pandas DataFrame to analyse
        min_unique (int, optional): Minimum number of unique values for a column to be checked. Columns with fewer unique values are skipped as
                                    they're likely boolean-like. Defaults to 2.

    Returns:
        List[str]: A list of warning messages for columns with inconsistent casing.

    Example:
        ```py
        >>> df = pd.DataFrame({'status': ['Active', 'active', 'Inactive', 'ACTIVE']})
        >>> warnings = check_case_consistency(df)
        >>> print(warnings[0])

        [Case Consistency] Column 'status': mixed case detected (e.g., 'Active', 'active', 'ACTIVE')
        ```
    """
    warnings: List[str] = []

    if df.empty:
        return warnings

    string_cols = df.select_dtypes(include=["object"]).columns

    for col in string_cols:
        non_null_values = df[col].dropna()
        if len(non_null_values) == 0:
            continue

        str_values = non_null_values.astype(str)

        unique_values = str_values.unique()

        lowercase_values = str_values.str.lower()
        unique_lowercase = lowercase_values.unique()

        if len(unique_values) < min_unique:
            continue

        if len(unique_values) > len(unique_lowercase):
            case_variants = {}
            for val in unique_values:
                lower_val = val.lower()
                if lower_val not in case_variants:
                    case_variants[lower_val] = []
                case_variants[lower_val].append(val)

            examples = []
            for lower_val, variants in case_variants.items():
                if len(variants) > 1:
                    examples = sorted(variants)[:3]
                    break

            examples_str = ", ".join([f"'{ex}'" for ex in examples])

            warnings.append(f"[Case Consistency] Column '{col}': mixed case detected (e.g., {examples_str})")

    return warnings


def check_cardinality(df: pd.DataFrame, high_threshold: int = 50, low_threshold: int = 2) -> List[str]:
    """Check for columns with unusually high or low cardinality.

    Identifies categorical columns with too many unique valies (high cardinality, potentially an ID column) or too few
    unique values (lower cardinality, potentially a constant or near-constant column (boolean-like)).

    Args:
        df (pd.DataFrame): The pandas DataFrame to check.
        high_threshold (int, optional): The maximum number of unique values for a column to be considered low cardinality. Defaults to 50.
        low_threshold (int, optional): The minimum number of unique values for a column to be considered high cardinality. Defaults to 2.

    Returns:
        List[str]: A list of warning messages for columns with unusual cardinality.

    Example:
        ```py
        >>> df = pd.DataFrame({'id': range(100), 'status': ['active'] * 100})
        >>> warnings = check_cardinality(df, high_threshold=80, low_threshold=5)
        >>> print(warnings[0])

        [High Cardinality] Column 'id' has 100 unique values (100.0% unique)

        >>> print(warnings[1])

        [Low Cardinality] Column 'status' has only 1 unique value.
        ```
    """
    warnings: List[str] = []

    if df.empty:
        return warnings

    for col in df.columns:
        non_null_values = df[col].dropna()

        if len(non_null_values) == 0:
            continue

        num_unique = non_null_values.nunique()
        total_non_null = len(non_null_values)
        unique_ratio = num_unique / total_non_null

        if num_unique > high_threshold:
            percent = unique_ratio * 100
            warnings.append(f"[High Cardinality] Column '{col}' has {num_unique} unique values ({percent:.1f}% unique)")
        elif num_unique < low_threshold:
            if num_unique == 1:
                warnings.append(f"[Low Cardinality] Column '{col}' has only 1 unique value.")
            else:
                warnings.append(f"[Low Cardinality] Column '{col}' has only {num_unique} unique values.")

    return warnings


def check_skewness(df: pd.DataFrame, threshold: float = 1.0) -> List[str]:
    """Check for skewness in numeric columns.

    Detects if a column is right or left leaning in variance. Recommends if a log transformation might be required.

    Args:
        df (pd.DataFrame): The pandas DataFrame to check
        threshold (float, optional): The threshold for detecting threshold. Defaults to 1.0.

    Raises:
        ValueError: If the threshold is not a positive number.

    Returns:
        List[str]: A list of warning messages for skewed columns.

    Example:
        ```py
        >>> df = pd.DataFrame({'a': [1, 2, 3, 100, 5]})
        >>> warnings = check_skewness(df, threshold=1.0)
        >>> print(warnings[0])

        [Skewness] Column 'a' is highly right-skewed (skewness=2.5). Consider log transformation.
        ```
    """
    warnings: List[str] = []

    if df.empty:
        return warnings

    if threshold and threshold <= 0:
        raise ValueError("Threshold must be a positive number.")

    numeric_columns = df.select_dtypes(include=[np.number]).columns

    for col in numeric_columns:
        non_null_values = df[col].dropna()

        if len(non_null_values) == 0:
            continue

        skewness = non_null_values.skew()

        if abs(skewness) > threshold:  # type: ignore
            direction = "right-skewed" if skewness > 0 else "left-skewed"  # type: ignore
            warnings.append(
                f"[Skewness] Column '{col}' is highly {direction} (skewness={skewness:.1f}). Consider log transformation."
            )

    return warnings


def check_duplicate_columns(df: pd.DataFrame) -> List[str]:
    """Check for columns with identical values (reduntant columns).

    Identifies pairs of columns that contain exactly the same data, which are often redundant and can be removed
    to simplify the dataset.

    Args:
        df (pd.DataFrame): The pandas DataFrame to check.

    Returns:
        List[str]: A list of warning messages for duplicate columns pairs.

    Example:
        ```py
        >>> df = pd.DataFrame({'a': [1, 2, 3], 'b': [1, 2, 3], 'c': [4, 5, 6]})
        >>> warnings = check_duplicate_columns(df)
        >>> print(warnings[0])

        [Duplicate Columns] Columns 'a' and 'b' are identical.
        ```
    """
    warnings: List[str] = []

    if df.empty:
        return warnings

    checked_pairs = set()

    for i, col1 in enumerate(df.columns):
        for col2 in df.columns[i + 1 :]:
            pair_key = tuple(sorted([col1, col2]))
            if pair_key in checked_pairs:
                continue

            checked_pairs.add(pair_key)

            if df[col1].equals(df[col2]):
                sorted_cols = sorted([col1, col2])
                warnings.append(f"[Duplicate Columns] Columns '{sorted_cols[0]}' and '{sorted_cols[1]}' are identical.")
    return warnings


def check_data_type_consistency(df: pd.DataFrame) -> List[str]:
    """Check if column data types match expected patterns based on column names.

    Uses heuristics to identify columns that may have incorrect data types based on commin naming patterns.
    For example, "columns" with 'date' in the name should be datetime, 'age' or 'count' should be numeric, etc.

    Args:
        df (pd.DataFrame): The pandas DataFrame to check.

    Returns:
        List[str]: A list of warning messages for data type inconsistencies.

    Example:
        ```py
        >>> df = pd.DataFrame({'age': ['25', '30', '35']})
        >>> warnings = check_data_type_consistency(df)
        >>> print(warnings[0])

        [Type Warning] Column 'age' is stored as object, consider numeric type.
        ```
    """
    warnings: List[str] = []

    if df.empty:
        return warnings

    numeric_patterns = [
        "age",
        "count",
        "number",
        "num",
        "quantity",
        "qty",
        "amount",
        "price",
        "total",
        "cost",
        "value",
        "sum",
        "average",
        "avg",
        "mean",
        "score",
        "rating",
        "percent",
        "percentage",
        "proportion",
        "rate",
        "ratio",
    ]

    datetime_patterns = [
        "date",
        "time",
        "timestamp",
        "datetime",
        "created",
        "updated",
        "modified",
        "birth",
        "dob",
        "year",
        "month",
    ]

    boolean_patterns = ["is_", "has_", "flag", "status", "active", "enabled", "disabled"]

    for col in df.columns:
        col_lower = col.lower()
        col_dtype = df[col].dtype

        if any(pattern in col_lower for pattern in numeric_patterns) and (
            col_dtype == "object" or col_dtype.name == "object"
        ):
            non_null_values = df[col].dropna()
            if len(non_null_values) > 0:
                try:
                    pd.to_numeric(non_null_values.astype(str), errors="coerce")
                    warnings.append(f"[Type Warning] Column '{col}' is stored as object, consider numeric type.")
                except Exception:
                    pass

        elif any(pattern in col_lower for pattern in datetime_patterns) and (
            col_dtype != "datetime64[ns]" and not pd.api.types.is_datetime64_any_dtype(df[col])
        ):
            warnings.append(f"[Type Warning] Column '{col}' is stored as {col_dtype}, consider datetime type.")

        elif any(col_lower.startswith(pattern) for pattern in boolean_patterns) and col_dtype != "bool":
            unique_vals = df[col].dropna().nunique()
            if unique_vals <= 2 and len(df[col].dropna()) > 0:
                warnings.append(f"[Type Warning] Column '{col}' is stored as {col_dtype}, consider boolean type.")

    return warnings


def check_negative_values(df: pd.DataFrame, columns: Optional[List[str]] = None) -> List[str]:
    """Check for negative values in columns that shouldn't have them.

    Detects negative values in numerical columns. Optionally specify which columns to check, otherwise all numerical columns are checked.

    Args:
        df (pd.DataFrame): The pandas DataFrame to check.
        columns (Optional[List[str]], optional): Specific columns to check. Defaults to None. If None, all numeric columns are checked.

    Returns:
        List[str]: A list of warning messages for columns with negative values.

    Example:
        ```py
        >>> df = pd.DataFrame({'age': [25, -30, 35], 'income': [50000, 60000, -70000]})
        >>> warnings = check_negative_values(df, columns=['age'])
        >>> print(warnings[0])

        [Negative Values] Column 'age' has 1 negative value(s).
        ```
    """
    warnings: List[str] = []

    if df.empty:
        return warnings

    if columns is None:
        columns_to_check = df.select_dtypes(include=[np.number]).columns.to_list()
    else:
        columns_to_check = [col for col in columns if col in df.columns and pd.api.types.is_numeric_dtype(df[col])]

    for col in columns_to_check:
        non_null_values = df[col].dropna()

        if len(non_null_values) == 0:
            continue

        negative_count = (non_null_values < 0).sum()

        if negative_count > 0:
            warnings.append(f"[Negative Values] Column '{col}' has {negative_count} negative value(s).")

    return warnings


def check_rare_categories(df: pd.DataFrame, threshold: float = 0.01) -> List[str]:
    """Check for categories that appear very infrequently.

    Identifies categorical valaues that appear less than the threshold  percentage of times. These
    rare categories can cause issues in modelling and analysis.

    Args:
        df (pd.DataFrame): The pandas DataFrame to check.
        threshold (float, optional): The minimum proportion for a category to not be considered rare. Defaults to 0.01 (1%).

    Raises:
        ValueError: If the threshold is not between 0 and 1.

    Returns:
        List[str]: A list of warning messages for columns with rare categories.

    Example:
        ```py
        >>> df = pd.DataFrame({'category': ['A'] * 98 + ['B', 'C']})
        >>> warnings = check_rare_categories(df, threshold=0.02)
        >>> print(warnings[0])

        [Rare Categories] Column 'category': 2 categories appear <2.0% of the time.
        ```
    """
    warnings: List[str] = []

    if df.empty:
        return warnings

    if not (0 < threshold < 1):
        raise ValueError("Threshold must be between 0 and 1.")

    categorical_columns = df.select_dtypes(include=["object", "category"]).columns

    for col in categorical_columns:
        non_null_values = df[col].dropna()

        if len(non_null_values) == 0:
            continue

        value_counts = non_null_values.value_counts()
        total_count = len(non_null_values)

        rare_categories = value_counts[value_counts / total_count < threshold]

        if len(rare_categories) > 0:
            percent = threshold * 100
            warnings.append(
                f"[Rare Categories] Column '{col}': {len(rare_categories)} categories appear <{percent:.1f}% of the time."
            )
    return warnings


def check_date_format_consistency(df: pd.DataFrame) -> List[str]:
    """Check for inconsistent date formats in string columns.

    Attemps to detect columns that contain dates in multiple formats (e.g., 'YYYY-MM-DD' and 'DD/MM/YYYY' mixed together).

    Args:
        df (pd.DataFrame): The pandas DataFrame to check.

    Returns:
        List[str]: A list of warning messages for columns with inconsistent date formats.

    Example:
        ```py
        >>> df = pd.DataFrame({'date': ['2020-01-01', '01/02/2020', '2020-03-01']})
        >>> warnings = check_date_format_consistency(df)
        >>> print(warnings[0])

        [Date Format Consistency] Column 'date' has inconsistent date formats.
        ```
    """
    warnings: List[str] = []

    if df.empty:
        return warnings

    date_patterns = [
        r"\d{4}-\d{2}-\d{2}",  # YYYY-MM-DD
        r"\d{2}-\d{2}-\d{4}",  # MM-DD-YYYY or DD-MM-YYYY
        r"\d{4}/\d{2}/\d{2}",  # YYYY/MM/DD
        r"\d{2}/\d{2}/\d{4}",  # MM/DD/YYYY or DD/MM/YYYY
        r"\d{4}\.\d{2}\.\d{2}",  # YYYY.MM.DD
        r"\d{2}\.\d{2}\.\d{4}",  # MM.DD.YYYY or DD.MM.YYYY
    ]

    string_columns = df.select_dtypes(include=["object"]).columns

    for col in string_columns:
        if "date" not in col.lower() and "time" not in col.lower():
            continue

        non_null_values = df[col].dropna().astype(str)

        if len(non_null_values) == 0:
            continue

        formats_found = set()
        for pattern in date_patterns:
            if non_null_values.str.contains(pattern, regex=True).any():
                formats_found.add(pattern)

        if len(formats_found) > 1:
            warnings.append(f"[Date Format Consistency] Column '{col}' has inconsistent date formats.")

    return warnings


def check_string_length_outliers(df: pd.DataFrame, threshold: float = 3.0) -> List[str]:
    """Check for strings that are significantly longer or shorter than others.

    Detects string values with unusual lengths compared to other values in the same
    column, which may indicate data entry errors or data quality issues.

    Args:
        df (pd.DataFrame): The pandas DataFrame to check.
        threshold (float, optional): For small samples (n<10), this is a ratio multiplier.
                                      For larger samples, this is the number of standard
                                      deviations. Defaults to 3.0.

    Returns:
        List[str]: A list of warning messages for columns with string length outliers.

    Example:
        ```py
        >>> df = pd.DataFrame({'email': ['a@b.com', 'test@example.com', 'x' * 100 + '@example.com']})
        >>> warnings = check_string_length_outliers(df)
        >>> print(warnings[0])

        [String Length Outliers] Column 'email' has 1 value(s) with unusual length
        ```
    """
    warnings: List[str] = []

    if df.empty:
        return warnings

    if threshold <= 0:
        raise ValueError("Threshold must be a positive number.")

    string_columns = df.select_dtypes(include=["object"]).columns

    for col in string_columns:
        non_null_values = df[col].dropna().astype(str)

        if len(non_null_values) < 3:
            continue

        lengths = non_null_values.str.len()
        n = len(lengths)

        if n < 10:
            median_length = lengths.median()

            if median_length == 0:
                continue

            outlier_count = ((lengths > threshold * median_length) | (lengths < median_length / threshold)).sum()  # type: ignore

            if outlier_count > 0:
                warnings.append(f"[String Length] Column '{col}' has {outlier_count} value(s) with unusual length")
        else:
            mean_length = lengths.mean()
            std_length = lengths.std()

            if std_length == 0:
                continue

            z_scores = (lengths - mean_length) / std_length
            outliers = (z_scores.abs() > threshold).sum()

            if outliers > 0:
                warnings.append(f"[String Length Outliers] Column '{col}' has {outliers} value(s) with unusual length")

    return warnings


def check_zero_inflation(df: pd.DataFrame, threshold: float = 0.5) -> List[str]:
    """Check for columns with an excessive proportion of zero values.

    Detects numerical columns where zeros make up more than the specified threshold percentage of values. This can
    indicate data collection issues, default values, or sparse data that may need special handling.

    Args:
        df (pd.DataFrame): The pandas DataFrame to check.
        threshold (float, optional): The minimum proportion of zeros to flag (0-1). Defaults to 0.5 (50%).

    Raises:
        ValueError: If the threshold is not between 0 and 1.

    Returns:
        List[str]: A list of warning messages for columns with excessive zero values.

    Example:
        ```py
        >>> df = pd.DataFrame({'purchases': [0, 0, 0, 0, 0, 100, 200]})
        >>> warnings = check_zero_inflation(df, threshold=0.5)
        >>> print(warnings[0])

        [Zero Inflation] Column 'purchases': 71.4% of values are zero
        ```
    """
    warnings: List[str] = []

    if df.empty:
        return warnings

    if not (0 < threshold < 1):
        raise ValueError("Threshold must be between 0 and 1.")

    numeric_columns = df.select_dtypes(include=[np.number]).columns

    for col in numeric_columns:
        non_null_values = df[col].dropna()

        if len(non_null_values) == 0:
            continue

        zero_count = (non_null_values == 0).sum()
        total_count = len(non_null_values)
        zero_ratio = zero_count / total_count

        if zero_ratio > threshold:
            percent = zero_ratio * 100
            warnings.append(f"[Zero Inflation] Column '{col}': {percent:.1f}% of values are zero")

    return warnings


def check_future_dates(
    df: pd.DataFrame, columns: Optional[List[str]] = None, reference_date: Optional[str] = None
) -> List[str]:
    """Check for dates that occur in the future.

    Identifies date values that are later than the reference date (default: today), which may
    indicate data entry errors or incorrect date parsing for historical data.

    Args:
        df (pd.DataFrame): The pandas DataFrame to check.
        columns (Optional[List[str]], optional): Specific columns to check. If None, checks all datetime columns and columns with 'date' in the name. Defaults to None.
        reference_date (Optional[str], optional): The reference date to compare against. If None, uses today's date. Defaults to None.

    Raises:
        ValueError: If reference_date is provided but not in ISO format (YYYY-MM-DD).

    Returns:
        List[str]: A list of warning messages for future dates.

    Example:
        ```py
        >>> df = pd.DataFrame({'birth_date': pd.to_datetime(['1990-01-01', '2050-01-01', '1985-06-15'])})
        >>> warnings = check_future_dates(df)
        >>> print(warnings[0])

        [Future Dates] Column 'birth_date' has 1 date(s) in the future compared to 2024-06-01.
        ```
    """
    warnings: List[str] = []

    if df.empty:
        return warnings

    if reference_date is None:
        reference_dt = pd.Timestamp.now()
    else:
        try:
            reference_dt = pd.to_datetime(reference_date)
        except Exception:
            raise ValueError("reference_date must be in ISO format (YYYY-MM-DD)")

    if columns is None:
        datetime_columns = df.select_dtypes(include=["datetime64"]).columns.to_list()
        date_name_columns = [col for col in df.columns if "date" in col.lower() or "time" in col.lower()]
        columns_to_check = list(set(datetime_columns + date_name_columns))
    else:
        columns_to_check = [col for col in columns if col in df.columns]

    for col in columns_to_check:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            date_values = df[col].dropna()
        else:
            try:
                date_values = pd.to_datetime(df[col], errors="coerce").dropna()
            except Exception:
                continue

        if len(date_values) == 0:
            continue

        future_dates = date_values[date_values > reference_dt]
        future_count = len(future_dates)

        if future_count > 0:
            warnings.append(
                f"[Future Dates] Column '{col}' has {future_count} date(s) in the future compared to {reference_dt.date()}."
            )

    return warnings


def check_special_characters(df: pd.DataFrame, threshold: float = 0.1) -> List[str]:
    """Check for unusual or potentially problematic special characters in text columns.

    Detects columns containing special characters that may indicate encoding issues, copy-paste errors,
    or data corruption. Looks for non-ASCII characters, control characters, and common mis-encoded symbols.

    Args:
        df (pd.DataFrame): The pandas DataFrame to check.
        threshold (float, optional): The proportion of special characters allowed before raising a warning. Defaults to 0.1.

    Raises:
        ValueError: If the threshold is not between 0 and 1.

    Returns:
        List[str]: A list of warning messages for special characters.

    Example:
        ```py
        >>> df = pd.DataFrame({'name': ['Alice', 'Bobâ„¢', 'Charlieâ€¢']})
        >>> warnings = check_special_characters(df)
        >>> print(warnings[0])

        [Special Characters] Column 'name': 66.7% of values contain special or non-standard characters.
        ```
    """
    warnings: List[str] = []

    if df.empty:
        return warnings

    if not (0 <= threshold < 1):
        raise ValueError("Threshold must be between 0 and 1, inclusive of 0.")

    string_columns = df.select_dtypes(include=["object"]).columns

    suspicious_pattern = (
        r"[^\x20-\x7E]|"  # Non-printable ASCII and non-ASCII characters
        r"â€[™¢ž¦]|"  # Common encoding artifacts
        r"â„¢|Â©|Â®"  # More encoding artifacts
    )

    for col in string_columns:
        non_null_values = df[col].dropna().astype(str)

        if len(non_null_values) == 0:
            continue

        has_special = non_null_values.str.contains(suspicious_pattern, regex=True, na=False)
        special_count = has_special.sum()
        total_count = len(non_null_values)
        special_ratio = special_count / total_count

        if special_ratio >= threshold:
            percent = special_ratio * 100
            warnings.append(
                f"[Special Characters] Column '{col}': {percent:.1f}% of values contain special or non-standard characters."
            )
    return warnings


def check_date_range_anomalies(
    df: pd.DataFrame, columns: Optional[List[str]] = None, threshold_years: float = 50
) -> List[str]:
    """Check for columns where the range between the minimum and maximum dates is unusually large.

    This funciton identifies date columns where the span between the earliest and latest dates exceeds a specified threshold (default: 50 years). Such
    anomalies may indicate data entry errors, incorrect date parsing, or unexpected data distributions.

    Args:
        df (pd.DataFrame): The pandas DataFrame to check.
        columns (Optional[List[str]], optional): Specific columns to check. Defaults to None.
        threshold_years (float, optional): Maximum acceptable date range in years. Columns with date ranges exceeding will be flagged. Defaults to 50.

    Returns:
        List[str]: A list of warning messages for date range anomalies.

    Example:
        ```py
        >>> df = pd.DataFrame({'event_date': pd.to_datetime(['1900-01-01', '2000-01-01', '1950-06-15'])})
        >>> warnings = check_date_range_anomalies(df, threshold_years=80)
        >>> print(warnings[0])

        [Date Range Anomalies] Column 'event_date': date range spans 100.0 years (1900-01-01 to 2000-01-01).
        ```
    """
    warnings: List[str] = []

    if df.empty:
        return warnings

    if threshold_years <= 0:
        raise ValueError("threshold_years must be a positive number.")
    if columns is None:
        datetime_columns = df.select_dtypes(include=["datetime64"]).columns.to_list()
        date_name_columns = [col for col in df.columns if "date" in col.lower() or "time" in col.lower()]
        columns_to_check = list(set(datetime_columns + date_name_columns))
    else:
        columns_to_check = [col for col in columns if col in df.columns]

    for col in columns_to_check:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            date_values = df[col].dropna()
        else:
            try:
                date_values = pd.to_datetime(df[col], errors="coerce").dropna()
            except Exception:
                continue

        if len(date_values) < 2:
            continue

        min_date = date_values.min()
        max_date = date_values.max()
        date_range_years = (max_date - min_date).days / 365.25

        if date_range_years > threshold_years:
            warnings.append(
                f"[Date Range Anomalies] Column '{col}': date range spans {date_range_years:.1f} years "
                f"({min_date.date()} to {max_date.date()})"
            )
    return warnings


def check_correlation_warnings(df: pd.DataFrame, threshold: float = 0.95) -> List[str]:
    """Check correlation between numeric columns.

    Identifies pairs of numeric columns that have a high correlation (above the specified threshold), which may indicate redundancy or multicollinearity issues.

    Args:
        df (pd.DataFrame): The pandas DataFrame to check.
        threshold (float, optional): Correlation threshold above which warnings are generated. Defaults to 0.95.

    Raises:
        ValueError: If the threshold is not between 0 and 1.
    Returns:
        List[str]: A list of warning messages for highly correlated column pairs.
    Example:
        ```py
        >>> df = pd.DataFrame({'a': [1, 2, 3, 4, 5], 'b': [2, 4, 6, 8, 10], 'c': [5, 4, 3, 2, 1]})
        >>> warnings = check_correlation_warnings(df, threshold=0.9)
        >>> print(warnings[0])

        [High Correlation] Columns 'a' and 'b' are 100.0% correlated.
        ```
    """
    warnings: List[str] = []

    if df.empty:
        return warnings

    if not (0 < threshold <= 1):
        raise ValueError("Correlation threshold must be between 0 and 1.")

    numeric_df = df.select_dtypes(include=[np.number])

    if len(numeric_df.columns) < 2:
        return warnings

    corr_matrix = numeric_df.corr()

    checked_pairs = set()

    for i, col1 in enumerate(corr_matrix.columns):
        for j, col2 in enumerate(corr_matrix.columns):
            if i >= j:
                continue

            pair_key = tuple(sorted([col1, col2]))
            if pair_key in checked_pairs:
                continue

            checked_pairs.add(pair_key)

            corr_value = abs(corr_matrix.loc[col1, col2])  # type: ignore

            if not pd.isna(corr_value) and corr_value >= threshold:  # type: ignore
                percent = corr_value * 100
                warnings.append(f"[High Correlation] Columns '{col1}' and '{col2}' are {percent:.1f}% correlated.")

    return warnings


def check_referential_integrity(
    df: pd.DataFrame,
    foreign_keys: Dict[str, Union[pd.DataFrame, Tuple[pd.DataFrame, str]]],
) -> List[str]:
    """Check if foreing key values exist in their referenced parent tables.

    This function validates referential integrity by checking whether values in specified foreign key columns exist in their corresponding
    parent tables. This is essential for multi-table data validation and ensures consistency across related datasets.

    Args:
        df (pd.DataFrame): The child DataFrame containing foreign key column(s) to validate.
        foreign_keys (Dict[str, Union[pd.DataFrame, Tuple[pd.DataFrame, str]]]): Dictionary mapping foreign key column names to their parent tables.
            Key: Name of the foreign key column in `df`.
            Value: Either
                a parent DataFrame (assumes the first column is the referenced column), or
                a tuple of (parent_df, parent_column_name) for explicit column reference.

    Raises:
        KeyError: If a foreign key column or parent column is not found in the child DataFrame or parent DataFrame respectively.

    Returns:
        List[str]: A list of warning messages for foreign key violations.

    Notes:
        - Null values in foreign key columns are ignored.
        - Only checks for existence; does not validate other constraints (e.g., cascading deletes).

    Example:
        ```py
        >>> users = pd.DataFrame({'user_id': [1, 2, 3]})
        >>> orders = pd.DataFrame({'order_id': [101, 102, 103], 'user_id': [1, 2, 4]})
        >>> warnings = check_referential_integrity(orders, {'user_id': users})
        >>> print(warnings[0])

        [Referential Integrity] Column 'user_id': 1 values not found in parent column 'user_id' (33.3% of non-null values).
        ```
    """
    warnings: List[str] = []

    if df.empty:
        return warnings

    if not foreign_keys:
        return warnings

    for fk_column, parent_ref in foreign_keys.items():
        if isinstance(parent_ref, tuple):
            parent_df, parent_column = parent_ref
        else:
            parent_df = parent_ref
            parent_column = parent_df.columns[0]

        if fk_column not in df.columns:
            raise KeyError(
                f"Foreign key column '{fk_column}' not found in DataFrame. Available columns: {df.columns.tolist()}"
            )

        if parent_column not in parent_df.columns:
            raise KeyError(
                f"Parent column '{parent_column}' not found in parent DataFrame. Available columns: {parent_df.columns.tolist()}"
            )

        fk_values = df[fk_column].dropna()

        if len(fk_values) == 0:
            continue

        parent_values = set(parent_df[parent_column].dropna())

        invalid_fk_values = set(fk_values) - parent_values

        if invalid_fk_values:
            num_invalid = len(invalid_fk_values)
            pot_invalid = (num_invalid / len(fk_values)) * 100

            warnings.append(
                f"[Referential Integrity] Column '{fk_column}': {num_invalid} values not found in parent column '{parent_column}' "
                f"({pot_invalid:.1f}% of non-null values)."
            )

    return warnings
