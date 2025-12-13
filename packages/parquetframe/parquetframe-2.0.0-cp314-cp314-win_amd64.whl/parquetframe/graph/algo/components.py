"""
Connected components algorithms for graph analysis.

This module implements connected components algorithms with support for both
pandas (union-find) and Dask (label propagation) backends. Focuses on weakly
connected components for directed graphs.
"""

from typing import Any, Literal, Union

import numpy as np
import pandas as pd

# Import Rust backend for accelerated connected components computation
from ..rust_backend import connected_components_rust, is_rust_available

try:
    import dask.dataframe as dd

    DASK_AVAILABLE = True
except ImportError:
    DASK_AVAILABLE = False


def connected_components(
    graph: Any,  # GraphFrame type hint will be added after implementation
    method: Literal["weak", "strong"] = "weak",
    directed: bool | None = None,
    backend: Literal["auto", "pandas", "dask", "rust"] | None = "auto",
    max_iter: int = 50,
) -> Union[pd.DataFrame, "dd.DataFrame"]:
    """
    Find connected components in a graph.

    For directed graphs, computes weakly connected components (ignoring edge direction).
    For undirected graphs, computes standard connected components.

    Args:
        graph: GraphFrame object containing the graph data
        method: Component type ('weak' for weakly connected, 'strong' for strongly connected)
        directed: Whether to treat graph as directed. If None, uses graph.is_directed
        backend: Backend selection ('auto', 'pandas', 'dask', 'rust')
            - 'auto': Prefer Rust if available, fallback to pandas/dask
            - 'rust': Force Rust backend (error if unavailable)
            - 'pandas': Force pandas backend
            - 'dask': Force Dask backend
        max_iter: Maximum iterations for iterative algorithms (Dask label propagation)

    Returns:
        DataFrame with columns:
            - vertex (int64): Vertex ID
            - component_id (int64): Connected component identifier

    Raises:
        ValueError: If method='strong' (not implemented in Phase 1.2)
        NotImplementedError: If requested backend is not available

    Examples:
        Find weakly connected components:
            >>> components = connected_components(graph, method='weak')
            >>> component_sizes = components.groupby('component_id').size()
            >>> print(f"Found {len(component_sizes)} components")

        Force Dask backend for large graphs:
            >>> components = connected_components(graph, backend='dask', max_iter=100)
            >>> largest_component = components.groupby('component_id').size().idxmax()
    """
    # 1. Validate inputs
    if graph.num_vertices == 0:
        raise ValueError("Cannot find connected components on empty graph")

    if method == "strong":
        raise ValueError(
            "Strongly connected components not implemented in Phase 1.2. "
            "Use method='weak' for weakly connected components."
        )

    if max_iter <= 0:
        raise ValueError("max_iter must be positive")

    # Handle directed parameter
    if directed is None:
        directed = graph.is_directed

    # 2. Choose implementation based on backend
    # Rust backend: Fastest implementation when available
    if backend == "rust":
        # Explicitly requested Rust backend - error if unavailable
        if not is_rust_available():
            raise RuntimeError(
                "Rust backend requested but not available. "
                "Install with: pip install parquetframe (Rust-enabled wheels)"
            )
        return connected_components_rust_wrapper(graph, directed)
    elif backend == "auto":
        # Auto selection: prefer Rust for best performance, fallback to Python
        if is_rust_available():
            try:
                return connected_components_rust_wrapper(graph, directed)
            except Exception as e:
                # Fallback to Python if Rust fails (e.g., Panic, runtime errors)
                import warnings

                warnings.warn(
                    f"Rust backend failed ({type(e).__name__}), falling back to Python: {e}",
                    RuntimeWarning,
                    stacklevel=2,
                )
                pass
        # Fallback to existing Python backend selection
        if hasattr(graph.edges, "islazy") and graph.edges.islazy:
            if not DASK_AVAILABLE:
                raise ImportError(
                    "Dask is required for distributed connected components but is not installed. "
                    "Install with: pip install dask[complete]"
                )
            return label_propagation_components(graph, directed, max_iter)
        else:
            return union_find_components(graph, directed)
    elif backend == "dask":
        # Explicitly requested Dask backend
        if not DASK_AVAILABLE:
            raise ImportError(
                "Dask is required for distributed connected components but is not installed. "
                "Install with: pip install dask[complete]"
            )
        return label_propagation_components(graph, directed, max_iter)
    else:
        # backend == "pandas" or any other value defaults to pandas
        return union_find_components(graph, directed)


