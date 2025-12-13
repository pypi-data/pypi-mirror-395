use async_trait::async_trait;
use datafusion::dataframe::DataFrame;
use crate::error::MlError;

#[async_trait]
pub trait Trainer: Send + Sync {
    /// Train a model on the given DataFrame
    async fn train(&self, df: DataFrame) -> Result<Vec<u8>, MlError>;
}
