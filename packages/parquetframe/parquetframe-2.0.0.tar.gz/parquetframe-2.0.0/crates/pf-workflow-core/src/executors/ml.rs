use async_trait::async_trait;
use std::collections::HashMap;
use std::sync::Arc;
use datafusion::dataframe::DataFrame;
use crate::executors::{StepExecutor, ExecutionContext, ExecutionError};
use pf_ml::{Trainer, Predictor, TabularTransformer, TabularPredictor};

pub struct TetnusTrainExecutor;

#[async_trait]
impl StepExecutor for TetnusTrainExecutor {
    async fn execute(&self, params: &HashMap<String, serde_yaml::Value>, inputs: Vec<Arc<DataFrame>>, _ctx: &ExecutionContext) -> Result<Option<Arc<DataFrame>>, ExecutionError> {
        // 1. Parse params
        let output_model_path = params.get("output_model")
            .and_then(|v| v.as_str())
            .ok_or_else(|| ExecutionError::StepFailed("Missing 'output_model' param".to_string()))?;

        let model_config = params.get("model")
            .ok_or_else(|| ExecutionError::StepFailed("Missing 'model' param".to_string()))?;

        let model_type = model_config.get("type")
            .and_then(|v| v.as_str())
            .ok_or_else(|| ExecutionError::StepFailed("Missing 'model.type' param".to_string()))?;

        let target_column = model_config.get("target_column")
            .and_then(|v| v.as_str())
            .ok_or_else(|| ExecutionError::StepFailed("Missing 'model.target_column' param".to_string()))?;

        // 2. Select Trainer based on type
        let trainer: Box<dyn Trainer> = match model_type {
            "TabularTransformer" => Box::new(TabularTransformer {
                target_column: target_column.to_string(),
                feature_columns: None, // TODO: Parse feature_columns
                hyperparameters: None, // TODO: Parse hyperparameters
            }),
            _ => return Err(ExecutionError::StepFailed(format!("Unknown model type: {}", model_type))),
        };

        // 3. Train
        if inputs.is_empty() {
            return Err(ExecutionError::StepFailed("Missing input data for training".to_string()));
        }
        let df = inputs[0].clone();

        // We need to dereference Arc<DataFrame> to get DataFrame, but Trainer expects DataFrame (owned)
        // DataFusion DataFrame is cheap to clone (Arc internals)
        let model_bytes = trainer.train((*df).clone()).await
            .map_err(|e| ExecutionError::StepFailed(format!("Training failed: {}", e)))?;

        // 4. Save model
        std::fs::write(output_model_path, model_bytes)
            .map_err(|e| ExecutionError::StepFailed(format!("Failed to save model: {}", e)))?;

        Ok(None)
    }
}

pub struct TetnusPredictExecutor;

#[async_trait]
impl StepExecutor for TetnusPredictExecutor {
    async fn execute(&self, params: &HashMap<String, serde_yaml::Value>, inputs: Vec<Arc<DataFrame>>, _ctx: &ExecutionContext) -> Result<Option<Arc<DataFrame>>, ExecutionError> {
        // 1. Parse params
        let model_path = params.get("model")
            .and_then(|v| v.as_str())
            .ok_or_else(|| ExecutionError::StepFailed("Missing 'model' param".to_string()))?;

        let prediction_column = params.get("prediction_column")
            .and_then(|v| v.as_str())
            .unwrap_or("prediction");

        // 2. Load model
        let model_bytes = std::fs::read(model_path)
            .map_err(|e| ExecutionError::StepFailed(format!("Failed to read model: {}", e)))?;

        // 3. Predict
        if inputs.is_empty() {
            return Err(ExecutionError::StepFailed("Missing input data for prediction".to_string()));
        }
        let df = inputs[0].clone();

        // For MVP, assume TabularPredictor. In real app, we'd detect model type from metadata.
        let predictor = TabularPredictor {
            prediction_column: prediction_column.to_string(),
        };

        let result_df = predictor.predict(&model_bytes, (*df).clone()).await
            .map_err(|e| ExecutionError::StepFailed(format!("Prediction failed: {}", e)))?;

        Ok(Some(Arc::new(result_df)))
    }
}

pub struct TetnusCompileExecutor;

#[async_trait]
impl StepExecutor for TetnusCompileExecutor {
    async fn execute(&self, _params: &HashMap<String, serde_yaml::Value>, _inputs: Vec<Arc<DataFrame>>, _ctx: &ExecutionContext) -> Result<Option<Arc<DataFrame>>, ExecutionError> {
        // Mock implementation for now
        println!("Mock: Compiling model for edge device...");
        Ok(None)
    }
}
