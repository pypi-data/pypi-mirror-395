"""
Cloud integration module.

Provides unified API for cloud storage operations (S3, GCS, Azure).
"""

from typing import TYPE_CHECKING, Union

import pandas as pd

from .config import AzureConfig, GCSConfig, S3Config
from .factory import CloudFactory
from .handlers.azure import AzureHandler
from .handlers.gcp import GCSHandler
from .handlers.s3 import S3Handler

if TYPE_CHECKING:
    import dask.dataframe as dd
    import polars as pl

# Type alias for DataFrames
DataFrameType = Union[pd.DataFrame, "pl.DataFrame", "pl.LazyFrame", "dd.DataFrame"]


def read_parquet_cloud(path: str, backend: str = "pandas", **kwargs) -> DataFrameType:
    """
    Read Parquet file from cloud storage.

    Automatically detects protocol (s3://, gs://, az://).

    Args:
        path: Cloud URI
        backend: Target backend (pandas/polars/dask)
        **kwargs: Additional options passed to reader

    Returns:
        DataFrame in requested backend format
    """
    handler = CloudFactory.get_handler(path)
    return handler.read_parquet(path, backend=backend, **kwargs)


def write_parquet_cloud(df: DataFrameType, path: str, **kwargs) -> None:
    """
    Write DataFrame to cloud storage as Parquet.

    Automatically detects protocol (s3://, gs://, az://).

    Args:
        df: DataFrame to write
        path: Target Cloud URI
        **kwargs: Additional options passed to writer
    """
    handler = CloudFactory.get_handler(path)
    handler.write_parquet(df, path, **kwargs)


# Backward compatibility aliases
read_parquet_s3 = read_parquet_cloud
write_parquet_s3 = write_parquet_cloud


__all__ = [
    "read_parquet_cloud",
    "write_parquet_cloud",
    "read_parquet_s3",
    "write_parquet_s3",
    "S3Config",
    "GCSConfig",
    "AzureConfig",
    "S3Handler",
    "GCSHandler",
    "AzureHandler",
    "CloudFactory",
]
