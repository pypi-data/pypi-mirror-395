use crate::{Result, TetnusNnError};
use tetnus_core::Tensor;

/// Stochastic Gradient Descent optimizer
pub struct SGD {
    params: Vec<Tensor>,
    lr: f32,
    momentum: f32,
    velocities: Vec<Option<Vec<f32>>>,
}

impl SGD {
    /// Create a new SGD optimizer
    pub fn new(params: Vec<Tensor>, lr: f32) -> Self {
        let velocities = vec![None; params.len()];
        Self {
            params,
            lr,
            momentum: 0.0,
            velocities,
        }
    }

    /// Set momentum
    pub fn with_momentum(mut self, momentum: f32) -> Self {
        self.momentum = momentum;
        self
    }

    /// Perform a single optimization step
    pub fn step(&mut self) -> Result<()> {
        for (i, param) in self.params.iter().enumerate() {
            if let Some(grad) = param.grad() {
                let p_data = param.data();
                let g_data = grad.data();

                if p_data.len() != g_data.len() {
                    return Err(TetnusNnError::InvalidInput(format!(
                        "Parameter and gradient shape mismatch: {:?} vs {:?}",
                        param.shape(),
                        grad.shape()
                    )));
                }

                let mut update = vec![0.0; p_data.len()];

                if self.momentum != 0.0 {
                    // Velocity update: v = m * v + g
                    // Param update: p = p - lr * v

                    let mut velocity = if let Some(v) = &self.velocities[i] {
                        v.clone()
                    } else {
                        vec![0.0; p_data.len()]
                    };

                    for j in 0..p_data.len() {
                        velocity[j] = self.momentum * velocity[j] + g_data[j];
                        update[j] = velocity[j];
                    }

                    self.velocities[i] = Some(velocity);
                } else {
                    // Standard SGD: p = p - lr * g
                    update = g_data;
                }

                // Apply update: p_new = p - lr * update
                let new_data: Vec<f32> = p_data
                    .iter()
                    .zip(update.iter())
                    .map(|(p, u)| p - self.lr * u)
                    .collect();

                param.set_data(new_data)?;
            }
        }
        Ok(())
    }

    /// Zero the gradients of all parameters
    pub fn zero_grad(&self) -> Result<()> {
        // We can't easily set grad to None safely via public API if there isn't one.
        // But Tensor has internal mutex.
        // Wait, we don't have a clear way to clear gradients on Tensor from outside
        // except replacing them with zero tensors?
        // PyTorch sets .grad = None.

        // We need a method on Tensor to clear grad.
        // Let's assume we'll add `Tensor::zero_grad()` to tetnus-core.
        // For now, I'll leave a TODO and implement it in core.
        for param in &self.params {
            param.zero_grad();
        }
        Ok(())
    }
}

/// Adam optimizer
pub struct Adam {
    params: Vec<Tensor>,
    lr: f32,
    beta1: f32,
    beta2: f32,
    epsilon: f32,
    step_count: usize,
    m: Vec<Option<Vec<f32>>>, // First moment
    v: Vec<Option<Vec<f32>>>, // Second moment
}

impl Adam {
    pub fn new(params: Vec<Tensor>, lr: f32) -> Self {
        let len = params.len();
        Self {
            params,
            lr,
            beta1: 0.9,
            beta2: 0.999,
            epsilon: 1e-8,
            step_count: 0,
            m: vec![None; len],
            v: vec![None; len],
        }
    }

    pub fn step(&mut self) -> Result<()> {
        self.step_count += 1;
        let t = self.step_count as f32;

        for (i, param) in self.params.iter().enumerate() {
            if let Some(grad) = param.grad() {
                let p_data = param.data();
                let g_data = grad.data();

                // Initialize moments if needed
                if self.m[i].is_none() {
                    self.m[i] = Some(vec![0.0; p_data.len()]);
                    self.v[i] = Some(vec![0.0; p_data.len()]);
                }

                let m_prev = self.m[i].as_ref().unwrap();
                let v_prev = self.v[i].as_ref().unwrap();

                let mut m_curr = vec![0.0; p_data.len()];
                let mut v_curr = vec![0.0; p_data.len()];
                let mut new_p = vec![0.0; p_data.len()];

                for j in 0..p_data.len() {
                    let g = g_data[j];

                    // m_t = beta1 * m_{t-1} + (1 - beta1) * g
                    m_curr[j] = self.beta1 * m_prev[j] + (1.0 - self.beta1) * g;

                    // v_t = beta2 * v_{t-1} + (1 - beta2) * g^2
                    v_curr[j] = self.beta2 * v_prev[j] + (1.0 - self.beta2) * g * g;

                    // Bias correction
                    let m_hat = m_curr[j] / (1.0 - self.beta1.powf(t));
                    let v_hat = v_curr[j] / (1.0 - self.beta2.powf(t));

                    // Update
                    new_p[j] = p_data[j] - self.lr * m_hat / (v_hat.sqrt() + self.epsilon);
                }

                self.m[i] = Some(m_curr);
                self.v[i] = Some(v_curr);

                param.set_data(new_p)?;
            }
        }
        Ok(())
    }

    pub fn zero_grad(&self) -> Result<()> {
        for param in &self.params {
            param.zero_grad();
        }
        Ok(())
    }
}
