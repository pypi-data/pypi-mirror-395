use tetnus_core::Tensor;
use tetnus_nn::{Module, Result, TetnusNnError};
use crate::model::SimpleTransformer;

/// Basic trainer for LLM fine-tuning with LoRA
pub struct Trainer {
    /// The model being trained
    model: SimpleTransformer,
}

impl Trainer {
    /// Create a new trainer
    pub fn new(model: SimpleTransformer) -> Self {
        Self { model }
    }

    /// Perform a single training step
    ///
    /// # Arguments
    /// * `inputs` - Input tensor (batch_size × seq_len × hidden_size)
    /// * `targets` - Target tensor (batch_size × seq_len × hidden_size)
    ///
    /// # Returns
    /// Mean squared error loss
    pub fn train_step(&mut self, inputs: &Tensor, targets: &Tensor) -> Result<f32> {
        // Forward pass
        let predictions = self.model.forward(inputs)?;

        // Compute MSE loss
        let loss = self.compute_mse_loss(&predictions, targets)?;

        Ok(loss)
    }

    /// Compute mean squared error loss
    fn compute_mse_loss(&self, predictions: &Tensor, targets: &Tensor) -> Result<f32> {
        let pred_data = predictions.data();
        let target_data = targets.data();

        if pred_data.len() != target_data.len() {
            return Err(TetnusNnError::InvalidInput(
                format!("Shape mismatch: predictions {} vs targets {}",
                        pred_data.len(), target_data.len())
            ));
        }

        // Compute MSE: mean((pred - target)^2)
        let mse: f32 = pred_data.iter()
            .zip(target_data.iter())
            .map(|(p, t)| (p - t).powi(2))
            .sum::<f32>() / pred_data.len() as f32;

        Ok(mse)
    }

    /// Get reference to the model
    pub fn model(&self) -> &SimpleTransformer {
        &self.model
    }

    /// Get mutable reference to the model
    pub fn model_mut(&mut self) -> &mut SimpleTransformer {
        &mut self.model
    }
}
