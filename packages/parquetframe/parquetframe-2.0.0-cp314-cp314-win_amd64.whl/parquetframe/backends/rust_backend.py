"""Rust backend detection and initialization.

This module provides functionality to detect and initialize the Rust backend
for ParquetFrame. It implements graceful fallback to pure Python when Rust
is unavailable.
"""

import os
import warnings

_rust_available: bool | None = None


def is_rust_available() -> bool:
    """Check if Rust backend is available.

    This function attempts to import the Rust extension module and caches
    the result for subsequent calls. It respects the PARQUETFRAME_DISABLE_RUST
    environment variable to allow users to disable Rust globally.

    Returns:
        bool: True if Rust backend is available and not disabled, False otherwise.

    Example:
        >>> from parquetframe.backends.rust_backend import is_rust_available
        >>> if is_rust_available():
        ...     print("Using Rust acceleration")
        ... else:
        ...     print("Using pure Python fallback")
    """
    global _rust_available

    if _rust_available is not None:
        return _rust_available

    # Check environment variable override
    rust_disabled = os.getenv("PARQUETFRAME_DISABLE_RUST", "0") == "1"
    if rust_disabled:
        _rust_available = False
        return False

    # Try importing Rust module
    try:
        from parquetframe._rustic import rust_available

        _rust_available = rust_available()
        return _rust_available
    except ImportError:
        _rust_available = False
        warnings.warn(
            "Rust backend not available. ParquetFrame will use pure Python fallback. "
            "For optimal performance, install Rust and rebuild: pip install maturin && maturin develop --release",
            stacklevel=2,
        )
        return False


def get_rust_backend():
    """Get Rust backend instance or None.

    Returns the Rust backend module if available, otherwise returns None.
    This allows code to conditionally use Rust functionality.

    Returns:
        Module or None: The _rustic module if available, None otherwise.

    Example:
        >>> rust = get_rust_backend()
        >>> if rust:
        ...     version = rust.rust_version()
        ...     print(f"Rust backend version: {version}")
    """
    if not is_rust_available():
        return None

    try:
        from parquetframe import _rustic

        return _rustic
    except ImportError:
        return None


def get_rust_version() -> str | None:
    """Get the version of the Rust backend.

    Returns:
        Optional[str]: Version string if Rust is available, None otherwise.
    """
    rust = get_rust_backend()
    if rust is None:
        return None

    try:
        return rust.rust_version()
    except AttributeError:
        return None
