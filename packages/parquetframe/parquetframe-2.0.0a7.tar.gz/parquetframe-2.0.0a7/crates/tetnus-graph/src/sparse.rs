use tetnus_core::Tensor;

/// A sparse tensor in COO (Coordinate) format.
/// Used for efficient storage of graph adjacency matrices.
#[derive(Clone)]
pub struct SparseTensor {
    pub indices: Tensor, // Shape [2, N] (row_indices, col_indices)
    pub values: Tensor,  // Shape [N]
    pub shape: Vec<usize>, // [rows, cols]
}

impl SparseTensor {
    pub fn new(indices: Tensor, values: Tensor, shape: Vec<usize>) -> Self {
        // TODO: Add validation
        Self {
            indices,
            values,
            shape,
        }
    }

    /// Performs sparse-dense matrix multiplication: A * B
    /// A is this sparse tensor (N x M)
    /// B is a dense tensor (M x K)
    /// Result is a dense tensor (N x K)
    pub fn matmul(&self, _other: &Tensor) -> Tensor {
        // Placeholder for actual sparse kernel implementation.
        // In a real implementation, this would call a CUDA/C++ kernel.
        // For now, we'll just return a dummy tensor or implement a slow CPU version if needed.
        // Given the scope, we will define the API surface.

        // Logic:
        // Gather rows from B based on col_indices of A
        // Scale by values of A
        // Scatter_add into result based on row_indices of A

        // For this prototype, we panic to indicate it's a stub,
        // or return a zero tensor of correct shape if we want to be "safe" but incorrect.
        // Let's return a zero tensor for now to allow compilation/linking without crashing immediately.

        // let (rows, cols) = (self.shape[0], self.shape[1]);
        // let other_shape = other.shape();
        // let K = other_shape[1];

        // tetnus_core::ops::zeros(&[rows, K])
        todo!("Sparse matmul not yet implemented")
    }
}
