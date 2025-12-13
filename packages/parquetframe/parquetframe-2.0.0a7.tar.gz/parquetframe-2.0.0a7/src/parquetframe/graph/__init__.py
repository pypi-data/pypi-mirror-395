"""
Graph processing functionality for ParquetFrame.

This module provides graph data processing capabilities, including:
- Apache GraphAr format support for large-scale graph data
- Graph data structures with vertex/edge property access
- CSR/CSC adjacency list representations for efficient traversal
- Integration with pandas/Dask backends for scalable processing

Examples:
    Basic graph loading:
        >>> import parquetframe as pf
        >>> graph = pf.graph.read_graph("my_social_network/")
        >>> print(graph.num_vertices, graph.num_edges)
        (1000000, 5000000)

    Graph property access:
        >>> users = graph.vertices  # Vertex properties as ParquetFrame
        >>> follows = graph.edges   # Edge properties as ParquetFrame
        >>> degree_out = graph.degree(vertex_id=123, mode="out")

    Graph traversal preparation:
        >>> adj_out = graph.out_adjacency  # CSR adjacency for outgoing edges
        >>> neighbors = adj_out.neighbors(vertex_id=123)
"""

from pathlib import Path
from typing import Any, Literal

from ..core_legacy import (
    ParquetFrame,  # Internal use only - avoids deprecation warnings
)
from .adjacency import CSCAdjacency, CSRAdjacency


