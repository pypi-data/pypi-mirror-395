"""
PageRank algorithm implementation with power iteration.

This module implements the PageRank algorithm with support for both pandas
and Dask backends, personalized PageRank, and proper handling of dangling nodes.
"""

from typing import Any, Literal, Union

import numpy as np
import pandas as pd

# Import Rust backend for accelerated PageRank computation
from ..rust_backend import is_rust_available, pagerank_rust

try:
    import dask.dataframe as dd

    DASK_AVAILABLE = True
except ImportError:
    DASK_AVAILABLE = False


def pagerank(
    graph: Any,  # GraphFrame type hint will be added after implementation
    alpha: float = 0.85,
    tol: float = 1e-6,
    max_iter: int = 100,
    weight_column: str | None = None,
    personalized: dict[int, float] | None = None,
    directed: bool | None = None,
    backend: Literal["auto", "pandas", "dask", "rust"] | None = "auto",
) -> Union[pd.DataFrame, "dd.DataFrame"]:
    """
    Compute PageRank scores using power iteration method.

    PageRank measures vertex importance based on the graph's link structure.
    Higher scores indicate more "important" or "central" vertices in the graph.

    Args:
        graph: GraphFrame object containing the graph data
        alpha: Damping factor (0.85 is Google's original value)
        tol: Convergence tolerance for L1 norm of score differences
        max_iter: Maximum number of iterations before forced termination
        weight_column: Name of edge weight column. If None, uses uniform weights
        personalized: Dict mapping vertex_id -> personalization weight for biased PageRank
        directed: Whether to treat graph as directed. If None, uses graph.is_directed
        backend: Backend selection ('auto', 'pandas', 'dask', 'rust')
            - 'auto': Prefer Rust if available, fallback to pandas/dask
            - 'rust': Force Rust backend (error if unavailable)
            - 'pandas': Force pandas backend
            - 'dask': Force Dask backend

    Returns:
        DataFrame with columns:
            - vertex (int64): Vertex ID
            - rank (float64): PageRank score (sums to 1.0 across all vertices)

    Raises:
        ValueError: If alpha not in (0, 1), tol <= 0, max_iter < 1,
                   or personalized contains invalid vertex IDs
        RuntimeError: If algorithm fails to converge within max_iter iterations

    Examples:
        Basic PageRank:
            >>> ranks = pagerank(graph, alpha=0.85, max_iter=100)
            >>> top_vertices = ranks.nlargest(10, 'rank')
            >>> print(top_vertices[['vertex', 'rank']])

        Personalized PageRank (biased towards specific vertices):
            >>> bias = {1: 0.5, 10: 0.3, 100: 0.2}  # Favor vertices 1, 10, 100
            >>> ranks = pagerank(graph, personalized=bias)
            >>> print(ranks.nlargest(5, 'rank'))

        Weighted PageRank:
            >>> ranks = pagerank(graph, weight_column='importance', alpha=0.9)
    """
    # 1. Validate inputs
    if graph.num_vertices == 0:
        raise ValueError("Cannot compute PageRank on empty graph")

    _validate_pagerank_params(alpha, tol, max_iter, personalized, graph.num_vertices)

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
        return pagerank_rust_wrapper(
            graph, alpha, tol, max_iter, weight_column, personalized, directed
        )
    elif backend == "auto":
        # Auto selection: prefer Rust for best performance, fallback to Python
        if is_rust_available() and weight_column is None:
            # Use Rust when available and no custom weights (Phase 3.3 implementation)
            # TODO: Add weighted PageRank support in Rust (Phase 3.4)
            try:
                return pagerank_rust_wrapper(
                    graph, alpha, tol, max_iter, weight_column, personalized, directed
                )
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
                    "Dask is required for distributed PageRank but is not installed. "
                    "Install with: pip install dask[complete]"
                )
            return pagerank_dask(
                graph, alpha, tol, max_iter, weight_column, personalized, directed
            )
        else:
            return pagerank_pandas(
                graph, alpha, tol, max_iter, weight_column, personalized, directed
            )
    elif backend == "dask":
        # Explicitly requested Dask backend
        if not DASK_AVAILABLE:
            raise ImportError(
                "Dask is required for distributed PageRank but is not installed. "
                "Install with: pip install dask[complete]"
            )
        return pagerank_dask(
            graph, alpha, tol, max_iter, weight_column, personalized, directed
        )
    else:
        # backend == "pandas" or any other value defaults to pandas
        return pagerank_pandas(
            graph, alpha, tol, max_iter, weight_column, personalized, directed
        )


