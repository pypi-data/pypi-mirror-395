"""
Entity graph visualization support for ParquetFrame.

Provides utilities to visualize entity relationships using NetworkX and PyVis.
Enables users to explore entity graphs interactively.
"""

from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass

# Optional dependencies
try:
    import networkx as nx

    NETWORKX_AVAILABLE = True
except ImportError:
    nx = None
    NETWORKX_AVAILABLE = False

try:
    from pyvis.network import Network

    PYVIS_AVAILABLE = True
except ImportError:
    Network = None
    PYVIS_AVAILABLE = False


def entities_to_networkx(
    entities: list[Any],
    include_relationships: bool = True,
    max_depth: int = 1,
) -> "nx.DiGraph":
    """
    Convert entities to NetworkX directed graph.

    Args:
        entities: List of entity instances to convert
        include_relationships: Whether to follow and include relationships
        max_depth: Maximum relationship depth to traverse

    Returns:
        NetworkX directed graph

    Example:
        >>> import networkx as nx
        >>> from parquetframe.entity.visualization import entities_to_networkx
        >>>
        >>> users = User.find_all()
        >>> G = entities_to_networkx(users, max_depth=2)
        >>> print(f"Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")
    """
    if not NETWORKX_AVAILABLE:
        raise ImportError(
            "NetworkX is required for graph visualization. "
            "Install with: pip install networkx"
        )

    G = nx.DiGraph()
    visited = set()

    def add_entity(entity: Any, depth: int = 0) -> None:
        """Recursively add entity and its relationships to graph."""
        if depth > max_depth:
            return

        # Get entity metadata
        if not hasattr(entity.__class__, "_entity_metadata"):
            return

        metadata = entity.__class__._entity_metadata
        pk_value = getattr(entity, metadata.primary_key)
        node_id = f"{metadata.name}:{pk_value}"

        if node_id in visited:
            return
        visited.add(node_id)

        # Add node with attributes
        G.add_node(
            node_id,
            entity_type=metadata.name,
            primary_key=pk_value,
            label=f"{metadata.name}\n{pk_value}",
        )

        # Add relationships if enabled
        if include_relationships and depth < max_depth:
            for rel_name, rel_info in metadata.relationships.items():
                try:
                    # Get the relationship method
                    rel_method = getattr(entity, rel_name)
                    related = rel_method()

                    # Handle both single and multiple results
                    if related is None:
                        continue

                    # Convert RelationshipQuery to list
                    if hasattr(related, "all"):
                        related = related.all()

                    if not isinstance(related, list):
                        related = [related]

                    # Add edges to related entities
                    for rel_entity in related:
                        if rel_entity:
                            rel_metadata = rel_entity.__class__._entity_metadata
                            rel_pk = getattr(rel_entity, rel_metadata.primary_key)
                            rel_node_id = f"{rel_metadata.name}:{rel_pk}"

                            # Determine edge direction based on reverse flag
                            if rel_info.get("reverse"):
                                # Reverse relationship: entity -> related
                                G.add_edge(
                                    node_id,
                                    rel_node_id,
                                    relationship=rel_name,
                                    label=rel_name,
                                )
                            else:
                                # Forward relationship: related <- entity
                                G.add_edge(
                                    rel_node_id,
                                    node_id,
                                    relationship=rel_name,
                                    label=rel_name,
                                )

                            # Recursively add related entity
                            add_entity(rel_entity, depth + 1)

                except Exception:
                    # Skip relationships that can't be resolved
                    continue

    # Add all input entities
    for entity in entities:
        add_entity(entity, depth=0)

    return G


def visualize_with_pyvis(
    graph: "nx.DiGraph",
    output_path: str | Path = "entity_graph.html",
    height: str = "750px",
    width: str = "100%",
    notebook: bool = False,
) -> str:
    """
    Create interactive HTML visualization using PyVis.

    Args:
        graph: NetworkX graph to visualize
        output_path: Path to save HTML file
        height: Height of visualization
        width: Width of visualization
        notebook: Whether to display in Jupyter notebook

    Returns:
        Path to generated HTML file

    Example:
        >>> G = entities_to_networkx(users)
        >>> visualize_with_pyvis(G, "users_graph.html")
        'users_graph.html'
    """
    if not PYVIS_AVAILABLE:
        raise ImportError(
            "PyVis is required for interactive visualization. "
            "Install with: pip install pyvis"
        )

    # Create PyVis network
    net = Network(height=height, width=width, directed=True, notebook=notebook)

    # Configure physics for better layout
    net.barnes_hut(
        gravity=-8000,
        central_gravity=0.3,
        spring_length=250,
        spring_strength=0.001,
        damping=0.09,
    )

    # Add nodes with colors based on entity type
    entity_colors = {}
    color_palette = [
        "#FF6B6B",
        "#4ECDC4",
        "#45B7D1",
        "#FFA07A",
        "#98D8C8",
        "#F7DC6F",
        "#BB8FCE",
        "#85C1E2",
    ]

    for node, data in graph.nodes(data=True):
        entity_type = data.get("entity_type", "Unknown")

        # Assign color per entity type
        if entity_type not in entity_colors:
            color_idx = len(entity_colors) % len(color_palette)
            entity_colors[entity_type] = color_palette[color_idx]

        net.add_node(
            node,
            label=data.get("label", node),
            title=f"{entity_type}: {data.get('primary_key')}",
            color=entity_colors[entity_type],
            shape="box",
        )

    # Add edges
    for source, target, data in graph.edges(data=True):
        net.add_edge(
            source,
            target,
            title=data.get("relationship", ""),
            label=data.get("label", ""),
            arrows="to",
        )

    # Save to file
    output_path = Path(output_path)
    net.save_graph(str(output_path))

    return str(output_path)


def export_to_graphviz(
    graph: "nx.DiGraph",
    output_path: str | Path = "entity_graph.dot",
) -> str:
    """
    Export graph to Graphviz DOT format.

    Args:
        graph: NetworkX graph to export
        output_path: Path to save DOT file

    Returns:
        Path to generated DOT file

    Example:
        >>> G = entities_to_networkx(users)
        >>> export_to_graphviz(G, "users.dot")
        'users.dot'
        >>> # Then: dot -Tpng users.dot -o users.png
    """
    if not NETWORKX_AVAILABLE:
        raise ImportError("NetworkX is required")

    try:
        from networkx.drawing.nx_pydot import write_dot
    except ImportError:
        raise ImportError(
            "pydot is required for Graphviz export. Install with: pip install pydot"
        ) from ImportError

    output_path = Path(output_path)
    write_dot(graph, output_path)

    return str(output_path)


def is_visualization_available() -> dict[str, bool]:
    """
    Check which visualization libraries are available.

    Returns:
        Dictionary of library availability

    Example:
        >>> from parquetframe.entity.visualization import is_visualization_available
        >>> avail = is_visualization_available()
        >>> if avail["networkx"]:
        ...     print("NetworkX graphs available")
        >>> if avail["pyvis"]:
        ...     print("Interactive HTML visualizations available")
    """
    return {
        "networkx": NETWORKX_AVAILABLE,
        "pyvis": PYVIS_AVAILABLE,
    }


__all__ = [
    "entities_to_networkx",
    "visualize_with_pyvis",
    "export_to_graphviz",
    "is_visualization_available",
]
