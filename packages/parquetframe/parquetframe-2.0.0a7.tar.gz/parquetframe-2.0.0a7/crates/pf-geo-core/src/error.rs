use thiserror::Error;

#[derive(Error, Debug)]
pub enum GeoError {
    #[error("Arrow error: {0}")]
    ArrowError(#[from] arrow::error::ArrowError),

    #[error("Geometry error: {0}")]
    GeometryError(String),

    #[error("CRS error: {0}")]
    CRSError(String),

    #[error("Projection error: {0}")]
    ProjectionError(String),

    #[error("I/O error: {0}")]
    IOError(#[from] std::io::Error),

    #[error("Invalid parameter: {0}")]
    InvalidParameter(String),

    #[error("WKB parse error: {0}")]
    WKBError(String),

    #[error("GeoJSON error: {0}")]
    GeoJSONError(String),
}
