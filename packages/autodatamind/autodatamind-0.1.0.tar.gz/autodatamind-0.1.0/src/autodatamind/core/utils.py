"""
Utilities - Helper Functions
=============================

Common utility functions used across the package.
"""

import pandas as pd
import numpy as np
from typing import List, Union, Any


def detect_problem_type(df: pd.DataFrame, target_col: str) -> str:
    """
    Detect ML problem type (regression, classification, clustering).
    
    Parameters
    ----------
    df : DataFrame
        Input data
    target_col : str
        Target column name
    
    Returns
    -------
    str
        'regression', 'binary_classification', 'multiclass_classification'
    """
    if target_col not in df.columns:
        return 'clustering'
    
    target = df[target_col]
    
    # Check if numeric
    if target.dtype in [np.float64, np.int64]:
        n_unique = target.nunique()
        
        if n_unique <= 10:
            return 'binary_classification' if n_unique == 2 else 'multiclass_classification'
        else:
            return 'regression'
    else:
        n_unique = target.nunique()
        return 'binary_classification' if n_unique == 2 else 'multiclass_classification'


def format_number(num: float) -> str:
    """Format number for display."""
    if abs(num) >= 1_000_000:
        return f"{num/1_000_000:.2f}M"
    elif abs(num) >= 1_000:
        return f"{num/1_000:.2f}K"
    else:
        return f"{num:.2f}"


def get_numeric_columns(df: pd.DataFrame) -> List[str]:
    """Get list of numeric column names."""
    return df.select_dtypes(include=[np.number]).columns.tolist()


def get_categorical_columns(df: pd.DataFrame) -> List[str]:
    """Get list of categorical column names."""
    return df.select_dtypes(include=['object', 'category']).columns.tolist()


def safe_divide(a: float, b: float, default: float = 0.0) -> float:
    """Safely divide two numbers."""
    try:
        if b == 0:
            return default
        return a / b
    except:
        return default


def create_summary_stats(series: pd.Series) -> dict:
    """Create summary statistics for a series."""
    stats = {
        'count': int(series.count()),
        'missing': int(series.isnull().sum()),
        'unique': int(series.nunique()),
    }
    
    if series.dtype in [np.number]:
        stats.update({
            'mean': float(series.mean()),
            'std': float(series.std()),
            'min': float(series.min()),
            'max': float(series.max()),
            'median': float(series.median()),
        })
    
    return stats
