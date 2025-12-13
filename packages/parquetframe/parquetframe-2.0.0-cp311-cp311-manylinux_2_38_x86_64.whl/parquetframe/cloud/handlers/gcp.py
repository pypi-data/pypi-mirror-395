"""
Google Cloud Storage (GCS) handler.
"""

from typing import Union

import pandas as pd

from ..config import GCSConfig
from .base import DASK_AVAILABLE, POLARS_AVAILABLE, CloudHandler, dd, pl


class GCSHandler(CloudHandler):
    """
    Handle GCS operations using gcsfs.
    """

    def __init__(self, config: GCSConfig | None = None):
        """Initialize GCS handler."""
        self.config = config or GCSConfig.from_env()

    def read_parquet(
        self, path: str, backend: str = "pandas", **kwargs
    ) -> Union[pd.DataFrame, "pl.LazyFrame", "dd.DataFrame"]:
        """Read Parquet from GCS."""
        storage_options = self.config.to_storage_options()

        if backend == "pandas":
            return pd.read_parquet(path, storage_options=storage_options, **kwargs)
        elif backend == "polars":
            if not POLARS_AVAILABLE:
                raise ImportError("Polars not installed")
            return pl.scan_parquet(path, storage_options=storage_options, **kwargs)
        elif backend == "dask":
            if not DASK_AVAILABLE:
                raise ImportError("Dask not installed")
            return dd.read_parquet(path, storage_options=storage_options, **kwargs)
        else:
            raise ValueError(f"Unknown backend: {backend}")

    def write_parquet(
        self, df: Union[pd.DataFrame, "pl.DataFrame"], path: str, **kwargs
    ):
        """Write DataFrame to GCS as Parquet."""
        storage_options = self.config.to_storage_options()

        if isinstance(df, pd.DataFrame):
            df.to_parquet(path, storage_options=storage_options, **kwargs)
        elif POLARS_AVAILABLE and isinstance(df, pl.DataFrame):
            df.write_parquet(path, storage_options=storage_options, **kwargs)
        else:
            raise TypeError(f"Unsupported DataFrame type: {type(df)}")
