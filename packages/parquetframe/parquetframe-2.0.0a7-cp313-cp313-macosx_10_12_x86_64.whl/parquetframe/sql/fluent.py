"""
Fluent SQL API for ParquetFrame.

Provides builder pattern and helper functions for SQL operations.
"""

import time
from dataclasses import dataclass, field
from typing import Any

import pandas as pd

from .engine import SQLEngine

# Check if DuckDB is available
try:
    import duckdb

    DUCKDB_AVAILABLE = True
except ImportError:
    duckdb = None
    DUCKDB_AVAILABLE = False

# Global query cache for SQLBuilder
_query_cache: dict[str, Any] = {}


@dataclass
class QueryResult:
    """
    Enhanced query result with execution metadata and profiling information.

    Attributes:
        data: The pandas DataFrame result
        execution_time: Query execution time in seconds
        row_count: Number of rows in the result
        column_count: Number of columns in the result
        query: The original SQL query
        from_cache: Whether the result came from cache
        memory_usage: Approximate memory usage in MB
        duckdb_profile: Optional DuckDB query profiling information
        query_plan: Optional query execution plan
    """

    data: pd.DataFrame
    execution_time: float = 0.0
    row_count: int = 0
    column_count: int = 0
    query: str = ""
    from_cache: bool = False
    memory_usage: float | None = None
    duckdb_profile: dict | None = None
    query_plan: str | None = None

    def __post_init__(self):
        """Calculate memory usage after initialization."""
        if self.memory_usage is None:
            try:
                # Estimate memory usage in MB
                self.memory_usage = self.data.memory_usage(deep=True).sum() / (
                    1024 * 1024
                )
            except Exception:
                self.memory_usage = 0.0

        # Backwards compatibility aliases
        self._df = self.data
        self.row_count = len(self.data)
        self.column_count = len(self.data.columns)

    # Convenience properties for easier access
    @property
    def rows(self) -> int:
        """Number of rows in the result."""
        return self.row_count

    @property
    def columns(self) -> int:
        """Number of columns in the result."""
        return self.column_count

    @property
    def cached(self) -> bool:
        """Whether the result came from cache."""
        return self.from_cache

    @property
    def dataframe(self):
        """The result data as a ParquetFrame."""
        from ..legacy import ParquetFrame

        return ParquetFrame(self.data)

    @property
    def memory_usage_mb(self) -> float:
        """Memory usage in MB."""
        return self.memory_usage or 0.0

    def summary(self) -> str:
        """Get a summary of the query execution."""
        cache_info = " (from cache)" if self.from_cache else ""
        return (
            f"Query executed in {self.execution_time:.3f}s{cache_info}\n"
            f"Result: {self.row_count} rows × {self.column_count} columns\n"
            f"Memory usage: {self.memory_usage:.2f} MB"
        )

    def to_pandas(self) -> pd.DataFrame:
        """Convert to pandas DataFrame."""
        return self.data

    def head(self, n: int = 5) -> pd.DataFrame:
        """Return first n rows."""
        return self.data.head(n)

    def count(self) -> int:
        """Return number of rows."""
        return self.row_count


@dataclass
class QueryContext:
    """
    Context object for SQL query execution with optimization hints.

    Attributes:
        format_hints: Format hints for file reading (e.g., {'df': 'csv'})
        predicate_pushdown: Enable predicate pushdown optimization
        projection_pushdown: Enable projection pushdown optimization
        enable_parallel: Enable parallel query execution
        memory_limit: Memory limit for query execution (e.g., '1GB')
        temp_directory: Directory for temporary files
        enable_statistics: Enable query statistics collection
        custom_pragmas: Additional DuckDB PRAGMA statements
    """

    format_hints: dict[str, str] = field(default_factory=dict)
    predicate_pushdown: bool = True
    projection_pushdown: bool = True
    enable_parallel: bool = True
    memory_limit: str | None = None
    temp_directory: str | None = None
    enable_statistics: bool = False
    custom_pragmas: dict[str, Any] = field(default_factory=dict)

    def to_duckdb_pragmas(self) -> list[str]:
        """Convert context to DuckDB PRAGMA statements."""
        pragmas = []

        if not self.predicate_pushdown:
            pragmas.append("PRAGMA enable_optimizer=false")

        if not self.enable_parallel:
            pragmas.append("PRAGMA threads=1")

        if self.memory_limit:
            pragmas.append(f"PRAGMA memory_limit='{self.memory_limit}'")

        if self.temp_directory:
            pragmas.append(f"PRAGMA temp_directory='{self.temp_directory}'")

        if self.enable_statistics:
            pragmas.append("PRAGMA enable_profiling=true")
            pragmas.append("PRAGMA profiling_output='query_profiling.json'")

        # Add custom pragmas
        for pragma, value in self.custom_pragmas.items():
            if value is True:
                pragmas.append(f"PRAGMA {pragma}=true")
            elif value is False:
                pragmas.append(f"PRAGMA {pragma}=false")
            elif value is not None:
                pragmas.append(f"PRAGMA {pragma}='{value}'")

        return pragmas


