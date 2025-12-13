"""
Graph traversal algorithms: Breadth-First Search (BFS) and Depth-First Search (DFS).

This module implements core graph traversal algorithms with support for both
pandas and Dask backends, multi-source traversal, and flexible output formats.
"""

from collections import deque
from typing import Any, Literal, Union

import numpy as np
import pandas as pd

try:
    import dask.dataframe as dd

    DASK_AVAILABLE = True
except ImportError:
    DASK_AVAILABLE = False


def bfs(
    graph: Any,  # GraphFrame type hint will be added after implementation
    sources: int | list[int] | None = None,
    max_depth: int | None = None,
    directed: bool | None = None,
    backend: Literal["auto", "pandas", "dask"] | None = "auto",
    include_unreachable: bool = False,
    # Dask-specific parameters
    partition_size: int | None = None,
    npartitions: int | None = None,
    compute: bool = True,
) -> Union[pd.DataFrame, "dd.DataFrame"]:
    """
    Perform Breadth-First Search (BFS) traversal of a graph.

    BFS explores vertices in order of their distance from the source(s),
    visiting all vertices at distance k before any vertices at distance k+1.

    Args:
        graph: GraphFrame object containing the graph data
        sources: Starting vertex ID(s). If None, uses vertex 0 or first available vertex
        max_depth: Maximum depth to traverse. If None, explores entire reachable component
        directed: Whether to treat graph as directed. If None, uses graph.is_directed
        backend: Backend selection ('auto', 'pandas', 'dask')
        include_unreachable: Whether to include unreachable vertices with infinite distance
        partition_size: Target partition size in MB for Dask operations (Dask only)
        npartitions: Number of partitions for Dask DataFrames (Dask only)
        compute: Whether to compute result immediately or return lazy DataFrame (Dask only)

    Returns:
        DataFrame with columns:
            - vertex (int64): Vertex ID
            - distance (int64): Distance from nearest source vertex
            - predecessor (int64): Previous vertex in BFS tree (nullable)
            - layer (int64): BFS layer/level (same as distance)

        For Dask backend: returns computed pandas DataFrame if compute=True,
        otherwise returns lazy Dask DataFrame for further operations.

    Raises:
        ValueError: If sources contain invalid vertex IDs or graph is empty
        NotImplementedError: If Dask backend is requested but not available

    Examples:
        Single source BFS:
            >>> result = bfs(graph, sources=1, max_depth=3)
            >>> print(result[result['distance'] <= 2])

        Multi-source BFS:
            >>> result = bfs(graph, sources=[1, 5, 10])
            >>> print(result.groupby('distance').size())
    """
    # 1. Validate inputs
    if graph.num_vertices == 0:
        raise ValueError("Cannot perform BFS on empty graph")

    # Normalize sources to list
    if sources is None:
        # Default to vertex 0 if it exists, otherwise first available vertex
        sources = [0] if graph.num_vertices > 0 else []
    elif isinstance(sources, int):
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

    # Validate parameters
    if max_depth is not None and max_depth < 0:
        raise ValueError("max_depth must be non-negative")

    # Handle directed parameter
    if directed is None:
        directed = graph.is_directed

    # Select backend implementation
    if backend == "dask" or (
        backend == "auto" and hasattr(graph.edges, "islazy") and graph.edges.islazy
    ):
        if not DASK_AVAILABLE:
            raise ImportError(
                "Dask is required for distributed BFS but is not installed. "
                "Install with: pip install dask[complete]"
            )
        return _bfs_dask(
            graph,
            sources,
            max_depth,
            directed,
            include_unreachable,
            partition_size,
            npartitions,
            compute,
        )

    # 2. Get adjacency structure for efficient neighbor lookups
    if directed:
        adj = graph.csr_adjacency  # Outgoing edges only
    else:
        # For undirected graphs, we need both directions
        # Use CSR but will need to check both directions
        adj = graph.csr_adjacency
        adj_reverse = graph.csc_adjacency  # For incoming edges

    # 3. Initialize BFS data structures
    num_vertices = graph.num_vertices
    distance = np.full(num_vertices, -1, dtype=np.int64)  # -1 = unvisited
    predecessor = np.full(num_vertices, -1, dtype=np.int64)  # -1 = no predecessor

    # Initialize queue with source vertices
    queue = deque()
    for src in sources:
        distance[src] = 0
        predecessor[src] = -1  # Sources have no predecessor
        queue.append(src)

    # 4. Main BFS loop
    current_depth = 0
    while queue:
        # Process all vertices at current depth level
        level_size = len(queue)

        # Check depth limit
        if max_depth is not None and current_depth >= max_depth:
            break

        for _ in range(level_size):
            current = queue.popleft()
            current_dist = distance[current]

            # Get neighbors based on graph directionality
            if directed:
                neighbors = adj.neighbors(current)
            else:
                # For undirected graphs, get both outgoing and incoming neighbors
                out_neighbors = adj.neighbors(current)
                in_neighbors = adj_reverse.predecessors(current)
                neighbors = np.unique(np.concatenate([out_neighbors, in_neighbors]))

            # Visit unvisited neighbors
            for neighbor in neighbors:
                if distance[neighbor] == -1:  # Unvisited
                    distance[neighbor] = current_dist + 1
                    predecessor[neighbor] = current
                    queue.append(neighbor)

        current_depth += 1

    # 5. Create result DataFrame
    result_data = {"vertex": [], "distance": [], "predecessor": [], "layer": []}

    for vertex in range(num_vertices):
        vertex_distance = distance[vertex]

        # Include vertex if:
        # - It was visited (distance != -1), OR
        # - include_unreachable is True
        if vertex_distance != -1 or include_unreachable:
            result_data["vertex"].append(vertex)

            # For unreachable vertices, use a large sentinel value instead of infinity
            if vertex_distance != -1:
                result_data["distance"].append(vertex_distance)
                result_data["layer"].append(vertex_distance)
            else:
                # Use -1 to indicate unreachable (will be handled in result processing)
                result_data["distance"].append(-1)
                result_data["layer"].append(-1)

            result_data["predecessor"].append(
                predecessor[vertex] if predecessor[vertex] != -1 else None
            )

    # Create DataFrame with proper dtypes
    result_df = pd.DataFrame(result_data)
    if not result_df.empty:
        result_df["vertex"] = result_df["vertex"].astype("int64")
        result_df["distance"] = result_df["distance"].astype("int64")
        result_df["predecessor"] = result_df["predecessor"].astype(
            "Int64"
        )  # Nullable int
        result_df["layer"] = result_df["layer"].astype("int64")
    else:
        # Handle empty result case
        result_df = pd.DataFrame(
            {
                "vertex": pd.Series([], dtype="int64"),
                "distance": pd.Series([], dtype="int64"),
                "predecessor": pd.Series([], dtype="Int64"),
                "layer": pd.Series([], dtype="int64"),
            }
        )

    return result_df


