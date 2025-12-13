pub mod datafusion;
pub mod parquet;
pub mod http;
pub mod ml;
pub mod tetnus;

pub use self::datafusion::DataFusionSqlExecutor;

use async_trait::async_trait;
use std::collections::HashMap;
use std::sync::Arc;
use ::datafusion::prelude::*;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ExecutionError {
    #[error("Step failed: {0}")]
    StepFailed(String),
    #[error("DataFusion error: {0}")]
    DataFusionError(#[from] ::datafusion::error::DataFusionError),
    #[error("IO error: {0}")]
    IoError(#[from] std::io::Error),
    #[error("Missing parameter: {0}")]
    MissingParameter(String),
}

pub type ExecutionResult<T> = Result<T, ExecutionError>;

/// Context passed to each step execution
pub struct ExecutionContext {
    pub session_ctx: SessionContext,
    pub data_handles: HashMap<String, Arc<DataFrame>>,
}

impl ExecutionContext {
    pub fn new() -> Self {
        Self {
            session_ctx: SessionContext::new(),
            data_handles: HashMap::new(),
        }
    }

    pub fn register_handle(&mut self, name: &str, df: Arc<DataFrame>) {
        self.data_handles.insert(name.to_string(), df);
    }

    pub fn get_handle(&self, name: &str) -> Option<Arc<DataFrame>> {
        self.data_handles.get(name).cloned()
    }
}

#[async_trait]
pub trait StepExecutor: Send + Sync {
    async fn execute(
        &self,
        params: &HashMap<String, serde_yaml::Value>,
        inputs: Vec<Arc<DataFrame>>,
        ctx: &ExecutionContext,
    ) -> ExecutionResult<Option<Arc<DataFrame>>>;
}
