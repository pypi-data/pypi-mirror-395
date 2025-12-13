"""
Rust I/O integration with Arrow fast paths.

Provides high-performance I/O using:
- Rust Parquet reader (via PyO3)
- Arrow zero-copy conversion
- Multi-backend output
"""

from typing import Union

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


class RustIO:
    """Rust-accelerated I/O operations."""

    @staticmethod
    def is_available() -> bool:
        """Check if Rust I/O is available."""
        try:
            import parquetframe.pf_py

            return hasattr(parquetframe.pf_py, "read_parquet_rust")
        except ImportError:
            return False

    @staticmethod
    def read_parquet(
        path: str, backend: str = "pandas", **kwargs
    ) -> Union[pd.DataFrame, "pl.LazyFrame", "dd.DataFrame"]:
        """
        Read Parquet using Rust, output to specified backend.

        Flow:
        1. Rust reads Parquet → Arrow Table (zero-copy)
        2. Convert Arrow → target backend

        Args:
            path: Path to Parquet file
            backend: Target backend (pandas/polars/dask)
            **kwargs: Backend-specific options

        Returns:
            DataFrame in target backend format
        """
        if not RustIO.is_available():
            raise RuntimeError("Rust I/O not available")

        # Import Rust module
        from parquetframe.pf_py import read_parquet_rust

        # Rust reads to Arrow (this is fast!)
        arrow_table = read_parquet_rust(path)

        # Convert to target backend
        if backend == "pandas":
            return arrow_table.to_pandas(**kwargs)

        elif backend == "polars":
            if not POLARS_AVAILABLE:
                raise ImportError("Polars not installed")
            # Polars can consume Arrow directly
            return pl.from_arrow(arrow_table)

        elif backend == "dask":
            if not DASK_AVAILABLE:
                raise ImportError("Dask not installed")
            # Convert via pandas (Dask uses pandas partitions)
            pandas_df = arrow_table.to_pandas()
            return dd.from_pandas(pandas_df, npartitions=kwargs.get("npartitions", 1))

        else:
            raise ValueError(f"Unknown backend: {backend}")

    @staticmethod
    def write_parquet(df: Union[pd.DataFrame, "pl.DataFrame"], path: str, **kwargs):
        """
        Write Parquet using Rust for maximum performance.

        Args:
            df: DataFrame to write
            path: Output path
            **kwargs: Write options
        """
        if not RustIO.is_available():
            raise RuntimeError("Rust I/O not available")

        from parquetframe.pf_py import write_parquet_rust

        # Convert to Arrow first
        if isinstance(df, pd.DataFrame):
            import pyarrow as pa

            arrow_table = pa.Table.from_pandas(df)
        elif POLARS_AVAILABLE and isinstance(df, pl.DataFrame):
            arrow_table = df.to_arrow()
        else:
            raise TypeError(f"Unsupported type for Rust write: {type(df)}")

        # Rust writes Arrow table
        write_parquet_rust(arrow_table, path, **kwargs)


def read_with_backend(
    path: str, backend: str, use_rust: bool = True, **kwargs
) -> Union[pd.DataFrame, "pl.LazyFrame", "dd.DataFrame"]:
    """
    Read data using specified backend with optional Rust acceleration.

    Args:
        path: Path to data
        backend: Backend to use (pandas/polars/dask)
        use_rust: Use Rust I/O if available
        **kwargs: Backend-specific options

    Returns:
        DataFrame in requested format
    """
    # Try Rust I/O first if requested
    if use_rust and RustIO.is_available() and path.endswith(".parquet"):
        try:
            return RustIO.read_parquet(path, backend=backend, **kwargs)
        except Exception as e:
            print(f"Rust I/O failed, falling back to native: {e}")

    # Fallback to native readers
    if backend == "pandas":
        return pd.read_parquet(path, **kwargs)

    elif backend == "polars":
        if not POLARS_AVAILABLE:
            raise ImportError("Polars not installed")
        # Use lazy scanning for Polars
        return pl.scan_parquet(path, **kwargs)

    elif backend == "dask":
        if not DASK_AVAILABLE:
            raise ImportError("Dask not installed")
        return dd.read_parquet(path, **kwargs)

    else:
        raise ValueError(f"Unknown backend: {backend}")


__all__ = ["RustIO", "read_with_backend"]
