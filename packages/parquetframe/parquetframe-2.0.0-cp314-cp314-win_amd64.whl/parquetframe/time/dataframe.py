"""
TimeSeriesDataFrame - Time-aware DataFrame extension.

Provides convenient time-series operations on top of pandas DataFrames.
"""

import pandas as pd

from . import operations


class TimeSeriesDataFrame:
    """
    Time-series aware DataFrame wrapper.

    Wraps a pandas DataFrame and provides convenient time-series operations.

    Args:
        df: Underlying pandas DataFrame
        time_col: Name of the timestamp column

    Example:
        >>> df = pd.DataFrame({
        ...     "timestamp": pd.date_range("2024-01-01", periods=100, freq="1s"),
        ...     "temperature": range(100),
        ...     "humidity": range(100, 200)
        ... })
        >>> ts = TimeSeriesDataFrame(df, "timestamp")
        >>> hourly = ts.resample("1H", agg="mean")
    """

    def __init__(self, df: pd.DataFrame, time_col: str):
        """Initialize TimeSeriesDataFrame."""
        self.df = df
        self.time_col = time_col

        # Ensure time column is datetime
        if not pd.api.types.is_datetime64_any_dtype(df[time_col]):
            self.df[time_col] = pd.to_datetime(df[time_col])

    def resample(self, freq: str, agg: str = "mean") -> "TimeSeriesDataFrame":
        """
        Resample to different frequency.

        Args:
            freq: Target frequency (e.g., "1H", "30s", "5min")
            agg: Aggregation method

        Returns:
            New TimeSeriesDataFrame with resampled data

        Example:
            >>> hourly = ts.resample("1H", agg="mean")
        """
        resampled = operations.resample(self.df, self.time_col, freq, agg)
        return TimeSeriesDataFrame(resampled, self.time_col)

    def rolling(self, window: int, agg: str = "mean") -> "TimeSeriesDataFrame":
        """
        Apply rolling window aggregation.

        Args:
            window: Window size
            agg: Aggregation method ("mean", "std", "min", "max")

        Returns:
            New TimeSeriesDataFrame with rolling aggregation

        Example:
            >>> smoothed = ts.rolling(window=7, agg="mean")
        """
        result = self.df.copy()

        for col in self.df.columns:
            if col == self.time_col:
                continue
            if pd.api.types.is_numeric_dtype(self.df[col]):
                result[col] = operations.rolling_window(self.df[col], window, agg)

        return TimeSeriesDataFrame(result, self.time_col)

    def asof_join(
        self,
        other: "TimeSeriesDataFrame",
        value_col: str,
        strategy: str = "backward",
        tolerance_ns: int | None = None,
    ) -> "TimeSeriesDataFrame":
        """
        Perform as-of join with another time-series.

        Args:
            other: Right TimeSeriesDataFrame
            value_col: Column from right to join
            strategy: Join strategy ("backward", "forward", "nearest")
            tolerance_ns: Maximum time difference in nanoseconds

        Returns:
            New TimeSeriesDataFrame with joined data

        Example:
            >>> trades_ts = TimeSeriesDataFrame(trades, "trade_time")
            >>> quotes_ts = TimeSeriesDataFrame(quotes, "quote_time")
            >>> result = trades_ts.asof_join(quotes_ts, "bid", strategy="backward")
        """
        joined = operations.asof_join(
            self.df,
            other.df,
            self.time_col,
            other.time_col,
            value_col,
            strategy,
            tolerance_ns,
        )
        return TimeSeriesDataFrame(joined, self.time_col)

    def to_pandas(self) -> pd.DataFrame:
        """Convert back to regular pandas DataFrame."""
        return self.df

    def __repr__(self) -> str:
        """String representation."""
        return f"TimeSeriesDataFrame(time_col='{self.time_col}', shape={self.df.shape})"

    def __len__(self) -> int:
        """Number of rows."""
        return len(self.df)
