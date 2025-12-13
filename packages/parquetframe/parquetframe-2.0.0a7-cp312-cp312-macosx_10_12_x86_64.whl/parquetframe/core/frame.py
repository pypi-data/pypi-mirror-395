"""
DataFrameProxy - Unified DataFrame interface for ParquetFrame Phase 2.

Provides a consistent API across pandas, Polars, and Dask DataFrame engines
with intelligent backend selection and seamless engine switching.
"""

from pathlib import Path
from typing import TYPE_CHECKING, Any

from .base import DataFrameLike, Engine
from .registry import EngineRegistry

if TYPE_CHECKING:
    from ..sql import QueryContext, QueryResult, SQLBuilder

try:
    from ..io_new.avro import AvroWriter

    AVRO_AVAILABLE = True
except ImportError:
    AvroWriter = None  # type: ignore[assignment,misc]
    AVRO_AVAILABLE = False


class DataFrameProxy:
    """
    Unified DataFrame interface with intelligent backend selection.

    Acts as a proxy to underlying DataFrame engines (pandas, Polars, Dask)
    providing a consistent API while leveraging engine-specific optimizations.
    """

    def __init__(
        self,
        data: DataFrameLike | None = None,
        engine: str | Engine | None = None,
        **kwargs: Any,
    ):
        """
        Initialize DataFrameProxy.

        Args:
            data: Underlying DataFrame object or None for empty frame
            engine: Engine name or Engine instance to use
            **kwargs: Additional arguments passed to engine
        """
        self._registry = EngineRegistry()
        self._data = data
        self._metadata = kwargs

        if isinstance(engine, str):
            self._engine = self._registry.get_engine(engine)
        elif isinstance(engine, Engine):
            self._engine = engine
        else:
            # Auto-select engine based on data characteristics
            # Use a simple size heuristic without needing engine yet
            data_size = self._estimate_data_size_simple(data) if data is not None else 0
            self._engine = self._registry.select_optimal_engine(
                data_size_bytes=data_size
            )

    @property
    def engine_name(self) -> str:
        """Name of the current engine."""
        return self._engine.name

    @property
    def is_lazy(self) -> bool:
        """Whether the current engine uses lazy evaluation."""
        return self._engine.is_lazy

    @property
    def native(self) -> DataFrameLike | None:
        """Access to underlying native DataFrame object."""
        return self._data

    @property
    def pandas_df(self) -> "DataFrameLike | None":
        """Backward compatibility: get pandas DataFrame representation."""
        if self._data is None:
            return None
        if self.engine_name == "pandas":
            return self._data
        # Convert to pandas if using a different engine
        return self._engine.to_pandas(self._data)

    def head(self, n: int = 5) -> "DataFrameProxy":
        """Return the first n rows."""
        if self._data is None:
            return self

        result = self._data.head(n)
        return DataFrameProxy(data=result, engine=self._engine)

    def tail(self, n: int = 5) -> "DataFrameProxy":
        """Return the last n rows."""
        if self._data is None:
            return self

        result = self._data.tail(n)
        return DataFrameProxy(data=result, engine=self._engine)

    @property
    def shape(self) -> tuple[int, int]:
        """Return (nrows, ncols)."""
        if self._data is None:
            return (0, 0)
        return self._data.shape  # type: ignore[misc,return-value]

    @property
    def columns(self) -> list[str]:
        """Return column names."""
        if self._data is None:
            return []
        # Convert to list for consistency across engines
        cols = self._data.columns  # type: ignore[misc]
        if hasattr(cols, "tolist"):
            return cols.tolist()
        return list(cols)  # type: ignore[call-overload]

    def compute(self) -> "DataFrameProxy":
        """
        Compute result for lazy engines, no-op for eager engines.

        Returns:
            DataFrameProxy with computed result
        """
        if self._data is None:
            return self

        computed_data = self._engine.compute_if_lazy(self._data)
        return DataFrameProxy(data=computed_data, engine=self._engine)

    def to_engine(self, engine_name: str) -> "DataFrameProxy":
        """
        Convert to a different engine.

        Args:
            engine_name: Target engine name ('pandas', 'polars', 'dask')

        Returns:
            New DataFrameProxy using the target engine
        """
        if self._data is None:
            return DataFrameProxy(engine=engine_name)

        target_engine = self._registry.get_engine(engine_name)

        # Convert via pandas as intermediate format
        pandas_df = self._engine.to_pandas(self._data)

        # Convert pandas to target engine
        if target_engine.name == "pandas":
            target_data = pandas_df
        elif target_engine.name == "polars":
            # Will be implemented in polars engine
            target_data = target_engine.from_pandas(pandas_df)  # type: ignore[attr-defined]
        elif target_engine.name == "dask":
            # Will be implemented in dask engine
            target_data = target_engine.from_pandas(pandas_df)  # type: ignore[attr-defined]
        else:
            raise ValueError(f"Unknown target engine: {engine_name}")

        return DataFrameProxy(data=target_data, engine=target_engine)  # type: ignore[arg-type]

    def to_pandas(self) -> "DataFrameProxy":
        """Convert to pandas engine."""
        return self.to_engine("pandas")

    def to_polars(self) -> "DataFrameProxy":
        """Convert to Polars engine."""
        return self.to_engine("polars")

    def to_dask(self) -> "DataFrameProxy":
        """Convert to Dask engine."""
        return self.to_engine("dask")

    def to_avro(
        self,
        path: str | Path,
        schema: dict[str, Any] | None = None,
        codec: str = "deflate",
    ) -> "DataFrameProxy":
        """
        Write DataFrame to Avro file.

        Args:
            path: Output file path
            schema: Avro schema (if None, will be inferred)
            codec: Compression codec ('deflate', 'snappy', 'null')

        Returns:
            Self for method chaining

        Examples:
            >>> df = pf2.read("data.csv")
            >>> df.to_avro("output.avro", codec="snappy")
        """
        if not AVRO_AVAILABLE:
            raise ImportError(
                "fastavro is required for Avro support. "
                "Install with: pip install fastavro"
            )

        if self._data is None:
            raise ValueError("Cannot write empty DataFrameProxy")

        writer = AvroWriter()
        writer.write(self._data, path, schema=schema, codec=codec)

        return self

    def to_orc(
        self,
        path: str | Path,
        **kwargs: Any,
    ) -> "DataFrameProxy":
        """
        Write DataFrame to ORC file.

        Args:
            path: Output file path
            **kwargs: Additional arguments passed to pyarrow.orc.write_table

        Returns:
            Self for method chaining

        Examples:
            >>> df = pf2.read("data.csv")
            >>> df.to_orc("output.orc")
        """
        try:
            import pyarrow as pa
            import pyarrow.orc as orc
        except ImportError as err:
            raise ImportError(
                "pyarrow with ORC support required. Install with: pip install pyarrow"
            ) from err

        if self._data is None:
            raise ValueError("Cannot write empty DataFrameProxy")

        # Convert to pandas first (as common denominator)
        # TODO: Optimize for engines that support Arrow directly
        pandas_df = self._engine.to_pandas(self._data)
        table = pa.Table.from_pandas(pandas_df)

        orc.write_table(table, str(path), **kwargs)

        return self

    def sql(
        self,
        query: str,
        profile: bool = False,
        use_cache: bool = True,
        context: "QueryContext | None" = None,
        **other_frames: "DataFrameProxy",
    ) -> "DataFrameProxy | QueryResult":
        """
        Execute SQL query on this DataFrameProxy using DuckDB.

        The current DataFrameProxy is available as 'df' in the SQL query.
        Additional DataFrameProxy objects can be passed as keyword arguments.

        Args:
            query: SQL query string (main frame available as 'df')
            profile: If True, return QueryResult with execution metadata
            use_cache: Enable query result caching
            context: QueryContext with optimization hints
            **other_frames: Additional DataFrameProxy objects for JOINs

        Returns:
            DataFrameProxy with query results, or QueryResult if profile=True

        Examples:
            >>> df = pf.read("data.csv")
            >>> result = df.sql("SELECT * FROM df WHERE age > 25")
            >>> # Multi-frame join:
            >>> df1 = pf.read("users.csv")
            >>> df2 = pf.read("orders.csv")
            >>> result = df1.sql(
            ...     "SELECT * FROM df JOIN orders ON df.id = orders.user_id",
            ...     orders=df2
            ... )
        """
        from ..sql import query_dataframes

        if self._data is None:
            raise ValueError("Cannot execute SQL on empty DataFrameProxy")

        # Convert main DataFrame to pandas for DuckDB
        # DuckDB also supports dask, but we'll standardize on pandas conversion
        if self.engine_name == "pandas":
            main_df = self._data
        else:
            # Convert to pandas via engine
            main_df = self._engine.to_pandas(self._data)  # type: ignore[attr-defined]

        # Convert other DataFrameProxy objects to pandas DataFrames
        other_dfs = {}
        for name, proxy in other_frames.items():
            if proxy._data is not None:
                if proxy.engine_name == "pandas":
                    other_dfs[name] = proxy._data
                else:
                    other_dfs[name] = proxy._engine.to_pandas(proxy._data)  # type: ignore[attr-defined]

        # Execute query using existing SQL infrastructure
        result = query_dataframes(
            main_df, query, other_dfs, profile, use_cache, context
        )

        # Return QueryResult directly if profiling
        if profile:
            return result  # type: ignore[return-value]

        # Wrap result in DataFrameProxy (always pandas from DuckDB)
        from ..engines.pandas_engine import PandasEngine

        return DataFrameProxy(data=result, engine=PandasEngine())

    def sql_hint(self, **hints: Any) -> "QueryContext":
        """
        Create a QueryContext with optimization hints for SQL queries.

        This is a convenience method for creating QueryContext objects.

        Args:
            **hints: Optimization hints (QueryContext parameters)
                - memory_limit: str (e.g., '1GB')
                - enable_parallel: bool
                - predicate_pushdown: bool
                - projection_pushdown: bool
                - custom_pragmas: dict

        Returns:
            QueryContext object that can be passed to sql()

        Examples:
            >>> df = pf.read("data.csv")
            >>> ctx = df.sql_hint(memory_limit="1GB", enable_parallel=False)
            >>> result = df.sql("SELECT * FROM df", context=ctx)
        """
        from ..sql import QueryContext

        return QueryContext(**hints)

    def sql_with_params(self, query: str, **params: Any) -> "DataFrameProxy":
        """
        Execute a parameterized SQL query.

        Uses named parameters in {param_name} format within the query.

        Args:
            query: SQL query with {param_name} placeholders
            **params: Named parameters to substitute

        Returns:
            DataFrameProxy with query results

        Raises:
            ValueError: If required parameters are missing

        Examples:
            >>> df = pf.read("data.csv")
            >>> result = df.sql_with_params(
            ...     "SELECT * FROM df WHERE age > {min_age} AND salary < {max_salary}",
            ...     min_age=25,
            ...     max_salary=70000
            ... )
        """
        from ..sql import parameterize_query

        # Parameterize the query
        final_query = parameterize_query(query, **params)

        # Execute the parameterized query
        return self.sql(final_query)  # type: ignore[return-value]

    def select(self, *columns: str) -> "SQLBuilder":
        """
        Start building a SQL query with SELECT.

        Returns a SQLBuilder for fluent API query construction.

        Args:
            *columns: Column names to select

        Returns:
            SQLBuilder for method chaining

        Examples:
            >>> df = pf.read("data.csv")
            >>> result = df.select("name", "age").where("age > 25").execute()
            >>> result = df.select("category", "COUNT(*) as count").group_by("category").execute()
        """
        from ..sql import SQLBuilder

        builder = SQLBuilder(self)  # type: ignore[arg-type]
        return builder.select(*columns)

    def where(self, condition: str) -> "SQLBuilder":
        """
        Start building a SQL query with WHERE.

        Returns a SQLBuilder for fluent API query construction.

        Args:
            condition: SQL WHERE condition

        Returns:
            SQLBuilder for method chaining

        Examples:
            >>> df = pf.read("data.csv")
            >>> result = df.where("age > 25").select("name", "age").execute()
        """
        from ..sql import SQLBuilder

        builder = SQLBuilder(self)  # type: ignore[arg-type]
        return builder.where(condition)

    def _estimate_data_size(self, data: DataFrameLike) -> int:
        """Estimate data size in bytes using engine."""
        if data is None:
            return 0
        return self._engine.estimate_memory_usage(data)

    def _estimate_data_size_simple(self, data: DataFrameLike) -> int:
        """Simple data size estimation without needing engine."""
        if data is None:
            return 0

        try:
            # Try to get memory usage directly from DataFrame
            if hasattr(data, "memory_usage"):
                # pandas DataFra me
                return int(data.memory_usage(deep=True).sum())
            elif hasattr(data, "estimated_size"):
                # Polars DataFrame
                return int(data.estimated_size())
            elif hasattr(data, "npartitions"):
                # Dask DataFrame - rough estimate
                return data.npartitions * 10 * 1024 * 1024  # 10MB per partition
            else:
                # Fallback: assume small dataset
                return 1024 * 1024  # 1MB default
        except Exception:
            # If estimation fails, assume small dataset
            return 1024 * 1024  # 1MB default

    def __getattr__(self, name: str) -> Any:
        """
        Delegate attribute access to underlying DataFrame.

        This enables transparent method delegation while wrapping
        DataFrame results back into DataFrameProxy.
        """
        if self._data is None:
            raise AttributeError(
                f"'DataFrameProxy' object (empty) has no attribute '{name}'"
            )

        # Get attribute from underlying DataFrame
        attr = getattr(self._data, name)

        # If it's a callable, wrap it to handle DataFrame returns
        if callable(attr):

            def wrapper(*args: Any, **kwargs: Any) -> Any:
                result = attr(*args, **kwargs)

                # If result is a DataFrame, wrap it in DataFrameProxy
                if self._is_dataframe_like(result):
                    return DataFrameProxy(data=result, engine=self._engine)
                else:
                    # Return scalar or other types as-is
                    return result

            return wrapper
        else:
            # Return non-callable attributes directly
            return attr

    def _is_dataframe_like(self, obj: Any) -> bool:
        """Check if object is a DataFrame-like object."""
        # Check for common DataFrame types
        type_name = type(obj).__name__
        dataframe_types = (
            "DataFrame",
            "LazyFrame",
            "Series",
            "DataFrameGroupBy",
            "SeriesGroupBy",
        )
        return (
            type_name in dataframe_types
            or hasattr(obj, "__dataframe__")
            or (hasattr(obj, "columns") and hasattr(obj, "shape"))
        )

    def __len__(self) -> int:
        """Return number of rows."""
        if self._data is None:
            return 0
        return len(self._data)  # type: ignore[arg-type]

    def __getitem__(self, key: Any) -> Any:
        """
        Support indexing operations (df[column] or df[columns]).
        """
        if self._data is None:
            raise ValueError("Cannot index empty DataFrameProxy")

        result = self._data[key]  # type: ignore[index]

        # Wrap result if it's DataFrame-like
        if self._is_dataframe_like(result):
            return DataFrameProxy(data=result, engine=self._engine)
        else:
            return result

    def __gt__(self, other: Any) -> Any:
        """Support > comparison."""
        if self._data is None:
            raise ValueError("Cannot compare empty DataFrameProxy")
        result = self._data > other
        if self._is_dataframe_like(result):
            return DataFrameProxy(data=result, engine=self._engine)
        return result

    def __lt__(self, other: Any) -> Any:
        """Support < comparison."""
        if self._data is None:
            raise ValueError("Cannot compare empty DataFrameProxy")
        result = self._data < other
        if self._is_dataframe_like(result):
            return DataFrameProxy(data=result, engine=self._engine)
        return result

    def __ge__(self, other: Any) -> Any:
        """Support >= comparison."""
        if self._data is None:
            raise ValueError("Cannot compare empty DataFrameProxy")
        result = self._data >= other
        if self._is_dataframe_like(result):
            return DataFrameProxy(data=result, engine=self._engine)
        return result

    def __le__(self, other: Any) -> Any:
        """Support <= comparison."""
        if self._data is None:
            raise ValueError("Cannot compare empty DataFrameProxy")
        result = self._data <= other
        if self._is_dataframe_like(result):
            return DataFrameProxy(data=result, engine=self._engine)
        return result

    def __eq__(self, other: Any) -> Any:
        """Support == comparison."""
        if self._data is None:
            raise ValueError("Cannot compare empty DataFrameProxy")
        result = self._data == other
        if self._is_dataframe_like(result):
            return DataFrameProxy(data=result, engine=self._engine)
        return result

    def __ne__(self, other: Any) -> Any:
        """Support != comparison."""
        if self._data is None:
            raise ValueError("Cannot compare empty DataFrameProxy")
        result = self._data != other
        if self._is_dataframe_like(result):
            return DataFrameProxy(data=result, engine=self._engine)
        return result

    def __repr__(self) -> str:
        """String representation."""
        if self._data is None:
            return f"DataFrameProxy(engine={self.engine_name}, empty=True)"

        shape_str = f"{self.shape[0]} rows × {self.shape[1]} columns"
        return f"DataFrameProxy(engine={self.engine_name}, {shape_str})"
