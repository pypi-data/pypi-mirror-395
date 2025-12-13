"""
Rust backend integration for I/O operations.

This module provides utilities for using the Rust backend for fast Parquet
metadata reading when available, with automatic fallback to Python implementations.
"""

import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Attempt to import Rust backend
try:
    from parquetframe import _rustic

    RUST_IO_AVAILABLE = True
except ImportError:
    RUST_IO_AVAILABLE = False
    _rustic = None

logger.debug(f"Rust I/O backend available: {RUST_IO_AVAILABLE}")


def is_rust_io_available() -> bool:
    """
    Check if Rust I/O backend is available and enabled.

    Considers both compile-time availability and runtime configuration.

    Returns:
        True if Rust backend is compiled and enabled in configuration
    """
    if not RUST_IO_AVAILABLE:
        return False

    # Check configuration
    try:
        from ..config import get_config

        config = get_config()
        return config.rust_io_enabled
    except Exception:
        # If config unavailable, fall back to compile-time check
        return RUST_IO_AVAILABLE


def get_backend_info() -> dict[str, Any]:
    """
    Get comprehensive backend availability information.

    Returns:
        Dictionary with backend status:
            - rust_compiled: bool - Rust backend was compiled
            - rust_io_enabled: bool - Rust I/O is enabled in config
            - rust_io_available: bool - Rust I/O can be used
    """
    try:
        from ..config import get_config

        config = get_config()
        rust_io_enabled = config.rust_io_enabled
    except Exception:
        rust_io_enabled = True  # Default to enabled if config unavailable

    return {
        "rust_compiled": RUST_IO_AVAILABLE,
        "rust_io_enabled": rust_io_enabled,
        "rust_io_available": RUST_IO_AVAILABLE and rust_io_enabled,
    }


def read_parquet_metadata_fast(path: Path) -> dict[str, Any]:
    """
    Read Parquet file metadata using Rust backend.

    This is significantly faster than pyarrow for metadata-only operations.

    Args:
        path: Path to Parquet file

    Returns:
        Dictionary with metadata:
            - num_rows: Number of rows
            - num_row_groups: Number of row groups
            - num_columns: Number of columns
            - file_size_bytes: File size in bytes (if available)
            - version: Parquet version
            - column_names: List of column names
            - column_types: List of column types

    Raises:
        RuntimeError: If Rust backend not available
        ValueError: If file doesn't exist or is invalid
    """
    if not RUST_IO_AVAILABLE:
        raise RuntimeError(
            "Rust I/O backend not available. Install with: pip install parquetframe[rust]"
        )

    path_str = str(path)
    return _rustic.read_parquet_metadata_rust(path_str)


def get_parquet_row_count_fast(path: Path) -> int:
    """
    Get row count from Parquet file (very fast).

    Reads only the file footer, typically completing in milliseconds
    even for multi-GB files.

    Args:
        path: Path to Parquet file

    Returns:
        Number of rows in the file

    Raises:
        RuntimeError: If Rust backend not available
        ValueError: If file doesn't exist or is invalid
    """
    if not RUST_IO_AVAILABLE:
        raise RuntimeError(
            "Rust I/O backend not available. Install with: pip install parquetframe[rust]"
        )

    path_str = str(path)
    return _rustic.get_parquet_row_count_rust(path_str)


def get_parquet_column_names_fast(path: Path) -> list[str]:
    """
    Get column names from Parquet file.

    Args:
        path: Path to Parquet file

    Returns:
        List of column names

    Raises:
        RuntimeError: If Rust backend not available
        ValueError: If file doesn't exist or is invalid
    """
    if not RUST_IO_AVAILABLE:
        raise RuntimeError(
            "Rust I/O backend not available. Install with: pip install parquetframe[rust]"
        )

    path_str = str(path)
    return _rustic.get_parquet_column_names_rust(path_str)


