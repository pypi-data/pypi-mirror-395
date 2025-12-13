//! PyO3 bindings for graph algorithms.
//!
//! Provides Python-accessible functions for CSR/CSC construction and graph traversal.

use numpy::{PyArray1, PyArrayMethods, PyReadonlyArray1};
use pf_graph_core::{
    bfs_parallel, bfs_sequential, dfs, dijkstra_rust, pagerank_rust, union_find_components,
    CscGraph, CsrGraph,
};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

// Type alias for CSR/CSC return types to simplify function signatures
type CsrResult<'py> = (
    Py<PyArray1<i64>>,
    Py<PyArray1<i32>>,
    Option<Py<PyArray1<f64>>>,
);

// Type alias for BFS result
type BfsResult<'py> = (Py<PyArray1<i32>>, Py<PyArray1<i32>>);

// Type alias for Dijkstra result
type DijkstraResult<'py> = (Py<PyArray1<f64>>, Py<PyArray1<i32>>);

/// Build CSR adjacency structure from edge lists.
///
/// # Arguments
/// * `src` - Source vertex IDs (numpy array)
/// * `dst` - Destination vertex IDs (numpy array)
/// * `num_vertices` - Total number of vertices
/// * `weights` - Optional edge weights (numpy array)
///
/// # Returns
/// Tuple of (indptr, indices, weights) as numpy arrays
#[pyfunction]
fn build_csr_rust<'py>(
    py: Python<'py>,
    src: PyReadonlyArray1<i32>,
    dst: PyReadonlyArray1<i32>,
    num_vertices: usize,
    weights: Option<PyReadonlyArray1<f64>>,
) -> PyResult<CsrResult<'py>> {
    let src_slice = src.as_slice()?;
    let dst_slice = dst.as_slice()?;
    let weights_slice = weights.as_ref().map(|w| w.as_slice()).transpose()?;

    let csr = CsrGraph::from_edges(src_slice, dst_slice, num_vertices, weights_slice)
        .map_err(|e| PyValueError::new_err(e.to_string()))?;

    let indptr = PyArray1::from_vec(py, csr.indptr).to_owned().into();
    let indices = PyArray1::from_vec(py, csr.indices).to_owned().into();
    let w = csr
        .weights
        .map(|ws| PyArray1::from_vec(py, ws).to_owned().into());

    Ok((indptr, indices, w))
}

/// Build CSC adjacency structure from edge lists.
///
/// # Arguments
/// * `src` - Source vertex IDs (numpy array)
/// * `dst` - Destination vertex IDs (numpy array)
/// * `num_vertices` - Total number of vertices
/// * `weights` - Optional edge weights (numpy array)
///
/// # Returns
/// Tuple of (indptr, indices, weights) as numpy arrays
#[pyfunction]
fn build_csc_rust<'py>(
    py: Python<'py>,
    src: PyReadonlyArray1<i32>,
    dst: PyReadonlyArray1<i32>,
    num_vertices: usize,
    weights: Option<PyReadonlyArray1<f64>>,
) -> PyResult<CsrResult<'py>> {
    let src_slice = src.as_slice()?;
    let dst_slice = dst.as_slice()?;
    let weights_slice = weights.as_ref().map(|w| w.as_slice()).transpose()?;

    let csc = CscGraph::from_edges(src_slice, dst_slice, num_vertices, weights_slice)
        .map_err(|e| PyValueError::new_err(e.to_string()))?;

    let indptr = PyArray1::from_vec(py, csc.indptr).to_owned().into();
    let indices = PyArray1::from_vec(py, csc.indices).to_owned().into();
    let w = csc
        .weights
        .map(|ws| PyArray1::from_vec(py, ws).to_owned().into());

    Ok((indptr, indices, w))
}

