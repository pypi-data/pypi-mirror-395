use async_trait::async_trait;
use datafusion::dataframe::DataFrame;
use crate::error::MlError;

#[async_trait]
pub trait Predictor: Send + Sync {
    /// Run inference on the given DataFrame
    async fn predict(&self, model_data: &[u8], df: DataFrame) -> Result<DataFrame, MlError>;
}
