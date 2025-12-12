# LintData

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/lintdata)](https://pypi.org/project/lintdata) [![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/) [![Licence: MIT](https://img.shields.io/badge/Licence-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![CI](https://github.com/patelheet30/lintdata/actions/workflows/ci.yml/badge.svg)](https://github.com/patelheet30/lintdata/actions/workflows/ci.yml)

</div>
A "linter" for pandas DataFrames to automate data quality audits.

## Installation

You can install LintData via pip:

```bash
pip install lintdata
```

Via UV:

```bash
uv add lintdata
```

Or install from source:

```bash
git clone https://github.com/patelheet30/lintdata.git
cd lintdata
pip install -e .
```

## Features

✅ **20+ Data Quality Checks** - Missing values, duplicates, outliers, type consistency, and more  
✅ **Zero Configuration** - Works out of the box with sensible defaults  
✅ **Highly Configurable** - Customize thresholds and select specific checks  
✅ **Multiple Export Formats** - Text, HTML, JSON, and CSV reports  
✅ **Custom Checks API** - Extend with your own validation logic  
✅ **Pandas Native** - Integrates seamlessly via `.lint` accessor

## Quick Start

```python
import pandas as pd
import lintdata

# Load your DataFrame
df = pd.read_csv("your_data.csv")

# Run quality checks
report = df.lint.report()
print(report)
```

**Example Output:**

```
--- LintData Quality Report ---
Shape: (1000, 8)

Running Checks:
Found 5 issue(s):
  1. [Missing Values] Column 'age': 45 missing values (4.5%)
  2. [Duplicates] Found 12 duplicate rows (1.2% of data)
  3. [Outliers] Column 'salary': 8 potential outliers detected (IQR method)
  4. [Mixed Types] Column 'phone' contains both numeric and string values
  5. [High Cardinality] Column 'user_id' has 987 unique values (98.7%)

--- End of Report ---
```

## Available Checks

LintData includes 22+ built-in checks across multiple categories:

- **Missing Data**: Missing values, missing patterns
- **Duplicates**: Duplicate rows, duplicate columns
- **Data Types**: Mixed types, type consistency
- **Statistical**: Outliers, skewness, correlation warnings
- **Categorical**: Cardinality, rare categories, case consistency
- **Numerical**: Negative values, zero inflation
- **Strings**: Whitespace, special characters, length outliers
- **Dates**: Format consistency, future dates, date range anomalies
- **Multi-table**: Referential integrity (foreign key validation)

## Export Formats

Save reports in multiple formats:

```python
# HTML report with visualizations
df.lint.report(report_format='html', output='report.html')

# JSON for programmatic access
df.lint.report(report_format='json', output='report.json')

# CSV for spreadsheet analysis
df.lint.report(report_format='csv', output='issues.csv')
```

## Custom Checks

Extend LintData with your own validation logic:

```python
def check_email_format(df):
    """Validate email addresses."""
    warnings = []
    for col in df.select_dtypes(include='object').columns:
        if 'email' in col.lower():
            invalid = df[~df[col].str.contains('@', na=False)]
            if len(invalid) > 0:
                warnings.append(f"[Email] Column '{col}': {len(invalid)} invalid emails")
    return warnings

# Register and use
df.lint.register_check(check_email_format)
df.lint.report()
```

## Documentation

Full documentation available at: [LintData Documentation](https://lintdata.patelheet.com)

## Issues and Support

For general help or to report bugs, please open an issue on GitHub: [LintData Issues](https://github.com/patelheet30/lintdata/issues).

If you have questions or need assistance, feel free to reach out via Discord: patelheet30
