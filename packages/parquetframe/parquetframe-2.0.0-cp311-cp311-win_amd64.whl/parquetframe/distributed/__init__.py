"""Distributed operations package."""

from .dask_ops import distributed_filter as dask_distributed_filter
from .ray_ops import distributed_filter as ray_distributed_filter

__all__ = ["ray_distributed_filter", "dask_distributed_filter"]
