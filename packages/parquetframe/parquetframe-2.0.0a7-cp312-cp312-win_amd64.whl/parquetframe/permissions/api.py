"""
Core API functions for Zanzibar-style permission checking and expansion.

This module implements the main permission APIs:
- check(): Verify if a subject has a specific relation to an object
- expand(): Find all objects a subject has a relation to
- list_objects(): Get all objects with a specific relation
- list_subjects(): Get all subjects with a relation to an object

Uses graph traversal algorithms from Phase 1.2 for efficient permission resolution.
"""

from __future__ import annotations

import pandas as pd

from ..core_legacy import (
    ParquetFrame,  # Internal use only - avoids deprecation warnings
)
from ..graph import GraphFrame
from ..graph.algo.shortest_path import shortest_path
from .core import RelationTuple, TupleStore


class PermissionError(Exception):
    """Base exception for permission-related errors."""

    pass


class TupleNotFoundError(PermissionError):
    """Raised when a required relation tuple is not found."""

    pass


def check(
    store: TupleStore,
    subject_namespace: str,
    subject_id: str,
    relation: str,
    object_namespace: str,
    object_id: str,
    allow_indirect: bool = True,
) -> bool:
    """
    Check if a subject has a specific relation to an object.

    This is the core permission checking function that determines whether:
    subject_namespace:subject_id has relation to object_namespace:object_id

    Supports both direct and indirect (transitive) permission checking.

    Args:
        store: TupleStore containing relation tuples
        subject_namespace: The subject's namespace (e.g., "user", "group")
        subject_id: The subject's ID (e.g., "alice", "eng-team")
        relation: The relation to check (e.g., "viewer", "editor")
        object_namespace: The object's namespace (e.g., "doc", "folder")
        object_id: The object's ID (e.g., "doc1", "folder1")
        allow_indirect: Whether to check for indirect permissions via graph traversal

    Returns:
        True if the subject has the relation to the object, False otherwise

    Examples:
        >>> # Direct permission check
        >>> check(store, "user", "alice", "viewer", "doc", "doc1")
        True

        >>> # Indirect permission via group membership
        >>> check(store, "user", "alice", "editor", "doc", "doc1", allow_indirect=True)
        True  # alice is member of group that has editor access

        >>> # Failed permission check
        >>> check(store, "user", "bob", "admin", "doc", "doc1")
        False
    """
    if store.is_empty():
        return False

    # First, check for direct permission
    direct_tuple = RelationTuple(
        namespace=object_namespace,
        object_id=object_id,
        relation=relation,
        subject_namespace=subject_namespace,
        subject_id=subject_id,
    )

    if store.has_tuple(direct_tuple):
        return True

    if not allow_indirect:
        return False

    # If direct check failed and indirect is allowed, use graph traversal
    # to find transitive permissions
    return _check_indirect_permission(
        store, subject_namespace, subject_id, relation, object_namespace, object_id
    )


def _check_indirect_permission(
    store: TupleStore,
    subject_namespace: str,
    subject_id: str,
    relation: str,
    object_namespace: str,
    object_id: str,
) -> bool:
    """
    Check for indirect permissions using graph traversal.

    This builds a graph from relation tuples and uses BFS to find
    if there's a path from the subject to the object through various relations.
    """
    try:
        # Build a permission graph from the tuple store
        graph = _build_permission_graph(store, relation)

        # Create vertex IDs for subject and object
        subject_vertex = f"{subject_namespace}:{subject_id}"
        object_vertex = f"{object_namespace}:{object_id}"

        # Use shortest path algorithm to find if there's a connection
        # If a path exists, the subject has indirect permission
        try:
            result = shortest_path(
                graph=graph,
                source=subject_vertex,
                target=object_vertex,
                weight_column=None,  # Unweighted for permission checks
                backend="auto",
            )

            # If we get a result back, a path exists
            return len(result) > 0 and not result["distance"].iloc[0] == float("inf")

        except Exception:
            # If shortest path fails, permission denied
            return False

    except Exception:
        # If graph building fails, fall back to direct permission only
        return False


