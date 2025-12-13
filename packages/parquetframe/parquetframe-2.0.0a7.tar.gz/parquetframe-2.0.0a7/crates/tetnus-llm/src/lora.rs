use tetnus_core::{Tensor, ops::matmul::matmul, ops::elementwise::{add, mul}};
use tetnus_nn::{Module, Result, TetnusNnError};

/// LoRA (Low-Rank Adaptation) Linear Layer
///
/// Implements efficient fine-tuning by freezing pretrained weights and adding
/// a low-rank trainable adapter: W' = W + alpha * B * A
///
/// # Mathematical Formulation
/// - Frozen weight: W (d × k)
/// - Low-rank matrices: A (d × r), B (r × k) where r << d, k
/// - Forward: y = x(W + alpha * B * A)
///
/// This dramatically reduces trainable parameters from d*k to (d+k)*r.
pub struct LoRALinear {
    /// Frozen pretrained weight (not trainable)
    frozen_weight: Tensor,
    /// Low-rank matrix A (trainable)
    lora_a: Tensor,
    /// Low-rank matrix B (trainable)
    lora_b: Tensor,
    /// LoRA rank
    rank: usize,
    /// LoRA scaling factor
    alpha: f32,
}

impl LoRALinear {
    /// Create a new LoRA linear layer
    ///
    /// # Arguments
    /// * `in_features` - Input dimension
    /// * `out_features` - Output dimension
    /// * `rank` - LoRA rank (typically 4, 8, 16, or 32)
    /// * `alpha` - LoRA scaling factor (typically 1.0 or equal to rank)
    pub fn new(in_features: usize, out_features: usize, rank: usize, alpha: f32) -> Self {
        // Initialize frozen weight (would typically be loaded from pretrained model)
        let frozen_weight = Tensor::randn(vec![in_features, out_features])
            .expect("Failed to create frozen weight");

        // Initialize LoRA matrices with small random values
        let lora_a = Tensor::randn(vec![in_features, rank])
            .expect("Failed to create LoRA A matrix")
            .requires_grad_();
        let lora_b = Tensor::randn(vec![rank, out_features])
            .expect("Failed to create LoRA B matrix")
            .requires_grad_();

        Self {
            frozen_weight,
            lora_a,
            lora_b,
            rank,
            alpha,
        }
    }

    /// Get trainable parameters (LoRA matrices only)
    pub fn trainable_parameters(&self) -> Vec<&Tensor> {
        vec![&self.lora_a, &self.lora_b]
    }
}

impl Module for LoRALinear {
    fn forward(&self, input: &Tensor) -> Result<Tensor> {
        // Compute LoRA adapter: delta_W = B * A
        let lora_product = matmul(&self.lora_a, &self.lora_b)
            .map_err(|e| TetnusNnError::InvalidInput(format!("LoRA matmul failed: {}", e)))?;

        // Scale by alpha using element-wise multiplication with a scalar tensor
        let alpha_tensor = Tensor::full(lora_product.shape().to_vec(), self.alpha)
            .map_err(|e| TetnusNnError::InvalidInput(format!("Failed to create alpha tensor: {}", e)))?;
        let scaled_lora = mul(&lora_product, &alpha_tensor)
            .map_err(|e| TetnusNnError::InvalidInput(format!("LoRA scaling failed: {}", e)))?;

        // Add to frozen weight: W' = W + alpha * B * A
        let effective_weight = add(&self.frozen_weight, &scaled_lora)
            .map_err(|e| TetnusNnError::InvalidInput(format!("Weight addition failed: {}", e)))?;

        // Apply linear transformation: y = x * W'
        let output = matmul(input, &effective_weight)
            .map_err(|e| TetnusNnError::InvalidInput(format!("Forward matmul failed: {}", e)))?;

        Ok(output)
    }

    fn parameters(&self) -> Vec<Tensor> {
        vec![self.lora_a.clone(), self.lora_b.clone()]
    }
}
