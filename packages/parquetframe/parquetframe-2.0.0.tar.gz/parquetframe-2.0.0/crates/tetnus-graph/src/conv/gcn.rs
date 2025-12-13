use tetnus_core::Tensor;
use tetnus_nn::module::Module;
use tetnus_nn::{Result, TetnusNnError};
use tetnus_nn::linear::Linear;
use crate::sparse::SparseTensor;

pub struct GCNConv {
    pub lin: Linear,
}

impl GCNConv {
    pub fn new(in_channels: usize, out_channels: usize) -> Self {
        Self {
            lin: Linear::new(in_channels, out_channels, true).expect("Failed to create Linear layer"),
        }
    }

    pub fn forward(&self, x: &Tensor, edge_index: &SparseTensor) -> Tensor {
        // Formula: H' = A * H * W
        // 1. Linear transformation: H_tmp = H * W (using self.lin)
        let h_tmp = self.lin.forward(x).expect("Linear forward failed");

        // 2. Sparse multiplication: H' = A * H_tmp
        // Note: In standard GCN, A is normalized (D^-0.5 * A * D^-0.5).
        // We assume edge_index is already normalized or we do it here.
        // For this MVP, we just do raw matmul.
        edge_index.matmul(&h_tmp)
    }
}

impl Module for GCNConv {
    fn forward(&self, _input: &Tensor) -> Result<Tensor> {
        // GCNConv requires edge_index, so it cannot be used with the standard Module::forward
        // which only takes a single input.
        Err(TetnusNnError::InvalidInput("GCNConv requires edge_index. Use GCNConv::forward(x, edge_index) instead.".into()))
    }

    fn parameters(&self) -> Vec<Tensor> {
        self.lin.parameters()
    }
}
