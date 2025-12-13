//! Graph algorithms and data structures for ParquetFrame.
//!
//! This crate provides high-performance graph operations including:
//! - CSR/CSC adjacency structure building
//! - Graph traversal algorithms (BFS, DFS)
//! - Advanced algorithms (PageRank, Dijkstra, Connected Components)
//!
//! # Phase 1: Core graph algorithms (CSR/CSC, BFS, DFS)
//! # Phase 3: Advanced graph algorithms (PageRank, Dijkstra, Connected Components)

pub mod bfs;
pub mod csc;
pub mod csr;
pub mod dfs;
pub mod error;
pub mod types;

// Phase 3: Advanced graph algorithms
pub mod components;
pub mod dijkstra;
pub mod pagerank;

// Re-export commonly used types
pub use bfs::{bfs_parallel, bfs_sequential, BfsResult};
pub use csc::CscGraph;
pub use csr::CsrGraph;
pub use dfs::dfs;
pub use error::{GraphError, Result};
pub use types::*;

// Re-export Phase 3 algorithm functions
pub use components::union_find_components;
pub use dijkstra::dijkstra_rust;
pub use pagerank::pagerank_rust;
