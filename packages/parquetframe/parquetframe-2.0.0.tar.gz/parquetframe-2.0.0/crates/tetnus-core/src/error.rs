/// Error types for tensor operations
use thiserror::Error;

#[derive(Error, Debug)]
pub enum TetnusError {
    #[error("Shape mismatch: expected {expected:?}, got {actual:?}")]
    ShapeMismatch {
        expected: Vec<usize>,
        actual: Vec<usize>,
    },

    #[error("Invalid input: {0}")]
    InvalidInput(String),

    #[error("Invalid shape: {0}")]
    InvalidShape(String),

    #[error("Dimension error: {0}")]
    DimensionError(String),

    #[error("Gradient error: {0}")]
    GradientError(String),

    #[error("Device error: {0}")]
    DeviceError(String),

    #[error("Arrow error: {0}")]
    ArrowError(#[from] arrow::error::ArrowError),

    #[error("Invalid operation: {0}")]
    InvalidOperation(String),

    #[error("Not implemented: {0}")]
    NotImplemented(String),
}

pub type Result<T> = std::result::Result<T, TetnusError>;
