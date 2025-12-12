"""
Tabular Data Loader
===================

Handles loading and preprocessing of tabular data (CSV, Excel, Parquet).
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Union


class TabularLoader:
    """Load and preprocess tabular data."""
    
    def load(self, data: Union[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Load tabular data from various sources.
        
        Parameters
        ----------
        data : str or DataFrame
            File path or DataFrame
        
        Returns
        -------
        DataFrame
            Loaded and preprocessed data
        """
        if isinstance(data, pd.DataFrame):
            return data
        
        # Load from file
        path = Path(data)
        ext = path.suffix.lower()
        
        if ext == '.csv':
            df = pd.read_csv(data)
        elif ext in ['.xlsx', '.xls']:
            df = pd.read_excel(data)
        elif ext == '.parquet':
            df = pd.read_parquet(data)
        elif ext == '.json':
            df = pd.read_json(data)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        
        return self._preprocess(df)
    
    def _preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """Basic preprocessing."""
        # Remove completely empty rows/columns
        df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)
        
        return df
