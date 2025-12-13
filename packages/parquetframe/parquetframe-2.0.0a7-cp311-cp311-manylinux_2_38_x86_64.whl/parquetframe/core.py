"""
Unified core module for ParquetFrame.

This module provides the Phase 2 multi-engine DataFrame API as the default,
while maintaining deprecated access to Phase 1 features with warnings.

Phase 2 API (Default):
    - DataFrameProxy: Unified DataFrame interface
    - read(), read_parquet(), read_csv(), etc.: Format-specific readers
    - EngineRegistry: Engine management
    - EngineHeuristics: Intelligent engine selection

Phase 1 API (Deprecated):
    - ParquetFrame: Original DataFrame wrapper (deprecated, use DataFrameProxy)
    - Access via: from parquetframe.core import ParquetFrame (triggers warning)

Examples:
    Phase 2 (Recommended):
        >>> from parquetframe.core import DataFrameProxy, read
        >>> df = read("data.csv")  # Auto-selects optimal engine
        >>> print(f"Using {df.engine_name} engine")

    Phase 1 (Deprecated):
        >>> from parquetframe.core import ParquetFrame  # DeprecationWarning
        >>> df = ParquetFrame.read("data.csv", islazy=True)
"""

import warnings
from typing import Any

# Phase 2 API - Import directly from core/ subdirectory
from .core.base import DataFrameLike, Engine, EngineCapabilities
from .core.frame import DataFrameProxy
from .core.heuristics import EngineHeuristics
from .core.reader import read, read_avro, read_csv, read_json, read_orc, read_parquet
from .core.registry import EngineRegistry

__all__ = [
    # Phase 2 Core types
    "DataFrameLike",
    "Engine",
    "EngineCapabilities",
    # Phase 2 Core classes
    "DataFrameProxy",
    "EngineRegistry",
    "EngineHeuristics",
    # Phase 2 Reader functions
    "read",
    "read_parquet",
    "read_csv",
    "read_json",
    "read_orc",
    "read_avro",
    # Phase 1 (deprecated) - available via __getattr__
    # "ParquetFrame",
]


def __getattr__(name: str) -> Any:
    """
    Provide deprecated access to Phase 1 features.

    This function is called when an attribute is not found in the module's
    normal namespace. It allows Phase 1 features to remain accessible with
    deprecation warnings.

    Args:
        name: Attribute name being accessed

    Returns:
        The requested Phase 1 attribute

    Raises:
        AttributeError: If the attribute doesn't exist in Phase 1 either

    Examples:
        >>> from parquetframe.core import ParquetFrame  # DeprecationWarning
        >>> df = ParquetFrame.read("data.csv")
    """
    # Import Phase 1 module lazily to avoid circular imports
    from . import core_legacy

    # Map of Phase 1 exports that should trigger deprecation warnings
    phase1_exports = {
        "ParquetFrame": core_legacy.ParquetFrame,
        "FileFormat": core_legacy.FileFormat,
        "detect_format": core_legacy.detect_format,
        "IOHandler": core_legacy.IOHandler,
        "ParquetHandler": core_legacy.ParquetHandler,
        "CsvHandler": core_legacy.CsvHandler,
        "JsonHandler": core_legacy.JsonHandler,
        "OrcHandler": core_legacy.OrcHandler,
    }

    if name in phase1_exports:
        warnings.warn(
            "\n"
            "=" * 80 + "\n"
            f"DEPRECATION WARNING: '{name}' (Phase 1 API)\n"
            f"=" * 80 + "\n"
            f"\n"
            f"The Phase 1 API is deprecated as of version 1.0.0 and will be removed\n"
            f"in version 2.0.0 (approximately 6-12 months).\n"
            f"\n"
            f"You are importing '{name}' from 'parquetframe.core', which is now\n"
            f"the Phase 2 multi-engine API. Please migrate to Phase 2:\n"
            f"\n"
            f"  Phase 1 (Deprecated):\n"
            f"    from parquetframe.core import {name}\n"
            f"\n"
            f"  Phase 2 (Recommended):\n"
            f"    from parquetframe.core import DataFrameProxy, read\n"
            f"    # Or from parquetframe import read, DataFrameProxy\n"
            f"\n"
            f"Key API changes:\n"
            f"  - ParquetFrame        →  DataFrameProxy\n"
            f"  - df.islazy          →  df.engine_name\n"
            f"  - df.df              →  df.native\n"
            f"  - islazy=True/False  →  engine='pandas'/'polars'/'dask'\n"
            f"\n"
            f"For detailed migration guide, see:\n"
            f"  - BREAKING_CHANGES.md\n"
            f"  - docs/phase2/MIGRATION_GUIDE.md\n"
            f"\n"
            f"=" * 80 + "\n",
            DeprecationWarning,
            stacklevel=2,
        )
        return phase1_exports[name]

    raise AttributeError(f"module 'parquetframe.core' has no attribute '{name}'")


# Expose Phase 2 as the module-level interface
# This allows: from parquetframe import core; core.read(...)
