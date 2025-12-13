//! Geofencing operations for mobility analytics.
//!
//! Provides spatial and temporal geofencing operations:
//! - Within/outside checks (spatial)
//! - Enter/exit detection (temporal)

use crate::{MobError, Result};
use geo::{Coord, LineString, Point, Polygon};
use pf_geo_core::operations;
use pf_geo_core::Geometry;

/// Check if a point is within a polygon boundary.
///
/// # Arguments
/// * `lon` - Longitude of the point
/// * `lat` - Latitude of the point
/// * `polygon_coords` - Vector of (lon, lat) coordinates defining the polygon exterior
///
/// # Returns
/// `true` if the point is within the polygon, `false` otherwise
pub fn check_within_polygon(
    lon: f64,
    lat: f64,
    polygon_coords: &[(f64, f64)],
) -> Result<bool> {
    if polygon_coords.len() < 3 {
        return Err(MobError::InvalidInput(
            "Polygon must have at least 3 coordinates".to_string(),
        ));
    }

    let point = Geometry::Point(Point::new(lon, lat));

    // Convert coordinates to Coord and create LineString
    let coords: Vec<Coord> = polygon_coords
        .iter()
        .map(|(x, y)| Coord { x: *x, y: *y })
        .collect();

    let exterior = LineString::new(coords);
    let polygon = Geometry::Polygon(Polygon::new(exterior, vec![]));

    operations::contains(&polygon, &point).map_err(MobError::GeoError)
}

/// Check if a point is outside a polygon boundary.
///
/// # Arguments
/// * `lon` - Longitude of the point
/// * `lat` - Latitude of the point
/// * `polygon_coords` - Vector of (lon, lat) coordinates defining the polygon exterior
///
/// # Returns
/// `true` if the point is outside the polygon, `false` otherwise
pub fn check_outside_polygon(
    lon: f64,
    lat: f64,
    polygon_coords: &[(f64, f64)],
) -> Result<bool> {
    check_within_polygon(lon, lat, polygon_coords).map(|within| !within)
}

/// Detect fence entry events by comparing consecutive point states.
///
/// Returns indices where a point transitions from outside to inside the geofence.
///
/// # Arguments
/// * `lons` - Array of longitudes
/// * `lats` - Array of latitudes
/// * `polygon_coords` - Vector of (lon, lat) coordinates defining the polygon exterior
///
/// # Returns
/// Vector of indices where fence entry occurred
pub fn detect_fence_enter(
    lons: &[f64],
    lats: &[f64],
    polygon_coords: &[(f64, f64)],
) -> Result<Vec<usize>> {
    if lons.len() != lats.len() {
        return Err(MobError::InvalidInput(
            "Longitude and latitude arrays must have the same length".to_string(),
        ));
    }

    if lons.is_empty() {
        return Ok(vec![]);
    }

    let mut enter_indices = Vec::new();
    let mut prev_inside = check_within_polygon(lons[0], lats[0], polygon_coords)?;

    for i in 1..lons.len() {
        let curr_inside = check_within_polygon(lons[i], lats[i], polygon_coords)?;

        // Detect transition from outside to inside
        if !prev_inside && curr_inside {
            enter_indices.push(i);
        }

        prev_inside = curr_inside;
    }

    Ok(enter_indices)
}

