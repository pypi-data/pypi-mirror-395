"""
Data Reader - Universal Data Loader
====================================

Automatically reads CSV, Excel, JSON, Parquet files.
Detects encoding, delimiters, and data types.
"""

import pandas as pd
import os
from typing import Union, Optional


def read_data(filepath: Union[str, pd.DataFrame], **kwargs) -> pd.DataFrame:
    """
    Universal data reader - automatically detects file type and loads it.
    
    Parameters
    ----------
    filepath : str or DataFrame
        Path to file (CSV, Excel, JSON, Parquet) or existing DataFrame
    **kwargs : dict
        Additional arguments passed to pandas readers
    
    Returns
    -------
    DataFrame
        Loaded data
    
    Examples
    --------
    >>> import autodatamind as adm
    >>> df = adm.read_data("sales.csv")
    >>> df = adm.read_data("data.xlsx")
    >>> df = adm.read_data("records.json")
    """
    # If already a DataFrame, return it
    if isinstance(filepath, pd.DataFrame):
        return filepath.copy()
    
    # Check if file exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    # Get file extension
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()
    
    try:
        if ext == '.csv':
            return _read_csv(filepath, **kwargs)
        elif ext in ['.xlsx', '.xls']:
            return _read_excel(filepath, **kwargs)
        elif ext == '.json':
            return _read_json(filepath, **kwargs)
        elif ext == '.parquet':
            return pd.read_parquet(filepath, **kwargs)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    
    except Exception as e:
        raise Exception(f"Error reading file {filepath}: {str(e)}")


def _read_csv(filepath: str, **kwargs) -> pd.DataFrame:
    """Read CSV with automatic encoding and delimiter detection."""
    # Try common encodings
    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    
    for encoding in encodings:
        try:
            # Try to detect delimiter
            return pd.read_csv(filepath, encoding=encoding, **kwargs)
        except:
            continue
    
    # If all fail, try with sep=None (auto-detect)
    try:
        return pd.read_csv(filepath, sep=None, engine='python', **kwargs)
    except:
        raise Exception(f"Could not read CSV file: {filepath}")


def _read_excel(filepath: str, **kwargs) -> pd.DataFrame:
    """Read Excel file."""
    # Read first sheet by default
    if 'sheet_name' not in kwargs:
        kwargs['sheet_name'] = 0
    
    return pd.read_excel(filepath, **kwargs)


def _read_json(filepath: str, **kwargs) -> pd.DataFrame:
    """Read JSON file."""
    # Try different JSON orientations
    orientations = ['records', 'index', 'columns', 'values']
    
    for orient in orientations:
        try:
            return pd.read_json(filepath, orient=orient, **kwargs)
        except:
            continue
    
    # Try as lines
    try:
        return pd.read_json(filepath, lines=True, **kwargs)
    except:
        raise Exception(f"Could not read JSON file: {filepath}")


def get_file_info(filepath: str) -> dict:
    """
    Get information about a data file.
    
    Parameters
    ----------
    filepath : str
        Path to file
    
    Returns
    -------
    dict
        File information
    """
    info = {
        'path': filepath,
        'exists': os.path.exists(filepath),
        'size_mb': 0,
        'extension': '',
    }
    
    if info['exists']:
        info['size_mb'] = os.path.getsize(filepath) / (1024 * 1024)
        _, ext = os.path.splitext(filepath)
        info['extension'] = ext.lower()
    
    return info
