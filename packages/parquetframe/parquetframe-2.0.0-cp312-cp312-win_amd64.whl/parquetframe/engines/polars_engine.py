"""
Polars engine implementation for ParquetFrame Phase 2.

Provides Polars DataFrame engine with lazy evaluation and high-performance
processing for medium-scale datasets.
"""

from pathlib import Path
from typing import Any

try:
    import polars as pl

    POLARS_AVAILABLE = True
except ImportError:
    pl = None  # type: ignore[assignment]
    POLARS_AVAILABLE = False

import pandas as pd

from ..core.base import DataFrameLike, Engine


class PolarsEngine(Engine):
    """Polars DataFrame engine implementation."""

    @property
    def name(self) -> str:
        """Engine name."""
        return "polars"

    @property
    def is_lazy(self) -> bool:
        """Polars supports lazy evaluation."""
        return True

    @property
    def is_available(self) -> bool:
        """Check if Polars is available."""
        return POLARS_AVAILABLE and pl is not None

    def read_parquet(self, path: str | Path, **kwargs: Any) -> DataFrameLike:
        """Read Parquet file using Polars (lazy by default)."""
        if not self.is_available:
            raise ImportError("Polars is not available")

        # Use lazy scanning for better performance
        return pl.scan_parquet(str(path), **kwargs)  # type: ignore[return-value]

    def read_csv(self, path: str | Path, **kwargs: Any) -> DataFrameLike:
        """Read CSV file using Polars (lazy by default)."""
        if not self.is_available:
            raise ImportError("Polars is not available")

        return pl.scan_csv(str(path), **kwargs)  # type: ignore[return-value]

    def to_pandas(self, df: DataFrameLike) -> pd.DataFrame:
        """Convert Polars DataFrame to pandas."""
        if not self.is_available:
            raise ImportError("Polars is not available")

        if isinstance(df, pl.LazyFrame):
            return df.collect().to_pandas()
        elif isinstance(df, pl.DataFrame):
            return df.to_pandas()
        else:
            # Already pandas or compatible
            return pd.DataFrame(df)  # type: ignore[arg-type,call-overload]

    def compute_if_lazy(self, df: DataFrameLike) -> DataFrameLike:
        """Compute LazyFrame to DataFrame."""
        if not self.is_available:
            raise ImportError("Polars is not available")

        if isinstance(df, pl.LazyFrame):
            return df.collect()  # type: ignore[return-value]
        else:
            return df

    def estimate_memory_usage(self, df: DataFrameLike) -> int:
        """Estimate memory usage in bytes."""
        if not self.is_available:
            return 0

        if isinstance(df, pl.LazyFrame):
            # For lazy frames, we can't easily estimate without computation
            # Return a rough estimate based on scan info if available
            try:
                # Try to get schema info
                schema = df.schema
                # Very rough estimation: assume 100k rows and average 8 bytes per value
                estimated_rows = 100000
                return estimated_rows * len(schema) * 8
            except Exception:
                return 1024 * 1024  # 1MB default

        elif isinstance(df, pl.DataFrame):
            try:
                return df.estimated_size()
            except Exception:
                # Fallback
                return len(df) * len(df.columns) * 8

        return 0

    def from_pandas(self, df: pd.DataFrame) -> "pl.LazyFrame":
        """Convert pandas DataFrame to Polars LazyFrame."""
        if not self.is_available:
            raise ImportError("Polars is not available")

        return pl.from_pandas(df).lazy()
