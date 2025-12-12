"""
Preprocessing Utilities
=======================

Data preprocessing helpers.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from typing import Tuple, Optional


def clean_data(df: pd.DataFrame, 
              handle_missing: str = 'drop',
              handle_duplicates: bool = True) -> pd.DataFrame:
    """
    Clean DataFrame.
    
    Parameters
    ----------
    df : DataFrame
        Input data
    handle_missing : str
        'drop', 'mean', 'median', 'mode'
    handle_duplicates : bool
        Remove duplicate rows
    
    Returns
    -------
    DataFrame
        Cleaned data
    """
    df_clean = df.copy()
    
    # Handle duplicates
    if handle_duplicates:
        df_clean = df_clean.drop_duplicates()
    
    # Handle missing values
    if handle_missing == 'drop':
        df_clean = df_clean.dropna()
    elif handle_missing == 'mean':
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].mean())
    elif handle_missing == 'median':
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())
    elif handle_missing == 'mode':
        for col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0] if not df_clean[col].mode().empty else 0)
    
    return df_clean


def scale_features(X: np.ndarray, method: str = 'standard') -> Tuple[np.ndarray, object]:
    """
    Scale numeric features.
    
    Parameters
    ----------
    X : ndarray
        Input features
    method : str
        'standard' (z-score) or 'minmax' (0-1)
    
    Returns
    -------
    tuple
        (scaled_data, scaler_object)
    """
    if method == 'standard':
        scaler = StandardScaler()
    elif method == 'minmax':
        scaler = MinMaxScaler()
    else:
        raise ValueError(f"Unknown method: {method}")
    
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, scaler


def encode_categorical(df: pd.DataFrame, 
                       columns: Optional[list] = None) -> Tuple[pd.DataFrame, dict]:
    """
    Encode categorical variables.
    
    Parameters
    ----------
    df : DataFrame
        Input data
    columns : list, optional
        Columns to encode. If None, encode all object/category columns.
    
    Returns
    -------
    tuple
        (encoded_dataframe, encoders_dict)
    """
    df_encoded = df.copy()
    encoders = {}
    
    if columns is None:
        columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    for col in columns:
        if col in df.columns:
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
    
    return df_encoded, encoders


def remove_outliers(df: pd.DataFrame, 
                   columns: Optional[list] = None,
                   method: str = 'iqr',
                   threshold: float = 1.5) -> pd.DataFrame:
    """
    Remove outliers from numeric columns.
    
    Parameters
    ----------
    df : DataFrame
        Input data
    columns : list, optional
        Columns to process. If None, use all numeric columns.
    method : str
        'iqr' (Interquartile Range) or 'zscore'
    threshold : float
        IQR multiplier (default: 1.5) or Z-score threshold (default: 3.0)
    
    Returns
    -------
    DataFrame
        Data with outliers removed
    """
    df_clean = df.copy()
    
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    mask = pd.Series([True] * len(df))
    
    for col in columns:
        if col not in df.columns:
            continue
        
        if method == 'iqr':
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            
            mask &= (df[col] >= lower_bound) & (df[col] <= upper_bound)
        
        elif method == 'zscore':
            z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
            mask &= z_scores < threshold
    
    return df_clean[mask]
