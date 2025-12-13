//! I/O operations for ParquetFrame.
//!
//! This crate provides high-performance I/O operations including:
//! - Parquet metadata parsing and fast-path filters
//! - Avro schema resolution and fast deserialization
//! - Columnar data operations on Arrow buffers
//!
//! Phase 2: I/O Fast-Paths Implementation

/// Error types for I/O operations
pub mod error;

/// Parquet metadata reading and statistics
pub mod parquet_meta;

/// High-performance readers that return Arrow IPC bytes for Python bridging
pub mod io_fast;

/// Avro schema resolution and deserialization
pub mod avro;

/// ORC schema resolution and deserialization
#[cfg(feature = "orc")]
pub mod orc;

// Re-export common types
pub use error::{IoError, Result};
pub use parquet_meta::{ColumnStatistics, ParquetMetadata};
pub use io_fast::{read_csv_ipc, read_parquet_ipc};
pub use avro::read_avro_ipc;
#[cfg(feature = "orc")]
pub use orc::read_orc_ipc;