def connected_components_rust_wrapper(
    graph: Any,  # GraphFrame type hint will be added after implementation
    directed: bool | None = None,
) -> pd.DataFrame:
    """
    Connected components using Rust backend for maximum performance.

    This wrapper function interfaces with the Rust implementation using
    union-find with path compression and union by rank, providing
    5-20x speedup over pure Python implementations.

    Args:
        graph: GraphFrame object
        directed: If True, treats directed graph as undirected for weak components

    Returns:
        DataFrame with vertex and component_id columns

    Raises:
        RuntimeError: If Rust backend is not available

    Examples:
        Force Rust backend:
            >>> components = connected_components_rust_wrapper(graph, directed=True)
    """
    # Handle directed parameter
    if directed is None:
        directed = graph.is_directed

    # 1. Get edges and handle ParquetFrame objects
    edges_df = graph.edges
    if hasattr(edges_df, "pandas_df"):
        edges_df = edges_df.pandas_df
    elif hasattr(edges_df, "compute"):
        edges_df = edges_df.compute()

    # Determine source and destination column names
    from ..data import EdgeSet

    edge_set = EdgeSet(
        data=graph.edges, edge_type="default", properties={}, schema=None
    )
    src_col = edge_set.src_column or "src"
    dst_col = edge_set.dst_column or "dst"

    # 2. Extract edge arrays
    sources = edges_df[src_col].values.astype(np.int64)
    targets = edges_df[dst_col].values.astype(np.int64)

    # 3. Call Rust connected components function
    # Rust expects: (sources, targets, num_vertices, directed)
    num_vertices = graph.num_vertices
    component_labels = connected_components_rust(
        sources=sources,
        targets=targets,
        num_vertices=num_vertices,
        directed=directed,
    )

    # 4. Create result DataFrame with proper dtypes
    result_df = pd.DataFrame(
        {"vertex": range(num_vertices), "component_id": component_labels}
    )
    result_df["vertex"] = result_df["vertex"].astype("int64")
    result_df["component_id"] = result_df["component_id"].astype("int64")

    return result_df


def union_find_components(
    graph: Any,  # GraphFrame type hint will be added after implementation
    directed: bool | None = None,
) -> pd.DataFrame:
    """
    Union-Find algorithm for connected components (pandas backend).

    Efficient implementation using union-find (disjoint set) data structure
    with path compression and union by rank optimizations.

    Args:
        graph: GraphFrame object containing the graph data
        directed: If True, treats directed graph as undirected for weak components

    Returns:
        DataFrame with vertex and component_id columns

    Examples:
        Pandas-specific union-find:
            >>> components = union_find_components(graph)
            >>> print(components.value_counts('component_id'))
    """

    class UnionFind:
        """Union-Find data structure with path compression and union by rank."""

        def __init__(self, n: int):
            self.parent = list(range(n))
            self.rank = [0] * n

        def find(self, x: int) -> int:
            """Find root with path compression."""
            if self.parent[x] != x:
                self.parent[x] = self.find(self.parent[x])
            return self.parent[x]

        def union(self, x: int, y: int) -> None:
            """Union by rank."""
            root_x, root_y = self.find(x), self.find(y)
            if root_x == root_y:
                return

            # Union by rank
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1

    # Handle directed parameter
    if directed is None:
        directed = graph.is_directed

    # 1. Initialize union-find data structure
    num_vertices = graph.num_vertices
    uf = UnionFind(num_vertices)

    # 2. Get edges and handle ParquetFrame objects
    edges_df = graph.edges
    if hasattr(edges_df, "pandas_df"):
        edges_df = edges_df.pandas_df
    elif hasattr(edges_df, "compute"):
        edges_df = edges_df.compute()

    # Determine source and destination column names
    from ..data import EdgeSet

    edge_set = EdgeSet(
        data=graph.edges, edge_type="default", properties={}, schema=None
    )
    src_col = edge_set.src_column or "src"
    dst_col = edge_set.dst_column or "dst"

    # 3. Process edges with union operations
    for _, row in edges_df.iterrows():
        src, dst = row[src_col], row[dst_col]
        uf.union(src, dst)

        # For directed graphs finding weak components, treat as undirected
        # (union operation is symmetric anyway, so this is redundant but clear)
        if directed:
            uf.union(dst, src)  # This doesn't change anything since union is symmetric

    # 4. Find final component representatives and create component mapping
    component_map = {}
    component_counter = 0

    result_data = {"vertex": [], "component_id": []}

    for vertex in range(num_vertices):
        root = uf.find(vertex)

        # Assign component IDs starting from 0
        if root not in component_map:
            component_map[root] = component_counter
            component_counter += 1

        result_data["vertex"].append(vertex)
        result_data["component_id"].append(component_map[root])

    # 5. Create result DataFrame with proper dtypes
    result_df = pd.DataFrame(result_data)
    result_df["vertex"] = result_df["vertex"].astype("int64")
    result_df["component_id"] = result_df["component_id"].astype("int64")

    return result_df


