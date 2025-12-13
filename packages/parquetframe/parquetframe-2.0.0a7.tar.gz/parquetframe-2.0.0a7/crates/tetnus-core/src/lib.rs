//! TETNUS Core: Arrow-Native Tensor Library with Autograd
//!
//! A high-performance tensor computation library built on Apache Arrow,
//! providing zero-copy integration with ParquetFrame DataFrames.
//!
//! # Features
//! - Arrow-native tensors (zero-copy from DataFrames)
//! - Automatic differentiation (autograd)
//! - CPU parallelization with rayon
//! - NumPy-compatible API via Python bindings
//!
//! # Architecture
//! - `tensor`: Core tensor structure with Arc-based sharing
//! - `ops`: Operations and computation graph
//! - `autograd`: Automatic differentiation engine
//! - `kernels`: Low-level compute kernels (CPU)

pub mod error;
pub mod tensor;
pub mod ops;
pub mod autograd;
pub mod kernels;

pub use error::{TetnusError, Result};
pub use tensor::{Tensor, Device};
pub use autograd::backward;
