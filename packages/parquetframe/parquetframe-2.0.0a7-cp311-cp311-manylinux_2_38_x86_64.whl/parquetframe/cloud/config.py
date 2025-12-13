"""
Cloud configuration and credential management.

Supports multiple providers:
- AWS S3 (and compatible)
- Google Cloud Storage (GCS)
- Azure Blob Storage (ABS)
"""

import os
from dataclasses import dataclass
from typing import Any, Protocol


class CloudConfig(Protocol):
    """Protocol for cloud configurations."""

    def to_storage_options(self) -> dict[str, Any]:
        """Convert to fsspec storage options."""
        ...


@dataclass
class S3Config:
    """
    S3 connection configuration.

    Supports standard AWS authentication patterns plus
    S3-compatible stores (MinIO, etc.).
    """

    access_key_id: str | None = None
    secret_access_key: str | None = None
    session_token: str | None = None
    region: str = "us-east-1"
    profile_name: str | None = None
    endpoint_url: str | None = None  # For S3-compatible stores

    @classmethod
    def from_env(cls) -> "S3Config":
        """Load from standard AWS environment variables."""
        return cls(
            access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            session_token=os.getenv("AWS_SESSION_TOKEN"),
            region=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
            endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
        )

    @classmethod
    def from_profile(cls, profile_name: str) -> "S3Config":
        """Load from AWS profile."""
        try:
            import boto3
        except ImportError:
            raise ImportError(
                "boto3 required for AWS profiles. Install with: pip install boto3"
            ) from None

        session = boto3.Session(profile_name=profile_name)
        credentials = session.get_credentials()

        if credentials is None:
            raise ValueError(f"No credentials found for profile: {profile_name}")

        return cls(
            access_key_id=credentials.access_key,
            secret_access_key=credentials.secret_key,
            session_token=credentials.token,
            region=session.region_name or "us-east-1",
            profile_name=profile_name,
        )

    def to_storage_options(self) -> dict:
        """Convert to fsspec/s3fs storage_options format."""
        options = {}

        if self.access_key_id:
            options["key"] = self.access_key_id
        if self.secret_access_key:
            options["secret"] = self.secret_access_key
        if self.session_token:
            options["token"] = self.session_token
        if self.endpoint_url:
            options["client_kwargs"] = {"endpoint_url": self.endpoint_url}

        return options


@dataclass
class GCSConfig:
    """
    Google Cloud Storage configuration.

    Uses gcsfs.
    """

    project: str | None = None
    token: str | None = None  # Path to JSON key, or 'google_default', 'cache', 'cloud'

    @classmethod
    def from_env(cls) -> "GCSConfig":
        """Load from GCP environment variables."""
        return cls(
            project=os.getenv("GCP_PROJECT") or os.getenv("GOOGLE_CLOUD_PROJECT"),
            token=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        )

    def to_storage_options(self) -> dict:
        """Convert to gcsfs storage options."""
        options = {}
        if self.project:
            options["project"] = self.project
        if self.token:
            options["token"] = self.token
        return options


@dataclass
class AzureConfig:
    """
    Azure Blob Storage configuration.

    Uses adlfs.
    """

    account_name: str | None = None
    account_key: str | None = None
    sas_token: str | None = None
    connection_string: str | None = None

    @classmethod
    def from_env(cls) -> "AzureConfig":
        """Load from Azure environment variables."""
        return cls(
            account_name=os.getenv("AZURE_STORAGE_ACCOUNT_NAME"),
            account_key=os.getenv("AZURE_STORAGE_ACCOUNT_KEY"),
            sas_token=os.getenv("AZURE_STORAGE_SAS_TOKEN"),
            connection_string=os.getenv("AZURE_STORAGE_CONNECTION_STRING"),
        )

    def to_storage_options(self) -> dict:
        """Convert to adlfs storage options."""
        options = {}
        if self.connection_string:
            options["connection_string"] = self.connection_string
        else:
            if self.account_name:
                options["account_name"] = self.account_name
            if self.account_key:
                options["account_key"] = self.account_key
            if self.sas_token:
                options["sas_token"] = self.sas_token
        return options


__all__ = ["CloudConfig", "S3Config", "GCSConfig", "AzureConfig"]