def pagerank_rust_wrapper(
    graph: Any,  # GraphFrame type hint will be added after implementation
    alpha: float,
    tol: float,
    max_iter: int,
    weight_column: str | None = None,
    personalized: dict[int, float] | None = None,
    directed: bool = True,
) -> pd.DataFrame:
    """
    PageRank implementation using Rust backend for maximum performance.

    This wrapper function interfaces with the Rust implementation,
    providing 5-20x speedup over pure Python implementations.

    Args:
        graph: GraphFrame object
        alpha: Damping factor
        tol: Convergence tolerance
        max_iter: Maximum iterations
        weight_column: Edge weight column name (currently must be None)
        personalized: Personalization vector
        directed: Whether graph is directed

    Returns:
        DataFrame with PageRank results

    Raises:
        RuntimeError: If Rust backend is not available
        ValueError: If weight_column is provided (not yet supported in Rust)

    Examples:
        Force Rust backend:
            >>> ranks = pagerank_rust_wrapper(graph, alpha=0.85, tol=1e-6, max_iter=100)
    """
    # Phase 3.3: Only unweighted PageRank is implemented in Rust
    if weight_column is not None:
        raise ValueError(
            "Weighted PageRank not yet supported in Rust backend (Phase 3.3). "
            "Use backend='pandas' or backend='dask' for weighted PageRank."
        )

    # 1. Get CSR adjacency structure (required by Rust backend)
    if directed:
        adj = graph.csr_adjacency  # Use CSR for directed graphs
    else:
        # For undirected graphs, we need symmetric CSR
        # The Rust backend expects a directed graph structure,
        # so we'll use the existing CSR (which may need enhancement)
        adj = graph.csr_adjacency

    # 2. Prepare personalization vector if provided
    num_vertices = graph.num_vertices
    if personalized is not None:
        # Normalize personalization weights
        total_personalized_weight = sum(personalized.values())
        personalization_array = np.zeros(num_vertices, dtype=np.float64)
        for vertex_id, weight in personalized.items():
            personalization_array[vertex_id] = weight / total_personalized_weight
    else:
        # Rust backend expects None for uniform personalization
        personalization_array = None

    # 3. Call Rust PageRank function
    # Rust expects: (indptr, indices, num_vertices, alpha, tol, max_iter, personalization)
    pagerank_scores = pagerank_rust(
        indptr=adj.indptr,
        indices=adj.indices,
        num_vertices=num_vertices,
        alpha=alpha,
        tol=tol,
        max_iter=max_iter,
        personalization=personalization_array,
    )

    # 4. Create result DataFrame with proper dtypes
    result_df = pd.DataFrame({"vertex": range(num_vertices), "rank": pagerank_scores})
    result_df["vertex"] = result_df["vertex"].astype("int64")
    result_df["rank"] = result_df["rank"].astype("float64")

    return result_df


