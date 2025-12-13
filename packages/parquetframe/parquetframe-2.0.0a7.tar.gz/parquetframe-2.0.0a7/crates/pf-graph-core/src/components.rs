//! Connected components algorithm using union-find data structure.
//!
//! This module implements weakly connected components for both directed and
//! undirected graphs using an efficient union-find (disjoint-set) data structure
//! with path compression and union by rank optimizations.

use crate::{GraphError, Result};
use rayon::prelude::*;

/// Union-Find data structure for connected components.
///
/// This implementation uses path compression during find operations
/// and union by rank to maintain balanced trees, achieving near-constant
/// amortized time complexity.
struct UnionFind {
    /// Parent pointers for each vertex
    parent: Vec<usize>,
    /// Rank (approximate tree height) for union by rank
    rank: Vec<usize>,
}

impl UnionFind {
    /// Create a new Union-Find structure with `n` vertices.
    ///
    /// Initially, each vertex is in its own component.
    fn new(n: usize) -> Self {
        UnionFind {
            parent: (0..n).collect(),
            rank: vec![0; n],
        }
    }

    /// Find the root of the component containing vertex `x` with path compression.
    ///
    /// Path compression flattens the tree structure during traversal,
    /// making future operations faster.
    fn find(&mut self, x: usize) -> usize {
        if self.parent[x] != x {
            self.parent[x] = self.find(self.parent[x]); // Path compression
        }
        self.parent[x]
    }

    /// Unite the components containing vertices `x` and `y`.
    ///
    /// Uses union by rank to keep trees balanced.
    fn union(&mut self, x: usize, y: usize) {
        let root_x = self.find(x);
        let root_y = self.find(y);

        if root_x == root_y {
            return; // Already in same component
        }

        // Union by rank: attach smaller tree under larger tree
        match self.rank[root_x].cmp(&self.rank[root_y]) {
            std::cmp::Ordering::Less => {
                self.parent[root_x] = root_y;
            }
            std::cmp::Ordering::Greater => {
                self.parent[root_y] = root_x;
            }
            std::cmp::Ordering::Equal => {
                self.parent[root_y] = root_x;
                self.rank[root_x] += 1;
            }
        }
    }
}

/// Find connected components using union-find algorithm.
///
/// For directed graphs, computes weakly connected components (treating edges as undirected).
/// For undirected graphs, computes standard connected components.
///
/// # Arguments
///
/// * `edges` - Slice of edge tuples (source, target) where vertices are 0-indexed
/// * `num_vertices` - Total number of vertices in the graph
/// * `directed` - Whether the graph is directed (for weak components vs strong)
///
/// # Returns
///
/// A vector of component labels where `result[v]` is the component ID of vertex `v`.
/// Component IDs are consecutive integers starting from 0.
///
/// # Errors
///
/// Returns `GraphError::InvalidVertex` if any edge references a vertex >= `num_vertices`.
/// Returns `GraphError::InvalidInput` if `num_vertices` is 0.
///
/// # Time Complexity
///
/// O(E × α(V)) where E is the number of edges, V is the number of vertices,
/// and α is the inverse Ackermann function (effectively constant).
///
/// # Examples
///
/// ```
/// use pf_graph_core::union_find_components;
///
/// // Simple graph with two components: (0-1-2) and (3-4)
/// let edges = vec![(0, 1), (1, 2), (3, 4)];
/// let components = union_find_components(&edges, 5, false).unwrap();
///
/// assert_eq!(components[0], components[1]); // 0 and 1 in same component
/// assert_eq!(components[1], components[2]); // 1 and 2 in same component
/// assert_ne!(components[0], components[3]); // 0 and 3 in different components
/// ```
pub fn union_find_components(
    edges: &[(usize, usize)],
    num_vertices: usize,
    directed: bool,
) -> Result<Vec<usize>> {
    // Validate inputs
    if num_vertices == 0 {
        return Err(GraphError::InvalidInput(
            "Cannot compute components on empty graph".to_string(),
        ));
    }

    // Validate that all edges reference valid vertices
    for &(src, dst) in edges {
        if src >= num_vertices {
            return Err(GraphError::InvalidVertex(src as i32));
        }
        if dst >= num_vertices {
            return Err(GraphError::InvalidVertex(dst as i32));
        }
    }

    // Initialize union-find structure
    let mut uf = UnionFind::new(num_vertices);

    // Process all edges
    for &(src, dst) in edges {
        uf.union(src, dst);

        // For directed graphs computing weak components, we treat edges as undirected
        // This is implicit in union-find (union is symmetric), but we make it explicit
        // by noting that we don't need to add the reverse edge
        if !directed {
            // For undirected graphs, union operation is already symmetric
            // so we don't need additional processing
        }
    }

    // Find final component representatives and create compact component IDs
    // We do this in parallel for better performance on large graphs
    let roots: Vec<usize> = (0..num_vertices)
        .into_par_iter()
        .map(|v| {
            // Note: We can't call uf.find(v) in parallel because it mutates uf
            // Instead, we'll do a two-pass approach: first collect roots, then renumber
            let mut current = v;
            let mut path = Vec::new();

            // Follow parent pointers without mutation
            while uf.parent[current] != current {
                path.push(current);
                current = uf.parent[current];
            }

            current // Return the root
        })
        .collect();

    // Create mapping from roots to consecutive component IDs
    let mut root_to_component: std::collections::HashMap<usize, usize> =
        std::collections::HashMap::new();
    let mut next_component_id = 0;

    for &root in &roots {
        root_to_component.entry(root).or_insert_with(|| {
            let id = next_component_id;
            next_component_id += 1;
            id
        });
    }

    // Assign component IDs to all vertices
    let component_labels: Vec<usize> = roots
        .into_iter()
        .map(|root| *root_to_component.get(&root).unwrap())
        .collect();

    Ok(component_labels)
}

