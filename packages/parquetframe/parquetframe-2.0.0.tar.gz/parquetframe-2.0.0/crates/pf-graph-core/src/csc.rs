//! Compressed Sparse Column (CSC) graph representation.
//!
//! CSC format is optimized for fast incoming edge queries - given a vertex,
//! quickly find all vertices that connect to it.

use crate::{EdgeIndex, GraphError, Result, VertexId, Weight};
use rayon::prelude::*;

/// Compressed Sparse Column (CSC) graph representation
///
/// Efficient for iterating incoming edges to vertices.
/// Uses three arrays:
/// - `indptr`: Boundary pointers for each vertex
/// - `indices`: Source vertex IDs for each edge
/// - `weights`: Optional edge weights
#[derive(Debug, Clone)]
pub struct CscGraph {
    /// Boundary pointers: indptr\[v\] to indptr\[v+1\] are edges to vertex v
    pub indptr: Vec<EdgeIndex>,
    /// Source vertex IDs for each edge
    pub indices: Vec<VertexId>,
    /// Optional edge weights
    pub weights: Option<Vec<Weight>>,
    /// Number of vertices
    pub num_vertices: usize,
}

impl CscGraph {
    /// Build CSC from edge lists using parallel sort
    ///
    /// # Arguments
    /// * `src` - Source vertex IDs
    /// * `dst` - Destination vertex IDs
    /// * `num_vertices` - Total number of vertices in graph
    /// * `weights` - Optional edge weights
    ///
    /// # Returns
    /// CSC graph structure
    ///
    /// # Errors
    /// Returns error if array lengths mismatch or vertex IDs are invalid
    pub fn from_edges(
        src: &[VertexId],
        dst: &[VertexId],
        num_vertices: usize,
        weights: Option<&[Weight]>,
    ) -> Result<Self> {
        if src.len() != dst.len() {
            return Err(GraphError::MismatchedLengths(format!(
                "src.len()={} != dst.len()={}",
                src.len(),
                dst.len()
            )));
        }

        if let Some(w) = weights {
            if w.len() != src.len() {
                return Err(GraphError::MismatchedLengths(format!(
                    "weights.len()={} != edges.len()={}",
                    w.len(),
                    src.len()
                )));
            }
        }

        let num_edges = src.len();

        // Handle empty graph
        if num_edges == 0 {
            return Ok(CscGraph {
                indptr: vec![0; num_vertices + 1],
                indices: Vec::new(),
                weights: None,
                num_vertices,
            });
        }

        // Create edge tuples with optional weights (parallel)
        let mut edges: Vec<(VertexId, VertexId, Option<Weight>)> = (0..num_edges)
            .into_par_iter()
            .map(|i| {
                let w = weights.map(|ws| ws[i]);
                (src[i], dst[i], w)
            })
            .collect();

        // Parallel sort by destination vertex (CSC stores by dst)
        edges.par_sort_unstable_by_key(|(_, d, _)| *d);

        // Build CSC arrays
        let mut indptr = vec![0; num_vertices + 1];
        let mut indices = Vec::with_capacity(num_edges);
        let mut csc_weights = weights.map(|_| Vec::with_capacity(num_edges));

        for (s, d, w) in edges {
            // Validate vertex IDs
            if s < 0 || s >= num_vertices as i32 {
                return Err(GraphError::InvalidVertex(s));
            }
            if d < 0 || d >= num_vertices as i32 {
                return Err(GraphError::InvalidVertex(d));
            }

            indices.push(s);
            if let Some(ref mut ws) = csc_weights {
                ws.push(w.unwrap());
            }
            indptr[d as usize + 1] += 1;
        }

        // Compute cumulative sum for indptr
        for i in 1..=num_vertices {
            indptr[i] += indptr[i - 1];
        }

        Ok(CscGraph {
            indptr,
            indices,
            weights: csc_weights,
            num_vertices,
        })
    }

    /// Get incoming edges for a vertex
    ///
    /// # Arguments
    /// * `v` - Vertex ID
    ///
    /// # Returns
    /// Slice of source vertex IDs
    ///
    /// # Errors
    /// Returns error if vertex ID is out of range
    pub fn in_edges(&self, v: VertexId) -> Result<&[VertexId]> {
        if v < 0 || v >= self.num_vertices as i32 {
            return Err(GraphError::InvalidVertex(v));
        }
        let start = self.indptr[v as usize] as usize;
        let end = self.indptr[v as usize + 1] as usize;
        Ok(&self.indices[start..end])
    }

    /// Get in-degree of a vertex
    ///
    /// # Arguments
    /// * `v` - Vertex ID
    ///
    /// # Returns
    /// Number of incoming edges
    pub fn degree(&self, v: VertexId) -> Result<usize> {
        if v < 0 || v >= self.num_vertices as i32 {
            return Err(GraphError::InvalidVertex(v));
        }
        let start = self.indptr[v as usize];
        let end = self.indptr[v as usize + 1];
        Ok((end - start) as usize)
    }

    /// Get number of edges
    pub fn num_edges(&self) -> usize {
        self.indices.len()
    }

    /// Check if graph has weights
    pub fn has_weights(&self) -> bool {
        self.weights.is_some()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_csc_simple() {
        let src = vec![0, 0, 1, 2];
        let dst = vec![1, 2, 2, 0];
        let csc = CscGraph::from_edges(&src, &dst, 3, None).unwrap();

        assert_eq!(csc.num_vertices, 3);
        assert_eq!(csc.num_edges(), 4);
        assert_eq!(csc.in_edges(0).unwrap(), &[2]);
        assert_eq!(csc.in_edges(1).unwrap(), &[0]);
        assert_eq!(csc.in_edges(2).unwrap(), &[0, 1]);
    }

    #[test]
    fn test_csc_with_weights() {
        let src = vec![0, 1];
        let dst = vec![1, 0];
        let weights = vec![1.5, 2.5];
        let csc = CscGraph::from_edges(&src, &dst, 2, Some(&weights)).unwrap();

        assert!(csc.has_weights());
        assert_eq!(csc.weights.as_ref().unwrap(), &vec![2.5, 1.5]); // Sorted by dst
    }

    #[test]
    fn test_csc_empty_graph() {
        let src: Vec<i32> = vec![];
        let dst: Vec<i32> = vec![];
        let csc = CscGraph::from_edges(&src, &dst, 5, None).unwrap();

        assert_eq!(csc.num_vertices, 5);
        assert_eq!(csc.num_edges(), 0);
        let edges = csc.in_edges(0).unwrap();
        assert_eq!(edges.len(), 0);
    }

    #[test]
    fn test_csc_degree() {
        let src = vec![0, 1, 2, 0];
        let dst = vec![1, 1, 1, 2];
        let csc = CscGraph::from_edges(&src, &dst, 3, None).unwrap();

        assert_eq!(csc.degree(0).unwrap(), 0);
        assert_eq!(csc.degree(1).unwrap(), 3); // Three incoming edges
        assert_eq!(csc.degree(2).unwrap(), 1);
    }

    #[test]
    fn test_csc_invalid_vertex() {
        let src = vec![0, 1];
        let dst = vec![1, 0];
        let csc = CscGraph::from_edges(&src, &dst, 2, None).unwrap();

        assert!(csc.in_edges(-1).is_err());
        assert!(csc.in_edges(5).is_err());
    }
}
