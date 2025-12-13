"""
Base cloud handler.
"""

from abc import ABC, abstractmethod
from typing import Union

import pandas as pd

try:
    import polars as pl

    POLARS_AVAILABLE = True
except ImportError:
    pl = None
    POLARS_AVAILABLE = False

try:
    import dask.dataframe as dd

    DASK_AVAILABLE = True
except ImportError:
    dd = None
    DASK_AVAILABLE = False


class CloudHandler(ABC):
    """Abstract base class for cloud storage handlers."""

    @abstractmethod
    def read_parquet(
        self, path: str, backend: str = "pandas", **kwargs
    ) -> Union[pd.DataFrame, "pl.LazyFrame", "dd.DataFrame"]:
        """Read Parquet file from cloud storage."""
        pass

    @abstractmethod
    def write_parquet(
        self, df: Union[pd.DataFrame, "pl.DataFrame"], path: str, **kwargs
    ) -> None:
        """Write DataFrame to cloud storage as Parquet."""
        pass
