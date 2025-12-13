"""
Reader factory for intelligent DataFrame engine selection.

Provides factory functions for reading data files with automatic engine
selection based on file size, format, and system resources.
"""

import logging
from pathlib import Path
from typing import Any

try:
    import pyarrow.parquet as pq

    PYARROW_AVAILABLE = True
except ImportError:
    pq = None
    PYARROW_AVAILABLE = False

# Optional Rust fast-path functions
try:
    from ..io.io_backend import try_get_row_count_fast as _try_get_row_count_fast
except Exception:  # noqa: BLE001 - broadened intentionally for optional dep
    _try_get_row_count_fast = None  # type: ignore[assignment]

from .proxy import DataFrameProxy
from .registry import EngineRegistry

try:
    from ..io_new.avro import AvroReader

    AVRO_AVAILABLE = True
except ImportError:
    AvroReader = None  # type: ignore[assignment,misc]
    AVRO_AVAILABLE = False

logger = logging.getLogger(__name__)


class DataReader:
    """Factory for reading data with intelligent engine selection."""

    def __init__(self):
        self._registry = EngineRegistry()

    def read_parquet(
        self, path: str | Path, engine: str | None = None, **kwargs: Any
    ) -> DataFrameProxy:
        """
        Read Parquet file with intelligent engine selection.

        Args:
            path: Path to Parquet file or directory
            engine: Force specific engine ('pandas', 'polars', 'dask', 'auto')
            **kwargs: Additional arguments passed to engine's read function

        Returns:
            DataFrameProxy with optimal engine selected
        """
        path = Path(path)

        # Check file existence first
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        # Estimate data size
        data_size = self._estimate_file_size(path)

        # Get row count from metadata if possible (more accurate)
        try:
            row_count = self._get_parquet_row_count(path)
            if row_count:
                # Adjust size estimate based on row count
                # Rough heuristic: 100 bytes per row on average
                estimated_memory = row_count * 100
                data_size = max(data_size, estimated_memory)
                logger.debug(
                    f"Parquet file has {row_count:,} rows, "
                    f"estimated memory: {estimated_memory / 1024 / 1024:.2f} MB"
                )
        except Exception as e:
            logger.debug(f"Could not read Parquet metadata: {e}")

        # Select engine
        if engine and engine != "auto":
            selected_engine = self._registry.get_engine(engine)
        else:
            selected_engine = self._registry.select_optimal_engine(
                data_size_bytes=data_size
            )

        logger.info(
            f"Reading Parquet file ({data_size / 1024 / 1024:.2f} MB) "
            f"with {selected_engine.name} engine"
        )

        # Read using selected engine
        native_df = selected_engine.read_parquet(path, **kwargs)

        return DataFrameProxy(data=native_df, engine=selected_engine.name)

    def read_csv(
        self, path: str | Path, engine: str | None = None, **kwargs: Any
    ) -> DataFrameProxy:
        """
        Read CSV file with intelligent engine selection.

        Args:
            path: Path to CSV file (.csv, .tsv)
            engine: Force specific engine ('pandas', 'polars', 'dask', 'auto')
            **kwargs: Additional arguments passed to engine's read function

        Returns:
            DataFrameProxy with optimal engine selected
        """
        path = Path(path)

        # Check file existence first
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        data_size = self._estimate_file_size(path)

        # Auto-detect TSV files and set separator if not explicitly provided
        suffix = path.suffix.lower()
        if suffix == ".tsv" and "sep" not in kwargs and "separator" not in kwargs:
            kwargs["sep"] = "\t"

        # Select engine
        if engine and engine != "auto":
            selected_engine = self._registry.get_engine(engine)
        else:
            selected_engine = self._registry.select_optimal_engine(
                data_size_bytes=data_size
            )

        logger.info(
            f"Reading CSV file ({data_size / 1024 / 1024:.2f} MB) "
            f"with {selected_engine.name} engine"
        )

        # Read using selected engine
        native_df = selected_engine.read_csv(path, **kwargs)

        return DataFrameProxy(data=native_df, engine=selected_engine.name)

    def read_avro(
        self, path: str | Path, engine: str | None = None, **kwargs: Any
    ) -> DataFrameProxy:
        """
        Read Avro file with intelligent engine selection.

        Args:
            path: Path to Avro file
            engine: Force specific engine ('pandas', 'polars', 'dask', 'auto')
            **kwargs: Additional arguments

        Returns:
            DataFrameProxy with optimal engine selected
        """
        if not AVRO_AVAILABLE:
            raise ImportError(
                "fastavro is required for Avro support. "
                "Install with: pip install fastavro"
            )

        path = Path(path)

        # Check file existence first
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        data_size = self._estimate_file_size(path)

        # Select engine
        if engine and engine != "auto":
            selected_engine = self._registry.get_engine(engine)
        else:
            selected_engine = self._registry.select_optimal_engine(
                data_size_bytes=data_size
            )

        logger.info(
            f"Reading Avro file ({data_size / 1024 / 1024:.2f} MB) "
            f"with {selected_engine.name} engine"
        )

        # Read using Avro reader
        reader = AvroReader()
        native_df = reader.read(path, engine=selected_engine.name)

        return DataFrameProxy(data=native_df, engine=selected_engine.name)

    def read_json(
        self, path: str | Path, engine: str | None = None, **kwargs: Any
    ) -> DataFrameProxy:
        """
        Read JSON or JSON Lines file with intelligent engine selection.

        Args:
            path: Path to JSON file (.json, .jsonl, .ndjson)
            engine: Force specific engine ('pandas', 'polars', 'dask', 'auto')
            **kwargs: Additional arguments (e.g., lines=True for JSON Lines)

        Returns:
            DataFrameProxy with optimal engine selected
        """
        path = Path(path)

        # Check file existence first
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        data_size = self._estimate_file_size(path)

        # Select engine
        if engine and engine != "auto":
            selected_engine = self._registry.get_engine(engine)
        else:
            selected_engine = self._registry.select_optimal_engine(
                data_size_bytes=data_size
            )

        # Auto-detect JSON Lines format from extension
        suffix = path.suffix.lower()
        is_jsonl = suffix in (".jsonl", ".ndjson")
        if is_jsonl and "lines" not in kwargs:
            kwargs["lines"] = True

        logger.info(
            f"Reading JSON{'L' if is_jsonl else ''} file "
            f"({data_size / 1024 / 1024:.2f} MB) "
            f"with {selected_engine.name} engine"
        )

        # Read using pandas (most reliable for JSON), then convert if needed
        import pandas as pd

        native_df = pd.read_json(path, **kwargs)

        # Convert to selected engine if not pandas
        if selected_engine.name != "pandas":
            native_df = selected_engine.from_pandas(native_df)  # type: ignore[attr-defined]

        return DataFrameProxy(data=native_df, engine=selected_engine.name)

    def read_orc(
        self, path: str | Path, engine: str | None = None, **kwargs: Any
    ) -> DataFrameProxy:
        """
        Read ORC file with intelligent engine selection.

        Args:
            path: Path to ORC file
            engine: Force specific engine ('pandas', 'polars', 'dask', 'auto')
            **kwargs: Additional arguments

        Returns:
            DataFrameProxy with optimal engine selected
        """
        path = Path(path)

        # Check file existence first
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        data_size = self._estimate_file_size(path)

        # Select engine
        if engine and engine != "auto":
            selected_engine = self._registry.get_engine(engine)
        else:
            selected_engine = self._registry.select_optimal_engine(
                data_size_bytes=data_size
            )

        logger.info(
            f"Reading ORC file ({data_size / 1024 / 1024:.2f} MB) "
            f"with {selected_engine.name} engine"
        )

        # Read ORC using pyarrow, then convert if needed
        try:
            import pyarrow.orc as orc
        except ImportError as err:
            raise ImportError(
                "pyarrow with ORC support required. Install with: pip install pyarrow"
            ) from err

        table = orc.read_table(path)
        native_df = table.to_pandas()

        # Convert to selected engine if not pandas
        if selected_engine.name != "pandas":
            native_df = selected_engine.from_pandas(native_df)  # type: ignore[attr-defined]

        return DataFrameProxy(data=native_df, engine=selected_engine.name)

    def read(
        self, path: str | Path, engine: str | None = None, **kwargs: Any
    ) -> DataFrameProxy:
        """
        Read data file with automatic format detection and engine selection.

        Supports: .parquet, .pqt, .csv, .tsv, .json, .jsonl, .ndjson, .avro, .orc

        Args:
            path: Path to data file
            engine: Force specific engine ('pandas', 'polars', 'dask', 'auto')
            **kwargs: Additional arguments passed to engine's read function

        Returns:
            DataFrameProxy with optimal engine selected
        """
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        # Detect format from extension
        suffix = path.suffix.lower()

        if suffix in (".parquet", ".pqt"):
            return self.read_parquet(path, engine=engine, **kwargs)
        elif suffix in (".csv", ".tsv"):
            return self.read_csv(path, engine=engine, **kwargs)
        elif suffix in (".json", ".jsonl", ".ndjson"):
            return self.read_json(path, engine=engine, **kwargs)
        elif suffix == ".avro":
            return self.read_avro(path, engine=engine, **kwargs)
        elif suffix == ".orc":
            return self.read_orc(path, engine=engine, **kwargs)
        else:
            raise ValueError(
                f"Unsupported file format: {suffix}. "
                f"Supported: .parquet, .pqt, .csv, .tsv, .json, .jsonl, .ndjson, .avro, .orc"
            )

    def _estimate_file_size(self, path: Path) -> int:
        """
        Estimate total size of file or directory.

        Args:
            path: Path to file or directory

        Returns:
            Total size in bytes
        """
        if path.is_file():
            return path.stat().st_size
        elif path.is_dir():
            # Sum all files in directory (for partitioned datasets)
            total_size = 0
            for file_path in path.rglob("*"):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
            return total_size
        else:
            raise ValueError(f"Path must be a file or directory: {path}")

    def _get_parquet_row_count(self, path: Path) -> int | None:
        """
        Get row count from Parquet metadata without reading data.

        Prefers Rust fast-path when available, with graceful fallback to pyarrow.

        Args:
            path: Path to Parquet file or directory

        Returns:
            Total row count or None if unavailable
        """
        # Try Rust fast-path first if available
        try:
            if _try_get_row_count_fast is not None:
                if path.is_file():
                    rc = _try_get_row_count_fast(path)
                    if rc is not None:
                        return int(rc)
                elif path.is_dir():
                    total_rows = 0
                    for file_path in path.rglob("*.parquet"):
                        if file_path.is_file():
                            rc = _try_get_row_count_fast(file_path)
                            if rc is not None:
                                total_rows += int(rc)
                    if total_rows > 0:
                        return total_rows
        except Exception as e:  # noqa: BLE001 - robustness over strictness
            logger.debug(f"Rust row count read failed, falling back: {e}")

        # Fallback to pyarrow if available
        if not PYARROW_AVAILABLE:
            return None

        try:
            if path.is_file():
                metadata = pq.read_metadata(path)
                return metadata.num_rows
            elif path.is_dir():
                # For partitioned datasets, sum row counts
                total_rows = 0
                for file_path in path.rglob("*.parquet"):
                    if file_path.is_file():
                        metadata = pq.read_metadata(file_path)
                        total_rows += metadata.num_rows
                return total_rows if total_rows > 0 else None
            else:
                return None
        except Exception as e:
            logger.debug(f"Could not read Parquet metadata: {e}")
            return None


