# Changelog

All notable changes to this project will be documented in this file.

## [Released] - 2025-11-27

## [1.1.0] - 2025-12-02 - 2025-12-05

### Added

- Add ParallelExecutor for parallel processing with multiprocessing, threading and joblib backends.
- Added tests for parallel execution in `tests/test_parallel.py`.

### Changed

- Updated `report()` method to include `backend` and `n_jobs` parameters for parallel execution control.

## [1.0.1] - 2025-11-27

### Added

- CI workflow to automatically publish new releases to PyPI on tag creation.

## [1.0.0] - 2025-11-27

### Added

- `check_referential_integrity`: New check to identify foreign key violations between DataFrames.

### Changed

- Updated `report()` method to include `foreign_key_mappings` parameter for referential integrity checks.

This marks the first stable release of LintData.

## [0.9.0] - 2025-11-26 - 2025-11-27

### Added

- `check_correlation_warnings`: New check to identify pairs of numerical columns with high correlation above a specified threshold.
- Added documentation via MkDocs and MkDocs Material theme. Using mkdocstrings-python for API reference generation.

## [0.8.0] - 2025-11-26

### Added

- `check_date_range_anomalies`: New check to identify date columns with values that fall outside a specified range (e.g., too old or too recent).
- Custom Check API: Users can now register their own custom checks using the `register_check` method on the `lint` accessor. Custom checks should be functions that accept a DataFrame and return a list of warning strings.
- Support for custom checks in the main `report()` method, allowing users to include their custom checks in the data quality audit.
- Users can also unregister custom checks using the `unregister_check` method on the `lint` accessor.

### Changed

- Added `threshold_years` parameter to `check_date_range_anomalies` to specify the number of years for anomaly detection.
- Optimised performance of `check_duplicate_rows` to handle large DataFrames with many rows more efficiently.
- Optimised performance of `check_mixed_types` using vectorised operations to reduce processing time on large DataFrames.
- Optimised performance of `check_whitespace` by leveraging pandas string methods for faster detection of whitespace issues.
- Optimised performance of `check_outliers` with reduced memory usage/allocation.

## [0.7.0] - 2025-11-21

### Added

- `check_zero_inflation`: New check to identify columns with a high proportion of zero values.
- `check_future_dates`: New check to identify dates that are in the future compared to a reference date.
- `check_special_characters`: New check to identify unusual or special characters in string columns.
- Integrate HTML outputs with existing reporting system.
- JSON, CSV, Dict outputs integrated with existing reporting system.
- New helper methods to parse warning strings into structured data.
- All export formats support the full configuration system (custom thresholds, check selection)

### Changed

- Enhanced `report()` method to include HTML output format alongside existing formats (text).
- Updated `report()` to add `output` parameter to specify output file path for saving reports; output format is now specified via the `report_format` parameter (e.g., `text`, `html`)
- Default is still `text` to maintain backward compatibility.

## [0.6.0] - 2025-11-13

### Added

- `check_negative_values`: New check to identify negative values in numerical columns.
- `check_rare_categories`: New check to detect infrequent categories in categorical columns.
- `check_date_format_consistency`: New check to identify inconsistent date formats within date columns.
- `check_string_length_outliers`: New check to identify string length outliers in text columns.
- Configuration system: Users can now customise thresholds and select specific checks to run.
- `report()` method now accepts parameters to:
  - Select specific checks via `checks_to_run` parameter
  - Customise outlier detection thresholds via `outlier_thresholds` parameter
  - Customise rare category frequency threshold via `rare_category_threshold` parameter
  - Customise skewness threshold via `skewness_threshold` parameter
  - Customise unique column threshold via `unique_column_threshold` parameter
  - Customise cardinality threshold via `cardinality_high_threshold` and `cardinality_low_threshold` parameters
  - Customise string length outlier thresholds via `string_length_threshold` parameter
  - Customise which columns to check for negative values via `negative_value_columns` parameter

## [0.5.0] - 2025-11-03 - 2025-11-06

### Added

- `check_cardinality`: New check to identify columns with high cardinality.
- `check_skewness`: New check to assess skewness in numerical columns.
- `check_duplicate_columns`: New check to identify duplicate columns in DataFrames.
- `check_data_type_consistency`: New check to identify columns with inconsistent data types.

## [0.4.0] - 2025-10-31 - 2025-11-02

### Added

- `check_outliers`: New check to identify outliers using the IQR method.
- `check_missing_patterns`: New check to detect common missing value patterns in DataFrames.
- `check_case_consistency`: New check to identify inconsistencies in string casing within columns.

## [0.3.0] - 2025-10-31

### Added

- `check_constant_columns`: New check to identify columns with constant values.
- `check_unique_columns`: New check to identify columns where all values are unique.

## [0.2.0] - 2025-10-27 - 2025-10-31

### Added

- `check_duplicate_rows`: New check to identify duplicate rows in DataFrames.
- `check_mixed_types`: New check to detect columns with mixed data types.
- `check_whitespace`: New check to identify leading or trailing whitespace in string columns.

## [0.1.0] - 2025-10-24

### Added

- Initial release of LintData.
- Basic check for missing values in DataFrames.
