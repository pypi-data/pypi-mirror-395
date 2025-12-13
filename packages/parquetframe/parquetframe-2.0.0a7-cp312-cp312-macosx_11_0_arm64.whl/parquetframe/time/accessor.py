"""
Time Series Accessor for ParquetFrame.

Provides pandas-style .ts accessor for time series operations.
"""

import pandas as pd


class TimeSeriesAccessor:
    """
    Time series operations accessor.

    Accessed via df.ts for time-indexed DataFrames.

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({
        ...     'timestamp': pd.date_range('2024-01-01', periods=100, freq='h'),
        ...     'value': range(100)
        ... }).set_index('timestamp')
        >>>
        >>> # Resample to daily
        >>> daily = df.ts.resample('1D', agg='mean')
        >>>
        >>> # Rolling window
        >>> smoothed = df.ts.rolling('7D', agg='mean')
    """

    def __init__(self, pandas_obj):
        """Initialize accessor with DataFrame."""
        self._obj = pandas_obj

        # Validate that index is datetime
        if not isinstance(self._obj.index, pd.DatetimeIndex):
            raise AttributeError(
                ".ts accessor requires a DatetimeIndex. "
                "Use df.set_index('timestamp_column') first."
            )

    def resample(self, rule: str, agg: str | list = "mean", **kwargs) -> pd.DataFrame:
        """
        Resample time series to different frequency.

        Args:
            rule: Resampling frequency (e.g., '1D', '1H', '5min')
            agg: Aggregation method ('mean', 'sum', 'min', 'max', 'count')
            **kwargs: Additional arguments for pandas resample

        Returns:
            Resampled DataFrame

        Example:
            >>> # Resample hourly data to daily
            >>> daily = df.ts.resample('1D', agg='mean')
            >>>
            >>> # Multiple aggregations
            >>> stats = df.ts.resample('1D', agg=['mean', 'std', 'count'])
        """
        resampler = self._obj.resample(rule, **kwargs)

        if isinstance(agg, str):
            return getattr(resampler, agg)()
        else:
            return resampler.agg(agg)

    def rolling(self, window: str | int, agg: str = "mean", **kwargs) -> pd.DataFrame:
        """
        Compute rolling window statistics.

        Args:
            window: Window size (e.g., '7D', 10)
            agg: Aggregation method
            **kwargs: Additional arguments for pandas rolling

        Returns:
            DataFrame with rolling statistics

        Example:
            >>> # 7-day rolling average
            >>> smoothed = df.ts.rolling('7D', agg='mean')
            >>>
            >>> # 10-period rolling sum
            >>> total = df.ts.rolling(10, agg='sum')
        """
        roller = self._obj.rolling(window, **kwargs)
        return getattr(roller, agg)()

    def interpolate(self, method: str = "linear", **kwargs) -> pd.DataFrame:
        """
        Interpolate missing values.

        Args:
            method: Interpolation method ('linear', 'time', 'polynomial')
            **kwargs: Additional arguments for pandas interpolate

        Returns:
            DataFrame with interpolated values

        Example:
            >>> # Linear interpolation
            >>> filled = df.ts.interpolate('linear')
            >>>
            >>> # Time-aware interpolation
            >>> filled = df.ts.interpolate('time')
        """
        return self._obj.interpolate(method=method, **kwargs)

    def shift(self, periods: int = 1, **kwargs) -> pd.DataFrame:
        """
        Shift time series by specified periods.

        Args:
            periods: Number of periods to shift
            **kwargs: Additional arguments for pandas shift

        Returns:
            Shifted DataFrame
        """
        return self._obj.shift(periods, **kwargs)

    def diff(self, periods: int = 1, **kwargs) -> pd.DataFrame:
        """
        Calculate difference between consecutive periods.

        Args:
            periods: Periods to shift for calculating difference
            **kwargs: Additional arguments for pandas diff

        Returns:
            DataFrame with differences
        """
        return self._obj.diff(periods, **kwargs)

    def pct_change(self, periods: int = 1, **kwargs) -> pd.DataFrame:
        """
        Calculate percentage change.

        Args:
            periods: Periods to shift for calculating change
            **kwargs: Additional arguments for pandas pct_change

        Returns:
            DataFrame with percentage changes
        """
        return self._obj.pct_change(periods, **kwargs)


# Register accessor with pandas
@pd.api.extensions.register_dataframe_accessor("ts")
class TSAccessor(TimeSeriesAccessor):
    """Pandas DataFrame accessor for time series operations."""

    pass


__all__ = ["TimeSeriesAccessor", "TSAccessor"]
