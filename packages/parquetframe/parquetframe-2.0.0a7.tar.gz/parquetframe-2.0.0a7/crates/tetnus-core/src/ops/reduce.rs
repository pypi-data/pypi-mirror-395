/// Reduction operations

use crate::{Tensor, Result, TetnusError, ops::{Op, with_graph}};
use crate::kernels::cpu;
use std::sync::Arc;

pub struct SumOp {
    input_shape: Vec<usize>,
}

impl SumOp {
    pub fn new(input_shape: Vec<usize>) -> Self {
        Self { input_shape }
    }
}

impl Op for SumOp {
    fn forward(&self, inputs: &[&Tensor]) -> Result<Tensor> {
        if inputs.len() != 1 {
            return Err(TetnusError::InvalidOperation(
                "Sum requires exactly 1 input".to_string()
            ));
        }

        let input = inputs[0];
        let data = input.data();
        let sum_val = cpu::cpu_sum(&data);

        // Return scalar (shape [1])
        let result = Tensor::new(vec![sum_val], vec![1])?;

        Ok(with_graph(result, Arc::new(SumOp::new(input.shape().to_vec())), inputs.iter().map(|&t| t.clone()).collect()))
    }

    fn backward(&self, grad_output: &Tensor) -> Result<Vec<Tensor>> {
        // Sum gradient broadcasts to all input elements
        let grad_data = grad_output.data();
        if grad_data.is_empty() {
            return Err(TetnusError::GradientError("Empty gradient".to_string()));
        }

        let grad_val = grad_data[0];
        let numel: usize = self.input_shape.iter().product();
        let grad_input = Tensor::new(vec![grad_val; numel], self.input_shape.clone())?;

        Ok(vec![grad_input])
    }

    fn name(&self) -> &str {
        "sum"
    }
}

pub struct MeanOp {
    input_shape: Vec<usize>,
}

impl MeanOp {
    pub fn new(input_shape: Vec<usize>) -> Self {
        Self { input_shape }
    }
}

impl Op for MeanOp {
    fn forward(&self, inputs: &[&Tensor]) -> Result<Tensor> {
        if inputs.len() != 1 {
            return Err(TetnusError::InvalidOperation(
                "Mean requires exactly 1 input".to_string()
            ));
        }

        let input = inputs[0];
        let data = input.data();
        let sum_val = cpu::cpu_sum(&data);
        let mean_val = sum_val / data.len() as f32;

        let result = Tensor::new(vec![mean_val], vec![1])?;

        Ok(with_graph(result, Arc::new(MeanOp::new(input.shape().to_vec())), inputs.iter().map(|&t| t.clone()).collect()))
    }

    fn backward(&self, grad_output: &Tensor) -> Result<Vec<Tensor>> {
        let grad_data = grad_output.data();
        if grad_data.is_empty() {
            return Err(TetnusError::GradientError("Empty gradient".to_string()));
        }

        let grad_val = grad_data[0];
        let numel: usize = self.input_shape.iter().product();
        let n = numel as f32;

        // Gradient is grad_val / N for every element
        let grad_elem = grad_val / n;
        let grad_input_data = vec![grad_elem; numel];

        let grad_input = Tensor::new(grad_input_data, self.input_shape.clone())?;

        Ok(vec![grad_input])
    }

    fn name(&self) -> &str {
        "mean"
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sum() {
        let t = Tensor::new(vec![1.0, 2.0, 3.0, 4.0], vec![4]).unwrap();
        let op = SumOp::new(vec![4]);

        let result = op.forward(&[&t]).unwrap();

        assert_eq!(result.shape(), &[1]);
        assert_eq!(result.data()[0], 10.0);
    }

    #[test]
    fn test_mean() {
        let t = Tensor::new(vec![2.0, 4.0, 6.0, 8.0], vec![4]).unwrap();
        let op = MeanOp::new(vec![4]);

        let result = op.forward(&[&t]).unwrap();
        assert_eq!(result.data()[0], 5.0);
    }
}