/// Perform BFS traversal on a graph.
///
/// # Arguments
/// * `indptr` - CSR indptr array
/// * `indices` - CSR indices array
/// * `num_vertices` - Total number of vertices
/// * `sources` - Source vertex IDs (numpy array)
/// * `max_depth` - Optional maximum traversal depth
///
/// # Returns
/// Tuple of (distances, predecessors) as numpy arrays
#[pyfunction]
fn bfs_rust<'py>(
    py: Python<'py>,
    indptr: PyReadonlyArray1<i64>,
    indices: PyReadonlyArray1<i32>,
    num_vertices: usize,
    sources: PyReadonlyArray1<i32>,
    max_depth: Option<i32>,
) -> PyResult<BfsResult<'py>> {
    let csr = CsrGraph {
        indptr: indptr.to_vec()?,
        indices: indices.to_vec()?,
        weights: None,
        num_vertices,
    };

    let sources_slice = sources.as_slice()?;
    let result = if sources_slice.len() == 1 {
        bfs_sequential(&csr, sources_slice[0], max_depth)
    } else {
        bfs_parallel(&csr, sources_slice, max_depth)
    }
    .map_err(|e| PyValueError::new_err(e.to_string()))?;

    let distances: Py<PyArray1<i32>> = PyArray1::from_vec(py, result.distances).to_owned().into();
    let predecessors: Py<PyArray1<i32>> = PyArray1::from_vec(py, result.predecessors)
        .to_owned()
        .into();

    Ok((distances, predecessors))
}

/// Perform DFS traversal on a graph.
///
/// # Arguments
/// * `indptr` - CSR indptr array
/// * `indices` - CSR indices array
/// * `num_vertices` - Total number of vertices
/// * `source` - Source vertex ID
/// * `max_depth` - Optional maximum traversal depth
///
/// # Returns
/// Array of visited vertex IDs in DFS order
#[pyfunction]
fn dfs_rust<'py>(
    py: Python<'py>,
    indptr: PyReadonlyArray1<i64>,
    indices: PyReadonlyArray1<i32>,
    num_vertices: usize,
    source: i32,
    max_depth: Option<i32>,
) -> PyResult<Py<PyArray1<i32>>> {
    let csr = CsrGraph {
        indptr: indptr.to_vec()?,
        indices: indices.to_vec()?,
        weights: None,
        num_vertices,
    };

    let result = dfs(&csr, source, max_depth).map_err(|e| PyValueError::new_err(e.to_string()))?;

    Ok(PyArray1::from_vec(py, result).to_owned().into())
}

/// Compute PageRank scores using power iteration.
///
/// # Arguments
/// * `indptr` - CSR indptr array (int64)
/// * `indices` - CSR indices array (int32)
/// * `num_vertices` - Total number of vertices
/// * `alpha` - Damping factor (typically 0.85)
/// * `tol` - Convergence tolerance (default 1e-6)
/// * `max_iter` - Maximum iterations (default 100)
/// * `personalization` - Optional personalization vector (float64)
///
/// # Returns
/// PageRank scores as numpy array (float64)
#[pyfunction]
#[allow(clippy::too_many_arguments)]
fn pagerank_rust_py<'py>(
    py: Python<'py>,
    indptr: PyReadonlyArray1<i64>,
    indices: PyReadonlyArray1<i32>,
    num_vertices: usize,
    alpha: f64,
    tol: f64,
    max_iter: usize,
    personalization: Option<PyReadonlyArray1<f64>>,
) -> PyResult<Py<PyArray1<f64>>> {
    // Convert numpy arrays to Rust slices
    let indptr_vec = indptr.to_vec()?;
    let indices_vec = indices.to_vec()?;
    let personalization_vec = personalization.as_ref().map(|p| p.to_vec()).transpose()?;

    // Build CSR graph structure
    let csr = CsrGraph {
        indptr: indptr_vec,
        indices: indices_vec,
        weights: None,
        num_vertices,
    };

    // Compute PageRank (no GIL release needed for pure Rust computation)
    let scores = pagerank_rust(&csr, alpha, tol, max_iter, personalization_vec.as_deref())
        .map_err(|e| PyValueError::new_err(e.to_string()))?;

    // Convert results to numpy array
    Ok(PyArray1::from_vec(py, scores).to_owned().into())
}

