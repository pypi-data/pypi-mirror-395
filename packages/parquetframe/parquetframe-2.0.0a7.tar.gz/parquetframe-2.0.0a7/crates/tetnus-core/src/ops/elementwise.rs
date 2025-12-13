/// Element-wise operations

use crate::{Tensor, Result, TetnusError, ops::{Op, with_graph}};
use crate::kernels::cpu;
use std::sync::Arc;

pub struct AddOp;

impl Op for AddOp {
    fn forward(&self, inputs: &[&Tensor]) -> Result<Tensor> {
        if inputs.len() != 2 {
            return Err(TetnusError::InvalidOperation(
                "Add requires exactly 2 inputs".to_string()
            ));
        }

        let a = inputs[0];
        let b = inputs[1];

        // Check shapes match
        if a.shape() != b.shape() {
            return Err(TetnusError::ShapeMismatch {
                expected: a.shape().to_vec(),
                actual: b.shape().to_vec(),
            });
        }

        let a_data = a.data();
        let b_data = b.data();
        let mut c_data = vec![0.0; a.numel()];

        cpu::cpu_add(&a_data, &b_data, &mut c_data);

        Tensor::new(c_data, a.shape().to_vec())
    }

    fn backward(&self, grad_output: &Tensor) -> Result<Vec<Tensor>> {
        // For C = A + B:
        // dL/dA = dL/dC (gradient flows equally)
        // dL/dB = dL/dC
        Ok(vec![grad_output.clone(), grad_output.clone()])
    }

    fn name(&self) -> &str {
        "add"
    }
}

pub struct SubOp;

impl Op for SubOp {
    fn forward(&self, inputs: &[&Tensor]) -> Result<Tensor> {
        if inputs.len() != 2 {
            return Err(TetnusError::InvalidOperation(
                "Sub requires exactly 2 inputs".to_string()
            ));
        }

        let a = inputs[0];
        let b = inputs[1];

        if a.shape() != b.shape() {
            return Err(TetnusError::ShapeMismatch {
                expected: a.shape().to_vec(),
                actual: b.shape().to_vec(),
            });
        }

        let a_data = a.data();
        let b_data = b.data();
        let mut c_data = vec![0.0; a.numel()];

        cpu::cpu_sub(&a_data, &b_data, &mut c_data);

        Tensor::new(c_data, a.shape().to_vec())
    }

    fn backward(&self, grad_output: &Tensor) -> Result<Vec<Tensor>> {
        // For C = A - B:
        // dL/dA = dL/dC
        // dL/dB = -dL/dC
        let grad_data = grad_output.data();

        // Negate gradient for B
        let grad_b_data: Vec<f32> = grad_data.iter().map(|&x| -x).collect();

        Ok(vec![
            grad_output.clone(),
            Tensor::new(grad_b_data, grad_output.shape().to_vec())?,
        ])
    }

    fn name(&self) -> &str {
        "sub"
    }
}

pub struct MulOp {
    // Store inputs for backward pass
    a: Tensor,
    b: Tensor,
}

impl MulOp {
    pub fn new(a: &Tensor, b: &Tensor) -> Self {
        Self {
            a: a.clone(),
            b: b.clone(),
        }
    }
}

impl Op for MulOp {
    fn forward(&self, inputs: &[&Tensor]) -> Result<Tensor> {
        if inputs.len() != 2 {
            return Err(TetnusError::InvalidOperation(
                "Mul requires exactly 2 inputs".to_string()
            ));
        }

        let a = inputs[0];
        let b = inputs[1];

        if a.shape() != b.shape() {
            return Err(TetnusError::ShapeMismatch {
                expected: a.shape().to_vec(),
                actual: b.shape().to_vec(),
            });
        }

        let a_data = a.data();
        let b_data = b.data();
        let mut c_data = vec![0.0; a.numel()];

        cpu::cpu_mul(&a_data, &b_data, &mut c_data);

        Tensor::new(c_data, a.shape().to_vec())
    }

    fn backward(&self, grad_output: &Tensor) -> Result<Vec<Tensor>> {
        // For C = A * B:
        // dL/dA = dL/dC * B
        // dL/dB = dL/dC * A
        let grad_a_data = grad_output.data();
        let b_data = self.b.data();
        let mut grad_a = vec![0.0; grad_a_data.len()];
        cpu::cpu_mul(&grad_a_data, &b_data, &mut grad_a);

        let a_data = self.a.data();
        let mut grad_b = vec![0.0; grad_a_data.len()];
        cpu::cpu_mul(&grad_a_data, &a_data, &mut grad_b);

        Ok(vec![
            Tensor::new(grad_a, self.a.shape().to_vec())?,
            Tensor::new(grad_b, self.b.shape().to_vec())?,
        ])
    }

