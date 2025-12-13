"""
Apache Avro support for ParquetFrame Phase 2.

High-performance Avro reading and writing using fastavro backend
with automatic schema inference and multi-engine compatibility.
"""

from pathlib import Path
from typing import TYPE_CHECKING, Any

try:
    import fastavro

    FASTAVRO_AVAILABLE = True
except ImportError:
    fastavro = None
    FASTAVRO_AVAILABLE = False

import pandas as pd

if TYPE_CHECKING:
    pass


def infer_avro_schema(
    df: pd.DataFrame, name: str = "ParquetFrameSchema"
) -> dict[str, Any]:
    """
    Infer Avro schema from pandas DataFrame.

    Args:
        df: pandas DataFrame
        name: Schema name

    Returns:
        Avro schema dictionary
    """
    if not FASTAVRO_AVAILABLE:
        raise ImportError("fastavro is required for Avro support")

    fields = []

    for column_name, dtype in df.dtypes.items():
        has_nulls = df[column_name].isnull().any()
        avro_field = {
            "name": str(column_name),
            "type": _pandas_dtype_to_avro_type(
                dtype, has_nulls, df[column_name] if has_nulls else None
            ),
        }
        fields.append(avro_field)

    schema = {"type": "record", "name": name, "fields": fields}

    return schema


def _pandas_dtype_to_avro_type(
    dtype: Any, has_nulls: bool = False, series: pd.Series | None = None
) -> str | list[str]:
    """Convert pandas dtype to Avro type."""
    dtype_str = str(dtype)

    # Basic type mapping
    if dtype_str.startswith("int") or dtype_str.startswith(
        "Int"
    ):  # Include nullable Int64
        avro_type = "long"
    elif dtype_str.startswith("float"):
        # Check if this might be an int column converted to float due to nulls
        # (pandas converts int to float64 when there are null values)
        if has_nulls and series is not None:
            non_null = series.dropna()
            if len(non_null) > 0:
                # Check if all non-null values are whole numbers
                try:
                    if (non_null == non_null.astype(int)).all():
                        avro_type = "long"
                    else:
                        avro_type = "double"
                except (ValueError, TypeError):
                    avro_type = "double"
            else:
                avro_type = "double"
        else:
            avro_type = "double"
    elif dtype_str.startswith("bool"):
        avro_type = "boolean"
    elif dtype_str.startswith("datetime"):
        # Use logical types for timestamps
        avro_type = {"type": "long", "logicalType": "timestamp-millis"}
    elif dtype_str == "object":
        # Assume string for object columns
        avro_type = "string"
    else:
        # Default to string for unknown types
        avro_type = "string"

    # Handle nullable fields
    if has_nulls:
        return ["null", avro_type]
    else:
        return avro_type


