"""Optional pandas integration utilities for GradientCast SDK.

This module provides helper functions for converting between pandas DataFrames
and the data formats expected by GradientCast endpoints.

All functions in this module require pandas to be installed.
Install with: pip install gradientcast[pandas]
"""

from typing import Any, Dict, List, Optional


def _check_pandas() -> Any:
    """Check if pandas is installed and return the module.

    Returns:
        The pandas module.

    Raises:
        ImportError: If pandas is not installed.
    """
    try:
        import pandas as pd
        return pd
    except ImportError:
        raise ImportError(
            "pandas is required for this operation. "
            "Install with: pip install gradientcast[pandas]"
        )


def dataframe_to_fm_input(
    df: Any,
    value_column: str,
    series_column: Optional[str] = None
) -> Dict[str, List[float]]:
    """Convert a DataFrame to GradientCastFM input format.

    Args:
        df: Input pandas DataFrame.
        value_column: Name of the column containing time series values.
        series_column: Column name for series identifier (for multi-series).
                      If None, treats all data as a single series.

    Returns:
        Dictionary mapping series names to lists of values.

    Example:
        >>> df = pd.DataFrame({
        ...     "date": pd.date_range("2024-01-01", periods=10),
        ...     "sales": [100, 120, 115, 130, 125, 140, 135, 150, 145, 160],
        ...     "product": ["A"] * 5 + ["B"] * 5
        ... })
        >>> input_data = dataframe_to_fm_input(df, "sales", "product")
        >>> # Returns: {"A": [100, 120, 115, 130, 125], "B": [140, 135, 150, 145, 160]}
    """
    pd = _check_pandas()

    if series_column is None:
        return {"default": df[value_column].tolist()}

    result = {}
    for series_name, group in df.groupby(series_column):
        result[str(series_name)] = group[value_column].tolist()

    return result


def dataframe_to_dense_ad_input(
    df: Any,
    timestamp_column: str = "timestamp",
    value_column: str = "value"
) -> List[Dict[str, Any]]:
    """Convert a DataFrame to GradientCastDenseAD input format.

    Args:
        df: Input pandas DataFrame.
        timestamp_column: Name of the datetime column.
        value_column: Name of the value column.

    Returns:
        List of dictionaries with "timestamp" and "value" keys.

    Example:
        >>> df = pd.DataFrame({
        ...     "timestamp": pd.date_range("2024-01-01", periods=3, freq="H"),
        ...     "value": [1500000, 1520000, 1480000]
        ... })
        >>> data = dataframe_to_ad_input(df)
        >>> # Returns: [
        >>> #     {"timestamp": "01/01/2024, 12:00 AM", "value": 1500000},
        >>> #     {"timestamp": "01/01/2024, 01:00 AM", "value": 1520000},
        >>> #     {"timestamp": "01/01/2024, 02:00 AM", "value": 1480000}
        >>> # ]
    """
    pd = _check_pandas()

    result = []
    for _, row in df.iterrows():
        ts = row[timestamp_column]

        # Convert pandas Timestamp to expected string format
        if isinstance(ts, pd.Timestamp):
            ts_str = ts.strftime("%m/%d/%Y, %I:%M %p")
        else:
            ts_str = str(ts)

        result.append({
            "timestamp": ts_str,
            "value": int(row[value_column])
        })

    return result


def dataframe_to_ad_input(
    df: Any,
    timestamp_column: str = "timestamp",
    value_column: str = "value",
    dimension_column: Optional[str] = None
) -> Dict[str, List[Dict[str, Any]]]:
    """Convert a DataFrame to GradientCastPulseAD input format.

    Args:
        df: Input pandas DataFrame.
        timestamp_column: Name of the timestamp column.
        value_column: Name of the value column.
        dimension_column: Column for dimension names. If None,
                         uses "default" as the dimension name.

    Returns:
        Dictionary mapping dimension names to lists of data points.

    Example:
        >>> df = pd.DataFrame({
        ...     "timestamp": pd.date_range("2024-01-01", periods=6, freq="H"),
        ...     "value": [1500000.0, 1520000.0, 1480000.0, 1510000.0, 1530000.0, 1490000.0],
        ...     "region": ["AllUp"] * 3 + ["Region_East"] * 3
        ... })
        >>> data = dataframe_to_tsfad_input(df, dimension_column="region")
        >>> # Returns: {
        >>> #     "AllUp": [{"timestamp": "...", "value": 1500000.0}, ...],
        >>> #     "Region_East": [{"timestamp": "...", "value": ...}, ...]
        >>> # }
    """
    pd = _check_pandas()

    def format_timestamp(ts: Any) -> str:
        if isinstance(ts, pd.Timestamp):
            return ts.strftime("%m/%d/%Y, %I:%M %p")
        return str(ts)

    if dimension_column is None:
        points = []
        for _, row in df.iterrows():
            points.append({
                "timestamp": format_timestamp(row[timestamp_column]),
                "value": float(row[value_column])
            })
        return {"default": points}

    result = {}
    for dimension, group in df.groupby(dimension_column):
        points = []
        for _, row in group.iterrows():
            points.append({
                "timestamp": format_timestamp(row[timestamp_column]),
                "value": float(row[value_column])
            })
        result[str(dimension)] = points

    return result


def forecast_response_to_dataframe(
    forecast: Dict[str, List[float]],
    freq: Optional[str] = None,
    start_index: int = 1
) -> Any:
    """Convert forecast results to a DataFrame.

    Args:
        forecast: Dictionary mapping series names to forecast values.
        freq: Optional frequency string for generating datetime index.
        start_index: Starting index for horizon_step (default 1).

    Returns:
        DataFrame with columns: series, horizon_step, forecast

    Example:
        >>> forecast = {"product_a": [100.5, 105.2, 110.1]}
        >>> df = forecast_response_to_dataframe(forecast)
        >>> print(df)
               series  horizon_step  forecast
        0  product_a             1     100.5
        1  product_a             2     105.2
        2  product_a             3     110.1
    """
    pd = _check_pandas()

    records = []
    for series_name, values in forecast.items():
        for i, value in enumerate(values):
            records.append({
                "series": series_name,
                "horizon_step": start_index + i,
                "forecast": value
            })

    return pd.DataFrame(records)
