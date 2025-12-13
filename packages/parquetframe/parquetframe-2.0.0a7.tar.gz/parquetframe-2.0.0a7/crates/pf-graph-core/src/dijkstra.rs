//! Dijkstra's shortest path algorithm implementation.
//!
//! This module implements Dijkstra's algorithm for finding shortest paths in
//! weighted graphs with non-negative edge weights using a binary heap priority queue.

use crate::{CsrGraph, GraphError, Result, VertexId, Weight};
use std::cmp::Ordering;
use std::collections::BinaryHeap;

/// State for priority queue in Dijkstra's algorithm.
///
/// The ordering is reversed so BinaryHeap acts as a min-heap.
#[derive(Copy, Clone, PartialEq)]
struct State {
    distance: Weight,
    vertex: VertexId,
}

impl Eq for State {}

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        // Reverse ordering for min-heap behavior
        other
            .distance
            .partial_cmp(&self.distance)
            .unwrap_or(Ordering::Equal)
            .then_with(|| self.vertex.cmp(&other.vertex))
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

/// Compute shortest paths using Dijkstra's algorithm.
///
/// Dijkstra's algorithm finds the shortest paths from source vertices to all
/// other vertices in a graph with non-negative edge weights.
///
/// # Arguments
///
/// * `csr` - The graph in CSR format
/// * `sources` - Array of source vertex IDs (single or multiple sources)
/// * `weights` - Edge weights (must have same length as number of edges in CSR)
///
/// # Returns
///
/// A tuple of (distances, predecessors):
/// - distances: `Vec<f64>` - Distance from nearest source to each vertex (inf for unreachable)
/// - predecessors: `Vec<i32>` - Previous vertex in shortest path (-1 for sources/unreachable)
///
/// # Errors
///
/// Returns `GraphError::InvalidInput` if:
/// - Sources array is empty
/// - Any source vertex is out of range
/// - Weights array length doesn't match number of edges
/// - Any weight is negative
///
/// # Example
///
/// ```
/// use pf_graph_core::{CsrGraph, dijkstra_rust};
///
/// let src = vec![0, 0, 1];
/// let dst = vec![1, 2, 2];
/// let weights = vec![1.0, 4.0, 2.0];
/// let csr = CsrGraph::from_edges(&src, &dst, 3, Some(&weights)).unwrap();
///
/// let (distances, predecessors) = dijkstra_rust(&csr, &[0], &weights).unwrap();
/// assert_eq!(distances[2], 3.0); // 0 -> 1 -> 2 with distance 1 + 2 = 3
/// ```
pub fn dijkstra_rust(
    csr: &CsrGraph,
    sources: &[VertexId],
    weights: &[Weight],
) -> Result<(Vec<f64>, Vec<i32>)> {
    let n = csr.num_vertices;

    // Validate inputs
    if sources.is_empty() {
        return Err(GraphError::InvalidInput(
            "At least one source vertex required".to_string(),
        ));
    }

    // Validate source vertices
    for &src in sources {
        if src < 0 || src >= n as i32 {
            return Err(GraphError::InvalidVertex(src));
        }
    }

    // Validate weights length
    let num_edges = csr.num_edges();
    if weights.len() != num_edges {
        return Err(GraphError::InvalidInput(format!(
            "Weights length {} doesn't match number of edges {}",
            weights.len(),
            num_edges
        )));
    }

    // Check for negative weights
    for &w in weights {
        if w < 0.0 {
            return Err(GraphError::InvalidInput(format!(
                "Dijkstra's algorithm requires non-negative weights, found {}",
                w
            )));
        }
    }

    // Initialize distances and predecessors
    let mut distances = vec![f64::INFINITY; n];
    let mut predecessors = vec![-1; n];
    let mut visited = vec![false; n];

    // Build edge index map for weight lookups
    // Map (src, dst) -> edge_index in the CSR structure
    let mut edge_index_map: Vec<Vec<(VertexId, usize)>> = vec![Vec::new(); n];
    let mut edge_idx = 0;
    for (v, edge_list) in edge_index_map.iter_mut().enumerate() {
        let start = csr.indptr[v] as usize;
        let end = csr.indptr[v + 1] as usize;
        for &dst in &csr.indices[start..end] {
            edge_list.push((dst, edge_idx));
            edge_idx += 1;
        }
    }

    // Priority queue for Dijkstra
    let mut heap = BinaryHeap::new();

    // Initialize sources
    for &src in sources {
        distances[src as usize] = 0.0;
        heap.push(State {
            distance: 0.0,
            vertex: src,
        });
    }

    // Main Dijkstra loop
    while let Some(State { distance, vertex }) = heap.pop() {
        let v = vertex as usize;

        // Skip if already visited
        if visited[v] {
            continue;
        }
        visited[v] = true;

        // Skip if this is an outdated entry
        if distance > distances[v] {
            continue;
        }

        // Relax edges from current vertex
        for &(neighbor, edge_idx) in &edge_index_map[v] {
            let u = neighbor as usize;
            let edge_weight = weights[edge_idx];
            let new_distance = distances[v] + edge_weight;

            // Update if we found a shorter path
            if new_distance < distances[u] {
                distances[u] = new_distance;
                predecessors[u] = vertex;
                heap.push(State {
                    distance: new_distance,
                    vertex: neighbor,
                });
            }
        }
    }

    Ok((distances, predecessors))
}

