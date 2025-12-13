/// Coordinate Reference System (CRS) management.
///
/// Handles CRS transformations. Uses PROJ library if "proj" feature is enabled.

use crate::{GeoError, Result};
use serde::{Deserialize, Serialize};

#[cfg(feature = "proj")]
use proj::Proj;

/// Coordinate Reference System.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CRS {
    /// EPSG code (e.g., 4326 for WGS84, 3857 for Web Mercator)
    epsg_code: Option<u32>,

    /// PROJ string representation
    proj_string: Option<String>,
}

impl CRS {
    /// Create a CRS from an EPSG code.
    ///
    /// # Examples
    ///
    /// ```ignore
    /// let wgs84 = CRS::from_epsg(4326);
    /// let web_mercator = CRS::from_epsg(3857);
    /// ```
    pub fn from_epsg(code: u32) -> Result<Self> {
        let proj_str = format!("EPSG:{}", code);

        #[cfg(feature = "proj")]
        {
            // Validate that we can create a Proj object
            Proj::new(&proj_str)
                .map_err(|e| GeoError::CRSError(format!("Invalid EPSG code {}: {}", code, e)))?;
        }

        Ok(CRS {
            epsg_code: Some(code),
            proj_string: Some(proj_str),
        })
    }

    /// Create a CRS from a PROJ string.
    pub fn from_proj_string(proj_string: impl Into<String>) -> Result<Self> {
        let proj_string = proj_string.into();

        #[cfg(feature = "proj")]
        {
            // Validate
            Proj::new(&proj_string)
                .map_err(|e| GeoError::CRSError(format!("Invalid PROJ string: {}", e)))?;
        }

        Ok(CRS {
            epsg_code: None,
            proj_string: Some(proj_string),
        })
    }

    /// Get the EPSG code if available.
    pub fn epsg_code(&self) -> Option<u32> {
        self.epsg_code
    }

    /// Get the PROJ string representation.
    pub fn proj_string(&self) -> Option<&str> {
        self.proj_string.as_deref()
    }

    /// Transform coordinates from this CRS to another CRS.
    ///
    /// # Arguments
    ///
    /// * `to_crs` - Target CRS
    /// * `x` - Longitude/X coordinate
    /// * `y` - Latitude/Y coordinate
    ///
    /// # Returns
    ///
    /// Transformed (x, y) coordinates
    pub fn transform(&self, to_crs: &CRS, x: f64, y: f64) -> Result<(f64, f64)> {
        #[cfg(feature = "proj")]
        {
            let from_proj = self.proj_string.as_ref()
                .ok_or_else(|| GeoError::CRSError("Source CRS has no PROJ string".to_string()))?;

            let to_proj = to_crs.proj_string.as_ref()
                .ok_or_else(|| GeoError::CRSError("Target CRS has no PROJ string".to_string()))?;

            // Create transformation
            let transformer = Proj::new_known_crs(from_proj, to_proj, None)
                .map_err(|e| GeoError::ProjectionError(format!("Failed to create transformer: {}", e)))?;

            // Transform point
            let (x_out, y_out) = transformer.convert((x, y))
                .map_err(|e| GeoError::ProjectionError(format!("Transformation failed: {}", e)))?;

            Ok((x_out, y_out))
        }

        #[cfg(not(feature = "proj"))]
        {
            // If PROJ is disabled, return error or identity if same CRS
            if self.proj_string == to_crs.proj_string {
                return Ok((x, y));
            }
            Err(GeoError::ProjectionError("PROJ support is disabled. Enable 'proj' feature for transformations.".to_string()))
        }
    }

    /// Common CRS: WGS 84 (EPSG:4326) - GPS coordinates
    pub fn wgs84() -> Result<Self> {
        Self::from_epsg(4326)
    }

    /// Common CRS: Web Mercator (EPSG:3857) - Web mapping
    pub fn web_mercator() -> Result<Self> {
        Self::from_epsg(3857)
    }
}

impl Default for CRS {
    fn default() -> Self {
        // Default to WGS84
        CRS::wgs84().unwrap()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_crs_creation() {
        let wgs84 = CRS::from_epsg(4326).unwrap();
        assert_eq!(wgs84.epsg_code(), Some(4326));
    }

    #[test]
    #[cfg(feature = "proj")]
    fn test_crs_transform() {
        let wgs84 = CRS::wgs84().unwrap();
        let web_merc = CRS::web_mercator().unwrap();

        // Transform New York coordinates (lon, lat)
        let (lon, lat) = (-74.0060, 40.7128);
        let (x, y) = wgs84.transform(&web_merc, lon, lat).unwrap();

        // Web Mercator coordinates should be in meters
        assert!(x.abs() > 1000.0); // Should be large values
        assert!(y.abs() > 1000.0);
    }

    #[test]
    fn test_common_crs() {
        let wgs84 = CRS::wgs84().unwrap();
        let web_merc = CRS::web_mercator().unwrap();

        assert_eq!(wgs84.epsg_code(), Some(4326));
        assert_eq!(web_merc.epsg_code(), Some(3857));
    }
}