/// Compute shortest paths using Dijkstra's algorithm.
///
/// # Arguments
/// * `indptr` - CSR indptr array (int64)
/// * `indices` - CSR indices array (int32)
/// * `num_vertices` - Total number of vertices
/// * `sources` - Source vertex IDs (int32)
/// * `weights` - Edge weights (float64)
///
/// # Returns
/// Tuple of (distances, predecessors) as numpy arrays
#[pyfunction]
fn dijkstra_rust_py<'py>(
    py: Python<'py>,
    indptr: PyReadonlyArray1<i64>,
    indices: PyReadonlyArray1<i32>,
    num_vertices: usize,
    sources: PyReadonlyArray1<i32>,
    weights: PyReadonlyArray1<f64>,
) -> PyResult<DijkstraResult<'py>> {
    // Convert numpy arrays to Rust types
    let indptr_vec = indptr.to_vec()?;
    let indices_vec = indices.to_vec()?;
    let sources_vec = sources.to_vec()?;
    let weights_vec = weights.to_vec()?;

    // Build CSR graph structure
    let csr = CsrGraph {
        indptr: indptr_vec,
        indices: indices_vec,
        weights: Some(weights_vec.clone()),
        num_vertices,
    };

    // Compute shortest paths (no GIL release needed for pure Rust computation)
    let (distances, predecessors) = dijkstra_rust(&csr, &sources_vec, &weights_vec)
        .map_err(|e| PyValueError::new_err(e.to_string()))?;

    // Convert results to numpy arrays
    let distances_arr: Py<PyArray1<f64>> = PyArray1::from_vec(py, distances).to_owned().into();
    let predecessors_arr: Py<PyArray1<i32>> =
        PyArray1::from_vec(py, predecessors).to_owned().into();

    Ok((distances_arr, predecessors_arr))
}

/// Find connected components using union-find algorithm.
///
/// # Arguments
/// * `sources` - Source vertex IDs (usize/uint64)
/// * `targets` - Target vertex IDs (usize/uint64)
/// * `num_vertices` - Total number of vertices
/// * `directed` - Whether graph is directed (for weak components)
///
/// # Returns
/// Component labels as numpy array (usize/uint64)
#[pyfunction]
fn connected_components_rust_py<'py>(
    py: Python<'py>,
    sources: PyReadonlyArray1<i64>,
    targets: PyReadonlyArray1<i64>,
    num_vertices: usize,
    directed: bool,
) -> PyResult<Py<PyArray1<i64>>> {
    // Convert numpy arrays to edge list
    let sources_vec = sources.to_vec()?;
    let targets_vec = targets.to_vec()?;

    if sources_vec.len() != targets_vec.len() {
        return Err(PyValueError::new_err(
            "Sources and targets must have same length",
        ));
    }

    let edges: Vec<(usize, usize)> = sources_vec
        .iter()
        .zip(targets_vec.iter())
        .map(|(&s, &t)| (s as usize, t as usize))
        .collect();

    // Compute components (no GIL release needed for pure Rust computation)
    let components = union_find_components(&edges, num_vertices, directed)
        .map_err(|e| PyValueError::new_err(e.to_string()))?;

    // Convert results to numpy array
    let components_i64: Vec<i64> = components.iter().map(|&c| c as i64).collect();
    Ok(PyArray1::from_vec(py, components_i64).to_owned().into())
}

/// Simple test function to verify module loading.
#[pyfunction]
fn graph_test() -> String {
    "Graph module loaded successfully".to_string()
}

/// Register graph functions with Python module.
pub fn register_graph_functions(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(graph_test, m)?)?;
    m.add_function(wrap_pyfunction!(build_csr_rust, m)?)?;
    m.add_function(wrap_pyfunction!(build_csc_rust, m)?)?;
    m.add_function(wrap_pyfunction!(bfs_rust, m)?)?;
    m.add_function(wrap_pyfunction!(dfs_rust, m)?)?;
    // Phase 3 algorithms
    m.add_function(wrap_pyfunction!(pagerank_rust_py, m)?)?;
    m.add_function(wrap_pyfunction!(dijkstra_rust_py, m)?)?;
    m.add_function(wrap_pyfunction!(connected_components_rust_py, m)?)?;
    Ok(())
}