    fn name(&self) -> &str {
        "mul"
    }
}

pub struct DivOp {
    a: Tensor,
    b: Tensor,
}

impl DivOp {
    pub fn new(a: &Tensor, b: &Tensor) -> Self {
        Self {
            a: a.clone(),
            b: b.clone(),
        }
    }
}

impl Op for DivOp {
    fn forward(&self, inputs: &[&Tensor]) -> Result<Tensor> {
        if inputs.len() != 2 {
            return Err(TetnusError::InvalidOperation(
                "Div requires exactly 2 inputs".to_string()
            ));
        }

        let a = inputs[0];
        let b = inputs[1];

        if a.shape() != b.shape() {
            return Err(TetnusError::ShapeMismatch {
                expected: a.shape().to_vec(),
                actual: b.shape().to_vec(),
            });
        }

        let a_data = a.data();
        let b_data = b.data();
        let mut c_data = vec![0.0; a.numel()];

        cpu::cpu_div(&a_data, &b_data, &mut c_data);

        Tensor::new(c_data, a.shape().to_vec())
    }

    fn backward(&self, grad_output: &Tensor) -> Result<Vec<Tensor>> {
        // For C = A / B:
        // dL/dA = dL/dC / B
        // dL/dB = -dL/dC * A / B^2
        let grad_c = grad_output.data();
        let a_data = self.a.data();
        let b_data = self.b.data();

        let mut grad_a = vec![0.0; grad_c.len()];
        let mut grad_b = vec![0.0; grad_c.len()];

        // Need parallel iterator? Using simple loop for now or iter if small.
        // Since cpu kernels use rayon, we should probably use standard iter for clarity unless performance critical here.
        // Actually, zip everything.
        for i in 0..grad_c.len() {
            let g = grad_c[i];
            let a_val = a_data[i];
            let b_val = b_data[i];

            // dL/dA = g / b
            grad_a[i] = g / b_val;

            // dL/dB = -g * a / b^2
            grad_b[i] = -g * a_val / (b_val * b_val);
        }

        Ok(vec![
            Tensor::new(grad_a, self.a.shape().to_vec())?,
            Tensor::new(grad_b, self.b.shape().to_vec())?,
        ])
    }

    fn name(&self) -> &str {
        "div"
    }
}

/// Helper functions
pub fn add(a: &Tensor, b: &Tensor) -> Result<Tensor> {
    let op = AddOp;
    let result = op.forward(&[a, b])?;

    Ok(with_graph(result, Arc::new(op), vec![a.clone(), b.clone()]))
}

pub fn sub(a: &Tensor, b: &Tensor) -> Result<Tensor> {
    let op = SubOp;
    let result = op.forward(&[a, b])?;

    Ok(with_graph(result, Arc::new(op), vec![a.clone(), b.clone()]))
}

pub fn mul(a: &Tensor, b: &Tensor) -> Result<Tensor> {
    let op = MulOp::new(a, b);
    let result = op.forward(&[a, b])?;

    Ok(with_graph(result, Arc::new(op), vec![a.clone(), b.clone()]))
}