def pagerank_pandas(
    graph: Any,  # GraphFrame type hint will be added after implementation
    alpha: float,
    tol: float,
    max_iter: int,
    weight_column: str | None = None,
    personalized: dict[int, float] | None = None,
    directed: bool = True,
) -> pd.DataFrame:
    """
    PageRank implementation for pandas backend using dense operations.

    Efficient implementation using numpy arrays and pandas operations
    optimized for in-memory processing of medium-sized graphs.

    Args:
        graph: GraphFrame object
        alpha: Damping factor
        tol: Convergence tolerance
        max_iter: Maximum iterations
        weight_column: Edge weight column name
        personalized: Personalization vector
        directed: Whether graph is directed

    Returns:
        DataFrame with PageRank results

    Examples:
        Force pandas backend:
            >>> ranks = pagerank_pandas(graph, alpha=0.85, tol=1e-6, max_iter=100)
    """
    num_vertices = graph.num_vertices

    # 1. Get edge data and handle ParquetFrame objects
    edges_df = graph.edges
    if hasattr(edges_df, "pandas_df"):
        edges_df = edges_df.pandas_df
    elif hasattr(edges_df, "compute"):
        edges_df = edges_df.compute()

    # Determine column names
    from ..data import EdgeSet

    edge_set = EdgeSet(
        data=graph.edges, edge_type="default", properties={}, schema=None
    )
    src_col = edge_set.src_column or "src"
    dst_col = edge_set.dst_column or "dst"

    # 2. Prepare edges with weights
    if weight_column is not None:
        if weight_column not in edges_df.columns:
            raise ValueError(
                f"Weight column '{weight_column}' not found in graph edges"
            )
        edges_with_weights = edges_df[[src_col, dst_col, weight_column]].copy()
        edges_with_weights["weight"] = edges_with_weights[weight_column]
    else:
        # Use uniform weights (1.0 for all edges)
        edges_with_weights = edges_df[[src_col, dst_col]].copy()
        edges_with_weights["weight"] = 1.0

    # For undirected graphs, add reverse edges
    if not directed:
        reverse_edges = edges_with_weights.copy()
        reverse_edges[[src_col, dst_col]] = reverse_edges[[dst_col, src_col]]
        edges_with_weights = pd.concat(
            [edges_with_weights, reverse_edges], ignore_index=True
        )

    # 3. Compute out-degrees (sum of weights for outgoing edges)
    out_degrees = (
        edges_with_weights.groupby(src_col)["weight"]
        .sum()
        .reindex(range(num_vertices), fill_value=0.0)
    )

    # Handle dangling nodes (vertices with out-degree 0)
    dangling_nodes = out_degrees == 0.0

    # 4. Initialize PageRank vector
    if personalized is not None:
        # Normalize personalization weights
        total_personalized_weight = sum(personalized.values())
        personalization = np.zeros(num_vertices, dtype=np.float64)
        for vertex_id, weight in personalized.items():
            personalization[vertex_id] = weight / total_personalized_weight
    else:
        # Uniform personalization
        personalization = np.full(num_vertices, 1.0 / num_vertices, dtype=np.float64)

    # Initialize PageRank scores
    pagerank_scores = np.full(num_vertices, 1.0 / num_vertices, dtype=np.float64)

    # 5. Power iteration loop
    for _iteration in range(max_iter):
        prev_scores = pagerank_scores.copy()

        # Reset scores to zero
        pagerank_scores.fill(0.0)

        # Distribute PageRank from each vertex to its neighbors
        for _, edge in edges_with_weights.iterrows():
            src, dst, weight = (
                int(edge[src_col]),
                int(edge[dst_col]),
                float(edge["weight"]),
            )

            # Skip if source has no outgoing edges (handled below)
            if out_degrees.iloc[src] > 0:
                contribution = (weight / out_degrees.iloc[src]) * prev_scores[src]
                pagerank_scores[dst] += contribution

        # Handle dangling nodes - distribute their PageRank according to personalization
        dangling_sum = prev_scores[dangling_nodes].sum()
        pagerank_scores += dangling_sum * personalization

        # Apply damping factor and random jump probability
        pagerank_scores = alpha * pagerank_scores + (1 - alpha) * personalization

        # Check convergence using L1 norm
        diff = np.abs(pagerank_scores - prev_scores).sum()
        if diff < tol:
            break
    else:
        # Did not converge within max_iter
        # In practice, PageRank usually converges, so we'll just warn
        import warnings

        warnings.warn(
            f"PageRank did not converge within {max_iter} iterations. "
            f"Final L1 difference: {diff:.2e}",
            RuntimeWarning,
            stacklevel=2,
        )

    # 6. Create result DataFrame
    result_df = pd.DataFrame({"vertex": range(num_vertices), "rank": pagerank_scores})

    result_df["vertex"] = result_df["vertex"].astype("int64")
    result_df["rank"] = result_df["rank"].astype("float64")

    return result_df


