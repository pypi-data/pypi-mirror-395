"""
ParquetFrame Mobility Module

Provides mobility analytics operations with Rust acceleration.
"""

import pandas as pd

from parquetframe._rustic import mob as _mob


class MobAccessor:
    """Accessor for mobility and fleet analytics operations."""

    def __init__(self, df: pd.DataFrame):
        self._df = df

    def geofence_check(
        self,
        lon_col: str,
        lat_col: str,
        polygon_coords: list[tuple[float, float]],
        op: str = "within",
        output_col: str | None = None,
    ) -> pd.DataFrame:
        """
        Check if points are within/outside a geofence or detect enter/exit events.

        Args:
            lon_col: Column name for longitude
            lat_col: Column name for latitude
            polygon_coords: Geofence boundary as list of (lon, lat) tuples
            op: Operation type - 'within', 'outside', 'enter', or 'exit'
            output_col: Name for output column (default varies by operation)

        Returns:
            DataFrame with result column added (boolean for within/outside,
            indices array for enter/exit)
        """
        if op not in ["within", "outside", "enter", "exit"]:
            raise ValueError(
                f"Invalid operation '{op}'. Must be 'within', 'outside', 'enter', or 'exit'"
            )

        df = self._df.copy()

        if op in ["within", "outside"]:
            # Spatial operations (row-by-row)
            if output_col is None:
                output_col = f"geofence_{op}"

            results = []
            for _, row in df.iterrows():
                if op == "within":
                    result = _mob.mob_geofence_check_within(
                        row[lon_col], row[lat_col], polygon_coords
                    )
                else:  # outside
                    result = _mob.mob_geofence_check_outside(
                        row[lon_col], row[lat_col], polygon_coords
                    )
                results.append(result)

            df[output_col] = results
            return df

        else:
            # Temporal operations (enter/exit detection)
            if output_col is None:
                output_col = f"geofence_{op}_indices"

            lons = df[lon_col].values
            lats = df[lat_col].values

            if op == "enter":
                indices = _mob.mob_geofence_detect_enter(lons, lats, polygon_coords)
            else:  # exit
                indices = _mob.mob_geofence_detect_exit(lons, lats, polygon_coords)

            # Store indices as a column (could be improved to mark rows)
            df[output_col] = None
            df.at[df.index[0], output_col] = list(indices)
            return df

    def reconstruct_routes(
        self,
        lon_col: str,
        lat_col: str,
        output_col: str = "route_coords",
    ) -> pd.DataFrame:
        """
        Reconstruct route from GPS points.

        Args:
            lon_col: Column name for longitude
            lat_col: Column name for latitude
            output_col: Name for output column containing route coordinates

        Returns:
            DataFrame with route coordinates column added
        """
        df = self._df.copy()

        lons = df[lon_col].values
        lats = df[lat_col].values

        route_coords = _mob.mob_reconstruct_route(lons, lats)

        # Store the full route in the first row
        df[output_col] = None
        df.at[df.index[0], output_col] = route_coords

        return df

    def route_start_point(
        self,
        lon_col: str,
        lat_col: str,
    ) -> tuple[float, float]:
        """
        Get the start point of a route.

        Args:
            lon_col: Column name for longitude
            lat_col: Column name for latitude

        Returns:
            Tuple of (lon, lat) for the route start
        """
        lons = self._df[lon_col].values
        lats = self._df[lat_col].values

        return _mob.mob_route_start_point(lons, lats)

    def route_end_point(
        self,
        lon_col: str,
        lat_col: str,
    ) -> tuple[float, float]:
        """
        Get the end point of a route.

        Args:
            lon_col: Column name for longitude
            lat_col: Column name for latitude

        Returns:
            Tuple of (lon, lat) for the route end
        """
        lons = self._df[lon_col].values
        lats = self._df[lat_col].values

        return _mob.mob_route_end_point(lons, lats)

    def route_point_count(
        self,
        lon_col: str,
        lat_col: str,
    ) -> int:
        """
        Get the number of points in a route.

        Args:
            lon_col: Column name for longitude
            lat_col: Column name for latitude

        Returns:
            Number of points in the route
        """
        lons = self._df[lon_col].values
        lats = self._df[lat_col].values

        return _mob.mob_route_point_count(lons, lats)


# Register the accessor
@pd.api.extensions.register_dataframe_accessor("mob")
class MobDataFrameAccessor(MobAccessor):
    """Pandas DataFrame accessor for mobility operations."""

    pass


__all__ = ["MobAccessor", "MobDataFrameAccessor"]
