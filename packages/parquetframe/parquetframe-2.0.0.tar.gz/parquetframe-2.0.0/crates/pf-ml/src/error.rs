use thiserror::Error;

#[derive(Error, Debug)]
pub enum MlError {
    #[error("Training failed: {0}")]
    TrainingError(String),
    #[error("Prediction failed: {0}")]
    PredictionError(String),
    #[error("Data error: {0}")]
    DataError(String),
    #[error("Model error: {0}")]
    ModelError(String),
    #[error("Arrow error: {0}")]
    ArrowError(#[from] arrow::error::ArrowError),
    #[error("DataFusion error: {0}")]
    DataFusionError(#[from] datafusion::error::DataFusionError),
    #[error("DataFusion Arrow error: {0}")]
    DataFusionArrowError(#[from] datafusion::arrow::error::ArrowError),
}
