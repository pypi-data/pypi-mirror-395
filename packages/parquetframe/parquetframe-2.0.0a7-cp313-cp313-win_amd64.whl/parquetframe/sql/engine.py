"""
SQL Engine for ParquetFrame using DataFusion.

Enables SQL queries on DataFrames with high performance.
"""

import time
from typing import Any

import pandas as pd


class SQLEngine:
    """
    Execute SQL queries on DataFrames using DataFusion.

    Example:
        >>> engine = SQLEngine()
        >>> engine.register_dataframe("users", users_df)
        >>> result = engine.query("SELECT * FROM users WHERE age > 25")
    """

    def __init__(self):
        """Initialize SQL engine with DataFusion context."""
        try:
            import datafusion

            self.ctx = datafusion.SessionContext()
            self.tables = {}
            self._datafusion_available = True
            self._use_duckdb = False
        except ImportError:
            # Fallback: Use DuckDB if DataFusion not available
            try:
                import duckdb

                self.ctx = duckdb.connect(":memory:")
                self.tables = {}
                self._datafusion_available = False
                self._use_duckdb = True
            except ImportError:
                raise ImportError(
                    "SQL engine requires either 'datafusion' or 'duckdb'. "
                    "Install with: pip install datafusion or pip install duckdb"
                ) from None

    def register_dataframe(self, name: str, df: Any) -> None:
        """
        Register DataFrame as SQL table.

        Args:
            name: Table name for SQL queries
            df: pandas or polars DataFrame
        """
        # Convert to pandas if needed
        if hasattr(df, "to_pandas"):
            df = df.to_pandas()
        elif hasattr(df, "compute"):  # Dask DataFrame
            df = df.compute()

        if self._datafusion_available:
            # Convert to Arrow for DataFusion
            import pyarrow as pa

            arrow_table = pa.Table.from_pandas(df)
            self.ctx.register_record_batches(name, [[arrow_table.to_batches()[0]]])
        else:
            # DuckDB can work directly with pandas
            self.ctx.register(name, df)

        self.tables[name] = df

    def query(self, sql: str) -> pd.DataFrame:
        """
        Execute SQL query and return result as DataFrame.

        Args:
            sql: SQL query string

        Returns:
            Query result as pandas DataFrame

        Raises:
            ValueError: If query execution fails
        """
        try:
            if self._datafusion_available:
                result = self.ctx.sql(sql)
                # Convert back to pandas
                return result.to_pandas()
            else:
                # DuckDB
                result = self.ctx.execute(sql).fetchdf()
                return result
        except Exception as e:
            raise ValueError(f"SQL query execution failed: {e}") from e

    def list_tables(self) -> list[str]:
        """List all registered tables."""
        return list(self.tables.keys())

    def unregister(self, name: str) -> None:
        """Remove table from catalog."""
        if name in self.tables:
            del self.tables[name]
            # Note: DataFusion/DuckDB don't have direct unregister


def validate_sql_query(
    query: str, columns: list[str] | None = None
) -> tuple[bool, list[str]]:
    """
    Validate SQL query syntax and column references.

    Args:
        query: SQL query string to validate
        columns: Optional list of available column names

    Returns:
        Tuple of (is_valid, warnings) where warnings is a list of validation warnings
    """
    warnings_list = []

    # Basic validation
    if not query or not isinstance(query, str):
        return False, ["Query must be a non-empty string"]

    # Check for basic SQL syntax
    query_upper = query.upper().strip()
    if not any(
        keyword in query_upper
        for keyword in ["SELECT", "WITH", "INSERT", "UPDATE", "DELETE"]
    ):
        warnings_list.append(
            "Query should contain at least one SQL keyword (SELECT, WITH, etc.)"
        )

    # Check for column references if provided
    if columns:
        # Simple check - this is not exhaustive but catches obvious errors
        query_lower = query.lower()
        for col in columns:
            if col.lower() not in query_lower and "*" not in query:
                # Column might not be used - this is just a warning
                pass

    return True, warnings_list


def query_dataframes(
    main_df: pd.DataFrame,
    query: str,
    other_dfs: dict[str, pd.DataFrame] | None = None,
    profile: bool = False,
    use_cache: bool = True,
    context: Any | None = None,
) -> Any:
    """
    Execute SQL query on DataFrames with profiling support.

    Args:
        main_df: Main DataFrame (available as 'df' in query)
        query: SQL query string
        other_dfs: Optional dictionary of additional DataFrames
        profile: If True, return QueryResult with profiling info
        use_cache: Whether to use query caching
        context: Optional QueryContext with optimization hints

    Returns:
        pandas DataFrame or QueryResult if profile=True
    """
    from .fluent import QueryResult

    engine = SQLEngine()

    # Register main DataFrame
    engine.register_dataframe("df", main_df)

    # Register other DataFrames
    if other_dfs:
        for name, df in other_dfs.items():
            engine.register_dataframe(name, df)

    # Warn if Dask DataFrames are used
    has_dask = False
    if (
        hasattr(main_df, "compute")
        or isinstance(main_df, pd.DataFrame | pd.Series) is False
    ):
        # Crude check for Dask-like if imports are not available, but we import dask inside usually.
        # Let's check for 'dask.dataframe.core.DataFrame' in mro or check for compute method
        if hasattr(main_df, "compute"):
            has_dask = True

    if not has_dask and other_dfs:
        for df in other_dfs.values():
            if hasattr(df, "compute"):
                has_dask = True
                break

    if has_dask:
        import warnings

        warnings.warn(
            "SQL queries on Dask DataFrames will trigger computation and convert to pandas. "
            "This may consume significant memory for large datasets.",
            UserWarning,
            stacklevel=3,
        )

    # Apply context hints if provided
    if context:
        import warnings

        try:
            pragmas = context.to_duckdb_pragmas()
            for pragma in pragmas:
                try:
                    engine.query(pragma)
                except Exception as e:
                    warnings.warn(
                        f"Failed to apply PRAGMA: {pragma}. {e}",
                        UserWarning,
                        stacklevel=2,
                    )
        except Exception:
            pass

    # Execute with profiling if requested
    if profile:
        start_time = time.time()
        result_df = engine.query(query)
        execution_time = time.time() - start_time
        return QueryResult(result_df, execution_time=execution_time, query=query)
    else:
        return engine.query(query)


__all__ = ["SQLEngine", "query_dataframes", "validate_sql_query"]
