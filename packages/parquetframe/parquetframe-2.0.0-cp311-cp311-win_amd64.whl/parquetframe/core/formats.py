"""
Multi-format support for ParquetFrame.

Provides format detection and handlers for CSV, JSON, Parquet, ORC, and other formats.
"""

from enum import Enum
from pathlib import Path
from typing import Any

import pandas as pd


class FileFormat(Enum):
    """Supported file formats."""

    CSV = "csv"
    JSON = "json"
    PARQUET = "parquet"
    ORC = "orc"


def detect_format(path: str | Path, explicit_format: str | None = None) -> FileFormat:
    """
    Detect file format from path or explicit format specification.

    Args:
        path: File path
        explicit_format: Optional explicit format override

    Returns:
        Detected FileFormat

    Raises:
        ValueError: If explicit format is invalid
    """
    if explicit_format:
        try:
            return FileFormat(explicit_format.lower())
        except ValueError:
            raise ValueError(f"Unsupported format: {explicit_format}") from None

    # Detect from extension
    path_str = str(path).lower()
    if path_str.endswith((".csv", ".tsv")):
        return FileFormat.CSV
    elif path_str.endswith((".json", ".jsonl", ".ndjson")):
        return FileFormat.JSON
    elif path_str.endswith(".orc"):
        return FileFormat.ORC
    else:
        # Default to parquet for backwards compatibility
        return FileFormat.PARQUET


class FormatHandler:
    """Base class for format handlers."""

    def __init__(self, extensions: list[str]):
        self.extensions = extensions

    def read(self, path: str | Path, use_dask: bool = False, **kwargs) -> Any:
        """Read file and return DataFrame."""
        raise NotImplementedError

    def write(self, df: Any, path: str | Path, **kwargs) -> None:
        """Write DataFrame to file."""
        raise NotImplementedError

    def resolve_file_path(self, path: str | Path) -> Path:
        """Resolve file path, trying extensions if needed."""
        path = Path(path)

        # If path exists as-is, return it
        if path.exists():
            return path

        # Try adding extensions
        for ext in self.extensions:
            candidate = path.parent / f"{path.name}{ext}"
            if candidate.exists():
                return candidate

        raise FileNotFoundError(f"File not found: {path}")


class CSVHandler(FormatHandler):
    """Handler for CSV and TSV files."""

    def __init__(self):
        super().__init__([".csv", ".tsv"])

    def read(self, path: str | Path, use_dask: bool = False, **kwargs) -> Any:
        """Read CSV/TSV file."""
        path = Path(path)

        # Auto-detect delimiter
        delimiter = "\t" if path.suffix == ".tsv" else ","
        kwargs.setdefault("sep", delimiter)

        if use_dask:
            import dask.dataframe as dd

            return dd.read_csv(path, **kwargs)
        else:
            return pd.read_csv(path, **kwargs)

    def write(self, df: Any, path: str | Path, **kwargs) -> None:
        """Write CSV/TSV file."""
        path = Path(path)

        # Auto-detect delimiter
        delimiter = "\t" if path.suffix == ".tsv" else ","
        kwargs.setdefault("sep", delimiter)
        kwargs.setdefault("index", False)

        # Convert to pandas if needed
        if hasattr(df, "compute"):
            df = df.compute()

        df.to_csv(path, **kwargs)


class JSONHandler(FormatHandler):
    """Handler for JSON and JSON Lines files."""

    def __init__(self):
        super().__init__([".json", ".jsonl", ".ndjson"])

    def read(self, path: str | Path, use_dask: bool = False, **kwargs) -> Any:
        """Read JSON file."""
        path = Path(path)

        # Auto-detect JSON Lines format
        lines = path.suffix in {".jsonl", ".ndjson"}
        kwargs.setdefault("lines", lines)

        if use_dask:
            import dask.dataframe as dd

            return dd.read_json(path, **kwargs)
        else:
            return pd.read_json(path, **kwargs)

    def write(self, df: Any, path: str | Path, **kwargs) -> None:
        """Write JSON file."""
        path = Path(path)

        # Auto-detect JSON Lines format
        lines = path.suffix in {".jsonl", ".ndjson"}
        kwargs.setdefault("lines", lines)
        kwargs.setdefault("orient", "records")

        # Convert to pandas if needed
        if hasattr(df, "compute"):
            df = df.compute()

        df.to_json(path, **kwargs)


class ParquetHandler(FormatHandler):
    """Handler for Parquet files."""

    def __init__(self):
        super().__init__([".parquet", ".pqt"])

    def read(self, path: str | Path, use_dask: bool = False, **kwargs) -> Any:
        """Read Parquet file."""
        if use_dask:
            import dask.dataframe as dd

            return dd.read_parquet(path, **kwargs)
        else:
            return pd.read_parquet(path, **kwargs)

    def write(self, df: Any, path: str | Path, **kwargs) -> None:
        """Write Parquet file."""
        # Convert to pandas if needed
        if hasattr(df, "compute"):
            df = df.compute()

        df.to_parquet(path, **kwargs)


class ORCHandler(FormatHandler):
    """Handler for ORC files."""

    def __init__(self):
        super().__init__([".orc"])

    def read(self, path: str | Path, use_dask: bool = False, **kwargs) -> Any:
        """Read ORC file."""
        try:
            import pyarrow.orc as orc
        except ImportError:
            raise ImportError(
                "ORC support requires pyarrow: pip install pyarrow"
            ) from None

        if use_dask:
            # Dask doesn't have native ORC support, read via PyArrow
            table = orc.read_table(path)
            return table.to_pandas()
        else:
            table = orc.read_table(path)
            return table.to_pandas()

    def write(self, df: Any, path: str | Path, **kwargs) -> None:
        """Write ORC file."""
        try:
            import pyarrow as pa
            import pyarrow.orc as orc
        except ImportError:
            raise ImportError(
                "ORC support requires pyarrow: pip install pyarrow"
            ) from None

        # Convert to pandas if needed
        if hasattr(df, "compute"):
            df = df.compute()

        # Convert to Arrow table and write
        table = pa.Table.from_pandas(df)
        orc.write_table(table, path)


# Format handler registry
FORMAT_HANDLERS = {
    FileFormat.CSV: CSVHandler(),
    FileFormat.JSON: JSONHandler(),
    FileFormat.PARQUET: ParquetHandler(),
    FileFormat.ORC: ORCHandler(),
}


__all__ = [
    "FileFormat",
    "FORMAT_HANDLERS",
    "detect_format",
    "FormatHandler",
    "CSVHandler",
    "JSONHandler",
    "ParquetHandler",
    "ORCHandler",
]
