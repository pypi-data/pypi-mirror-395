"""
Rust backend integration for graph algorithms.

This module provides utilities for detecting and using the Rust backend
for graph algorithms when available, with automatic fallback to Python
implementations.
"""

import logging

import numpy as np

# Attempt to import Rust backend
try:
    from parquetframe import _rustic

    RUST_AVAILABLE = True
    RUST_VERSION = _rustic.rust_version()
except ImportError:
    RUST_AVAILABLE = False
    RUST_VERSION = None
    _rustic = None

logger = logging.getLogger(__name__)


def is_rust_available() -> bool:
    """Check if Rust backend is available."""
    return RUST_AVAILABLE


def get_rust_version() -> str | None:
    """Get Rust backend version if available."""
    return RUST_VERSION


def build_csr_rust(
    sources: np.ndarray,
    targets: np.ndarray,
    num_vertices: int,
    weights: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray | None]:
    """
    Build CSR adjacency structure using Rust backend.

    Args:
        sources: Source vertex IDs (int32)
        targets: Target vertex IDs (int32)
        num_vertices: Total number of vertices
        weights: Optional edge weights (float64)

    Returns:
        Tuple of (indptr, indices, weights) arrays

    Raises:
        RuntimeError: If Rust backend is not available
    """
    if not RUST_AVAILABLE:
        raise RuntimeError(
            "Rust backend not available. Install with: pip install parquetframe[rust]"
        )

    # Ensure correct dtypes
    sources = np.asarray(sources, dtype=np.int32)
    targets = np.asarray(targets, dtype=np.int32)
    if weights is not None:
        weights = np.asarray(weights, dtype=np.float64)

    # Call Rust function
    indptr, indices, rust_weights = _rustic.build_csr_rust(
        sources, targets, num_vertices, weights
    )

    # Convert to int64 for consistency with Python implementation
    indptr = np.asarray(indptr, dtype=np.int64)
    indices = np.asarray(indices, dtype=np.int64)

    return indptr, indices, rust_weights


def build_csc_rust(
    sources: np.ndarray,
    targets: np.ndarray,
    num_vertices: int,
    weights: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray | None]:
    """
    Build CSC adjacency structure using Rust backend.

    Args:
        sources: Source vertex IDs (int32)
        targets: Target vertex IDs (int32)
        num_vertices: Total number of vertices
        weights: Optional edge weights (float64)

    Returns:
        Tuple of (indptr, indices, weights) arrays

    Raises:
        RuntimeError: If Rust backend is not available
    """
    if not RUST_AVAILABLE:
        raise RuntimeError(
            "Rust backend not available. Install with: pip install parquetframe[rust]"
        )

    # Ensure correct dtypes
    sources = np.asarray(sources, dtype=np.int32)
    targets = np.asarray(targets, dtype=np.int32)
    if weights is not None:
        weights = np.asarray(weights, dtype=np.float64)

    # Call Rust function
    indptr, indices, rust_weights = _rustic.build_csc_rust(
        sources, targets, num_vertices, weights
    )

    # Convert to int64 for consistency with Python implementation
    indptr = np.asarray(indptr, dtype=np.int64)
    indices = np.asarray(indices, dtype=np.int64)

    return indptr, indices, rust_weights


