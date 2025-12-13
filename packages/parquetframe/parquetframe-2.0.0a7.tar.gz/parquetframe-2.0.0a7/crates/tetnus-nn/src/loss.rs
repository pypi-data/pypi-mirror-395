use crate::{Module, Result, TetnusNnError};
use tetnus_core::{Tensor, ops::{self, Op, with_graph}, TetnusError};
use std::sync::Arc;

/// Mean Squared Error Loss
pub struct MSELoss;

impl MSELoss {
    pub fn new() -> Self {
        Self
    }

    pub fn forward(&self, input: &Tensor, target: &Tensor) -> Result<Tensor> {
        if input.shape() != target.shape() {
            return Err(TetnusNnError::InvalidInput(format!(
                "MSELoss: Input shape {:?} does not match target shape {:?}",
                input.shape(), target.shape()
            )));
        }

        // diff = input - target
        let diff = ops::elementwise::sub(input, target)?;

        // sq = diff * diff
        let sq = ops::elementwise::mul(&diff, &diff)?;

        // mean = mean(sq)
        // Note: Current MeanOp reduces everything to scalar
        let op = ops::reduce::MeanOp::new(sq.shape().to_vec());
        let mean_tensor = op.forward(&[&sq])?;

        // We need to construct the graph manually for the mean op since we called forward directly
        // Or use a helper if available. tetnus-core doesn't expose a 'mean' helper in reduce yet?
        // Let's check if there is a helper. If not, we use with_graph.

        Ok(with_graph(mean_tensor, Arc::new(op), vec![sq]))
    }
}

/// Cross Entropy Loss (with built-in Softmax)
/// Expects logits and one-hot targets (or probabilities)
pub struct CrossEntropyLoss;

impl CrossEntropyLoss {
    pub fn new() -> Self {
        Self
    }

    pub fn forward(&self, input: &Tensor, target: &Tensor) -> Result<Tensor> {
        // Input: [Batch, Classes]
        // Target: [Batch, Classes]
        if input.shape() != target.shape() {
            return Err(TetnusNnError::InvalidInput(format!(
                "CrossEntropyLoss: Input shape {:?} does not match target shape {:?}",
                input.shape(), target.shape()
            )));
        }

        let op = CrossEntropyOp {
            input: input.clone(),
            target: target.clone(),
        };

        let result = op.forward(&[input, target])?;
        Ok(with_graph(result, Arc::new(op), vec![input.clone(), target.clone()]))
    }
}

struct CrossEntropyOp {
    input: Tensor,
    target: Tensor,
}

impl Op for CrossEntropyOp {
    fn forward(&self, inputs: &[&Tensor]) -> std::result::Result<Tensor, TetnusError> {
        let input = inputs[0]; // Logits
        let target = inputs[1]; // Probabilities/One-hot

        let input_data = input.data();
        let target_data = target.data();
        let shape = input.shape();

        if shape.len() != 2 {
             return Err(TetnusError::InvalidInput(
                "CrossEntropyLoss requires 2D input [Batch, Classes]".to_string()
            ));
        }

        let batch_size = shape[0];
        let num_classes = shape[1];

        let mut total_loss = 0.0;

        // Loop over batch
        for b in 0..batch_size {
            let offset = b * num_classes;
            let logits = &input_data[offset..offset + num_classes];
            let targets = &target_data[offset..offset + num_classes];

            // 1. Max for stability
            let max_logit = logits.iter().fold(f32::NEG_INFINITY, |a, &b| a.max(b));

            // 2. Sum exp
            let mut sum_exp = 0.0;
            for &l in logits {
                sum_exp += (l - max_logit).exp();
            }

            // 3. Log Sum Exp
            let log_sum_exp = max_logit + sum_exp.ln();

            // 4. Loss: -sum(target * (logit - log_sum_exp))
            let mut sample_loss = 0.0;
            for i in 0..num_classes {
                let log_prob = logits[i] - log_sum_exp;
                sample_loss += -targets[i] * log_prob;
            }

            total_loss += sample_loss;
        }

        let mean_loss = total_loss / batch_size as f32;

        Tensor::new(vec![mean_loss], vec![1])
    }

    fn backward(&self, grad_output: &Tensor) -> std::result::Result<Vec<Tensor>, TetnusError> {
        let input_data = self.input.data();
        let target_data = self.target.data();
        let grad_out_data = grad_output.data(); // Scalar gradient

        if grad_out_data.is_empty() {
             return Err(TetnusError::GradientError("Empty gradient".to_string()));
        }
        let grad_scale = grad_out_data[0];

        let shape = self.input.shape();
        let batch_size = shape[0];
        let num_classes = shape[1];
        let numel = self.input.numel();

        let mut grad_input = vec![0.0; numel];

        // grad_input = (softmax(input) - target) / batch_size * grad_scale

        for b in 0..batch_size {
            let offset = b * num_classes;
            let logits = &input_data[offset..offset + num_classes];
            let targets = &target_data[offset..offset + num_classes];
            let grads = &mut grad_input[offset..offset + num_classes];

            // Softmax
            let max_logit = logits.iter().fold(f32::NEG_INFINITY, |a, &b| a.max(b));
            let mut sum_exp = 0.0;
            let mut exps = vec![0.0; num_classes];
            for i in 0..num_classes {
                exps[i] = (logits[i] - max_logit).exp();
                sum_exp += exps[i];
            }

            for i in 0..num_classes {
                let softmax = exps[i] / sum_exp;
                grads[i] = (softmax - targets[i]) / (batch_size as f32) * grad_scale;
            }
        }

        // We don't compute gradient for target usually
        let grad_target = Tensor::zeros(self.target.shape().to_vec())?;

        Ok(vec![
            Tensor::new(grad_input, shape.to_vec())?,
            grad_target
        ])
    }

    fn name(&self) -> &str {
        "cross_entropy_loss"
    }
}
