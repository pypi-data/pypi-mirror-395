/// I/O operations for geospatial data.
///
/// Handles GeoJSON reading/writing and GeoParquet metadata.

use crate::{Geometry, GeoError, Result};
use serde_json::{json, Value};
use std::io::{Read, Write};

/// Read geometries from GeoJSON.
///
/// Supports FeatureCollection, Feature, and bare Geometry objects.
pub fn read_geojson<R: Read>(reader: R) -> Result<Vec<Geometry>> {
    let geojson: Value = serde_json::from_reader(reader)
        .map_err(|e| GeoError::GeoJSONError(format!("Failed to parse GeoJSON: {}", e)))?;

    let mut geometries = Vec::new();

    match geojson.get("type").and_then(|t| t.as_str()) {
        Some("FeatureCollection") => {
            // Extract geometries from features
            if let Some(features) = geojson.get("features").and_then(|f| f.as_array()) {
                for feature in features {
                    if let Some(geom) = feature.get("geometry") {
                        if let Ok(g) = parse_geojson_geometry(geom) {
                            geometries.push(g);
                        }
                    }
                }
            }
        }
        Some("Feature") => {
            // Single feature
            if let Some(geom) = geojson.get("geometry") {
                if let Ok(g) = parse_geojson_geometry(geom) {
                    geometries.push(g);
                }
            }
        }
        Some("Point") | Some("LineString") | Some("Polygon") => {
            // Bare geometry
            if let Ok(g) = parse_geojson_geometry(&geojson) {
                geometries.push(g);
            }
        }
        _ => {
            return Err(GeoError::GeoJSONError(
                "Unsupported GeoJSON type".to_string(),
            ))
        }
    }

    Ok(geometries)
}

/// Parse a GeoJSON geometry object into our Geometry type.
fn parse_geojson_geometry(geom: &Value) -> Result<Geometry> {
    let geom_type = geom
        .get("type")
        .and_then(|t| t.as_str())
        .ok_or_else(|| GeoError::GeoJSONError("Missing geometry type".to_string()))?;

    let coords = geom
        .get("coordinates")
        .ok_or_else(|| GeoError::GeoJSONError("Missing coordinates".to_string()))?;

    match geom_type {
        "Point" => {
            let coords = coords
                .as_array()
                .ok_or_else(|| GeoError::GeoJSONError("Invalid Point coordinates".to_string()))?;
            if coords.len() < 2 {
                return Err(GeoError::GeoJSONError(
                    "Point needs at least 2 coordinates".to_string(),
                ));
            }
            let x = coords[0]
                .as_f64()
                .ok_or_else(|| GeoError::GeoJSONError("Invalid x coordinate".to_string()))?;
            let y = coords[1]
                .as_f64()
                .ok_or_else(|| GeoError::GeoJSONError("Invalid y coordinate".to_string()))?;

            Ok(Geometry::point(x, y))
        }
        "LineString" => {
            let coords_array = coords.as_array().ok_or_else(|| {
                GeoError::GeoJSONError("Invalid LineString coordinates".to_string())
            })?;

            let mut points = Vec::new();
            for coord in coords_array {
                let pt = coord.as_array().ok_or_else(|| {
                    GeoError::GeoJSONError("Invalid coordinate in LineString".to_string())
                })?;
                if pt.len() < 2 {
                    return Err(GeoError::GeoJSONError("Invalid coordinate".to_string()));
                }
                let x = pt[0]
                    .as_f64()
                    .ok_or_else(|| GeoError::GeoJSONError("Invalid x".to_string()))?;
                let y = pt[1]
                    .as_f64()
                    .ok_or_else(|| GeoError::GeoJSONError("Invalid y".to_string()))?;
                points.push((x, y));
            }

            use geo::LineString;
            let ls = LineString::from(points);
            Ok(Geometry::LineString(ls))
        }
        "Polygon" => {
            let rings = coords
                .as_array()
                .ok_or_else(|| GeoError::GeoJSONError("Invalid Polygon coordinates".to_string()))?;

            if rings.is_empty() {
                return Err(GeoError::GeoJSONError("Empty polygon".to_string()));
            }

            // Parse exterior ring
            let exterior_coords = rings[0].as_array().ok_or_else(|| {
                GeoError::GeoJSONError("Invalid exterior ring".to_string())
            })?;

            let mut exterior_points = Vec::new();
            for coord in exterior_coords {
                let pt = coord
                    .as_array()
                    .ok_or_else(|| GeoError::GeoJSONError("Invalid coordinate".to_string()))?;
                if pt.len() < 2 {
                    return Err(GeoError::GeoJSONError("Invalid coordinate".to_string()));
                }
                let x = pt[0]
                    .as_f64()
                    .ok_or_else(|| GeoError::GeoJSONError("Invalid x".to_string()))?;
                let y = pt[1]
                    .as_f64()
                    .ok_or_else(|| GeoError::GeoJSONError("Invalid y".to_string()))?;
                exterior_points.push((x, y));
            }

            use geo::{LineString, Polygon};
            let exterior = LineString::from(exterior_points);
            let polygon = Polygon::new(exterior, vec![]);
            Ok(Geometry::Polygon(polygon))
        }
        _ => Err(GeoError::GeoJSONError(format!(
            "Unsupported geometry type: {}",
            geom_type
        ))),
    }
}

