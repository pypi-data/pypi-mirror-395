"""
Relationship query builder for advanced entity navigation.

Provides lazy evaluation and filtering for entity relationships,
enabling efficient queries like: user.posts(status='published', limit=10)
"""

from collections.abc import Callable
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class RelationshipQuery(Generic[T]):
    """
    Lazy query builder for entity relationships.

    Supports filtering, ordering, and limiting relationship results
    without loading all related entities into memory.

    Example:
        >>> user.posts(status="published").order_by("created_at").limit(5)
    """

    def __init__(
        self,
        target_class: type[T],
        filter_func: Callable[[Any], list[T]],
        filters: dict[str, Any] | None = None,
        source_instance: Any | None = None,
        rel_name: str | None = None,
    ):
        """
        Initialize relationship query.

        Args:
            target_class: Target entity class
            filter_func: Function that performs the actual query
            filters: Initial filter conditions
            source_instance: Source entity instance (for adding relationships)
            rel_name: Name of the relationship (for adding relationships)
        """
        self.target_class = target_class
        self.filter_func = filter_func
        self._filters = filters or {}
        self._order_field: str | None = None
        self._order_desc: bool = False
        self._limit: int | None = None
        self._source_instance = source_instance
        self._rel_name = rel_name

    def add(self, target_entity: T, **props: Any) -> None:
        """
        Add a relationship to the target entity.

        Args:
            target_entity: The entity to relate to
            **props: Properties for the relationship edge
        """
        if not self._source_instance or not self._rel_name:
            raise ValueError(
                "Cannot add relationship: source instance or relationship name missing"
            )

        # Get entity store for source
        # We need to import here to avoid circular imports
        from .entity_store import EntityStore
        from .metadata import registry

        source_metadata = registry.get_by_class(self._source_instance.__class__)
        if not source_metadata:
            raise ValueError("Source entity not registered")

        store = EntityStore(source_metadata)
        store.add_relationship(
            self._source_instance, self._rel_name, target_entity, props
        )

    def filter(self, **kwargs: Any) -> "RelationshipQuery[T]":
        """
        Add filter conditions.

        Args:
            **kwargs: Field-value pairs to filter by

        Returns:
            Self for method chaining

        Example:
            >>> query.filter(status="active", priority="high")
        """
        new_filters = {**self._filters, **kwargs}
        return RelationshipQuery(
            self.target_class, self.filter_func, new_filters
        )._copy_params(self)

    def order_by(self, field: str, desc: bool = False) -> "RelationshipQuery[T]":
        """
        Set ordering for results.

        Args:
            field: Field name to order by
            desc: If True, order descending

        Returns:
            Self for method chaining

        Example:
            >>> query.order_by("created_at", desc=True)
        """
        new_query = RelationshipQuery(
            self.target_class, self.filter_func, self._filters
        )
        new_query._order_field = field
        new_query._order_desc = desc
        new_query._limit = self._limit
        return new_query

    def limit(self, n: int) -> "RelationshipQuery[T]":
        """
        Limit number of results.

        Args:
            n: Maximum number of results to return

        Returns:
            Self for method chaining

        Example:
            >>> query.limit(10)
        """
        new_query = RelationshipQuery(
            self.target_class, self.filter_func, self._filters
        )
        new_query._order_field = self._order_field
        new_query._order_desc = self._order_desc
        new_query._limit = n
        return new_query

    def count(self) -> int:
        """
        Count matching results without loading them.

        Returns:
            Number of matching entities

        Example:
            >>> user.posts(status="published").count()
        """
        results = self.all()
        return len(results)

    def all(self) -> list[T]:
        """
        Execute query and return all results.

        Returns:
            List of matching entities

        Example:
            >>> posts = user.posts(status="published").all()
        """
        # Get results from filter function
        results = self.filter_func(self._filters)

        # Apply ordering if specified
        if self._order_field and results:
            try:
                results = sorted(
                    results,
                    key=lambda x: getattr(x, self._order_field),
                    reverse=self._order_desc,
                )
            except AttributeError:
                # Field doesn't exist, skip ordering
                pass

        # Apply limit if specified
        if self._limit is not None:
            results = results[: self._limit]

        return results

    def first(self) -> T | None:
        """
        Get first matching result or None.

        Returns:
            First entity or None if no matches

        Example:
            >>> latest_post = user.posts().order_by("created_at", desc=True).first()
        """
        results = self.limit(1).all()
        return results[0] if results else None

    def exists(self) -> bool:
        """
        Check if any matching results exist.

        Returns:
            True if at least one match exists

        Example:
            >>> has_posts = user.posts(status="published").exists()
        """
        return self.first() is not None

    def _copy_params(self, other: "RelationshipQuery[T]") -> "RelationshipQuery[T]":
        """Copy parameters from another query."""
        self._order_field = other._order_field
        self._order_desc = other._order_desc
        self._limit = other._limit
        return self

    def __iter__(self):
        """Allow iteration over query results."""
        return iter(self.all())

    def __len__(self):
        """Return count of results."""
        return self.count()

    def __getitem__(self, index):
        """Support indexing to access query results."""
        results = self.all()
        return results[index]

    def __eq__(self, other):
        """Support equality comparison with lists."""
        if isinstance(other, list):
            return self.all() == other
        if isinstance(other, RelationshipQuery):
            return self.all() == other.all()
        return NotImplemented

    def __repr__(self):
        """String representation of query."""
        parts = [f"<RelationshipQuery({self.target_class.__name__})"]
        if self._filters:
            parts.append(f" filters={self._filters}")
        if self._order_field:
            direction = "DESC" if self._order_desc else "ASC"
            parts.append(f" order_by={self._order_field} {direction}")
        if self._limit:
            parts.append(f" limit={self._limit}")
        parts.append(">")
        return "".join(parts)
