"""
Zanzibar-style permissions engine for ParquetFrame.

This module provides a graph-based permission system inspired by Google's Zanzibar,
implementing relation-based access control (ReBAC) using ParquetFrame's graph engine.

Core Components:
    - RelationTuple: Fundamental permission data structure
    - TupleStore: Efficient storage and querying of relation tuples
    - check(): Permission checking API
    - expand(): Permission expansion for bulk queries
    - list_objects()/list_subjects(): Bulk permission enumeration

Example Usage:
    >>> import parquetframe as pf
    >>> from parquetframe.permissions import RelationTuple, TupleStore, check

    >>> # Create a tuple store
    >>> store = TupleStore()

    >>> # Add some relations
    >>> store.add_tuple(RelationTuple("doc", "doc1", "viewer", "user", "alice"))
    >>> store.add_tuple(RelationTuple("doc", "doc1", "owner", "user", "bob"))

    >>> # Check permissions
    >>> check(store, "alice", "viewer", "doc", "doc1")  # True
    >>> check(store, "alice", "editor", "doc", "doc1")  # False
"""

from __future__ import annotations

from .api import check, expand, list_objects, list_subjects

# Core components
from .core import RelationTuple, TupleStore

# Utilities
from .models import PermissionModel, StandardModels

__all__ = [
    # Core data structures
    "RelationTuple",
    "TupleStore",
    # Permission APIs
    "check",
    "expand",
    "list_objects",
    "list_subjects",
    # Permission models
    "PermissionModel",
    "StandardModels",
]

__version__ = "0.1.0"