/// Write geometries to GeoJSON FeatureCollection.
pub fn write_geojson<W: Write>(geometries: &[Geometry], writer: W) -> Result<()> {
    let mut features = Vec::new();

    for geom in geometries {
        let geom_json = geometry_to_geojson(geom)?;
        features.push(json!({
            "type": "Feature",
            "geometry": geom_json,
            "properties": {}
        }));
    }

    let feature_collection = json!({
        "type": "FeatureCollection",
        "features": features
    });

    serde_json::to_writer_pretty(writer, &feature_collection)
        .map_err(|e| GeoError::GeoJSONError(format!("Failed to write GeoJSON: {}", e)))?;

    Ok(())
}

/// Convert a Geometry to GeoJSON Value.
fn geometry_to_geojson(geom: &Geometry) -> Result<Value> {
    match geom {
        Geometry::Point(p) => Ok(json!({
            "type": "Point",
            "coordinates": [p.x(), p.y()]
        })),
        Geometry::LineString(ls) => {
            let coords: Vec<Vec<f64>> = ls
                .coords()
                .map(|c| vec![c.x, c.y])
                .collect();
            Ok(json!({
                "type": "LineString",
                "coordinates": coords
            }))
        }
        Geometry::Polygon(poly) => {
            let exterior: Vec<Vec<f64>> = poly
                .exterior()
                .coords()
                .map(|c| vec![c.x, c.y])
                .collect();
            Ok(json!({
                "type": "Polygon",
                "coordinates": [exterior]
            }))
        }
        _ => Err(GeoError::GeoJSONError(
            "Geometry type not yet supported for GeoJSON export".to_string(),
        )),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Cursor;

    #[test]
    fn test_read_geojson_point() {
        let geojson = r#"{
            "type": "Point",
            "coordinates": [1.0, 2.0]
        }"#;

        let geometries = read_geojson(Cursor::new(geojson)).unwrap();
        assert_eq!(geometries.len(), 1);
        assert_eq!(geometries[0].geometry_type(), "Point");
    }

    #[test]
    fn test_read_geojson_feature_collection() {
        let geojson = r#"{
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [1.0, 2.0]
                    },
                    "properties": {}
                }
            ]
        }"#;

        let geometries = read_geojson(Cursor::new(geojson)).unwrap();
        assert_eq!(geometries.len(), 1);
    }

    #[test]
    fn test_write_geojson() {
        let geom = Geometry::point(1.0, 2.0);
        let mut output = Vec::new();

        write_geojson(&[geom], &mut output).unwrap();

        let result = String::from_utf8(output).unwrap();
        assert!(result.contains("FeatureCollection"));
        assert!(result.contains("Point"));
    }

    #[test]
    fn test_geojson_roundtrip() {
        let original = Geometry::point(10.5, 20.3);

        // Write to GeoJSON
        let mut buffer = Vec::new();
        write_geojson(&[original], &mut buffer).unwrap();

        // Read back
        let geometries = read_geojson(Cursor::new(buffer)).unwrap();

        assert_eq!(geometries.len(), 1);
        assert_eq!(geometries[0].geometry_type(), "Point");
    }
}
