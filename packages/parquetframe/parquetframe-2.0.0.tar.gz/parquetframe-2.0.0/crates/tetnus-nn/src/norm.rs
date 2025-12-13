use crate::module::Module;
use crate::{Result, TetnusNnError};
use tetnus_core::{Tensor, ops};
use tetnus_core::ops::Op;

/// Layer Normalization
///
/// y = (x - mean) / sqrt(var + eps) * gamma + beta
#[derive(Clone)]
pub struct LayerNorm {
    normalized_shape: Vec<usize>,
    eps: f32,
    gamma: Tensor, // weight
    beta: Tensor,  // bias
}

impl LayerNorm {
    pub fn new(normalized_shape: Vec<usize>, eps: f32) -> Result<Self> {
        let numel: usize = normalized_shape.iter().product();

        // Initialize gamma to ones, beta to zeros
        let mut gamma = Tensor::ones(vec![numel])?;
        gamma = gamma.requires_grad_();

        let mut beta = Tensor::zeros(vec![numel])?;
        beta = beta.requires_grad_();

        Ok(LayerNorm {
            normalized_shape,
            eps,
            gamma,
            beta,
        })
    }
}

impl Module for LayerNorm {
    fn forward(&self, input: &Tensor) -> Result<Tensor> {
        // Input: [Batch, Features]
        // 1. Compute mean: [Batch, 1]
        // 2. Compute var: [Batch, 1]
        // 3. Normalize: (x - mean) / sqrt(var + eps)
        // 4. Scale and shift: * gamma + beta

        // Note: We need comprehensive reduction ops (mean, var) along a dimension.
        // tetnus-core's `mean` currently reduces EVERYTHING to a scalar.
        // This is a limitation.
        // For now, we assume the input is [Batch, Features] and we want to normalize over Features.
        // We can hack this if we assume batch_size=1 for testing, or iterate.
        // But for real usage, we need `mean(dim=1)`.

        // Implementing a hacky forward pass for now assuming we can expand this later.
        // Or better: Implement `LayerNorm` as a single Op in tetnus-core if needed.
        // But sticking to composite Ops is better for autograd.

        // Let's assume strict [Batch, Features] input for now.
        let shape = input.shape();
        if shape.len() != 2 {
             return Err(TetnusNnError::InvalidInput("LayerNorm currently only supports 2D inputs".to_string()));
        }
        let batch_size = shape[0];
        let features = shape[1];

        // Manual row-wise mean and variance
        // This is incredibly slow in pure Rust loop without vectorized ops, but works for proof of concept.
        // We need to build the graph though!
        // If we do manual loops, we break the graph unless we use tensor ops for everything.
        // We CANNOT use manual loops for calculating mean if we want gradients to flow through the mean calculation.

        // Workaround:
        // 1. Sum over features (MatMul with Ones vector)
        //    Input: [B, F] @ Ones[F, 1] -> [B, 1] (Sum)
        // 2. Mean = Sum / F

        // 1. Sum
        let ones_col = Tensor::ones(vec![features, 1])?;
        let sum = ops::matmul::matmul(input, &ones_col)?; // [B, 1]

        // 2. Mean
        let f_tensor = Tensor::full(vec![batch_size, 1], features as f32)?;
        let mean = ops::elementwise::div(&sum, &f_tensor)?; // [B, 1]

        // 3. Variance: sum((x - mean)^2) / F
        // Need to broadcast Mean [B, 1] to [B, F].
        // MatMul: Mean [B, 1] @ Ones [1, F] -> [B, F]
        let ones_row = Tensor::ones(vec![1, features])?;
        let mean_expanded = ops::matmul::matmul(&mean, &ones_row)?;

        // x - mean
        let diff = ops::elementwise::sub(input, &mean_expanded)?;

        // (x - mean)^2
        let diff_sq = ops::elementwise::mul(&diff, &diff)?;

        // Sum((x - mean)^2) -> [B, F] @ Ones[F, 1] -> [B, 1]
        let sum_sq = ops::matmul::matmul(&diff_sq, &ones_col)?;

        // Var = SumSq / F
        let var = ops::elementwise::div(&sum_sq, &f_tensor)?;

        // sqrt(var + eps)
        let eps_tensor = Tensor::full(vec![batch_size, 1], self.eps)?;
        let var_eps = ops::elementwise::add(&var, &eps_tensor)?;
        let std_dev = ops::elementwise::sqrt(&var_eps)?;

        // 1 / std_dev
        // We need a generic `inv` op or div(1, std_dev).
        let one_tensor = Tensor::ones(vec![batch_size, 1])?;
        let inv_std = ops::elementwise::div(&one_tensor, &std_dev)?;

        // Broadcast inv_std to [B, F]
        let inv_std_expanded = ops::matmul::matmul(&inv_std, &ones_row)?;

        // Normalized X = (x - mean) * inv_std
        let x_norm = ops::elementwise::mul(&diff, &inv_std_expanded)?;

        // Scale and Shift
        // Gamma [F], Beta [F] need to be broadcast to [B, F]
        // Gamma: Ones [B, 1] @ Gamma [1, F]
        // But Gamma is stored as [F]. Reshape to [1, F].
        let reshape_op = ops::view::ReshapeOp::new(vec![features], vec![1, features]);
        let gamma_reshaped = reshape_op.forward(&[&self.gamma])?;
        let beta_reshaped = reshape_op.forward(&[&self.beta])?;

        let ones_col_batch = Tensor::ones(vec![batch_size, 1])?;
        let gamma_broadcast = ops::matmul::matmul(&ones_col_batch, &gamma_reshaped)?;
        let beta_broadcast = ops::matmul::matmul(&ones_col_batch, &beta_reshaped)?;

        let scaled = ops::elementwise::mul(&x_norm, &gamma_broadcast)?;
        let result = ops::elementwise::add(&scaled, &beta_broadcast)?;

        Ok(result)
    }

    fn parameters(&self) -> Vec<Tensor> {
        vec![self.gamma.clone(), self.beta.clone()]
    }
}
