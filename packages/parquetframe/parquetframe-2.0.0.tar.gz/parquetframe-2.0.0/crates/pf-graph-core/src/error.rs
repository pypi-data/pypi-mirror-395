//! Error types for graph operations.

use thiserror::Error;

/// Errors that can occur during graph operations
#[derive(Error, Debug)]
pub enum GraphError {
    #[error("Invalid vertex ID: {0}")]
    InvalidVertex(i32),

    #[error("Empty graph: no vertices")]
    EmptyGraph,

    #[error("Mismatched array lengths: {0}")]
    MismatchedLengths(String),

    #[error("Out of bounds: {0}")]
    OutOfBounds(String),

    #[error("Invalid input: {0}")]
    InvalidInput(String),

    #[error("Algorithm did not converge: {0}")]
    ConvergenceFailed(String),
}

/// Result type alias for graph operations
pub type Result<T> = std::result::Result<T, GraphError>;
