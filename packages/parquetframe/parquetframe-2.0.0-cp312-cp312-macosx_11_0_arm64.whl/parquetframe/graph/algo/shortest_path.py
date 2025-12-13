"""
Shortest path algorithms for weighted and unweighted graphs.

This module implements shortest path algorithms including BFS for unweighted
graphs and Dijkstra's algorithm for weighted graphs with non-negative weights.
"""

import heapq
from typing import Any, Literal

import numpy as np
import pandas as pd

# Import Rust backend for accelerated Dijkstra shortest path computation
from ..rust_backend import dijkstra_rust, is_rust_available


def shortest_path(
    graph: Any,  # GraphFrame type hint will be added after implementation
    sources: int | list[int],
    weight_column: str | None = None,
    directed: bool | None = None,
    backend: Literal["auto", "pandas", "dask", "rust"] | None = "auto",
    include_unreachable: bool = True,
) -> pd.DataFrame:
    """
    Find shortest paths from source vertices to all reachable vertices.

    For unweighted graphs (weight_column=None), uses BFS for optimal performance.
    For weighted graphs, uses Dijkstra's algorithm with non-negative weights.

    Args:
        graph: GraphFrame object containing the graph data
        sources: Starting vertex ID(s) for shortest path computation
        weight_column: Name of edge weight column. If None, treats as unweighted (uniform weight 1)
        directed: Whether to treat graph as directed. If None, uses graph.is_directed
        backend: Backend selection ('auto', 'pandas', 'dask', 'rust')
            - 'auto': Prefer Rust if available, fallback to pandas/dask
            - 'rust': Force Rust backend (error if unavailable, weighted graphs only)
            - 'pandas': Force pandas backend
            - 'dask': Force Dask backend
        include_unreachable: Whether to include unreachable vertices with infinite distance

    Returns:
        DataFrame with columns:
            - vertex (int64): Vertex ID
            - distance (float64): Shortest distance from nearest source (inf for unreachable)
            - predecessor (int64): Previous vertex in shortest path (nullable)

    Raises:
        ValueError: If sources contain invalid vertex IDs, weight_column not found,
                   or negative weights detected (Dijkstra)
        NotImplementedError: If Dask backend requested for weighted shortest paths

    Examples:
        Unweighted shortest paths:
            >>> paths = shortest_path(graph, sources=[1, 2])
            >>> reachable = paths[paths['distance'] < float('inf')]

        Weighted shortest paths:
            >>> paths = shortest_path(graph, sources=[1], weight_column='cost')
            >>> print(paths.nsmallest(10, 'distance'))
    """
    # 1. Validate inputs
    if graph.num_vertices == 0:
        raise ValueError("Cannot compute shortest paths on empty graph")

    # Normalize sources to list
    if isinstance(sources, int):
        sources = [sources]
    else:
        sources = list(sources)

    if not sources:
        raise ValueError("At least one source vertex must be specified")

    # Validate source vertices exist
    for src in sources:
        if src < 0 or src >= graph.num_vertices:
            raise ValueError(
                f"Source vertex {src} out of range [0, {graph.num_vertices})"
            )

    # Handle directed parameter
    if directed is None:
        directed = graph.is_directed

    # 2. Choose algorithm based on whether weights are provided
    if weight_column is None:
        # Unweighted graph - use BFS
        return bfs_shortest_path(graph, sources, directed, include_unreachable)
    else:
        # Weighted graph - use Dijkstra's algorithm
        if backend == "dask":
            raise NotImplementedError(
                "Dask backend for weighted shortest paths not yet implemented. "
                "Use backend='pandas' for Dijkstra's algorithm."
            )
        return dijkstra(
            graph, sources, weight_column, directed, include_unreachable, backend
        )


