"""
S3 operations handler.
"""

from typing import Union

import pandas as pd

from ..config import S3Config
from .base import DASK_AVAILABLE, POLARS_AVAILABLE, CloudHandler, dd, pl


class S3Handler(CloudHandler):
    """
    Handle S3 operations with intelligent backend selection.

    Attempts Rust implementation first, falls back to fsspec/s3fs.
    """

    def __init__(self, config: S3Config | None = None):
        """Initialize S3 handler."""
        self.config = config or S3Config.from_env()
        self._rust_available = self._check_rust_s3()

    def _check_rust_s3(self) -> bool:
        """Check if Rust S3 module is available."""
        try:
            from parquetframe import _rustic

            return hasattr(_rustic, "read_parquet_s3_rust")
        except ImportError:
            return False

    def read_parquet(
        self, path: str, backend: str = "pandas", **kwargs
    ) -> Union[pd.DataFrame, "pl.LazyFrame", "dd.DataFrame"]:
        """Read Parquet from S3."""
        # Try Rust implementation first
        if self._rust_available:
            try:
                return self._read_rust(path, backend, **kwargs)
            except Exception as e:
                print(f"Rust S3 read failed, falling back: {e}")

        # Fallback to fsspec
        return self._read_fsspec(path, backend, **kwargs)

    def _read_rust(self, s3_path: str, backend: str, **kwargs):
        """Use Rust S3 reader."""
        from parquetframe._rustic import read_parquet_s3_rust

        arrow_table = read_parquet_s3_rust(
            s3_path,
            access_key=self.config.access_key_id,
            secret_key=self.config.secret_access_key,
            session_token=self.config.session_token,
            region=self.config.region,
        )

        if backend == "pandas":
            return arrow_table.to_pandas()
        elif backend == "polars":
            if not POLARS_AVAILABLE:
                raise ImportError("Polars not installed")
            return pl.from_arrow(arrow_table)
        elif backend == "dask":
            if not DASK_AVAILABLE:
                raise ImportError("Dask not installed")
            pandas_df = arrow_table.to_pandas()
            return dd.from_pandas(pandas_df, npartitions=1)
        else:
            raise ValueError(f"Unknown backend: {backend}")

    def _read_fsspec(self, s3_path: str, backend: str, **kwargs):
        """Fallback to fsspec/s3fs."""
        storage_options = self.config.to_storage_options()

        if backend == "pandas":
            return pd.read_parquet(s3_path, storage_options=storage_options, **kwargs)
        elif backend == "polars":
            if not POLARS_AVAILABLE:
                raise ImportError("Polars not installed")
            return pl.scan_parquet(s3_path, storage_options=storage_options, **kwargs)
        elif backend == "dask":
            if not DASK_AVAILABLE:
                raise ImportError("Dask not installed")
            return dd.read_parquet(s3_path, storage_options=storage_options, **kwargs)
        else:
            raise ValueError(f"Unknown backend: {backend}")

    def write_parquet(
        self, df: Union[pd.DataFrame, "pl.DataFrame"], path: str, **kwargs
    ):
        """Write DataFrame to S3 as Parquet."""
        if self._rust_available:
            try:
                return self._write_rust(df, path, **kwargs)
            except Exception as e:
                print(f"Rust S3 write failed, falling back: {e}")

        return self._write_fsspec(df, path, **kwargs)

    def _write_rust(self, df, s3_path: str, **kwargs):
        """Use Rust S3 writer."""
        from parquetframe._rustic import write_parquet_s3_rust

        if isinstance(df, pd.DataFrame):
            import pyarrow as pa

            arrow_table = pa.Table.from_pandas(df)
        elif POLARS_AVAILABLE and isinstance(df, pl.DataFrame):
            arrow_table = df.to_arrow()
        else:
            raise TypeError(f"Unsupported type: {type(df)}")

        write_parquet_s3_rust(
            arrow_table,
            s3_path,
            access_key=self.config.access_key_id,
            secret_key=self.config.secret_access_key,
            session_token=self.config.session_token,
            region=self.config.region,
        )

    def _write_fsspec(self, df, s3_path: str, **kwargs):
        """Fallback to fsspec for write."""
        storage_options = self.config.to_storage_options()

        if isinstance(df, pd.DataFrame):
            df.to_parquet(s3_path, storage_options=storage_options, **kwargs)
        elif POLARS_AVAILABLE and isinstance(df, pl.DataFrame):
            df.write_parquet(s3_path, storage_options=storage_options, **kwargs)
        else:
            raise TypeError(f"Unsupported DataFrame type: {type(df)}")
