"""
Cloud handler factory.
"""

from urllib.parse import urlparse

from .config import AzureConfig, GCSConfig, S3Config
from .handlers.azure import AzureHandler
from .handlers.base import CloudHandler
from .handlers.gcp import GCSHandler
from .handlers.s3 import S3Handler


class CloudFactory:
    """Factory for creating cloud handlers."""

    @staticmethod
    def get_handler(uri: str) -> CloudHandler:
        """
        Get appropriate handler for the given URI.

        Args:
            uri: Cloud URI (s3://, gs://, az://, abfs://)

        Returns:
            CloudHandler instance
        """
        parsed = urlparse(uri)
        scheme = parsed.scheme.lower()

        if scheme == "s3":
            return S3Handler()
        elif scheme == "gs":
            return GCSHandler()
        elif scheme in ("az", "abfs", "abfss"):
            return AzureHandler()
        else:
            raise ValueError(f"Unsupported cloud scheme: {scheme}")

    @staticmethod
    def get_s3_handler(config: S3Config | None = None) -> S3Handler:
        """Get S3 handler with optional config."""
        return S3Handler(config)

    @staticmethod
    def get_gcs_handler(config: GCSConfig | None = None) -> GCSHandler:
        """Get GCS handler with optional config."""
        return GCSHandler(config)

    @staticmethod
    def get_azure_handler(config: AzureConfig | None = None) -> AzureHandler:
        """Get Azure handler with optional config."""
        return AzureHandler(config)