def get_parquet_column_stats_fast(path: Path) -> list[dict[str, Any]]:
    """
    Get column statistics from Parquet file.

    Extracts statistics from metadata including null counts and min/max values.

    Args:
        path: Path to Parquet file

    Returns:
        List of dictionaries with statistics for each column:
            - name: Column name
            - null_count: Number of nulls (if available)
            - distinct_count: Number of distinct values (if available)
            - min_value: Minimum value as string (if available)
            - max_value: Maximum value as string (if available)

    Raises:
        RuntimeError: If Rust backend not available
        ValueError: If file doesn't exist or is invalid
    """
    if not RUST_IO_AVAILABLE:
        raise RuntimeError(
            "Rust I/O backend not available. Install with: pip install parquetframe[rust]"
        )

    path_str = str(path)
    return _rustic.get_parquet_column_stats_rust(path_str)


def try_read_metadata_fast(path: Path) -> dict[str, Any] | None:  # noqa: UP045
    """
    Try to read Parquet metadata using Rust backend.

    Returns None if Rust backend is unavailable or if there's an error.
    Use this for optional fast-path optimizations.

    Args:
        path: Path to Parquet file

    Returns:
        Metadata dictionary or None if unavailable
    """
    if not is_rust_io_available():
        return None

    try:
        return read_parquet_metadata_fast(path)
    except Exception as e:
        logger.debug(f"Rust metadata read failed, falling back: {e}")
        return None


def try_get_row_count_fast(path: Path) -> int | None:  # noqa: UP045
    """
    Try to get row count using Rust backend.

    Returns None if Rust backend is unavailable or if there's an error.

    Args:
        path: Path to Parquet file

    Returns:
        Row count or None if unavailable
    """
    if not is_rust_io_available():
        return None

    try:
        return get_parquet_row_count_fast(path)
    except Exception as e:
        logger.debug(f"Rust row count read failed, falling back: {e}")
        return None


def try_get_column_names_fast(path: Path) -> list[str] | None:  # noqa: UP045
    """
    Try to get column names using Rust backend.

    Returns None if Rust backend is unavailable or if there's an error.

    Args:
        path: Path to Parquet file

    Returns:
        List of column names or None if unavailable
    """
    if not is_rust_io_available():
        return None

    try:
        return get_parquet_column_names_fast(path)
    except Exception as e:
        logger.debug(f"Rust column names read failed, falling back: {e}")
        return None


def try_get_column_stats_fast(
    path: Path,
) -> list[dict[str, Any]] | None:  # noqa: UP045
    """
    Try to get column statistics using Rust backend.

    Returns None if Rust backend is unavailable or if there's an error.

    Args:
        path: Path to Parquet file

    Returns:
        List of column statistics dictionaries or None if unavailable
    """
    if not is_rust_io_available():
        return None

    try:
        return get_parquet_column_stats_fast(path)
    except Exception as e:
        logger.debug(f"Rust column stats read failed, falling back: {e}")
        return None


def get_parquet_info_fast(
    path: Path,
) -> dict[str, Any] | None:  # noqa: UP045
    """
    Get comprehensive Parquet file info using Rust backend with fallback.

    This is a high-level function that tries Rust first, then falls back
    to pyarrow if needed. Returns standardized metadata dict.

    Args:
        path: Path to Parquet file

    Returns:
        Dictionary with file info or None if unavailable:
            - num_rows: int
            - num_columns: int
            - column_names: list[str]
            - column_types: list[str]
            - file_size_bytes: int
            - backend_used: str ("rust" or "pyarrow")
    """
    # Try Rust fast-path first
    metadata = try_read_metadata_fast(path)
    if metadata is not None:
        metadata["backend_used"] = "rust"
        return metadata

    # Fallback to pyarrow
    try:
        import pyarrow.parquet as pq

        parquet_file = pq.ParquetFile(path)
        metadata_obj = parquet_file.metadata
        schema = parquet_file.schema_arrow

        return {
            "num_rows": metadata_obj.num_rows,
            "num_columns": metadata_obj.num_columns,
            "num_row_groups": metadata_obj.num_row_groups,
            "column_names": schema.names,
            "column_types": [str(schema.field(i).type) for i in range(len(schema))],
            "file_size_bytes": path.stat().st_size,
            "version": metadata_obj.format_version,
            "backend_used": "pyarrow",
        }
    except Exception as e:
        logger.debug(f"Parquet metadata read failed: {e}")
        return None
