"""
Legacy Phase 1 API support (deprecated).

This module provides backward compatibility for Phase 1 API while the project
transitions to Phase 2 multi-engine framework. The Phase 1 API will be removed
in version 2.0.0.

⚠️ DEPRECATION WARNING:
The Phase 1 API is deprecated as of version 1.0.0 and will be removed in version 2.0.0.
Please migrate to the Phase 2 multi-engine API for:
- Better performance (2-5x improvements)
- More engine options (pandas, Polars, Dask)
- Apache Avro support
- Entity-graph framework
- Improved developer experience

Migration Guide:
----------------
Phase 1 (Deprecated):
    >>> from parquetframe.legacy import ParquetFrame
    >>> df = ParquetFrame.read("data.csv", islazy=True)
    >>> if df.islazy:
    >>>     result = df.df.compute()
    >>> else:
    >>>     result = df.df

Phase 2 (Current):
    >>> import parquetframe as pf
    >>> df = pf.read("data.csv", engine="dask")
    >>> if df.engine_name == "dask":
    >>>     result = df.native.compute()
    >>> else:
    >>>     result = df.native

Key Changes:
-----------
- `ParquetFrame` → `DataFrameProxy`
- `.islazy` → `.engine_name`
- `.df` → `.native`
- `islazy=True/False` → `engine="pandas"/"polars"/"dask"`

For detailed migration instructions, see:
- BREAKING_CHANGES.md
- docs/phase2/MIGRATION_GUIDE.md
"""

import warnings
from typing import Any

# Issue deprecation warning when legacy module is imported
warnings.warn(
    "\n"
    "=" * 80 + "\n"
    "DEPRECATION WARNING: Phase 1 API (parquetframe.legacy)\n"
    "=" * 80 + "\n"
    "\n"
    "The Phase 1 API is deprecated as of version 1.0.0 and will be removed\n"
    "in version 2.0.0 (approximately 6-12 months).\n"
    "\n"
    "Please migrate to the Phase 2 multi-engine API:\n"
    "\n"
    "  Before:  from parquetframe.legacy import ParquetFrame\n"
    "  After:   import parquetframe as pf\n"
    "           # Use pf.read(), pf.DataFrameProxy, etc.\n"
    "\n"
    "Key API changes:\n"
    "  - ParquetFrame        →  DataFrameProxy\n"
    "  - df.islazy          →  df.engine_name\n"
    "  - df.df              →  df.native\n"
    "  - islazy=True/False  →  engine='pandas'/'polars'/'dask'\n"
    "\n"
    "For detailed migration guide, see:\n"
    "  - BREAKING_CHANGES.md\n"
    "  - docs/phase2/MIGRATION_GUIDE.md\n"
    "\n"
    "=" * 80 + "\n",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export Phase 1 API from core_legacy
from ..core_legacy import ParquetFrame  # noqa: E402

__all__ = [
    "ParquetFrame",
]


def __getattr__(name: str) -> Any:
    """
    Dynamic attribute access with deprecation warnings.

    This ensures deprecation warnings are shown for any Phase 1 functionality
    accessed through the legacy module.
    """
    # Try to import from core_legacy
    try:
        import importlib

        core_legacy = importlib.import_module("..core_legacy", package=__name__)
        if hasattr(core_legacy, name):
            return getattr(core_legacy, name)
    except ImportError:
        pass

    raise AttributeError(f"module 'parquetframe.legacy' has no attribute '{name}'")
