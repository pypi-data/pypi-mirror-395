"""
Data preprocessing utilities.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from sklearn.preprocessing import StandardScaler, MinMaxScaler


def normalize_features(data: np.ndarray, method: str = 'standard') -> Tuple[np.ndarray, object]:
    """
    Normalize feature data.
    
    Args:
        data: Input data array
        method: 'standard' (z-score) or 'minmax' (0-1)
        
    Returns:
        Tuple of (normalized_data, scaler)
    """
    if method == 'standard':
        scaler = StandardScaler()
    elif method == 'minmax':
        scaler = MinMaxScaler()
    else:
        raise ValueError(f"Unknown normalization method: {method}")
    
    normalized = scaler.fit_transform(data)
    
    return normalized, scaler


def handle_missing_values(df: pd.DataFrame, strategy: str = 'mean') -> pd.DataFrame:
    """
    Handle missing values in DataFrame.
    
    Args:
        df: Input DataFrame
        strategy: 'mean', 'median', 'drop', or 'zero'
        
    Returns:
        DataFrame with handled missing values
    """
    df_copy = df.copy()
    
    if strategy == 'mean':
        df_copy = df_copy.fillna(df_copy.mean())
    elif strategy == 'median':
        df_copy = df_copy.fillna(df_copy.median())
    elif strategy == 'drop':
        df_copy = df_copy.dropna()
    elif strategy == 'zero':
        df_copy = df_copy.fillna(0)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")
    
    return df_copy


def clip_outliers(data: np.ndarray, n_std: float = 3.0) -> np.ndarray:
    """
    Clip outliers beyond n standard deviations.
    
    Args:
        data: Input array
        n_std: Number of standard deviations
        
    Returns:
        Clipped array
    """
    mean = np.mean(data)
    std = np.std(data)
    
    lower_bound = mean - n_std * std
    upper_bound = mean + n_std * std
    
    return np.clip(data, lower_bound, upper_bound)


def smooth_timeseries(data: np.ndarray, window_size: int = 3) -> np.ndarray:
    """
    Apply moving average smoothing to time series.
    
    Args:
        data: Input array
        window_size: Size of smoothing window
        
    Returns:
        Smoothed array
    """
    if len(data) < window_size:
        return data
    
    smoothed = np.convolve(data, np.ones(window_size)/window_size, mode='same')
    
    return smoothed


def create_feature_matrix(data_dict: Dict, feature_names: List[str]) -> np.ndarray:
    """
    Create feature matrix from dictionary of features.
    
    Args:
        data_dict: Dictionary with feature data
        feature_names: List of feature names to extract
        
    Returns:
        Feature matrix
    """
    features = []
    
    for name in feature_names:
        if name in data_dict:
            value = data_dict[name]
            if isinstance(value, (int, float)):
                features.append(value)
            elif isinstance(value, dict):
                # Extract nested value
                features.append(list(value.values())[0] if value else 0)
            else:
                features.append(0)
        else:
            features.append(0)
    
    return np.array(features).reshape(1, -1)


def aggregate_spatial_data(values: List[float], method: str = 'mean') -> float:
    """
    Aggregate spatial data points.
    
    Args:
        values: List of values
        method: 'mean', 'median', 'sum', 'max', 'min'
        
    Returns:
        Aggregated value
    """
    if not values:
        return 0.0
    
    values = np.array(values)
    
    if method == 'mean':
        return float(np.mean(values))
    elif method == 'median':
        return float(np.median(values))
    elif method == 'sum':
        return float(np.sum(values))
    elif method == 'max':
        return float(np.max(values))
    elif method == 'min':
        return float(np.min(values))
    else:
        raise ValueError(f"Unknown method: {method}")


def calculate_percentile_rank(value: float, distribution: List[float]) -> float:
    """
    Calculate percentile rank of value in distribution.
    
    Args:
        value: Value to rank
        distribution: Reference distribution
        
    Returns:
        Percentile rank (0-100)
    """
    if not distribution:
        return 50.0
    
    distribution = sorted(distribution)
    n = len(distribution)
    
    # Count values less than target
    count_below = sum(1 for x in distribution if x < value)
    
    # Percentile rank
    percentile = (count_below / n) * 100
    
    return float(percentile)


def log_transform(data: np.ndarray, offset: float = 1.0) -> np.ndarray:
    """
    Apply log transformation to data.
    
    Args:
        data: Input array
        offset: Offset to add before log (to handle zeros)
        
    Returns:
        Log-transformed array
    """
    return np.log1p(data + offset - 1)


def inverse_log_transform(data: np.ndarray, offset: float = 1.0) -> np.ndarray:
    """
    Inverse log transformation.
    
    Args:
        data: Log-transformed array
        offset: Offset used in transformation
        
    Returns:
        Original scale array
    """
    return np.expm1(data) - offset + 1


def bin_continuous_variable(values: np.ndarray, n_bins: int = 5, 
                           labels: Optional[List[str]] = None) -> np.ndarray:
    """
    Bin continuous variable into categories.
    
    Args:
        values: Continuous values
        n_bins: Number of bins
        labels: Optional bin labels
        
    Returns:
        Binned categories
    """
    bins = pd.qcut(values, q=n_bins, labels=labels, duplicates='drop')
    
    return bins


def calculate_z_score(value: float, mean: float, std: float) -> float:
    """
    Calculate z-score for a value.
    
    Args:
        value: Value to score
        mean: Mean of distribution
        std: Standard deviation
        
    Returns:
        Z-score
    """
    if std == 0:
        return 0.0
    
    return (value - mean) / std


def robust_scale(data: np.ndarray) -> np.ndarray:
    """
    Robust scaling using median and IQR.
    
    Args:
        data: Input array
        
    Returns:
        Scaled array
    """
    median = np.median(data)
    q75, q25 = np.percentile(data, [75, 25])
    iqr = q75 - q25
    
    if iqr == 0:
        return data - median
    
    return (data - median) / iqr


def weighted_average(values: List[float], weights: List[float]) -> float:
    """
    Calculate weighted average.
    
    Args:
        values: List of values
        weights: List of weights (must sum to 1)
        
    Returns:
        Weighted average
    """
    if len(values) != len(weights):
        raise ValueError("Values and weights must have same length")
    
    if not np.isclose(sum(weights), 1.0):
        # Normalize weights
        weights = np.array(weights) / sum(weights)
    
    return float(np.average(values, weights=weights))


def interpolate_missing(values: List[float]) -> List[float]:
    """
    Interpolate missing values (NaN) in list.
    
    Args:
        values: List with possible NaN values
        
    Returns:
        List with interpolated values
    """
    values = np.array(values, dtype=float)
    
    # Find indices of non-NaN values
    valid_idx = ~np.isnan(values)
    
    if not valid_idx.any():
        return values.tolist()
    
    # Interpolate
    interpolated = np.interp(
        np.arange(len(values)),
        np.where(valid_idx)[0],
        values[valid_idx]
    )
    
    return interpolated.tolist()
