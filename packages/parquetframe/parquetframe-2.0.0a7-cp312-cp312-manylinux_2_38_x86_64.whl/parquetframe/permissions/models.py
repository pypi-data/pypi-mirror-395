"""
Standard permission models and utilities for common Zanzibar patterns.

This module provides pre-defined permission models for common use cases:
- Document/Folder permissions (Google Drive-style)
- Organization/Team permissions (GitHub-style)
- Resource/Role permissions (Cloud IAM-style)

These models define common relation hierarchies and inheritance patterns.
"""

from __future__ import annotations

from dataclasses import dataclass

from .core import RelationTuple, TupleStore


@dataclass
class PermissionModel:
    """
    A permission model defines a set of relations and their inheritance rules.

    Attributes:
        name: Human-readable name of the model
        description: Description of the model's use case
        relations: Dictionary mapping relation names to their descriptions
        inheritance: Dictionary mapping child relations to parent relations
        namespaces: Set of valid object/subject namespaces for this model
    """

    name: str
    description: str
    relations: dict[str, str]
    inheritance: dict[str, list[str]]  # child -> [parent1, parent2]
    namespaces: dict[str, str]

    def get_inherited_relations(self, relation: str) -> list[str]:
        """
        Get all relations that inherit from the given relation.

        Args:
            relation: The base relation

        Returns:
            List of relations that inherit from the base relation
        """
        inherited = []
        for child, parents in self.inheritance.items():
            if relation in parents:
                inherited.append(child)
        return inherited

    def get_parent_relations(self, relation: str) -> list[str]:
        """
        Get all relations that the given relation inherits from.

        Args:
            relation: The child relation

        Returns:
            List of parent relations
        """
        return self.inheritance.get(relation, [])

    def validate_tuple(self, tuple_obj: RelationTuple) -> bool:
        """
        Validate that a relation tuple is valid for this model.

        Args:
            tuple_obj: RelationTuple to validate

        Returns:
            True if valid, False otherwise
        """
        # Check if relation exists
        if tuple_obj.relation not in self.relations:
            return False

        # Check if namespaces are valid (if defined)
        if self.namespaces:
            if tuple_obj.namespace not in self.namespaces:
                return False
            if tuple_obj.subject_namespace not in self.namespaces:
                return False

        return True

    def expand_inherited_tuples(
        self, tuples: list[RelationTuple]
    ) -> list[RelationTuple]:
        """
        Expand a list of tuples to include inherited relations.

        For example, if "owner" inherits from "editor" and "viewer",
        an owner tuple will generate additional editor and viewer tuples.

        Args:
            tuples: List of base relation tuples

        Returns:
            Expanded list including inherited relation tuples
        """
        expanded = list(tuples)  # Start with original tuples

        for tuple_obj in tuples:
            # Find all relations that this relation inherits from
            parent_relations = self.get_parent_relations(tuple_obj.relation)

            # Create tuples for each parent relation
            for parent_relation in parent_relations:
                inherited_tuple = RelationTuple(
                    namespace=tuple_obj.namespace,
                    object_id=tuple_obj.object_id,
                    relation=parent_relation,
                    subject_namespace=tuple_obj.subject_namespace,
                    subject_id=tuple_obj.subject_id,
                )
                expanded.append(inherited_tuple)

        return expanded


