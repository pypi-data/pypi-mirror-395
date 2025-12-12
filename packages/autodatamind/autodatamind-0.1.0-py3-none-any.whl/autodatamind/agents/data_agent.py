"""
Data Agent - Intelligent Data Handler
======================================

Automatically loads, cleans, and prepares data.
"""

import pandas as pd
from typing import Union, Optional
from autodatamind.core.reader import read_data
from autodatamind.core.cleaner import autoclean
from autodatamind.core.validator import validate_data


class DataAgent:
    """
    Data Agent handles all data operations automatically.
    """
    
    def __init__(self):
        self.data = None
        self.original_data = None
        self.validation_results = None
    
    def load(self, source: Union[str, pd.DataFrame]) -> pd.DataFrame:
        """Load data from file or DataFrame."""
        self.original_data = read_data(source)
        self.data = self.original_data.copy()
        self.validation_results = validate_data(self.data)
        return self.data
    
    def clean(self, **kwargs) -> pd.DataFrame:
        """Auto-clean the loaded data."""
        if self.data is None:
            raise ValueError("No data loaded. Use load() first.")
        
        self.data = autoclean(self.data, **kwargs)
        return self.data
    
    def get_info(self) -> dict:
        """Get data information."""
        if self.data is None:
            return {}
        
        return {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'dtypes': {col: str(dtype) for col, dtype in self.data.dtypes.items()},
            'memory_mb': self.data.memory_usage(deep=True).sum() / (1024 * 1024),
            'validation': self.validation_results,
        }