# Singleton instance for convenience
_reader = DataReader()


# Convenience functions
def read_parquet(
    path: str | Path, engine: str | None = None, **kwargs: Any
) -> DataFrameProxy:
    """
    Read Parquet file with intelligent engine selection.

    Args:
        path: Path to Parquet file or directory
        engine: Force specific engine ('pandas', 'polars', 'dask', 'auto')
        **kwargs: Additional arguments passed to engine's read function

    Returns:
        DataFrameProxy with optimal engine selected
    """
    return _reader.read_parquet(path, engine=engine, **kwargs)


def read_csv(
    path: str | Path, engine: str | None = None, **kwargs: Any
) -> DataFrameProxy:
    """
    Read CSV file with intelligent engine selection.

    Args:
        path: Path to CSV file
        engine: Force specific engine ('pandas', 'polars', 'dask', 'auto')
        **kwargs: Additional arguments passed to engine's read function

    Returns:
        DataFrameProxy with optimal engine selected
    """
    return _reader.read_csv(path, engine=engine, **kwargs)


def read_avro(
    path: str | Path, engine: str | None = None, **kwargs: Any
) -> DataFrameProxy:
    """
    Read Avro file with intelligent engine selection.

    Args:
        path: Path to Avro file
        engine: Force specific engine ('pandas', 'polars', 'dask', 'auto')
        **kwargs: Additional arguments

    Returns:
        DataFrameProxy with optimal engine selected
    """
    return _reader.read_avro(path, engine=engine, **kwargs)