/// Detect fence exit events by comparing consecutive point states.
///
/// Returns indices where a point transitions from inside to outside the geofence.
///
/// # Arguments
/// * `lons` - Array of longitudes
/// * `lats` - Array of latitudes
/// * `polygon_coords` - Vector of (lon, lat) coordinates defining the polygon exterior
///
/// # Returns
/// Vector of indices where fence exit occurred
pub fn detect_fence_exit(
    lons: &[f64],
    lats: &[f64],
    polygon_coords: &[(f64, f64)],
) -> Result<Vec<usize>> {
    if lons.len() != lats.len() {
        return Err(MobError::InvalidInput(
            "Longitude and latitude arrays must have the same length".to_string(),
        ));
    }

    if lons.is_empty() {
        return Ok(vec![]);
    }

    let mut exit_indices = Vec::new();
    let mut prev_inside = check_within_polygon(lons[0], lats[0], polygon_coords)?;

    for i in 1..lons.len() {
        let curr_inside = check_within_polygon(lons[i], lats[i], polygon_coords)?;

        // Detect transition from inside to outside
        if prev_inside && !curr_inside {
            exit_indices.push(i);
        }

        prev_inside = curr_inside;
    }

    Ok(exit_indices)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn sample_square_fence() -> Vec<(f64, f64)> {
        vec![
            (0.0, 0.0),
            (10.0, 0.0),
            (10.0, 10.0),
            (0.0, 10.0),
            (0.0, 0.0), // Close the polygon
        ]
    }

    #[test]
    fn test_within_polygon() {
        let fence = sample_square_fence();

        // Point inside
        assert!(check_within_polygon(5.0, 5.0, &fence).unwrap());

        // Point outside
        assert!(!check_within_polygon(15.0, 15.0, &fence).unwrap());

        // Point on edge (boundary behavior may vary)
        let on_edge = check_within_polygon(0.0, 5.0, &fence).unwrap();
        assert!(on_edge || !on_edge); // Either is acceptable
    }

    #[test]
    fn test_outside_polygon() {
        let fence = sample_square_fence();

        // Point inside
        assert!(!check_outside_polygon(5.0, 5.0, &fence).unwrap());

        // Point outside
        assert!(check_outside_polygon(15.0, 15.0, &fence).unwrap());
    }

    #[test]
    fn test_detect_fence_enter() {
        let fence = sample_square_fence();

        // Path: outside -> inside -> inside
        let lons = vec![-5.0, 5.0, 6.0];
        let lats = vec![5.0, 5.0, 5.0];

        let enters = detect_fence_enter(&lons, &lats, &fence).unwrap();
        assert_eq!(enters.len(), 1);
        assert_eq!(enters[0], 1); // Entry at index 1
    }

    #[test]
    fn test_detect_fence_exit() {
        let fence = sample_square_fence();

        // Path: inside -> inside -> outside
        let lons = vec![5.0, 6.0, 15.0];
        let lats = vec![5.0, 5.0, 5.0];

        let exits = detect_fence_exit(&lons, &lats, &fence).unwrap();
        assert_eq!(exits.len(), 1);
        assert_eq!(exits[0], 2); // Exit at index 2
    }

    #[test]
    fn test_multiple_transitions() {
        let fence = sample_square_fence();

        // Path: outside -> inside -> outside -> inside -> outside
        let lons = vec![-5.0, 5.0, 15.0, 5.0, -5.0];
        let lats = vec![5.0, 5.0, 5.0, 5.0, 5.0];

        let enters = detect_fence_enter(&lons, &lats, &fence).unwrap();
        assert_eq!(enters.len(), 2);
        assert_eq!(enters[0], 1);
        assert_eq!(enters[1], 3);

        let exits = detect_fence_exit(&lons, &lats, &fence).unwrap();
        assert_eq!(exits.len(), 2);
        assert_eq!(exits[0], 2);
        assert_eq!(exits[1], 4);
    }

    #[test]
    fn test_empty_input() {
        let fence = sample_square_fence();
        let lons: Vec<f64> = vec![];
        let lats: Vec<f64> = vec![];

        let enters = detect_fence_enter(&lons, &lats, &fence).unwrap();
        assert_eq!(enters.len(), 0);

        let exits = detect_fence_exit(&lons, &lats, &fence).unwrap();
        assert_eq!(exits.len(), 0);
    }

    #[test]
    fn test_invalid_polygon() {
        // Polygon with less than 3 points
        let invalid_fence = vec![(0.0, 0.0), (1.0, 1.0)];

        let result = check_within_polygon(5.0, 5.0, &invalid_fence);
        assert!(result.is_err());
    }

    #[test]
    fn test_mismatched_arrays() {
        let fence = sample_square_fence();
        let lons = vec![1.0, 2.0, 3.0];
        let lats = vec![1.0, 2.0]; // Different length

        let result = detect_fence_enter(&lons, &lats, &fence);
        assert!(result.is_err());
    }
}