#[cfg(test)]
mod tests {
    use super::*;

    fn assert_approx_eq(a: f64, b: f64, tol: f64) {
        assert!(
            (a - b).abs() < tol,
            "Values differ: {} vs {} (diff: {})",
            a,
            b,
            (a - b).abs()
        );
    }

    #[test]
    fn test_dijkstra_simple_path() {
        // Simple path: 0 -> 1 -> 2 with weights 1.0 and 2.0
        let src = vec![0, 1];
        let dst = vec![1, 2];
        let weights = vec![1.0, 2.0];
        let csr = CsrGraph::from_edges(&src, &dst, 3, Some(&weights)).unwrap();

        let (distances, predecessors) =
            dijkstra_rust(&csr, &[0], csr.weights.as_ref().unwrap()).unwrap();

        assert_approx_eq(distances[0], 0.0, 1e-9);
        assert_approx_eq(distances[1], 1.0, 1e-9);
        assert_approx_eq(distances[2], 3.0, 1e-9);

        assert_eq!(predecessors[0], -1); // Source
        assert_eq!(predecessors[1], 0);
        assert_eq!(predecessors[2], 1);
    }

    #[test]
    fn test_dijkstra_multiple_paths() {
        // Graph with multiple paths: 0 -> 1 (weight 4), 0 -> 2 (weight 1), 2 -> 1 (weight 2)
        // Shortest path to 1 is 0 -> 2 -> 1 with distance 3
        let src = vec![0, 0, 2];
        let dst = vec![1, 2, 1];
        let weights = vec![4.0, 1.0, 2.0];
        let csr = CsrGraph::from_edges(&src, &dst, 3, Some(&weights)).unwrap();

        let (distances, _) = dijkstra_rust(&csr, &[0], csr.weights.as_ref().unwrap()).unwrap();

        assert_approx_eq(distances[0], 0.0, 1e-9);
        assert_approx_eq(distances[1], 3.0, 1e-9); // Via vertex 2
        assert_approx_eq(distances[2], 1.0, 1e-9);
    }

    #[test]
    fn test_dijkstra_multi_source() {
        // Graph: 0 -> 2 (weight 5), 1 -> 2 (weight 1)
        // With sources [0, 1], vertex 2 should be reached from source 1
        let src = vec![0, 1];
        let dst = vec![2, 2];
        let weights = vec![5.0, 1.0];
        let csr = CsrGraph::from_edges(&src, &dst, 3, Some(&weights)).unwrap();

        let (distances, predecessors) =
            dijkstra_rust(&csr, &[0, 1], csr.weights.as_ref().unwrap()).unwrap();

        assert_approx_eq(distances[0], 0.0, 1e-9);
        assert_approx_eq(distances[1], 0.0, 1e-9);
        assert_approx_eq(distances[2], 1.0, 1e-9); // Reached from source 1
        assert_eq!(predecessors[2], 1); // Predecessor is source 1
    }

    #[test]
    fn test_dijkstra_disconnected() {
        // Disconnected graph: 0 -> 1, 2 isolated
        let src = vec![0];
        let dst = vec![1];
        let weights = vec![1.0];
        let csr = CsrGraph::from_edges(&src, &dst, 3, Some(&weights)).unwrap();

        let (distances, predecessors) =
            dijkstra_rust(&csr, &[0], csr.weights.as_ref().unwrap()).unwrap();

        assert_approx_eq(distances[0], 0.0, 1e-9);
        assert_approx_eq(distances[1], 1.0, 1e-9);
        assert!(distances[2].is_infinite()); // Unreachable
        assert_eq!(predecessors[2], -1); // No predecessor
    }

    #[test]
    fn test_dijkstra_single_vertex() {
        // Single vertex graph with self-loop
        let src = vec![0];
        let dst = vec![0];
        let weights = vec![1.0];
        let csr = CsrGraph::from_edges(&src, &dst, 1, Some(&weights)).unwrap();

        let (distances, predecessors) =
            dijkstra_rust(&csr, &[0], csr.weights.as_ref().unwrap()).unwrap();

        assert_approx_eq(distances[0], 0.0, 1e-9);
        assert_eq!(predecessors[0], -1);
    }

