/// Python bindings for pf-mob-core mobility operations.

use pyo3::prelude::*;
use pyo3::exceptions::{PyValueError, PyRuntimeError};
use numpy::{PyReadonlyArray1, PyArray1};

/// Check if a point is within a geofence polygon.
#[pyfunction]
fn mob_geofence_check_within(
    lon: f64,
    lat: f64,
    polygon_coords: Vec<(f64, f64)>,
) -> PyResult<bool> {
    pf_mob_core::geofence::check_within_polygon(lon, lat, &polygon_coords)
        .map_err(|e| PyValueError::new_err(format!("Geofence check failed: {}", e)))
}

/// Check if a point is outside a geofence polygon.
#[pyfunction]
fn mob_geofence_check_outside(
    lon: f64,
    lat: f64,
    polygon_coords: Vec<(f64, f64)>,
) -> PyResult<bool> {
    pf_mob_core::geofence::check_outside_polygon(lon, lat, &polygon_coords)
        .map_err(|e| PyValueError::new_err(format!("Geofence check failed: {}", e)))
}

/// Detect when points enter a geofence.
#[pyfunction]
fn mob_geofence_detect_enter<'py>(
    py: Python<'py>,
    lons: PyReadonlyArray1<f64>,
    lats: PyReadonlyArray1<f64>,
    polygon_coords: Vec<(f64, f64)>,
) -> PyResult<Bound<'py, PyArray1<usize>>> {
    let lons_slice = lons.as_slice()?;
    let lats_slice = lats.as_slice()?;

    let indices = pf_mob_core::geofence::detect_fence_enter(lons_slice, lats_slice, &polygon_coords)
        .map_err(|e| PyValueError::new_err(format!("Enter detection failed: {}", e)))?;

    Ok(PyArray1::from_vec(py, indices))
}

/// Detect when points exit a geofence.
#[pyfunction]
fn mob_geofence_detect_exit<'py>(
    py: Python<'py>,
    lons: PyReadonlyArray1<f64>,
    lats: PyReadonlyArray1<f64>,
    polygon_coords: Vec<(f64, f64)>,
) -> PyResult<Bound<'py, PyArray1<usize>>> {
    let lons_slice = lons.as_slice()?;
    let lats_slice = lats.as_slice()?;

    let indices = pf_mob_core::geofence::detect_fence_exit(lons_slice, lats_slice, &polygon_coords)
        .map_err(|e| PyValueError::new_err(format!("Exit detection failed: {}", e)))?;

    Ok(PyArray1::from_vec(py, indices))
}

/// Reconstruct a route from GPS points.
#[pyfunction]
fn mob_reconstruct_route(
    lons: PyReadonlyArray1<f64>,
    lats: PyReadonlyArray1<f64>,
) -> PyResult<Vec<(f64, f64)>> {
    let lons_slice = lons.as_slice()?;
    let lats_slice = lats.as_slice()?;

    let route = pf_mob_core::routes::reconstruct_route(lons_slice, lats_slice)
        .map_err(|e| PyValueError::new_err(format!("Route reconstruction failed: {}", e)))?;

    pf_mob_core::routes::extract_route_coords(&route)
        .map_err(|e| PyRuntimeError::new_err(format!("Failed to extract coordinates: {}", e)))
}

/// Get the start point of a route.
#[pyfunction]
fn mob_route_start_point(
    lons: PyReadonlyArray1<f64>,
    lats: PyReadonlyArray1<f64>,
) -> PyResult<(f64, f64)> {
    let lons_slice = lons.as_slice()?;
    let lats_slice = lats.as_slice()?;

    let route = pf_mob_core::routes::reconstruct_route(lons_slice, lats_slice)
        .map_err(|e| PyValueError::new_err(format!("Route reconstruction failed: {}", e)))?;

    pf_mob_core::routes::route_start_point(&route)
        .map_err(|e| PyRuntimeError::new_err(format!("Failed to get start point: {}", e)))
}

/// Get the end point of a route.
#[pyfunction]
fn mob_route_end_point(
    lons: PyReadonlyArray1<f64>,
    lats: PyReadonlyArray1<f64>,
) -> PyResult<(f64, f64)> {
    let lons_slice = lons.as_slice()?;
    let lats_slice = lats.as_slice()?;

    let route = pf_mob_core::routes::reconstruct_route(lons_slice, lats_slice)
        .map_err(|e| PyValueError::new_err(format!("Route reconstruction failed: {}", e)))?;

    pf_mob_core::routes::route_end_point(&route)
        .map_err(|e| PyRuntimeError::new_err(format!("Failed to get end point: {}", e)))
}

/// Get the number of points in a route.
#[pyfunction]
fn mob_route_point_count(
    lons: PyReadonlyArray1<f64>,
    lats: PyReadonlyArray1<f64>,
) -> PyResult<usize> {
    let lons_slice = lons.as_slice()?;
    let lats_slice = lats.as_slice()?;

    let route = pf_mob_core::routes::reconstruct_route(lons_slice, lats_slice)
        .map_err(|e| PyValueError::new_err(format!("Route reconstruction failed: {}", e)))?;

    pf_mob_core::routes::route_point_count(&route)
        .map_err(|e| PyRuntimeError::new_err(format!("Failed to count points: {}", e)))
}

/// Register MOB functions in the Python module.
pub fn register_mob_functions(parent_module: &Bound<'_, PyModule>) -> PyResult<()> {
    let mob_module = PyModule::new(parent_module.py(), "mob")?;

    // Geofencing functions
    mob_module.add_function(wrap_pyfunction!(mob_geofence_check_within, &mob_module)?)?;
    mob_module.add_function(wrap_pyfunction!(mob_geofence_check_outside, &mob_module)?)?;
    mob_module.add_function(wrap_pyfunction!(mob_geofence_detect_enter, &mob_module)?)?;
    mob_module.add_function(wrap_pyfunction!(mob_geofence_detect_exit, &mob_module)?)?;

    // Route reconstruction functions
    mob_module.add_function(wrap_pyfunction!(mob_reconstruct_route, &mob_module)?)?;
    mob_module.add_function(wrap_pyfunction!(mob_route_start_point, &mob_module)?)?;
    mob_module.add_function(wrap_pyfunction!(mob_route_end_point, &mob_module)?)?;
    mob_module.add_function(wrap_pyfunction!(mob_route_point_count, &mob_module)?)?;

    parent_module.add_submodule(&mob_module)?;
    Ok(())
}