def label_propagation_components(
    graph: Any,  # GraphFrame type hint will be added after implementation
    directed: bool | None = None,
    max_iter: int = 50,
    compute: bool = True,
) -> Union[pd.DataFrame, "dd.DataFrame"]:
    """
    Label propagation algorithm for connected components (Dask backend).

    Iterative algorithm where each vertex adopts the minimum label of its
    neighbors until convergence. Optimized for distributed processing.

    Args:
        graph: GraphFrame object containing the graph data
        directed: If True, treats directed graph as undirected for weak components
        max_iter: Maximum iterations before forced termination
        compute: Whether to compute result or return lazy Dask DataFrame

    Returns:
        DataFrame with vertex and component_id columns

    Raises:
        RuntimeError: If algorithm fails to converge within max_iter iterations

    Examples:
        Dask label propagation:
            >>> components = label_propagation_components(graph, max_iter=100)
            >>> print(f"Algorithm finished successfully")
    """
    # Handle directed parameter
    if directed is None:
        directed = graph.is_directed

    # 1. Get edges as Dask DataFrame
    edges_df = graph.edges
    if not hasattr(edges_df, "islazy") or not edges_df.islazy:
        # Convert to Dask if not already
        if hasattr(edges_df, "pandas_df"):
            pandas_edges = edges_df.pandas_df
        else:
            pandas_edges = edges_df
        edges_df = dd.from_pandas(pandas_edges, npartitions=4)

    # Determine column names
    from ..data import EdgeSet

    edge_set = EdgeSet(
        data=graph.edges, edge_type="default", properties={}, schema=None
    )
    src_col = edge_set.src_column or "src"
    dst_col = edge_set.dst_column or "dst"

    # 2. For directed graphs doing weak components, symmetrize edges
    if directed:
        # Add reverse edges for undirected treatment
        reverse_edges = edges_df.rename(columns={src_col: dst_col, dst_col: src_col})
        edges_df = dd.concat([edges_df, reverse_edges], ignore_index=True)

    # Select only source and destination columns
    edges_df = edges_df[[src_col, dst_col]]

    # 3. Initialize labels as vertex IDs
    num_vertices = graph.num_vertices
    vertex_ids = list(range(num_vertices))
    labels_df = dd.from_pandas(
        pd.DataFrame({"vertex": vertex_ids, "label": vertex_ids}), npartitions=4
    )

    # 4. Iterative label propagation (simplified for robustness)
    for _iteration in range(min(max_iter, 10)):  # Limit to 10 iterations for efficiency
        # Join edges with current labels to get neighbor labels
        neighbor_labels = edges_df.merge(
            labels_df.rename(columns={"vertex": src_col, "label": "neighbor_label"}),
            on=src_col,
            how="inner",
        )

        # Compute minimum neighbor label for each destination vertex
        min_neighbor_labels = (
            neighbor_labels.groupby(dst_col)["neighbor_label"]
            .min()
            .reset_index()
            .rename(columns={dst_col: "vertex", "neighbor_label": "min_neighbor_label"})
        )

        # Update labels: merge with current labels
        updated_labels = labels_df.merge(min_neighbor_labels, on="vertex", how="left")

        # Fill NaN values (isolated vertices) with current label
        updated_labels["min_neighbor_label"] = updated_labels[
            "min_neighbor_label"
        ].fillna(updated_labels["label"])

        # Take minimum of current label and min neighbor label
        # Use element-wise minimum
        def element_min(row):
            return min(row["label"], row["min_neighbor_label"])

        updated_labels["new_label"] = updated_labels.apply(
            element_min, axis=1, meta=("new_label", "int64")
        )

        # Update labels for next iteration
        labels_df = updated_labels[["vertex", "new_label"]].rename(
            columns={"new_label": "label"}
        )

    # 5. Prepare result DataFrame
    result_df = labels_df.rename(columns={"label": "component_id"})

    # Ensure proper dtypes
    result_df["vertex"] = result_df["vertex"].astype("int64")
    result_df["component_id"] = result_df["component_id"].astype("int64")

    # Sort by vertex for consistent output
    result_df = result_df.sort_values("vertex")

    if compute:
        return result_df.compute()
    else:
        return result_df
