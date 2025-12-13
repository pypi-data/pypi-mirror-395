"""
GraphAr Schema generation.

Generates YAML schema definitions for entities and relationships
compatible with the GraphAr specification.
"""

import yaml


class GraphArSchema:
    """Generates GraphAr schema definitions."""

    @staticmethod
    def generate_entity_schema(entity_class: type, primary_key: str = "id") -> str:
        """
        Generate GraphAr YAML schema for an entity class.

        Args:
            entity_class: The entity class
            primary_key: Name of the primary key field

        Returns:
            YAML string of the schema
        """
        name = entity_class.__name__
        properties = []

        # Inspect class annotations if available
        if hasattr(entity_class, "__annotations__"):
            for prop_name, prop_type in entity_class.__annotations__.items():
                dtype = GraphArSchema._map_type(prop_type)
                properties.append(
                    {
                        "name": prop_name,
                        "data_type": dtype,
                        "is_primary": (prop_name == primary_key),
                    }
                )

        schema = {"name": name, "type": "VERTEX", "properties": properties}

        return yaml.dump(schema, sort_keys=False)

    @staticmethod
    def _map_type(py_type: type) -> str:
        """Map Python types to GraphAr types."""
        type_str = str(py_type)
        if py_type is int or "int" in type_str:
            return "INT64"
        elif py_type is float or "float" in type_str:
            return "DOUBLE"
        elif py_type is str or "str" in type_str:
            return "STRING"
        elif py_type is bool or "bool" in type_str:
            return "BOOLEAN"
        else:
            return "STRING"  # Fallback


__all__ = ["GraphArSchema"]
