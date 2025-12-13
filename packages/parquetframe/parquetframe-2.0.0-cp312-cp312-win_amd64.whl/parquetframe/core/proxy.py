"""
DataFrameProxy: Unified DataFrame wrapper with Rust-first execution.

Provides:
- Narwhals-based backend compatibility (pandas/Polars/Dask)
- Rust-accelerated operations with GIL release
- Execution mode support (local/distributed/hybrid)
- Zero-overhead delegation
"""

from typing import Any, Union

import pandas as pd

try:
    import polars as pl

    POLARS_AVAILABLE = True
except ImportError:
    POLARS_AVAILABLE = False
    pl = None

try:
    import dask.dataframe as dd

    DASK_AVAILABLE = True
except ImportError:
    DASK_AVAILABLE = False
    dd = None

try:
    import narwhals as nw

    NARWHALS_AVAILABLE = True
except ImportError:
    NARWHALS_AVAILABLE = False
    nw = None

from .execution import ExecutionContext, ExecutionMode, get_execution_context


class DataFrameProxy:
    """
    Unified DataFrame wrapper with Rust-first design.

    Operations automatically choose between:
    - Rust parallel (PyO3 + Rayon)
    - Rust distributed (Ray workers + Rayon)
    - Narwhals backend-agnostic (fallback)

    Examples:
        # Auto-detect execution mode
        >>> proxy = DataFrameProxy(df)
        >>> result = proxy.filter(condition)

        # Explicit distributed mode
        >>> proxy = DataFrameProxy(df, execution_mode="distributed")
        >>> result = proxy.join(other, on="id")
    """

    def __init__(
        self,
        native_df: Union[pd.DataFrame, "pl.DataFrame", "dd.DataFrame"] = None,
        execution_ctx: ExecutionContext | None = None,
        execution_mode: str | None = None,
        data: Union[pd.DataFrame, "pl.DataFrame", "dd.DataFrame"] = None,
        engine: str | None = None,
    ):
        """
        Initialize DataFrameProxy.

        Args:
            native_df: Native DataFrame (pandas/Polars/Dask)
            execution_ctx: Optional execution context
            execution_mode: Optional mode override (auto/local/distributed/hybrid)
            data: Alias for native_df (for backward compatibility)
            engine: Optional engine name (pandas/polars/dask)
        """
        if native_df is None and data is not None:
            native_df = data

        if native_df is None:
            # Handle empty init
            self._native = None
            self._backend = engine if engine else "pandas"  # Default to pandas if empty
            self._nw = None
            self._exec_ctx = execution_ctx or ExecutionContext.auto_detect(0, 1)
            self._rust_available = self._check_rust_available()
            return

        self._native = native_df
        self._backend = self._detect_backend(native_df)

        # Initialize narwhals wrapper if available and supported
        if NARWHALS_AVAILABLE and self._is_narwhals_supported(native_df):
            try:
                self._nw = nw.from_native(native_df)
            except Exception:
                self._nw = None
        else:
            self._nw = None

        # Setup execution context
        if execution_mode:
            self._exec_ctx = get_execution_context().resolve(execution_mode)
        elif execution_ctx:
            self._exec_ctx = execution_ctx
        else:
            # Auto-detect based on data size
            size_gb = self._estimate_size_gb()
            from .execution import ExecutionPlanner

            available, num_nodes = ExecutionPlanner.check_distributed_available()
            self._exec_ctx = ExecutionContext.auto_detect(size_gb, num_nodes)

        # Check if Rust backend available
        self._rust_available = self._check_rust_available()

    def _detect_backend(self, df) -> str:
        """Detect backend type."""
        if isinstance(df, pd.DataFrame | pd.Series):
            return "pandas"
        elif POLARS_AVAILABLE and isinstance(
            df, pl.DataFrame | pl.LazyFrame | pl.Series
        ):
            return "polars"
        elif DASK_AVAILABLE and isinstance(df, dd.DataFrame | dd.Series):
            return "dask"

        # Check for GroupBy objects
        type_name = type(df).__name__
        if "GroupBy" in type_name:
            # Try to infer from module
            module = type(df).__module__
            if "pandas" in module:
                return "pandas"
            if "polars" in module:
                return "polars"
            if "dask" in module:
                return "dask"

        # Fallback or error
        if hasattr(df, "to_pandas"):  # Polars/Arrow objects often have this
            return "polars"

        # If we can't detect, assume pandas if it looks like it, or raise error
        # But for now, let's be permissive for wrapped objects
        return "pandas"

    def _is_narwhals_supported(self, df) -> bool:
        """Check if object is supported by narwhals."""
        # Narwhals mainly supports DataFrames and LazyFrames
        if isinstance(df, pd.DataFrame):
            return True
        if POLARS_AVAILABLE and isinstance(df, pl.DataFrame | pl.LazyFrame):
            return True
        if DASK_AVAILABLE and isinstance(df, dd.DataFrame):
            return True
        return False

    def _check_rust_available(self) -> bool:
        """Check if Rust backend is available."""
        import importlib.util

        return importlib.util.find_spec("parquetframe._rustic") is not None

    def _estimate_size_gb(self) -> float:
        """Estimate DataFrame size in GB."""
        try:
            if self._backend == "pandas":
                if hasattr(self._native, "memory_usage"):
                    return self._native.memory_usage(deep=True).sum() / 1e9
            elif self._backend == "polars":
                if hasattr(self._native, "estimated_size"):
                    return self._native.estimated_size() / 1e9
            elif self._backend == "dask":
                # Estimate from metadata
                if hasattr(self._native, "memory_usage"):
                    return self._native.memory_usage(deep=True).sum().compute() / 1e9
        except Exception:
            pass
        return 0.1  # Conservative fallback

    # =========================================================================
    # Rust-Accelerated Operations (Bypass Narwhals)
    # =========================================================================

    def filter_rust(self, condition):
        """
        Rust-accelerated filter with execution mode support.

        Chooses between:
        - Local parallel (Rayon)
        - Distributed (Ray/Dask + Rayon)

        Args:
            condition: Filter condition

        Returns:
            New DataFrameProxy with filtered data
        """
        if not self._rust_available:
            return self.filter(condition)  # Fallback to narwhals

        if self._exec_ctx.mode == ExecutionMode.DISTRIBUTED:
            return self._filter_distributed_rust(condition)
        else:
            return self._filter_local_rust(condition)

    def _filter_local_rust(self, condition):
        """Rust parallel filter (Rayon)."""
        from parquetframe._rustic import filter_parallel

        result = filter_parallel(
            self._native, condition, num_threads=self._exec_ctx.rust_threads or 0
        )
        return DataFrameProxy(result, self._exec_ctx)

    def _filter_distributed_rust(self, condition):
        """Distributed Rust filter (Ray/Dask workers)."""
        if self._exec_ctx.distributed_backend == "ray":
            from parquetframe.distributed.ray_ops import distributed_filter

            result = distributed_filter(
                self._native,
                condition,
                num_nodes=self._exec_ctx.distributed_nodes,
                rust_threads=self._exec_ctx.rust_threads,
            )
        else:
            from parquetframe.distributed.dask_ops import distributed_filter

            result = distributed_filter(
                self._native,
                condition,
                num_workers=self._exec_ctx.distributed_nodes,
                rust_threads=self._exec_ctx.rust_threads,
            )

        return DataFrameProxy(result, self._exec_ctx)

    # =========================================================================
    # Narwhals-Based Operations (Backend Agnostic)
    # =========================================================================

    def filter(self, *predicates):
        """
        Generic filter using narwhals.

        Provides backend-agnostic filtering when Rust not available
        or for complex predicates.
        """
        if not NARWHALS_AVAILABLE:
            raise RuntimeError(
                "Narwhals not available. Install with: pip install narwhals"
            )

        result = self._nw.filter(*predicates)
        return DataFrameProxy(result.to_native(), self._exec_ctx)

    def select(self, *cols):
        """
        Start fluent SQL query with SELECT.

        This returns a SQLBuilder for method chaining.
        For direct column selection without SQL, use df[['col1', 'col2']] syntax.
        """
        from parquetframe.sql import SQLBuilder

        return SQLBuilder(self).select(*cols)

    def where(self, condition: str):
        """
        Start fluent SQL query with WHERE condition.

        Args:
            condition: SQL WHERE condition string

        Returns:
            SQLBuilder for method chaining
        """
        from parquetframe.sql import SQLBuilder

        return SQLBuilder(self).where(condition)

    def group_by(self, *cols):
        """
        Start fluent SQL query with GROUP BY.

        Returns:
            SQLBuilder for method chaining
        """
        from parquetframe.sql import SQLBuilder

        return SQLBuilder(self).group_by(*cols)

    def order_by(self, *args):
        """
        Start fluent SQL query with ORDER BY.

        Returns:
            SQLBuilder for method chaining
        """
        from parquetframe.sql import SQLBuilder

        return SQLBuilder(self).order_by(*args)

    # =========================================================================
    # Properties and Utilities
    # =========================================================================

    @property
    def native(self):
        """Get the underlying native DataFrame."""
        return self._native

    @property
    def backend(self) -> str:
        """Get backend name."""
        return self._backend

    @property
    def engine_name(self) -> str:
        """Get backend engine name (alias for backend)."""
        return self._backend

    @property
    def execution_mode(self):
        """Get execution mode."""
        return self._exec_ctx.mode

    @property
    def is_lazy(self) -> bool:
        """Check if the underlying DataFrame is lazy."""
        if self._native is None:
            return False
        if self._backend == "dask":
            return True
        if self._backend == "polars" and isinstance(self._native, pl.LazyFrame):
            return True
        return False

    @property
    def columns(self) -> list[str]:
        """Get column names."""
        if self._native is None:
            return []
        if hasattr(self._native, "columns"):
            return list(self._native.columns)
        if self._backend == "polars" and isinstance(self._native, pl.LazyFrame):
            return self._native.collect_schema().names()
        return []

    def __len__(self) -> int:
        """Get number of rows."""
        if self._native is None:
            return 0
        if self._backend == "pandas":
            return len(self._native)
        if self._backend == "polars":
            if isinstance(self._native, pl.LazyFrame):
                # This might be expensive, but __len__ implies eager
                return self._native.collect().height
            return self._native.height
        if self._backend == "dask":
            return len(self._native)
        return 0

    def to_pandas(self) -> "DataFrameProxy":
        """Convert to pandas backend."""
        if self._native is None:
            return self
        if self._backend == "pandas":
            return self

        if self._backend == "polars":
            if isinstance(self._native, pl.LazyFrame):
                return DataFrameProxy(
                    self._native.collect().to_pandas(), self._exec_ctx
                )
            return DataFrameProxy(self._native.to_pandas(), self._exec_ctx)

        if self._backend == "dask":
            return DataFrameProxy(self._native.compute(), self._exec_ctx)

        return self

    def to_polars(self) -> "DataFrameProxy":
        """Convert to Polars backend."""
        if not POLARS_AVAILABLE:
            raise ImportError("Polars not available")
        if self._native is None:
            return self
        if self._backend == "polars":
            return self

        if self._backend == "pandas":
            return DataFrameProxy(pl.from_pandas(self._native), self._exec_ctx)

        if self._backend == "dask":
            # Compute first
            return DataFrameProxy(
                pl.from_pandas(self._native.compute()), self._exec_ctx
            )

        return self

    def to_dask(self, npartitions=None) -> "DataFrameProxy":
        """Convert to Dask backend."""
        if not DASK_AVAILABLE:
            raise ImportError("Dask not available")
        if self._native is None:
            return self
        if self._backend == "dask":
            return self

        if self._backend == "pandas":
            return DataFrameProxy(
                dd.from_pandas(self._native, npartitions=npartitions or 1),
                self._exec_ctx,
            )

        if self._backend == "polars":
            # Convert to pandas first (expensive)
            pdf = self.to_pandas().native
            return DataFrameProxy(
                dd.from_pandas(pdf, npartitions=npartitions or 1), self._exec_ctx
            )

        return self

    def compute(self) -> "DataFrameProxy":
        """Compute lazy DataFrame."""
        if self._native is None:
            return self
        if self._backend == "dask":
            return DataFrameProxy(self._native.compute(), self._exec_ctx)
        if self._backend == "polars" and isinstance(self._native, pl.LazyFrame):
            return DataFrameProxy(self._native.collect(), self._exec_ctx)
        return self

    def to_avro(self, path, **kwargs):
        """Write to Avro file."""
        if self._native is None:
            raise ValueError("Cannot write empty DataFrameProxy")

        try:
            import fastavro
        except ImportError as e:
            raise ImportError("fastavro required for Avro support") from e

        # Simple pandas implementation for now
        df = self.to_pandas().native
        records = df.to_dict("records")

        # Infer schema if not provided
        schema = kwargs.get("schema")
        if not schema:
            # Basic schema inference
            from parquetframe.io_new.avro import infer_avro_schema

            schema = infer_avro_schema(df)

        with open(path, "wb") as out:
            fastavro.writer(out, schema, records, codec=kwargs.get("codec", "null"))

        return self

    @property
    def pandas_df(self) -> pd.DataFrame:
        """Get the underlying pandas DataFrame (converting if necessary)."""
        return self.to_pandas().native

    def sql(
        self,
        query: str,
        profile: bool = False,
        use_cache: bool = True,
        context: Any = None,
        **other_frames,
    ):
        """
        Execute a SQL query on this DataFrame.

        Args:
            query: SQL query string
            profile: Whether to enable profiling
            use_cache: Whether to use query cache
            context: Optional QueryContext
            **other_frames: Additional DataFrames for JOINs

        Returns:
            Result DataFrameProxy or QueryResult
        """
        from parquetframe.sql import QueryResult, query_dataframes

        # Convert other_frames to native if they are proxies
        native_others = {}
        for name, frame in other_frames.items():
            if isinstance(frame, DataFrameProxy):
                native_others[name] = frame.native
            else:
                native_others[name] = frame

        result = query_dataframes(
            self._native,
            query,
            other_dfs=native_others,
            profile=profile,
            use_cache=use_cache,
            context=context,
        )

        if isinstance(result, QueryResult):
            return result

        return DataFrameProxy(result, self._exec_ctx)

    def sql_with_params(self, query: str, **params):
        """
        Execute a parameterized SQL query.

        Args:
            query: SQL query template
            **params: Parameters to substitute

        Returns:
            Result DataFrameProxy
        """
        from parquetframe.sql import parameterize_query

        final_query = parameterize_query(query, **params)
        return self.sql(final_query)

    def sql_hint(self, **hints):
        """
        Create a QueryContext with optimization hints.

        Args:
            **hints: Optimization hints

        Returns:
            QueryContext object
        """
        from parquetframe.sql import QueryContext

        return QueryContext(**hints)

    def sql_builder(self):
        """
        Create a SQLBuilder for fluent query construction.

        Returns:
            SQLBuilder instance
        """
        from parquetframe.sql import SQLBuilder

        return SQLBuilder(self)

    def set_execution_mode(self, mode: str):
        """Change execution mode for this proxy."""
        self._exec_ctx = self._exec_ctx.resolve(mode)
        return self

    def collect(self):
        """
        Materialize lazy operations.

        For Polars LazyFrame or Dask DataFrame.
        """
        if isinstance(self._native, pl.LazyFrame):
            return DataFrameProxy(self._native.collect(), self._exec_ctx)
        elif DASK_AVAILABLE and isinstance(self._native, dd.DataFrame):
            return DataFrameProxy(self._native.compute(), self._exec_ctx)
        return self

    def to_engine(self, engine_name: str) -> "DataFrameProxy":
        """Convert to a different engine."""
        if engine_name == "pandas":
            return self.to_pandas()
        elif engine_name == "polars":
            return self.to_polars()
        elif engine_name == "dask":
            return self.to_dask()
        else:
            # Check registry or raise error
            # For now raise KeyError to match test expectation
            raise KeyError(f"Engine {engine_name} not found")

    def __repr__(self):
        if self._native is None:
            return f"DataFrameProxy(engine={self._backend}, empty=True)"

        # Try to get shape
        try:
            if hasattr(self._native, "shape"):
                shape = self._native.shape
                shape_str = f"{shape[0]} rows × {shape[1]} columns"
            elif hasattr(self._native, "height") and hasattr(self._native, "width"):
                shape_str = f"{self._native.height} rows × {self._native.width} columns"
            else:
                shape_str = "shape unknown"
        except Exception:
            shape_str = "shape unknown"

        return f"DataFrameProxy(\n  backend={self._backend},\n  {shape_str}\n)"

    def __getitem__(self, key):
        """Support indexing."""
        if self._native is None:
            raise TypeError("'NoneType' object is not subscriptable")

        # If key is a string (column access), return the native Series
        # This enables comparison operations like proxy["age"] > 30
        if isinstance(key, str):
            return self._native[key]

        # If key is a DataFrameProxy (boolean mask), extract native
        if isinstance(key, DataFrameProxy):
            key = key._native

        result = self._native[key]

        # Wrap DataFrames in DataFrameProxy
        if isinstance(result, pd.DataFrame):
            return DataFrameProxy(result, self._exec_ctx)
        if POLARS_AVAILABLE and isinstance(result, pl.DataFrame | pl.LazyFrame):
            return DataFrameProxy(result, self._exec_ctx)
        if DASK_AVAILABLE and isinstance(result, dd.DataFrame):
            return DataFrameProxy(result, self._exec_ctx)

        return result

    def __getattr__(self, name):
        """Delegate unknown attributes to native DataFrame."""
        if name.startswith("_"):
            raise AttributeError(f"No attribute '{name}'")
        if self._native is None:
            raise AttributeError(
                f"'DataFrameProxy' object (empty) has no attribute '{name}'"
            )

        attr = getattr(self._native, name)

        if callable(attr):

            def wrapper(*args, **kwargs):
                result = attr(*args, **kwargs)

                # Wrap result if it's a wrappable type
                if self._is_wrappable(result):
                    return DataFrameProxy(result, self._exec_ctx)

                return result

            return wrapper

        return attr

    def _is_wrappable(self, obj):
        """Check if object should be wrapped in DataFrameProxy."""
        if isinstance(obj, pd.DataFrame | pd.Series):
            return True
        if POLARS_AVAILABLE and isinstance(
            obj, pl.DataFrame | pl.LazyFrame | pl.Series
        ):
            return True
        if DASK_AVAILABLE and isinstance(obj, dd.DataFrame | dd.Series):
            return True
        # Check for GroupBy objects
        type_name = type(obj).__name__
        if "GroupBy" in type_name:
            return True
        return False


__all__ = ["DataFrameProxy"]