def _bfs_dask(
    graph: Any,
    sources: list[int],
    max_depth: int | None,
    directed: bool,
    include_unreachable: bool,
    partition_size: int | None = None,
    npartitions: int | None = None,
    compute: bool = True,
) -> pd.DataFrame | dd.DataFrame:
    """
    Dask-optimized BFS using level-synchronous frontier expansion.

    This implementation uses a frontier-based approach where each level of the
    BFS is computed in parallel using Dask DataFrames. The algorithm maintains
    a frontier of vertices at the current distance and expands it by joining
    with the edges DataFrame.

    Args:
        graph: GraphFrame object containing the graph data
        sources: List of source vertex IDs
        max_depth: Maximum depth to traverse
        directed: Whether to treat graph as directed
        include_unreachable: Whether to include unreachable vertices
        partition_size: Target partition size for Dask operations
        npartitions: Number of partitions for Dask DataFrames
        compute: Whether to compute result or return lazy Dask DataFrame

    Returns:
        DataFrame with BFS results (computed or lazy based on compute parameter)
    """
    # Get edge data as Dask DataFrame
    edges_df = graph.edges
    if not hasattr(edges_df, "islazy") or not edges_df.islazy:
        # Convert ParquetFrame to pandas DataFrame, then to Dask
        if hasattr(edges_df, "pandas_df"):
            # ParquetFrame object - get the underlying pandas DataFrame
            pandas_edges = edges_df.pandas_df
        else:
            # Already a pandas DataFrame
            pandas_edges = edges_df

        edges_df = dd.from_pandas(pandas_edges, npartitions=npartitions or 4)
    else:
        # Already a Dask DataFrame
        pass

    # Determine source and destination column names
    from ..data import EdgeSet

    edge_set = EdgeSet(
        data=graph.edges, edge_type="default", properties={}, schema=None
    )
    src_col = edge_set.src_column or "src"
    dst_col = edge_set.dst_column or "dst"

    # Create edges for undirected graphs (add reverse edges)
    if not directed:
        # Add reverse edges for undirected traversal
        reverse_edges = edges_df.rename(columns={src_col: dst_col, dst_col: src_col})
        edges_df = dd.concat([edges_df, reverse_edges], ignore_index=True)

    # Repartition edges for optimal join performance
    if partition_size is not None:
        edges_df = edges_df.repartition(partition_size=f"{partition_size}MB")
    elif npartitions is not None:
        edges_df = edges_df.repartition(npartitions=npartitions)

    # Initialize frontier with source vertices
    frontier_data = {
        "vertex": sources,
        "distance": [0] * len(sources),
        "predecessor": [None] * len(sources),
        "layer": [0] * len(sources),
    }
    frontier = dd.from_pandas(pd.DataFrame(frontier_data), npartitions=1)

    # Initialize visited tracking
    visited = dd.from_pandas(
        pd.DataFrame({"vertex": sources, "visited": [True] * len(sources)}),
        npartitions=1,
    )

    # Store results from each level
    results = [frontier]

    current_depth = 0

    # Level-synchronous BFS loop
    while True:
        # Check depth limit
        if max_depth is not None and current_depth >= max_depth:
            break

        # Check if frontier is empty
        frontier_size = len(frontier)
        if hasattr(frontier_size, "compute"):
            frontier_size = frontier_size.compute()
        if frontier_size == 0:
            break

        # Expand frontier by joining with edges
        # Join frontier vertices with outgoing edges
        next_frontier = edges_df.merge(
            frontier[["vertex", "distance"]].rename(columns={"vertex": src_col}),
            on=src_col,
            how="inner",
        )

        # Select destination vertices and update distance
        next_frontier = next_frontier[[dst_col, "distance", src_col]].rename(
            columns={dst_col: "vertex", src_col: "predecessor"}
        )
        next_frontier["distance"] = next_frontier["distance"] + 1
        next_frontier["layer"] = next_frontier["distance"]

        # Remove already visited vertices
        next_frontier = next_frontier.merge(visited, on="vertex", how="left")
        next_frontier = next_frontier[next_frontier["visited"].isna()]
        next_frontier = next_frontier.drop("visited", axis=1)

        # Check if we have new vertices to explore
        next_frontier_size = len(next_frontier)
        if hasattr(next_frontier_size, "compute"):
            next_frontier_size = next_frontier_size.compute()
        if next_frontier_size == 0:
            break

        # For vertices reached from multiple sources in the same level,
        # keep only the first occurrence (arbitrary but deterministic)
        next_frontier = next_frontier.drop_duplicates(subset=["vertex"], keep="first")

        # Update visited set
        new_visited = next_frontier[["vertex"]].copy()
        new_visited["visited"] = True
        visited = dd.concat([visited, new_visited], ignore_index=True)

        # Add to results
        results.append(next_frontier)

        # Update frontier for next iteration
        frontier = next_frontier
        current_depth += 1

        # Safety check to prevent infinite loops
        if current_depth > 1000:  # Reasonable limit for most graphs
            break

    # Combine all results
    if len(results) > 1:
        result_df = dd.concat(results, ignore_index=True)
    else:
        result_df = results[0]

    # Handle unreachable vertices if requested
    if include_unreachable:
        # This is complex in Dask and may require computing the result first
        # For now, we'll note this limitation
        pass  # TODO: Implement unreachable vertex handling for Dask

    # Sort by vertex ID for consistent output
    result_df = result_df.sort_values("vertex")

    # Ensure correct data types
    result_df["vertex"] = result_df["vertex"].astype("int64")
    result_df["distance"] = result_df["distance"].astype("int64")
    result_df["layer"] = result_df["layer"].astype("int64")
    # Note: predecessor handling for nullable int in Dask is complex

    if compute:
        return result_df.compute()
    else:
        return result_df