class GraphFrame:
    """
    A graph data structure built on top of ParquetFrame.

    GraphFrame represents a graph with vertex and edge data stored in
    columnar format (Parquet), enabling scalable graph processing using
    pandas or Dask backends.

    The graph follows the Apache GraphAr specification for standardized
    graph data organization and metadata.

    Attributes:
        vertices: ParquetFrame containing vertex data and properties
        edges: ParquetFrame containing edge data and properties
        metadata: Dict containing graph metadata from GraphAr format
        num_vertices: Number of vertices in the graph
        num_edges: Number of edges in the graph

    Examples:
        Access graph components:
            >>> graph = read_graph("social_network/")
            >>> print(f"Graph has {graph.num_vertices} vertices, {graph.num_edges} edges")
            >>> users = graph.vertices  # Access vertex data
            >>> connections = graph.edges  # Access edge data

        Vertex/edge property queries:
            >>> active_users = graph.vertices.query("last_login > '2024-01-01'")
            >>> strong_ties = graph.edges.query("weight > 0.8")

        Degree calculations:
            >>> out_degree = graph.degree(vertex_id=123, mode="out")
            >>> in_degree = graph.degree(vertex_id=123, mode="in")
            >>> total_degree = graph.degree(vertex_id=123, mode="all")
    """

    def __init__(
        self,
        vertices: ParquetFrame,
        edges: ParquetFrame,
        metadata: dict[str, Any],
        adjacency_data: dict[str, Any] | None = None,
    ):
        """
        Initialize a GraphFrame.

        Args:
            vertices: ParquetFrame containing vertex data
            edges: ParquetFrame containing edge data
            metadata: Graph metadata dictionary from GraphAr format
            adjacency_data: Optional precomputed adjacency structures

        Note:
            This constructor is typically not called directly. Use read_graph()
            to load graphs from GraphAr directories.
        """
        self.vertices = vertices
        self.edges = edges
        self.metadata = metadata
        self._adjacency_data = adjacency_data or {}

        # Lazy-loaded adjacency structures
        self._csr_adjacency = None
        self._csc_adjacency = None

    @property
    def num_vertices(self) -> int:
        """Number of vertices in the graph."""
        return len(self.vertices)

    @property
    def num_edges(self) -> int:
        """Number of edges in the graph."""
        return len(self.edges)

    @property
    def is_directed(self) -> bool:
        """Whether the graph is directed."""
        return self.metadata.get("directed", True)

    @property
    def vertex_properties(self) -> list[str]:
        """List of vertex property column names."""
        return [col for col in self.vertices.columns if col not in ("vertex_id", "id")]

    @property
    def edge_properties(self) -> list[str]:
        """List of edge property column names."""
        return [
            col
            for col in self.edges.columns
            if col not in ("src", "dst", "source", "target")
        ]

    def degree(self, vertex_id: int, mode: Literal["in", "out", "all"] = "all") -> int:
        """
        Calculate vertex degree using efficient adjacency structures.

        Args:
            vertex_id: The vertex ID to calculate degree for
            mode: Type of degree ("in", "out", "all")

        Returns:
            Vertex degree count

        Examples:
            >>> graph.degree(123)  # Total degree
            15
            >>> graph.degree(123, mode="out")  # Outgoing edges only
            8
            >>> graph.degree(123, mode="in")   # Incoming edges only
            7
        """
        if mode == "out":
            csr = self._get_csr_adjacency()
            return csr.degree(vertex_id)
        elif mode == "in":
            csc = self._get_csc_adjacency()
            return csc.degree(vertex_id)
        else:  # mode == "all"
            out_degree = self.degree(vertex_id, mode="out")
            in_degree = self.degree(vertex_id, mode="in")
            return out_degree + in_degree

    def neighbors(
        self, vertex_id: int, mode: Literal["in", "out", "all"] = "out"
    ) -> list:
        """
        Get neighboring vertex IDs using efficient adjacency structures.

        Args:
            vertex_id: The vertex to find neighbors for
            mode: Direction to traverse ("in", "out", "all")

        Returns:
            List of neighboring vertex IDs

        Examples:
            >>> graph.neighbors(123)  # Outgoing neighbors
            [456, 789, 101112]
            >>> graph.neighbors(123, mode="in")  # Incoming neighbors
            [13, 14, 15]
        """
        if mode == "out":
            csr = self._get_csr_adjacency()
            return csr.neighbors(vertex_id).tolist()
        elif mode == "in":
            csc = self._get_csc_adjacency()
            return csc.predecessors(vertex_id).tolist()
        else:  # mode == "all"
            out_neighbors = set(self.neighbors(vertex_id, mode="out"))
            in_neighbors = set(self.neighbors(vertex_id, mode="in"))
            return list(out_neighbors | in_neighbors)

    def subgraph(self, vertex_ids: list[int]) -> "GraphFrame":
        """
        Extract a subgraph containing only the specified vertices.

        Args:
            vertex_ids: List of vertex IDs to include in subgraph

        Returns:
            New GraphFrame containing the subgraph

        Examples:
            >>> important_nodes = [1, 5, 10, 23, 45]
            >>> subgraph = graph.subgraph(important_nodes)
            >>> print(subgraph.num_vertices, subgraph.num_edges)
            (5, 12)
        """
        # Filter vertices
        vertex_mask = self.vertices["vertex_id"].isin(vertex_ids)
        filtered_vertices = self.vertices[vertex_mask]

        # Filter edges (only edges between selected vertices)
        edge_mask = self.edges["src"].isin(vertex_ids) & self.edges["dst"].isin(
            vertex_ids
        )
        filtered_edges = self.edges[edge_mask]

        # Create new GraphFrame with filtered data
        return GraphFrame(
            vertices=filtered_vertices,
            edges=filtered_edges,
            metadata={**self.metadata, "subgraph": True},
        )

    def __repr__(self) -> str:
        """String representation of the GraphFrame."""
        directed_str = "directed" if self.is_directed else "undirected"
        return (
            f"GraphFrame({self.num_vertices:,} vertices, {self.num_edges:,} edges, "
            f"{directed_str})"
        )

    def __str__(self) -> str:
        """User-friendly string representation."""
        return self.__repr__()

    def _get_csr_adjacency(self) -> CSRAdjacency:
        """
        Get or create CSR adjacency structure for outgoing edges.

        Returns:
            CSRAdjacency instance for this graph
        """
        if self._csr_adjacency is None:
            from .data import EdgeSet

            # Create EdgeSet from edges DataFrame
            edge_set = EdgeSet(
                data=self.edges, edge_type="default", properties={}, schema=None
            )
            self._csr_adjacency = CSRAdjacency.from_edge_set(
                edge_set, num_vertices=self.num_vertices
            )
        return self._csr_adjacency

    def _get_csc_adjacency(self) -> CSCAdjacency:
        """
        Get or create CSC adjacency structure for incoming edges.

        Returns:
            CSCAdjacency instance for this graph
        """
        if self._csc_adjacency is None:
            from .data import EdgeSet

            # Create EdgeSet from edges DataFrame
            edge_set = EdgeSet(
                data=self.edges, edge_type="default", properties={}, schema=None
            )
            self._csc_adjacency = CSCAdjacency.from_edge_set(
                edge_set, num_vertices=self.num_vertices
            )
        return self._csc_adjacency

    @property
    def csr_adjacency(self) -> CSRAdjacency:
        """
        CSR (Compressed Sparse Row) adjacency structure for outgoing edges.

        This property provides efficient neighbor lookups and out-degree calculations.
        The structure is built lazily on first access.

        Returns:
            CSRAdjacency instance

        Examples:
            >>> csr = graph.csr_adjacency
            >>> neighbors = csr.neighbors(vertex_id=123)
            >>> out_degree = csr.degree(vertex_id=123)
        """
        return self._get_csr_adjacency()

    @property
    def csc_adjacency(self) -> CSCAdjacency:
        """
        CSC (Compressed Sparse Column) adjacency structure for incoming edges.

        This property provides efficient predecessor lookups and in-degree calculations.
        The structure is built lazily on first access.

        Returns:
            CSCAdjacency instance

        Examples:
            >>> csc = graph.csc_adjacency
            >>> predecessors = csc.predecessors(vertex_id=123)
            >>> in_degree = csc.degree(vertex_id=123)
        """
        return self._get_csc_adjacency()

    def has_edge(self, source: int, target: int) -> bool:
        """
        Check if an edge exists between two vertices.

        Args:
            source: Source vertex ID
            target: Target vertex ID

        Returns:
            True if edge exists, False otherwise

        Examples:
            >>> if graph.has_edge(123, 456):
            ...     print("Edge 123 -> 456 exists")
        """
        csr = self._get_csr_adjacency()
        return csr.has_edge(source, target)

    # Algorithm Convenience Methods (Phase 3.5 Task 1.1)

    def pagerank(
        self,
        alpha: float = 0.85,
        tol: float = 1e-6,
        max_iter: int = 100,
        weight_column: str | None = None,
        personalized: dict[int, float] | None = None,
        backend: Literal["auto", "pandas", "dask", "rust"] = "auto",
    ):
        """
        Compute PageRank scores using power iteration method.

        PageRank measures vertex importance based on the graph's link structure.
        Uses Rust backend automatically when available for 5-20x speedup.

        Args:
            alpha: Damping factor (0.85 is Google's original value)
            tol: Convergence tolerance for L1 norm of score differences
            max_iter: Maximum number of iterations before forced termination
            weight_column: Name of edge weight column. If None, uses uniform weights
            personalized: Dict mapping vertex_id -> personalization weight
            backend: Backend selection ('auto', 'pandas', 'dask', 'rust')
                - 'auto': Prefer Rust if available, fallback to pandas/dask
                - 'rust': Force Rust backend (error if unavailable)
                - 'pandas': Force pandas backend
                - 'dask': Force Dask backend

        Returns:
            DataFrame with columns:
                - vertex (int64): Vertex ID
                - rank (float64): PageRank score (sums to 1.0)

        Examples:
            Basic PageRank:
                >>> ranks = graph.pagerank(alpha=0.85)
                >>> top_nodes = ranks.nlargest(10, 'rank')

            Personalized PageRank:
                >>> bias = {1: 0.5, 10: 0.5}  # Favor vertices 1 and 10
                >>> ranks = graph.pagerank(personalized=bias)

            Force Rust backend:
                >>> ranks = graph.pagerank(backend='rust')  # 10-20x faster
        """
        from .algo.pagerank import pagerank

        return pagerank(
            self,
            alpha=alpha,
            tol=tol,
            max_iter=max_iter,
            weight_column=weight_column,
            personalized=personalized,
            directed=None,  # Use graph.is_directed
            backend=backend,
        )

    def shortest_path(
        self,
        sources: int | list[int],
        weight_column: str | None = None,
        backend: Literal["auto", "pandas", "dask", "rust"] = "auto",
        include_unreachable: bool = True,
    ):
        """
        Find shortest paths from source vertices to all reachable vertices.

        For unweighted graphs (weight_column=None), uses BFS.
        For weighted graphs, uses Dijkstra's algorithm with Rust backend
        when available for 8-15x speedup.

        Args:
            sources: Starting vertex ID(s) for shortest path computation
            weight_column: Name of edge weight column. If None, treats as unweighted
            backend: Backend selection ('auto', 'pandas', 'dask', 'rust')
            include_unreachable: Whether to include unreachable vertices (inf distance)

        Returns:
            DataFrame with columns:
                - vertex (int64): Vertex ID
                - distance (float64): Shortest distance from nearest source
                - predecessor (int64): Previous vertex in shortest path

        Examples:
            Unweighted shortest paths:
                >>> paths = graph.shortest_path(sources=[1, 2])
                >>> reachable = paths[paths['distance'] < float('inf')]

            Weighted shortest paths:
                >>> paths = graph.shortest_path(sources=[1], weight_column='cost')
                >>> print(paths.nsmallest(10, 'distance'))

            Force Rust backend:
                >>> paths = graph.shortest_path(sources=[1], backend='rust')
        """
        from .algo.shortest_path import shortest_path

        return shortest_path(
            self,
            sources=sources,
            weight_column=weight_column,
            directed=None,  # Use graph.is_directed
            backend=backend,
            include_unreachable=include_unreachable,
        )

    def connected_components(
        self,
        method: Literal["weak", "strong"] = "weak",
        backend: Literal["auto", "pandas", "dask", "rust"] = "auto",
        max_iter: int = 50,
    ):
        """
        Find connected components in the graph.

        For directed graphs, computes weakly connected components (ignoring edge direction).
        Uses Rust backend automatically when available for 12-20x speedup.

        Args:
            method: Component type ('weak' for weakly connected)
            backend: Backend selection ('auto', 'pandas', 'dask', 'rust')
            max_iter: Maximum iterations for iterative algorithms

        Returns:
            DataFrame with columns:
                - vertex (int64): Vertex ID
                - component_id (int64): Connected component identifier

        Examples:
            Find components:
                >>> components = graph.connected_components()
                >>> sizes = components.groupby('component_id').size()
                >>> print(f"Found {len(sizes)} components")

            Force Rust backend:
                >>> components = graph.connected_components(backend='rust')
        """
        from .algo.components import connected_components

        return connected_components(
            self, method=method, directed=None, backend=backend, max_iter=max_iter
        )

    def bfs(
        self,
        sources: int | list[int],
        max_depth: int | None = None,
        backend: Literal["auto", "pandas", "rust"] = "auto",
    ):
        """
        Perform breadth-first search (BFS) traversal.

        BFS explores vertices level by level from source vertices.
        Uses Rust backend automatically when available for 5-10x speedup.

        Args:
            sources: Starting vertex ID(s) for BFS traversal
            max_depth: Maximum traversal depth (None for unlimited)
            backend: Backend selection ('auto', 'pandas', 'rust')

        Returns:
            DataFrame with columns:
                - vertex (int64): Vertex ID
                - distance (int64): Distance from nearest source
                - predecessor (int64): Previous vertex in BFS tree

        Examples:
            Single source BFS:
                >>> result = graph.bfs(sources=0)
                >>> print(result[result['distance'] <= 2])  # Within 2 hops

            Multi-source BFS:
                >>> result = graph.bfs(sources=[0, 10, 20])

            Force Rust backend:
                >>> result = graph.bfs(sources=0, backend='rust')
        """
        from .algo.traversal import bfs

        return bfs(
            self, sources=sources, max_depth=max_depth, directed=None, backend=backend
        )

    def dfs(
        self,
        source: int,
        max_depth: int | None = None,
        backend: Literal["auto", "pandas", "rust"] = "auto",
    ):
        """
        Perform depth-first search (DFS) traversal.

        DFS explores as far as possible along each branch before backtracking.
        Uses Rust backend automatically when available for 5-10x speedup.

        Args:
            source: Starting vertex ID for DFS traversal
            max_depth: Maximum traversal depth (None for unlimited)
            backend: Backend selection ('auto', 'pandas', 'rust')

        Returns:
            Array of vertex IDs visited in DFS order

        Examples:
            Basic DFS:
                >>> visited = graph.dfs(source=0)
                >>> print(f"Visited {len(visited)} vertices")

            Limited depth DFS:
                >>> visited = graph.dfs(source=0, max_depth=5)

            Force Rust backend:
                >>> visited = graph.dfs(source=0, backend='rust')
        """
        from .algo.traversal import dfs

        return dfs(
            self, source=source, max_depth=max_depth, directed=None, backend=backend
        )

    @classmethod
    def from_edges(
        cls,
        sources,  # Union[list[int], np.ndarray]
        targets,  # Union[list[int], np.ndarray]
        num_vertices: int | None = None,
        edge_weights=None,  # Union[list[float], np.ndarray, None]
        vertex_data=None,  # Union[pd.DataFrame, None]
        edge_data=None,  # Union[pd.DataFrame, None]
        directed: bool = True,
    ) -> "GraphFrame":
        """
        Create GraphFrame directly from edge lists.

        This is a convenience method for quickly creating graphs from arrays
        without needing to construct DataFrames manually.

        Args:
            sources: Source vertex IDs (array-like)
            targets: Target vertex IDs (array-like)
            num_vertices: Total number of vertices (inferred if None)
            edge_weights: Optional edge weights (same length as sources/targets)
            vertex_data: Optional vertex properties DataFrame
            edge_data: Optional edge properties DataFrame (must include src/dst columns)
            directed: Whether graph is directed (default True)

        Returns:
            GraphFrame instance

        Examples:
            Simple graph from arrays:
                >>> sources = [0, 1, 2]
                >>> targets = [1, 2, 0]
                >>> graph = GraphFrame.from_edges(sources, targets)
                >>> print(graph)
                GraphFrame(3 vertices, 3 edges, directed)

            Weighted graph:
                >>> sources = [0, 1, 2]
                >>> targets = [1, 2, 0]
                >>> weights = [1.5, 2.0, 1.0]
                >>> graph = GraphFrame.from_edges(sources, targets, edge_weights=weights)

            With vertex properties:
                >>> import pandas as pd
                >>> sources = [0, 1]
                >>> targets = [1, 0]
                >>> vertex_props = pd.DataFrame({
                ...     'vertex_id': [0, 1],
                ...     'name': ['Alice', 'Bob']
                ... })
                >>> graph = GraphFrame.from_edges(sources, targets, vertex_data=vertex_props)
        """
        import numpy as np
        import pandas as pd

        # Convert to numpy arrays
        sources_arr = np.asarray(sources, dtype=np.int64)
        targets_arr = np.asarray(targets, dtype=np.int64)

        if len(sources_arr) != len(targets_arr):
            raise ValueError(
                f"sources and targets must have same length: "
                f"{len(sources_arr)} != {len(targets_arr)}"
            )

        # Determine number of vertices
        if num_vertices is None:
            if len(sources_arr) == 0:
                num_vertices = 0
            else:
                num_vertices = max(sources_arr.max(), targets_arr.max()) + 1

        # Build edges DataFrame
        if edge_data is not None:
            # Use provided edge data (must include src/dst columns)
            if "src" not in edge_data.columns or "dst" not in edge_data.columns:
                raise ValueError("edge_data must include 'src' and 'dst' columns")
            edges_df = edge_data.copy()
        else:
            edges_df = pd.DataFrame({"src": sources_arr, "dst": targets_arr})
            if edge_weights is not None:
                weights_arr = np.asarray(edge_weights, dtype=np.float64)
                if len(weights_arr) != len(sources_arr):
                    raise ValueError(
                        f"edge_weights length {len(weights_arr)} != "
                        f"sources length {len(sources_arr)}"
                    )
                edges_df["weight"] = weights_arr

        # Build vertices DataFrame
        if vertex_data is not None:
            if "vertex_id" not in vertex_data.columns:
                raise ValueError("vertex_data must include 'vertex_id' column")
            vertices_df = vertex_data.copy()
        else:
            vertices_df = pd.DataFrame({"vertex_id": range(num_vertices)})

        # Create metadata
        metadata = {"directed": directed, "created_from": "from_edges"}

        # Wrap with ParquetFrame for consistency
        vertices_pf = ParquetFrame(vertices_df)
        edges_pf = ParquetFrame(edges_df)

        return cls(vertices=vertices_pf, edges=edges_pf, metadata=metadata)