class SQLBuilder:
    """Fluent builder for SQL queries with join support."""

    def __init__(self, table: Any, engine: SQLEngine | None = None):
        self.table = table  # Can be str or DataFrameProxy/ParquetFrame
        self.engine = engine or SQLEngine()
        self._select = ["*"]
        self._where = []
        self._joins = []
        self._group_by = []
        self._having = []
        self._order_by = []
        self._limit = None
        self._context = None
        self._profile = False
        self._cache = False
        self._cache_store: dict[str, Any] = {}

    def select(self, *columns: str) -> "SQLBuilder":
        """Select columns."""
        self._select = list(columns)
        return self

    def where(self, condition: str) -> "SQLBuilder":
        """Add WHERE clause."""
        self._where.append(condition)
        return self

    def inner_join(self, table: Any, on: str, alias: str = None) -> "SQLBuilder":
        """Add INNER JOIN."""
        self._joins.append(("INNER", table, on, alias))
        return self

    def left_join(self, table: Any, on: str, alias: str = None) -> "SQLBuilder":
        """Add LEFT JOIN."""
        self._joins.append(("LEFT", table, on, alias))
        return self

    def right_join(self, table: Any, on: str, alias: str = None) -> "SQLBuilder":
        """Add RIGHT JOIN."""
        self._joins.append(("RIGHT", table, on, alias))
        return self

    def full_join(self, table: Any, on: str, alias: str = None) -> "SQLBuilder":
        """Add FULL OUTER JOIN."""
        self._joins.append(("FULL OUTER", table, on, alias))
        return self

    def group_by(self, *columns: str) -> "SQLBuilder":
        """Add GROUP BY clause."""
        self._group_by = list(columns)
        return self

    def having(self, condition: str) -> "SQLBuilder":
        """Add HAVING clause."""
        self._having.append(condition)
        return self

    def order_by(self, *args: str) -> "SQLBuilder":
        """Add ORDER BY clause.

        Args can be:
        - Single column: order_by("name")
        - Column with direction: order_by("name", "DESC")
        - Multiple columns: order_by("name", "DESC", "age", "ASC")
        - Expression: order_by("name DESC", "age ASC")
        """
        # Process args to handle (column, direction) pairs
        order_clauses = []
        i = 0
        while i < len(args):
            col = args[i]
            # Check if next arg is a direction (ASC/DESC)
            if i + 1 < len(args) and args[i + 1].upper() in ("ASC", "DESC"):
                direction = args[i + 1].upper()
                order_clauses.append(f"{col} {direction}")
                i += 2
            else:
                # Single column (or already contains direction)
                order_clauses.append(col)
                i += 1
        self._order_by = order_clauses
        return self

    def limit(self, n: int) -> "SQLBuilder":
        """Add LIMIT clause."""
        self._limit = n
        return self

    def hint(self, **kwargs) -> "SQLBuilder":
        """Add optimization hints."""
        self._context = QueryContext(**kwargs)
        return self

    def profile(self, enable: bool = True) -> "SQLBuilder":
        """Enable query profiling."""
        self._profile = enable
        return self

    def cache(self, enable: bool = True) -> "SQLBuilder":
        """Enable query result caching."""
        self._cache = enable
        return self

    def join(
        self,
        table: Any,
        on: str,
        join_type: str = "INNER",
        alias: str | None = None,
    ) -> "SQLBuilder":
        """Add a JOIN clause.

        Args:
            table: Table to join (DataFrame, ParquetFrame, or table name)
            on: Join condition (e.g., "df.id = other.id")
            join_type: Type of join - INNER, LEFT, RIGHT, FULL
            alias: Optional alias for the joined table (defaults to 'other')
        """
        join_type_upper = join_type.upper()
        if join_type_upper == "FULL":
            join_type_upper = "FULL OUTER"
        actual_alias = alias or "other"
        self._joins.append((join_type_upper, table, on, actual_alias))
        return self

    def build(self) -> str:
        """Build SQL query string."""
        # Handle table name if it's a proxy object
        is_obj = (
            hasattr(self.table, "engine_name")
            or hasattr(self.table, "to_pandas")
            or hasattr(self.table, "pandas_df")
            or hasattr(self.table, "_df")
        )
        if is_obj:
            table_name = "df"
        else:
            table_name = str(self.table)

        query = f"SELECT {', '.join(self._select)} FROM {table_name}"

        # Add joins
        for join_type, table, condition, alias in self._joins:
            # If table is an object, use alias or generate name
            is_obj = (
                hasattr(table, "engine_name")
                or hasattr(table, "to_pandas")
                or hasattr(table, "pandas_df")
                or hasattr(table, "_df")
            )
            if is_obj:
                if not alias:
                    # Should have alias if it's an object, otherwise we can't reference it easily
                    # But for now, let's assume user provided alias if needed
                    alias = f"table_{id(table)}"
                table_ref = alias
            else:
                table_ref = str(table)
                if alias:
                    table_ref += f" AS {alias}"

            query += f" {join_type} JOIN {table_ref} ON {condition}"

        # Add WHERE
        if self._where:
            query += f" WHERE {' AND '.join(self._where)}"

        # Add GROUP BY
        if self._group_by:
            query += f" GROUP BY {', '.join(self._group_by)}"

        # Add HAVING
        if self._having:
            query += f" HAVING {' AND '.join(self._having)}"

        # Add ORDER BY
        if self._order_by:
            query += f" ORDER BY {', '.join(self._order_by)}"

        # Add LIMIT
        if self._limit is not None:
            query += f" LIMIT {self._limit}"

        return query

    def execute(self) -> Any:
        """Execute query and return result with optional profiling and caching."""
        import hashlib

        # Handle DataFrameProxy/ParquetFrame input
        table_name = "df"

        # Store object for build() context
        self._execution_table_obj = self.table

        # Remember the input type for proper return type
        input_type = type(self.table).__name__
        is_parquet_frame = input_type == "ParquetFrame"

        # Helper to register a table
        def register_table(obj, name):
            if hasattr(obj, "to_pandas"):
                df = obj.to_pandas()
                if hasattr(df, "native"):
                    df = df.native
            elif hasattr(obj, "pandas_df"):
                df = obj.pandas_df
            elif hasattr(obj, "_df"):
                df = obj._df
            else:
                df = obj

            if hasattr(df, "compute"):
                df = df.compute()

            # Ensure we have a pandas DataFrame
            if isinstance(df, pd.DataFrame):
                self.engine.register_dataframe(name, df)
            else:
                print("Already a pandas DataFrame.")
                self.engine.register_dataframe(name, df)

        # Check if self.table is a proxy/frame object
        is_frame_obj = (
            hasattr(self.table, "pandas_df")
            or hasattr(self.table, "native")
            or hasattr(self.table, "_df")
        )

        if is_frame_obj:
            register_table(self.table, table_name)
        else:
            # It's likely a string table name already registered
            table_name = str(self.table)

        # Register joined tables
        for _, table, _, alias in self._joins:
            is_obj = (
                hasattr(table, "pandas_df")
                or hasattr(table, "native")
                or hasattr(table, "_df")
                or hasattr(table, "to_pandas")
            )
            if is_obj:
                name = alias or f"table_{id(table)}"
                register_table(table, name)

        # Build query
        sql = self.build()

        # Create cache key if caching enabled
        cache_key = None
        if self._cache:
            cache_key = hashlib.md5(sql.encode()).hexdigest()
            if cache_key in _query_cache:
                cached_result = _query_cache[cache_key]
                if self._profile:
                    return QueryResult(
                        cached_result.copy(),
                        execution_time=0.0,
                        query=sql,
                        row_count=len(cached_result),
                        column_count=len(cached_result.columns),
                        from_cache=True,
                    )
                else:
                    if is_parquet_frame:
                        from ..legacy import ParquetFrame

                        return ParquetFrame(cached_result.copy())
                    from ..core.proxy import DataFrameProxy

                    return DataFrameProxy(cached_result.copy(), engine="pandas")

        # Apply context/hints if set
        if self._context and DUCKDB_AVAILABLE:
            import warnings

            pragmas = self._context.to_duckdb_pragmas()
            for pragma in pragmas:
                try:
                    self.engine.query(pragma)
                except Exception as e:
                    warnings.warn(
                        f"Failed to apply optimization hint: {pragma}. {e}",
                        UserWarning,
                        stacklevel=2,
                    )

        # Execute query
        start_time = time.time()
        df = self.engine.query(sql)
        execution_time = time.time() - start_time

        # Store in cache if caching enabled
        if self._cache and cache_key:
            _query_cache[cache_key] = df.copy()

        # Return with profiling if enabled
        if self._profile:
            return QueryResult(
                df,
                execution_time=execution_time,
                query=sql,
                row_count=len(df),
                column_count=len(df.columns),
                from_cache=False,
            )
        else:
            # Return ParquetFrame if input was ParquetFrame, else DataFrameProxy
            if is_parquet_frame:
                from ..legacy import ParquetFrame

                return ParquetFrame(df)
            from ..core.proxy import DataFrameProxy

            return DataFrameProxy(df, engine="pandas")


