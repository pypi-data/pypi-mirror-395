use crate::module::Module;
use crate::{Result, TetnusNnError};
use tetnus_core::{Tensor, ops};

/// Embedding layer: Lookup table for categorical embeddings
///
/// Maps integer indices to dense vectors.
#[derive(Clone)]
pub struct Embedding {
    num_embeddings: usize,
    embedding_dim: usize,
    weight: Tensor,
}

impl Embedding {
    /// Create a new Embedding layer.
    ///
    /// # Arguments
    /// * `num_embeddings` - Size of the dictionary of embeddings
    /// * `embedding_dim` - The size of each embedding vector
    pub fn new(num_embeddings: usize, embedding_dim: usize) -> Result<Self> {
        // Initialize with normal distribution
        let mut weight = Tensor::randn(vec![num_embeddings, embedding_dim])?;
        weight = weight.requires_grad_();

        Ok(Embedding {
            num_embeddings,
            embedding_dim,
            weight,
        })
    }
}

impl Module for Embedding {
    fn forward(&self, input: &Tensor) -> Result<Tensor> {
        // Input should be indices (integers).
        // For now, we assume input is a Tensor of floats (since we only have float tensors)
        // and we cast them to indices.
        // Shape: [Batch, Seq] -> [Batch, Seq, Dim] or [Batch] -> [Batch, Dim]

        // Note: tetnus-core currently lacks a "Gather" or "Take" op with autograd.
        // We will implement a simple forward pass using data copying for now,
        // but this will NOT have proper autograd until we implement GatherOp in tetnus-core.
        // Alternatively, we can simulate it with one-hot * matrix_mul if memory allows (very expensive).
        //
        // Given the constraints, I will implement a basic Gather operation here
        // or stub it.
        // Let's assume we can implement a GatherOp in tetnus-core later.
        // For this task, I'll implement a "soft" lookup by assuming we verify autograd for this later
        // or implement a naive MatMul approach (OneHot @ Weight).

        // Naive Autograd-Safe Approach (One-Hot Encoding):
        // 1. Convert indices to One-Hot vectors: [Batch] -> [Batch, NumEmbeddings]
        // 2. MatMul: [Batch, NumEmbeddings] @ [NumEmbeddings, Dim] -> [Batch, Dim]
        // This works with existing MatMul autograd!

        let input_data = input.data();
        let input_shape = input.shape();
        let batch_size: usize = input_shape.iter().product();

        // Create One-Hot matrix
        let mut one_hot_data = vec![0.0; batch_size * self.num_embeddings];
        for (i, &val) in input_data.iter().enumerate() {
            let idx = val as usize;
            if idx >= self.num_embeddings {
                return Err(TetnusNnError::InvalidInput(format!(
                    "Index {} out of bounds for embedding size {}",
                    idx, self.num_embeddings
                )));
            }
            one_hot_data[i * self.num_embeddings + idx] = 1.0;
        }

        let one_hot_shape = if input.ndim() == 1 {
            vec![input_shape[0], self.num_embeddings]
        } else {
            // Flatten batch for matmul then reshape back?
            // MatMul requires 2D. Let's assume 1D input [Batch] for now.
            vec![batch_size, self.num_embeddings]
        };

        // Note: One-Hot tensor does NOT require grad (it's data derived).
        let one_hot = Tensor::new(one_hot_data, one_hot_shape)?;

        // Perform MatMul: [Batch, Num] @ [Num, Dim] -> [Batch, Dim]
        let output = ops::matmul::matmul(&one_hot, &self.weight)?;

        // If input was multidimensional (e.g. [Batch, Seq]), we would reshape output here.
        // For now, output is [Batch*Seq, Dim].

        Ok(output)
    }

    fn parameters(&self) -> Vec<Tensor> {
        vec![self.weight.clone()]
    }
}