def read_graph(
    path: str | Path,
    *,
    threshold_mb: float | None = None,
    islazy: bool | None = None,
    validate_schema: bool = True,
    load_adjacency: bool = False,
) -> GraphFrame:
    """
    Read a graph from GraphAr format directory.

    GraphAr is a columnar format for graph data that organizes vertices
    and edges in Parquet files with standardized metadata and schema files.

    Args:
        path: Path to GraphAr directory containing graph data
        threshold_mb: Size threshold in MB for pandas/Dask backend selection
        islazy: Force backend selection (True=Dask, False=pandas, None=auto)
        validate_schema: Whether to validate GraphAr schema compliance
        load_adjacency: Whether to preload adjacency structures for fast traversal

    Returns:
        GraphFrame object containing the loaded graph

    Raises:
        FileNotFoundError: If GraphAr directory or required files are missing
        ValueError: If GraphAr schema validation fails
        ImportError: If required dependencies for format are missing

    Examples:
        Basic usage:
            >>> graph = read_graph("my_social_network/")
            >>> print(f"Loaded {graph.num_vertices} vertices, {graph.num_edges} edges")

        Force Dask backend for large graphs:
            >>> large_graph = read_graph("web_graph/", islazy=True)
            >>> print(f"Using Dask: {large_graph.vertices.islazy}")
            True

        Skip schema validation for performance:
            >>> graph = read_graph("trusted_graph/", validate_schema=False)

        Preload adjacency for traversal algorithms:
            >>> graph = read_graph("social_net/", load_adjacency=True)
            >>> neighbors = graph.neighbors(vertex_id=123)  # Fast lookup
    """
    # This is a placeholder - actual implementation will be in the GraphArReader
    from .io.graphar import GraphArReader

    reader = GraphArReader()
    return reader.read(
        path=path,
        threshold_mb=threshold_mb,
        islazy=islazy,
        validate_schema=validate_schema,
        load_adjacency=load_adjacency,
    )


__all__ = [
    # Core classes
    "GraphFrame",
    "read_graph",
    # Adjacency structures
    "CSRAdjacency",
    "CSCAdjacency",
]
