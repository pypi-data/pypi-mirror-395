"""
Auto Cleaner - Intelligent Data Cleaning
=========================================

Automatically cleans data without user intervention:
- Removes duplicates
- Handles missing values
- Fixes data types
- Normalizes formats
- Detects and handles outliers
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, Any


def autoclean(data: pd.DataFrame, 
              remove_duplicates: bool = True,
              handle_missing: str = 'auto',
              fix_types: bool = True,
              remove_outliers: bool = False,
              verbose: bool = True) -> pd.DataFrame:
    """
    Automatically clean data.
    
    Parameters
    ----------
    data : DataFrame
        Input data
    remove_duplicates : bool
        Remove duplicate rows
    handle_missing : str
        'auto', 'drop', 'mean', 'median', 'mode', 'forward_fill'
    fix_types : bool
        Automatically fix data types
    remove_outliers : bool
        Remove statistical outliers
    verbose : bool
        Print cleaning steps
    
    Returns
    -------
    DataFrame
        Cleaned data
    
    Examples
    --------
    >>> import autodatamind as adm
    >>> clean_df = adm.autoclean(df)
    """
    df = data.copy()
    steps = []
    
    # Remove duplicates
    if remove_duplicates:
        n_duplicates = df.duplicated().sum()
        if n_duplicates > 0:
            df = df.drop_duplicates()
            steps.append(f"Removed {n_duplicates} duplicate rows")
    
    # Fix data types
    if fix_types:
        df, type_changes = _auto_fix_types(df)
        if type_changes:
            steps.append(f"Fixed {type_changes} column types")
    
    # Handle missing values
    if handle_missing != 'none':
        df, missing_handled = _handle_missing(df, method=handle_missing)
        if missing_handled > 0:
            steps.append(f"Handled missing values in {missing_handled} columns")
    
    # Remove outliers
    if remove_outliers:
        df, n_outliers = _remove_outliers(df)
        if n_outliers > 0:
            steps.append(f"Removed {n_outliers} outlier rows")
    
    # Print summary
    if verbose and steps:
        print("✓ AutoClean Summary:")
        for step in steps:
            print(f"  • {step}")
        print(f"  • Final shape: {df.shape[0]} rows × {df.shape[1]} columns")
    
    return df


def _auto_fix_types(df: pd.DataFrame) -> tuple:
    """Automatically detect and fix column types."""
    type_changes = 0
    
    for col in df.columns:
        # Try to convert to datetime
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_datetime(df[col], errors='ignore')
                if df[col].dtype != 'object':
                    type_changes += 1
                    continue
            except:
                pass
            
            # Try to convert to numeric
            try:
                df[col] = pd.to_numeric(df[col], errors='ignore')
                if df[col].dtype != 'object':
                    type_changes += 1
            except:
                pass
    
    return df, type_changes


def _handle_missing(df: pd.DataFrame, method: str = 'auto') -> tuple:
    """Handle missing values intelligently."""
    missing_handled = 0
    
    for col in df.columns:
        if df[col].isnull().sum() == 0:
            continue
        
        missing_handled += 1
        
        if method == 'auto':
            # Auto-detect best strategy
            if df[col].dtype in [np.float64, np.int64]:
                # Numeric: use median
                df[col].fillna(df[col].median(), inplace=True)
            elif df[col].dtype == 'object':
                # Categorical: use mode
                mode_val = df[col].mode()
                if len(mode_val) > 0:
                    df[col].fillna(mode_val[0], inplace=True)
            else:
                # Default: forward fill
                df[col].fillna(method='ffill', inplace=True)
        
        elif method == 'drop':
            df = df.dropna(subset=[col])
        
        elif method == 'mean':
            if df[col].dtype in [np.float64, np.int64]:
                df[col].fillna(df[col].mean(), inplace=True)
        
        elif method == 'median':
            if df[col].dtype in [np.float64, np.int64]:
                df[col].fillna(df[col].median(), inplace=True)
        
        elif method == 'mode':
            mode_val = df[col].mode()
            if len(mode_val) > 0:
                df[col].fillna(mode_val[0], inplace=True)
        
        elif method == 'forward_fill':
            df[col].fillna(method='ffill', inplace=True)
    
    return df, missing_handled


def _remove_outliers(df: pd.DataFrame, threshold: float = 3.0) -> tuple:
    """Remove statistical outliers using Z-score method."""
    n_outliers = 0
    mask = pd.Series([True] * len(df))
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
        mask &= (z_scores < threshold)
    
    n_outliers = (~mask).sum()
    df = df[mask]
    
    return df, n_outliers


def get_data_quality_report(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate data quality report.
    
    Parameters
    ----------
    df : DataFrame
        Input data
    
    Returns
    -------
    dict
        Quality metrics
    """
    report = {
        'n_rows': len(df),
        'n_columns': len(df.columns),
        'n_duplicates': df.duplicated().sum(),
        'missing_values': {},
        'column_types': {},
        'memory_usage_mb': df.memory_usage(deep=True).sum() / (1024 * 1024),
    }
    
    # Missing values per column
    for col in df.columns:
        n_missing = df[col].isnull().sum()
        if n_missing > 0:
            report['missing_values'][col] = {
                'count': int(n_missing),
                'percentage': float(n_missing / len(df) * 100)
            }
    
    # Column types
    for col in df.columns:
        report['column_types'][col] = str(df[col].dtype)
    
    return report
