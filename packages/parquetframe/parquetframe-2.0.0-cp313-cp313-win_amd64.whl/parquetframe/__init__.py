"""
ParquetFrame: A universal data processing framework with multi-format support.

This package provides seamless switching between pandas, Polars, and Dask DataFrames
based on intelligent engine selection, with automatic format detection for multiple
file types including CSV, JSON, Parquet, ORC, and Avro.

Supported formats:
    - CSV (.csv, .tsv) - Comma or tab-separated values
    - JSON (.json, .jsonl, .ndjson) - Regular or JSON Lines format
    - Parquet (.parquet, .pqt) - Columnar format (optimal performance)
    - ORC (.orc) - Optimized Row Columnar format
    - Avro (.avro) - Schema-rich serialization format (Phase 2+)
    - GraphAr - Graph data in Apache GraphAr format (Phase 1.1+)

Engines:
    - pandas - Eager execution for small datasets (<100MB)
    - Polars - Lazy evaluation for medium datasets (100MB-10GB)
    - Dask - Distributed processing for large datasets (>10GB)

Examples:
    Multi-engine data processing:
        >>> import parquetframe as pf
        >>> df = pf.read("sales.csv")  # Auto-selects optimal engine
        >>> print(f"Using {df.engine_name} engine")  # pandas, polars, or dask
        >>> result = df[df["price"] > 100].groupby("category")["revenue"].sum()

    Graph processing (Phase 1.1+):
        >>> import parquetframe as pf
        >>> graph = pf.graph.read_graph("social_network/")  # GraphAr format
        >>> print(f"Graph: {graph.num_vertices} vertices, {graph.num_edges} edges")
        >>> neighbors = graph.neighbors(vertex_id=123)

    Manual engine control:
        >>> df = pf.read("data.csv", engine="polars")  # Force Polars engine
        >>> df = pf.read("large_data.csv", engine="dask")  # Force Dask

    Configuration:
        >>> pf.set_config(pandas_threshold_mb=50.0, polars_threshold_mb=100.0)
        >>> df = pf.read("data.csv")  # Uses configured thresholds
"""

from pathlib import Path
from typing import Any

from .config import config_context, get_config, reset_config, set_config

# Phase 2 multi-engine core (default as of v1.0.0)
from .core import (
    DataFrameProxy,
    Engine,
    EngineCapabilities,
    read_avro,
    read_csv,
    read_json,
    read_orc,
    read_parquet,
)
from .core import read as _read_v2

# Phase 2 multi-engine components (available for direct import)
try:
    from . import core  # Multi-engine core
except ImportError:
    core = None

# Import submodules
try:
    from . import graph
except ImportError:
    # Graph module not available
    graph = None

try:
    from . import permissions
except ImportError:
    # Permissions module not available
    permissions = None

try:
    from . import entity
except ImportError:
    # Entity framework not available
    entity = None

# Legacy Phase 1 support (deprecated as of v1.0.0)
# Import lazily to avoid triggering warnings unless explicitly used
legacy = None  # Will be imported on first access via __getattr__


# Backward compatibility: ParquetFrame is now DataFrameProxy
ParquetFrame = DataFrameProxy


def create_empty(engine: str = "pandas", **kwargs: Any) -> DataFrameProxy:
    """
    Create an empty DataFrameProxy.

    Args:
        engine: Engine to use ("pandas", "polars", or "dask"). Defaults to "pandas".
        **kwargs: Additional arguments passed to the engine.

    Returns:
        Empty DataFrameProxy with the specified engine.

    Examples:
        >>> import parquetframe as pf
        >>> empty_df = pf.create_empty()
        >>> print(f"Engine: {empty_df.engine_name}")
        Engine: pandas
        >>>
        >>> empty_polars = pf.create_empty(engine="polars")
        >>> print(f"Engine: {empty_polars.engine_name}")
        Engine: polars
    """
    import pandas as pd

    empty_pandas = pd.DataFrame()

    # Convert to appropriate engine type
    if engine == "dask":
        try:
            import dask.dataframe as dd

            empty_dask = dd.from_pandas(empty_pandas, npartitions=1)
            return DataFrameProxy(data=empty_dask, **kwargs)
        except ImportError:
            # Fall back to pandas if dask not available
            pass
    elif engine == "polars":
        try:
            import polars as pl

            empty_polars = pl.DataFrame()
            return DataFrameProxy(data=empty_polars, **kwargs)
        except ImportError:
            # Fall back to pandas if polars not available
            pass

    return DataFrameProxy(data=empty_pandas, **kwargs)


