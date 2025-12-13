"""
Dask engine implementation for ParquetFrame Phase 2.

Provides Dask DataFrame engine with distributed computing capabilities
for large-scale datasets and out-of-core processing.
"""

from pathlib import Path
from typing import Any

try:
    import dask.dataframe as dd

    DASK_AVAILABLE = True
except ImportError:
    dd = None  # type: ignore[assignment]
    DASK_AVAILABLE = False

import pandas as pd

from ..core.base import DataFrameLike, Engine


class DaskEngine(Engine):
    """Dask DataFrame engine implementation."""

    @property
    def name(self) -> str:
        """Engine name."""
        return "dask"

    @property
    def is_lazy(self) -> bool:
        """Dask is lazy by default."""
        return True

    @property
    def is_available(self) -> bool:
        """Check if Dask is available."""
        return DASK_AVAILABLE and dd is not None

    def read_parquet(self, path: str | Path, **kwargs: Any) -> DataFrameLike:
        """Read Parquet file using Dask."""
        if not self.is_available:
            raise ImportError("Dask is not available")

        return dd.read_parquet(str(path), **kwargs)  # type: ignore[return-value]

    def read_csv(self, path: str | Path, **kwargs: Any) -> DataFrameLike:
        """Read CSV file using Dask."""
        if not self.is_available:
            raise ImportError("Dask is not available")

        return dd.read_csv(str(path), **kwargs)  # type: ignore[return-value]

    def to_pandas(self, df: DataFrameLike) -> pd.DataFrame:
        """Convert Dask DataFrame to pandas."""
        if not self.is_available:
            raise ImportError("Dask is not available")

        if isinstance(df, dd.DataFrame):
            return df.compute()
        else:
            # Already pandas or compatible
            return pd.DataFrame(df)  # type: ignore[arg-type,call-overload]

    def compute_if_lazy(self, df: DataFrameLike) -> DataFrameLike:
        """Compute Dask DataFrame to pandas."""
        if not self.is_available:
            raise ImportError("Dask is not available")

        if isinstance(df, dd.DataFrame):
            return df.compute()  # type: ignore[return-value]
        else:
            return df

    def estimate_memory_usage(self, df: DataFrameLike) -> int:
        """Estimate memory usage in bytes."""
        if not self.is_available:
            return 0

        if isinstance(df, dd.DataFrame):
            try:
                # Estimate based on partitions and dtypes
                memory_per_partition = (
                    df.get_partition(0).memory_usage(deep=True).sum().compute()
                )
                num_partitions = df.npartitions
                return int(memory_per_partition * num_partitions)
            except Exception:
                # Fallback: rough estimate
                try:
                    nrows = len(df)  # This might be expensive for Dask
                    ncols = len(df.columns)
                    return nrows * ncols * 8  # 8 bytes per value
                except Exception:
                    # Last resort
                    return df.npartitions * 1024 * 1024  # 1MB per partition

        return 0

    def from_pandas(self, df: pd.DataFrame, npartitions: int = None) -> "dd.DataFrame":
        """Convert pandas DataFrame to Dask DataFrame."""
        if not self.is_available:
            raise ImportError("Dask is not available")

        if npartitions is None:
            # Auto-determine partitions based on size
            nrows = len(df)
            if nrows < 10000:
                npartitions = 1
            elif nrows < 100000:
                npartitions = 2
            else:
                npartitions = max(2, nrows // 100000)

        return dd.from_pandas(df, npartitions=npartitions)
