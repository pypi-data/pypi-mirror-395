"""
SQL API for ParquetFrame.

Provides simple SQL query interface for DataFrames.
"""

from typing import Any

import pandas as pd

from .engine import SQLEngine, query_dataframes
from .fluent import (
    DUCKDB_AVAILABLE,
    QueryContext,
    QueryResult,
    SQLBuilder,
    build_join_query,
    duckdb,
    explain_query,
    validate_sql_query,
)
from .utilities import parameterize_query, query_dataframes_from_files


def sql(query: str, **tables) -> pd.DataFrame:
    """
    Execute SQL query on DataFrames.

    Args:
        query: SQL query string
        **tables: DataFrames to query (name=df pairs)

    Returns:
        Query result as DataFrame

    Example:
        >>> import parquetframe as pf
        >>> import pandas as pd
        >>>
        >>> users = pd.DataFrame({
        ...     'id': [1, 2, 3],
        ...     'name': ['Alice', 'Bob', 'Charlie'],
        ...     'age': [25, 30, 35]
        ... })
        >>>
        >>> result = pf.sql(
        ...     "SELECT name, age FROM users WHERE age > 25",
        ...     users=users
        ... )
    """
    if not tables:
        raise ValueError("At least one DataFrame must be provided")

    # Create engine and register tables
    engine = SQLEngine()
    for name, df in tables.items():
        engine.register_dataframe(name, df)

    # Execute query
    return engine.query(query)


class SQLContext:
    """
    Persistent SQL context for multiple queries.

    Example:
        >>> ctx = SQLContext()
        >>> ctx.register("users", users_df)
        >>> ctx.register("orders", orders_df)
        >>>
        >>> result = ctx.query('''
        ...     SELECT u.name, COUNT(*) as order_count
        ...     FROM users u
        ...     JOIN orders o ON u.id = o.user_id
        ...     GROUP BY u.name
        ... ''')
    """

    def __init__(self):
        """Initialize SQL context."""
        self.engine = SQLEngine()

    def register(self, name: str, df: Any) -> None:
        """Register DataFrame as table."""
        self.engine.register_dataframe(name, df)

    def query(self, sql: str) -> pd.DataFrame:
        """Execute SQL query."""
        return self.engine.query(sql)

    def list_tables(self) -> list[str]:
        """List registered tables."""
        return self.engine.list_tables()

    def unregister(self, name: str) -> None:
        """Remove table from context."""
        self.engine.unregister(name)


__all__ = [
    "sql",
    "SQLContext",
    "SQLEngine",
    "QueryResult",
    "SQLBuilder",
    "QueryContext",
    "explain_query",
    "query_dataframes",
    "validate_sql_query",
    "build_join_query",
    "parameterize_query",
    "query_dataframes_from_files",
    "DUCKDB_AVAILABLE",
    "duckdb",
]
