"""
High-level visualization API.

Exposes entity graph visualization capabilities in a simple API.
"""

# Import from existing visualization module
from .entity.entity_store import EntityStore
from .entity.metadata import registry
from .entity.visualization import (
    entities_to_networkx,
    export_to_graphviz,
    is_visualization_available,
    visualize_with_pyvis,
)


def visualize_store(
    entity_types: list[type] | None = None,
    output_path: str = "entity_graph.html",
    include_relationships: bool = True,
    max_depth: int = 2,
    notebook: bool = False,
) -> str:
    """
    Visualize entities from the store.

    Args:
        entity_types: List of entity classes to include (None = all)
        output_path: Path to save the visualization
        include_relationships: Whether to include edges
        max_depth: Depth of relationship traversal
        notebook: Whether to render for Jupyter notebook

    Returns:
        Path to the generated file
    """
    # Check availability
    avail = is_visualization_available()
    if not avail["networkx"] or not avail["pyvis"]:
        raise ImportError(
            "Visualization requires networkx and pyvis. "
            "Install with: pip install networkx pyvis"
        )

    # Collect entities
    entities = []

    if entity_types is None:
        # Load all registered entities
        # Note: This could be heavy for large stores!
        # In a real scenario, we might want to sample or limit.
        for name in registry.list_entities():
            metadata = registry.get(name)
            if metadata:
                store = EntityStore(metadata)
                entities.extend(store.find_all())
    else:
        for cls in entity_types:
            metadata = registry.get_by_class(cls)
            if metadata:
                store = EntityStore(metadata)
                entities.extend(store.find_all())

    if not entities:
        print("No entities found to visualize.")
        return ""

    # Convert to graph
    G = entities_to_networkx(
        entities, include_relationships=include_relationships, max_depth=max_depth
    )

    # Render
    return visualize_with_pyvis(G, output_path=output_path, notebook=notebook)


__all__ = [
    "visualize_store",
    "entities_to_networkx",
    "visualize_with_pyvis",
    "export_to_graphviz",
]
