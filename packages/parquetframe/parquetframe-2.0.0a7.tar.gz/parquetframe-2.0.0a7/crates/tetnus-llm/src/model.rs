use tetnus_core::Tensor;
use tetnus_nn::{Module, Result};
use crate::{LoRALinear, config::ModelConfig};

/// Simple transformer model with LoRA support
pub struct SimpleTransformer {
    /// Model configuration
    config: ModelConfig,
    /// Transformer layers (simplified - just linear projections for MVP)
    layers: Vec<LoRALinear>,
}

impl SimpleTransformer {
    /// Create a new transformer model from configuration
    pub fn new(config: ModelConfig) -> Self {
        let mut layers = Vec::new();

        // Create simple linear layers for each transformer layer
        // In a full implementation, this would include attention, FFN, etc.
        for _ in 0..config.num_layers {
            layers.push(LoRALinear::new(
                config.hidden_size,
                config.hidden_size,
                8,    // default rank
                1.0,  // default alpha
            ));
        }

        Self { config, layers }
    }

    /// Apply LoRA to all layers with specified parameters
    pub fn apply_lora(&mut self, rank: usize, alpha: f32) {
        // Recreate layers with new LoRA parameters
        self.layers.clear();
        for _ in 0..self.config.num_layers {
            self.layers.push(LoRALinear::new(
                self.config.hidden_size,
                self.config.hidden_size,
                rank,
                alpha,
            ));
        }
    }

    /// Get all trainable parameters (LoRA adapters only)
    pub fn trainable_parameters(&self) -> Vec<Tensor> {
        let mut params = Vec::new();
        for layer in &self.layers {
            params.extend(layer.trainable_parameters().iter().map(|t| (*t).clone()));
        }
        params
    }

    /// Get model configuration
    pub fn config(&self) -> &ModelConfig {
        &self.config
    }
}

impl Module for SimpleTransformer {
    fn forward(&self, input: &Tensor) -> Result<Tensor> {
        let mut x = input.clone();

        // Pass through each layer
        for layer in &self.layers {
            x = layer.forward(&x)?;
        }

        Ok(x)
    }

    fn parameters(&self) -> Vec<Tensor> {
        self.trainable_parameters()
    }
}
