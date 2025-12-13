/// Spatial operations on geometries.
///
/// Provides distance calculations, buffer operations, and spatial predicates.

use crate::{Geometry, GeoError, Result};
use geo::{
    HaversineDistance, VincentyDistance,
    Contains, Intersects, Within,
    Area, EuclideanLength,
};

/// Calculate Haversine distance between two points (in meters).
///
/// Uses spherical Earth approximation, suitable for most applications.
pub fn haversine_distance(geom1: &Geometry, geom2: &Geometry) -> Result<f64> {
    match (geom1, geom2) {
        (Geometry::Point(p1), Geometry::Point(p2)) => {
            Ok(p1.haversine_distance(p2))
        }
        _ => Err(GeoError::InvalidParameter(
            "Haversine distance only supports Point geometries".to_string(),
        )),
    }
}

/// Calculate Vinc enty distance between two points (in meters).
///
/// More accurate than Haversine, using ellipsoidal Earth model.
pub fn vincenty_distance(geom1: &Geometry, geom2: &Geometry) -> Result<f64> {
    match (geom1, geom2) {
        (Geometry::Point(p1), Geometry::Point(p2)) => {
            p1.vincenty_distance(p2)
                .map_err(|e| GeoError::GeometryError(format!("Vincenty distance failed: {}", e)))
        }
        _ => Err(GeoError::InvalidParameter(
            "Vincenty distance only supports Point geometries".to_string(),
        )),
    }
}

/// Calculate the area of a geometry (in square units of the CRS).
pub fn area(geom: &Geometry) -> Result<f64> {
    match geom {
        Geometry::Polygon(poly) => Ok(poly.unsigned_area()),
        Geometry::MultiPolygon(polys) => {
            Ok(polys.iter().map(|p| p.unsigned_area()).sum())
        }
        _ => Err(GeoError::InvalidParameter(
            "Area calculation only supports Polygon geometries".to_string(),
        )),
    }
}

/// Calculate the length of a geometry (in units of the CRS).
pub fn length(geom: &Geometry) -> Result<f64> {
    match geom {
        Geometry::LineString(ls) => Ok(ls.euclidean_length()),
        Geometry::MultiLineString(mls) => {
            Ok(mls.iter().map(|ls| ls.euclidean_length()).sum())
        }
        _ => Err(GeoError::InvalidParameter(
            "Length calculation only supports LineString geometries".to_string(),
        )),
    }
}

/// Check if geom1 contains geom2.
pub fn contains(geom1: &Geometry, geom2: &Geometry) -> Result<bool> {
    match (geom1, geom2) {
        (Geometry::Polygon(poly), Geometry::Point(point)) => {
            Ok(poly.contains(point))
        }
        _ => Err(GeoError::InvalidParameter(
            "Contains currently only supports Polygon.contains(Point)".to_string(),
        )),
    }
}

/// Check if geom1 intersects geom2.
pub fn intersects(geom1: &Geometry, geom2: &Geometry) -> Result<bool> {
    match (geom1, geom2) {
        (Geometry::Polygon(poly1), Geometry::Polygon(poly2)) => {
            Ok(poly1.intersects(poly2))
        }
        (Geometry::LineString(ls1), Geometry::LineString(ls2)) => {
            Ok(ls1.intersects(ls2))
        }
        _ => Err(GeoError::InvalidParameter(
            "Intersects not implemented for these geometry types".to_string(),
        )),
    }
}

/// Check if geom1 is within geom2.
pub fn within(geom1: &Geometry, geom2: &Geometry) -> Result<bool> {
    match (geom1, geom2) {
        (Geometry::Point(point), Geometry::Polygon(poly)) => {
            Ok(point.is_within(poly))
        }
        _ => Err(GeoError::InvalidParameter(
            "Within currently only supports Point.within(Polygon)".to_string(),
        )),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use geo::{point, polygon};

    #[test]
    fn test_haversine_distance() {
        // New York to London (approx 5570 km)
        let ny = Geometry::Point(point!(x: -74.0060, y: 40.7128));
        let london = Geometry::Point(point!(x: -0.1278, y: 51.5074));

        let dist = haversine_distance(&ny, &london).unwrap();

        // Should be approximately 5.57 million meters
        assert!(dist > 5_500_000.0);
        assert!(dist < 5_600_000.0);
    }

    #[test]
    fn test_polygon_area() {
        let poly = Geometry::Polygon(polygon![
            (x: 0.0, y: 0.0),
            (x: 1.0, y: 0.0),
            (x: 1.0, y: 1.0),
            (x: 0.0, y: 1.0),
            (x: 0.0, y: 0.0),
        ]);

        let a = area(&poly).unwrap();
        assert_eq!(a, 1.0); // Unit square
    }

    #[test]
    fn test_contains() {
        let poly = Geometry::Polygon(polygon![
            (x: 0.0, y: 0.0),
            (x: 10.0, y: 0.0),
            (x: 10.0, y: 10.0),
            (x: 0.0, y: 10.0),
            (x: 0.0, y: 0.0),
        ]);

        let inside = Geometry::Point(point!(x: 5.0, y: 5.0));
        let outside = Geometry::Point(point!(x: 15.0, y: 15.0));

        assert!(contains(&poly, &inside).unwrap());
        assert!(!contains(&poly, &outside).unwrap());
    }
}
