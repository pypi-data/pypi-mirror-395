"""
Knowlogy: Computable Knowledge Graph.

Provides semantic grounding and symbolic reasoning capabilities.
"""

from .core import KnowlogyEngine
from .library import list_libraries, load_library
from .storage import Application, Concept, Formula

# Global instance
_engine = KnowlogyEngine()


def search(query: str):
    """Search for concepts."""
    return _engine.search_concepts(query)


def get_formula(concept_name: str):
    """Get formula for a concept."""
    return _engine.get_formula(concept_name)


def get_context(query: str) -> str:
    """Get RAG context."""
    return _engine.get_context_for_rag(query)


__all__ = [
    "KnowlogyEngine",
    "Concept",
    "Formula",
    "Application",
    "search",
    "get_formula",
    "get_context",
    "load_library",
    "list_libraries",
]
