"""
Base protocols and abstract interfaces for the multi-engine DataFrame core.

Defines the contracts that all DataFrame engines must implement to be compatible
with the ParquetFrame abstraction layer.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Protocol

import pandas as pd

try:
    import polars as pl

    POLARS_AVAILABLE = True
except ImportError:
    pl = None  # type: ignore[assignment]
    POLARS_AVAILABLE = False

try:
    import dask.dataframe as dd

    DASK_AVAILABLE = True
except ImportError:
    dd = None  # type: ignore[assignment]
    DASK_AVAILABLE = False


class DataFrameLike(Protocol):
    """Protocol for DataFrame-like objects across different engines."""

    def head(self, n: int = 5) -> "DataFrameLike":
        """Return the first n rows."""
        ...

    def tail(self, n: int = 5) -> "DataFrameLike":
        """Return the last n rows."""
        ...

    def shape(self) -> tuple[int, int]:
        """Return (nrows, ncols)."""
        ...

    def columns(self) -> list[str]:
        """Return column names."""
        ...


class Engine(ABC):
    """Abstract base class for DataFrame engines."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Engine name (e.g., 'pandas', 'polars', 'dask')."""
        pass

    @property
    @abstractmethod
    def is_lazy(self) -> bool:
        """Whether this engine uses lazy evaluation by default."""
        pass

    @property
    @abstractmethod
    def is_available(self) -> bool:
        """Whether this engine is available (library installed)."""
        pass

    @abstractmethod
    def read_parquet(self, path: str | Path, **kwargs: Any) -> DataFrameLike:
        """Read a Parquet file using this engine."""
        pass

    @abstractmethod
    def read_csv(self, path: str | Path, **kwargs: Any) -> DataFrameLike:
        """Read a CSV file using this engine."""
        pass

    @abstractmethod
    def to_pandas(self, df: DataFrameLike) -> pd.DataFrame:
        """Convert DataFrame to pandas."""
        pass

    @abstractmethod
    def compute_if_lazy(self, df: DataFrameLike) -> DataFrameLike:
        """Compute result if DataFrame is lazy, otherwise return as-is."""
        pass

    @abstractmethod
    def estimate_memory_usage(self, df: DataFrameLike) -> int:
        """Estimate memory usage in bytes."""
        pass


class EngineCapabilities:
    """Describes capabilities and characteristics of a DataFrame engine."""

    def __init__(
        self,
        name: str,
        is_lazy: bool = False,
        supports_distributed: bool = False,
        optimal_size_range: tuple[float, float] = (0, float("inf")),
        memory_efficiency: float = 1.0,
        performance_score: float = 1.0,
    ):
        self.name = name
        self.is_lazy = is_lazy
        self.supports_distributed = supports_distributed
        self.optimal_size_range = optimal_size_range
        self.memory_efficiency = memory_efficiency
        self.performance_score = performance_score
