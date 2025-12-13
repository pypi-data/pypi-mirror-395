"""
Adjacency list representations for efficient graph traversal.

This module implements Compressed Sparse Row (CSR) and Compressed Sparse Column (CSC)
formats for representing graph adjacency information. These structures enable efficient
neighbor lookups, degree calculations, and graph traversal algorithms.

The implementations use numpy arrays for optimal performance and memory efficiency,
with integration for both pandas and Dask backends.
"""

import warnings

import numpy as np

from .data import EdgeSet
from .rust_backend import RUST_AVAILABLE, build_csc_rust, build_csr_rust


class CSRAdjacency:
    """
    Compressed Sparse Row (CSR) adjacency representation.

    CSR format is optimized for fast outgoing edge queries - given a vertex,
    quickly find all vertices it connects to. This is ideal for algorithms
    that need to traverse outgoing edges efficiently.

    The CSR format uses three arrays:
    - indices: Target vertex IDs for each edge
    - indptr: Index pointers marking start of each vertex's neighbors
    - data: Optional edge weights/properties

    Memory usage: O(V + E) where V=vertices, E=edges
    Neighbor lookup: O(degree) - very fast for sparse graphs

    Examples:
        Create from EdgeSet:
            >>> edges = EdgeSet.from_parquet("edges/follows/")
            >>> csr = CSRAdjacency.from_edge_set(edges)
            >>> neighbors = csr.neighbors(vertex_id=123)
            >>> degree = csr.degree(vertex_id=123)

        Manual construction:
            >>> csr = CSRAdjacency(
            ...     indices=[1, 2, 0, 2, 0, 1],  # Target vertices
            ...     indptr=[0, 2, 4, 6],         # Vertex boundaries
            ...     num_vertices=3
            ... )
    """

    def __init__(
        self,
        indices: np.ndarray,
        indptr: np.ndarray,
        data: np.ndarray | None = None,
        num_vertices: int | None = None,
    ):
        """
        Initialize CSR adjacency structure.

        Args:
            indices: Array of target vertex IDs (length = num_edges)
            indptr: Index pointers for vertex boundaries (length = num_vertices + 1)
            data: Optional edge weights/properties (length = num_edges)
            num_vertices: Number of vertices (inferred if not provided)
        """
        self.indices = np.asarray(indices, dtype=np.int64)
        self.indptr = np.asarray(indptr, dtype=np.int64)
        self.data = np.asarray(data) if data is not None else None
        self._num_vertices = num_vertices or (len(self.indptr) - 1)

        # Validate array dimensions
        if len(self.indptr) < 1:
            raise ValueError("indptr must have at least 1 element")
        if self.indptr[0] != 0:
            raise ValueError("indptr[0] must be 0")
        if self.indptr[-1] != len(self.indices):
            raise ValueError("indptr[-1] must equal len(indices)")
        # For standard CSR: len(indptr) should be num_vertices + 1
        expected_indptr_len = self._num_vertices + 1 if self._num_vertices > 0 else 1
        if len(self.indptr) != expected_indptr_len:
            raise ValueError(
                f"indptr length {len(self.indptr)} != {expected_indptr_len} (num_vertices + 1)"
            )
        if self.data is not None and len(self.data) != len(self.indices):
            raise ValueError("data and indices must have same length")

    @classmethod
    def from_edge_set(
        cls,
        edge_set: EdgeSet,
        include_weights: bool = False,
        weight_column: str | None = None,
        num_vertices: int | None = None,
    ) -> "CSRAdjacency":
        """
        Create CSR adjacency from an EdgeSet.

        Args:
            edge_set: EdgeSet containing edge data
            include_weights: Whether to include edge weights in data array
            weight_column: Column name for edge weights (auto-detected if None)
            num_vertices: Explicit vertex count (inferred from edges if None)

        Returns:
            CSRAdjacency instance

        Examples:
            >>> edges = EdgeSet.from_parquet("social_network/edges/follows/")
            >>> csr = CSRAdjacency.from_edge_set(edges)
            >>> csr_weighted = CSRAdjacency.from_edge_set(edges, include_weights=True)
        """
        # Get source and destination columns
        src_col = edge_set.src_column
        dst_col = edge_set.dst_column

        if not src_col or not dst_col:
            raise ValueError("EdgeSet missing required source/destination columns")

        # Extract edge data - convert to pandas if using Dask
        edge_data = edge_set.data
        if edge_data.islazy:
            warnings.warn(
                "Converting Dask EdgeSet to pandas for adjacency construction. "
                "This may be slow for very large graphs.",
                UserWarning,
                stacklevel=2,
            )
            edge_data = edge_data.to_pandas()

        df = edge_data
        sources = df[src_col].values.astype(np.int64)
        targets = df[dst_col].values.astype(np.int64)

        # Handle weights if requested
        weights = None
        if include_weights:
            if weight_column:
                if weight_column not in df.columns:
                    raise ValueError(f"Weight column '{weight_column}' not found")
                weights = df[weight_column].values
            else:
                # Try to find a suitable weight column
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                weight_candidates = [
                    col for col in numeric_cols if col not in (src_col, dst_col)
                ]
                if weight_candidates:
                    weight_column = weight_candidates[0]
                    weights = df[weight_column].values
                    warnings.warn(
                        f"Auto-selected weight column: '{weight_column}'",
                        UserWarning,
                        stacklevel=2,
                    )

        # Determine vertex range
        if num_vertices is None:
            # Infer from edges if not explicitly provided
            if len(sources) == 0:
                num_vertices = 0
            else:
                num_vertices = max(sources.max(), targets.max()) + 1

        # Build CSR format
        if num_vertices == 0:
            # Handle empty graph case
            return cls(
                indices=np.array([], dtype=np.int64),
                indptr=np.array([0], dtype=np.int64),
                data=None,
                num_vertices=0,
            )

        # Try Rust backend first for performance
        if RUST_AVAILABLE:
            try:
                indptr, indices, weights_out = build_csr_rust(
                    sources, targets, num_vertices, weights
                )
                return cls(
                    indices=indices,
                    indptr=indptr,
                    data=weights_out,
                    num_vertices=num_vertices,
                )
            except Exception as e:
                warnings.warn(
                    f"Rust CSR construction failed ({e}), falling back to Python",
                    UserWarning,
                    stacklevel=2,
                )

        # Fallback to Python implementation
        # Sort edges by source vertex for efficient construction
        sort_idx = np.argsort(sources)
        sources_sorted = sources[sort_idx]
        targets_sorted = targets[sort_idx]
        weights_sorted = weights[sort_idx] if weights is not None else None

        # Build indptr array - count edges per source vertex
        indptr = np.zeros(num_vertices + 1, dtype=np.int64)
        for src in sources_sorted:
            indptr[src + 1] += 1
        # Convert counts to cumulative indices
        np.cumsum(indptr, out=indptr)

        return cls(
            indices=targets_sorted,
            indptr=indptr,
            data=weights_sorted,
            num_vertices=num_vertices,
        )

    @property
    def num_vertices(self) -> int:
        """Number of vertices in the graph."""
        return self._num_vertices

    @property
    def num_edges(self) -> int:
        """Number of edges in the graph."""
        return len(self.indices)

    @property
    def has_weights(self) -> bool:
        """Whether the adjacency includes edge weights."""
        return self.data is not None

    def neighbors(self, vertex: int) -> np.ndarray:
        """
        Get neighboring vertices for a given vertex (outgoing edges).

        Args:
            vertex: Source vertex ID

        Returns:
            Array of target vertex IDs

        Examples:
            >>> neighbors = csr.neighbors(123)  # All vertices that 123 connects to
            >>> print(f"Vertex 123 connects to: {neighbors}")
        """
        if vertex < 0 or vertex >= self.num_vertices:
            raise ValueError(f"Vertex {vertex} out of range [0, {self.num_vertices})")

        start = self.indptr[vertex]
        end = self.indptr[vertex + 1]
        return self.indices[start:end].copy()

    def degree(self, vertex: int) -> int:
        """
        Get the out-degree of a vertex.

        Args:
            vertex: Vertex ID

        Returns:
            Number of outgoing edges

        Examples:
            >>> degree = csr.degree(123)
            >>> print(f"Vertex 123 has out-degree: {degree}")
        """
        if vertex < 0 or vertex >= self.num_vertices:
            raise ValueError(f"Vertex {vertex} out of range [0, {self.num_vertices})")

        return int(self.indptr[vertex + 1] - self.indptr[vertex])

    def edge_weights(self, vertex: int) -> np.ndarray | None:
        """
        Get edge weights for outgoing edges from a vertex.

        Args:
            vertex: Source vertex ID

        Returns:
            Array of edge weights, or None if no weights stored

        Examples:
            >>> weights = csr.edge_weights(123)
            >>> if weights is not None:
            ...     print(f"Edge weights: {weights}")
        """
        if not self.has_weights:
            return None

        if vertex < 0 or vertex >= self.num_vertices:
            raise ValueError(f"Vertex {vertex} out of range [0, {self.num_vertices})")

        start = self.indptr[vertex]
        end = self.indptr[vertex + 1]
        return self.data[start:end].copy()

    def has_edge(self, source: int, target: int) -> bool:
        """
        Check if an edge exists between two vertices.

        Args:
            source: Source vertex ID
            target: Target vertex ID

        Returns:
            True if edge exists, False otherwise

        Examples:
            >>> if csr.has_edge(123, 456):
            ...     print("Edge 123 -> 456 exists")
        """
        if source < 0 or source >= self.num_vertices:
            return False

        neighbors = self.neighbors(source)
        return target in neighbors

    def subgraph(self, vertices: list[int] | set[int] | np.ndarray) -> "CSRAdjacency":
        """
        Extract a subgraph containing only the specified vertices.

        Args:
            vertices: Collection of vertex IDs to include

        Returns:
            New CSRAdjacency with only edges between specified vertices

        Examples:
            >>> important_vertices = [1, 5, 10, 23, 45]
            >>> subgraph = csr.subgraph(important_vertices)
            >>> print(f"Subgraph has {subgraph.num_edges} edges")
        """
        vertex_set = set(vertices)
        vertex_mapping = {v: i for i, v in enumerate(sorted(vertex_set))}
        new_num_vertices = len(vertex_mapping)

        new_indices = []
        new_indptr = [0]
        new_data = [] if self.has_weights else None

        for vertex in sorted(vertex_set):
            if vertex >= self.num_vertices:
                # Vertex doesn't exist in original graph
                new_indptr.append(len(new_indices))
                continue

            neighbors = self.neighbors(vertex)
            weights = self.edge_weights(vertex) if self.has_weights else None

            # Keep only edges to vertices in the subgraph
            for i, neighbor in enumerate(neighbors):
                if neighbor in vertex_set:
                    new_indices.append(vertex_mapping[neighbor])
                    if weights is not None:
                        new_data.append(weights[i])

            new_indptr.append(len(new_indices))

        return CSRAdjacency(
            indices=np.array(new_indices, dtype=np.int64),
            indptr=np.array(new_indptr, dtype=np.int64),
            data=np.array(new_data) if new_data is not None else None,
            num_vertices=new_num_vertices,
        )

    def to_dense(self) -> np.ndarray:
        """
        Convert to dense adjacency matrix (use carefully for large graphs).

        Returns:
            Dense boolean adjacency matrix

        Examples:
            >>> dense = csr.to_dense()  # Only for small graphs!
            >>> print(dense.shape)  # (num_vertices, num_vertices)
        """
        if self.num_vertices > 10000:
            warnings.warn(
                f"Converting large graph ({self.num_vertices} vertices) to dense matrix. "
                "This may use excessive memory.",
                UserWarning,
                stacklevel=2,
            )

        dense = np.zeros((self.num_vertices, self.num_vertices), dtype=bool)
        for vertex in range(self.num_vertices):
            neighbors = self.neighbors(vertex)
            if len(neighbors) > 0:
                dense[vertex, neighbors] = True
        return dense

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"CSRAdjacency({self.num_vertices:,} vertices, {self.num_edges:,} edges"
            f"{', weighted' if self.has_weights else ''})"
        )


