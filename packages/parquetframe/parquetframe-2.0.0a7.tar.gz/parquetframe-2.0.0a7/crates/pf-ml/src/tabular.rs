use async_trait::async_trait;
use datafusion::dataframe::DataFrame;
use datafusion::arrow::array::{Float64Array, Array};
use datafusion::arrow::record_batch::RecordBatch;
use smartcore::ensemble::random_forest_regressor::RandomForestRegressor;
use smartcore::linalg::basic::matrix::DenseMatrix;
use std::sync::Arc;
use crate::error::MlError;
use crate::trainer::Trainer;

pub struct TabularTransformer {
    pub target_column: String,
    pub feature_columns: Option<Vec<String>>,
    pub hyperparameters: Option<serde_json::Value>,
}

#[async_trait]
impl Trainer for TabularTransformer {
    async fn train(&self, df: DataFrame) -> Result<Vec<u8>, MlError> {
        // 1. Collect data into memory (MVP: fits in memory)
        let batches = df.collect().await?;
        if batches.is_empty() {
            return Err(MlError::DataError("No data to train on".to_string()));
        }

        // 2. Prepare X (features) and y (target)
        let (x_data, y_data) = self.prepare_data(&batches)?;

        // 3. Train Random Forest (SmartCore)
        // MVP: Hardcoded params or basic parsing
        let x = DenseMatrix::from_2d_vec(&x_data);
        let y = y_data;

        let model = RandomForestRegressor::fit(&x, &y, Default::default())
            .map_err(|e| MlError::TrainingError(format!("SmartCore error: {}", e)))?;

        // 4. Serialize model (using bincode 2.0)
        let config = bincode::config::standard();
        let model_bytes = bincode::serde::encode_to_vec(&model, config)
            .map_err(|e| MlError::ModelError(format!("Serialization error: {}", e)))?;

        Ok(model_bytes)
    }
}

impl TabularTransformer {
    fn prepare_data(&self, batches: &[RecordBatch]) -> Result<(Vec<Vec<f64>>, Vec<f64>), MlError> {
        let mut x_out = Vec::new();
        let mut y_out = Vec::new();

        for batch in batches {
            let target_col = batch.column_by_name(&self.target_column)
                .ok_or_else(|| MlError::DataError(format!("Target column '{}' not found", self.target_column)))?;

            let target_arr = target_col.as_any().downcast_ref::<Float64Array>()
                .ok_or_else(|| MlError::DataError("Target column must be Float64 for regression".to_string()))?;

            // Identify feature columns
            let feature_cols: Vec<usize> = if let Some(cols) = &self.feature_columns {
                cols.iter().map(|name| {
                    batch.schema().index_of(name).map_err(|_| MlError::DataError(format!("Feature '{}' not found", name)))
                }).collect::<Result<Vec<_>, _>>()?
            } else {
                (0..batch.num_columns())
                    .filter(|&i| batch.schema().field(i).name() != &self.target_column)
                    .collect()
            };

            for row_idx in 0..batch.num_rows() {
                let mut row_features = Vec::new();
                for &col_idx in &feature_cols {
                    let col = batch.column(col_idx);
                    // MVP: Only support Float64 features
                    let val = if let Some(arr) = col.as_any().downcast_ref::<Float64Array>() {
                        arr.value(row_idx)
                    } else {
                        // TODO: Handle other types
                        0.0
                    };
                    row_features.push(val);
                }
                x_out.push(row_features);
                y_out.push(target_arr.value(row_idx));
            }
        }

        Ok((x_out, y_out))
    }
}

pub struct TabularPredictor {
    pub prediction_column: String,
}

#[async_trait]
impl crate::predictor::Predictor for TabularPredictor {
    async fn predict(&self, model_data: &[u8], df: DataFrame) -> Result<DataFrame, MlError> {
        // 1. Deserialize model
        let config = bincode::config::standard();
        let (model, _): (RandomForestRegressor<f64, f64, DenseMatrix<f64>, Vec<f64>>, usize) =
            bincode::serde::decode_from_slice(model_data, config)
            .map_err(|e| MlError::ModelError(format!("Deserialization error: {}", e)))?;

        // 2. Collect data
        let batches = df.collect().await?;
        if batches.is_empty() {
            return Ok(datafusion::dataframe::DataFrame::new(
                datafusion::prelude::SessionContext::new().state(),
                datafusion::logical_expr::LogicalPlan::EmptyRelation(datafusion::logical_expr::EmptyRelation {
                    produce_one_row: false,
                    schema: Arc::new(datafusion::common::DFSchema::empty()),
                })
            ));
        }

        // 3. Prepare features (similar to training, but no target)
        // We need to know which columns were used. Ideally this is stored in the model metadata.
        // For MVP, we assume all float columns except target (which we don't have here) are features.
        // Actually, we should probably store feature names in the model blob or metadata.
        // For now, let's assume all numeric columns are features.

        let mut new_batches = Vec::new();

        for batch in &batches {
            let mut x_batch = Vec::new();
            let feature_cols: Vec<usize> = (0..batch.num_columns())
                .filter(|&i| {
                    let schema = batch.schema();
                    let field = schema.field(i);
                    field.data_type() == &datafusion::arrow::datatypes::DataType::Float64
                })
                .collect();

            for row_idx in 0..batch.num_rows() {
                let mut row_features = Vec::new();
                for &col_idx in &feature_cols {
                    let col = batch.column(col_idx);
                    let val = col.as_any().downcast_ref::<Float64Array>().unwrap().value(row_idx);
                    row_features.push(val);
                }
                x_batch.push(row_features);
            }

            let x = DenseMatrix::from_2d_vec(&x_batch);
            let y_hat = model.predict(&x).map_err(|e| MlError::PredictionError(format!("Prediction error: {}", e)))?;

            // Create prediction array
            let pred_array = Float64Array::from(y_hat);

            // Append to batch
            let mut columns = batch.columns().to_vec();
            columns.push(Arc::new(pred_array));

            let mut fields = batch.schema().fields().to_vec();
            fields.push(Arc::new(datafusion::arrow::datatypes::Field::new(&self.prediction_column, datafusion::arrow::datatypes::DataType::Float64, true)));

            let new_schema = Arc::new(datafusion::arrow::datatypes::Schema::new(fields));
            let new_batch = RecordBatch::try_new(new_schema, columns)?;
            new_batches.push(new_batch);
        }

        // 4. Return new DataFrame
        let ctx = datafusion::prelude::SessionContext::new();
        let df = ctx.read_batches(new_batches)?;
        Ok(df)
    }
}
