use tetnus_core::Tensor;
use crate::Result;

/// A trait for neural network modules.
///
/// Modules can contain other modules (submodules) and parameters.
pub trait Module: Send + Sync {
    /// Perform the forward pass.
    fn forward(&self, input: &Tensor) -> Result<Tensor>;

    /// Return a list of all learnable parameters in this module (and submodules).
    fn parameters(&self) -> Vec<Tensor>;

    /// Set training mode.
    fn train(&mut self) {}

    /// Set evaluation mode.
    fn eval(&mut self) {}
}
