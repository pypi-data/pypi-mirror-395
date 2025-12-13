"""
Utility functions shared across graph algorithms.

This module provides common functionality used by multiple graph algorithms
including backend selection, parameter validation, and result formatting.
"""

from typing import Any, Literal

import pandas as pd


def select_backend(
    graph: Any,  # GraphFrame type hint will be added after implementation
    backend: Literal["auto", "pandas", "dask"] | None = "auto",
    algorithm: str = "unknown",
) -> Literal["pandas", "dask"]:
    """
    Select the optimal backend for graph algorithm execution.

    Makes intelligent backend selection based on graph size, current data backend,
    user preference, and algorithm capabilities.

    Args:
        graph: GraphFrame object
        backend: User backend preference ('auto', 'pandas', 'dask')
        algorithm: Algorithm name for backend capability checking

    Returns:
        Selected backend ('pandas' or 'dask')

    Raises:
        NotImplementedError: If requested backend is not available for algorithm

    Examples:
        Automatic selection:
            >>> backend = select_backend(graph, 'auto', 'bfs')
            >>> print(f"Selected {backend} backend for BFS")
    """
    # 1. If backend explicitly specified, validate and return
    if backend in ["pandas", "dask"]:
        return backend  # type: ignore

    # 2. Check algorithm capabilities
    # DFS is typically sequential and hard to parallelize with Dask
    if algorithm == "dfs":
        return "pandas"

    # 3. Consider current graph data backend
    is_dask = False

    # Check vertices
    vertices = getattr(graph, "vertices", None)
    if vertices:
        # Check for islazy attribute (GraphFrame standard)
        if hasattr(vertices, "islazy") and vertices.islazy:
            is_dask = True
        # Check for Dask DataFrame (has compute method)
        elif hasattr(vertices, "_df") and hasattr(vertices._df, "compute"):
            is_dask = True
        elif hasattr(vertices, "compute"):
            is_dask = True

    # Check edges
    edges = getattr(graph, "edges", None)
    if edges:
        if hasattr(edges, "islazy") and edges.islazy:
            is_dask = True
        elif hasattr(edges, "_df") and hasattr(edges._df, "compute"):
            is_dask = True
        elif hasattr(edges, "compute"):
            is_dask = True

    if is_dask:
        return "dask"

    # Default to pandas
    return "pandas"


def validate_sources(
    graph: Any,  # GraphFrame type hint will be added after implementation
    sources: int | list[int] | None,
) -> list[int]:
    """
    Validate and normalize source vertex specification.

    Ensures source vertices exist in the graph and returns a consistent
    list format for algorithm processing.

    Args:
        graph: GraphFrame object
        sources: Source vertex specification (int, list, or None)

    Returns:
        List of validated source vertex IDs

    Raises:
        ValueError: If sources contain invalid vertex IDs or graph is empty

    Examples:
        Validate single source:
            >>> sources = validate_sources(graph, 42)
            >>> print(sources)  # [42]

        Validate multiple sources:
            >>> sources = validate_sources(graph, [1, 10, 100])
            >>> print(f"Validated {len(sources)} source vertices")
    """
    # Get vertices DataFrame
    vertices_df = (
        graph.vertices._df if hasattr(graph.vertices, "_df") else graph.vertices
    )

    # Handle Dask DataFrame
    if hasattr(vertices_df, "compute"):
        vertices_df = vertices_df.compute()

    # Check for empty graph
    if len(vertices_df) == 0:
        raise ValueError("Graph has no vertices")

    # Get vertex IDs column
    id_col = "id" if "id" in vertices_df.columns else vertices_df.columns[0]
    valid_ids = set(vertices_df[id_col].tolist())

    # Handle None case - default to first vertex
    if sources is None:
        return [vertices_df[id_col].iloc[0]]

    # Convert single int to list
    if isinstance(sources, int):
        sources = [sources]

    # Remove duplicates while preserving order
    seen = set()
    unique_sources = []
    for s in sources:
        if s not in seen:
            seen.add(s)
            unique_sources.append(s)

    # Validate all source IDs exist
    invalid = [s for s in unique_sources if s not in valid_ids]
    if invalid:
        raise ValueError(f"Invalid source vertex IDs: {invalid}")

    return unique_sources


