"""Time Series Data Loader."""

import pandas as pd
import numpy as np
from typing import Union


class TimeSeriesLoader:
    """Load and preprocess time series data."""
    
    def load(self, data: Union[str, pd.DataFrame]) -> pd.DataFrame:
        """Load time series data."""
        if isinstance(data, pd.DataFrame):
            df = data
        else:
            df = pd.read_csv(data, parse_dates=True, infer_datetime_format=True)
        
        # Try to identify time column
        for col in df.columns:
            if 'date' in col.lower() or 'time' in col.lower():
                df[col] = pd.to_datetime(df[col])
                df = df.sort_values(col)
                break
        
        return df
