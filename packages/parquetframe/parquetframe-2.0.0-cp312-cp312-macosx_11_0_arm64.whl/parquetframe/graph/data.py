"""
Graph data structures for vertex and edge sets.

This module provides VertexSet and EdgeSet classes that encapsulate
parquet row-groups with property schemas, supporting lazy loading
with pandas or Dask backends based on ParquetFrame conventions.
"""

import warnings
from pathlib import Path
from typing import Any

from ..core_legacy import (
    ParquetFrame,  # Internal use only - avoids deprecation warnings
)


class VertexSet:
    """
    A collection of vertices with associated properties.

    VertexSet encapsulates vertex data stored in Parquet format with
    schema information and property metadata. It supports lazy loading
    and automatic backend selection consistent with ParquetFrame.

    Attributes:
        data: ParquetFrame containing vertex data
        vertex_type: Type name of the vertices (e.g., "users", "pages")
        properties: Dict of property metadata from schema
        schema: Full schema definition for this vertex type

    Examples:
        Access vertex data:
            >>> vertices = VertexSet.from_parquet("vertices/users/")
            >>> print(f"Loaded {len(vertices)} users")
            >>> active_users = vertices.data.query("status == 'active'")

        Property access:
            >>> print(vertices.properties)  # {'name': 'string', 'age': 'int64'}
            >>> user_names = vertices.data['name']
    """

    def __init__(
        self,
        data: ParquetFrame,
        vertex_type: str,
        properties: dict[str, Any],
        schema: dict[str, Any] | None = None,
    ):
        """
        Initialize a VertexSet.

        Args:
            data: ParquetFrame containing vertex data
            vertex_type: Type name for these vertices
            properties: Property metadata from schema
            schema: Full schema definition for vertex type
        """
        self.data = data
        self.vertex_type = vertex_type
        self.properties = properties
        self.schema = schema or {}

        # Validate essential columns
        self._validate_vertex_schema()

    @classmethod
    def from_parquet(
        cls,
        path: str | Path,
        vertex_type: str | None = None,
        threshold_mb: float | None = None,
        islazy: bool | None = None,
        properties: dict[str, Any] | None = None,
        schema: dict[str, Any] | None = None,
    ) -> "VertexSet":
        """
        Create a VertexSet from Parquet files.

        Args:
            path: Path to vertex parquet files or directory
            vertex_type: Type name (inferred from path if not provided)
            threshold_mb: Size threshold for backend selection
            islazy: Force backend selection (True=Dask, False=pandas)
            properties: Property metadata
            schema: Schema definition

        Returns:
            VertexSet instance with loaded data

        Examples:
            >>> vertices = VertexSet.from_parquet("vertices/users/")
            >>> vertices = VertexSet.from_parquet("users.parquet", vertex_type="users")
        """
        # Load data using ParquetFrame
        data = ParquetFrame.read(path, threshold_mb=threshold_mb, islazy=islazy)

        # Infer vertex type from path if not provided
        if vertex_type is None:
            path_obj = Path(path)
            if path_obj.is_dir():
                vertex_type = path_obj.name
            else:
                # Use parent directory name or stem
                vertex_type = path_obj.parent.name or path_obj.stem

        # Default empty properties if not provided
        properties = properties or {}

        return cls(
            data=data,
            vertex_type=vertex_type,
            properties=properties,
            schema=schema,
        )

    def _validate_vertex_schema(self) -> None:
        """
        Validate vertex data has required columns and schema compliance.

        Raises:
            ValueError: If required vertex columns are missing
        """
        columns = list(self.data.columns)

        # Check for vertex ID column (flexible naming)
        id_columns = [
            col for col in columns if col.lower() in ("id", "vertex_id", "node_id")
        ]

        if not id_columns:
            warnings.warn(
                f"Vertex data for type '{self.vertex_type}' has no ID column. "
                "Expected one of: 'id', 'vertex_id', 'node_id'",
                UserWarning,
                stacklevel=2,
            )
        elif len(id_columns) > 1:
            warnings.warn(
                f"Multiple ID columns found: {id_columns}. Using '{id_columns[0]}'",
                UserWarning,
                stacklevel=2,
            )

        # Validate property types if schema is provided
        if self.schema and "properties" in self.schema:
            self._validate_property_types()

    def _validate_property_types(self) -> None:
        """Validate data types match schema definitions."""
        schema_props = self.schema.get("properties", {})
        data_dtypes = dict(self.data.dtypes)

        for prop_name, prop_def in schema_props.items():
            if prop_name in data_dtypes:
                expected_type = prop_def.get("type")
                actual_dtype = str(data_dtypes[prop_name])

                # Basic type compatibility check
                if expected_type and not self._types_compatible(
                    expected_type, actual_dtype
                ):
                    warnings.warn(
                        f"Type mismatch for property '{prop_name}': "
                        f"expected {expected_type}, got {actual_dtype}",
                        UserWarning,
                        stacklevel=3,
                    )

    def _types_compatible(self, schema_type: str, pandas_dtype: str) -> bool:
        """Check if schema type and pandas dtype are compatible."""
        # Simple compatibility mapping
        compatibility_map = {
            "string": ["object", "string"],
            "integer": ["int32", "int64", "Int32", "Int64"],
            "float": ["float32", "float64", "Float32", "Float64"],
            "boolean": ["bool", "boolean"],
            "timestamp": ["datetime64", "timestamp"],
        }

        compatible_types = compatibility_map.get(schema_type.lower(), [])
        return any(dtype in pandas_dtype for dtype in compatible_types)

    @property
    def id_column(self) -> str | None:
        """Name of the vertex ID column."""
        columns = list(self.data.columns)
        id_columns = [
            col for col in columns if col.lower() in ("id", "vertex_id", "node_id")
        ]
        return id_columns[0] if id_columns else None

    @property
    def num_vertices(self) -> int:
        """Number of vertices in this set."""
        return len(self.data)

    @property
    def property_columns(self) -> list[str]:
        """List of property column names (excluding ID)."""
        all_columns = list(self.data.columns)
        id_col = self.id_column
        return [col for col in all_columns if col != id_col]

    def get_vertices_by_ids(self, vertex_ids: list[int]) -> ParquetFrame:
        """
        Get subset of vertices by their IDs.

        Args:
            vertex_ids: List of vertex IDs to retrieve

        Returns:
            ParquetFrame with matching vertices

        Examples:
            >>> user_subset = vertices.get_vertices_by_ids([1, 5, 10, 25])
            >>> print(len(user_subset))  # Number of found vertices
        """
        id_col = self.id_column
        if not id_col:
            raise ValueError("Cannot filter by ID: no ID column found")

        mask = self.data[id_col].isin(vertex_ids)
        return self.data[mask]

    def __len__(self) -> int:
        """Number of vertices in this set."""
        return self.num_vertices

    def __repr__(self) -> str:
        """String representation of the VertexSet."""
        return f"VertexSet(type='{self.vertex_type}', vertices={self.num_vertices:,})"


