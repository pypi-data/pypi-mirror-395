use async_trait::async_trait;
use std::collections::HashMap;
use std::sync::Arc;
use datafusion::prelude::*;
use crate::executors::{StepExecutor, ExecutionContext, ExecutionResult, ExecutionError};

pub struct ParquetReadExecutor;

#[async_trait]
impl StepExecutor for ParquetReadExecutor {
    async fn execute(
        &self,
        params: &HashMap<String, serde_yaml::Value>,
        _inputs: Vec<Arc<DataFrame>>,
        ctx: &ExecutionContext,
    ) -> ExecutionResult<Option<Arc<DataFrame>>> {
        let path = params.get("path")
            .and_then(|v| v.as_str())
            .ok_or_else(|| ExecutionError::MissingParameter("path".to_string()))?;

        let options = ParquetReadOptions::default();
        let df = ctx.session_ctx.read_parquet(path, options).await?;

        Ok(Some(Arc::new(df)))
    }
}

pub struct ParquetWriteExecutor;

#[async_trait]
impl StepExecutor for ParquetWriteExecutor {
    async fn execute(
        &self,
        params: &HashMap<String, serde_yaml::Value>,
        inputs: Vec<Arc<DataFrame>>,
        ctx: &ExecutionContext,
    ) -> ExecutionResult<Option<Arc<DataFrame>>> {
        let path = params.get("path")
            .and_then(|v| v.as_str())
            .ok_or_else(|| ExecutionError::MissingParameter("path".to_string()))?;

        if inputs.is_empty() {
            return Err(ExecutionError::StepFailed("ParquetWrite requires an input".to_string()));
        }
        let df = &inputs[0];

        // Register input as temp table
        let temp_table = format!("temp_write_{}", uuid::Uuid::new_v4().simple());
        ctx.session_ctx.register_table(&temp_table, df.as_ref().clone().into_view())?;

        // Execute COPY command
        let sql = format!("COPY {} TO '{}'", temp_table, path);
        ctx.session_ctx.sql(&sql).await?.collect().await?;

        Ok(None)
    }
}