# Convenience function for backward-compatible reading
def read(
    file: str | Path,
    engine: str | None = None,
    **kwargs: Any,
) -> DataFrameProxy:
    """
    Read a data file with automatic format detection and intelligent engine selection.

    This function provides the Phase 2 multi-engine API with automatic selection
    between pandas, Polars, and Dask based on dataset characteristics.

    Args:
        file: Path to the data file. Format auto-detected from extension.
        engine: Force specific engine ("pandas", "polars", or "dask").
                If None, automatically selects optimal engine.
        **kwargs: Additional keyword arguments passed to format-specific readers.

    Returns:
        DataFrameProxy: Unified DataFrame interface with intelligent backend.

    Supported Formats:
        - CSV (.csv, .tsv)
        - JSON (.json, .jsonl, .ndjson)
        - Parquet (.parquet, .pqt)
        - ORC (.orc)
        - Avro (.avro)

    Engine Selection (when engine=None):
        - pandas: < 100MB (eager, rich ecosystem)
        - Polars: 100MB - 10GB (lazy, high performance)
        - Dask: > 10GB (distributed, scalable)

    Examples:
        >>> import parquetframe as pf
        >>> # Automatic engine selection
        >>> df = pf.read("sales.csv")
        >>> print(f"Using {df.engine_name} engine")
        >>>
        >>> # Force specific engine
        >>> df = pf.read("data.parquet", engine="polars")
        >>>
        >>> # Configure thresholds globally
        >>> pf.set_config(pandas_threshold_mb=50.0)
        >>> df = pf.read("medium.csv")  # Uses configured threshold

    Migration from Phase 1:
        Phase 1 code using `islazy` parameter should migrate to `engine` parameter:

        Before (Phase 1):
            >>> df = pf.read("data.csv", islazy=True)  # Force Dask
            >>> if df.islazy:
            >>>     result = df.df.compute()

        After (Phase 2):
            >>> df = pf.read("data.csv", engine="dask")  # Force Dask
            >>> if df.engine_name == "dask":
            >>>     result = df.native.compute()

    See Also:
        - read_csv(): Read CSV files specifically
        - read_parquet(): Read Parquet files specifically
        - read_avro(): Read Avro files specifically
        - parquetframe.legacy: Phase 1 API (deprecated)
    """
    return _read_v2(file, engine=engine, **kwargs)


# Rust backend availability
def rust_available() -> bool:
    """Check if Rust backend is available.

    Returns:
        True if the Rust backend (_rustic module) is successfully loaded.

    Example:
        >>> import parquetframe as pf
        >>> if pf.rust_available():
        ...     print("Rust acceleration enabled")
        ... else:
        ...     print("Using Python fallback")
    """
    try:
        from parquetframe import _rustic

        return _rustic.rust_available()
    except ImportError:
        return False


def rust_version() -> str | None:
    """Get the version of the Rust backend.

    Returns:
        Version string if Rust backend is available, None otherwise.

    Example:
        >>> import parquetframe as pf
        >>> if pf.rust_available():
        ...     print(f"Rust backend version: {pf.rust_version()}")
    """
    try:
        from parquetframe import _rustic

        return _rustic.rust_version()
    except ImportError:
        return None


__version__ = "2.0.0"
__all__ = [
    # Main Phase 2 API
    "DataFrameProxy",
    "ParquetFrame",  # Backward compatibility alias
    "read",
    "create_empty",
    "read_csv",
    "read_parquet",
    "read_json",
    "read_orc",
    "read_avro",
    # Engine types
    "Engine",
    "EngineCapabilities",
    # Configuration
    "get_config",
    "set_config",
    "reset_config",
    "config_context",
    # Rust backend
    "rust_available",
    "rust_version",
    # Submodules
    "graph",
    "permissions",
    "entity",
    "core",
    # Legacy (deprecated)
    "legacy",
]


def __getattr__(name: str) -> Any:
    """
    Lazy loading for submodules to avoid premature deprecation warnings.

    This allows the legacy module to be imported only when explicitly accessed,
    preventing deprecation warnings from appearing when users import Phase 2 APIs.
    """
    global legacy

    if name == "legacy":
        if legacy is None:
            from . import legacy as _legacy

            legacy = _legacy
        return legacy

    raise AttributeError(f"module 'parquetframe' has no attribute '{name}'")
