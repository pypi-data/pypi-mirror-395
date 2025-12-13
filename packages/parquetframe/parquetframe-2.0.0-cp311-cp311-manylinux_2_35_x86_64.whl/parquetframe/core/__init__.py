"""Core package for ParquetFrame backend abstraction."""

from ..core_legacy import ParquetFrame
from .backend import BackendSelector
from .base import Engine, EngineCapabilities
from .execution import (
    ExecutionContext,
    ExecutionMode,
    ExecutionPlanner,
    get_execution_context,
    set_execution_config,
)
from .formats import FORMAT_HANDLERS, FileFormat, detect_format
from .proxy import DataFrameProxy
from .reader import read, read_avro, read_csv, read_json, read_orc, read_parquet
from .rust_io import RustIO, read_with_backend

__all__ = [
    "ExecutionMode",
    "ExecutionContext",
    "ExecutionPlanner",
    "set_execution_config",
    "get_execution_context",
    "BackendSelector",
    "DataFrameProxy",
    "RustIO",
    "read_with_backend",
    "Engine",
    "EngineCapabilities",
    "ParquetFrame",
    "read",
    "read_csv",
    "read_json",
    "read_parquet",
    "read_orc",
    "read_avro",
    "FORMAT_HANDLERS",
    "FileFormat",
    "detect_format",
]