    #[test]
    fn test_dijkstra_triangle() {
        // Triangle: 0 -> 1 (2), 1 -> 2 (3), 0 -> 2 (10)
        // Shortest path 0 -> 2 is via 1 with distance 5
        let src = vec![0, 1, 0];
        let dst = vec![1, 2, 2];
        let weights = vec![2.0, 3.0, 10.0];
        let csr = CsrGraph::from_edges(&src, &dst, 3, Some(&weights)).unwrap();

        let (distances, predecessors) =
            dijkstra_rust(&csr, &[0], csr.weights.as_ref().unwrap()).unwrap();

        assert_approx_eq(distances[0], 0.0, 1e-9);
        assert_approx_eq(distances[1], 2.0, 1e-9);
        assert_approx_eq(distances[2], 5.0, 1e-9); // Via vertex 1
        assert_eq!(predecessors[1], 0);
        assert_eq!(predecessors[2], 1); // Came from 1, not directly from 0
    }

    #[test]
    fn test_dijkstra_zero_weights() {
        // Graph with zero-weight edges: 0 -> 1 (0), 1 -> 2 (0)
        let src = vec![0, 1];
        let dst = vec![1, 2];
        let weights = vec![0.0, 0.0];
        let csr = CsrGraph::from_edges(&src, &dst, 3, Some(&weights)).unwrap();

        let (distances, _) = dijkstra_rust(&csr, &[0], csr.weights.as_ref().unwrap()).unwrap();

        assert_approx_eq(distances[0], 0.0, 1e-9);
        assert_approx_eq(distances[1], 0.0, 1e-9);
        assert_approx_eq(distances[2], 0.0, 1e-9);
    }

    #[test]
    fn test_dijkstra_negative_weights_error() {
        // Graph with negative weight - should error
        let src = vec![0, 1];
        let dst = vec![1, 2];
        let weights = vec![1.0, -2.0];
        let csr = CsrGraph::from_edges(&src, &dst, 3, Some(&weights)).unwrap();

        let result = dijkstra_rust(&csr, &[0], &weights);
        assert!(result.is_err());
        assert!(matches!(result, Err(GraphError::InvalidInput(_))));
    }

    #[test]
    fn test_dijkstra_empty_sources() {
        let src = vec![0, 1];
        let dst = vec![1, 2];
        let weights = vec![1.0, 2.0];
        let csr = CsrGraph::from_edges(&src, &dst, 3, Some(&weights)).unwrap();

        let result = dijkstra_rust(&csr, &[], &weights);
        assert!(result.is_err());
        assert!(matches!(result, Err(GraphError::InvalidInput(_))));
    }

    #[test]
    fn test_dijkstra_invalid_source() {
        let src = vec![0, 1];
        let dst = vec![1, 2];
        let weights = vec![1.0, 2.0];
        let csr = CsrGraph::from_edges(&src, &dst, 3, Some(&weights)).unwrap();

        let result = dijkstra_rust(&csr, &[5], &weights);
        assert!(result.is_err());
        assert!(matches!(result, Err(GraphError::InvalidVertex(_))));
    }

    #[test]
    fn test_dijkstra_wrong_weights_length() {
        let src = vec![0, 1];
        let dst = vec![1, 2];
        let weights = vec![1.0]; // Wrong length
        let csr = CsrGraph::from_edges(&src, &dst, 3, Some(&[1.0, 2.0])).unwrap();

        let result = dijkstra_rust(&csr, &[0], &weights);
        assert!(result.is_err());
        assert!(matches!(result, Err(GraphError::InvalidInput(_))));
    }

    #[test]
    fn test_dijkstra_complex_graph() {
        // More complex graph with multiple shortest paths
        // 0 -> 1 (1), 0 -> 2 (4), 1 -> 2 (2), 1 -> 3 (5), 2 -> 3 (1)
        // Shortest paths: 0->0 (0), 0->1 (1), 0->2 (3), 0->3 (4)
        let src = vec![0, 0, 1, 1, 2];
        let dst = vec![1, 2, 2, 3, 3];
        let weights = vec![1.0, 4.0, 2.0, 5.0, 1.0];
        let csr = CsrGraph::from_edges(&src, &dst, 4, Some(&weights)).unwrap();

        let (distances, _) = dijkstra_rust(&csr, &[0], csr.weights.as_ref().unwrap()).unwrap();

        assert_approx_eq(distances[0], 0.0, 1e-9);
        assert_approx_eq(distances[1], 1.0, 1e-9);
        assert_approx_eq(distances[2], 3.0, 1e-9); // Via 1
        assert_approx_eq(distances[3], 4.0, 1e-9); // Via 2
    }
}
