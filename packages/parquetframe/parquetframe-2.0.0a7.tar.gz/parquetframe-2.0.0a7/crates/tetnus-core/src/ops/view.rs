/// View operations (reshape, transpose) - zero-copy when possible

use crate::{Tensor, Result, TetnusError, ops::{Op, with_graph}};
use std::sync::Arc;

pub struct ReshapeOp {
    old_shape: Vec<usize>,
    new_shape: Vec<usize>,
}

impl ReshapeOp {
    pub fn new(old_shape: Vec<usize>, new_shape: Vec<usize>) -> Self {
        Self { old_shape, new_shape }
    }
}

impl Op for ReshapeOp {
    fn forward(&self, inputs: &[&Tensor]) -> Result<Tensor> {
        if inputs.len() != 1 {
            return Err(TetnusError::InvalidOperation(
                "Reshape requires exactly 1 input".to_string()
            ));
        }

        let input = inputs[0];
        let old_numel: usize = input.shape().iter().product();
        let new_numel: usize = self.new_shape.iter().product();

        if old_numel != new_numel {
            return Err(TetnusError::InvalidShape(format!(
                "Cannot reshape tensor of {} elements to shape {:?}",
                old_numel, self.new_shape
            )));
        }

        // Reshape is a view operation - just change shape
        let data = input.data();
        let result = Tensor::new(data, self.new_shape.clone())?;

        Ok(with_graph(result, Arc::new(ReshapeOp::new(self.old_shape.clone(), self.new_shape.clone())), inputs.iter().map(|&t| t.clone()).collect()))
    }

    fn backward(&self, grad_output: &Tensor) -> Result<Vec<Tensor>> {
        // Gradient has same shape transformationin reverse
        let grad_data = grad_output.data();
        let grad_input = Tensor::new(grad_data, self.old_shape.clone())?;
        Ok(vec![grad_input])
    }

    fn name(&self) -> &str {
        "reshape"
    }
}

pub struct TransposeOp {
    shape: Vec<usize>,
}

impl TransposeOp {
    pub fn new(shape: Vec<usize>) -> Self {
        Self { shape }
    }
}

impl Op for TransposeOp {
    fn forward(&self, inputs: &[&Tensor]) -> Result<Tensor> {
        if inputs.len() != 1 {
            return Err(TetnusError::InvalidOperation(
                "Transpose requires exactly 1 input".to_string()
            ));
        }

        let input = inputs[0];

        if input.ndim() != 2 {
            return Err(TetnusError::DimensionError(
                "Transpose currently only supports 2D tensors".to_string()
            ));
        }

        let shape = input.shape();
        let m = shape[0];
        let n = shape[1];

        // Simple transpose implementation
        let data = input.data();
        let mut result = vec![0.0; data.len()];
        for i in 0..m {
            for j in 0..n {
                result[j * m + i] = data[i * n + j];
            }
        }

        let result_tensor = Tensor::new(result, vec![n, m])?;

        Ok(with_graph(
            result_tensor,
            Arc::new(TransposeOp::new(self.shape.clone())),
            inputs.iter().map(|&t| t.clone()).collect()
        ))
    }

    fn backward(&self, grad_output: &Tensor) -> Result<Vec<Tensor>> {
        // Transpose gradient is also transposed
        let op = TransposeOp::new(grad_output.shape().to_vec());
        op.forward(&[grad_output])
            .map(|t| vec![t])
    }

    fn name(&self) -> &str {
        "transpose"
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_reshape() {
        let t = Tensor::new(vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0], vec![2, 3]).unwrap();
        let op = ReshapeOp::new(vec![2, 3], vec![3, 2]);

        let reshaped = op.forward(&[&t]).unwrap();

        assert_eq!(reshaped.shape(), &[3, 2]);
        assert_eq!(reshaped.numel(), 6);
    }

    #[test]
    fn test_transpose() {
        let t = Tensor::new(vec![1.0, 2.0, 3.0, 4.0], vec![2, 2]).unwrap();
        let op = TransposeOp::new(vec![2, 2]);

        let transposed = op.forward(&[&t]).unwrap();

        assert_eq!(transposed.shape(), &[2, 2]);
        let data = transposed.data();
        // [[1, 2], [3, 4]]^T = [[1, 3], [2, 4]]
        assert_eq!(data, vec![1.0, 3.0, 2.0, 4.0]);
    }
}
