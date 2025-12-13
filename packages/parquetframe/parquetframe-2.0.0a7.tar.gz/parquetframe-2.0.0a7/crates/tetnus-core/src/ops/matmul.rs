/// Matrix multiplication operation with gradient support

use crate::{Tensor, Result, TetnusError, ops::{Op, with_graph}};
use crate::kernels::cpu;
use std::sync::Arc;

pub struct MatMulOp {
    // Store input shapes and values for backward pass
    a: Tensor,
    b: Tensor,
}

impl MatMulOp {
    pub fn new(a: &Tensor, b: &Tensor) -> Self {
        Self {
            a: a.clone(),
            b: b.clone(),
        }
    }
}

impl Op for MatMulOp {
    fn forward(&self, inputs: &[&Tensor]) -> Result<Tensor> {
        if inputs.len() != 2 {
            return Err(TetnusError::InvalidOperation(
                "MatMul requires exactly 2 inputs".to_string()
            ));
        }

        let a = inputs[0];
        let b = inputs[1];

        // Validate shapes: (m, k) @ (k, n) = (m, n)
        if a.ndim() != 2 || b.ndim() != 2 {
            return Err(TetnusError::DimensionError(
                "MatMul requires 2D tensors".to_string()
            ));
        }

        let a_shape = a.shape();
        let b_shape = b.shape();

        if a_shape[1] != b_shape[0] {
            return Err(TetnusError::ShapeMismatch {
                expected: vec![a_shape[0], a_shape[1], a_shape[1], b_shape[1]],
                actual: vec![a_shape[0], a_shape[1], b_shape[0], b_shape[1]],
            });
        }

        let m = a_shape[0];
        let k = a_shape[1];
        let n = b_shape[1];

        // Get data
        let a_data = a.data();
        let b_data = b.data();
        let mut c_data = vec![0.0; m * n];

        // Compute C = A @ B
        cpu::cpu_matmul(&a_data, &b_data, &mut c_data, m, k, n);

        Tensor::new(c_data, vec![m, n])
    }

    fn backward(&self, grad_output: &Tensor) -> Result<Vec<Tensor>> {
        // For C = A @ B:
        // dL/dA = dL/dC @ B^T   (m, n) @ (n, k) = (m, k)
        // dL/dB = A^T @ dL/dC   (k, m) @ (m, n) = (k, n)

        let a_shape = self.a.shape();
        let b_shape = self.b.shape();
        let m = a_shape[0];
        let k = a_shape[1];
        let n = b_shape[1];

        let grad_c = grad_output.data();
        let a_data = self.a.data();
        let b_data = self.b.data();

        // dL/dA = dL/dC @ B^T
        // Need to transpose B: (k, n) -> (n, k)
        let mut b_t = vec![0.0; k * n];
        for i in 0..k {
            for j in 0..n {
                b_t[j * k + i] = b_data[i * n + j];
            }
        }
        let mut grad_a = vec![0.0; m * k];
        cpu::cpu_matmul(&grad_c, &b_t, &mut grad_a, m, n, k);

        // dL/dB = A^T @ dL/dC
        // Need to transpose A: (m, k) -> (k, m)
        let mut a_t = vec![0.0; m * k];
        for i in 0..m {
            for j in 0..k {
                a_t[j * m + i] = a_data[i * k + j];
            }
        }
        let mut grad_b = vec![0.0; k * n];
        cpu::cpu_matmul(&a_t, &grad_c, &mut grad_b, k, m, n);

        Ok(vec![
            Tensor::new(grad_a, vec![m, k])?,
            Tensor::new(grad_b, vec![k, n])?,
        ])
    }

    fn name(&self) -> &str {
        "matmul"
    }
}

/// Helper function to perform matrix multiplication
pub fn matmul(a: &Tensor, b: &Tensor) -> Result<Tensor> {
    let op = MatMulOp::new(a, b);
    let result = op.forward(&[a, b])?;

    Ok(with_graph(result, Arc::new(op), vec![a.clone(), b.clone()]))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_matmul_forward() {
        // 2x3 @ 3x2 = 2x2
        let a = Tensor::new(
            vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            vec![2, 3]
        ).unwrap();
        let b = Tensor::new(
            vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            vec![3, 2]
        ).unwrap();

        let c = matmul(&a, &b).unwrap();

        assert_eq!(c.shape(), &[2, 2]);
        let data = c.data();

        // Expected: [[22, 28], [49, 64]]
        assert_eq!(data[0], 22.0);
        assert_eq!(data[1], 28.0);
        assert_eq!(data[2], 49.0);
        assert_eq!(data[3], 64.0);
    }

    #[test]
    fn test_matmul_requires_grad() {
        let a = Tensor::ones(vec![2, 3]).unwrap().requires_grad_();
        let b = Tensor::ones(vec![3, 2]).unwrap();

        let c = matmul(&a, &b).unwrap();

        assert!(c.0.requires_grad);
        assert!(c.0.op.is_some());
        assert_eq!(c.0.inputs.len(), 2);
    }
}
