"""
Profile Agent - Intelligent Data Profiling
===========================================

Automatically analyzes data and generates insights.
"""

import pandas as pd
import numpy as np
from typing import Union, Dict, Any
from autodatamind.core.reader import read_data
from autodatamind.core.cleaner import autoclean
from autodatamind.core.utils import get_numeric_columns, get_categorical_columns


def analyze(data: Union[str, pd.DataFrame],
            auto_clean: bool = True,
            verbose: bool = True) -> Dict[str, Any]:
    """
    Automatically analyze data and generate insights.
    
    Parameters
    ----------
    data : str or DataFrame
        Path to file or DataFrame
    auto_clean : bool
        Automatically clean data before analysis
    verbose : bool
        Print insights
    
    Returns
    -------
    dict
        Complete analysis results
    
    Examples
    --------
    >>> import autodatamind as adm
    >>> results = adm.analyze("sales.csv")
    """
    # Load data
    df = read_data(data)
    
    # Auto-clean if requested
    if auto_clean:
        df = autoclean(df, verbose=False)
    
    # Run analysis
    results = {
        'overview': _get_overview(df),
        'statistics': _get_statistics(df),
        'correlations': _get_correlations(df),
        'insights': _generate_insights(df),
        'recommendations': _generate_recommendations(df),
    }
    
    # Print summary
    if verbose:
        _print_analysis_summary(results)
    
    return results


def _get_overview(df: pd.DataFrame) -> Dict[str, Any]:
    """Get data overview."""
    return {
        'n_rows': len(df),
        'n_columns': len(df.columns),
        'n_numeric': len(get_numeric_columns(df)),
        'n_categorical': len(get_categorical_columns(df)),
        'memory_mb': float(df.memory_usage(deep=True).sum() / (1024 * 1024)),
        'duplicates': int(df.duplicated().sum()),
        'total_missing': int(df.isnull().sum().sum()),
    }


def _get_statistics(df: pd.DataFrame) -> Dict[str, Dict]:
    """Get statistics for all columns."""
    stats = {}
    
    for col in df.columns:
        col_stats = {
            'type': str(df[col].dtype),
            'count': int(df[col].count()),
            'missing': int(df[col].isnull().sum()),
            'unique': int(df[col].nunique()),
        }
        
        if df[col].dtype in [np.float64, np.int64]:
            col_stats.update({
                'mean': float(df[col].mean()),
                'std': float(df[col].std()),
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'median': float(df[col].median()),
            })
        
        stats[col] = col_stats
    
    return stats


def _get_correlations(df: pd.DataFrame) -> Dict[str, Any]:
    """Get correlation analysis."""
    numeric_cols = get_numeric_columns(df)
    
    if len(numeric_cols) < 2:
        return {'available': False}
    
    corr_matrix = df[numeric_cols].corr()
    
    # Find strong correlations
    strong_corr = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_val = corr_matrix.iloc[i, j]
            if abs(corr_val) > 0.7:
                strong_corr.append({
                    'feature1': corr_matrix.columns[i],
                    'feature2': corr_matrix.columns[j],
                    'correlation': float(corr_val),
                })
    
    return {
        'available': True,
        'strong_correlations': strong_corr,
        'matrix': corr_matrix.to_dict(),
    }


def _generate_insights(df: pd.DataFrame) -> list:
    """Generate automatic insights."""
    insights = []
    
    # Dataset size insight
    n_rows = len(df)
    if n_rows < 100:
        insights.append(f"⚠️  Small dataset ({n_rows} rows) - results may not be robust")
    elif n_rows > 100000:
        insights.append(f"✓ Large dataset ({n_rows:,} rows) - good for analysis")
    
    # Missing data insight
    missing_pct = df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100
    if missing_pct > 10:
        insights.append(f"⚠️  High missing data ({missing_pct:.1f}%) - consider imputation")
    elif missing_pct > 0:
        insights.append(f"ℹ️  Some missing data ({missing_pct:.1f}%) - handled automatically")
    
    # Imbalance insight
    categorical_cols = get_categorical_columns(df)
    for col in categorical_cols[:3]:  # Check first 3
        value_counts = df[col].value_counts()
        if len(value_counts) > 1:
            imbalance_ratio = value_counts.iloc[0] / value_counts.iloc[1]
            if imbalance_ratio > 10:
                insights.append(f"⚠️  Imbalanced '{col}' column (ratio: {imbalance_ratio:.1f}:1)")
    
    # High cardinality insight
    for col in categorical_cols:
        n_unique = df[col].nunique()
        if n_unique > len(df) * 0.9:
            insights.append(f"ℹ️  '{col}' has very high cardinality ({n_unique} unique values)")
    
    return insights


def _generate_recommendations(df: pd.DataFrame) -> list:
    """Generate action recommendations."""
    recommendations = []
    
    # Duplicate check
    n_duplicates = df.duplicated().sum()
    if n_duplicates > 0:
        recommendations.append(f"Remove {n_duplicates} duplicate rows")
    
    # Missing data
    cols_with_missing = [col for col in df.columns if df[col].isnull().any()]
    if cols_with_missing:
        recommendations.append(f"Handle missing values in {len(cols_with_missing)} columns")
    
    # Feature engineering
    numeric_cols = get_numeric_columns(df)
    if len(numeric_cols) > 0:
        recommendations.append("Consider feature scaling for numeric columns")
    
    categorical_cols = get_categorical_columns(df)
    if len(categorical_cols) > 0:
        recommendations.append("Consider encoding categorical variables")
    
    # Outlier detection
    if len(numeric_cols) > 0:
        recommendations.append("Check for outliers in numeric columns")
    
    return recommendations


def _print_analysis_summary(results: Dict[str, Any]):
    """Print analysis summary."""
    print("\n" + "=" * 70)
    print("📊 AUTODATAMIND ANALYSIS")
    print("=" * 70)
    
    # Overview
    overview = results['overview']
    print(f"\n📈 Dataset Overview:")
    print(f"  • Rows: {overview['n_rows']:,}")
    print(f"  • Columns: {overview['n_columns']}")
    print(f"  • Numeric: {overview['n_numeric']}, Categorical: {overview['n_categorical']}")
    print(f"  • Memory: {overview['memory_mb']:.2f} MB")
    
    if overview['duplicates'] > 0:
        print(f"  • Duplicates: {overview['duplicates']}")
    if overview['total_missing'] > 0:
        print(f"  • Missing values: {overview['total_missing']}")
    
    # Correlations
    corr = results['correlations']
    if corr.get('available') and corr['strong_correlations']:
        print(f"\n🔗 Strong Correlations:")
        for c in corr['strong_correlations'][:5]:
            print(f"  • {c['feature1']} ↔ {c['feature2']}: {c['correlation']:.2f}")
    
    # Insights
    if results['insights']:
        print(f"\n💡 Insights:")
        for insight in results['insights']:
            print(f"  {insight}")
    
    # Recommendations
    if results['recommendations']:
        print(f"\n🎯 Recommendations:")
        for i, rec in enumerate(results['recommendations'][:5], 1):
            print(f"  {i}. {rec}")
    
    print("\n" + "=" * 70 + "\n")


class ProfileAgent:
    """
    Profile Agent for intelligent data analysis.
    """
    
    def __init__(self):
        pass
    
    def analyze(self, data: Union[str, pd.DataFrame], **kwargs) -> Dict[str, Any]:
        """Analyze data."""
        return analyze(data, **kwargs)
