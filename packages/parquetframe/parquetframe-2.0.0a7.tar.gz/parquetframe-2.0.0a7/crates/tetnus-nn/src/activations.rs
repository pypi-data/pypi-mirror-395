use crate::module::Module;
use crate::Result;
use tetnus_core::{Tensor, ops};

/// Rectified Linear Unit
#[derive(Default, Clone)]
pub struct ReLU;

impl ReLU {
    pub fn new() -> Self {
        Self
    }
}

impl Module for ReLU {
    fn forward(&self, input: &Tensor) -> Result<Tensor> {
        ops::elementwise::relu(input).map_err(|e| e.into())
    }

    fn parameters(&self) -> Vec<Tensor> {
        vec![]
    }
}