class EdgeSet:
    """
    A collection of edges with associated properties.

    EdgeSet encapsulates edge data stored in Parquet format with
    schema information and property metadata. It supports lazy loading
    and automatic backend selection consistent with ParquetFrame.

    Attributes:
        data: ParquetFrame containing edge data
        edge_type: Type name of the edges (e.g., "follows", "likes")
        properties: Dict of property metadata from schema
        schema: Full schema definition for this edge type

    Examples:
        Access edge data:
            >>> edges = EdgeSet.from_parquet("edges/follows/")
            >>> print(f"Loaded {len(edges)} follow relationships")
            >>> recent_follows = edges.data.query("timestamp > '2024-01-01'")

        Property access:
            >>> print(edges.properties)  # {'weight': 'float64', 'timestamp': 'datetime64'}
            >>> follow_weights = edges.data['weight']
    """

    def __init__(
        self,
        data: ParquetFrame,
        edge_type: str,
        properties: dict[str, Any],
        schema: dict[str, Any] | None = None,
    ):
        """
        Initialize an EdgeSet.

        Args:
            data: ParquetFrame containing edge data
            edge_type: Type name for these edges
            properties: Property metadata from schema
            schema: Full schema definition for edge type
        """
        self.data = data
        self.edge_type = edge_type
        self.properties = properties
        self.schema = schema or {}

        # Validate essential columns
        self._validate_edge_schema()

    @classmethod
    def from_parquet(
        cls,
        path: str | Path,
        edge_type: str | None = None,
        threshold_mb: float | None = None,
        islazy: bool | None = None,
        properties: dict[str, Any] | None = None,
        schema: dict[str, Any] | None = None,
    ) -> "EdgeSet":
        """
        Create an EdgeSet from Parquet files.

        Args:
            path: Path to edge parquet files or directory
            edge_type: Type name (inferred from path if not provided)
            threshold_mb: Size threshold for backend selection
            islazy: Force backend selection (True=Dask, False=pandas)
            properties: Property metadata
            schema: Schema definition

        Returns:
            EdgeSet instance with loaded data

        Examples:
            >>> edges = EdgeSet.from_parquet("edges/follows/")
            >>> edges = EdgeSet.from_parquet("follows.parquet", edge_type="follows")
        """
        # Load data using ParquetFrame
        data = ParquetFrame.read(path, threshold_mb=threshold_mb, islazy=islazy)

        # Infer edge type from path if not provided
        if edge_type is None:
            path_obj = Path(path)
            if path_obj.is_dir():
                edge_type = path_obj.name
            else:
                # Use parent directory name or stem
                edge_type = path_obj.parent.name or path_obj.stem

        # Default empty properties if not provided
        properties = properties or {}

        return cls(
            data=data,
            edge_type=edge_type,
            properties=properties,
            schema=schema,
        )

    def _validate_edge_schema(self) -> None:
        """
        Validate edge data has required columns and schema compliance.

        Raises:
            ValueError: If required edge columns are missing
        """
        columns = list(self.data.columns)

        # Check for source/target columns (flexible naming)
        src_columns = [
            col
            for col in columns
            if col.lower() in ("src", "source", "from", "from_id")
        ]
        dst_columns = [
            col for col in columns if col.lower() in ("dst", "target", "to", "to_id")
        ]

        if not src_columns:
            raise ValueError(
                f"Edge data for type '{self.edge_type}' missing source column. "
                "Expected one of: 'src', 'source', 'from', 'from_id'"
            )
        if not dst_columns:
            raise ValueError(
                f"Edge data for type '{self.edge_type}' missing target column. "
                "Expected one of: 'dst', 'target', 'to', 'to_id'"
            )

        if len(src_columns) > 1:
            warnings.warn(
                f"Multiple source columns found: {src_columns}. Using '{src_columns[0]}'",
                UserWarning,
                stacklevel=2,
            )
        if len(dst_columns) > 1:
            warnings.warn(
                f"Multiple target columns found: {dst_columns}. Using '{dst_columns[0]}'",
                UserWarning,
                stacklevel=2,
            )

        # Validate property types if schema is provided
        if self.schema and "properties" in self.schema:
            self._validate_property_types()

    def _validate_property_types(self) -> None:
        """Validate data types match schema definitions."""
        # Same implementation as VertexSet
        schema_props = self.schema.get("properties", {})
        data_dtypes = dict(self.data.dtypes)

        for prop_name, prop_def in schema_props.items():
            if prop_name in data_dtypes:
                expected_type = prop_def.get("type")
                actual_dtype = str(data_dtypes[prop_name])

                if expected_type and not self._types_compatible(
                    expected_type, actual_dtype
                ):
                    warnings.warn(
                        f"Type mismatch for property '{prop_name}': "
                        f"expected {expected_type}, got {actual_dtype}",
                        UserWarning,
                        stacklevel=3,
                    )

    def _types_compatible(self, schema_type: str, pandas_dtype: str) -> bool:
        """Check if schema type and pandas dtype are compatible."""
        # Same implementation as VertexSet
        compatibility_map = {
            "string": ["object", "string"],
            "integer": ["int32", "int64", "Int32", "Int64"],
            "float": ["float32", "float64", "Float32", "Float64"],
            "boolean": ["bool", "boolean"],
            "timestamp": ["datetime64", "timestamp"],
        }

        compatible_types = compatibility_map.get(schema_type.lower(), [])
        return any(dtype in pandas_dtype for dtype in compatible_types)

    @property
    def src_column(self) -> str | None:
        """Name of the source vertex column."""
        columns = list(self.data.columns)
        src_columns = [
            col
            for col in columns
            if col.lower() in ("src", "source", "from", "from_id")
        ]
        return src_columns[0] if src_columns else None

    @property
    def dst_column(self) -> str | None:
        """Name of the target vertex column."""
        columns = list(self.data.columns)
        dst_columns = [
            col for col in columns if col.lower() in ("dst", "target", "to", "to_id")
        ]
        return dst_columns[0] if dst_columns else None

    @property
    def num_edges(self) -> int:
        """Number of edges in this set."""
        return len(self.data)

    @property
    def property_columns(self) -> list[str]:
        """List of property column names (excluding src/dst)."""
        all_columns = list(self.data.columns)
        src_col = self.src_column
        dst_col = self.dst_column
        return [col for col in all_columns if col not in (src_col, dst_col)]

    def get_edges_from_vertex(self, vertex_id: int) -> ParquetFrame:
        """
        Get all edges originating from a specific vertex.

        Args:
            vertex_id: Source vertex ID

        Returns:
            ParquetFrame with matching edges

        Examples:
            >>> user_follows = edges.get_edges_from_vertex(user_id=123)
            >>> print(f"User 123 follows {len(user_follows)} people")
        """
        src_col = self.src_column
        if not src_col:
            raise ValueError("Cannot filter by source: no source column found")

        return self.data[self.data[src_col] == vertex_id]

    def get_edges_to_vertex(self, vertex_id: int) -> ParquetFrame:
        """
        Get all edges targeting a specific vertex.

        Args:
            vertex_id: Target vertex ID

        Returns:
            ParquetFrame with matching edges

        Examples:
            >>> user_followers = edges.get_edges_to_vertex(user_id=123)
            >>> print(f"User 123 has {len(user_followers)} followers")
        """
        dst_col = self.dst_column
        if not dst_col:
            raise ValueError("Cannot filter by target: no target column found")

        return self.data[self.data[dst_col] == vertex_id]

    def get_edges_between_vertices(
        self, src_ids: list[int], dst_ids: list[int]
    ) -> ParquetFrame:
        """
        Get edges between specific sets of vertices.

        Args:
            src_ids: List of source vertex IDs
            dst_ids: List of target vertex IDs

        Returns:
            ParquetFrame with edges from src_ids to dst_ids

        Examples:
            >>> connections = edges.get_edges_between_vertices([1, 2, 3], [10, 20, 30])
            >>> print(f"Found {len(connections)} connections")
        """
        src_col = self.src_column
        dst_col = self.dst_column

        if not src_col or not dst_col:
            raise ValueError("Cannot filter edges: missing source or target columns")

        mask = self.data[src_col].isin(src_ids) & self.data[dst_col].isin(dst_ids)
        return self.data[mask]

    def __len__(self) -> int:
        """Number of edges in this set."""
        return self.num_edges

    def __repr__(self) -> str:
        """String representation of the EdgeSet."""
        return f"EdgeSet(type='{self.edge_type}', edges={self.num_edges:,})"
