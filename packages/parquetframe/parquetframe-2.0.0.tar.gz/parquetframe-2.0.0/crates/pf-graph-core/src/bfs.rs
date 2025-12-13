//! Breadth-First Search (BFS) algorithms.
//!
//! Implements both sequential and parallel BFS for graph traversal.

use crate::{CsrGraph, GraphError, Result, VertexId};
use rayon::prelude::*;
use std::collections::VecDeque;

/// BFS traversal result
#[derive(Debug, Clone)]
pub struct BfsResult {
    /// Distance from source to each vertex (-1 = unreachable)
    pub distances: Vec<i32>,
    /// Predecessor in BFS tree (-1 = none/source)
    pub predecessors: Vec<i32>,
}

impl BfsResult {
    /// Get vertices reachable from sources
    pub fn reachable_vertices(&self) -> Vec<VertexId> {
        self.distances
            .iter()
            .enumerate()
            .filter(|(_, &d)| d >= 0)
            .map(|(v, _)| v as VertexId)
            .collect()
    }
}

/// Sequential BFS traversal
///
/// Performs breadth-first search from a single source vertex.
///
/// # Arguments
/// * `csr` - CSR graph structure
/// * `source` - Starting vertex ID
/// * `max_depth` - Optional maximum depth to traverse
///
/// # Returns
/// BfsResult containing distances and predecessors
///
/// # Errors
/// Returns error if source vertex is invalid
pub fn bfs_sequential(
    csr: &CsrGraph,
    source: VertexId,
    max_depth: Option<i32>,
) -> Result<BfsResult> {
    let n = csr.num_vertices;
    let max_d = max_depth.unwrap_or(i32::MAX);

    if source < 0 || source >= n as i32 {
        return Err(GraphError::InvalidVertex(source));
    }

    let mut distances = vec![-1; n];
    let mut predecessors = vec![-1; n];
    let mut queue = VecDeque::new();

    distances[source as usize] = 0;
    queue.push_back(source);

    while let Some(v) = queue.pop_front() {
        let depth = distances[v as usize];
        if depth >= max_d {
            continue;
        }

        for &u in csr.out_edges(v)? {
            if distances[u as usize] < 0 {
                distances[u as usize] = depth + 1;
                predecessors[u as usize] = v;
                queue.push_back(u);
            }
        }
    }

    Ok(BfsResult {
        distances,
        predecessors,
    })
}

/// Level-synchronous parallel BFS with Rayon
///
/// Performs parallel breadth-first search from multiple source vertices.
/// Uses level-synchronous approach where all vertices at depth k are
/// processed before any vertices at depth k+1.
///
/// # Arguments
/// * `csr` - CSR graph structure
/// * `sources` - Array of starting vertex IDs
/// * `max_depth` - Optional maximum depth to traverse
///
/// # Returns
/// BfsResult containing distances and predecessors
///
/// # Errors
/// Returns error if any source vertex is invalid
pub fn bfs_parallel(
    csr: &CsrGraph,
    sources: &[VertexId],
    max_depth: Option<i32>,
) -> Result<BfsResult> {
    let n = csr.num_vertices;
    let max_d = max_depth.unwrap_or(i32::MAX);

    // Initialize distances and predecessors
    let mut distances = vec![-1; n];
    let mut predecessors = vec![-1; n];

    // Initialize sources
    for &src in sources {
        if src < 0 || src >= n as i32 {
            return Err(GraphError::InvalidVertex(src));
        }
        distances[src as usize] = 0;
    }

    // Current and next frontiers
    let mut current_frontier: Vec<VertexId> = sources.to_vec();
    let mut depth = 0;

    while !current_frontier.is_empty() && depth < max_d {
        // Parallel frontier expansion
        let next_frontier: Vec<VertexId> = current_frontier
            .par_iter()
            .flat_map(|&v| {
                let neighbors = csr.out_edges(v).unwrap_or(&[]);
                neighbors
                    .iter()
                    .filter_map(|&u| {
                        if distances[u as usize] < 0 {
                            Some(u)
                        } else {
                            None
                        }
                    })
                    .collect::<Vec<_>>()
            })
            .collect();

        // Update distances and predecessors (sequential to avoid races)
        let mut deduped_next = Vec::new();
        for u in next_frontier {
            if distances[u as usize] < 0 {
                distances[u as usize] = depth + 1;
                deduped_next.push(u);
                // Find predecessor (any parent in current frontier)
                for &v in &current_frontier {
                    if let Ok(neighbors) = csr.out_edges(v) {
                        if neighbors.contains(&u) {
                            predecessors[u as usize] = v;
                            break;
                        }
                    }
                }
            }
        }

        current_frontier = deduped_next;
        depth += 1;
    }

    Ok(BfsResult {
        distances,
        predecessors,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bfs_simple() {
        let src = vec![0, 0, 1, 2];
        let dst = vec![1, 2, 2, 0];
        let csr = CsrGraph::from_edges(&src, &dst, 3, None).unwrap();

        let result = bfs_sequential(&csr, 0, None).unwrap();
        assert_eq!(result.distances, vec![0, 1, 1]);
        assert_eq!(result.reachable_vertices(), vec![0, 1, 2]);
    }

    #[test]
    fn test_bfs_max_depth() {
        let src = vec![0, 1, 2];
        let dst = vec![1, 2, 3];
        let csr = CsrGraph::from_edges(&src, &dst, 4, None).unwrap();

        let result = bfs_sequential(&csr, 0, Some(2)).unwrap();
        assert_eq!(result.distances, vec![0, 1, 2, -1]);
    }

    #[test]
    fn test_bfs_unreachable() {
        // Disconnected graph: 0->1, 2->3
        let src = vec![0, 2];
        let dst = vec![1, 3];
        let csr = CsrGraph::from_edges(&src, &dst, 4, None).unwrap();

        let result = bfs_sequential(&csr, 0, None).unwrap();
        assert_eq!(result.distances, vec![0, 1, -1, -1]);
        assert_eq!(result.predecessors, vec![-1, 0, -1, -1]);
    }

    #[test]
    fn test_bfs_parallel_multi_source() {
        let src = vec![0, 1, 2];
        let dst = vec![1, 2, 3];
        let csr = CsrGraph::from_edges(&src, &dst, 4, None).unwrap();

        let sources = vec![0, 2];
        let result = bfs_parallel(&csr, &sources, None).unwrap();

        // All vertices reachable from either source
        assert_eq!(result.distances, vec![0, 1, 0, 1]);
        assert_eq!(result.reachable_vertices(), vec![0, 1, 2, 3]);
    }

    #[test]
    fn test_bfs_invalid_source() {
        let src = vec![0, 1];
        let dst = vec![1, 0];
        let csr = CsrGraph::from_edges(&src, &dst, 2, None).unwrap();

        let result = bfs_sequential(&csr, 5, None);
        assert!(result.is_err());
    }

    #[test]
    fn test_bfs_self_loop() {
        let src = vec![0, 0];
        let dst = vec![0, 1];
        let csr = CsrGraph::from_edges(&src, &dst, 2, None).unwrap();

        let result = bfs_sequential(&csr, 0, None).unwrap();
        assert_eq!(result.distances, vec![0, 1]);
    }
}
