/// Advanced geometric operations for Phase 2.
///
/// Provides buffer, intersection, union, and difference operations.

use crate::{Geometry, GeoError, Result};
use geo::{BooleanOps, Contains};
// use geo::prelude::*;
// use geo_buffer::Buffer; // Not available

/// Create a buffer around a geometry.
///
/// Returns a polygon representing all points within the specified distance.
pub fn buffer(geom: &Geometry, distance: f64) -> Result<Geometry> {
    match geom {
        Geometry::Point(p) => {
            // Simple circular buffer around point (approximate with 32 points)
            // Create a circle using geo-types or manual calculation
            // Since geo doesn't have a circle primitive that converts to polygon easily in 0.28 without features,
            // we'll manually generate points.
            let center = p.0;
            let mut coords = Vec::with_capacity(33);
            for i in 0..33 {
                let angle = (i as f64) * 2.0 * std::f64::consts::PI / 32.0;
                let x = center.x + distance * angle.cos();
                let y = center.y + distance * angle.sin();
                coords.push((x, y));
            }
            let exterior = geo::LineString::from(coords);
            Ok(Geometry::Polygon(geo::Polygon::new(exterior, vec![])))
        }
        Geometry::LineString(_ls) => {
             Err(GeoError::GeometryError(
                "Buffer for LineString not supported by current backend".to_string(),
            ))
        }
        Geometry::Polygon(poly) => {
            // Use geo-buffer crate
            // We need to handle potential version mismatch if types are not compatible.
            // But geo-types should be compatible.
            let buffered = geo_buffer::buffer_polygon(poly, distance);
            // geo-buffer returns MultiPolygon
            Ok(Geometry::MultiPolygon(buffered.0))
        }
        _ => Err(GeoError::GeometryError(
            "Buffer not yet implemented for this geometry type".to_string(),
        )),
    }
}

/// Calculate the intersection of two geometries.
pub fn intersection(geom1: &Geometry, geom2: &Geometry) -> Result<Option<Geometry>> {
    match (geom1, geom2) {
        (Geometry::Polygon(p1), Geometry::Polygon(p2)) => {
            let result = p1.intersection(p2);
            if !result.0.is_empty() {
                if let Some(first) = result.0.first() {
                    Ok(Some(Geometry::Polygon(first.clone())))
                } else {
                    Ok(None)
                }
            } else {
                Ok(None)
            }
        }
        _ => Err(GeoError::GeometryError(
            "Intersection only supports Polygon geometries currently".to_string(),
        )),
    }
}

/// Calculate the union of two geometries.
pub fn union(geom1: &Geometry, geom2: &Geometry) -> Result<Geometry> {
    match (geom1, geom2) {
        (Geometry::Polygon(p1), Geometry::Polygon(p2)) => {
            let result = p1.union(p2);
            Ok(Geometry::MultiPolygon(result.0))
        }
        _ => Err(GeoError::GeometryError(
            "Union only supports Polygon geometries currently".to_string(),
        )),
    }
}

/// Calculate the difference of two geometries (geom1 - geom2).
pub fn difference(geom1: &Geometry, geom2: &Geometry) -> Result<Option<Geometry>> {
    match (geom1, geom2) {
        (Geometry::Polygon(p1), Geometry::Polygon(p2)) => {
            // difference() returns MultiPolygon directly
            let result = p1.difference(p2);

            if !result.0.is_empty() {
                if let Some(first) = result.0.first() {
                    Ok(Some(Geometry::Polygon(first.clone())))
                } else {
                    Ok(None)
                }
            } else {
                Ok(None)
            }
        }
        _ => Err(GeoError::GeometryError(
            "Difference only supports Polygon geometries currently".to_string(),
        )),
    }
}

/// Check if two geometries are disjoint (do not intersect).
pub fn disjoint(geom1: &Geometry, geom2: &Geometry) -> Result<bool> {
    match (geom1, geom2) {
        (Geometry::Polygon(p1), Geometry::Polygon(p2)) => {
            use geo::Intersects;
            Ok(!p1.intersects(p2))
        }
        (Geometry::Point(pt), Geometry::Polygon(poly)) => Ok(!poly.contains(pt)),
        (Geometry::Polygon(poly), Geometry::Point(pt)) => Ok(!poly.contains(pt)),
        _ => Err(GeoError::GeometryError(
            "Disjoint not implemented for these geometry types".to_string(),
        )),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use geo::{point, polygon};

    #[test]
    fn test_buffer_point() {
        let pt = Geometry::Point(point!(x: 0.0, y: 0.0));
        let buffered = buffer(&pt, 1.0).unwrap();

        // Should return a polygon
        assert_eq!(buffered.geometry_type(), "Polygon");
    }

    #[test]
    fn test_intersection() {
        // Two overlapping squares
        let poly1 = Geometry::Polygon(polygon![
            (x: 0.0, y: 0.0),
            (x: 2.0, y: 0.0),
            (x: 2.0, y: 2.0),
            (x: 0.0, y: 2.0),
            (x: 0.0, y: 0.0),
        ]);

        let poly2 = Geometry::Polygon(polygon![
            (x: 1.0, y: 1.0),
            (x: 3.0, y: 1.0),
            (x: 3.0, y: 3.0),
            (x: 1.0, y: 3.0),
            (x: 1.0, y: 1.0),
        ]);

        let result = intersection(&poly1, &poly2).unwrap();
        assert!(result.is_some());
    }

    #[test]
    fn test_union() {
        let poly1 = Geometry::Polygon(polygon![
            (x: 0.0, y: 0.0),
            (x: 1.0, y: 0.0),
            (x: 1.0, y: 1.0),
            (x: 0.0, y: 1.0),
            (x: 0.0, y: 0.0),
        ]);

        let poly2 = Geometry::Polygon(polygon![
            (x: 0.5, y: 0.5),
            (x: 1.5, y: 0.5),
            (x: 1.5, y: 1.5),
            (x: 0.5, y: 1.5),
            (x: 0.5, y: 0.5),
        ]);

        let result = union(&poly1, &poly2).unwrap();
        // Union should succeed
        assert!(matches!(
            result,
            Geometry::Polygon(_) | Geometry::MultiPolygon(_)
        ));
    }

    #[test]
    fn test_disjoint() {
        let poly1 = Geometry::Polygon(polygon![
            (x: 0.0, y: 0.0),
            (x: 1.0, y: 0.0),
            (x: 1.0, y: 1.0),
            (x: 0.0, y: 1.0),
            (x: 0.0, y: 0.0),
        ]);

        let poly2 = Geometry::Polygon(polygon![
            (x: 5.0, y: 5.0),
            (x: 6.0, y: 5.0),
            (x: 6.0, y: 6.0),
            (x: 5.0, y: 6.0),
            (x: 5.0, y: 5.0),
        ]);

        assert!(disjoint(&poly1, &poly2).unwrap());
    }
}