pub fn div(a: &Tensor, b: &Tensor) -> Result<Tensor> {
    let op = DivOp::new(a, b);
    let result = op.forward(&[a, b])?;

    Ok(with_graph(result, Arc::new(op), vec![a.clone(), b.clone()]))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        let a = Tensor::new(vec![1.0, 2.0, 3.0], vec![3]).unwrap();
        let b = Tensor::new(vec![4.0, 5.0, 6.0], vec![3]).unwrap();

        let c = add(&a, &b).unwrap();

        assert_eq!(c.data(), vec![5.0, 7.0, 9.0]);
    }

    #[test]
    fn test_mul() {
        let a = Tensor::new(vec![2.0, 3.0, 4.0], vec![3]).unwrap();
        let b = Tensor::new(vec![5.0, 6.0, 7.0], vec![3]).unwrap();

        let c = mul(&a, &b).unwrap();

        assert_eq!(c.data(), vec![10.0, 18.0, 28.0]);
    }

    #[test]
    fn test_sin() {
        let a = Tensor::new(vec![0.0, std::f32::consts::PI / 2.0, std::f32::consts::PI], vec![3]).unwrap();
        let c = sin(&a).unwrap();
        let data = c.data();

        assert!((data[0] - 0.0).abs() < 1e-6);
        assert!((data[1] - 1.0).abs() < 1e-6);
        assert!((data[2] - 0.0).abs() < 1e-6);
    }

    #[test]
    fn test_cos() {
        let a = Tensor::new(vec![0.0, std::f32::consts::PI / 2.0, std::f32::consts::PI], vec![3]).unwrap();
        let c = cos(&a).unwrap();
        let data = c.data();

        assert!((data[0] - 1.0).abs() < 1e-6);
        assert!((data[1] - 0.0).abs() < 1e-6);
        assert!((data[2] - (-1.0)).abs() < 1e-6);
    }

    #[test]
    fn test_exp() {
        let a = Tensor::new(vec![0.0, 1.0, 2.0], vec![3]).unwrap();
        let c = exp(&a).unwrap();
        let data = c.data();

        assert!((data[0] - 1.0).abs() < 1e-6);
        assert!((data[1] - std::f32::consts::E).abs() < 1e-6);
        assert!((data[2] - (std::f32::consts::E * std::f32::consts::E)).abs() < 1e-5);
    }

    #[test]
    fn test_log() {
        let a = Tensor::new(vec![1.0, std::f32::consts::E, 10.0], vec![3]).unwrap();
        let c = log(&a).unwrap();
        let data = c.data();

        assert!((data[0] - 0.0).abs() < 1e-6);
        assert!((data[1] - 1.0).abs() < 1e-6);
        assert!((data[2] - 10.0_f32.ln()).abs() < 1e-6);
    }

    #[test]
    fn test_sqrt() {
        let a = Tensor::new(vec![1.0, 4.0, 9.0, 16.0], vec![4]).unwrap();
        let c = sqrt(&a).unwrap();
        let data = c.data();

        assert_eq!(data, vec![1.0, 2.0, 3.0, 4.0]);
    }
}

/// Unary operation for mathematical functions
pub struct UnaryOp {
    name: String,
    forward_fn: fn(f32) -> f32,
    backward_fn: fn(f32, f32) -> f32,  // (input, grad_output) -> grad_input
    input: Tensor,
}

impl UnaryOp {
    pub fn new(
        name: String,
        forward_fn: fn(f32) -> f32,
        backward_fn: fn(f32, f32) -> f32,
        input: &Tensor,
    ) -> Self {
        Self {
            name,
            forward_fn,
            backward_fn,
            input: input.clone(),
        }
    }
}

impl Op for UnaryOp {
    fn forward(&self, inputs: &[&Tensor]) -> Result<Tensor> {
        if inputs.len() != 1 {
            return Err(TetnusError::InvalidOperation(
                format!("{} requires exactly 1 input", self.name)
            ));
        }

        let a = inputs[0];
        let a_data = a.data();
        let c_data: Vec<f32> = a_data.iter().map(|&x| (self.forward_fn)(x)).collect();

        Tensor::new(c_data, a.shape().to_vec())
    }

    fn backward(&self, grad_output: &Tensor) -> Result<Vec<Tensor>> {
        let input_data = self.input.data();
        let grad_data = grad_output.data();
        let grad_input: Vec<f32> = input_data
            .iter()
            .zip(grad_data.iter())
            .map(|(&x, &g)| (self.backward_fn)(x, g))
            .collect();

        Ok(vec![Tensor::new(grad_input, self.input.shape().to_vec())?])
    }

    fn name(&self) -> &str {
        &self.name
    }
}

/// Helper macro for creating unary operations
macro_rules! unary_op {
    ($name:ident, $forward:expr, $backward:expr) => {
        pub fn $name(a: &Tensor) -> Result<Tensor> {
            let op = UnaryOp::new(
                stringify!($name).to_string(),
                $forward,
                $backward,
                a,
            );
            let result = op.forward(&[a])?;

            Ok(with_graph(result, Arc::new(op), vec![a.clone()]))
        }
    };
}

// Trigonometric functions
unary_op!(sin, |x: f32| x.sin(), |x: f32, g: f32| g * x.cos());
unary_op!(cos, |x: f32| x.cos(), |x: f32, g: f32| g * (-x.sin()));
unary_op!(tan, |x: f32| x.tan(), |x: f32, g: f32| {
    let c = x.cos();
    g / (c * c)
});

// Exponential and logarithmic
unary_op!(exp, |x: f32| x.exp(), |x: f32, g: f32| g * x.exp());
unary_op!(log, |x: f32| x.ln(), |_x: f32, g: f32| g / _x);
unary_op!(sqrt, |x: f32| x.sqrt(), |x: f32, g: f32| g / (2.0 * x.sqrt()));

// Activation functions
unary_op!(relu, |x: f32| if x > 0.0 { x } else { 0.0 }, |x: f32, g: f32| if x > 0.0 { g } else { 0.0 });
