"""
DataFrame engine implementations for ParquetFrame Phase 2.

Provides concrete implementations of the Engine interface for pandas, Polars,
and Dask with consistent behavior and optimal performance characteristics.
"""

from .dask_engine import DaskEngine
from .pandas_engine import PandasEngine
from .polars_engine import PolarsEngine

__all__ = [
    "PandasEngine",
    "PolarsEngine",
    "DaskEngine",
]