def _build_permission_graph(store: TupleStore, target_relation: str) -> GraphFrame:
    """
    Build a directed graph from relation tuples for permission traversal.

    The graph represents permission relationships where:
    - Vertices are subject/object references (namespace:id)
    - Edges represent relation connections
    - Edge direction follows permission flow

    Args:
        store: TupleStore containing relation tuples
        target_relation: The relation type we're checking for

    Returns:
        GraphFrame representing the permission graph
    """
    if store.is_empty():
        # Return empty graph
        empty_vertices = pd.DataFrame({"vertex_id": []})
        empty_edges = pd.DataFrame({"src": [], "dst": []})
        return GraphFrame(
            vertices=ParquetFrame(empty_vertices),
            edges=ParquetFrame(empty_edges),
            metadata={"directed": True},
        )

    # Get all tuples for the target relation
    relation_tuples = store.query_tuples(relation=target_relation)

    if not relation_tuples:
        # No tuples for this relation
        empty_vertices = pd.DataFrame({"vertex_id": []})
        empty_edges = pd.DataFrame({"src": [], "dst": []})
        return GraphFrame(
            vertices=ParquetFrame(empty_vertices),
            edges=ParquetFrame(empty_edges),
            metadata={"directed": True},
        )

    # Build vertices (all unique subjects and objects)
    vertices = set()
    edges = []

    for tuple_obj in relation_tuples:
        subject_ref = tuple_obj.subject_ref
        object_ref = tuple_obj.object_ref

        vertices.add(subject_ref)
        vertices.add(object_ref)

        # Create edge from subject to object (subject can access object)
        edges.append({"src": subject_ref, "dst": object_ref})

    # Create vertex DataFrame
    vertex_df = pd.DataFrame({"vertex_id": list(vertices)})

    # Create edge DataFrame
    edge_df = pd.DataFrame(edges)

    # Handle empty graph case
    if vertex_df.empty:
        vertex_df = pd.DataFrame({"vertex_id": []})
    if edge_df.empty:
        edge_df = pd.DataFrame({"src": [], "dst": []})

    return GraphFrame(
        vertices=ParquetFrame(vertex_df),
        edges=ParquetFrame(edge_df),
        metadata={"directed": True},
    )


def expand(
    store: TupleStore,
    subject_namespace: str,
    subject_id: str,
    relation: str,
    object_namespace: str | None = None,
    allow_indirect: bool = True,
) -> list[tuple[str, str]]:
    """
    Find all objects that a subject has a specific relation to.

    This is useful for:
    - Finding all documents a user can view
    - Listing all folders a user can edit
    - Generating permission lists for UI

    Args:
        store: TupleStore containing relation tuples
        subject_namespace: The subject's namespace
        subject_id: The subject's ID
        relation: The relation to expand
        object_namespace: Optional filter by object namespace
        allow_indirect: Whether to include indirectly accessible objects

    Returns:
        List of (object_namespace, object_id) tuples the subject can access

    Examples:
        >>> # Find all documents alice can view
        >>> expand(store, "user", "alice", "viewer", "doc")
        [("doc", "doc1"), ("doc", "doc2"), ("doc", "doc3")]

        >>> # Find all resources bob can edit (any namespace)
        >>> expand(store, "user", "bob", "editor")
        [("doc", "doc1"), ("folder", "folder1"), ("project", "proj1")]
    """
    if store.is_empty():
        return []

    # Start with direct permissions
    direct_objects = store.get_objects_for_subject(
        subject_namespace=subject_namespace,
        subject_id=subject_id,
        relation=relation,
        namespace=object_namespace,
    )

    if not allow_indirect:
        return direct_objects

    # For indirect permissions, we need to find all reachable objects
    # through the permission graph
    try:
        graph = _build_permission_graph(store, relation)
        subject_vertex = f"{subject_namespace}:{subject_id}"

        # Find all vertices reachable from the subject
        reachable = _find_reachable_objects(graph, subject_vertex)

        # Convert back to (namespace, object_id) tuples
        indirect_objects = []
        for vertex in reachable:
            if ":" in vertex:
                ns, obj_id = vertex.split(":", 1)
                if object_namespace is None or ns == object_namespace:
                    indirect_objects.append((ns, obj_id))

        # Combine direct and indirect, remove duplicates
        all_objects = list(set(direct_objects + indirect_objects))
        return sorted(all_objects)

    except Exception:
        # If graph traversal fails, return just direct permissions
        return direct_objects