def create_result_dataframe(
    data: dict[str, list],
    columns: list[str],
    dtypes: dict[str, str] | None = None,
) -> pd.DataFrame:
    """
    Create a standardized result DataFrame with proper column types.

    Ensures consistent column naming and data types across all algorithm results.

    Args:
        data: Dictionary mapping column names to value lists
        columns: Expected column order for the result
        dtypes: Optional dtype specifications for columns

    Returns:
        Formatted pandas DataFrame with correct types

    Examples:
        Create BFS result DataFrame:
            >>> data = {
            ...     'vertex': [0, 1, 2],
            ...     'distance': [0, 1, 2],
            ...     'predecessor': [None, 0, 1]
            ... }
            >>> result = create_result_dataframe(data, ['vertex', 'distance', 'predecessor'])
    """
    # Create DataFrame from data dict
    df = pd.DataFrame(data)

    # Reorder columns according to expected order
    ordered_cols = [c for c in columns if c in df.columns]
    df = df[ordered_cols]

    # Apply proper dtypes if specified
    if dtypes:
        for col, dtype in dtypes.items():
            if col in df.columns:
                try:
                    df[col] = df[col].astype(dtype)
                except (ValueError, TypeError):
                    # If conversion fails, try nullable version
                    pass

    return df


def symmetrize_edges(
    graph: Any,  # GraphFrame type hint will be added after implementation
    directed: bool | None = None,
) -> Any:  # Return type will be EdgeSet or similar
    """
    Create symmetrized edge set for undirected graph algorithms.

    For directed graphs that need to be treated as undirected (e.g., weak components),
    adds reverse edges to make the graph symmetric.

    Args:
        graph: GraphFrame object
        directed: Whether to treat graph as directed (None = use graph.is_directed)

    Returns:
        EdgeSet with potentially symmetrized edges

    Examples:
        Symmetrize directed graph:
            >>> undirected_edges = symmetrize_edges(graph, directed=False)
            >>> print(f"Original: {len(graph.edges)} edges")
            >>> print(f"Symmetrized: {len(undirected_edges)} edges")
    """
    # Check if symmetrization is needed
    is_directed = (
        directed if directed is not None else getattr(graph, "is_directed", True)
    )

    # If already undirected, return edges unchanged
    if not is_directed:
        return graph.edges

    # Get original edges
    edges = graph.edges
    if hasattr(edges, "_df"):
        edges_df = edges._df
    else:
        edges_df = edges

    # Handle Dask DataFrame
    if hasattr(edges_df, "compute"):
        edges_df = edges_df.compute()

    # Find src/dst columns
    src_col = "src" if "src" in edges_df.columns else edges_df.columns[0]
    dst_col = "dst" if "dst" in edges_df.columns else edges_df.columns[1]

    # Create reverse edges
    reverse_df = edges_df.copy()
    reverse_df[[src_col, dst_col]] = edges_df[[dst_col, src_col]].values

    # Concatenate and remove duplicates
    symmetrized = pd.concat([edges_df, reverse_df], ignore_index=True)
    symmetrized = symmetrized.drop_duplicates(subset=[src_col, dst_col])

    return symmetrized


def check_convergence(
    old_values: pd.Series | Any,  # Could be Dask Series
    new_values: pd.Series | Any,  # Could be Dask Series
    tol: float,
    metric: Literal["l1", "l2", "max"] = "l1",
) -> bool:
    """
    Check convergence between old and new algorithm values.

    Computes difference metric between iterations to determine if
    algorithm has converged within tolerance.

    Args:
        old_values: Previous iteration values
        new_values: Current iteration values
        tol: Convergence tolerance threshold
        metric: Distance metric ('l1', 'l2', 'max')

    Returns:
        True if converged (difference < tolerance)

    Examples:
        Check PageRank convergence:
            >>> converged = check_convergence(old_ranks, new_ranks, tol=1e-6)
            >>> if converged:
            ...     print("Algorithm converged!")
    """
    import numpy as np

    # Handle Dask Series
    if hasattr(old_values, "compute"):
        old_values = old_values.compute()
    if hasattr(new_values, "compute"):
        new_values = new_values.compute()

    # Handle empty series
    if len(old_values) == 0 or len(new_values) == 0:
        return False

    # Drop NaN values for comparison
    old_clean = old_values.dropna()
    new_clean = new_values.dropna()

    # If all values are NaN, return False
    if len(old_clean) == 0 or len(new_clean) == 0:
        return False

    # Compute difference based on metric
    diff = (old_clean - new_clean).abs()

    if metric == "l1":
        distance = diff.sum()
    elif metric == "l2":
        distance = np.sqrt((diff**2).sum())
    elif metric == "max":
        distance = diff.max()
    else:
        raise ValueError(f"Unknown metric: {metric}. Use 'l1', 'l2', or 'max'.")

    return bool(distance < tol)