class StandardModels:
    """Collection of standard permission models for common use cases."""

    @staticmethod
    def google_drive() -> PermissionModel:
        """
        Google Drive-style document and folder permissions.

        Relations:
            - owner: Can do everything (delete, share, edit, comment, view)
            - editor: Can edit, comment, and view
            - commenter: Can comment and view
            - viewer: Can view only

        Namespaces:
            - doc: Documents
            - folder: Folders
            - user: Users
            - group: Groups
        """
        return PermissionModel(
            name="Google Drive",
            description="Document and folder permissions similar to Google Drive",
            relations={
                "owner": "Full control including delete and share permissions",
                "editor": "Can edit content, add comments, and view",
                "commenter": "Can add comments and view content",
                "viewer": "Can view content only",
            },
            inheritance={
                "owner": ["editor", "commenter", "viewer"],
                "editor": ["commenter", "viewer"],
                "commenter": ["viewer"],
            },
            namespaces={
                "doc": "Documents and files",
                "folder": "Folders and directories",
                "user": "Individual users",
                "group": "User groups and teams",
            },
        )

    @staticmethod
    def github_org() -> PermissionModel:
        """
        GitHub-style organization and repository permissions.

        Relations:
            - admin: Full administrative access
            - maintain: Maintain repositories (manage settings, not admin)
            - write: Push to repositories
            - triage: Manage issues and pull requests without write access
            - read: Read repositories and clone

        Namespaces:
            - org: Organizations
            - repo: Repositories
            - user: Users
            - team: Teams within organizations
        """
        return PermissionModel(
            name="GitHub Organization",
            description="Organization and repository permissions similar to GitHub",
            relations={
                "admin": "Full administrative access to org/repo",
                "maintain": "Maintain repositories without admin privileges",
                "write": "Push to repositories and manage code",
                "triage": "Manage issues and PRs without write access",
                "read": "Read access to repositories",
            },
            inheritance={
                "admin": ["maintain", "write", "triage", "read"],
                "maintain": ["write", "triage", "read"],
                "write": ["triage", "read"],
                "triage": ["read"],
            },
            namespaces={
                "org": "GitHub organizations",
                "repo": "Git repositories",
                "user": "Individual users",
                "team": "Teams within organizations",
            },
        )

    @staticmethod
    def cloud_iam() -> PermissionModel:
        """
        Cloud IAM-style resource permissions.

        Relations:
            - owner: Full ownership of resources
            - admin: Administrative access without ownership transfer
            - editor: Edit resources and configurations
            - viewer: View resources and configurations
            - user: Basic user access to resources

        Namespaces:
            - project: Cloud projects
            - resource: Cloud resources (VMs, storage, etc.)
            - service: Cloud services
            - user: Individual users
            - service_account: Service accounts
            - group: User groups
        """
        return PermissionModel(
            name="Cloud IAM",
            description="Cloud IAM-style resource and project permissions",
            relations={
                "owner": "Full ownership and billing access",
                "admin": "Administrative access without ownership",
                "editor": "Edit and configure resources",
                "viewer": "View resources and configurations",
                "user": "Basic access to use resources",
            },
            inheritance={
                "owner": ["admin", "editor", "viewer", "user"],
                "admin": ["editor", "viewer", "user"],
                "editor": ["viewer", "user"],
                "viewer": ["user"],
            },
            namespaces={
                "project": "Cloud projects and billing accounts",
                "resource": "Cloud resources (compute, storage, network)",
                "service": "Cloud services and APIs",
                "user": "Individual human users",
                "service_account": "Service accounts for applications",
                "group": "User groups and organizational units",
            },
        )

    @staticmethod
    def simple_rbac() -> PermissionModel:
        """
        Simple role-based access control model.

        Relations:
            - admin: System administrator
            - manager: Resource manager
            - user: Regular user
            - guest: Guest access

        Namespaces:
            - system: System resources
            - app: Applications
            - data: Data resources
            - user: Users
            - role: Roles
        """
        return PermissionModel(
            name="Simple RBAC",
            description="Simple role-based access control for applications",
            relations={
                "admin": "System administrator with full access",
                "manager": "Resource manager with elevated privileges",
                "user": "Regular user with standard access",
                "guest": "Guest with limited read-only access",
            },
            inheritance={
                "admin": ["manager", "user", "guest"],
                "manager": ["user", "guest"],
                "user": ["guest"],
            },
            namespaces={
                "system": "System-level resources and configuration",
                "app": "Applications and services",
                "data": "Data resources and databases",
                "user": "Individual users",
                "role": "Roles and permissions",
            },
        )


def create_model_store(
    model: PermissionModel, expand_inheritance: bool = True
) -> TupleStore:
    """
    Create an empty TupleStore configured for a specific permission model.

    Args:
        model: The permission model to use
        expand_inheritance: Whether to automatically expand inherited relations

    Returns:
        Empty TupleStore ready for the model
    """
    return ModelTupleStore(model, expand_inheritance)


class ModelTupleStore(TupleStore):
    """
    A TupleStore that validates tuples against a permission model.

    This extends the base TupleStore to add:
    - Validation against the model's relations and namespaces
    - Automatic expansion of inherited relations
    - Model-specific query methods
    """

    def __init__(self, model: PermissionModel, expand_inheritance: bool = True):
        """
        Initialize ModelTupleStore with a permission model.

        Args:
            model: The permission model to enforce
            expand_inheritance: Whether to auto-expand inherited relations
        """
        super().__init__()
        self.model = model
        self.expand_inheritance = expand_inheritance

    def add_tuple(self, tuple_obj: RelationTuple) -> TupleStore:
        """Add a tuple with model validation and inheritance expansion."""
        if not self.model.validate_tuple(tuple_obj):
            raise ValueError(
                f"Tuple {tuple_obj} is not valid for model '{self.model.name}'"
            )

        tuples_to_add = [tuple_obj]
        if self.expand_inheritance:
            tuples_to_add = self.model.expand_inherited_tuples([tuple_obj])

        return super().add_tuples(tuples_to_add)

    def add_tuples(self, tuples: list[RelationTuple]) -> TupleStore:
        """Add multiple tuples with model validation and inheritance expansion."""
        for tuple_obj in tuples:
            if not self.model.validate_tuple(tuple_obj):
                raise ValueError(
                    f"Tuple {tuple_obj} is not valid for model '{self.model.name}'"
                )

        tuples_to_add = tuples
        if self.expand_inheritance:
            tuples_to_add = self.model.expand_inherited_tuples(tuples)

        return super().add_tuples(tuples_to_add)

    def get_model_relations(self) -> dict[str, str]:
        """Get the relations defined in the model."""
        return self.model.relations.copy()

    def get_model_namespaces(self) -> dict[str, str]:
        """Get the namespaces defined in the model."""
        return self.model.namespaces.copy()
