use thiserror::Error;

#[derive(Error, Debug)]
pub enum TetnusNnError {
    #[error("Tetnus Core Error: {0}")]
    CoreError(#[from] tetnus_core::TetnusError),

    #[error("Invalid Input: {0}")]
    InvalidInput(String),

    #[error("Parameter Error: {0}")]
    ParameterError(String),
}

pub type Result<T> = std::result::Result<T, TetnusNnError>;
