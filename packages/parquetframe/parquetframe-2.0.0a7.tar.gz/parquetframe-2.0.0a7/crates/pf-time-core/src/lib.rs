//! Time-series operations for ParquetFrame.
//!
//! This crate provides high-performance time-series operations including:
//! - Resampling (upsample/downsample)
//! - Rolling window aggregations
//! - As-of joins (point-in-time correctness)
//!
//! Phase 3: TIME Core Implementation

/// Error types for time-series operations
pub mod error;

/// Resampling operations (upsample, downsample, aggregations)
pub mod resample;

/// Rolling window operations (moving averages, statistics)
pub mod rolling;

/// As-of join operations (point-in-time correctness)
pub mod asof;

/// Time index structures and utilities
pub mod index;

// Re-export common types
pub use error::{TimeError, Result};
