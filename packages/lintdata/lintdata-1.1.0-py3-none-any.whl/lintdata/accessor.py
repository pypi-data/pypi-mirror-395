"""
Implements the core LintData accessor for pandas Dataframes
"""

import csv
import json
import re
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import pandas as pd

from . import checks
from .parallel import ParallelExecutor
from .report_formatter import HTMLReportFormatter

__all__ = ["LintAccessor"]


@pd.api.extensions.register_dataframe_accessor("lint")
class LintAccessor:
    """An Accessor for pandas DataFrames to run data quality checks."""

    def __init__(self, pandas_obj: pd.DataFrame) -> None:
        self._validate(pandas_obj)
        self._df = pandas_obj
        self._custom_checks: Dict[str, Any] = {}

    @staticmethod
    def _validate(obj: pd.DataFrame) -> None:
        if not isinstance(obj, pd.DataFrame):
            raise AttributeError("LintData accessor can only be used with pandas DataFrames.")

    def register_check(self, check_func: Any, name: Optional[str] = None) -> None:
        """Register a custom check function.

        Custom check functions should accept a DataFrame as the first argument and return a List[str] of warning messages.

        Args:
            check_func (Any): Function that takes a DataFrame and returns List[str] of warnings.
            name (Optional[str], optional): Name to register the check under. Defaults to None.

        Raises:
            ValueError: If check function is not callable or name already registered.

        Example:
            ```py
            >>> def check_email_format(df):
            ...     warnings = []
            ...     for col in df.select_dtypes(include="object").columns:
            ...         if "email" in col.lower():
            ...             # Simple regex check for email format
            ...             pass
            ...     return warnings
            >>> df.lint.register_check(check_email_format, name="email_format")
            ```
        """
        if not callable(check_func):
            raise ValueError("check_func must be a callable function.")

        check_name = name or check_func.__name__

        if check_name in self._custom_checks:
            raise ValueError(f"A check with the name '{check_name}' is already registered.")

        self._custom_checks[check_name] = check_func

    def unregister_check(self, name: str) -> None:
        """Remove a custom check function by name.

        Args:
            name (str): Name of the custom check to remove.

        Raises:
            ValueError: If the custom check is not registered.

        Example:
            ```py
            >>> df.lint.unregister_check("email_format")
            ```
        """
        if name not in self._custom_checks:
            raise ValueError(f"Custom check '{name}' is not registered.")

        del self._custom_checks[name]

    def list_custom_checks(self) -> List[str]:
        """List all registered custom check names.

        Returns:
            List[str]: Names of registered custom checks.
        """
        return list(self._custom_checks.keys())

    def report(
        self,
        checks_to_run: Optional[Union[List[str], str]] = None,
        outlier_threshold: float = 1.5,
        skewness_threshold: float = 1.0,
        rare_category_threshold: float = 0.01,
        unique_column_threshold: float = 0.95,
        cardinality_high_threshold: int = 50,
        cardinality_low_threshold: int = 2,
        string_length_threshold: float = 3.0,
        negative_value_columns: Optional[List[str]] = None,
        zero_inflation_threshold: float = 0.5,
        future_date_columns: Optional[List[str]] = None,
        future_date_reference: Optional[str] = None,
        special_chars_threshold: float = 0.1,
        threshold_years: float = 50,
        correlation_threshold: float = 0.95,
        foreign_key_mappings: Optional[Dict[str, Union[pd.DataFrame, Tuple[pd.DataFrame, str]]]] = None,
        report_format: str = "text",
        output: Optional[str] = None,
        return_dict: bool = False,
        n_jobs: int = 1,
        backend: str = "multiprocessing",
        min_checks_for_parallel: int = 3,
    ) -> Union[str, Dict[str, Any]]:
        """Generate a comprehensive quality report for the DataFrame.

        Args:
            checks_to_run (Optional[Union[List[str], str]], optional): Specific checks to run.
                Options: 'missing', 'duplicates', 'mixed_types', 'whitespace', 'constant',
                'unique', 'outliers', 'missing_patterns', 'case', 'cardinality', 'skewness',
                'duplicate_columns', 'type_consistency', 'negative', 'rare_categories',
                'date_format', 'string_length', 'zero_inflation', 'future_dates',
                'special_chars', 'date_anomalies', 'correlation', 'foreign_keys'. Use 'all' to run all checks. Defaults to None.
            outlier_threshold (float, optional): Outlier detection threshold using the IQR method. Defaults to 1.5.
            skewness_threshold (float, optional): Threshold for skewness detection. Defaults to 1.0.
            rare_category_threshold (float, optional): Minimum proportion for rare categories. Defaults to 0.01.
            unique_column_threshold (float, optional): Threshold for identifying unique columns. Defaults to 0.95.
            cardinality_high_threshold (int, optional): High cardinality threshold. Defaults to 50.
            cardinality_low_threshold (int, optional): Low cardinality threshold. Defaults to 2.
            string_length_threshold (float, optional): Threshold for identifying string length outliers. Defaults to 3.0.
            negative_value_columns (Optional[List[str]], optional): Specific columns to check for negative values. Defaults to None.
            zero_inflation_threshold (float, optional): Minimum proportion of zeros to flag. Defaults to 0.5.
            future_date_columns (Optional[List[str]], optional): Specific columns to check for future dates. Defaults to None.
            future_date_reference (Optional[str], optional): Reference date for future date check (YYYY-MM-DD). Defaults to None (today).
            special_chars_threshold (float, optional): Minimum proportion of values with special characters. Defaults to 0.1.
            threshold_years (float, optional): Maximum acceptable date range in years. Columns with date ranges exceeding will be flagged. Defaults to 50.
            correlation_threshold (float, optional): Threshold for flagging highly correlated columns. Defaults to 0.95.
            foreign_key_mappings (Optional[Dict[str, Union[pd.DataFrame, Tuple[pd.DataFrame, str]]]], optional):
                Mappings for referential integrity checks. Key: foreign key column in the DataFrame.
                Value: either parent DataFrame (assumes first column is referenced) or tuple of (parent_df, parent_column_name). Defaults to None.
            report_format (str, optional): Output format. Options: 'text', 'html', 'json', 'csv'. Defaults to 'text'.
            output (Optional[str], optional): File path to save the report. If None, returns as string. Defaults to None.
            return_dict (bool, optional): If True, returns structured dictionary instead of formatted string. Defaults to False.
            n_jobs (int, optional): Number of parallel workers. -1: Use all cores, 1: Serial execution, n > 1: Use n workers. Defaults to 1.
            backend (str, optional): Parallelisation backend. Options: 'multiprocessing', 'threading', 'joblib'. Defaults to 'multiprocessing'.
            min_checks_for_parallel (int, optional): Minimum number of checks required to trigger parallel execution. Defaults to 3.

        Raises:
            ValueError: If invalid check names are provided or invalid format specified.

        Returns:
            Union[str, Dict[str, Any]]: A comprehensive quality report in the specified format,
                or a structured dictionary if return_dict=True.

        Example:
            ```py
            >>> # Text report
            >>> report = df.lint.report()

            >>> # HTML report
            >>> df.lint.report(report_format='html', output='report.html')

            >>> # JSON export
            >>> df.lint.report(report_format='json', output='report.json')

            >>> # CSV export
            >>> df.lint.report(report_format='csv', output='issues.csv')

            >>> # Get structured data
            >>> data = df.lint.report(return_dict=True)

            >>> # Parallel execution with all cores
            >>> df.lint.report(n_jobs=-1)

            >>> # Parallel execution with specific backend
            >>> df.lint.report(n_jobs=4, backend='threading')
            ```
        """
        valid_formats = ["text", "html", "json", "csv"]
        if report_format not in valid_formats:
            raise ValueError(f"Invalid format '{report_format}'. Valid options: {valid_formats}")

        if self._df.empty:
            if return_dict:
                return {"shape": [0, 0], "issues": [], "issue_count": 0}

            empty_message = "The DataFrame is empty. No checks run."
            if report_format == "text":
                result = f"--- LintData Quality Report ---\n{empty_message}"
            elif report_format == "html":
                result = HTMLReportFormatter.generate((0, 0), [])
            elif report_format == "json":
                result = json.dumps({"shape": [0, 0], "issues": [], "issue_count": 0}, indent=2)
            elif report_format == "csv":
                from io import StringIO

                output_io = StringIO()
                writer = csv.writer(output_io)
                writer.writerow(["check", "column", "severity", "message"])
                result = output_io.getvalue()

            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)  # pyright: ignore[reportPossiblyUnboundVariable]

            return result  # pyright: ignore[reportPossiblyUnboundVariable]

        check_functions: List[Callable] = []
        check_kwargs: Dict[str, Dict[str, Any]] = {}

        available_checks = {
            "missing": (checks.check_missing_values, {}),
            "duplicates": (checks.check_duplicate_rows, {}),
            "mixed_types": (checks.check_mixed_types, {}),
            "whitespace": (checks.check_whitespace, {}),
            "constant": (checks.check_constant_columns, {}),
            "unique": (checks.check_unique_columns, {"threshold": unique_column_threshold}),
            "outliers": (checks.check_outliers, {"threshold": outlier_threshold}),
            "missing_patterns": (checks.check_missing_patterns, {}),
            "case": (checks.check_case_consistency, {}),
            "cardinality": (
                checks.check_cardinality,
                {"high_threshold": cardinality_high_threshold, "low_threshold": cardinality_low_threshold},
            ),
            "skewness": (checks.check_skewness, {"threshold": skewness_threshold}),
            "duplicate_columns": (checks.check_duplicate_columns, {}),
            "type_consistency": (checks.check_data_type_consistency, {}),
            "negative": (checks.check_negative_values, {"columns": negative_value_columns}),
            "rare_categories": (checks.check_rare_categories, {"threshold": rare_category_threshold}),
            "date_format": (checks.check_date_format_consistency, {}),
            "string_length": (checks.check_string_length_outliers, {"threshold": string_length_threshold}),
            "zero_inflation": (checks.check_zero_inflation, {"threshold": zero_inflation_threshold}),
            "future_dates": (
                checks.check_future_dates,
                {"columns": future_date_columns, "reference_date": future_date_reference},
            ),
            "special_chars": (checks.check_special_characters, {"threshold": special_chars_threshold}),
            "date_anomalies": (
                checks.check_date_range_anomalies,
                {"columns": future_date_columns, "threshold_years": threshold_years},
            ),
            "correlation": (checks.check_correlation_warnings, {"threshold": correlation_threshold}),
            "foreign_keys": (checks.check_referential_integrity, {"foreign_keys": foreign_key_mappings or {}}),
        }

        if checks_to_run is None:
            checks_to_execute = list(available_checks.keys())
        else:
            if isinstance(checks_to_run, str) and checks_to_run == "all":
                checks_to_execute = list(available_checks.keys())
            else:
                checks_to_execute = checks_to_run if isinstance(checks_to_run, list) else [checks_to_run]

            invalid_checks = [c for c in checks_to_execute if c not in available_checks]
            if invalid_checks:
                raise ValueError(f"Invalid check(s): {invalid_checks}. Valid options: {list(available_checks.keys())}")

        for check_name in checks_to_execute:
            func, kwargs = available_checks[check_name]
            check_functions.append(func)
            check_kwargs[func.__name__] = kwargs

        executor = ParallelExecutor(n_jobs=n_jobs, backend=backend, min_checks_for_parallel=min_checks_for_parallel)
        results = executor.execute_checks(check_functions, self._df, check_kwargs)

        all_warnings: List[str] = []
        for func in check_functions:
            all_warnings.extend(results[func.__name__])

        for check_name, check_func in self._custom_checks.items():
            try:
                custom_warnings = check_func(self._df)
                if isinstance(custom_warnings, list):
                    all_warnings.extend(custom_warnings)
                else:
                    all_warnings.append(f"[Custom Check Error] '{check_name}' did not return a list of warnings.")
            except Exception as e:
                all_warnings.append(f"[Custom Check Error] '{check_name}' raised an exception: {e!s}")

        if return_dict:
            structured_data = self._format_as_dict(all_warnings)
            return structured_data

        if report_format == "text":
            report_lines = ["--- LintData Quality Report ---"]
            report_lines.append(f"Shape: {self._df.shape}")
            report_lines.append("\nRunning checks...")

            if not all_warnings:
                report_lines.append("No issues found. DataFrame looks good!")
            else:
                report_lines.append(f"Found {len(all_warnings)} issue(s):")
                for i, warning in enumerate(all_warnings, 1):
                    report_lines.append(f"  {i}. {warning}")

            report_lines.append("\n--- End of Report ---")
            result = "\n".join(report_lines)

        elif report_format == "html":
            result = HTMLReportFormatter.generate(self._df.shape, all_warnings)

        elif report_format == "json":
            structured_data = self._format_as_dict(all_warnings)
            result = json.dumps(structured_data, indent=2)

        elif report_format == "csv":
            result = self._format_as_csv(all_warnings)

        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(result)  # pyright: ignore[reportPossiblyUnboundVariable]

        return result  # pyright: ignore[reportPossiblyUnboundVariable]

    def _format_as_dict(self, warnings: List[str]) -> Dict[str, Any]:
        """Convert warnings to structured dictionary.

        Args:
            warnings: List of warning strings

        Returns:
            Dict with shape, issues list, and metadata
        """
        issues = []
        for warning in warnings:
            parsed = self._parse_warning(warning)
            issues.append(parsed)

        return {"shape": list(self._df.shape), "issue_count": len(warnings), "issues": issues}

    def _parse_warning(self, warning: str) -> Dict[str, Any]:
        """Parse a warning string into structured data.

        Args:
            warning: Warning string like "[Missing Values] Column 'age': 5 missing values"

        Returns:
            Dict with check, column, severity, and message
        """
        # Extract check type from [brackets]
        if "]" in warning:
            check_type = warning.split("]")[0].replace("[", "").strip()
            message = warning.split("]", 1)[1].strip()
        else:
            check_type = "Unknown"
            message = warning

        # Extract column name if present
        column = None
        column_match = re.search(r"Column (['\"])(.*?)\1", message)
        column = column_match.group(2) if column_match else None

        # Determine severity
        severity = self._get_severity(warning)

        return {"check": check_type, "column": column, "severity": severity, "message": message}

    def _get_severity(self, warning: str) -> str:
        """Determine severity level from warning text.

        Args:
            warning: Warning string

        Returns:
            'high', 'medium', or 'low'
        """
        warning_lower = warning.lower()

        high_indicators = [
            "missing values",
            "duplicate rows",
            "mixed types",
            "future dates",
            "negative values",
        ]

        medium_indicators = [
            "outliers",
            "whitespace",
            "case consistency",
            "special characters",
            "date format",
        ]

        if any(indicator in warning_lower for indicator in high_indicators):
            return "high"
        elif any(indicator in warning_lower for indicator in medium_indicators):
            return "medium"
        else:
            return "low"

    def _format_as_csv(self, warnings: List[str]) -> str:
        """Format warnings as CSV string.

        Args:
            warnings: List of warning strings

        Returns:
            CSV formatted string
        """
        from io import StringIO

        output = StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(["check", "column", "severity", "message"])

        # Write data
        for warning in warnings:
            parsed = self._parse_warning(warning)
            writer.writerow([parsed["check"], parsed["column"] or "N/A", parsed["severity"], parsed["message"]])

        return output.getvalue()