def dijkstra(
    graph: Any,  # GraphFrame type hint will be added after implementation
    sources: int | list[int],
    weight_column: str,
    directed: bool | None = None,
    include_unreachable: bool = True,
    backend: Literal["auto", "pandas", "rust"] | None = "auto",
) -> pd.DataFrame:
    """
    Dijkstra's algorithm for single/multi-source shortest paths with non-negative weights.

    This is a specialized implementation of Dijkstra's algorithm optimized for
    pandas backend processing with CSRAdjacency neighbor lookups.

    Args:
        graph: GraphFrame object containing the graph data
        sources: Starting vertex ID(s)
        weight_column: Name of edge weight column (must exist and be numeric)
        directed: Whether to treat graph as directed. If None, uses graph.is_directed
        include_unreachable: Whether to include unreachable vertices
        backend: Backend selection ('auto', 'pandas', 'rust')
            - 'auto': Prefer Rust if available, fallback to pandas
            - 'rust': Force Rust backend (error if unavailable)
            - 'pandas': Force pandas backend

    Returns:
        DataFrame with shortest path results

    Raises:
        ValueError: If weight_column contains negative weights

    Examples:
        Single source Dijkstra:
            >>> result = dijkstra(graph, sources=1, weight_column='weight')
            >>> print(result.nsmallest(5, 'distance'))
    """
    # 0. Check if Rust backend is explicitly requested or preferred
    if backend == "rust":
        # Explicitly requested Rust backend - error if unavailable
        if not is_rust_available():
            raise RuntimeError(
                "Rust backend requested but not available. "
                "Install with: pip install parquetframe (Rust-enabled wheels)"
            )
        return dijkstra_rust_wrapper(
            graph, sources, weight_column, directed, include_unreachable
        )
    elif backend == "auto" and is_rust_available():
        # Auto selection: prefer Rust for best performance
        try:
            return dijkstra_rust_wrapper(
                graph, sources, weight_column, directed, include_unreachable
            )
        except ValueError as e:
            # Re-raise validation errors (user input errors)
            error_msg = str(e)
            if "not found" in error_msg or "negative" in error_msg:
                raise
            # Fall back for other ValueError types
            import warnings

            warnings.warn(
                f"Rust backend failed ({type(e).__name__}), falling back to Python: {e}",
                RuntimeWarning,
                stacklevel=2,
            )
        except (IndexError, RuntimeError) as e:
            # Fallback to pandas for runtime errors
            import warnings

            warnings.warn(
                f"Rust backend failed ({type(e).__name__}), falling back to Python: {e}",
                RuntimeWarning,
                stacklevel=2,
            )

    # Continue with pandas implementation
    return dijkstra_pandas(graph, sources, weight_column, directed, include_unreachable)


def dijkstra_rust_wrapper(
    graph: Any,  # GraphFrame type hint will be added after implementation
    sources: int | list[int],
    weight_column: str,
    directed: bool | None = None,
    include_unreachable: bool = True,
) -> pd.DataFrame:
    """
    Dijkstra's algorithm using Rust backend for maximum performance.

    This wrapper function interfaces with the Rust implementation,
    providing 5-20x speedup over pure Python implementations.

    Args:
        graph: GraphFrame object
        sources: Starting vertex ID(s)
        weight_column: Name of edge weight column (must exist and be numeric)
        directed: Whether to treat graph as directed
        include_unreachable: Whether to include unreachable vertices

    Returns:
        DataFrame with shortest path results

    Raises:
        RuntimeError: If Rust backend is not available
        ValueError: If weight_column contains negative weights

    Examples:
        Force Rust backend:
            >>> result = dijkstra_rust_wrapper(graph, sources=[1], weight_column='weight')
    """
    # 1. Validate weight_column exists and contains non-negative numeric values
    if weight_column not in graph.edges.columns:
        raise ValueError(f"Weight column '{weight_column}' not found in graph edges")

    # Handle directed parameter
    if directed is None:
        directed = graph.is_directed

    # 2. Get CSR adjacency and edge data
    if directed:
        adj = graph.csr_adjacency  # Use CSR for directed graphs
    else:
        # For undirected graphs, Rust expects CSR built from both directions
        # The CSR should already include reverse edges for undirected graphs
        adj = graph.csr_adjacency

    # Defensive check: ensure CSR indptr has correct size
    if len(adj.indptr) != graph.num_vertices + 1:
        raise ValueError(
            f"CSR indptr size mismatch: expected {graph.num_vertices + 1}, "
            f"got {len(adj.indptr)}. This indicates a graph construction issue."
        )

    # 3. Get edge weights in CSR order
    edges_df = graph.edges
    if hasattr(edges_df, "pandas_df"):
        edges_df = edges_df.pandas_df
    elif hasattr(edges_df, "compute"):
        edges_df = edges_df.compute()

    # Get column names
    from ..data import EdgeSet

    edge_set = EdgeSet(
        data=graph.edges, edge_type="default", properties={}, schema=None
    )
    src_col = edge_set.src_column or "src"
    dst_col = edge_set.dst_column or "dst"

    # Create edge weight array aligned with CSR structure
    # Rust expects weights in the same order as indices in CSR
    edge_weights_list = []
    for src_vertex in range(graph.num_vertices):
        start_idx = adj.indptr[src_vertex]
        end_idx = adj.indptr[src_vertex + 1]
        neighbors = adj.indices[start_idx:end_idx]

        for neighbor in neighbors:
            # Find weight for this edge
            edge_row = edges_df[
                (edges_df[src_col] == src_vertex) & (edges_df[dst_col] == neighbor)
            ]
            if len(edge_row) > 0:
                weight = edge_row[weight_column].iloc[0]
                edge_weights_list.append(weight)
            else:
                # Should not happen with valid CSR, but handle gracefully
                edge_weights_list.append(1.0)

    edge_weights = np.array(edge_weights_list, dtype=np.float64)

    # Check for negative weights (only if there are edges)
    if len(edge_weights) > 0 and edge_weights.min() < 0:
        raise ValueError("Dijkstra's algorithm requires non-negative edge weights")

    # 4. Normalize sources to array
    if isinstance(sources, int):
        sources_array = np.array([sources], dtype=np.int32)
    else:
        sources_array = np.array(sources, dtype=np.int32)

    # 5. Call Rust Dijkstra function
    # Rust expects: (indptr, indices, num_vertices, sources, weights)
    num_vertices = graph.num_vertices
    distances, predecessors = dijkstra_rust(
        indptr=adj.indptr,
        indices=adj.indices,
        num_vertices=num_vertices,
        sources=sources_array,
        weights=edge_weights,
    )

    # 6. Create result DataFrame
    result_data = {"vertex": [], "distance": [], "predecessor": []}

    for vertex in range(num_vertices):
        vertex_distance = distances[vertex]

        # Include vertex if:
        # - It was reached (distance != inf), OR
        # - include_unreachable is True
        if vertex_distance != np.inf or include_unreachable:
            result_data["vertex"].append(vertex)
            result_data["distance"].append(vertex_distance)
            result_data["predecessor"].append(
                int(predecessors[vertex]) if predecessors[vertex] != -1 else None
            )

    # Create DataFrame with proper dtypes
    result_df = pd.DataFrame(result_data)
    if not result_df.empty:
        result_df["vertex"] = result_df["vertex"].astype("int64")
        result_df["distance"] = result_df["distance"].astype("float64")
        result_df["predecessor"] = result_df["predecessor"].astype(
            "Int64"
        )  # Nullable int
    else:
        # Handle empty result case
        result_df = pd.DataFrame(
            {
                "vertex": pd.Series([], dtype="int64"),
                "distance": pd.Series([], dtype="float64"),
                "predecessor": pd.Series([], dtype="Int64"),
            }
        )

    return result_df


