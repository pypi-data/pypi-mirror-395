"""
Standalone time-series operations.

These functions provide direct access to time-series operations
without requiring a TimeSeriesDataFrame wrapper.
"""

import pandas as pd


def resample(
    df: pd.DataFrame,
    time_col: str,
    freq: str,
    agg: str = "mean",
) -> pd.DataFrame:
    """
    Resample time-series data using Rust backend.

    Args:
        df: Input DataFrame
        time_col: Name of timestamp column
        freq: Target frequency (e.g., "1H", "30s", "5min")
        agg: Aggregation method ("mean", "sum", "first", "last", "min", "max", "count")

    Returns:
        Resampled DataFrame

    Example:
        >>> df = pd.DataFrame({
        ...     "timestamp": pd.date_range("2024-01-01", periods=100, freq="1s"),
        ...     "value": range(100)
        ... })
        >>> hourly = resample(df, "timestamp", "1H", "mean")
    """
    try:
        from parquetframe._rustic import resample_ts
    except ImportError as err:
        raise ImportError(
            "Rust backend not available. Install with: pip install parquetframe[rust]"
        ) from err

    # Convert timestamps to nanoseconds
    timestamps = pd.to_datetime(df[time_col]).astype("int64").values.tolist()

    # Resample all numeric columns
    result_data = {time_col: []}

    for col in df.columns:
        if col == time_col:
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            values = df[col].astype("float64").values.tolist()
            new_ts, new_vals = resample_ts(timestamps, values, freq, agg)

            if time_col not in result_data or not result_data[time_col]:
                result_data[time_col] = new_ts
            result_data[col] = new_vals

    # Convert back to DataFrame
    result = pd.DataFrame(result_data)
    result[time_col] = pd.to_datetime(result[time_col])

    return result


def rolling_window(
    series: pd.Series,
    window: int,
    agg: str = "mean",
) -> pd.Series:
    """
    Compute rolling window using Rust backend.

    Args:
        series: Input series
        window: Window size
        agg: Aggregation method ("mean", "std", "min", "max")

    Returns:
        Series with rolling aggregation

    Example:
        >>> s = pd.Series([1, 2, 3, 4, 5])
        >>> rolling_mean = rolling_window(s, window=3, agg="mean")
    """
    try:
        from parquetframe._rustic import (
            rolling_max_ts,
            rolling_mean_ts,
            rolling_min_ts,
            rolling_std_ts,
        )
    except ImportError as err:
        raise ImportError("Rust backend not available") from err

    values = series.astype("float64").values.tolist()

    if agg == "mean":
        result = rolling_mean_ts(values, window)
    elif agg == "std":
        result = rolling_std_ts(values, window)
    elif agg == "min":
        result = rolling_min_ts(values, window)
    elif agg == "max":
        result = rolling_max_ts(values, window)
    else:
        raise ValueError(f"Unknown aggregation: {agg}")

    return pd.Series(result, index=series.index)


def asof_join(
    left: pd.DataFrame,
    right: pd.DataFrame,
    left_time_col: str,
    right_time_col: str,
    right_value_col: str,
    strategy: str = "backward",
    tolerance_ns: int | None = None,
) -> pd.DataFrame:
    """
    Perform as-of join using Rust backend.

    Joins left DataFrame with right DataFrame based on nearest timestamp.

    Args:
        left: Left DataFrame
        right: Right DataFrame (must be sorted by time column)
        left_time_col: Time column in left DataFrame
        right_time_col: Time column in right DataFrame
        right_value_col: Value column from right to join
        strategy: Join strategy ("backward", "forward", "nearest")
        tolerance_ns: Maximum time difference in nanoseconds

    Returns:
        Left DataFrame with joined column

    Example:
        >>> trades = pd.DataFrame({
        ...     "trade_time": pd.date_range("2024-01-01", periods=10, freq="1s"),
        ...     "price": [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
        ... })
        >>> quotes = pd.DataFrame({
        ...     "quote_time": pd.date_range("2024-01-01", periods=20, freq="500ms"),
        ...     "bid": range(20)
        ... })
        >>> result = asof_join(trades, quotes, "trade_time", "quote_time", "bid")
    """
    try:
        from parquetframe._rustic import asof_join_ts
    except ImportError as err:
        raise ImportError("Rust backend not available") from err

    # Convert to nanoseconds
    left_times = pd.to_datetime(left[left_time_col]).astype("int64").values.tolist()
    right_times = pd.to_datetime(right[right_time_col]).astype("int64").values.tolist()
    right_values = right[right_value_col].astype("float64").values.tolist()

    # Perform join
    matched_values = asof_join_ts(
        left_times,
        right_times,
        right_values,
        strategy,
        tolerance_ns,
    )

    # Add to left DataFrame
    result = left.copy()
    result[right_value_col] = matched_values

    return result
