"""
AI module for Retrieval-Augmented Generation (RAG).

Provides permission-aware querying over EntityStore using LLMs.
"""

# Keep existing LLM agent for backwards compatibility
from .agent import LLMAgent, LLMError, QueryResult
from .config import AIConfig

# Embedding models
from .embeddings import (
    OLLAMA_EMBEDDING_AVAILABLE,
    SENTENCE_TRANSFORMERS_AVAILABLE,
    BaseEmbeddingModel,
    OllamaEmbeddingModel,
    SentenceTransformerModel,
    TetnusEmbeddingModel,
)

# Language models
from .models import OLLAMA_AVAILABLE, BaseLanguageModel, OllamaModel

# RAG pipelines
from .rag_pipeline import SimpleRagPipeline, VectorRagPipeline

# Vector store
from .vector_store import SQLiteVectorStore

__all__ = [
    # Language models
    "BaseLanguageModel",
    "OllamaModel",
    "OLLAMA_AVAILABLE",
    # Embedding models
    "BaseEmbeddingModel",
    "TetnusEmbeddingModel",
    "SentenceTransformerModel",
    "OllamaEmbeddingModel",
    "SENTENCE_TRANSFORMERS_AVAILABLE",
    "OLLAMA_EMBEDDING_AVAILABLE",
    # Config
    "AIConfig",
    # RAG pipelines
    "SimpleRagPipeline",
    "VectorRagPipeline",
    # Vector store
    "SQLiteVectorStore",
    # Legacy exports
    "LLMAgent",
    "LLMError",
    "QueryResult",
]