def dijkstra_pandas(
    graph: Any,  # GraphFrame type hint will be added after implementation
    sources: int | list[int],
    weight_column: str,
    directed: bool | None = None,
    include_unreachable: bool = True,
) -> pd.DataFrame:
    """
    Dijkstra's algorithm using pandas backend (legacy implementation).

    Efficient implementation for pandas backend processing with
    CSRAdjacency neighbor lookups.

    Args:
        graph: GraphFrame object
        sources: Starting vertex ID(s)
        weight_column: Name of edge weight column
        directed: Whether to treat graph as directed
        include_unreachable: Whether to include unreachable vertices

    Returns:
        DataFrame with shortest path results
    """
    # 1. Validate weight_column exists and contains non-negative numeric values
    if weight_column not in graph.edges.columns:
        raise ValueError(f"Weight column '{weight_column}' not found in graph edges")

    # Get edge weights and check for negative values
    edge_weights = graph.edges[weight_column]
    if hasattr(edge_weights, "pandas_df"):
        edge_weights = edge_weights.pandas_df  # Handle ParquetFrame
    elif hasattr(edge_weights, "compute"):
        edge_weights = edge_weights.compute()  # Handle Dask

    if edge_weights.min() < 0:
        raise ValueError("Dijkstra's algorithm requires non-negative edge weights")

    # Normalize sources to list
    if isinstance(sources, int):
        sources = [sources]
    else:
        sources = list(sources)

    # Handle directed parameter
    if directed is None:
        directed = graph.is_directed

    # 2. Get adjacency structures and edge data for efficient lookups
    if directed:
        adj = graph.csr_adjacency  # Outgoing edges only
    else:
        # For undirected graphs, we need both directions
        adj = graph.csr_adjacency
        adj_reverse = graph.csc_adjacency

    # Get edge data for weight lookups
    edges_df = graph.edges
    if hasattr(edges_df, "pandas_df"):
        edges_df = edges_df.pandas_df
    elif hasattr(edges_df, "compute"):
        edges_df = edges_df.compute()

    # Create edge weight lookup dictionary for efficient access
    # Format: {(src, dst): weight}
    from ..data import EdgeSet

    edge_set = EdgeSet(
        data=graph.edges, edge_type="default", properties={}, schema=None
    )
    src_col = edge_set.src_column or "src"
    dst_col = edge_set.dst_column or "dst"

    edge_weights_dict = {}
    for _, row in edges_df.iterrows():
        src, dst, weight = row[src_col], row[dst_col], row[weight_column]
        edge_weights_dict[(src, dst)] = weight
        if not directed:
            # Add reverse edge for undirected graphs
            edge_weights_dict[(dst, src)] = weight

    # 3. Initialize Dijkstra's data structures
    num_vertices = graph.num_vertices
    distances = np.full(num_vertices, np.inf, dtype=np.float64)
    predecessors = np.full(num_vertices, -1, dtype=np.int64)
    visited = np.full(num_vertices, False, dtype=bool)

    # Priority queue: (distance, vertex)
    pq = []

    # Initialize sources
    for src in sources:
        distances[src] = 0.0
        predecessors[src] = -1  # Sources have no predecessor
        heapq.heappush(pq, (0.0, src))

    # 4. Main Dijkstra loop
    while pq:
        current_dist, current_vertex = heapq.heappop(pq)

        # Skip if we've already processed this vertex with a better distance
        if visited[current_vertex] or current_dist > distances[current_vertex]:
            continue

        visited[current_vertex] = True

        # Get neighbors based on graph directionality
        if directed:
            neighbors = adj.neighbors(current_vertex)
        else:
            # For undirected graphs, get both outgoing and incoming neighbors
            out_neighbors = adj.neighbors(current_vertex)
            if current_vertex < adj_reverse.num_vertices:
                in_neighbors = adj_reverse.predecessors(current_vertex)
                neighbors = np.unique(np.concatenate([out_neighbors, in_neighbors]))
            else:
                neighbors = out_neighbors

        # Relax edges to neighbors
        for neighbor in neighbors:
            if visited[neighbor]:
                continue

            # Get edge weight
            edge_weight = edge_weights_dict.get((current_vertex, neighbor))
            if edge_weight is None:
                continue  # Skip if edge weight not found

            new_distance = distances[current_vertex] + edge_weight

            # Relaxation step
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current_vertex
                heapq.heappush(pq, (new_distance, neighbor))

    # 5. Create result DataFrame
    result_data = {"vertex": [], "distance": [], "predecessor": []}

    for vertex in range(num_vertices):
        vertex_distance = distances[vertex]

        # Include vertex if:
        # - It was reached (distance != inf), OR
        # - include_unreachable is True
        if vertex_distance != np.inf or include_unreachable:
            result_data["vertex"].append(vertex)
            result_data["distance"].append(vertex_distance)
            result_data["predecessor"].append(
                predecessors[vertex] if predecessors[vertex] != -1 else None
            )

    # Create DataFrame with proper dtypes
    result_df = pd.DataFrame(result_data)
    if not result_df.empty:
        result_df["vertex"] = result_df["vertex"].astype("int64")
        result_df["distance"] = result_df["distance"].astype("float64")
        result_df["predecessor"] = result_df["predecessor"].astype(
            "Int64"
        )  # Nullable int
    else:
        # Handle empty result case
        result_df = pd.DataFrame(
            {
                "vertex": pd.Series([], dtype="int64"),
                "distance": pd.Series([], dtype="float64"),
                "predecessor": pd.Series([], dtype="Int64"),
            }
        )

    return result_df


