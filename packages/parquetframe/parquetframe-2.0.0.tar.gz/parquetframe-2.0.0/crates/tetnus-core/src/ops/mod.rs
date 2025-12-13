/// Computation graph operations

use crate::{Tensor, Result};

use std::sync::Arc;

/// Trait for differentiable operations
pub trait Op: Send + Sync {
    /// Forward pass: compute the output
    fn forward(&self, inputs: &[&Tensor]) -> Result<Tensor>;

    /// Backward pass: compute gradients for inputs given output gradient
    fn backward(&self, grad_output: &Tensor) -> Result<Vec<Tensor>>;

    /// Name of the operation (for debugging)
    fn name(&self) -> &str;
}

/// Helper to attach computation graph to a result if inputs require grad
pub fn with_graph(result: Tensor, op: Arc<dyn Op>, inputs: Vec<Tensor>) -> Tensor {
    if inputs.iter().any(|x| x.0.requires_grad) {
        let internal = &*result.0;
        Tensor(Arc::new(crate::tensor::TensorInternal {
            data: Arc::clone(&internal.data),
            shape: internal.shape.clone(),
            strides: internal.strides.clone(),
            offset: internal.offset,
            device: internal.device,
            requires_grad: true,
            grad: parking_lot::Mutex::new(None),
            op: Some(op),
            inputs,
        }))
    } else {
        result
    }
}

// Stub implementations - will be filled in next
pub mod elementwise;
pub mod matmul;
pub mod reduce;
pub mod view;
