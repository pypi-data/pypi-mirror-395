/// Error types for mobility operations
use thiserror::Error;

#[derive(Error, Debug)]
pub enum MobError {
    #[error("Geofence error: {0}")]
    GeofenceError(String),

    #[error("Route reconstruction error: {0}")]
    RouteError(String),

    #[error("Geo operation failed: {0}")]
    GeoError(#[from] pf_geo_core::GeoError),

    #[error("Arrow error: {0}")]
    ArrowError(#[from] arrow::error::ArrowError),

    #[error("Invalid input: {0}")]
    InvalidInput(String),
}
