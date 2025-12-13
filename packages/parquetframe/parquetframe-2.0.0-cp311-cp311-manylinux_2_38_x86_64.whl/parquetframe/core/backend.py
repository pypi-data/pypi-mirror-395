"""
Backend selection logic for intelligent engine switching.

Chooses optimal backend based on:
- Data size
- Rust availability
- Distributed cluster availability
"""

import os
from pathlib import Path

import pandas as pd

try:
    import polars as pl

    POLARS_AVAILABLE = True
except ImportError:
    POLARS_AVAILABLE = False
    pl = None

try:
    import dask.dataframe as dd

    DASK_AVAILABLE = True
except ImportError:
    DASK_AVAILABLE = False
    dd = None


class BackendSelector:
    """
    Intelligent backend selection for ParquetFrame.

    Selection criteria:
    1. Data size (small/medium/large)
    2. Rust I/O availability
    3. File format
    4. User preferences
    """

    # Thresholds (GB)
    POLARS_THRESHOLD = 1.0  # Switch to Polars
    DASK_THRESHOLD = 100.0  # Switch to Dask

    @staticmethod
    def check_rust_available() -> bool:
        """Check if Rust backend is compiled and available."""
        import importlib.util

        return importlib.util.find_spec("parquetframe._rustic") is not None

    @staticmethod
    def estimate_size(path: str) -> int:
        """
        Estimate dataset size in bytes.

        For Parquet: uses metadata without reading data
        For others: uses file size
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path not found: {path}")

        # Single file
        if os.path.isfile(path):
            if path.endswith(".parquet"):
                return BackendSelector._parquet_metadata_size(path)
            else:
                return Path(path).stat().st_size

        # Directory of files
        elif os.path.isdir(path):
            total = 0
            for file in Path(path).rglob("*"):
                if file.is_file():
                    total += file.stat().st_size
            return total

        return 0

    @staticmethod
    def _parquet_metadata_size(path: str) -> int:
        """Estimate Parquet size from metadata."""
        try:
            import pyarrow.parquet as pq

            metadata = pq.read_metadata(path)
            # Estimate uncompressed size
            return metadata.num_rows * metadata.num_columns * 8  # Conservative
        except Exception:
            # Fallback to file size
            return Path(path).stat().st_size

    @staticmethod
    def select_backend(
        path: str, user_preference: str | None = None, rust_io: bool = True
    ) -> tuple[str, bool]:
        """
        Select optimal backend for reading data.

        Args:
            path: Path to data file/directory
            user_preference: Optional user-specified backend
            rust_io: Whether to use Rust I/O if available

        Returns:
            (backend_name, use_rust_io) tuple
        """
        # User override
        if user_preference:
            rust_available = BackendSelector.check_rust_available() and rust_io
            return (user_preference, rust_available)

        # Check Rust availability
        rust_available = BackendSelector.check_rust_available() and rust_io

        # Estimate size
        size_bytes = BackendSelector.estimate_size(path)
        size_gb = size_bytes / 1e9

        # File format check
        is_parquet = path.endswith(".parquet") or os.path.isdir(path)

        # Decision matrix
        if size_gb >= BackendSelector.DASK_THRESHOLD:
            # Large data → Dask
            return ("dask", rust_available and is_parquet)

        elif size_gb >= BackendSelector.POLARS_THRESHOLD:
            # Medium data → Polars (if available)
            if POLARS_AVAILABLE:
                return ("polars", rust_available and is_parquet)
            else:
                return ("pandas", rust_available and is_parquet)

        else:
            # Small data → pandas
            return ("pandas", rust_available and is_parquet)

    @staticmethod
    def select_for_dataframe(df) -> str:
        """Select backend for existing DataFrame."""
        if isinstance(df, pd.DataFrame):
            return "pandas"
        elif POLARS_AVAILABLE and isinstance(df, pl.DataFrame | pl.LazyFrame):
            return "polars"
        elif DASK_AVAILABLE and isinstance(df, dd.DataFrame):
            return "dask"
        else:
            raise TypeError(f"Unknown DataFrame type: {type(df)}")


__all__ = ["BackendSelector"]
