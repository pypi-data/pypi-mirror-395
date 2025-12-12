"""
Validator - Data Validation
============================

Validates data quality and structure.
"""

import pandas as pd
from typing import List, Dict, Any


def validate_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Validate DataFrame and return issues.
    
    Parameters
    ----------
    df : DataFrame
        Input data
    
    Returns
    -------
    dict
        Validation results with issues found
    """
    issues = []
    warnings = []
    
    # Check if empty
    if len(df) == 0:
        issues.append("Dataset is empty")
    
    # Check for all-null columns
    null_cols = [col for col in df.columns if df[col].isnull().all()]
    if null_cols:
        issues.append(f"Columns with all nulls: {null_cols}")
    
    # Check for high missing rate
    for col in df.columns:
        missing_pct = df[col].isnull().sum() / len(df) * 100
        if missing_pct > 50:
            warnings.append(f"{col}: {missing_pct:.1f}% missing values")
    
    # Check for single-value columns
    single_val_cols = [col for col in df.columns if df[col].nunique() == 1]
    if single_val_cols:
        warnings.append(f"Columns with single value: {single_val_cols}")
    
    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'warnings': warnings,
    }
