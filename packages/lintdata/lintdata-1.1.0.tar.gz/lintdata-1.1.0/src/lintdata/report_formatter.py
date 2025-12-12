import html
from typing import List, Tuple


class HTMLReportFormatter:
    """Format LintData reports as HTML with styling."""

    @staticmethod
    def generate(df_shape: Tuple[int, int], warnings: List[str]) -> str:
        """Generate an HTML report from warnings.

        Args:
            df_shape: Tuple of (rows, columns) from DataFrame.shape
            warnings: List of warning strings from checks

        Returns:
            str: Complete HTML document as string
        """
        rows, cols = df_shape

        # Generate warnings HTML
        if not warnings:
            warnings_html = '<div class="success">✓ No issues found. DataFrame looks good!</div>'
        else:
            warnings_items = ""
            for i, warning in enumerate(warnings, 1):
                # Determine severity from warning type
                severity = HTMLReportFormatter._get_severity(warning)
                warnings_items += (
                    f'<div class="warning {severity}"><span class="number">{i}.</span> {html.escape(warning)}</div>\n'
                )

            warnings_html = f"""
            <div class="summary">Found {len(warnings)} issue(s):</div>
            <div class="warnings-list">
                {warnings_items}
            </div>
            """

        # Complete HTML document
        html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LintData Quality Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 10px;
        }}

        .header .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .content {{
            padding: 40px;
        }}

        .metadata {{
            display: flex;
            gap: 30px;
            margin-bottom: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }}

        .metadata-item {{
            flex: 1;
        }}

        .metadata-label {{
            font-size: 0.85em;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }}

        .metadata-value {{
            font-size: 1.5em;
            font-weight: 600;
            color: #2c3e50;
        }}

        .summary {{
            font-size: 1.2em;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 20px;
        }}

        .success {{
            background: #d4edda;
            color: #155724;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #28a745;
            font-size: 1.1em;
            font-weight: 500;
        }}

        .warnings-list {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .warning {{
            padding: 16px;
            border-radius: 8px;
            border-left: 4px solid;
            display: flex;
            align-items: flex-start;
            gap: 12px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .warning:hover {{
            transform: translateX(4px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}

        .warning .number {{
            font-weight: 700;
            min-width: 30px;
        }}

        .warning.high {{
            background: #f8d7da;
            border-left-color: #dc3545;
            color: #721c24;
        }}

        .warning.medium {{
            background: #fff3cd;
            border-left-color: #ffc107;
            color: #856404;
        }}

        .warning.low {{
            background: #d1ecf1;
            border-left-color: #17a2b8;
            color: #0c5460;
        }}

        .footer {{
            background: #f8f9fa;
            padding: 20px 40px;
            text-align: center;
            color: #6c757d;
            font-size: 0.9em;
        }}

        @media (max-width: 768px) {{
            .metadata {{
                flex-direction: column;
                gap: 15px;
            }}

            .header h1 {{
                font-size: 2em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 LintData Quality Report</h1>
            <div class="subtitle">Automated Data Quality Audit</div>
        </div>

        <div class="content">
            <div class="metadata">
                <div class="metadata-item">
                    <div class="metadata-label">Rows</div>
                    <div class="metadata-value">{rows:,}</div>
                </div>
                <div class="metadata-item">
                    <div class="metadata-label">Columns</div>
                    <div class="metadata-value">{cols}</div>
                </div>
                <div class="metadata-item">
                    <div class="metadata-label">Issues Found</div>
                    <div class="metadata-value">{len(warnings)}</div>
                </div>
            </div>

            {warnings_html}
        </div>

        <div class="footer">
            Generated by LintData • Data Quality Analysis Tool
        </div>
    </div>
</body>
</html>
"""
        return html_doc

    @staticmethod
    def _get_severity(warning: str) -> str:
        """Determine severity level from warning text.

        Args:
            warning: Warning string

        Returns:
            str: 'high', 'medium', or 'low'
        """
        warning_lower = warning.lower()

        # High severity indicators
        high_indicators = [
            "missing values",
            "duplicate rows",
            "mixed types",
            "future dates",
            "negative values",
        ]

        # Medium severity indicators
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
