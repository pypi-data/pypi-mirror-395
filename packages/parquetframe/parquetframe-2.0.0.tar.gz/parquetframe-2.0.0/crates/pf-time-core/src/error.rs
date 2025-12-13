//! Error types for time-series operations.

use thiserror::Error;

/// Result type for time-series operations.
pub type Result<T> = std::result::Result<T, TimeError>;

/// Error types for time-series operations.
#[derive(Error, Debug)]
pub enum TimeError {
    /// Invalid time index
    #[error("Invalid time index: {0}")]
    InvalidIndex(String),

    /// Resampling error
    #[error("Resampling error: {0}")]
    ResampleError(String),

    /// Rolling window error
    #[error("Rolling window error: {0}")]
    RollingError(String),

    /// As-of join error
    #[error("As-of join error: {0}")]
    AsofError(String),

    /// Arrow error
    #[error("Arrow error: {0}")]
    Arrow(#[from] arrow::error::ArrowError),

    /// Generic error
    #[error("{0}")]
    Other(String),
}