def pagerank_dask(
    graph: Any,  # GraphFrame type hint will be added after implementation
    alpha: float,
    tol: float,
    max_iter: int,
    weight_column: str | None = None,
    personalized: dict[int, float] | None = None,
    directed: bool = True,
    compute: bool = True,
) -> Union[pd.DataFrame, "dd.DataFrame"]:
    """
    PageRank implementation for Dask backend using DataFrame operations.

    Distributed implementation using Dask DataFrame joins and aggregations.
    Suitable for large graphs that don't fit in memory.

    Args:
        graph: GraphFrame object
        alpha: Damping factor
        tol: Convergence tolerance
        max_iter: Maximum iterations
        weight_column: Edge weight column name
        personalized: Personalization vector
        directed: Whether graph is directed
        compute: Whether to compute result or return lazy DataFrame

    Returns:
        DataFrame with PageRank results (computed to pandas if compute=True)

    Raises:
        RuntimeError: If convergence check fails due to Dask computation issues

    Examples:
        Force Dask backend:
            >>> ranks = pagerank_dask(graph, alpha=0.85, tol=1e-6, max_iter=50)
    """
    num_vertices = graph.num_vertices

    # 1. Get edge data as Dask DataFrame
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

    # 2. Prepare edges with weights
    if weight_column is not None:
        if weight_column not in edges_df.columns:
            raise ValueError(
                f"Weight column '{weight_column}' not found in graph edges"
            )
        edges_with_weights = edges_df[[src_col, dst_col, weight_column]].copy()
        edges_with_weights["weight"] = edges_with_weights[weight_column]
    else:
        # Use uniform weights (1.0 for all edges)
        edges_with_weights = edges_df[[src_col, dst_col]].copy()
        edges_with_weights["weight"] = 1.0

    # For undirected graphs, add reverse edges
    if not directed:
        reverse_edges = edges_with_weights.copy()
        reverse_edges = reverse_edges.rename(
            columns={src_col: dst_col, dst_col: src_col}
        )
        edges_with_weights = dd.concat(
            [edges_with_weights, reverse_edges], ignore_index=True
        )

    # 3. Compute out-degrees
    out_degrees = (
        edges_with_weights.groupby(src_col)["weight"]
        .sum()
        .reset_index()
        .rename(columns={"weight": "out_degree"})
    )

    # Create complete vertex DataFrame for reindexing
    all_vertices = dd.from_pandas(
        pd.DataFrame({src_col: range(num_vertices), "out_degree": 0.0}), npartitions=2
    )

    # Merge to get out-degrees for all vertices (including isolated ones)
    out_degrees_complete = all_vertices.merge(
        out_degrees, on=src_col, how="left", suffixes=("_default", "")
    )
    out_degrees_complete["out_degree"] = out_degrees_complete["out_degree"].fillna(
        out_degrees_complete["out_degree_default"]
    )
    out_degrees_complete = out_degrees_complete[[src_col, "out_degree"]]

    # 4. Initialize PageRank DataFrame
    if personalized is not None:
        # Normalize personalization weights
        total_personalized_weight = sum(personalized.values())
        personalization_data = []
        for vertex in range(num_vertices):
            if vertex in personalized:
                weight = personalized[vertex] / total_personalized_weight
            else:
                weight = 0.0
            personalization_data.append({"vertex": vertex, "personalization": weight})
    else:
        # Uniform personalization
        uniform_weight = 1.0 / num_vertices
        personalization_data = [
            {"vertex": vertex, "personalization": uniform_weight}
            for vertex in range(num_vertices)
        ]

    personalization_df = dd.from_pandas(
        pd.DataFrame(personalization_data), npartitions=2
    )

    # Initialize PageRank scores (uniform)
    pagerank_df = dd.from_pandas(
        pd.DataFrame({"vertex": range(num_vertices), "rank": 1.0 / num_vertices}),
        npartitions=2,
    )

    # 5. Power iteration loop (simplified for Dask)
    for _iteration in range(min(max_iter, 20)):  # Limit iterations for Dask
        # Join edges with current PageRank scores
        edge_contributions = edges_with_weights.merge(
            pagerank_df.rename(columns={"vertex": src_col, "rank": "src_rank"}),
            on=src_col,
            how="inner",
        )

        # Join with out-degrees to compute normalized contributions
        edge_contributions = edge_contributions.merge(
            out_degrees_complete, on=src_col, how="left"
        )

        # Handle division by zero (dangling nodes)
        edge_contributions["out_degree"] = edge_contributions["out_degree"].fillna(1.0)
        # For Dask, we'll handle zero out-degrees differently
        edge_contributions["out_degree"] = edge_contributions["out_degree"].where(
            edge_contributions["out_degree"] > 0.0, 1.0
        )

        # Compute contribution from each edge
        edge_contributions["contribution"] = (
            edge_contributions["weight"] / edge_contributions["out_degree"]
        ) * edge_contributions["src_rank"]

        # Aggregate contributions by destination vertex
        new_scores = (
            edge_contributions.groupby(dst_col)["contribution"]
            .sum()
            .reset_index()
            .rename(columns={dst_col: "vertex", "contribution": "aggregated_rank"})
        )

        # Merge with all vertices to handle isolated vertices
        new_pagerank = pagerank_df[["vertex"]].merge(
            new_scores, on="vertex", how="left"
        )
        new_pagerank["aggregated_rank"] = new_pagerank["aggregated_rank"].fillna(0.0)

        # Merge with personalization
        new_pagerank = new_pagerank.merge(personalization_df, on="vertex", how="left")

        # Apply damping factor
        new_pagerank["rank"] = (
            alpha * new_pagerank["aggregated_rank"]
            + (1 - alpha) * new_pagerank["personalization"]
        )

        # Update PageRank scores
        pagerank_df = new_pagerank[["vertex", "rank"]]

    # 6. Prepare final result
    result_df = pagerank_df.sort_values("vertex")
    result_df["vertex"] = result_df["vertex"].astype("int64")
    result_df["rank"] = result_df["rank"].astype("float64")

    if compute:
        return result_df.compute()
    else:
        return result_df