def bfs_shortest_path(
    graph: Any,  # GraphFrame type hint will be added after implementation
    sources: int | list[int],
    directed: bool | None = None,
    include_unreachable: bool = True,
) -> pd.DataFrame:
    """
    BFS-based shortest paths for unweighted graphs (all edge weights = 1).

    Optimized implementation that delegates to the main BFS algorithm
    but returns results in shortest_path format for consistency.

    Args:
        graph: GraphFrame object containing the graph data
        sources: Starting vertex ID(s)
        directed: Whether to treat graph as directed
        include_unreachable: Whether to include unreachable vertices

    Returns:
        DataFrame with shortest path results (distance as float64 for consistency)

    Examples:
        Multi-source unweighted shortest paths:
            >>> result = bfs_shortest_path(graph, sources=[1, 10, 100])
            >>> print(result[result['distance'] <= 3])
    """
    # 1. Delegate to main BFS function
    from .traversal import bfs

    # Call BFS with include_unreachable to get consistent behavior
    bfs_result = bfs(
        graph=graph,
        sources=sources,
        directed=directed,
        include_unreachable=include_unreachable,
        backend="pandas",  # Always use pandas for consistency with Dijkstra
    )

    # 2. Convert BFS result to shortest_path format
    result_df = bfs_result[["vertex", "distance", "predecessor"]].copy()

    # Convert distance from int64 to float64 for consistency with Dijkstra
    result_df["distance"] = result_df["distance"].astype("float64")

    # Handle unreachable vertices (BFS uses -1 for unreachable, we want inf)
    if include_unreachable:
        result_df.loc[result_df["distance"] == -1.0, "distance"] = np.inf
    else:
        # Filter out unreachable vertices (those with distance -1)
        result_df = result_df[result_df["distance"] != -1.0]

    return result_df
