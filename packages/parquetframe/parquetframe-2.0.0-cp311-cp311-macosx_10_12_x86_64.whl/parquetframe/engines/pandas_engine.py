"""
Pandas engine implementation for ParquetFrame Phase 2.

Provides pandas DataFrame engine with consistent interface and optimizations
for small to medium-scale datasets.
"""

from pathlib import Path
from typing import Any

import pandas as pd

from ..core.base import DataFrameLike, Engine


class PandasEngine(Engine):
    """Pandas DataFrame engine implementation."""

    @property
    def name(self) -> str:
        """Engine name."""
        return "pandas"

    @property
    def is_lazy(self) -> bool:
        """Pandas is eager by default."""
        return False

    @property
    def is_available(self) -> bool:
        """Check if pandas is available."""
        try:
            import importlib.util

            return importlib.util.find_spec("pandas") is not None
        except Exception:
            return False

    def read_parquet(self, path: str | Path, **kwargs: Any) -> DataFrameLike:
        """Read Parquet file using pandas."""
        return pd.read_parquet(path, **kwargs)  # type: ignore[return-value]

    def read_csv(self, path: str | Path, **kwargs: Any) -> DataFrameLike:
        """Read CSV file using pandas."""
        return pd.read_csv(path, **kwargs)  # type: ignore[return-value]

    def to_pandas(self, df: DataFrameLike) -> pd.DataFrame:
        """Convert to pandas DataFrame."""
        if isinstance(df, pd.DataFrame):
            return df

        # If it's another engine's DataFrame, try to convert
        if hasattr(df, "to_pandas"):
            return df.to_pandas()

        # Fallback: assume it has pandas-compatible interface
        return pd.DataFrame(df)  # type: ignore[arg-type,call-overload]

    def compute_if_lazy(self, df: DataFrameLike) -> DataFrameLike:
        """No-op for pandas (always eager)."""
        return df

    def estimate_memory_usage(self, df: DataFrameLike) -> int:
        """Estimate memory usage in bytes."""
        try:
            if not isinstance(df, pd.DataFrame):
                df = pd.DataFrame(df)  # type: ignore[arg-type,call-overload]
            return int(df.memory_usage(deep=True).sum())  # type: ignore[attr-defined]
        except Exception:
            # Fallback estimation - assume it has len and columns
            return len(df) * len(df.columns) * 8  # type: ignore[arg-type]

    def from_pandas(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert from pandas (no-op)."""
        return df
