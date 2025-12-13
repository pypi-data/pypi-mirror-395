use async_trait::async_trait;
use std::collections::HashMap;
use std::sync::Arc;
use datafusion::prelude::*;
use crate::executors::{StepExecutor, ExecutionContext, ExecutionResult, ExecutionError};

pub struct HttpExecutor;

#[async_trait]
impl StepExecutor for HttpExecutor {
    async fn execute(
        &self,
        params: &HashMap<String, serde_yaml::Value>,
        _inputs: Vec<Arc<DataFrame>>,
        ctx: &ExecutionContext,
    ) -> ExecutionResult<Option<Arc<DataFrame>>> {
        let url = params.get("url")
            .and_then(|v| v.as_str())
            .ok_or_else(|| ExecutionError::MissingParameter("url".to_string()))?;

        let format = params.get("format")
            .and_then(|v| v.as_str())
            .unwrap_or("json");

        // Fetch data
        let response = reqwest::get(url).await
            .map_err(|e| ExecutionError::StepFailed(format!("HTTP request failed: {}", e)))?
            .text().await
            .map_err(|e| ExecutionError::StepFailed(format!("Failed to read response body: {}", e)))?;

        // Parse based on format
        let temp_path = format!("/tmp/pf_http_{}.{}", uuid::Uuid::new_v4(), format);

        if format == "json" {
            // Convert JSON array to NDJSON
            let json: serde_json::Value = serde_json::from_str(&response)
                .map_err(|e| ExecutionError::StepFailed(format!("Failed to parse JSON response: {}", e)))?;

            let mut file_content = String::new();
            if let Some(array) = json.as_array() {
                for item in array {
                    file_content.push_str(&item.to_string());
                    file_content.push('\n');
                }
            } else {
                // Single object
                file_content.push_str(&json.to_string());
                file_content.push('\n');
            }
            std::fs::write(&temp_path, file_content)?;
        } else {
            std::fs::write(&temp_path, response)?;
        }

        let df = match format {
            "json" => ctx.session_ctx.read_json(&temp_path, NdJsonReadOptions::default()).await?,
            "csv" => ctx.session_ctx.read_csv(&temp_path, CsvReadOptions::default()).await?,
            _ => return Err(ExecutionError::StepFailed(format!("Unsupported format: {}", format))),
        };

        // Clean up temp file? Maybe later or let OS handle /tmp

        Ok(Some(Arc::new(df)))
    }
}
