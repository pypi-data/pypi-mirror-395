use async_trait::async_trait;
use std::collections::HashMap;
use std::sync::Arc;
use datafusion::prelude::*;
use crate::executors::{StepExecutor, ExecutionContext, ExecutionResult, ExecutionError};

pub struct DataFusionSqlExecutor;

#[async_trait]
impl StepExecutor for DataFusionSqlExecutor {
    async fn execute(
        &self,
        params: &HashMap<String, serde_yaml::Value>,
        _inputs: Vec<Arc<DataFrame>>,
        ctx: &ExecutionContext,
    ) -> ExecutionResult<Option<Arc<DataFrame>>> {
        let sql = params.get("sql")
            .and_then(|v| v.as_str())
            .ok_or_else(|| ExecutionError::MissingParameter("sql".to_string()))?;

        // Execute SQL against the session context (which has tables registered)
        let df = ctx.session_ctx.sql(sql).await?;

        // We need to execute the plan to get the result, but here we return the DataFrame
        // which represents the logical plan. The actual execution happens when we collect or write.
        // However, for the next steps to use it, they might need it registered.
        // In DataFusion, `ctx.sql()` returns a DataFrame.

        Ok(Some(Arc::new(df)))
    }
}
