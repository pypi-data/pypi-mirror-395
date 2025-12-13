"""
GeoSpatial functionality for ParquetFrame.

Provides .geo accessor for GeoDataFrames.
"""

# Import accessor to register it
from .accessor import GeoAccessor

__all__ = ["GeoAccessor"]
