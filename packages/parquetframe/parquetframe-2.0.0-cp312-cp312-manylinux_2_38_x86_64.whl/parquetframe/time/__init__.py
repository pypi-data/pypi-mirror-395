"""
Time-series operations for ParquetFrame.

High-performance time-series functionality powered by Rust.
"""

# Import accessor to register it
from .accessor import TimeSeriesAccessor, TSAccessor
from .dataframe import TimeSeriesDataFrame
from .operations import asof_join, resample, rolling_window

__all__ = [
    "TimeSeriesDataFrame",
    "resample",
    "rolling_window",
    "asof_join",
    "TimeSeriesAccessor",
    "TSAccessor",
]
