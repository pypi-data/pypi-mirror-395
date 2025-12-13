//! Depth-First Search (DFS) algorithm.
//!
//! Implements iterative DFS using an explicit stack.

use crate::{CsrGraph, GraphError, Result, VertexId};

/// DFS traversal result (visited vertices in order)
pub type DfsResult = Vec<VertexId>;

/// Iterative DFS using explicit stack
///
/// Performs depth-first search from a source vertex using an iterative
/// approach with an explicit stack (no recursion).
///
/// # Arguments
/// * `csr` - CSR graph structure
/// * `source` - Starting vertex ID
/// * `max_depth` - Optional maximum depth to traverse
///
/// # Returns
/// Vector of visited vertex IDs in DFS order
///
/// # Errors
/// Returns error if source vertex is invalid
pub fn dfs(csr: &CsrGraph, source: VertexId, max_depth: Option<i32>) -> Result<DfsResult> {
    let n = csr.num_vertices;
    let max_d = max_depth.unwrap_or(i32::MAX);

    if source < 0 || source >= n as i32 {
        return Err(GraphError::InvalidVertex(source));
    }

    let mut visited = vec![false; n];
    let mut result = Vec::new();
    let mut stack = vec![(source, 0)]; // (vertex, depth)

    while let Some((v, depth)) = stack.pop() {
        if visited[v as usize] || depth > max_d {
            continue;
        }

        visited[v as usize] = true;
        result.push(v);

        // Push neighbors to stack in reverse order (to maintain left-to-right)
        for &u in csr.out_edges(v)?.iter().rev() {
            if !visited[u as usize] {
                stack.push((u, depth + 1));
            }
        }
    }

    Ok(result)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dfs_simple() {
        let src = vec![0, 0, 1, 2];
        let dst = vec![1, 2, 2, 0];
        let csr = CsrGraph::from_edges(&src, &dst, 3, None).unwrap();

        let result = dfs(&csr, 0, None).unwrap();
        assert!(result.contains(&0));
        assert!(result.contains(&1));
        assert!(result.contains(&2));
        assert_eq!(result.len(), 3);
    }

    #[test]
    fn test_dfs_max_depth() {
        // Linear graph: 0 -> 1 -> 2 -> 3
        let src = vec![0, 1, 2];
        let dst = vec![1, 2, 3];
        let csr = CsrGraph::from_edges(&src, &dst, 4, None).unwrap();

        let result = dfs(&csr, 0, Some(2)).unwrap();
        // Should visit 0, 1, 2 but not 3 (depth 3)
        assert!(result.contains(&0));
        assert!(result.contains(&1));
        assert!(result.contains(&2));
        assert!(!result.contains(&3));
    }

    #[test]
    fn test_dfs_tree() {
        // Tree: 0 -> {1, 2}, 1 -> {3, 4}
        let src = vec![0, 0, 1, 1];
        let dst = vec![1, 2, 3, 4];
        let csr = CsrGraph::from_edges(&src, &dst, 5, None).unwrap();

        let result = dfs(&csr, 0, None).unwrap();
        assert_eq!(result.len(), 5);
        assert_eq!(result[0], 0); // Root first
    }

    #[test]
    fn test_dfs_disconnected() {
        // Disconnected: 0 -> 1, 2 -> 3
        let src = vec![0, 2];
        let dst = vec![1, 3];
        let csr = CsrGraph::from_edges(&src, &dst, 4, None).unwrap();

        let result = dfs(&csr, 0, None).unwrap();
        // Should only visit component containing 0
        assert_eq!(result.len(), 2);
        assert!(result.contains(&0));
        assert!(result.contains(&1));
        assert!(!result.contains(&2));
        assert!(!result.contains(&3));
    }

    #[test]
    fn test_dfs_invalid_source() {
        let src = vec![0, 1];
        let dst = vec![1, 0];
        let csr = CsrGraph::from_edges(&src, &dst, 2, None).unwrap();

        let result = dfs(&csr, 5, None);
        assert!(result.is_err());
    }

    #[test]
    fn test_dfs_cycle() {
        // Cycle: 0 -> 1 -> 2 -> 0
        let src = vec![0, 1, 2];
        let dst = vec![1, 2, 0];
        let csr = CsrGraph::from_edges(&src, &dst, 3, None).unwrap();

        let result = dfs(&csr, 0, None).unwrap();
        // Should visit all vertices exactly once
        assert_eq!(result.len(), 3);
        assert!(result.contains(&0));
        assert!(result.contains(&1));
        assert!(result.contains(&2));
    }
}
