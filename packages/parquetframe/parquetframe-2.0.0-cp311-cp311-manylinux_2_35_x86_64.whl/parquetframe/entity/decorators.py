"""
Decorators for entity and relationship definition.

Provides @entity and @rel decorators for data modeling.
"""

from collections.abc import Callable
from dataclasses import fields, is_dataclass
from functools import wraps
from pathlib import Path
from typing import Any, TypeVar

from .entity_store import EntityStore
from .metadata import EntityMetadata, registry
from .query import RelationshipQuery

T = TypeVar("T")


def entity(
    storage_path: str | Path,
    primary_key: str,
    format: str = "parquet",
    base_path: str | Path | None = None,
) -> Callable[[type[T]], type[T]]:
    """
    Decorator to mark a dataclass as an entity with persistence.

    Args:
        storage_path: Directory or file path for entity storage
        primary_key: Name of the primary key field
        format: Storage format ('parquet' or 'avro')
        base_path: Optional base path for relative storage paths

    Returns:
        Decorated class with persistence methods

    Example:
        >>> @entity(storage_path="users", primary_key="user_id")
        >>> @dataclass
        >>> class User:
        >>>     user_id: int
        >>>     name: str
        >>>     email: str
        >>>
        >>> # Usage
        >>> user = User(1, "Alice", "alice@example.com")
        >>> user.save()
        >>> loaded = User.find(1)
    """

    def decorator(cls: type[T]) -> type[T]:
        # Verify it's a dataclass
        if not is_dataclass(cls):
            raise TypeError(f"{cls.__name__} must be a dataclass to use @entity")

        # Resolve storage path
        resolved_path = Path(storage_path)
        if base_path:
            resolved_path = Path(base_path) / resolved_path

        # Ensure storage directory exists
        resolved_path.mkdir(parents=True, exist_ok=True)

        # Extract field information
        field_types = {}
        for field_obj in fields(cls):
            field_types[field_obj.name] = field_obj.type

        # Verify primary key exists
        if primary_key not in field_types:
            raise ValueError(
                f"Primary key '{primary_key}' not found in {cls.__name__} fields"
            )

        # Create metadata
        metadata = EntityMetadata(
            name=cls.__name__,
            cls=cls,
            storage_path=resolved_path,
            primary_key=primary_key,
            format=format,
            fields=field_types,
        )

        # Register entity

        registry.register(metadata)

        # Create entity store for this entity
        store = EntityStore(metadata)

        # Add persistence methods to the class
        def save(self) -> None:
            """Save this entity instance to storage."""
            store.save(self)

        def delete(self) -> None:
            """Delete this entity instance from storage."""
            pk_value = getattr(self, metadata.primary_key)
            store.delete(pk_value)

        @classmethod
        def find(cls, pk_value: Any) -> T | None:
            """
            Find entity by primary key.

            Args:
                pk_value: Primary key value

            Returns:
                Entity instance or None if not found
            """
            return store.find(pk_value)

        @classmethod
        def find_all(cls) -> list[T]:
            """
            Find all entities of this type.

            Returns:
                List of entity instances
            """
            return store.find_all()

        @classmethod
        def find_by(cls, **filters: Any) -> list[T]:
            """
            Find entities matching filters.

            Args:
                **filters: Field name and value pairs to filter by

            Returns:
                List of matching entity instances
            """
            return store.find_by(**filters)

        @classmethod
        def count(cls) -> int:
            """
            Count total entities of this type.

            Returns:
                Number of entities
            """
            return store.count()

        @classmethod
        def delete_all(cls) -> None:
            """Delete all entities of this type."""
            store.delete_all()

        # Attach methods to the class
        cls.save = save
        cls.delete = delete
        cls.find = find
        cls.find_all = find_all
        cls.find_by = find_by
        cls.count = count
        cls.delete_all = delete_all

        # Store metadata on the class
        cls._entity_metadata = metadata
        cls._entity_store = store

        # Register relationships defined with @rel decorator
        for attr_name in dir(cls):
            if attr_name.startswith("_"):
                continue

            attr = getattr(cls, attr_name)
            if callable(attr) and hasattr(attr, "_rel_target"):
                # This method was decorated with @rel
                target_name = (
                    attr._rel_target
                    if isinstance(attr._rel_target, str)
                    else attr._rel_target.__name__
                )

                # Register relationship metadata
                metadata.relationships[attr_name] = {
                    "target": target_name,
                    "foreign_key": attr._rel_foreign_key,
                    "reverse": attr._rel_reverse,
                }

        return cls

    return decorator