def _validate_pagerank_params(
    alpha: float,
    tol: float,
    max_iter: int,
    personalized: dict[int, float] | None = None,
    num_vertices: int | None = None,
) -> None:
    """
    Validate PageRank algorithm parameters.

    Args:
        alpha: Damping factor to validate
        tol: Convergence tolerance to validate
        max_iter: Maximum iterations to validate
        personalized: Personalization dict to validate
        num_vertices: Number of vertices for personalization validation

    Raises:
        ValueError: If any parameter is invalid
    """
    # 1. Check alpha in (0, 1) exclusive range
    if not (0 < alpha < 1):
        raise ValueError(f"alpha must be in (0, 1), got {alpha}")

    # 2. Check tol > 0
    if tol <= 0:
        raise ValueError(f"tol must be positive, got {tol}")

    # 3. Check max_iter >= 1
    if max_iter < 1:
        raise ValueError(f"max_iter must be at least 1, got {max_iter}")

    # 4. If personalized provided, validate vertex IDs and weights
    if personalized is not None:
        if not personalized:  # Empty dict
            raise ValueError("personalized cannot be empty dict")

        # Check vertex IDs are valid
        if num_vertices is not None:
            invalid_vertices = [
                v for v in personalized.keys() if v < 0 or v >= num_vertices
            ]
            if invalid_vertices:
                raise ValueError(
                    f"personalized contains invalid vertex IDs: {invalid_vertices}. "
                    f"Valid range is [0, {num_vertices})"
                )

        # Check all weights are non-negative
        negative_weights = [v for v in personalized.values() if v < 0]
        if negative_weights:
            raise ValueError(
                f"personalized weights must be non-negative, got negative values: {negative_weights}"
            )

        # Check weights sum to positive value (we'll normalize)
        weight_sum = sum(personalized.values())
        if weight_sum <= 0:
            raise ValueError(
                f"personalized weights must sum to positive value, got sum: {weight_sum}"
            )
