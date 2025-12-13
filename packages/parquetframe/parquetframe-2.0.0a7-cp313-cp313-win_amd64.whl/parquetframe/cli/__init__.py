"""
CLI utilities for ParquetFrame.
"""

from ..exceptions import (
    check_dependencies,
    format_dependency_status,
    suggest_installation_commands,
)
from .commands import (
    BENCHMARK_AVAILABLE,
    INTERACTIVE_AVAILABLE,
    SQL_AVAILABLE,
    WORKFLOW_AVAILABLE,
    WORKFLOW_HISTORY_AVAILABLE,
    WORKFLOW_VISUALIZATION_AVAILABLE,
    console,
    main,
)
from .repl import start_basic_repl, start_repl

__all__ = [
    "start_repl",
    "start_basic_repl",
    "main",
    "console",
    "check_dependencies",
    "format_dependency_status",
    "suggest_installation_commands",
    "BENCHMARK_AVAILABLE",
    "INTERACTIVE_AVAILABLE",
    "SQL_AVAILABLE",
    "WORKFLOW_AVAILABLE",
    "WORKFLOW_HISTORY_AVAILABLE",
    "WORKFLOW_VISUALIZATION_AVAILABLE",
]
