"""
Entity metadata and registry.

Tracks entity definitions, schemas, and configuration.
"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class EntityMetadata:
    """Metadata for an entity class."""

    name: str
    cls: type
    storage_path: Path
    primary_key: str
    format: str = "parquet"  # or "avro"
    fields: dict[str, type] = field(default_factory=dict)
    relationships: dict[str, "RelationshipMetadata"] = field(default_factory=dict)

    @property
    def storage_file(self) -> Path:
        """Get the storage file path for this entity."""
        suffix = ".parquet" if self.format == "parquet" else ".avro"
        return self.storage_path / f"{self.name}{suffix}"

    @property
    def entity_class(self) -> type:
        """Get the entity class (alias for cls)."""
        return self.cls


@dataclass
class RelationshipMetadata:
    """Metadata for a relationship between entities."""

    name: str
    source_entity: str
    target_entity: str
    foreign_key: str
    relationship_type: str = "one-to-many"  # or "many-to-one", "many-to-many"


class EntityRegistry:
    """Global registry for entity metadata."""

    _instance = None
    _entities: dict[str, EntityMetadata] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._entities = {}
        return cls._instance

    def register(self, metadata: EntityMetadata) -> None:
        """Register an entity."""
        self._entities[metadata.name] = metadata

    def get(self, name: str) -> EntityMetadata | None:
        """Get entity metadata by name."""
        return self._entities.get(name)

    def get_by_class(self, cls: type) -> EntityMetadata | None:
        """Get entity metadata by class."""
        for metadata in self._entities.values():
            if metadata.cls == cls:
                return metadata
        return None

    def list_entities(self) -> list[str]:
        """List all registered entity names."""
        return list(self._entities.keys())

    def clear(self) -> None:
        """Clear all registered entities (for testing)."""
        self._entities.clear()


# Singleton instance
registry = EntityRegistry()