class CSCAdjacency:
    """
    Compressed Sparse Column (CSC) adjacency representation.

    CSC format is optimized for fast incoming edge queries - given a vertex,
    quickly find all vertices that connect to it. This is ideal for algorithms
    that need to traverse incoming edges efficiently (e.g., PageRank).

    The CSC format uses three arrays:
    - indices: Source vertex IDs for each edge
    - indptr: Index pointers marking start of each vertex's predecessors
    - data: Optional edge weights/properties

    Memory usage: O(V + E) where V=vertices, E=edges
    Predecessor lookup: O(in-degree) - very fast for sparse graphs

    Examples:
        Create from EdgeSet:
            >>> edges = EdgeSet.from_parquet("edges/follows/")
            >>> csc = CSCAdjacency.from_edge_set(edges)
            >>> predecessors = csc.predecessors(vertex_id=123)
            >>> in_degree = csc.degree(vertex_id=123)
    """

    def __init__(
        self,
        indices: np.ndarray,
        indptr: np.ndarray,
        data: np.ndarray | None = None,
        num_vertices: int | None = None,
    ):
        """
        Initialize CSC adjacency structure.

        Args:
            indices: Array of source vertex IDs (length = num_edges)
            indptr: Index pointers for vertex boundaries (length = num_vertices + 1)
            data: Optional edge weights/properties (length = num_edges)
            num_vertices: Number of vertices (inferred if not provided)
        """
        self.indices = np.asarray(indices, dtype=np.int64)
        self.indptr = np.asarray(indptr, dtype=np.int64)
        self.data = np.asarray(data) if data is not None else None
        self._num_vertices = num_vertices or (len(self.indptr) - 1)

        # Validate array dimensions
        if len(self.indptr) < 1:
            raise ValueError("indptr must have at least 1 element")
        if self.indptr[0] != 0:
            raise ValueError("indptr[0] must be 0")
        if self.indptr[-1] != len(self.indices):
            raise ValueError("indptr[-1] must equal len(indices)")
        # For standard CSC: len(indptr) should be num_vertices + 1
        expected_indptr_len = self._num_vertices + 1 if self._num_vertices > 0 else 1
        if len(self.indptr) != expected_indptr_len:
            raise ValueError(
                f"indptr length {len(self.indptr)} != {expected_indptr_len} (num_vertices + 1)"
            )
        if self.data is not None and len(self.data) != len(self.indices):
            raise ValueError("data and indices must have same length")

    @classmethod
    def from_edge_set(
        cls,
        edge_set: EdgeSet,
        include_weights: bool = False,
        weight_column: str | None = None,
        num_vertices: int | None = None,
    ) -> "CSCAdjacency":
        """
        Create CSC adjacency from an EdgeSet.

        Args:
            edge_set: EdgeSet containing edge data
            include_weights: Whether to include edge weights in data array
            weight_column: Column name for edge weights (auto-detected if None)
            num_vertices: Explicit vertex count (inferred from edges if None)

        Returns:
            CSCAdjacency instance
        """
        # Get source and destination columns
        src_col = edge_set.src_column
        dst_col = edge_set.dst_column

        if not src_col or not dst_col:
            raise ValueError("EdgeSet missing required source/destination columns")

        # Extract edge data - convert to pandas if using Dask
        edge_data = edge_set.data
        if edge_data.islazy:
            warnings.warn(
                "Converting Dask EdgeSet to pandas for adjacency construction. "
                "This may be slow for very large graphs.",
                UserWarning,
                stacklevel=2,
            )
            edge_data = edge_data.to_pandas()

        df = edge_data
        sources = df[src_col].values.astype(np.int64)
        targets = df[dst_col].values.astype(np.int64)

        # Handle weights if requested
        weights = None
        if include_weights:
            if weight_column:
                if weight_column not in df.columns:
                    raise ValueError(f"Weight column '{weight_column}' not found")
                weights = df[weight_column].values
            else:
                # Try to find a suitable weight column
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                weight_candidates = [
                    col for col in numeric_cols if col not in (src_col, dst_col)
                ]
                if weight_candidates:
                    weight_column = weight_candidates[0]
                    weights = df[weight_column].values
                    warnings.warn(
                        f"Auto-selected weight column: '{weight_column}'",
                        UserWarning,
                        stacklevel=2,
                    )

        # Determine vertex range
        if num_vertices is None:
            # Infer from edges if not explicitly provided
            if len(sources) == 0:
                num_vertices = 0
            else:
                num_vertices = max(sources.max(), targets.max()) + 1

        # Build CSC format
        if num_vertices == 0:
            # Handle empty graph case
            return cls(
                indices=np.array([], dtype=np.int64),
                indptr=np.array([0], dtype=np.int64),
                data=None,
                num_vertices=0,
            )

        # Try Rust backend first for performance
        if RUST_AVAILABLE:
            try:
                indptr, indices, weights_out = build_csc_rust(
                    sources, targets, num_vertices, weights
                )
                return cls(
                    indices=indices,
                    indptr=indptr,
                    data=weights_out,
                    num_vertices=num_vertices,
                )
            except Exception as e:
                warnings.warn(
                    f"Rust CSC construction failed ({e}), falling back to Python",
                    UserWarning,
                    stacklevel=2,
                )

        # Fallback to Python implementation
        # Sort by target vertex
        sort_idx = np.argsort(targets)
        sources_sorted = sources[sort_idx]
        targets_sorted = targets[sort_idx]
        weights_sorted = weights[sort_idx] if weights is not None else None

        # Build indptr array - count edges per target vertex
        indptr = np.zeros(num_vertices + 1, dtype=np.int64)
        for tgt in targets_sorted:
            indptr[tgt + 1] += 1
        # Convert counts to cumulative indices
        np.cumsum(indptr, out=indptr)

        return cls(
            indices=sources_sorted,
            indptr=indptr,
            data=weights_sorted,
            num_vertices=num_vertices,
        )

    @property
    def num_vertices(self) -> int:
        """Number of vertices in the graph."""
        return self._num_vertices

    @property
    def num_edges(self) -> int:
        """Number of edges in the graph."""
        return len(self.indices)

    @property
    def has_weights(self) -> bool:
        """Whether the adjacency includes edge weights."""
        return self.data is not None

    def predecessors(self, vertex: int) -> np.ndarray:
        """
        Get predecessor vertices for a given vertex (incoming edges).

        Args:
            vertex: Target vertex ID

        Returns:
            Array of source vertex IDs

        Examples:
            >>> predecessors = csc.predecessors(123)  # All vertices that connect to 123
            >>> print(f"Vertex 123 has predecessors: {predecessors}")
        """
        if vertex < 0 or vertex >= self.num_vertices:
            raise ValueError(f"Vertex {vertex} out of range [0, {self.num_vertices})")

        start = self.indptr[vertex]
        end = self.indptr[vertex + 1]
        return self.indices[start:end].copy()

    def degree(self, vertex: int) -> int:
        """
        Get the in-degree of a vertex.

        Args:
            vertex: Vertex ID

        Returns:
            Number of incoming edges

        Examples:
            >>> degree = csc.degree(123)
            >>> print(f"Vertex 123 has in-degree: {degree}")
        """
        if vertex < 0 or vertex >= self.num_vertices:
            raise ValueError(f"Vertex {vertex} out of range [0, {self.num_vertices})")

        return int(self.indptr[vertex + 1] - self.indptr[vertex])

    def edge_weights(self, vertex: int) -> np.ndarray | None:
        """
        Get edge weights for incoming edges to a vertex.

        Args:
            vertex: Target vertex ID

        Returns:
            Array of edge weights, or None if no weights stored
        """
        if not self.has_weights:
            return None

        if vertex < 0 or vertex >= self.num_vertices:
            raise ValueError(f"Vertex {vertex} out of range [0, {self.num_vertices})")

        start = self.indptr[vertex]
        end = self.indptr[vertex + 1]
        return self.data[start:end].copy()

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"CSCAdjacency({self.num_vertices:,} vertices, {self.num_edges:,} edges"
            f"{', weighted' if self.has_weights else ''})"
        )