def explain_query(query: str, engine: SQLEngine | None = None) -> str:
    """Explain query execution plan."""
    engine = engine or SQLEngine()
    # Simple explain implementation
    if DUCKDB_AVAILABLE:
        try:
            result = engine.query(f"EXPLAIN {query}")
            return result.to_string()
        except Exception:
            pass
    return f"EXPLAIN {query}"


def query_dataframes(query: str, **tables) -> pd.DataFrame:
    """
    Execute query on provided DataFrames.

    DEPRECATED: Use parquetframe.sql.engine.query_dataframes instead.
    """
    engine = SQLEngine()
    for name, df in tables.items():
        engine.register_dataframe(name, df)
    return engine.query(query)


def validate_sql_query(query: str) -> bool:
    """Validate SQL syntax (basic check)."""
    return bool(query and isinstance(query, str) and "SELECT" in query.upper())


def build_join_query(
    main_table: str = "df",
    select_cols: list[str] | None = None,
    joins: list[dict] | None = None,
    where_conditions: list[str] | None = None,
    group_by: list[str] | None = None,
    having_conditions: list[str] | None = None,
    order_by: list[str] | None = None,
    limit: int | None = None,
) -> str:
    """
    Build a SQL query with JOIN operations using a structured approach.

    Args:
        main_table: Name of the main table (default "df")
        select_cols: List of columns to select
        joins: List of join dictionaries with 'table', 'condition', 'type' keys
        where_conditions: List of WHERE conditions
        group_by: List of GROUP BY columns
        having_conditions: List of HAVING conditions
        order_by: List of ORDER BY clauses
        limit: LIMIT value

    Returns:
        Complete SQL query string

    Examples:
        >>> joins = [{'table': 'users', 'condition': 'df.user_id = users.id', 'type': 'LEFT'}]
        >>> build_join_query(select_cols=['df.name', 'users.email'], joins=joins)
        "SELECT df.name, users.email FROM df LEFT JOIN users ON df.user_id = users.id"
    """
    parts = []

    # SELECT
    select_clause = "*" if not select_cols else ", ".join(select_cols)
    parts.append(f"SELECT {select_clause}")

    # FROM
    parts.append(f"FROM {main_table}")

    # JOINs
    if joins:
        for join in joins:
            join_type = join.get("type", "INNER").upper()
            if not join_type.endswith("JOIN"):
                join_type = f"{join_type} JOIN"
            parts.append(f"{join_type} {join['table']} ON {join['condition']}")

    # WHERE
    if where_conditions:
        parts.append(f"WHERE {' AND '.join(where_conditions)}")

    # GROUP BY
    if group_by:
        parts.append(f"GROUP BY {', '.join(group_by)}")

    # HAVING
    if having_conditions:
        parts.append(f"HAVING {' AND '.join(having_conditions)}")

    # ORDER BY
    if order_by:
        parts.append(f"ORDER BY {', '.join(order_by)}")

    # LIMIT
    if limit is not None:
        parts.append(f"LIMIT {limit}")

    return " ".join(parts)


__all__ = [
    "QueryResult",
    "QueryContext",
    "SQLBuilder",
    "explain_query",
    "validate_sql_query",
    "build_join_query",
    "query_dataframes",
    "DUCKDB_AVAILABLE",
    "duckdb",
]
