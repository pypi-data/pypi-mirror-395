/// Python bindings for pf-geo-core geospatial operations.

use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use numpy::PyReadonlyArray1;

/// Calculate Haversine distance between two points (in meters).
#[pyfunction]
fn geo_haversine_distance(
    lon1: f64,
    lat1: f64,
    lon2: f64,
    lat2: f64,
) -> PyResult<f64> {
    use pf_geo_core::{operations, Geometry};

    let p1 = Geometry::point(lon1, lat1);
    let p2 = Geometry::point(lon2, lat2);

    operations::haversine_distance(&p1, &p2)
        .map_err(|e| PyValueError::new_err(format!("Distance calculation failed: {}", e)))
}

/// Create a buffer around a point (returns polygon coordinates).
#[pyfunction]
fn geo_buffer_point(
    lon: f64,
    lat: f64,
    distance: f64,
) -> PyResult<Vec<(f64, f64)>> {
    use pf_geo_core::{advanced_ops, Geometry};

    let point = Geometry::point(lon, lat);
    let buffered = advanced_ops::buffer(&point, distance)
        .map_err(|e| PyValueError::new_err(format!("Buffer failed: {}", e)))?;

    // Extract coordinates from buffered polygon
    match buffered {
        Geometry::Polygon(poly) => {
            Ok(poly.exterior().coords().map(|c| (c.x, c.y)).collect())
        }
        _ => Err(PyValueError::new_err("Expected polygon result")),
    }
}

/// Check if a point is within a polygon.
#[pyfunction]
fn geo_point_in_polygon(
    point_lon: f64,
    point_lat: f64,
    polygon_coords: Vec<(f64, f64)>,
) -> PyResult<bool> {
    use pf_geo_core::{operations, Geometry};
    use geo::{LineString, Polygon};

    let point = Geometry::point(point_lon, point_lat);
    let exterior = LineString::from(polygon_coords);
    let polygon = Geometry::Polygon(Polygon::new(exterior, vec![]));

    operations::contains(&polygon, &point)
        .map_err(|e| PyValueError::new_err(format!("Contains check failed: {}", e)))
}

/// Read GeoJSON and return list of point coordinates.
#[pyfunction]
fn geo_read_geojson(geojson_str: &str) -> PyResult<Vec<(f64, f64)>> {
    use pf_geo_core::{io, Geometry};
    use std::io::Cursor;

    let geometries = io::read_geojson(Cursor::new(geojson_str))
        .map_err(|e| PyValueError::new_err(format!("GeoJSON parse failed: {}", e)))?;

    let mut points = Vec::new();
    for geom in geometries {
        if let Geometry::Point(p) = geom {
            points.push((p.x(), p.y()));
        }
    }

    Ok(points)
}

/// Write points to GeoJSON string.
#[pyfunction]
fn geo_write_geojson(points: Vec<(f64, f64)>) -> PyResult<String> {
    use pf_geo_core::{io, Geometry};

    let geometries: Vec<Geometry> = points
        .into_iter()
        .map(|(x, y)| Geometry::point(x, y))
        .collect();

    let mut output = Vec::new();
    io::write_geojson(&geometries, &mut output)
        .map_err(|e| PyValueError::new_err(format!("GeoJSON write failed: {}", e)))?;

    String::from_utf8(output)
        .map_err(|e| PyValueError::new_err(format!("UTF-8 conversion failed: {}", e)))
}

/// Transform coordinates from one CRS to another.
#[pyfunction]
fn geo_transform_coords(
    lon: f64,
    lat: f64,
    from_epsg: u32,
    to_epsg: u32,
) -> PyResult<(f64, f64)> {
    use pf_geo_core::CRS;

    let from_crs = CRS::from_epsg(from_epsg)
        .map_err(|e| PyValueError::new_err(format!("Invalid from_epsg: {}", e)))?;

    let to_crs = CRS::from_epsg(to_epsg)
        .map_err(|e| PyValueError::new_err(format!("Invalid to_epsg: {}", e)))?;

    from_crs.transform(&to_crs, lon, lat)
        .map_err(|e| PyValueError::new_err(format!("Transform failed: {}", e)))
}

/// Register geo functions in the Python module.
pub fn register_geo_functions(parent_module: &Bound<'_, PyModule>) -> PyResult<()> {
    let geo_module = PyModule::new(parent_module.py(), "geo")?;

    geo_module.add_function(wrap_pyfunction!(geo_haversine_distance, &geo_module)?)?;
    geo_module.add_function(wrap_pyfunction!(geo_buffer_point, &geo_module)?)?;
    geo_module.add_function(wrap_pyfunction!(geo_point_in_polygon, &geo_module)?)?;
    geo_module.add_function(wrap_pyfunction!(geo_read_geojson, &geo_module)?)?;
    geo_module.add_function(wrap_pyfunction!(geo_write_geojson, &geo_module)?)?;
    geo_module.add_function(wrap_pyfunction!(geo_transform_coords, &geo_module)?)?;

    parent_module.add_submodule(&geo_module)?;
    Ok(())
}
