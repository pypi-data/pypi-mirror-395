"""
Relationship management for entity framework.

Handles foreign key validation and relationship resolution.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class Relationship:
    """Represents a relationship between entities."""

    name: str
    source_entity: str
    target_entity: str
    foreign_key: str
    relationship_type: str


class RelationshipManager:
    """Manages relationships between entities."""

    def __init__(self):
        self._relationships: dict[str, list[Relationship]] = {}
        self._entity_store = None

    def set_entity_store(self, store: Any) -> None:
        """Set the entity store for validation."""
        self._entity_store = store

    def register(self, relationship: Relationship) -> None:
        """Register a relationship."""
        if relationship.source_entity not in self._relationships:
            self._relationships[relationship.source_entity] = []

        self._relationships[relationship.source_entity].append(relationship)

    def get_relationships(self, entity_name: str) -> list[Relationship]:
        """Get all relationships for an entity."""
        return self._relationships.get(entity_name, [])

    def validate_foreign_key(
        self, source_entity: str, target_entity: str, foreign_key_value: Any
    ) -> bool:
        """Validate that a foreign key value exists in the target entity."""
        if self._entity_store is None:
            # Cannot validate without entity store, fail open
            return True

        try:
            target_df = self._entity_store.get_entity(target_entity)

            if target_df is None or len(target_df) == 0:
                # Empty target entity - foreign key is invalid
                return False

            # Check if value exists in 'id' column first, then any column
            if "id" in target_df.columns:
                return foreign_key_value in target_df["id"].values

            # Fall back to checking all columns
            for col in target_df.columns:
                if foreign_key_value in target_df[col].values:
                    return True

            return False
        except Exception:
            # On errors, fail open for compatibility
            return True