class AvroReader:
    """High-performance Avro file reader using fastavro."""

    def __init__(self):
        if not FASTAVRO_AVAILABLE:
            raise ImportError("fastavro is required for Avro support")

    def read(self, path: str | Path, engine: str = "pandas") -> Any:
        """
        Read Avro file to DataFrame.

        Args:
            path: Path to Avro file
            engine: Target engine ('pandas', 'polars', 'dask')

        Returns:
            DataFrame in the requested engine format
        """
        records = []

        with open(path, "rb") as f:
            avro_reader = fastavro.reader(f)
            for record in avro_reader:
                records.append(record)

        if not records:
            return self._empty_dataframe(engine)

        # Convert to pandas first (common intermediate format)
        df = pd.DataFrame(records)

        # Handle timestamp columns if they exist
        df = self._handle_timestamps(df)

        # Convert to target engine
        return self._convert_to_engine(df, engine)

    def _empty_dataframe(self, engine: str) -> Any:
        """Create empty DataFrame for the specified engine."""
        if engine == "pandas":
            return pd.DataFrame()
        elif engine == "polars":
            try:
                import polars as pl

                return pl.DataFrame()
            except ImportError as e:
                raise ImportError("Polars is required for polars engine") from e
        elif engine == "dask":
            try:
                import dask.dataframe as dd

                return dd.from_pandas(pd.DataFrame(), npartitions=1)
            except ImportError as e:
                raise ImportError("Dask is required for dask engine") from e
        else:
            raise ValueError(f"Unsupported engine: {engine}")

    def _convert_to_engine(self, df: pd.DataFrame, engine: str) -> Any:
        """Convert pandas DataFrame to target engine."""
        if engine == "pandas":
            return df
        elif engine == "polars":
            try:
                import polars as pl

                return pl.from_pandas(df)
            except ImportError as e:
                raise ImportError("Polars is required for polars engine") from e
        elif engine == "dask":
            try:
                import dask.dataframe as dd

                # Determine appropriate partitions
                nrows = len(df)
                npartitions = max(1, nrows // 100000)  # ~100k rows per partition
                return dd.from_pandas(df, npartitions=npartitions)
            except ImportError as e:
                raise ImportError("Dask is required for dask engine") from e
        else:
            raise ValueError(f"Unsupported engine: {engine}")

    def _handle_timestamps(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert timestamp columns from milliseconds to datetime."""
        for column in df.columns:
            # Check if column contains timestamp-like values
            if df[column].dtype == "int64":
                try:
                    # Try to convert as timestamp (milliseconds)
                    sample = (
                        df[column].dropna().iloc[:10]
                        if len(df) > 10
                        else df[column].dropna()
                    )
                    if len(sample) > 0:
                        # Check if values are in reasonable timestamp range
                        min_val = sample.min()
                        if (
                            1000000000000 <= min_val <= 9999999999999
                        ):  # Year 2001-2286 in ms
                            df[column] = pd.to_datetime(df[column], unit="ms")
                except Exception:
                    # If conversion fails, leave as-is
                    pass

        return df


class AvroWriter:
    """High-performance Avro file writer using fastavro."""

    def __init__(self):
        if not FASTAVRO_AVAILABLE:
            raise ImportError("fastavro is required for Avro support")

    def write(
        self,
        df: Any,
        path: str | Path,
        schema: dict[str, Any] | None = None,
        codec: str = "deflate",
    ) -> None:
        """
        Write DataFrame to Avro file.

        Supports pandas, Polars, and Dask DataFrames. All formats are
        converted to pandas for writing.

        Args:
            df: DataFrame (pandas, Polars, or Dask)
            path: Output file path
            schema: Avro schema (if None, will be inferred)
            codec: Compression codec ('deflate', 'snappy', 'null')
        """
        # Convert to pandas if needed
        pandas_df = self._to_pandas(df)

        if schema is None:
            schema = infer_avro_schema(pandas_df)

        # Convert DataFrame to records
        records = self._df_to_records(pandas_df, schema)

        # Write to Avro file
        with open(path, "wb") as f:
            fastavro.writer(f, schema, records, codec=codec)

    def _to_pandas(self, df: Any) -> pd.DataFrame:
        """Convert any DataFrame type to pandas."""
        if isinstance(df, pd.DataFrame):
            return df

        # Check for Polars DataFrame
        if hasattr(df, "to_pandas"):
            return df.to_pandas()

        # Check for Dask DataFrame
        if hasattr(df, "compute"):
            return df.compute()

        # Try direct conversion
        try:
            return pd.DataFrame(df)
        except Exception as e:
            raise TypeError(
                f"Cannot convert {type(df).__name__} to pandas DataFrame: {e}"
            ) from e

    def _df_to_records(
        self, df: pd.DataFrame, schema: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Convert DataFrame to list of records for Avro writing."""
        # Handle timestamp columns
        df_converted = df.copy()

        # Convert datetime columns to milliseconds for Avro
        for field in schema["fields"]:
            field_name = field["name"]
            field_type = field["type"]

            if field_name in df_converted.columns:
                # Handle timestamp logical types
                if (
                    isinstance(field_type, dict)
                    and field_type.get("logicalType") == "timestamp-millis"
                ):
                    if pd.api.types.is_datetime64_any_dtype(df_converted[field_name]):
                        df_converted[field_name] = (
                            df_converted[field_name].astype("int64") // 1_000_000
                        )

                # Handle nullable fields
                elif isinstance(field_type, list) and "null" in field_type:
                    # Replace NaN with None for Avro null handling
                    df_converted[field_name] = df_converted[field_name].where(
                        pd.notnull(df_converted[field_name]), None
                    )

        # Convert to records
        return df_converted.to_dict("records")
