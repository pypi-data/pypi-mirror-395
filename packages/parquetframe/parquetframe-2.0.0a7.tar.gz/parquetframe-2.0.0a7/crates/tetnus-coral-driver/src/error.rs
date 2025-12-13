use thiserror::Error;

#[derive(Debug, Error)]
pub enum CoralError {
    #[error("Failed to initialize Edge TPU context")]
    InitFailed,

    #[error("Model loading failed: {0}")]
    ModelLoadError(String),

    #[error("Inference failed: {0}")]
    InferenceError(String),

    #[error("Edge TPU hardware not available")]
    HardwareUnavailable,

    #[error("Invalid input/output tensor shape")]
    InvalidTensorShape,
}

pub type Result<T> = std::result::Result<T, CoralError>;
