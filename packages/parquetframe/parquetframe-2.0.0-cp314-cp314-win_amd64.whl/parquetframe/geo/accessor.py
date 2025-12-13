"""
GeoSpatial Accessor for ParquetFrame.

Provides .geo accessor for geospatial operations on GeoDataFrames.
"""

import importlib.util

import pandas as pd


class GeoAccessor:
    """
    Geospatial operations accessor.

    Accessed via gdf.geo for GeoDataFrames.

    Example:
        >>> import geopandas as gpd
        >>> gdf = gpd.read_file("cities.geojson")
        >>> buffered = gdf.geo.buffer(1000)  # 1km buffer
        >>> area = gdf.geo.area()
    """

    def __init__(self, geopandas_obj):
        """Initialize accessor with GeoDataFrame."""
        self._obj = geopandas_obj

        # Check if it's a GeoDataFrame
        try:
            import geopandas as gpd

            if not isinstance(self._obj, gpd.GeoDataFrame):
                raise AttributeError(
                    ".geo accessor requires a GeoDataFrame. "
                    "Use gpd.GeoDataFrame.from_file() or set_geometry() first."
                )
        except ImportError:
            raise ImportError(
                "GeoSpatial operations require 'geopandas'. "
                "Install with: pip install geopandas"
            ) from ImportError

    def buffer(self, distance: float, **kwargs) -> pd.DataFrame:
        """
        Create buffer around geometries.

        Args:
            distance: Buffer distance in units of CRS
            **kwargs: Additional arguments for buffer

        Returns:
            GeoDataFrame with buffered geometries
        """
        result = self._obj.copy()
        result.geometry = result.geometry.buffer(distance, **kwargs)
        return result

    def area(self) -> pd.Series:
        """Calculate area of geometries."""
        return self._obj.geometry.area

    def length(self) -> pd.Series:
        """Calculate length/perimeter of geometries."""
        return self._obj.geometry.length

    def distance(self, other, **kwargs) -> pd.Series:
        """
        Calculate distance to other geometry.

        Args:
            other: Geometry or GeoSeries to calculate distance to
            **kwargs: Additional arguments

        Returns:
            Series of distances
        """
        return self._obj.geometry.distance(other, **kwargs)

    def centroid(self) -> pd.DataFrame:
        """Get centroids of geometries."""
        result = self._obj.copy()
        result.geometry = result.geometry.centroid
        return result

    def intersection(self, other, **kwargs) -> pd.DataFrame:
        """
        Calculate intersection with other geometry.

        Args:
            other: Geometry to intersect with
            **kwargs: Additional arguments

        Returns:
            GeoDataFrame with intersection geometries
        """
        result = self._obj.copy()
        result.geometry = result.geometry.intersection(other, **kwargs)
        return result

    def union(self, other=None, **kwargs) -> pd.DataFrame:
        """
        Calculate union of geometries.

        Args:
            other: Optional geometry to union with
            **kwargs: Additional arguments

        Returns:
            GeoDataFrame with union geometries
        """
        result = self._obj.copy()
        if other is not None:
            result.geometry = result.geometry.union(other, **kwargs)
        else:
            # Union all geometries together
            result.geometry = result.geometry.unary_union
        return result

    def contains(self, other, **kwargs) -> pd.Series:
        """Check if geometries contain other geometry."""
        return self._obj.geometry.contains(other, **kwargs)

    def within(self, other, **kwargs) -> pd.Series:
        """Check if geometries are within other geometry."""
        return self._obj.geometry.within(other, **kwargs)

    def intersects(self, other, **kwargs) -> pd.Series:
        """Check if geometries intersect with other geometry."""
        return self._obj.geometry.intersects(other, **kwargs)

    def to_crs(self, crs, **kwargs) -> pd.DataFrame:
        """
        Transform to different coordinate reference system.

        Args:
            crs: Target CRS (e.g., 'EPSG:4326')
            **kwargs: Additional arguments

        Returns:
            GeoDataFrame in new CRS
        """
        return self._obj.to_crs(crs, **kwargs)

    def sjoin(self, other, how: str = "inner", predicate: str = "intersects", **kwargs):
        """
        Spatial join with another GeoDataFrame.

        Args:
            other: GeoDataFrame to join with
            how: Type of join ('inner', 'left', 'right')
            predicate: Spatial relationship ('intersects', 'contains', 'within')
            **kwargs: Additional arguments

        Returns:
            Joined GeoDataFrame
        """
        import geopandas as gpd

        return gpd.sjoin(self._obj, other, how=how, predicate=predicate, **kwargs)


# Register accessor with geopandas


if importlib.util.find_spec("geopandas"):
    import geopandas as gpd  # noqa: F401
    import pandas as pd

    @pd.api.extensions.register_dataframe_accessor("geo")
    class GeoDataFrameAccessor(GeoAccessor):
        """GeoDataFrame accessor for spatial operations."""

        pass

else:
    # GeoPandas not installed, skip registration
    pass


__all__ = ["GeoAccessor"]