def read_json(
    path: str | Path, engine: str | None = None, **kwargs: Any
) -> DataFrameProxy:
    """
    Read JSON or JSON Lines file with intelligent engine selection.

    Args:
        path: Path to JSON file (.json, .jsonl, .ndjson)
        engine: Force specific engine ('pandas', 'polars', 'dask', 'auto')
        **kwargs: Additional arguments (e.g., lines=True for JSON Lines)

    Returns:
        DataFrameProxy with optimal engine selected
    """
    return _reader.read_json(path, engine=engine, **kwargs)


def read_orc(
    path: str | Path, engine: str | None = None, **kwargs: Any
) -> DataFrameProxy:
    """
    Read ORC file with intelligent engine selection.

    Args:
        path: Path to ORC file
        engine: Force specific engine ('pandas', 'polars', 'dask', 'auto')
        **kwargs: Additional arguments

    Returns:
        DataFrameProxy with optimal engine selected
    """
    return _reader.read_orc(path, engine=engine, **kwargs)


def read(path: str | Path, engine: str | None = None, **kwargs: Any) -> DataFrameProxy:
    """
    Read data file with automatic format detection and engine selection.

    Supports: .parquet, .pqt, .csv, .tsv, .json, .jsonl, .ndjson, .avro, .orc

    Args:
        path: Path to data file
        engine: Force specific engine ('pandas', 'polars', 'dask', 'auto')
        **kwargs: Additional arguments passed to engine's read function

    Returns:
        DataFrameProxy with optimal engine selected

    Examples:
        >>> import parquetframe.core as pf2
        >>> # Automatic engine selection based on file size
        >>> df = pf2.read("data.parquet")
        >>> print(f"Using {df.engine_name} engine")
        >>>
        >>> # Force specific engine
        >>> df = pf2.read("data.csv", engine="polars")
        >>>
        >>> # Avro support with schema inference
        >>> df = pf2.read("data.avro")
        >>>
        >>> # DataFrame operations work transparently
        >>> result = df.groupby("category").sum()
        >>> print(result)
    """
    return _reader.read(path, engine=engine, **kwargs)
