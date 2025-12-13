//! Tetnus Neural Network Library
//!
//! Provides high-level neural network layers and modules built on tetnus-core.

pub mod error;
pub mod module;
pub mod linear;
pub mod activations;
pub mod sequential;
pub mod optim;
pub mod loss;
pub mod preprocessing;
pub mod embedding;
pub mod norm;
pub mod quantization;

pub use error::{Result, TetnusNnError};
pub use module::Module;
pub use linear::Linear;
pub use activations::ReLU;
pub use sequential::Sequential;
pub use embedding::Embedding;
pub use norm::LayerNorm;
pub use preprocessing::{NumericalProcessor, CategoricalProcessor};
pub use quantization::{QuantizationParams, quantize_tensor, dequantize_tensor, quantize_model_weights};
