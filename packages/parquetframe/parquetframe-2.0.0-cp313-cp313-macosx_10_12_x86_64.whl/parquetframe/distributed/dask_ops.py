"""Distributed operations using Dask with Rust acceleration."""

from typing import Any

import pandas as pd

# Dask is optional
try:
    import dask.dataframe as dd
    from dask.distributed import Client

    DASK_AVAILABLE = True
except ImportError:
    DASK_AVAILABLE = False


def distributed_filter(
    data: pd.DataFrame, condition: Any, num_workers: int, rust_threads: int = 8
):
    """
    Distribute filtering across Dask workers with Rust parallel execution.

    Architecture:
    - Data partitioned across N Dask workers
    - Each worker runs Rust-parallel filter (Rayon)
    - Results computed and concatenated

    Args:
        data: Input DataFrame
        condition: Filter condition
        num_workers: Number of Dask workers
        rust_threads: Rayon threads per worker

    Returns:
        Filtered DataFrame
    """
    if not DASK_AVAILABLE:
        raise RuntimeError(
            "Dask not available. Install with: pip install dask[distributed]"
        )

    try:
        Client.current()
    except ValueError:
        raise RuntimeError(
            "Dask client not initialized. Create a Client first"
        ) from None

    # Convert to Dask DataFrame with partitions
    ddf = dd.from_pandas(data, npartitions=num_workers)

    # Apply Rust filter to each partition
    def rust_filter_partition(partition):
        from parquetframe.pf_py import filter_parallel

        return filter_parallel(partition, condition, num_threads=rust_threads)

    # Map operation across partitions
    result_ddf = ddf.map_partitions(rust_filter_partition, meta=data)

    # Compute result
    return result_ddf.compute()


__all__ = ["distributed_filter"]
