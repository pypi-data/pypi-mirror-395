use crate::module::Module;
use crate::Result;
use tetnus_core::{Tensor, ops};
use tetnus_core::ops::Op;
use crate::norm::LayerNorm;
use crate::embedding::Embedding;

/// Numerical Processor
///
/// Preprocesses numerical features:
/// 1. (Optional) Imputes missing values (TODO)
/// 2. Normalizes: (x - mu) / sigma (Learnable LayerNorm)
#[derive(Clone)]
pub struct NumericalProcessor {
    norm: LayerNorm,
}

impl NumericalProcessor {
    /// Create new NumericalProcessor
    pub fn new() -> Result<Self> {
        // For scalar input features, we normalize [Batch, 1]
        // So normalized_shape = [1]
        Ok(NumericalProcessor {
            norm: LayerNorm::new(vec![1], 1e-5)?,
        })
    }
}

impl Module for NumericalProcessor {
    fn forward(&self, input: &Tensor) -> Result<Tensor> {
        // Input: [Batch, 1] or [Batch]
        let mut x = input.clone();
        if x.ndim() == 1 {
            // Reshape to [Batch, 1]
            let op = ops::view::ReshapeOp::new(x.shape().to_vec(), vec![x.numel(), 1]);
            x = op.forward(&[&x])?;
        }

        // Apply LayerNorm
        self.norm.forward(&x)
    }

    fn parameters(&self) -> Vec<Tensor> {
        self.norm.parameters()
    }
}

/// Categorical Processor
///
/// Preprocesses categorical features:
/// 1. (Optional) Hashes string to index (TODO: outside tensor graph for now)
/// 2. Embeds index: [Batch] -> [Batch, EmbedDim]
#[derive(Clone)]
pub struct CategoricalProcessor {
    embedding: Embedding,
}

impl CategoricalProcessor {
    pub fn new(num_categories: usize, embedding_dim: usize) -> Result<Self> {
        Ok(CategoricalProcessor {
            embedding: Embedding::new(num_categories, embedding_dim)?,
        })
    }
}

impl Module for CategoricalProcessor {
    fn forward(&self, input: &Tensor) -> Result<Tensor> {
        // Input: [Batch] indices
        self.embedding.forward(input)
    }

    fn parameters(&self) -> Vec<Tensor> {
        self.embedding.parameters()
    }
}
