use crate::module::Module;
use crate::{Result, TetnusNnError};
use tetnus_core::{Tensor, ops};
use tetnus_core::ops::Op;

/// A fully connected linear layer: y = xA^T + b
#[derive(Clone)]
pub struct Linear {
    weight: Tensor,
    bias: Option<Tensor>,
}

impl Linear {
    /// Create a new Linear layer.
    ///
    /// # Arguments
    /// * `in_features` - Size of each input sample
    /// * `out_features` - Size of each output sample
    /// * `bias` - If set to false, the layer will not learn an additive bias.
    pub fn new(in_features: usize, out_features: usize, bias: bool) -> Result<Self> {
        // Kaiming initialization or similar would be better, but using randn for now
        let mut weight = Tensor::randn(vec![out_features, in_features])?;
        weight = weight.requires_grad_();

        let bias_tensor = if bias {
            let mut b = Tensor::zeros(vec![out_features])?;
            b = b.requires_grad_();
            Some(b)
        } else {
            None
        };

        Ok(Linear {
            weight,
            bias: bias_tensor,
        })
    }
}

impl Module for Linear {
    fn forward(&self, input: &Tensor) -> Result<Tensor> {
        // y = input @ weight.T + bias

        // Transpose weight: [Out, In] -> [In, Out]
        let transpose_op = ops::view::TransposeOp::new(self.weight.shape().to_vec());
        let w_t = transpose_op.forward(&[&self.weight])?;

        // Matmul
        let mut output = ops::matmul::matmul(input, &w_t)?;

        if let Some(b) = &self.bias {
            // Broadcast add
            // Current tetnus-core::add requires exact shape match.
            // We broadcast bias [Out] -> [Batch, Out] using MatMul: Ones(Batch, 1) @ Bias(1, Out)
            let batch_size = output.shape()[0];
            let out_features = output.shape()[1];

            if b.shape()[0] != out_features {
                 return Err(TetnusNnError::InvalidInput(format!(
                    "Bias shape {:?} does not match output features {}",
                    b.shape(), out_features
                )));
            }

            // 1. Create ones [Batch, 1]
            let ones = Tensor::ones(vec![batch_size, 1])?;

            // 2. Reshape bias [Out] -> [1, Out]
            // We must use the Op to ensure the graph is built
            let reshape_op = ops::view::ReshapeOp::new(b.shape().to_vec(), vec![1, out_features]);
            let b_reshaped = reshape_op.forward(&[b])?;

            // 3. Broadcast via MatMul -> [Batch, Out]
            // This connects bias to the computation graph
            let bias_broadcast = ops::matmul::matmul(&ones, &b_reshaped)?;

            // 4. Add
            output = ops::elementwise::add(&output, &bias_broadcast)?;
        }

        Ok(output)
    }

    fn parameters(&self) -> Vec<Tensor> {
        let mut params = vec![self.weight.clone()];
        if let Some(b) = &self.bias {
            params.push(b.clone());
        }
        params
    }
}