/// Find connected components with parallel edge processing for very large graphs.
///
/// This is an experimental variant that attempts to parallelize the union operations
/// using a more sophisticated approach. For most graphs, the standard `union_find_components`
/// is sufficient and may be faster due to lower overhead.
///
/// # Note
///
/// This function is currently marked as dead code because union-find with path compression
/// is inherently sequential during the union operations. The parallel variant doesn't
/// provide significant benefits and adds complexity.
#[allow(dead_code)]
fn union_find_components_parallel(
    edges: &[(usize, usize)],
    num_vertices: usize,
    _directed: bool,
) -> Result<Vec<usize>> {
    if num_vertices == 0 {
        return Err(GraphError::InvalidInput(
            "Cannot compute components on empty graph".to_string(),
        ));
    }

    // For very large graphs, we could use parallel label propagation instead
    // of union-find, but that requires multiple iterations

    // For now, fall back to sequential union-find
    union_find_components(edges, num_vertices, _directed)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_components_empty_graph() {
        // Graph with no edges - each vertex is its own component
        let edges: Vec<(usize, usize)> = vec![];
        let components = union_find_components(&edges, 5, false).unwrap();

        assert_eq!(components.len(), 5);
        // Each vertex should be in a unique component
        let unique_components: std::collections::HashSet<_> = components.iter().collect();
        assert_eq!(unique_components.len(), 5);
    }

    #[test]
    fn test_components_single_vertex() {
        // Single vertex with no edges
        let edges: Vec<(usize, usize)> = vec![];
        let components = union_find_components(&edges, 1, false).unwrap();

        assert_eq!(components.len(), 1);
        assert_eq!(components[0], 0);
    }

    #[test]
    fn test_components_disconnected_components() {
        // Two separate components: (0-1-2) and (3-4)
        let edges = vec![(0, 1), (1, 2), (3, 4)];
        let components = union_find_components(&edges, 5, false).unwrap();

        assert_eq!(components.len(), 5);

        // Vertices 0, 1, 2 should be in same component
        assert_eq!(components[0], components[1]);
        assert_eq!(components[1], components[2]);

        // Vertices 3, 4 should be in same component
        assert_eq!(components[3], components[4]);

        // But these two components should be different
        assert_ne!(components[0], components[3]);
    }

    #[test]
    fn test_components_single_component() {
        // All vertices connected: 0-1-2-3-4 (linear chain)
        let edges = vec![(0, 1), (1, 2), (2, 3), (3, 4)];
        let components = union_find_components(&edges, 5, false).unwrap();

        assert_eq!(components.len(), 5);

        // All vertices should be in the same component
        let unique_components: std::collections::HashSet<_> = components.iter().collect();
        assert_eq!(unique_components.len(), 1);
    }

    #[test]
    fn test_components_directed_weak() {
        // Directed graph: 0->1, 2->1, 3->4
        // Weak components: (0,1,2) and (3,4)
        let edges = vec![(0, 1), (2, 1), (3, 4)];
        let components = union_find_components(&edges, 5, true).unwrap();

        assert_eq!(components.len(), 5);

        // In weak components, 0, 1, 2 should be connected
        assert_eq!(components[0], components[1]);
        assert_eq!(components[1], components[2]);

        // 3 and 4 should be connected
        assert_eq!(components[3], components[4]);

        // But separate from first component
        assert_ne!(components[0], components[3]);
    }

    #[test]
    fn test_components_self_loops() {
        // Graph with self-loops: 0-0, 1-1, 0-1
        let edges = vec![(0, 0), (1, 1), (0, 1)];
        let components = union_find_components(&edges, 3, false).unwrap();

        assert_eq!(components.len(), 3);

        // 0 and 1 should be in same component
        assert_eq!(components[0], components[1]);

        // 2 should be in its own component
        assert_ne!(components[0], components[2]);
    }

    #[test]
    fn test_components_parallel_edges() {
        // Multiple edges between same vertices
        let edges = vec![(0, 1), (0, 1), (0, 1), (1, 2)];
        let components = union_find_components(&edges, 3, false).unwrap();

        assert_eq!(components.len(), 3);

        // All should be in same component
        let unique_components: std::collections::HashSet<_> = components.iter().collect();
        assert_eq!(unique_components.len(), 1);
    }

    #[test]
    fn test_components_large_graph() {
        // Create a larger graph with multiple components
        // Component 1: 0-99 (linear chain)
        let mut edges = Vec::new();
        for i in 0..99 {
            edges.push((i, i + 1));
        }

        // Component 2: 100-199 (linear chain)
        for i in 100..199 {
            edges.push((i, i + 1));
        }

        let components = union_find_components(&edges, 200, false).unwrap();

        assert_eq!(components.len(), 200);

        // First 100 vertices should be in same component
        let comp0 = components[0];
        for component in components.iter().take(100).skip(1) {
            assert_eq!(*component, comp0);
        }

        // Next 100 vertices should be in same component (but different from first)
        let comp100 = components[100];
        assert_ne!(comp0, comp100);
        for component in components.iter().skip(101).take(99) {
            assert_eq!(*component, comp100);
        }
    }

    #[test]
    fn test_components_star_graph() {
        // Star graph: center vertex 0 connected to all others
        let edges: Vec<(usize, usize)> = (1..10).map(|i| (0, i)).collect();
        let components = union_find_components(&edges, 10, false).unwrap();

        assert_eq!(components.len(), 10);

        // All vertices should be in same component
        let unique_components: std::collections::HashSet<_> = components.iter().collect();
        assert_eq!(unique_components.len(), 1);
    }

    #[test]
    fn test_components_chain_graph() {
        // Linear chain: 0-1-2-3-4-5-6-7-8-9
        let edges: Vec<(usize, usize)> = (0..9).map(|i| (i, i + 1)).collect();
        let components = union_find_components(&edges, 10, false).unwrap();

        assert_eq!(components.len(), 10);

        // All vertices should be in same component
        let unique_components: std::collections::HashSet<_> = components.iter().collect();
        assert_eq!(unique_components.len(), 1);
    }

    #[test]
    fn test_components_invalid_vertex() {
        // Edge references vertex 10 but only 5 vertices exist
        let edges = vec![(0, 1), (1, 10)];
        let result = union_find_components(&edges, 5, false);

        assert!(result.is_err());
        match result {
            Err(GraphError::InvalidVertex(v)) => assert_eq!(v, 10),
            _ => panic!("Expected InvalidVertex error"),
        }
    }

    #[test]
    fn test_components_zero_vertices() {
        // Cannot create components for graph with 0 vertices
        let edges: Vec<(usize, usize)> = vec![];
        let result = union_find_components(&edges, 0, false);

        assert!(result.is_err());
        match result {
            Err(GraphError::InvalidInput(_)) => {}
            _ => panic!("Expected InvalidInput error"),
        }
    }

    #[test]
    fn test_union_find_path_compression() {
        // Test that path compression works correctly
        let mut uf = UnionFind::new(10);

        // Create a long chain: 0 <- 1 <- 2 <- 3 <- 4
        uf.union(0, 1);
        uf.union(1, 2);
        uf.union(2, 3);
        uf.union(3, 4);

        // After path compression, all should point directly to root
        let root = uf.find(4);
        assert_eq!(uf.find(0), root);
        assert_eq!(uf.find(1), root);
        assert_eq!(uf.find(2), root);
        assert_eq!(uf.find(3), root);
    }

    #[test]
    fn test_union_find_union_by_rank() {
        // Test that union by rank maintains balanced trees
        let mut uf = UnionFind::new(10);

        // Create two separate trees
        uf.union(0, 1);
        uf.union(0, 2);

        uf.union(5, 6);
        uf.union(5, 7);
        uf.union(5, 8);

        // Union the two trees
        uf.union(0, 5);

        // All should be in same component
        let root = uf.find(0);
        assert_eq!(uf.find(1), root);
        assert_eq!(uf.find(2), root);
        assert_eq!(uf.find(5), root);
        assert_eq!(uf.find(6), root);
        assert_eq!(uf.find(7), root);
        assert_eq!(uf.find(8), root);
    }
}
