"""
Entity storage and persistence.

Handles reading and writing entities using DataFrameProxy.
"""

from dataclasses import asdict
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from ..core.reader import read_avro, read_parquet
from .delta_log import DeltaLog


class EntityStore:
    """Storage manager for entity persistence."""

    def __init__(self, metadata):
        """
        Initialize entity store.

        Args:
            metadata: EntityMetadata instance
        """
        self.metadata = metadata
        self._ensure_storage()

        # Initialize Delta Log for O(1) writes
        self.delta_log = DeltaLog(
            storage_path=self.metadata.storage_path,
            primary_key=self.metadata.primary_key,
        )

    def _ensure_storage(self) -> None:
        """Ensure storage directory exists."""
        self.metadata.storage_path.mkdir(parents=True, exist_ok=True)

    def _load_dataframe(self) -> pd.DataFrame:
        """Load entity data as pandas DataFrame with delta log replay."""
        base_path = self.metadata.storage_path / "base.parquet"

        # Load base data
        if base_path.exists():
            base_df = pd.read_parquet(base_path)
        else:
            # Try legacy storage file
            storage_file = self.metadata.storage_file
            if storage_file.exists():
                if self.metadata.format == "parquet":
                    proxy = read_parquet(storage_file, engine="pandas")
                    base_df = proxy.native
                elif self.metadata.format == "avro":
                    proxy = read_avro(storage_file, engine="pandas")
                    base_df = proxy.native
                else:
                    raise ValueError(f"Unsupported format: {self.metadata.format}")
            else:
                # No data yet
                base_df = pd.DataFrame(columns=list(self.metadata.fields.keys()))

        # Apply delta log
        merged_df = self.delta_log.replay(base_df)
        return merged_df

    def _save_dataframe(self, df: pd.DataFrame) -> None:
        """Save DataFrame to storage."""
        storage_file = self.metadata.storage_file

        if self.metadata.format == "parquet":
            df.to_parquet(storage_file, index=False)
        elif self.metadata.format == "avro":
            # Use Avro writer if available
            try:
                from ..io_new.avro import AvroWriter

                writer = AvroWriter()
                writer.write(df, storage_file)
            except ImportError as e:
                raise ImportError("fastavro required for Avro format") from e
        else:
            raise ValueError(f"Unsupported format: {self.metadata.format}")

        # Generate GraphAr metadata files
        self._write_graphar_metadata(df)

    def _write_graphar_metadata(self, df: pd.DataFrame) -> None:
        """Write GraphAr-compliant metadata files."""
        storage_path = self.metadata.storage_path

        # Generate _metadata.yaml
        metadata_content = {
            "name": self.metadata.name,
            "version": "0.1.0",
            "format": "graphar",
            "vertices": [
                {
                    "label": self.metadata.name,
                    "prefix": f"vertices/{self.metadata.name}/",
                    "count": len(df),
                }
            ],
            "edges": [],  # Entities don't have edges by default
        }

        metadata_file = storage_path / "_metadata.yaml"
        with open(metadata_file, "w") as f:
            yaml.dump(metadata_content, f, default_flow_style=False, sort_keys=False)

        # Generate _schema.yaml
        schema_content = self._generate_schema(df)
        schema_file = storage_path / "_schema.yaml"
        with open(schema_file, "w") as f:
            yaml.dump(schema_content, f, default_flow_style=False, sort_keys=False)

    def _generate_schema(self, df: pd.DataFrame) -> dict:
        """Generate GraphAr schema from DataFrame."""
        # Map pandas dtypes to GraphAr types
        type_mapping = {
            "int64": "int64",
            "int32": "int32",
            "float64": "double",
            "float32": "float",
            "object": "string",
            "bool": "bool",
            "datetime64[ns]": "timestamp",
        }

        properties = []
        for col_name, dtype in df.dtypes.items():
            dtype_str = str(dtype)
            graphar_type = type_mapping.get(dtype_str, "string")
            properties.append(
                {
                    "name": col_name,
                    "type": graphar_type,
                    "nullable": bool(df[col_name].isnull().any()),
                }
            )

        schema = {
            "vertices": [
                {
                    "label": self.metadata.name,
                    "properties": properties,
                    "primary_key": self.metadata.primary_key,
                }
            ],
            "edges": [],
        }

        return schema

    def save(self, instance: Any) -> None:
        """
        Save an entity instance using O(1) delta log append.

        Args:
            instance: Entity instance to save
        """
        # Convert instance to dict
        data = asdict(instance)

        # Append to delta log (O(1) operation!)
        self.delta_log.append("UPSERT", data)

        # Trigger compaction if needed (background-worthy)
        if self.delta_log.should_compact():
            self._compact()
        else:
            # Still write metadata even without compaction
            # Load current dataframe state and write metadata
            df = self._load_dataframe()
            self._write_graphar_metadata(df)
            # Ensure legacy storage file exists for compatibility (e.g., Document.parquet)
            storage_file = self.metadata.storage_file
            if not storage_file.exists():
                self._save_dataframe(df)

    def _compact(self) -> None:
        """Compact delta log into base parquet file."""
        # Load all data with deltas
        df = self._load_dataframe()

        # Compact
        self.delta_log.compact(df)

        # Update GraphAr metadata
        self._write_graphar_metadata(df)

    def delete(self, pk_value: Any) -> None:
        """
        Delete an entity by primary key using O(1) delta log append.

        Args:
            pk_value: Primary key value
        """
        # Append delete operation to delta log
        data = {self.metadata.primary_key: pk_value}
        self.delta_log.append("DELETE", data)

        # Trigger compaction if needed
        if self.delta_log.should_compact():
            self._compact()

    def find(self, pk_value: Any) -> Any | None:
        """
        Find entity by primary key.

        Args:
            pk_value: Primary key value

        Returns:
            Entity instance or None
        """
        df = self._load_dataframe()

        if len(df) == 0:
            return None

        # Filter by primary key
        pk_col = self.metadata.primary_key
        result_df = df[df[pk_col] == pk_value]

        if len(result_df) == 0:
            return None

        # Convert first row to entity instance
        row_dict = result_df.iloc[0].to_dict()
        return self.metadata.cls(**row_dict)

    def find_all(self) -> list[Any]:
        """
        Find all entities.

        Returns:
            List of entity instances
        """
        df = self._load_dataframe()

        if len(df) == 0:
            return []

        # Convert all rows to entity instances
        instances = []
        for _, row in df.iterrows():
            row_dict = row.to_dict()
            instances.append(self.metadata.cls(**row_dict))

        return instances

    def find_by(self, **filters: Any) -> list[Any]:
        """
        Find entities matching filters.

        Args:
            **filters: Column name and value pairs

        Returns:
            List of matching entity instances
        """
        df = self._load_dataframe()

        if len(df) == 0:
            return []

        # Apply filters
        mask = pd.Series([True] * len(df))
        for col, value in filters.items():
            if col in df.columns:
                mask &= df[col] == value

        result_df = df[mask]

        # Convert to entity instances
        instances = []
        for _, row in result_df.iterrows():
            row_dict = row.to_dict()
            instances.append(self.metadata.cls(**row_dict))

        return instances

    def count(self) -> int:
        """
        Count total entities.

        Returns:
            Number of entities
        """
        df = self._load_dataframe()
        return len(df)

    def delete_all(self) -> int:
        """
        Delete all entities.

        Returns:
            Number of entities deleted
        """
        df = self._load_dataframe()
        count = len(df)

        # Clear delta log
        self.delta_log.clear()

        # Remove all files in storage path
        storage_path = self.metadata.storage_path
        if storage_path.exists():
            for file in storage_path.iterdir():
                if file.is_file():
                    file.unlink()

        # Recreate empty base file - get unique columns from dataclass fields
        # (primary_key is already a field, so we don't need to add it separately)
        field_names = [f.name for f in self.metadata.cls.__dataclass_fields__.values()]
        # Remove duplicates while preserving order
        unique_columns = list(dict.fromkeys(field_names))
        empty_df = pd.DataFrame(columns=unique_columns)
        self._save_dataframe(empty_df)

        return count

    def add_relationship(
        self,
        source: Any,
        rel_name: str,
        target: Any,
        props: dict[str, Any] | None = None,
    ) -> None:
        """
        Log a relationship between two entities.

        Args:
            source: Source entity instance
            rel_name: Name of the relationship
            target: Target entity instance
            props: Optional relationship properties
        """
        source_type = self.metadata.name
        # We assume target is an entity instance, get its type name
        target_type = target.__class__.__name__

        # GraphAr convention: Source_REL_Target
        rel_dir_name = f"{source_type}_{rel_name}_{target_type}"
        rel_dir = self.metadata.storage_path.parent / rel_dir_name
        rel_dir.mkdir(parents=True, exist_ok=True)

        # Prepare data
        src_pk = getattr(source, self.metadata.primary_key)

        # Find target PK - assuming target has metadata or we can guess
        # For now, look for 'id' or try to find registered metadata for target class
        from .metadata import registry

        target_metadata = registry.get_by_class(target.__class__)
        if target_metadata:
            dst_pk = getattr(target, target_metadata.primary_key)
        else:
            # Fallback: assume 'id' or same PK name as source
            dst_pk = getattr(
                target, "id", getattr(target, self.metadata.primary_key, None)
            )

        if src_pk is None or dst_pk is None:
            raise ValueError("Entities must have primary keys to be related.")

        data = {"src_id": src_pk, "dst_id": dst_pk}

        if props:
            data.update(props)

        # Append to edge file (using simple append for now, similar to delta log concept)
        # In a real GraphAr impl, this would be partitioned.
        edge_file = rel_dir / "adj_list.parquet"

        new_df = pd.DataFrame([data])

        if edge_file.exists():
            existing_df = pd.read_parquet(edge_file)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            combined_df.to_parquet(edge_file)
        else:
            new_df.to_parquet(edge_file)

        # Update/Create edge metadata
        self._write_edge_metadata(rel_dir, source_type, rel_name, target_type)

    def _write_edge_metadata(
        self, rel_dir: Path, src_type: str, rel_name: str, dst_type: str
    ) -> None:
        """Write GraphAr edge metadata."""
        metadata_file = rel_dir / "_metadata.yaml"

        content = {
            "name": rel_name,
            "type": "EDGE",
            "src_label": src_type,
            "dst_label": dst_type,
            "prefix": f"edges/{src_type}_{rel_name}_{dst_type}/",
            "adj_lists": [
                {"ordered": False, "prefix": "adj_list/", "file_type": "parquet"}
            ],
        }

        with open(metadata_file, "w") as f:
            yaml.dump(content, f, sort_keys=False)
