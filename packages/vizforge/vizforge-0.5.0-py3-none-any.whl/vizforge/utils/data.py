"""Data processing utilities for VizForge."""

from typing import Optional, List, Union, Tuple
import pandas as pd
import numpy as np


def clean_data(
    df: pd.DataFrame,
    drop_duplicates: bool = True,
    fill_na: Optional[Union[str, float]] = None,
    drop_na: bool = False,
    columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Clean DataFrame for visualization.

    Args:
        df: Input DataFrame
        drop_duplicates: Remove duplicate rows
        fill_na: Value to fill NaN with ('mean', 'median', 'mode', or number)
        drop_na: Drop rows with NaN
        columns: Specific columns to clean (None = all)

    Returns:
        Cleaned DataFrame

    Examples:
        >>> import vizforge as vz
        >>> df = vz.clean_data(df, fill_na='mean', drop_duplicates=True)
    """
    df = df.copy()

    # Select columns
    cols = columns or df.columns.tolist()

    # Drop duplicates
    if drop_duplicates:
        df = df.drop_duplicates()

    # Handle NaN
    if drop_na:
        df = df.dropna(subset=cols)
    elif fill_na is not None:
        if fill_na == 'mean':
            df[cols] = df[cols].fillna(df[cols].mean())
        elif fill_na == 'median':
            df[cols] = df[cols].fillna(df[cols].median())
        elif fill_na == 'mode':
            df[cols] = df[cols].fillna(df[cols].mode().iloc[0])
        else:
            df[cols] = df[cols].fillna(fill_na)

    return df


def aggregate_data(
    df: pd.DataFrame,
    group_by: Union[str, List[str]],
    agg_column: str,
    agg_func: str = 'sum'
) -> pd.DataFrame:
    """
    Aggregate data for visualization.

    Args:
        df: Input DataFrame
        group_by: Column(s) to group by
        agg_column: Column to aggregate
        agg_func: Aggregation function ('sum', 'mean', 'count', 'min', 'max')

    Returns:
        Aggregated DataFrame

    Examples:
        >>> import vizforge as vz
        >>> df_agg = vz.aggregate_data(df, group_by='category', agg_column='sales', agg_func='sum')
    """
    return df.groupby(group_by)[agg_column].agg(agg_func).reset_index()


def resample_timeseries(
    df: pd.DataFrame,
    time_column: str,
    freq: str,
    agg_func: str = 'mean'
) -> pd.DataFrame:
    """
    Resample time series data.

    Args:
        df: Input DataFrame
        time_column: Column with datetime values
        freq: Resampling frequency ('D', 'W', 'M', 'Q', 'Y')
        agg_func: Aggregation function

    Returns:
        Resampled DataFrame

    Examples:
        >>> import vizforge as vz
        >>> df_daily = vz.resample_timeseries(df, 'date', freq='D', agg_func='sum')
    """
    df = df.copy()
    df[time_column] = pd.to_datetime(df[time_column])
    df = df.set_index(time_column)
    df_resampled = df.resample(freq).agg(agg_func).reset_index()
    return df_resampled


def detect_outliers(
    df: pd.DataFrame,
    column: str,
    method: str = 'iqr',
    threshold: float = 1.5
) -> pd.DataFrame:
    """
    Detect outliers in data.

    Args:
        df: Input DataFrame
        column: Column to check for outliers
        method: Detection method ('iqr', 'zscore')
        threshold: Threshold for outlier detection

    Returns:
        DataFrame with outlier flag column

    Examples:
        >>> import vizforge as vz
        >>> df = vz.detect_outliers(df, 'price', method='iqr')
        >>> # Filter outliers: df[~df['outlier']]
    """
    df = df.copy()

    if method == 'iqr':
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - threshold * IQR
        upper = Q3 + threshold * IQR
        df['outlier'] = (df[column] < lower) | (df[column] > upper)

    elif method == 'zscore':
        mean = df[column].mean()
        std = df[column].std()
        df['outlier'] = np.abs((df[column] - mean) / std) > threshold

    return df


def normalize_data(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    method: str = 'minmax'
) -> pd.DataFrame:
    """
    Normalize data for visualization.

    Args:
        df: Input DataFrame
        columns: Columns to normalize (None = all numeric)
        method: Normalization method ('minmax', 'zscore')

    Returns:
        Normalized DataFrame

    Examples:
        >>> import vizforge as vz
        >>> df_norm = vz.normalize_data(df, columns=['value1', 'value2'])
    """
    df = df.copy()
    cols = columns or df.select_dtypes(include=[np.number]).columns.tolist()

    if method == 'minmax':
        for col in cols:
            min_val = df[col].min()
            max_val = df[col].max()
            df[col] = (df[col] - min_val) / (max_val - min_val)

    elif method == 'zscore':
        for col in cols:
            mean = df[col].mean()
            std = df[col].std()
            df[col] = (df[col] - mean) / std

    return df


def bin_data(
    df: pd.DataFrame,
    column: str,
    bins: Union[int, List[float]],
    labels: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Bin continuous data into categories.

    Args:
        df: Input DataFrame
        column: Column to bin
        bins: Number of bins or list of bin edges
        labels: Labels for bins

    Returns:
        DataFrame with binned column

    Examples:
        >>> import vizforge as vz
        >>> df = vz.bin_data(df, 'age', bins=[0, 18, 30, 50, 100],
        ...                  labels=['Child', 'Young', 'Adult', 'Senior'])
    """
    df = df.copy()
    df[f'{column}_binned'] = pd.cut(df[column], bins=bins, labels=labels)
    return df
