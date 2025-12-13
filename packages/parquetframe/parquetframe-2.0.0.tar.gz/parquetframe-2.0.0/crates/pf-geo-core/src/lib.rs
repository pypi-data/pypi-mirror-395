//! ParquetFrame Geospatial Core (`pf-geo-core`)
//!
//! High-performance geospatial operations for ParquetFrame.
//!
//! This crate provides:
//! - Geometry types (Point, LineString, Polygon, etc.)
//! - CRS (Coordinate Reference System) management
//! - Spatial operations (distance, buffer, intersection, etc.)
//! - GeoJSON I/O
//!
//! # Architecture
//!
//! Geometries are stored as Well-Known Binary (WKB) in Arrow LargeBinaryArray,
//! enabling zero-copy operations and efficient serialization.

pub mod error;
pub mod types;
pub mod crs;
pub mod operations;
pub mod io;

pub use error::GeoError;
pub type Result<T> = std::result::Result<T, GeoError>;

// Re-export commonly used types
pub use types::Geometry;
pub use crs::CRS;
pub mod advanced_ops;