def dfs(
    graph: Any,  # GraphFrame type hint will be added after implementation
    sources: int | list[int] | None = None,
    max_depth: int | None = None,
    directed: bool | None = None,
    backend: Literal["auto", "pandas", "dask"] | None = "auto",
    forest: bool = False,
) -> pd.DataFrame:
    """
    Perform Depth-First Search (DFS) traversal of a graph.

    DFS explores vertices by going as deep as possible along each branch
    before backtracking. Uses iterative implementation to avoid recursion limits.

    Args:
        graph: GraphFrame object containing the graph data
        sources: Starting vertex ID(s). If None and forest=False, uses vertex 0
        max_depth: Maximum depth to traverse. If None, explores until leaf nodes
        directed: Whether to treat graph as directed. If None, uses graph.is_directed
        backend: Backend selection ('auto', 'pandas', 'dask')
        forest: If True, performs DFS forest traversal over all components

    Returns:
        DataFrame with columns:
            - vertex (int64): Vertex ID
            - predecessor (int64): Previous vertex in DFS tree (nullable)
            - discovery_time (int64): Timestamp when vertex was first discovered
            - finish_time (int64): Timestamp when vertex processing completed
            - component_id (int64): Connected component ID (for forest traversal)

    Raises:
        ValueError: If sources contain invalid vertex IDs or graph is empty
        NotImplementedError: If Dask backend is requested (falls back to pandas)

    Examples:
        Single source DFS:
            >>> result = dfs(graph, sources=1)
            >>> print(result[['vertex', 'discovery_time', 'finish_time']])

        DFS forest (all components):
            >>> result = dfs(graph, forest=True)
            >>> print(result.groupby('component_id').size())
    """
    # 1. Validate inputs
    if graph.num_vertices == 0:
        raise ValueError("Cannot perform DFS on empty graph")

    # Handle directed parameter
    if directed is None:
        directed = graph.is_directed

    # Select backend (for Phase 1.2, only pandas is implemented)
    if backend == "dask":
        raise NotImplementedError(
            "Dask backend for DFS not implemented. "
            "DFS requires sequential traversal that doesn't parallelize well. "
            "Consider using BFS for large distributed graphs."
        )

    # Validate parameters
    if max_depth is not None and max_depth < 0:
        raise ValueError("max_depth must be non-negative")

    # 2. Get adjacency structure for efficient neighbor lookups
    if directed:
        adj = graph.csr_adjacency  # Outgoing edges only
    else:
        # For undirected graphs, we need both directions
        adj = graph.csr_adjacency
        adj_reverse = graph.csc_adjacency  # For incoming edges

    # 3. Initialize DFS data structures
    num_vertices = graph.num_vertices
    discovery_time = np.full(num_vertices, -1, dtype=np.int64)  # -1 = undiscovered
    finish_time = np.full(num_vertices, -1, dtype=np.int64)  # -1 = unfinished
    predecessor = np.full(num_vertices, -1, dtype=np.int64)  # -1 = no predecessor
    component_id = np.full(num_vertices, -1, dtype=np.int64)  # -1 = unassigned

    time_counter = 0
    current_component = 0

    def _dfs_visit(start_vertex: int, component: int) -> int:
        """Perform DFS visit from a starting vertex using iterative approach."""
        nonlocal time_counter

        # Stack stores tuples of (vertex, neighbors_iterator, depth)
        # We use a custom iterator approach to handle the iterative DFS properly
        stack = [(start_vertex, None, 0)]  # (vertex, neighbors_iter, depth)
        vertex_state = {}  # Track state: 'discovering', 'processing', 'finished'

        while stack:
            vertex, neighbors_iter, depth = stack[-1]

            # Check depth limit
            if max_depth is not None and depth > max_depth:
                stack.pop()
                continue

            # Initialize vertex if first time seeing it
            if vertex not in vertex_state:
                if discovery_time[vertex] != -1:  # Already discovered in this component
                    stack.pop()
                    continue

                # Discover vertex
                vertex_state[vertex] = "discovering"
                discovery_time[vertex] = time_counter
                component_id[vertex] = component
                time_counter += 1

                # Get neighbors based on graph directionality
                # Handle isolated vertices (vertex >= adjacency structure size)
                if vertex >= adj.num_vertices:
                    neighbors = np.array([], dtype=np.int64)  # Isolated vertex
                elif directed:
                    neighbors = adj.neighbors(vertex)
                else:
                    out_neighbors = adj.neighbors(vertex)
                    if vertex >= adj_reverse.num_vertices:
                        in_neighbors = np.array([], dtype=np.int64)
                    else:
                        in_neighbors = adj_reverse.predecessors(vertex)

                    # Handle case where vertex has no neighbors in either direction
                    if len(out_neighbors) == 0 and len(in_neighbors) == 0:
                        neighbors = np.array([], dtype=np.int64)
                    elif len(out_neighbors) == 0:
                        neighbors = in_neighbors
                    elif len(in_neighbors) == 0:
                        neighbors = out_neighbors
                    else:
                        neighbors = np.unique(
                            np.concatenate([out_neighbors, in_neighbors])
                        )

                # Update stack with neighbors iterator
                stack[-1] = (vertex, iter(neighbors), depth)
                vertex_state[vertex] = "processing"
                continue

            # Process next neighbor
            if vertex_state[vertex] == "processing":
                try:
                    neighbor = next(neighbors_iter)
                    if discovery_time[neighbor] == -1:  # Undiscovered
                        predecessor[neighbor] = vertex
                        stack.append((neighbor, None, depth + 1))
                except StopIteration:
                    # Finished processing all neighbors
                    finish_time[vertex] = time_counter
                    time_counter += 1
                    vertex_state[vertex] = "finished"
                    stack.pop()

        return time_counter

    # 4. Handle forest vs single-source modes
    if forest:
        # Forest traversal: visit all vertices, creating components
        for vertex in range(num_vertices):
            if discovery_time[vertex] == -1:  # Undiscovered
                _dfs_visit(vertex, current_component)
                current_component += 1
    else:
        # Single or multi-source traversal
        if sources is None:
            sources = [0] if num_vertices > 0 else []
        elif isinstance(sources, int):
            sources = [sources]
        else:
            sources = list(sources)

        if not sources:
            raise ValueError("At least one source vertex must be specified")

        # Validate source vertices exist
        for src in sources:
            if src < 0 or src >= num_vertices:
                raise ValueError(
                    f"Source vertex {src} out of range [0, {num_vertices})"
                )

        # Visit each source (handles multi-source case)
        for src in sources:
            if discovery_time[src] == -1:  # Not yet discovered
                _dfs_visit(src, current_component)
                current_component += 1

    # 5. Create result DataFrame
    result_data = {
        "vertex": [],
        "predecessor": [],
        "discovery_time": [],
        "finish_time": [],
        "component_id": [],
    }

    for vertex in range(num_vertices):
        # Include vertex if it was discovered
        if discovery_time[vertex] != -1:
            result_data["vertex"].append(vertex)
            result_data["predecessor"].append(
                predecessor[vertex] if predecessor[vertex] != -1 else None
            )
            result_data["discovery_time"].append(discovery_time[vertex])
            result_data["finish_time"].append(finish_time[vertex])
            result_data["component_id"].append(component_id[vertex])

    # Create DataFrame with proper dtypes
    result_df = pd.DataFrame(result_data)
    if not result_df.empty:
        result_df["vertex"] = result_df["vertex"].astype("int64")
        result_df["predecessor"] = result_df["predecessor"].astype(
            "Int64"
        )  # Nullable int
        result_df["discovery_time"] = result_df["discovery_time"].astype("int64")
        result_df["finish_time"] = result_df["finish_time"].astype("int64")
        result_df["component_id"] = result_df["component_id"].astype("int64")
    else:
        # Handle empty result case
        result_df = pd.DataFrame(
            {
                "vertex": pd.Series([], dtype="int64"),
                "predecessor": pd.Series([], dtype="Int64"),
                "discovery_time": pd.Series([], dtype="int64"),
                "finish_time": pd.Series([], dtype="int64"),
                "component_id": pd.Series([], dtype="int64"),
            }
        )

    return result_df