def _find_reachable_objects(graph: GraphFrame, source_vertex: str) -> list[str]:
    """
    Find all vertices reachable from a source vertex using BFS.

    Args:
        graph: GraphFrame to traverse
        source_vertex: Starting vertex

    Returns:
        List of reachable vertex IDs
    """
    try:
        # Use shortest_path with no target to get all reachable vertices
        result = shortest_path(
            graph=graph,
            source=source_vertex,
            target=None,  # All vertices
            weight_column=None,
            backend="auto",
        )

        # Filter out unreachable vertices (distance = inf)
        reachable = result[result["distance"] != float("inf")]
        return reachable["target"].tolist()

    except Exception:
        return []


def list_objects(
    store: TupleStore,
    relation: str,
    object_namespace: str | None = None,
) -> list[tuple[str, str]]:
    """
    List all objects that have the specified relation.

    Args:
        store: TupleStore containing relation tuples
        relation: The relation to list objects for
        object_namespace: Optional filter by object namespace

    Returns:
        List of (object_namespace, object_id) tuples

    Examples:
        >>> # Find all viewable documents
        >>> list_objects(store, "viewer", "doc")
        [("doc", "doc1"), ("doc", "doc2")]
    """
    if store.is_empty():
        return []

    relation_tuples = store.query_tuples(
        relation=relation,
        namespace=object_namespace,
    )

    objects = [(t.namespace, t.object_id) for t in relation_tuples]
    return sorted(set(objects))


def list_subjects(
    store: TupleStore,
    relation: str,
    object_namespace: str,
    object_id: str,
    subject_namespace: str | None = None,
) -> list[tuple[str, str]]:
    """
    List all subjects that have a specific relation to an object.

    Args:
        store: TupleStore containing relation tuples
        relation: The relation to check
        object_namespace: The object's namespace
        object_id: The object's ID
        subject_namespace: Optional filter by subject namespace

    Returns:
        List of (subject_namespace, subject_id) tuples

    Examples:
        >>> # Find all users who can view doc1
        >>> list_subjects(store, "viewer", "doc", "doc1", "user")
        [("user", "alice"), ("user", "bob")]
    """
    if store.is_empty():
        return []

    subjects = store.get_subjects_for_object(
        namespace=object_namespace,
        object_id=object_id,
        relation=relation,
        subject_namespace=subject_namespace,
    )

    return sorted(subjects)


def batch_check(
    store: TupleStore,
    checks: list[tuple[str, str, str, str, str]],
    allow_indirect: bool = True,
) -> list[bool]:
    """
    Perform multiple permission checks efficiently.

    Args:
        store: TupleStore containing relation tuples
        checks: List of (subject_ns, subject_id, relation, object_ns, object_id) tuples
        allow_indirect: Whether to allow indirect permissions

    Returns:
        List of boolean results corresponding to each check

    Examples:
        >>> checks = [
        ...     ("user", "alice", "viewer", "doc", "doc1"),
        ...     ("user", "bob", "editor", "doc", "doc2"),
        ...     ("user", "charlie", "admin", "folder", "folder1"),
        ... ]
        >>> batch_check(store, checks)
        [True, False, True]
    """
    results = []

    for subject_ns, subject_id, relation, object_ns, object_id in checks:
        result = check(
            store=store,
            subject_namespace=subject_ns,
            subject_id=subject_id,
            relation=relation,
            object_namespace=object_ns,
            object_id=object_id,
            allow_indirect=allow_indirect,
        )
        results.append(result)

    return results