def rel(
    target: str | type,
    foreign_key: str,
    reverse: bool = False,
) -> Callable:
    """
    Decorator to define a relationship between entities.

    Used as a method decorator on entity classes to define relationships.

    Args:
        target: Target entity class name (string) or class
        foreign_key: Foreign key field name
        reverse: If True, this is a reverse relationship (one-to-many from target's perspective)

    Returns:
        Decorated function that resolves the relationship

    Example:
        >>> @entity(storage_path="users", primary_key="user_id")
        >>> @dataclass
        >>> class User:
        >>>     user_id: int
        >>>     name: str
        >>>
        >>>     @rel("Post", foreign_key="user_id", reverse=True)
        >>>     def posts(self):
        >>>         '''Get all posts for this user.'''
        >>>         pass
        >>>
        >>> @entity(storage_path="posts", primary_key="post_id")
        >>> @dataclass
        >>> class Post:
        >>>     post_id: int
        >>>     user_id: int
        >>>     title: str
        >>>
        >>>     @rel("User", foreign_key="user_id")
        >>>     def author(self):
        >>>         '''Get the author of this post.'''
        >>>         pass
    """

    def decorator(func: Callable) -> Callable:
        # Store metadata to be resolved later when entity class is available
        @wraps(func)
        def wrapper(self, **kwargs: Any) -> list[Any] | Any | None | RelationshipQuery:
            """Resolve the relationship with optional filtering."""
            # Get source entity metadata from self
            source_class = self.__class__
            source_metadata = registry.get_by_class(source_class)

            if not source_metadata:
                raise ValueError(f"{source_class.__name__} is not a registered entity")

            # Get target entity metadata
            target_name = target if isinstance(target, str) else target.__name__
            target_metadata = registry.get(target_name)

            if not target_metadata:
                raise ValueError(f"Target entity '{target_name}' is not registered")

            if not reverse:
                # Forward relationship: get the foreign key value from self
                # and find the target entity with that primary key
                fk_value = getattr(self, foreign_key)

                # Query target using its primary key
                target_store = EntityStore(target_metadata)
                result = target_store.find(fk_value)
                return result
            else:
                # Reverse relationship: find all target entities where
                # their foreign key matches our primary key
                pk_value = getattr(self, source_metadata.primary_key)

                # Create filter function that queries the target store
                def filter_func(filters: dict[str, Any]) -> list[Any]:
                    # Always filter by the FK matching our PK
                    combined_filters = {foreign_key: pk_value, **filters}
                    target_store = EntityStore(target_metadata)
                    return target_store.find_by(**combined_filters)

                # If kwargs provided, create query with initial filters and execute
                if kwargs:
                    query = RelationshipQuery(
                        target_metadata.cls,
                        filter_func,
                        filters=kwargs,
                        source_instance=self,
                        rel_name=func.__name__,
                    )
                    return query.all()  # Execute immediately for backward compatibility
                else:
                    # No filters, return query builder for chaining
                    return RelationshipQuery(
                        target_metadata.cls,
                        filter_func,
                        filters={},
                        source_instance=self,
                        rel_name=func.__name__,
                    )

        # Store relationship info for registration
        wrapper._rel_target = target
        wrapper._rel_foreign_key = foreign_key
        wrapper._rel_reverse = reverse
        wrapper._rel_func_name = func.__name__

        return wrapper

    return decorator
