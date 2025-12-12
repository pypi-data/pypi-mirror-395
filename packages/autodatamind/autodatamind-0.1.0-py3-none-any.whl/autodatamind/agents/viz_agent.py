"""
Visualization Agent - Automatic Charts & Dashboards
====================================================

Automatically creates beautiful visualizations and HTML dashboards.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Union, Optional, List
import os
from datetime import datetime
from autodatamind.core.reader import read_data
from autodatamind.core.cleaner import autoclean
from autodatamind.core.utils import get_numeric_columns, get_categorical_columns


def dashboard(data: Union[str, pd.DataFrame],
              output_file: Optional[str] = None,
              auto_clean: bool = True,
              title: str = "AutoDataMind Dashboard") -> str:
    """
    Automatically generate interactive HTML dashboard.
    
    Parameters
    ----------
    data : str or DataFrame
        Path to file or DataFrame
    output_file : str, optional
        Output HTML file path. If None, generates automatic name.
    auto_clean : bool
        Automatically clean data
    title : str
        Dashboard title
    
    Returns
    -------
    str
        Path to generated HTML file
    
    Examples
    --------
    >>> import autodatamind as adm
    >>> adm.dashboard("sales.csv")
    >>> adm.dashboard(df, output_file="my_dashboard.html")
    """
    # Load data
    df = read_data(data)
    
    # Auto-clean if requested
    if auto_clean:
        df = autoclean(df, verbose=False)
    
    # Generate output filename
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"autodatamind_dashboard_{timestamp}.html"
    
    # Create dashboard HTML
    html = _generate_dashboard_html(df, title)
    
    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Dashboard created: {output_file}")
    return output_file


def _generate_dashboard_html(df: pd.DataFrame, title: str) -> str:
    """Generate complete HTML dashboard."""
    
    # Get data insights
    overview = _get_dashboard_overview(df)
    numeric_cols = get_numeric_columns(df)
    categorical_cols = get_categorical_columns(df)
    
    # Build HTML
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        .header h1 {{
            color: #667eea;
            margin-bottom: 10px;
        }}
        .header p {{
            color: #666;
            font-size: 14px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .stat-card h3 {{
            font-size: 36px;
            color: #667eea;
            margin-bottom: 10px;
        }}
        .stat-card p {{
            color: #666;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .section {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #f8f9fa;
            color: #667eea;
            font-weight: 600;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }}
        .badge-numeric {{
            background: #e3f2fd;
            color: #1976d2;
        }}
        .badge-categorical {{
            background: #fff3e0;
            color: #f57c00;
        }}
        .badge-datetime {{
            background: #f3e5f5;
            color: #7b1fa2;
        }}
        .footer {{
            text-align: center;
            color: white;
            margin-top: 30px;
            padding: 20px;
        }}
        .footer p {{
            margin: 5px 0;
            opacity: 0.9;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 {title}</h1>
            <p>Generated by AutoDataMind on {datetime.now().strftime("%B %d, %Y at %H:%M")}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>{overview['n_rows']:,}</h3>
                <p>Total Rows</p>
            </div>
            <div class="stat-card">
                <h3>{overview['n_columns']}</h3>
                <p>Total Columns</p>
            </div>
            <div class="stat-card">
                <h3>{overview['n_numeric']}</h3>
                <p>Numeric Columns</p>
            </div>
            <div class="stat-card">
                <h3>{overview['n_categorical']}</h3>
                <p>Categorical Columns</p>
            </div>
            <div class="stat-card">
                <h3>{overview['memory_mb']:.2f} MB</h3>
                <p>Memory Usage</p>
            </div>
            <div class="stat-card">
                <h3>{overview['missing_pct']:.1f}%</h3>
                <p>Missing Data</p>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 Column Information</h2>
            <table>
                <thead>
                    <tr>
                        <th>Column Name</th>
                        <th>Type</th>
                        <th>Unique Values</th>
                        <th>Missing</th>
                        <th>Sample Values</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    # Add column information
    for col in df.columns:
        dtype = df[col].dtype
        unique = df[col].nunique()
        missing = df[col].isnull().sum()
        missing_pct = (missing / len(df)) * 100
        
        # Determine badge type
        if dtype in [np.float64, np.int64]:
            badge = '<span class="badge badge-numeric">Numeric</span>'
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            badge = '<span class="badge badge-datetime">DateTime</span>'
        else:
            badge = '<span class="badge badge-categorical">Categorical</span>'
        
        # Get sample values
        sample_values = df[col].dropna().head(3).tolist()
        sample_str = ", ".join([str(v)[:20] for v in sample_values])
        
        html += f"""
                    <tr>
                        <td><strong>{col}</strong></td>
                        <td>{badge}</td>
                        <td>{unique:,}</td>
                        <td>{missing} ({missing_pct:.1f}%)</td>
                        <td style="color: #666; font-size: 12px;">{sample_str}</td>
                    </tr>
        """
    
    html += """
                </tbody>
            </table>
        </div>
    """
    
    # Add numeric statistics
    if numeric_cols:
        html += """
        <div class="section">
            <h2>🔢 Numeric Statistics</h2>
            <table>
                <thead>
                    <tr>
                        <th>Column</th>
                        <th>Mean</th>
                        <th>Median</th>
                        <th>Std Dev</th>
                        <th>Min</th>
                        <th>Max</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for col in numeric_cols:
            stats = df[col].describe()
            html += f"""
                    <tr>
                        <td><strong>{col}</strong></td>
                        <td>{stats['mean']:.2f}</td>
                        <td>{stats['50%']:.2f}</td>
                        <td>{stats['std']:.2f}</td>
                        <td>{stats['min']:.2f}</td>
                        <td>{stats['max']:.2f}</td>
                    </tr>
            """
        
        html += """
                </tbody>
            </table>
        </div>
        """
    
    # Add categorical value counts
    if categorical_cols:
        html += """
        <div class="section">
            <h2>📑 Categorical Distribution</h2>
        """
        
        for col in categorical_cols[:5]:  # Limit to 5
            value_counts = df[col].value_counts().head(10)
            html += f"""
            <h3 style="color: #666; margin: 20px 0 10px 0;">{col}</h3>
            <table>
                <thead>
                    <tr>
                        <th>Value</th>
                        <th>Count</th>
                        <th>Percentage</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            for val, count in value_counts.items():
                pct = (count / len(df)) * 100
                html += f"""
                    <tr>
                        <td>{val}</td>
                        <td>{count:,}</td>
                        <td>{pct:.1f}%</td>
                    </tr>
                """
            
            html += """
                </tbody>
            </table>
            """
        
        html += """
        </div>
        """
    
    # Footer
    html += f"""
        <div class="footer">
            <p><strong>AutoDataMind</strong> - Your Native Automated Data & ML Engine</p>
            <p>Made with ❤️ by Idriss Olivier Bado</p>
        </div>
    </div>
</body>
</html>
    """
    
    return html


def _get_dashboard_overview(df: pd.DataFrame) -> dict:
    """Get dashboard overview statistics."""
    return {
        'n_rows': len(df),
        'n_columns': len(df.columns),
        'n_numeric': len(get_numeric_columns(df)),
        'n_categorical': len(get_categorical_columns(df)),
        'memory_mb': df.memory_usage(deep=True).sum() / (1024 * 1024),
        'missing_pct': (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100,
    }


class VizAgent:
    """
    Visualization Agent for creating charts and dashboards.
    """
    
    def __init__(self):
        self.data = None
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def create_dashboard(self, data: Union[str, pd.DataFrame], **kwargs) -> str:
        """Create HTML dashboard."""
        return dashboard(data, **kwargs)