def bfs_rust(
    indptr: np.ndarray,
    indices: np.ndarray,
    num_vertices: int,
    sources: list[int] | np.ndarray,
    max_depth: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Perform BFS traversal using Rust backend.

    Args:
        indptr: CSR indptr array (int64)
        indices: CSR indices array (int64)
        num_vertices: Total number of vertices
        sources: Source vertex IDs
        max_depth: Maximum traversal depth (None for unlimited)

    Returns:
        Tuple of (distances, predecessors) arrays

    Raises:
        RuntimeError: If Rust backend is not available
    """
    if not RUST_AVAILABLE:
        raise RuntimeError(
            "Rust backend not available. Install with: pip install parquetframe[rust]"
        )

    # Ensure correct dtypes
    indptr = np.asarray(indptr, dtype=np.int64)
    indices = np.asarray(indices, dtype=np.int32)  # Rust uses int32
    sources = np.asarray(sources, dtype=np.int32)

    # Call Rust function
    distances, predecessors = _rustic.bfs_rust(
        indptr, indices, num_vertices, sources, max_depth
    )

    # Convert to int64 for consistency
    distances = np.asarray(distances, dtype=np.int64)
    predecessors = np.asarray(predecessors, dtype=np.int64)

    return distances, predecessors


def dfs_rust(
    indptr: np.ndarray,
    indices: np.ndarray,
    num_vertices: int,
    source: int,
    max_depth: int | None = None,
) -> np.ndarray:
    """
    Perform DFS traversal using Rust backend.

    Args:
        indptr: CSR indptr array (int64)
        indices: CSR indices array (int64)
        num_vertices: Total number of vertices
        source: Source vertex ID
        max_depth: Maximum traversal depth (None for unlimited)

    Returns:
        Array of visited vertex IDs in DFS order

    Raises:
        RuntimeError: If Rust backend is not available
    """
    if not RUST_AVAILABLE:
        raise RuntimeError(
            "Rust backend not available. Install with: pip install parquetframe[rust]"
        )

    # Ensure correct dtypes
    indptr = np.asarray(indptr, dtype=np.int64)
    indices = np.asarray(indices, dtype=np.int32)  # Rust uses int32

    # Call Rust function
    visited = _rustic.dfs_rust(indptr, indices, num_vertices, source, max_depth)

    # Convert to int64 for consistency
    visited = np.asarray(visited, dtype=np.int64)

    return visited


def pagerank_rust(
    indptr: np.ndarray,
    indices: np.ndarray,
    num_vertices: int,
    alpha: float = 0.85,
    tol: float = 1e-6,
    max_iter: int = 100,
    personalization: np.ndarray | None = None,
) -> np.ndarray:
    """
    Compute PageRank using Rust implementation.

    PageRank measures vertex importance based on the graph's link structure
    using power iteration method with damping factor.

    Args:
        indptr: CSR indptr array (int64)
        indices: CSR indices array (int32)
        num_vertices: Total number of vertices in the graph
        alpha: Damping factor, typically 0.85 (probability of following links)
        tol: Convergence tolerance for L1 norm (default 1e-6)
        max_iter: Maximum number of iterations (default 100)
        personalization: Optional personalization vector (float64) for
            personalized PageRank. Must have length num_vertices.

    Returns:
        PageRank scores as numpy array (float64), normalized to sum to 1.0

    Raises:
        RuntimeError: If Rust backend is not available
        ValueError: If inputs are invalid (e.g., alpha not in (0,1))

    Examples:
        >>> indptr = np.array([0, 2, 3, 3], dtype=np.int64)
        >>> indices = np.array([1, 2, 2], dtype=np.int32)
        >>> scores = pagerank_rust(indptr, indices, 3)
        >>> print(scores)  # doctest: +SKIP
        [0.333, 0.333, 0.333]
    """
    if not RUST_AVAILABLE:
        raise RuntimeError(
            "Rust backend not available. Install with: pip install parquetframe"
        )

    # Ensure correct dtypes
    indptr = np.asarray(indptr, dtype=np.int64)
    indices = np.asarray(indices, dtype=np.int32)
    if personalization is not None:
        personalization = np.asarray(personalization, dtype=np.float64)

    # Call Rust function (note: PyO3 binding is named pagerank_rust_py)
    scores = _rustic.pagerank_rust_py(
        indptr, indices, num_vertices, alpha, tol, max_iter, personalization
    )

    return scores


def dijkstra_rust(
    indptr: np.ndarray,
    indices: np.ndarray,
    num_vertices: int,
    sources: np.ndarray,
    weights: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute shortest paths using Dijkstra's algorithm in Rust.

    Dijkstra's algorithm finds shortest paths from source vertices to all
    other vertices in a graph with non-negative edge weights using a
    binary heap priority queue.

    Args:
        indptr: CSR indptr array (int64)
        indices: CSR indices array (int32)
        num_vertices: Total number of vertices in the graph
        sources: Source vertex IDs (int32 array)
        weights: Edge weights (float64 array), must have same length as
            number of edges in CSR structure

    Returns:
        Tuple of (distances, predecessors):
            - distances: Distance from nearest source to each vertex (float64),
              inf for unreachable vertices
            - predecessors: Previous vertex in shortest path (int32),
              -1 for sources and unreachable vertices

    Raises:
        RuntimeError: If Rust backend is not available
        ValueError: If weights contain negative values or length mismatch

    Examples:
        >>> indptr = np.array([0, 2, 3], dtype=np.int64)
        >>> indices = np.array([1, 2, 2], dtype=np.int32)
        >>> weights = np.array([1.0, 4.0, 2.0], dtype=np.float64)
        >>> sources = np.array([0], dtype=np.int32)
        >>> distances, preds = dijkstra_rust(indptr, indices, 3, sources, weights)
        >>> print(distances)  # doctest: +SKIP
        [0.0, 1.0, 3.0]
    """
    if not RUST_AVAILABLE:
        raise RuntimeError(
            "Rust backend not available. Install with: pip install parquetframe"
        )

    # Ensure correct dtypes
    indptr = np.asarray(indptr, dtype=np.int64)
    indices = np.asarray(indices, dtype=np.int32)
    sources = np.asarray(sources, dtype=np.int32)
    weights = np.asarray(weights, dtype=np.float64)

    # Call Rust function (note: PyO3 binding is named dijkstra_rust_py)
    distances, predecessors = _rustic.dijkstra_rust_py(
        indptr, indices, num_vertices, sources, weights
    )

    return distances, predecessors


def connected_components_rust(
    sources: np.ndarray,
    targets: np.ndarray,
    num_vertices: int,
    directed: bool = False,
) -> np.ndarray:
    """
    Find connected components using union-find algorithm in Rust.

    For directed graphs, computes weakly connected components (treating
    edges as undirected). For undirected graphs, computes standard
    connected components.

    Uses an efficient union-find (disjoint-set) data structure with
    path compression and union by rank optimizations, achieving
    O(E × α(V)) time complexity where α is the inverse Ackermann function.

    Args:
        sources: Source vertex IDs (int64 array)
        targets: Target vertex IDs (int64 array)
        num_vertices: Total number of vertices in the graph
        directed: Whether graph is directed (for weak vs strong components)

    Returns:
        Component labels as numpy array (int64) where result[v] is the
        component ID of vertex v. Component IDs are consecutive integers
        starting from 0.

    Raises:
        RuntimeError: If Rust backend is not available
        ValueError: If sources and targets have different lengths or
            contain invalid vertex IDs

    Examples:
        >>> # Graph with two components: (0-1-2) and (3-4)
        >>> sources = np.array([0, 1, 3], dtype=np.int64)
        >>> targets = np.array([1, 2, 4], dtype=np.int64)
        >>> labels = connected_components_rust(sources, targets, 5, False)
        >>> print(labels)  # doctest: +SKIP
        [0, 0, 0, 1, 1]
    """
    if not RUST_AVAILABLE:
        raise RuntimeError(
            "Rust backend not available. Install with: pip install parquetframe"
        )

    # Ensure correct dtypes
    sources = np.asarray(sources, dtype=np.int64)
    targets = np.asarray(targets, dtype=np.int64)

    # Call Rust function (note: PyO3 binding is named connected_components_rust_py)
    components = _rustic.connected_components_rust_py(
        sources, targets, num_vertices, directed
    )

    return components
