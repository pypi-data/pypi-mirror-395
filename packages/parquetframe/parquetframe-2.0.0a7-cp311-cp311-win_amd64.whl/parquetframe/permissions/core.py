"""
Core data structures for Zanzibar-style permissions.

This module defines the fundamental data structures used in the permission system:
- RelationTuple: Individual permission relationships
- TupleStore: Efficient storage and querying of relation tuples
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from ..core_legacy import (
    ParquetFrame,  # Internal use only - avoids deprecation warnings
)


@dataclass(frozen=True)
class RelationTuple:
    """
    A relation tuple representing a permission relationship.

    Follows the Zanzibar model where permissions are expressed as:
    "subject has relation to object in namespace"

    Examples:
        RelationTuple("doc", "doc1", "viewer", "user", "alice")
        -> user:alice has viewer relation to doc:doc1

        RelationTuple("folder", "folder1", "editor", "group", "eng-team")
        -> group:eng-team has editor relation to folder:folder1

        RelationTuple("doc", "doc1", "viewer", "folder", "folder1#viewer")
        -> folder:folder1#viewer has viewer relation to doc:doc1
        (inherited permission via folder membership)

    Attributes:
        namespace: The namespace/type of the object (e.g., "doc", "folder")
        object_id: The ID of the object (e.g., "doc1", "folder1")
        relation: The relation type (e.g., "viewer", "editor", "owner")
        subject_namespace: The namespace of the subject (e.g., "user", "group")
        subject_id: The ID of the subject (e.g., "alice", "eng-team")
    """

    namespace: str
    object_id: str
    relation: str
    subject_namespace: str
    subject_id: str

    def __post_init__(self):
        """Validate the relation tuple after initialization."""
        if not all(
            [
                self.namespace,
                self.object_id,
                self.relation,
                self.subject_namespace,
                self.subject_id,
            ]
        ):
            raise ValueError("All relation tuple fields must be non-empty")

        # Basic format validation
        for field_name, value in [
            ("namespace", self.namespace),
            ("object_id", self.object_id),
            ("relation", self.relation),
            ("subject_namespace", self.subject_namespace),
            ("subject_id", self.subject_id),
        ]:
            if not isinstance(value, str):
                raise TypeError(f"{field_name} must be a string")
            if len(value.strip()) != len(value):
                raise ValueError(
                    f"{field_name} cannot have leading/trailing whitespace"
                )

    @property
    def object_ref(self) -> str:
        """Get the full object reference (namespace:object_id)."""
        return f"{self.namespace}:{self.object_id}"

    @property
    def subject_ref(self) -> str:
        """Get the full subject reference (subject_namespace:subject_id)."""
        return f"{self.subject_namespace}:{self.subject_id}"

    @property
    def tuple_key(self) -> str:
        """Get a unique key for this tuple (for deduplication and indexing)."""
        return f"{self.object_ref}#{self.relation}@{self.subject_ref}"

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"{self.subject_ref} {self.relation} {self.object_ref}"

    def __repr__(self) -> str:
        """Machine-readable string representation."""
        return (
            f"RelationTuple(namespace='{self.namespace}', object_id='{self.object_id}', "
            f"relation='{self.relation}', subject_namespace='{self.subject_namespace}', "
            f"subject_id='{self.subject_id}')"
        )

    def to_dict(self) -> dict[str, str]:
        """Convert to dictionary for DataFrame storage."""
        return {
            "namespace": self.namespace,
            "object_id": self.object_id,
            "relation": self.relation,
            "subject_namespace": self.subject_namespace,
            "subject_id": self.subject_id,
            "object_ref": self.object_ref,
            "subject_ref": self.subject_ref,
            "tuple_key": self.tuple_key,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> RelationTuple:
        """Create RelationTuple from dictionary."""
        return cls(
            namespace=data["namespace"],
            object_id=data["object_id"],
            relation=data["relation"],
            subject_namespace=data["subject_namespace"],
            subject_id=data["subject_id"],
        )


class TupleStore:
    """
    Efficient storage and querying of relation tuples using ParquetFrame.

    The TupleStore provides the foundational storage layer for the permission system,
    optimized for the common query patterns:
    - Check if a specific tuple exists
    - Find all objects a subject can access with a given relation
    - Find all subjects that have a relation to an object
    - Bulk operations for UI generation

    Uses ParquetFrame for storage with optimized schema and indexing.
    """

    def __init__(self, data: ParquetFrame | pd.DataFrame | None = None):
        """
        Initialize TupleStore.

        Args:
            data: Optional initial data as ParquetFrame or DataFrame
        """
        if data is None:
            # Create empty DataFrame with optimized schema
            data = pd.DataFrame(
                columns=[
                    "namespace",
                    "object_id",
                    "relation",
                    "subject_namespace",
                    "subject_id",
                    "object_ref",
                    "subject_ref",
                    "tuple_key",
                ]
            )

        if isinstance(data, pd.DataFrame):
            self._data = ParquetFrame(data, islazy=False)
        else:
            self._data = data

    @property
    def data(self) -> ParquetFrame:
        """Get the underlying ParquetFrame data."""
        return self._data

    @property
    def size(self) -> int:
        """Get the number of tuples in the store."""
        return len(self._data)

    def is_empty(self) -> bool:
        """Check if the tuple store is empty."""
        return self.size == 0

    def add_tuple(self, tuple_obj: RelationTuple) -> TupleStore:
        """
        Add a single relation tuple to the store.

        Args:
            tuple_obj: The RelationTuple to add

        Returns:
            Self for method chaining
        """
        new_row = pd.DataFrame([tuple_obj.to_dict()])

        if self.is_empty():
            self._data = ParquetFrame(new_row, islazy=False)
        else:
            combined = pd.concat([self._data._df, new_row], ignore_index=True)
            # Remove duplicates based on tuple_key
            combined = combined.drop_duplicates(subset=["tuple_key"], keep="last")
            self._data = ParquetFrame(combined, islazy=False)

        return self

    def add_tuples(self, tuples: list[RelationTuple]) -> TupleStore:
        """
        Add multiple relation tuples to the store.

        Args:
            tuples: List of RelationTuple objects to add

        Returns:
            Self for method chaining
        """
        if not tuples:
            return self

        new_rows = pd.DataFrame([t.to_dict() for t in tuples])

        if self.is_empty():
            self._data = ParquetFrame(new_rows, islazy=False)
        else:
            combined = pd.concat([self._data._df, new_rows], ignore_index=True)
            # Remove duplicates based on tuple_key
            combined = combined.drop_duplicates(subset=["tuple_key"], keep="last")
            self._data = ParquetFrame(combined, islazy=False)

        return self

    def remove_tuple(self, tuple_obj: RelationTuple) -> TupleStore:
        """
        Remove a relation tuple from the store.

        Args:
            tuple_obj: The RelationTuple to remove

        Returns:
            Self for method chaining
        """
        if self.is_empty():
            return self

        mask = self._data._df["tuple_key"] != tuple_obj.tuple_key
        filtered = self._data._df[mask]
        self._data = ParquetFrame(filtered.reset_index(drop=True), islazy=False)

        return self

    def has_tuple(self, tuple_obj: RelationTuple) -> bool:
        """
        Check if a specific tuple exists in the store.

        Args:
            tuple_obj: The RelationTuple to check for

        Returns:
            True if the tuple exists, False otherwise
        """
        if self.is_empty():
            return False

        return tuple_obj.tuple_key in self._data._df["tuple_key"].values

    def query_tuples(
        self,
        namespace: str | None = None,
        object_id: str | None = None,
        relation: str | None = None,
        subject_namespace: str | None = None,
        subject_id: str | None = None,
    ) -> list[RelationTuple]:
        """
        Query tuples by any combination of fields.

        Args:
            namespace: Filter by object namespace
            object_id: Filter by object ID
            relation: Filter by relation type
            subject_namespace: Filter by subject namespace
            subject_id: Filter by subject ID

        Returns:
            List of matching RelationTuple objects
        """
        if self.is_empty():
            return []

        df = self._data._df

        # Build filter conditions
        conditions = []
        if namespace is not None:
            conditions.append(df["namespace"] == namespace)
        if object_id is not None:
            conditions.append(df["object_id"] == object_id)
        if relation is not None:
            conditions.append(df["relation"] == relation)
        if subject_namespace is not None:
            conditions.append(df["subject_namespace"] == subject_namespace)
        if subject_id is not None:
            conditions.append(df["subject_id"] == subject_id)

        # Apply all conditions
        if conditions:
            mask = conditions[0]
            for condition in conditions[1:]:
                mask &= condition
            filtered = df[mask]
        else:
            filtered = df

        # Convert back to RelationTuple objects
        return [RelationTuple.from_dict(row) for _, row in filtered.iterrows()]

    def get_objects_for_subject(
        self,
        subject_namespace: str,
        subject_id: str,
        relation: str | None = None,
        namespace: str | None = None,
    ) -> list[tuple[str, str]]:
        """
        Get all objects that a subject has relations to.

        Args:
            subject_namespace: The subject's namespace
            subject_id: The subject's ID
            relation: Optional filter by relation type
            namespace: Optional filter by object namespace

        Returns:
            List of (namespace, object_id) tuples
        """
        tuples = self.query_tuples(
            subject_namespace=subject_namespace,
            subject_id=subject_id,
            relation=relation,
            namespace=namespace,
        )

        return [(t.namespace, t.object_id) for t in tuples]

    def get_subjects_for_object(
        self,
        namespace: str,
        object_id: str,
        relation: str | None = None,
        subject_namespace: str | None = None,
    ) -> list[tuple[str, str]]:
        """
        Get all subjects that have relations to an object.

        Args:
            namespace: The object's namespace
            object_id: The object's ID
            relation: Optional filter by relation type
            subject_namespace: Optional filter by subject namespace

        Returns:
            List of (subject_namespace, subject_id) tuples
        """
        tuples = self.query_tuples(
            namespace=namespace,
            object_id=object_id,
            relation=relation,
            subject_namespace=subject_namespace,
        )

        return [(t.subject_namespace, t.subject_id) for t in tuples]

    def get_relations(self) -> set[str]:
        """Get all unique relation types in the store."""
        if self.is_empty():
            return set()
        return set(self._data._df["relation"].unique())

    def get_namespaces(self) -> set[str]:
        """Get all unique object namespaces in the store."""
        if self.is_empty():
            return set()
        return set(self._data._df["namespace"].unique())

    def get_subject_namespaces(self) -> set[str]:
        """Get all unique subject namespaces in the store."""
        if self.is_empty():
            return set()
        return set(self._data._df["subject_namespace"].unique())

    def __iter__(self) -> Iterator[RelationTuple]:
        """Iterate over all tuples in the store."""
        if self.is_empty():
            return iter([])

        for _, row in self._data._df.iterrows():
            yield RelationTuple.from_dict(row)

    def __len__(self) -> int:
        """Get the number of tuples in the store."""
        return self.size

    def __bool__(self) -> bool:
        """Check if the store has any tuples."""
        return not self.is_empty()

    def save(self, path: str) -> None:
        """Save the tuple store as a GraphAr-compliant permission graph.

        Creates a directory structure following Apache GraphAr specification:
        - _metadata.yaml: Graph metadata
        - _schema.yaml: Vertex and edge schemas
        - vertices/: Subject and object vertices
        - edges/: Permission tuples as edges grouped by relation

        Args:
            path: Directory path for the GraphAr permission graph

        Example:
            >>> store.save("./permissions_graph")
            # Creates:
            # permissions_graph/
            # ├── _metadata.yaml
            # ├── _schema.yaml
            # ├── vertices/
            # │   ├── user/part0.parquet
            # │   ├── board/part0.parquet
            # │   └── ...
            # └── edges/
            #     ├── owner/part0.parquet
            #     ├── editor/part0.parquet
            #     └── viewer/part0.parquet
        """
        base_path = Path(path)
        base_path.mkdir(parents=True, exist_ok=True)

        # Write GraphAr metadata and schema files (even for empty stores)
        self._write_graphar_metadata(base_path, "permissions")
        self._write_graphar_schema(base_path)

        # Create required directories (even for empty stores)
        vertices_path = base_path / "vertices"
        edges_path = base_path / "edges"
        vertices_path.mkdir(parents=True, exist_ok=True)
        edges_path.mkdir(parents=True, exist_ok=True)

        # Only create vertex/edge files if store has data
        if not self.is_empty():
            # Group tuples by relation type (owner/editor/viewer)
            edges_by_relation = self._group_by_relation()

            # Extract and save unique vertices
            vertices = self._extract_vertex_sets()
            self._save_vertices(base_path / "vertices", vertices)

            # Save edges by relation type
            self._save_edges(base_path / "edges", edges_by_relation)

    @classmethod
    def load(cls, path: str) -> TupleStore:
        """Load a tuple store from a GraphAr-compliant permission graph.

        Reads from a GraphAr directory structure and reconstructs relation tuples
        from the vertices and edges.

        Args:
            path: Directory path to the GraphAr permission graph

        Returns:
            TupleStore instance with loaded tuples

        Raises:
            FileNotFoundError: If the path doesn't exist
            ValueError: If the GraphAr structure is invalid

        Example:
            >>> store = TupleStore.load("./permissions_graph")
            >>> print(f"Loaded {len(store)} tuples")
        """
        base_path = Path(path)

        if not base_path.exists():
            raise FileNotFoundError(f"Permission graph not found: {path}")

        # Validate GraphAr structure
        cls._validate_graphar_structure(base_path)

        # Load all edges from relation directories
        tuples = []
        edges_path = base_path / "edges"

        if edges_path.exists() and edges_path.is_dir():
            for relation_dir in edges_path.iterdir():
                if relation_dir.is_dir():
                    relation_tuples = cls._load_relation_edges(relation_dir)
                    tuples.extend(relation_tuples)

        # Create TupleStore with loaded tuples
        store = cls()
        if tuples:
            store.add_tuples(tuples)

        return store

    def stats(self) -> dict[str, Any]:
        """Get statistics about the tuple store."""
        if self.is_empty():
            return {
                "total_tuples": 0,
                "unique_objects": 0,
                "unique_subjects": 0,
                "unique_relations": 0,
                "unique_namespaces": 0,
            }

        df = self._data._df
        return {
            "total_tuples": len(df),
            "unique_objects": df["object_ref"].nunique(),
            "unique_subjects": df["subject_ref"].nunique(),
            "unique_relations": df["relation"].nunique(),
            "unique_namespaces": df["namespace"].nunique()
            + df["subject_namespace"].nunique(),
        }

    # =========================================================================
    # GraphAr Compliance Helper Methods
    # =========================================================================

    def _write_graphar_metadata(self, base_path: Path, graph_name: str) -> None:
        """Generate _metadata.yaml for permission graph.

        Args:
            base_path: Base directory for the graph
            graph_name: Name of the graph (e.g., "permissions")
        """
        # Get vertex and edge info for metadata
        vertices_info = []
        edges_info = []

        # Add subjects vertex metadata
        subject_count = (
            len(self._data._df[["subject_namespace", "subject_id"]].drop_duplicates())
            if not self.is_empty()
            else 0
        )
        vertices_info.append(
            {
                "label": "subjects",
                "prefix": "vertices/subjects/",
                "count": subject_count,
            }
        )

        # Add objects vertex metadata
        object_count = (
            len(self._data._df[["namespace", "object_id"]].drop_duplicates())
            if not self.is_empty()
            else 0
        )
        vertices_info.append(
            {
                "label": "objects",
                "prefix": "vertices/objects/",
                "count": object_count,
            }
        )

        # Add edge metadata for each relation type
        relations = self.get_relations()
        for relation in sorted(relations):
            # Count edges for this relation
            edge_count = (
                len(self._data._df[self._data._df["relation"] == relation])
                if not self.is_empty()
                else 0
            )
            edges_info.append(
                {
                    "label": relation,
                    "prefix": f"edges/{relation}/",
                    "source": "subjects",
                    "target": "objects",
                    "count": edge_count,
                }
            )

        metadata = {
            "name": graph_name,
            "format": "graphar",
            "version": "1.0",
            "directed": True,
            "description": "Zanzibar-style permission graph with relation-based access control",
            "creator": "ParquetFrame Permissions System",
            "created_at": datetime.utcnow().isoformat() + "Z",
            "vertices": vertices_info,
            "edges": edges_info,
        }

        metadata_path = base_path / "_metadata.yaml"
        with open(metadata_path, "w", encoding="utf-8") as f:
            yaml.dump(metadata, f, default_flow_style=False, sort_keys=False)

    def _write_graphar_schema(self, base_path: Path) -> None:
        """Generate _schema.yaml for permission graph.

        Args:
            base_path: Base directory for the graph
        """
        # Get unique namespaces from tuples
        relations = self.get_relations()

        # Build vertex schemas - use "subjects" and "objects" as labels
        vertices = [
            {
                "label": "subjects",
                "properties": [
                    {
                        "name": "id",
                        "type": "string",
                        "description": "Subject identifier",
                    },
                    {
                        "name": "namespace",
                        "type": "string",
                        "description": "Subject namespace/type",
                    },
                ],
            },
            {
                "label": "objects",
                "properties": [
                    {
                        "name": "id",
                        "type": "string",
                        "description": "Object identifier",
                    },
                    {
                        "name": "namespace",
                        "type": "string",
                        "description": "Object namespace/type",
                    },
                ],
            },
        ]

        # Build edge schemas (one per relation type)
        edges = []
        for relation in sorted(relations):
            edges.append(
                {
                    "label": relation,
                    "source": "subjects",
                    "target": "objects",
                    "properties": [
                        {
                            "name": "subject_id",
                            "type": "string",
                            "description": "Subject ID",
                        },
                        {
                            "name": "object_id",
                            "type": "string",
                            "description": "Object ID",
                        },
                        {
                            "name": "subject_namespace",
                            "type": "string",
                            "description": "Type of subject",
                        },
                        {
                            "name": "object_namespace",
                            "type": "string",
                            "description": "Type of object",
                        },
                    ],
                }
            )

        schema = {
            "vertices": vertices,
            "edges": edges,
        }

        schema_path = base_path / "_schema.yaml"
        with open(schema_path, "w", encoding="utf-8") as f:
            yaml.dump(schema, f, default_flow_style=False, sort_keys=False)

    def _extract_vertex_sets(self) -> dict[str, set[str]]:
        """Extract unique subjects and objects as vertex sets.

        Returns:
            Dictionary mapping namespace to set of vertex IDs
        """
        vertices: dict[str, set[str]] = {}

        if self.is_empty():
            return vertices

        df = self._data._df

        # Extract subjects
        for _, row in (
            df[["subject_namespace", "subject_id"]].drop_duplicates().iterrows()
        ):
            ns = row["subject_namespace"]
            vid = row["subject_id"]
            if ns not in vertices:
                vertices[ns] = set()
            vertices[ns].add(vid)

        # Extract objects
        for _, row in df[["namespace", "object_id"]].drop_duplicates().iterrows():
            ns = row["namespace"]
            vid = row["object_id"]
            if ns not in vertices:
                vertices[ns] = set()
            vertices[ns].add(vid)

        return vertices

    def _group_by_relation(self) -> dict[str, list[RelationTuple]]:
        """Group tuples by relation type.

        Returns:
            Dictionary mapping relation type to list of tuples
        """
        groups: dict[str, list[RelationTuple]] = {}

        for tuple_obj in self:
            relation = tuple_obj.relation
            if relation not in groups:
                groups[relation] = []
            groups[relation].append(tuple_obj)

        return groups

    def _save_vertices(
        self, vertices_path: Path, vertices: dict[str, set[str]]
    ) -> None:
        """Save vertex sets to parquet files.

        Args:
            vertices_path: Base path for vertices directory
            vertices: Dictionary mapping namespace to vertex IDs
        """
        vertices_path.mkdir(parents=True, exist_ok=True)

        # Separate subjects and objects
        subject_namespaces = self.get_subject_namespaces()
        object_namespaces = self.get_namespaces()

        # Collect all subjects
        subjects_data = []
        for ns in subject_namespaces:
            if ns in vertices:
                for vid in vertices[ns]:
                    subjects_data.append({"id": vid, "namespace": ns})

        # Collect all objects
        objects_data = []
        for ns in object_namespaces:
            if ns in vertices:
                for vid in vertices[ns]:
                    objects_data.append({"id": vid, "namespace": ns})

        # Save subjects
        if subjects_data:
            subjects_dir = vertices_path / "subjects"
            subjects_dir.mkdir(exist_ok=True)
            subjects_df = pd.DataFrame(subjects_data)
            subjects_df = subjects_df.drop_duplicates()
            output_path = subjects_dir / "part0.parquet"
            subjects_df.to_parquet(output_path, index=False, compression="snappy")

        # Save objects
        if objects_data:
            objects_dir = vertices_path / "objects"
            objects_dir.mkdir(exist_ok=True)
            objects_df = pd.DataFrame(objects_data)
            objects_df = objects_df.drop_duplicates()
            output_path = objects_dir / "part0.parquet"
            objects_df.to_parquet(output_path, index=False, compression="snappy")

    def _save_edges(
        self, edges_path: Path, edges_by_relation: dict[str, list[RelationTuple]]
    ) -> None:
        """Save edges grouped by relation type.

        Args:
            edges_path: Base path for edges directory
            edges_by_relation: Dictionary mapping relation to tuples
        """
        edges_path.mkdir(parents=True, exist_ok=True)

        for relation, tuples in edges_by_relation.items():
            relation_dir = edges_path / relation
            relation_dir.mkdir(exist_ok=True)

            # Create DataFrame with edge data
            edge_data = []
            for t in tuples:
                edge_data.append(
                    {
                        "subject_id": t.subject_id,
                        "object_id": t.object_id,
                        "subject_namespace": t.subject_namespace,
                        "object_namespace": t.namespace,
                    }
                )

            edge_df = pd.DataFrame(edge_data)

            # Save to parquet
            output_path = relation_dir / "part0.parquet"
            edge_df.to_parquet(output_path, index=False, compression="snappy")

    @classmethod
    def _validate_graphar_structure(cls, base_path: Path) -> None:
        """Validate that the directory follows GraphAr structure.

        Args:
            base_path: Base directory to validate

        Raises:
            ValueError: If structure is invalid
        """
        required_files = ["_metadata.yaml", "_schema.yaml"]
        for filename in required_files:
            file_path = base_path / filename
            if not file_path.exists():
                raise FileNotFoundError(
                    f"Invalid GraphAr structure: missing {filename}. "
                    f"Expected GraphAr-compliant directory with metadata and schema files."
                )

        # Check for vertices and edges directories
        vertices_path = base_path / "vertices"
        edges_path = base_path / "edges"

        if not vertices_path.exists() or not vertices_path.is_dir():
            raise FileNotFoundError(
                "Invalid GraphAr structure: missing vertices/ directory. "
                "Permission graph must contain vertex data."
            )

        if not edges_path.exists() or not edges_path.is_dir():
            raise FileNotFoundError(
                "Invalid GraphAr structure: missing edges/ directory. "
                "Permission graph must contain edges with relation types."
            )

    @classmethod
    def _load_relation_edges(cls, relation_dir: Path) -> list[RelationTuple]:
        """Load edges from a single relation directory.

        Args:
            relation_dir: Directory containing edges for one relation type

        Returns:
            List of RelationTuple objects
        """
        tuples = []
        relation = relation_dir.name

        # Read all parquet files in the relation directory
        for parquet_file in relation_dir.glob("*.parquet"):
            edge_df = pd.read_parquet(parquet_file)

            for _, row in edge_df.iterrows():
                # Handle both old (src/dst) and new (subject_id/object_id) column names
                subject_id = row.get("subject_id", row.get("src"))
                object_id = row.get("object_id", row.get("dst"))

                tuple_obj = RelationTuple(
                    namespace=row["object_namespace"],
                    object_id=object_id,
                    relation=relation,
                    subject_namespace=row["subject_namespace"],
                    subject_id=subject_id,
                )
                tuples.append(tuple_obj)

        return tuples
