"""
I/O utilities for graph data formats.

This module provides readers and writers for various graph data formats,
with primary support for Apache GraphAr format.
"""

from .graphar import GraphArReader

__all__ = ["GraphArReader"]
