"""
Knowlogy library management.

Provides utilities for loading and managing knowledge libraries.
"""

import subprocess
import sys
from pathlib import Path


class LibraryManager:
    """Manages Knowlogy knowledge libraries."""

    AVAILABLE_LIBRARIES = {
        "statistics": "Core statistical concepts and formulas",
        "physics": "Classical physics concepts, laws, and formulas",
        "finance": "Financial analysis concepts, metrics, and valuation formulas",
    }

    @classmethod
    def list_libraries(cls) -> dict:
        """List available knowledge libraries."""
        return cls.AVAILABLE_LIBRARIES

    @classmethod
    def load_library(cls, name: str) -> bool:
        """
        Load a knowledge library.

        Args:
            name: Library name (e.g., "statistics")

        Returns:
            True if successful, False otherwise
        """
        if name not in cls.AVAILABLE_LIBRARIES:
            raise ValueError(
                f"Unknown library: {name}. Available: {list(cls.AVAILABLE_LIBRARIES.keys())}"
            )

        # Find ingestion script
        repo_root = Path(__file__).parent.parent.parent
        script_path = repo_root / "scripts" / "knowlogy" / f"ingest_{name}.py"

        if not script_path.exists():
            raise FileNotFoundError(f"Ingestion script not found: {script_path}")

        # Run ingestion script
        result = subprocess.run(
            [sys.executable, str(script_path)], capture_output=True, text=True
        )

        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print(f"Error loading library: {result.stderr}")
            return False

    @classmethod
    def is_library_loaded(cls, name: str) -> bool:
        """
        Check if a library is already loaded.

        Args:
            name: Library name

        Returns:
            True if loaded, False otherwise
        """
        from parquetframe.knowlogy import search

        # Simple check: try searching for a known concept from the library
        if name == "statistics":
            results = search("mean")
            return len(results) > 0
        elif name == "physics":
            results = search("Newton")
            return len(results) > 0
        elif name == "finance":
            results = search("NPV")
            return len(results) > 0

        return False


def load_library(name: str) -> bool:
    """
    Load a knowledge library.

    Args:
        name: Library name

    Returns:
        True if successful

    Example:
        >>> from parquetframe.knowlogy import load_library
        >>> load_library("statistics")
    """
    return LibraryManager.load_library(name)


def list_libraries() -> dict:
    """
    List available knowledge libraries.

    Returns:
        Dictionary mapping library names to descriptions
    """
    return LibraryManager.list_libraries()


__all__ = ["LibraryManager", "load_library", "list_libraries"]
