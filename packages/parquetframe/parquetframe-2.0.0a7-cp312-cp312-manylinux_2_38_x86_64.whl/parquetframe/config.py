"""
Configuration system for ParquetFrame.

Provides global configuration management with environment variable support.
"""

import os
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

EngineType = Literal["pandas", "polars", "dask"]
FormatType = Literal["parquet", "avro", "csv"]


@dataclass
class Config:
    """Global configuration for ParquetFrame."""

    # Engine selection
    default_engine: EngineType | None = None
    pandas_threshold_mb: float = 100.0
    polars_threshold_mb: float = 10_000.0

    # Entity framework
    default_entity_format: FormatType = "parquet"
    default_entity_base_path: Path | None = None

    # I/O settings
    default_compression: str | None = None
    chunk_size: int = 10_000

    # UX settings
    verbose: bool = False
    show_warnings: bool = True
    progress_bar: bool = False

    # Performance
    parallel_read: bool = True
    max_workers: int | None = None

    # Rust backend
    use_rust_backend: bool = True  # Enable Rust acceleration by default
    rust_io_enabled: bool = True  # Use Rust for I/O operations
    rust_graph_enabled: bool = True  # Use Rust for graph algorithms

    _instance: "Config | None" = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """Load configuration from environment variables."""
        self._load_from_env()

    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        # Engine settings
        if env_engine := os.getenv("PARQUETFRAME_ENGINE"):
            if env_engine in ("pandas", "polars", "dask"):
                self.default_engine = env_engine  # type: ignore

        if env_pandas_threshold := os.getenv("PARQUETFRAME_PANDAS_THRESHOLD_MB"):
            try:
                self.pandas_threshold_mb = float(env_pandas_threshold)
            except ValueError:
                pass

        if env_polars_threshold := os.getenv("PARQUETFRAME_POLARS_THRESHOLD_MB"):
            try:
                self.polars_threshold_mb = float(env_polars_threshold)
            except ValueError:
                pass

        # Entity settings
        if env_format := os.getenv("PARQUETFRAME_ENTITY_FORMAT"):
            if env_format in ("parquet", "avro", "csv"):
                self.default_entity_format = env_format  # type: ignore

        if env_base_path := os.getenv("PARQUETFRAME_ENTITY_BASE_PATH"):
            self.default_entity_base_path = Path(env_base_path)

        # UX settings
        if os.getenv("PARQUETFRAME_VERBOSE", "").lower() in ("1", "true", "yes"):
            self.verbose = True

        if os.getenv("PARQUETFRAME_QUIET", "").lower() in ("1", "true", "yes"):
            self.show_warnings = False

        if os.getenv("PARQUETFRAME_PROGRESS", "").lower() in ("1", "true", "yes"):
            self.progress_bar = True

        # Rust backend settings
        if os.getenv("PARQUETFRAME_DISABLE_RUST", "").lower() in ("1", "true", "yes"):
            self.use_rust_backend = False
            self.rust_io_enabled = False
            self.rust_graph_enabled = False

        if os.getenv("PARQUETFRAME_DISABLE_RUST_IO", "").lower() in (
            "1",
            "true",
            "yes",
        ):
            self.rust_io_enabled = False

        if os.getenv("PARQUETFRAME_DISABLE_RUST_GRAPH", "").lower() in (
            "1",
            "true",
            "yes",
        ):
            self.rust_graph_enabled = False

    def set(self, **kwargs: Any) -> None:
        """
        Set configuration values.

        Args:
            **kwargs: Configuration key-value pairs
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Unknown configuration key: {key}")

    def reset(self) -> None:
        """Reset configuration to defaults."""
        self.__init__()  # type: ignore

    def to_dict(self) -> dict[str, Any]:
        """
        Export configuration as dictionary.

        Returns:
            Dictionary of configuration values
        """
        return {
            "default_engine": self.default_engine,
            "pandas_threshold_mb": self.pandas_threshold_mb,
            "polars_threshold_mb": self.polars_threshold_mb,
            "default_entity_format": self.default_entity_format,
            "default_entity_base_path": (
                str(self.default_entity_base_path)
                if self.default_entity_base_path
                else None
            ),
            "default_compression": self.default_compression,
            "chunk_size": self.chunk_size,
            "verbose": self.verbose,
            "show_warnings": self.show_warnings,
            "progress_bar": self.progress_bar,
            "parallel_read": self.parallel_read,
            "max_workers": self.max_workers,
            "use_rust_backend": self.use_rust_backend,
            "rust_io_enabled": self.rust_io_enabled,
            "rust_graph_enabled": self.rust_graph_enabled,
        }

    @classmethod
    def from_dict(cls, config_dict: dict[str, Any]) -> "Config":
        """
        Create configuration from dictionary.

        Args:
            config_dict: Dictionary of configuration values

        Returns:
            Config instance
        """
        # Filter valid keys
        valid_keys = {
            "default_engine",
            "pandas_threshold_mb",
            "polars_threshold_mb",
            "default_entity_format",
            "default_entity_base_path",
            "default_compression",
            "chunk_size",
            "verbose",
            "show_warnings",
            "progress_bar",
            "parallel_read",
            "max_workers",
            "use_rust_backend",
            "rust_io_enabled",
            "rust_graph_enabled",
        }

        filtered = {k: v for k, v in config_dict.items() if k in valid_keys}

        # Convert string path to Path
        if (
            "default_entity_base_path" in filtered
            and filtered["default_entity_base_path"]
        ):
            filtered["default_entity_base_path"] = Path(
                filtered["default_entity_base_path"]
            )

        return cls(**filtered)


# Global configuration instance
_config: Config | None = None


def get_config() -> Config:
    """
    Get the global configuration instance.

    Returns:
        Global Config instance
    """
    global _config
    if _config is None:
        _config = Config()
    return _config


def set_config(**kwargs: Any) -> None:
    """
    Set global configuration values.

    Args:
        **kwargs: Configuration key-value pairs

    Example:
        >>> set_config(default_engine="polars", verbose=True)
    """
    config = get_config()
    config.set(**kwargs)


def reset_config() -> None:
    """Reset global configuration to defaults."""
    global _config
    _config = Config()


@contextmanager
def config_context(**kwargs: Any):
    """
    Temporarily modify configuration within a context.

    Args:
        **kwargs: Configuration key-value pairs

    Example:
        >>> with config_context(default_engine="dask"):
        ...     df = read("large_file.parquet")  # Uses Dask
    """
    config = get_config()
    old_values = {k: getattr(config, k) for k in kwargs}

    try:
        config.set(**kwargs)
        yield config
    finally:
        config.set(**old_values)
