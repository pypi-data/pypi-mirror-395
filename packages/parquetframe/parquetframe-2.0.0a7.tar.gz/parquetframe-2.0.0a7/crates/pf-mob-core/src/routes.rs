//! Route reconstruction for mobility analytics.
//!
//! Converts sequences of GPS points into route geometries (LineStrings).

use crate::{MobError, Result};
use geo::{Coord, LineString, Point};
use pf_geo_core::Geometry;

/// Reconstruct a route from a sequence of GPS points.
///
/// Converts a series of (lon, lat) coordinates into a LineString geometry,
/// which can be used for route visualization and analysis.
///
/// # Arguments
/// * `lons` - Array of longitudes in order
/// * `lats` - Array of latitudes in order
///
/// # Returns
/// A `Geometry::LineString` representing the route
///
/// # Errors
/// Returns error if:
/// - Arrays have different lengths
/// - Less than 2 points provided (need at least 2 for a line)
pub fn reconstruct_route(lons: &[f64], lats: &[f64]) -> Result<Geometry> {
    if lons.len() != lats.len() {
        return Err(MobError::InvalidInput(
            "Longitude and latitude arrays must have the same length".to_string(),
        ));
    }

    if lons.len() < 2 {
        return Err(MobError::InvalidInput(
            "Need at least 2 points to create a route".to_string(),
        ));
    }

    let coords: Vec<Coord> = lons
        .iter()
        .zip(lats.iter())
        .map(|(lon, lat)| Coord { x: *lon, y: *lat })
        .collect();

    Ok(Geometry::LineString(LineString::new(coords)))
}

/// Extract coordinates from a route LineString.
///
/// Helper function to convert a LineString back to coordinate pairs.
///
/// # Arguments
/// * `route` - A Geometry::LineString
///
/// # Returns
/// Vector of (lon, lat) tuples
pub fn extract_route_coords(route: &Geometry) -> Result<Vec<(f64, f64)>> {
    match route {
        Geometry::LineString(ls) => {
            Ok(ls.coords().map(|c| (c.x, c.y)).collect())
        }
        _ => Err(MobError::RouteError(
            "Expected LineString geometry".to_string(),
        )),
    }
}

/// Calculate the total number of points in a route.
///
/// # Arguments
/// * `route` - A Geometry::LineString
///
/// # Returns
/// Number of points in the route
pub fn route_point_count(route: &Geometry) -> Result<usize> {
    match route {
        Geometry::LineString(ls) => Ok(ls.coords().count()),
        _ => Err(MobError::RouteError(
            "Expected LineString geometry".to_string(),
        )),
    }
}

/// Get the start point of a route.
///
/// # Arguments
/// * `route` - A Geometry::LineString
///
/// # Returns
/// The first point in the route as (lon, lat)
pub fn route_start_point(route: &Geometry) -> Result<(f64, f64)> {
    match route {
        Geometry::LineString(ls) => {
            if let Some(coord) = ls.coords().next() {
                Ok((coord.x, coord.y))
            } else {
                Err(MobError::RouteError("Route has no points".to_string()))
            }
        }
        _ => Err(MobError::RouteError(
            "Expected LineString geometry".to_string(),
        )),
    }
}

/// Get the end point of a route.
///
/// # Arguments
/// * `route` - A Geometry::LineString
///
/// # Returns
/// The last point in the route as (lon, lat)
pub fn route_end_point(route: &Geometry) -> Result<(f64, f64)> {
    match route {
        Geometry::LineString(ls) => {
            if let Some(coord) = ls.coords().last() {
                Ok((coord.x, coord.y))
            } else {
                Err(MobError::RouteError("Route has no points".to_string()))
            }
        }
        _ => Err(MobError::RouteError(
            "Expected LineString geometry".to_string(),
        )),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_reconstruct_simple_route() {
        let lons = vec![0.0, 1.0, 2.0, 3.0];
        let lats = vec![0.0, 1.0, 2.0, 3.0];

        let route = reconstruct_route(&lons, &lats).unwrap();

        match route {
            Geometry::LineString(ls) => {
                assert_eq!(ls.coords().count(), 4);
            }
            _ => panic!("Expected LineString"),
        }
    }

    #[test]
    fn test_extract_coords() {
        let lons = vec![0.0, 1.0, 2.0];
        let lats = vec![10.0, 11.0, 12.0];

        let route = reconstruct_route(&lons, &lats).unwrap();
        let coords = extract_route_coords(&route).unwrap();

        assert_eq!(coords.len(), 3);
        assert_eq!(coords[0], (0.0, 10.0));
        assert_eq!(coords[1], (1.0, 11.0));
        assert_eq!(coords[2], (2.0, 12.0));
    }

    #[test]
    fn test_route_point_count() {
        let lons = vec![0.0, 1.0, 2.0, 3.0, 4.0];
        let lats = vec![0.0, 1.0, 2.0, 3.0, 4.0];

        let route = reconstruct_route(&lons, &lats).unwrap();
        let count = route_point_count(&route).unwrap();

        assert_eq!(count, 5);
    }

    #[test]
    fn test_route_start_end_points() {
        let lons = vec![-74.0, -73.9, -73.8];
        let lats = vec![40.7, 40.8, 40.9];

        let route = reconstruct_route(&lons, &lats).unwrap();

        let start = route_start_point(&route).unwrap();
        assert_eq!(start, (-74.0, 40.7));

        let end = route_end_point(&route).unwrap();
        assert_eq!(end, (-73.8, 40.9));
    }

    #[test]
    fn test_mismatched_arrays() {
        let lons = vec![0.0, 1.0, 2.0];
        let lats = vec![0.0, 1.0]; // Different length

        let result = reconstruct_route(&lons, &lats);
        assert!(result.is_err());
    }

    #[test]
    fn test_insufficient_points() {
        let lons = vec![0.0];
        let lats = vec![0.0];

        let result = reconstruct_route(&lons, &lats);
        assert!(result.is_err());
    }

    #[test]
    fn test_minimum_points() {
        let lons = vec![0.0, 1.0];
        let lats = vec![0.0, 1.0];

        let route = reconstruct_route(&lons, &lats).unwrap();
        let count = route_point_count(&route).unwrap();

        assert_eq!(count, 2);
    }

    #[test]
    fn test_extract_coords_wrong_geometry() {
        // Test with a Point geometry instead of LineString
        let point = Geometry::Point(Point::new(0.0, 0.0));
        let result = extract_route_coords(&point);
        assert!(result.is_err());
    }
}
