use thiserror::Error;

#[derive(Error, Debug)]
pub enum FinError {
    #[error("Arrow error: {0}")]
    ArrowError(#[from] arrow::error::ArrowError),

    #[error("Time series error: {0}")]
    TimeSeriesError(String),

    #[error("Invalid parameter: {0}")]
    InvalidParameter(String),

    #[error("Calculation error: {0}")]
    CalculationError(String),
}
