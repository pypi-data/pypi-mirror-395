/// Geometry types for ParquetFrame geospatial operations.
///
/// Geometries are stored as WKB (Well-Known Binary) for efficient
/// storage in Arrow arrays.

use crate::{GeoError, Result};
use geo::{Geometry as GeoGeometry, Point as GeoPoint, LineString as GeoLineString, Polygon as GeoPolygon};
use std::io::Cursor;

/// Unified geometry type supporting all OGC Simple Features.
#[derive(Debug, Clone)]
pub enum Geometry {
    Point(GeoPoint<f64>),
    LineString(GeoLineString<f64>),
    Polygon(GeoPolygon<f64>),
    MultiPoint(Vec<GeoPoint<f64>>),
    MultiLineString(Vec<GeoLineString<f64>>),
    MultiPolygon(Vec<GeoPolygon<f64>>),
}

impl Geometry {
    /// Create a Point geometry.
    pub fn point(x: f64, y: f64) -> Self {
        Geometry::Point(GeoPoint::new(x, y))
    }

    /// Convert geometry to WKB (Well-Known Binary).
    pub fn to_wkb(&self) -> Result<Vec<u8>> {
        // Simplified WKB encoding for now - will enhance in Phase 3
        match self {
            Geometry::Point(p) => {
                // Simple WKB Point encoding
                let mut wkb = Vec::with_capacity(21);
                wkb.push(1); // Little endian
                wkb.extend_from_slice(&1u32.to_le_bytes()); // Point type
                wkb.extend_from_slice(&p.x().to_le_bytes());
                wkb.extend_from_slice(&p.y().to_le_bytes());
                Ok(wkb)
            }
            _ => Err(GeoError::GeometryError("Only Point to_wkb implemented currently".to_string())),
        }
    }

    /// Parse geometry from WKB (Well-Known Binary).
    pub fn from_wkb(wkb: &[u8]) -> Result<Self> {
        if wkb.len() < 21 {
            return Err(GeoError::WKBError("WKB too short for Point".to_string()));
        }

        // Parse simple WKB Point
        if wkb[0] != 1 {
            return Err(GeoError::WKBError("Only little-endian WKB supported".to_string()));
        }

        let geom_type = u32::from_le_bytes([wkb[1], wkb[2], wkb[3], wkb[4]]);
        if geom_type != 1 {
            return Err(GeoError::WKBError("Only Point WKB parsing implemented".to_string()));
        }

        let x = f64::from_le_bytes([wkb[5], wkb[6], wkb[7], wkb[8], wkb[9], wkb[10], wkb[11], wkb[12]]);
        let y = f64::from_le_bytes([wkb[13], wkb[14], wkb[15], wkb[16], wkb[17], wkb[18], wkb[19], wkb[20]]);

        Ok(Geometry::Point(GeoPoint::new(x, y)))
    }

    /// Get the geometry type as a string.
    pub fn geometry_type(&self) -> &'static str {
        match self {
            Geometry::Point(_) => "Point",
            Geometry::LineString(_) => "LineString",
            Geometry::Polygon(_) => "Polygon",
            Geometry::MultiPoint(_) => "MultiPoint",
            Geometry::MultiLineString(_) => "MultiLineString",
            Geometry::MultiPolygon(_) => "MultiPolygon",
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_point_creation() {
        let point = Geometry::point(1.0, 2.0);
        assert_eq!(point.geometry_type(), "Point");
    }

    #[test]
    fn test_point_wkb_roundtrip() {
        let point = Geometry::point(10.5, 20.3);
        let wkb = point.to_wkb().unwrap();
        let parsed = Geometry::from_wkb(&wkb).unwrap();

        assert_eq!(parsed.geometry_type(), "Point");
        if let Geometry::Point(p) = parsed {
            assert!((p.x() - 10.5).abs() < 0.0001);
            assert!((p.y() - 20.3).abs() < 0.0001);
        } else {
            panic!("Expected Point geometry");
        }
    }
}
