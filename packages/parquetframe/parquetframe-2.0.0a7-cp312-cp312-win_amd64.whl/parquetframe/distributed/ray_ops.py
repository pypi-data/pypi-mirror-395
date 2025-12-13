"""Distributed operations using Ray with Rust acceleration."""

from typing import Any

import pandas as pd

# Ray is optional
try:
    import ray

    RAY_AVAILABLE = True
except ImportError:
    RAY_AVAILABLE = False


@ray.remote
class RustFilterWorker:
    """
    Ray actor that wraps Rust parallel operations.

    Each worker runs Rust-parallel filtering using Rayon,
    enabling distributed + parallel execution.
    """

    def filter(self, data_partition, condition, rust_threads: int):
        """
        Filter partition using Rust parallel execution.

        Args:
            data_partition: DataFrame partition
            condition: Filter condition
            rust_threads: Number of Rayon threads per worker

        Returns:
            Filtered partition
        """
        from parquetframe.pf_py import filter_parallel

        return filter_parallel(data_partition, condition, num_threads=rust_threads)


def distributed_filter(
    data: pd.DataFrame, condition: Any, num_nodes: int, rust_threads: int = 8
):
    """
    Distribute filtering across Ray workers with Rust parallel execution.

    Architecture:
    - Data partitioned across N Ray workers
    - Each worker runs Rust-parallel filter (Rayon)
    - Results gathered and concatenated

    Args:
        data: Input DataFrame
        condition: Filter condition
        num_nodes: Number of Ray workers
        rust_threads: Rayon threads per worker

    Returns:
        Filtered DataFrame
    """
    if not RAY_AVAILABLE:
        raise RuntimeError("Ray not available. Install with: pip install ray")

    if not ray.is_initialized():
        raise RuntimeError("Ray not initialized. Call ray.init() first")

    # Partition data
    partitions = partition_dataframe(data, num_nodes)

    # Create Ray actors (one per node)
    workers = [RustFilterWorker.remote() for _ in range(num_nodes)]

    # Distribute work (Rust parallel within each worker)
    futures = [
        workers[i].filter.remote(partitions[i], condition, rust_threads)
        for i in range(num_nodes)
    ]

    # Gather results
    results = ray.get(futures)
    return concat_partitions(results)


def partition_dataframe(df: pd.DataFrame, num_partitions: int):
    """Partition DataFrame into roughly equal chunks."""
    chunk_size = len(df) // num_partitions
    partitions = []

    for i in range(num_partitions):
        start = i * chunk_size
        end = start + chunk_size if i < num_partitions - 1 else len(df)
        partitions.append(df.iloc[start:end])

    return partitions


def concat_partitions(partitions):
    """Concatenate partition results."""
    return pd.concat(partitions, ignore_index=True)


__all__ = ["distributed_filter", "RustFilterWorker"]
