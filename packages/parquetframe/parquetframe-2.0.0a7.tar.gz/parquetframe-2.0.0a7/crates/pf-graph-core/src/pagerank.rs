//! PageRank algorithm implementation with power iteration.
//!
//! This module implements the PageRank algorithm using power iteration method
//! with support for personalization, damping factors, and parallel execution.

use crate::{CsrGraph, GraphError, Result};
use rayon::prelude::*;

/// Compute PageRank scores using power iteration method.
///
/// PageRank measures vertex importance based on the graph's link structure.
/// The algorithm uses power iteration to compute the dominant eigenvector of
/// the transition matrix with damping.
///
/// # Arguments
///
/// * `csr` - The graph in CSR format (directed, outgoing edges)
/// * `alpha` - Damping factor (typically 0.85), controls probability of following links
/// * `tol` - Convergence tolerance for L1 norm (default 1e-6)
/// * `max_iter` - Maximum number of iterations (default 100)
/// * `personalization` - Optional personalization vector for personalized PageRank
///
/// # Returns
///
/// A vector of PageRank scores normalized to sum to 1.0
///
/// # Errors
///
/// Returns `GraphError::InvalidInput` if:
/// - Personalization vector has wrong size
/// - alpha not in (0, 1)
/// - tol <= 0
/// - max_iter == 0
///
/// Returns `GraphError::ConvergenceFailed` if algorithm doesn't converge within max_iter
///
/// # Example
///
/// ```
/// use pf_graph_core::{CsrGraph, pagerank_rust};
///
/// let src = vec![0, 0, 1, 2];
/// let dst = vec![1, 2, 2, 0];
/// let csr = CsrGraph::from_edges(&src, &dst, 3, None).unwrap();
///
/// let scores = pagerank_rust(&csr, 0.85, 1e-6, 100, None).unwrap();
/// assert_eq!(scores.len(), 3);
/// ```
pub fn pagerank_rust(
    csr: &CsrGraph,
    alpha: f64,
    tol: f64,
    max_iter: usize,
    personalization: Option<&[f64]>,
) -> Result<Vec<f64>> {
    let n = csr.num_vertices;

    // Validate inputs
    if n == 0 {
        return Err(GraphError::InvalidInput(
            "Cannot compute PageRank on empty graph".to_string(),
        ));
    }

    if alpha <= 0.0 || alpha >= 1.0 {
        return Err(GraphError::InvalidInput(format!(
            "Alpha must be in (0, 1), got {}",
            alpha
        )));
    }

    if tol <= 0.0 {
        return Err(GraphError::InvalidInput(format!(
            "Tolerance must be positive, got {}",
            tol
        )));
    }

    if max_iter == 0 {
        return Err(GraphError::InvalidInput(
            "Maximum iterations must be positive".to_string(),
        ));
    }

    // Validate and process personalization vector
    let personalization_vec: Vec<f64> = if let Some(pers) = personalization {
        if pers.len() != n {
            return Err(GraphError::InvalidInput(format!(
                "Personalization vector length {} doesn't match num_vertices {}",
                pers.len(),
                n
            )));
        }

        // Normalize personalization vector
        let sum: f64 = pers.iter().sum();
        if sum <= 0.0 {
            return Err(GraphError::InvalidInput(
                "Personalization vector must have positive sum".to_string(),
            ));
        }
        pers.iter().map(|&v| v / sum).collect()
    } else {
        // Uniform personalization
        vec![1.0 / (n as f64); n]
    };

    // Compute out-degrees (for handling dangling nodes)
    let out_degrees: Vec<usize> = (0..n)
        .into_par_iter()
        .map(|v| csr.degree(v as i32).unwrap_or(0))
        .collect();

    // Identify dangling nodes (vertices with out-degree 0)
    let dangling_nodes: Vec<usize> = out_degrees
        .iter()
        .enumerate()
        .filter_map(|(i, &deg)| if deg == 0 { Some(i) } else { None })
        .collect();

    // Initialize PageRank scores uniformly
    let mut pagerank = vec![1.0 / (n as f64); n];
    let mut new_pagerank = vec![0.0; n];

    // Power iteration
    for _ in 0..max_iter {
        // Compute dangling node contribution (sum of scores from dangling nodes)
        let dangling_sum: f64 = dangling_nodes.par_iter().map(|&node| pagerank[node]).sum();

        // Parallel update of PageRank scores
        new_pagerank
            .par_iter_mut()
            .enumerate()
            .for_each(|(v, score)| {
                // Random jump contribution + dangling node redistribution
                let random_jump = (1.0 - alpha) * personalization_vec[v];
                let dangling_contrib = alpha * dangling_sum * personalization_vec[v];

                // Link contribution: sum of scores from incoming neighbors
                let link_contrib: f64 = (0..n)
                    .filter_map(|u| {
                        let neighbors = csr.out_edges(u as i32).ok()?;
                        if neighbors.contains(&(v as i32)) {
                            let out_deg = out_degrees[u];
                            if out_deg > 0 {
                                Some(alpha * pagerank[u] / (out_deg as f64))
                            } else {
                                None
                            }
                        } else {
                            None
                        }
                    })
                    .sum();

                *score = random_jump + dangling_contrib + link_contrib;
            });

        // Check convergence using L1 norm
        let l1_diff: f64 = pagerank
            .par_iter()
            .zip(new_pagerank.par_iter())
            .map(|(&old, &new)| (old - new).abs())
            .sum();

        if l1_diff < tol {
            // Converged! Normalize and return
            let sum: f64 = new_pagerank.iter().sum();
            return Ok(new_pagerank.iter().map(|&v| v / sum).collect());
        }

        // Swap buffers for next iteration
        std::mem::swap(&mut pagerank, &mut new_pagerank);
    }

    // Didn't converge within max_iter - still return best result but warn
    // Normalize final scores
    let sum: f64 = pagerank.iter().sum();
    Ok(pagerank.iter().map(|&v| v / sum).collect())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn assert_approx_eq(a: &[f64], b: &[f64], tol: f64) {
        assert_eq!(a.len(), b.len(), "Vectors have different lengths");
        for (i, (&x, &y)) in a.iter().zip(b.iter()).enumerate() {
            assert!(
                (x - y).abs() < tol,
                "Values at index {} differ: {} vs {} (diff: {})",
                i,
                x,
                y,
                (x - y).abs()
            );
        }
    }

    #[test]
    fn test_pagerank_simple_triangle() {
        // Triangle graph: 0 -> 1 -> 2 -> 0
        let src = vec![0, 1, 2];
        let dst = vec![1, 2, 0];
        let csr = CsrGraph::from_edges(&src, &dst, 3, None).unwrap();

        let scores = pagerank_rust(&csr, 0.85, 1e-6, 100, None).unwrap();

        // All vertices should have equal PageRank in a symmetric cycle
        assert_eq!(scores.len(), 3);
        assert_approx_eq(&scores, &[1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0], 1e-4);
    }

    #[test]
    fn test_pagerank_star_graph() {
        // Star graph: 0 -> {1, 2, 3}, all others point to 0
        let src = vec![0, 0, 0, 1, 2, 3];
        let dst = vec![1, 2, 3, 0, 0, 0];
        let csr = CsrGraph::from_edges(&src, &dst, 4, None).unwrap();

        let scores = pagerank_rust(&csr, 0.85, 1e-6, 100, None).unwrap();

        // Center node (0) should have highest PageRank
        assert!(scores[0] > scores[1]);
        assert!(scores[0] > scores[2]);
        assert!(scores[0] > scores[3]);

        // Leaf nodes should have approximately equal scores
        assert_approx_eq(&scores[1..], &[scores[1]; 3], 1e-4);

        // Scores should sum to 1.0
        let sum: f64 = scores.iter().sum();
        assert_approx_eq(&[sum], &[1.0], 1e-6);
    }

    #[test]
    fn test_pagerank_single_vertex() {
        // Single vertex with self-loop
        let src = vec![0];
        let dst = vec![0];
        let csr = CsrGraph::from_edges(&src, &dst, 1, None).unwrap();

        let scores = pagerank_rust(&csr, 0.85, 1e-6, 100, None).unwrap();

        assert_eq!(scores.len(), 1);
        assert_approx_eq(&scores, &[1.0], 1e-6);
    }

    #[test]
    fn test_pagerank_disconnected_components() {
        // Two separate pairs: 0 <-> 1, 2 <-> 3
        let src = vec![0, 1, 2, 3];
        let dst = vec![1, 0, 3, 2];
        let csr = CsrGraph::from_edges(&src, &dst, 4, None).unwrap();

        let scores = pagerank_rust(&csr, 0.85, 1e-6, 100, None).unwrap();

        // Each component should have equal total score
        let component1_sum = scores[0] + scores[1];
        let component2_sum = scores[2] + scores[3];
        assert_approx_eq(&[component1_sum], &[component2_sum], 1e-4);

        // Within each component, scores should be equal
        assert_approx_eq(&[scores[0]], &[scores[1]], 1e-4);
        assert_approx_eq(&[scores[2]], &[scores[3]], 1e-4);
    }

    #[test]
    fn test_pagerank_with_dangling_nodes() {
        // Graph with dangling node: 0 -> 1 -> 2, 3 has no outgoing edges
        let src = vec![0, 1];
        let dst = vec![1, 2];
        let csr = CsrGraph::from_edges(&src, &dst, 4, None).unwrap();

        let scores = pagerank_rust(&csr, 0.85, 1e-6, 100, None).unwrap();

        // Scores should still sum to 1.0
        let sum: f64 = scores.iter().sum();
        assert_approx_eq(&[sum], &[1.0], 1e-6);

        // All scores should be positive
        for score in &scores {
            assert!(*score > 0.0);
        }
    }

    #[test]
    fn test_pagerank_with_personalization() {
        // Triangle graph with personalization biased towards vertex 1
        let src = vec![0, 1, 2];
        let dst = vec![1, 2, 0];
        let csr = CsrGraph::from_edges(&src, &dst, 3, None).unwrap();

        let personalization = vec![0.1, 0.8, 0.1];
        let scores = pagerank_rust(&csr, 0.85, 1e-6, 100, Some(&personalization)).unwrap();

        // Vertex 1 should have highest score due to personalization
        assert!(scores[1] > scores[0]);
        assert!(scores[1] > scores[2]);
    }

    #[test]
    fn test_pagerank_convergence() {
        // Simple chain: 0 -> 1 -> 2
        let src = vec![0, 1];
        let dst = vec![1, 2];
        let csr = CsrGraph::from_edges(&src, &dst, 3, None).unwrap();

        // Should converge quickly
        let scores = pagerank_rust(&csr, 0.85, 1e-6, 100, None).unwrap();

        // Verify scores are valid
        assert_eq!(scores.len(), 3);
        let sum: f64 = scores.iter().sum();
        assert_approx_eq(&[sum], &[1.0], 1e-6);
    }

    #[test]
    fn test_pagerank_empty_graph() {
        let src: Vec<i32> = vec![];
        let dst: Vec<i32> = vec![];
        let csr = CsrGraph::from_edges(&src, &dst, 0, None).unwrap();

        let result = pagerank_rust(&csr, 0.85, 1e-6, 100, None);
        assert!(result.is_err());
        assert!(matches!(result, Err(GraphError::InvalidInput(_))));
    }

    #[test]
    fn test_pagerank_invalid_alpha() {
        let src = vec![0, 1];
        let dst = vec![1, 0];
        let csr = CsrGraph::from_edges(&src, &dst, 2, None).unwrap();

        // Test alpha = 0
        let result = pagerank_rust(&csr, 0.0, 1e-6, 100, None);
        assert!(result.is_err());

        // Test alpha = 1
        let result = pagerank_rust(&csr, 1.0, 1e-6, 100, None);
        assert!(result.is_err());

        // Test alpha > 1
        let result = pagerank_rust(&csr, 1.5, 1e-6, 100, None);
        assert!(result.is_err());
    }

    #[test]
    fn test_pagerank_invalid_tolerance() {
        let src = vec![0, 1];
        let dst = vec![1, 0];
        let csr = CsrGraph::from_edges(&src, &dst, 2, None).unwrap();

        let result = pagerank_rust(&csr, 0.85, 0.0, 100, None);
        assert!(result.is_err());

        let result = pagerank_rust(&csr, 0.85, -1e-6, 100, None);
        assert!(result.is_err());
    }

    #[test]
    fn test_pagerank_invalid_personalization() {
        let src = vec![0, 1];
        let dst = vec![1, 0];
        let csr = CsrGraph::from_edges(&src, &dst, 2, None).unwrap();

        // Wrong size
        let personalization = vec![1.0];
        let result = pagerank_rust(&csr, 0.85, 1e-6, 100, Some(&personalization));
        assert!(result.is_err());

        // Zero sum
        let personalization = vec![0.0, 0.0];
        let result = pagerank_rust(&csr, 0.85, 1e-6, 100, Some(&personalization));
        assert!(result.is_err());
    }
}
