//! ParquetFrame Mobility Core (`pf-mob-core`)
//!
//! High-performance mobility and fleet management analytics.
//!
//! This crate provides:
//! - Geofencing operations
//! - Route reconstruction
//! - Fleet analytics
//!
//! # Architecture
//!
//! This is an application-layer crate that orchestrates:
//! - `pf-geo-core` for spatial operations
//! - `pf-time-core` for temporal operations
//! - `pf-graph-core` for graph operations

pub mod error;
pub mod geofence;
pub mod routes;

pub use error::MobError;
pub type Result<T> = std::result::Result<T, MobError>;
