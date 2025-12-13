"""
Embedding models for RAG system.

Provides abstractions for various embedding backends including
tetnus-llm embeddings, sentence-transformers, and Ollama.
"""

import logging
from abc import ABC, abstractmethod

import numpy as np

logger = logging.getLogger(__name__)


class BaseEmbeddingModel(ABC):
    """Abstract base class for embedding models."""

    @abstractmethod
    def embed(self, text: str) -> np.ndarray:
        """
        Embed a single text string.

        Args:
            text: Text to embed

        Returns:
            Embedding vector as numpy array
        """
        pass

    @abstractmethod
    def embed_batch(self, texts: list[str]) -> np.ndarray:
        """
        Embed a batch of text strings.

        Args:
            texts: List of texts to embed

        Returns:
            2D numpy array of embeddings (batch_size x embedding_dim)
        """
        pass

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Return the embedding dimension."""
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the model name/identifier."""
        pass


class TetnusEmbeddingModel(BaseEmbeddingModel):
    """
    Embedding model using tetnus-llm Embedding layer.

    This leverages the existing tetnus neural network infrastructure
    for generating embeddings. Useful for keeping everything in the
    tetnus ecosystem.
    """

    def __init__(
        self, embedding_dim: int = 384, vocab_size: int = 30000, use_bpe: bool = True
    ):
        """
        Initialize tetnus embedding model.

        Args:
            embedding_dim: Dimension of embedding vectors
            vocab_size: Size of vocabulary for tokenization
            use_bpe: Whether to use BPE tokenizer (recommended) vs character-level
        """
        try:
            from parquetframe._rustic.tetnus import Embedding
        except ImportError as e:
            raise ImportError(
                "tetnus module not available. Ensure pf-py is built with tetnus support."
            ) from e

        self.embedding_layer = Embedding(
            num_embeddings=vocab_size, embedding_dim=embedding_dim
        )
        self._dim = embedding_dim
        self._vocab_size = vocab_size
        self._use_bpe = use_bpe

        if use_bpe:
            # Use BPE tokenizer for better quality
            from .tokenizer import BPETokenizer

            self.tokenizer = BPETokenizer(vocab_size=vocab_size)
            logger.info("Using BPE tokenizer for embeddings")
        else:
            # Fall back to simple character-level tokenizer
            self.char_to_idx = {chr(i): i for i in range(256)}
            self.tokenizer = None

    def _tokenize(self, text: str, max_length: int = 512) -> np.ndarray:
        """
        Tokenize text using BPE or character-level.

        Args:
            text: Text to tokenize
            max_length: Maximum sequence length

        Returns:
            Array of token indices
        """
        if self._use_bpe and self.tokenizer is not None:
            # BPE tokenization
            tokens = self.tokenizer.encode(text, add_special_tokens=False)
            # Truncate or pad
            if len(tokens) > max_length:
                tokens = tokens[:max_length]
            else:
                tokens.extend(
                    [self.tokenizer.vocab[self.tokenizer.pad_token]]
                    * (max_length - len(tokens))
                )
            return np.array(tokens, dtype=np.int32) % self._vocab_size
        else:
            # Character-level tokenization (legacy)
            text = text.lower()[:max_length]
            tokens = [self.char_to_idx.get(c, 0) % self._vocab_size for c in text]
            if len(tokens) < max_length:
                tokens.extend([0] * (max_length - len(tokens)))
            return np.array(tokens, dtype=np.int32)

    def embed(self, text: str) -> np.ndarray:
        """
        Embed single text using tetnus embedding layer.

        The embedding is computed by:
        1. Tokenizing the text
        2. Passing through embedding layer
        3. Mean pooling over sequence dimension

        Args:
            text: Text to embed

        Returns:
            Embedding vector (dimension: embedding_dim)
        """
        tokens = self._tokenize(text)

        # Forward through embedding layer
        # Shape: (seq_len, embedding_dim)
        embeddings = self.embedding_layer.forward(tokens)

        # Mean pool over sequence dimension
        # Shape: (embedding_dim,)
        pooled = np.mean(embeddings, axis=0)

        # L2 normalize
        norm = np.linalg.norm(pooled)
        if norm > 0:
            pooled = pooled / norm

        return pooled

    def embed_batch(self, texts: list[str]) -> np.ndarray:
        """
        Embed batch of texts.

        Args:
            texts: List of texts

        Returns:
            2D array of embeddings (batch_size x embedding_dim)
        """
        return np.array([self.embed(text) for text in texts])

    @property
    def dimension(self) -> int:
        """Return embedding dimension."""
        return self._dim

    @property
    def model_name(self) -> str:
        """Return model identifier."""
        return f"tetnus-embedding-{self._dim}d"


# Optional: Sentence Transformers support
try:
    from sentence_transformers import SentenceTransformer

    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False


class SentenceTransformerModel(BaseEmbeddingModel):
    """
    Embedding model using sentence-transformers library.

    This provides access to high-quality pre-trained models
    like all-MiniLM-L6-v2, which are excellent for semantic search.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize sentence transformer model.

        Args:
            model_name: HuggingFace model name
        """
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise ImportError(
                "sentence-transformers not installed. "
                "Install with: pip install sentence-transformers"
            )

        self.model = SentenceTransformer(model_name)
        self._model_name = model_name
        self._dim = self.model.get_sentence_embedding_dimension()

    def embed(self, text: str) -> np.ndarray:
        """Embed single text."""
        return self.model.encode(text, normalize_embeddings=True)

    def embed_batch(self, texts: list[str]) -> np.ndarray:
        """Embed batch of texts."""
        return self.model.encode(texts, normalize_embeddings=True)

    @property
    def dimension(self) -> int:
        """Return embedding dimension."""
        return self._dim

    @property
    def model_name(self) -> str:
        """Return model name."""
        return self._model_name


# Optional: Ollama embeddings support
try:
    import ollama

    OLLAMA_EMBEDDING_AVAILABLE = True
except ImportError:
    OLLAMA_EMBEDDING_AVAILABLE = False


class OllamaEmbeddingModel(BaseEmbeddingModel):
    """
    Embedding model using Ollama's embedding endpoints.

    Supports models like nomic-embed-text or mxbai-embed-large.
    """

    def __init__(self, model_name: str = "nomic-embed-text", host: str | None = None):
        """
        Initialize Ollama embedding model.

        Args:
            model_name: Ollama embedding model name
            host: Optional Ollama host URL
        """
        if not OLLAMA_EMBEDDING_AVAILABLE:
            raise ImportError(
                "ollama package not installed. Install with: pip install ollama"
            )

        self._model_name = model_name
        self.client_args = {}
        if host:
            self.client_args["host"] = host

        # Get embedding dimension by embedding test text
        test_embed = self._embed_single("test")
        self._dim = len(test_embed)

    def _embed_single(self, text: str) -> np.ndarray:
        """Internal method to embed single text."""
        try:
            response = ollama.embeddings(
                model=self._model_name, prompt=text, **self.client_args
            )
            return np.array(response["embedding"], dtype=np.float32)
        except Exception as e:
            raise RuntimeError(
                f"Ollama embedding error for model {self._model_name}: {e}"
            ) from e

    def embed(self, text: str) -> np.ndarray:
        """Embed single text."""
        embedding = self._embed_single(text)
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        return embedding

    def embed_batch(self, texts: list[str]) -> np.ndarray:
        """Embed batch of texts."""
        # Ollama doesn't have native batching, so we iterate
        return np.array([self.embed(text) for text in texts])

    @property
    def dimension(self) -> int:
        """Return embedding dimension."""
        return self._dim

    @property
    def model_name(self) -> str:
        """Return model name."""
        return self._model_name


__all__ = [
    "BaseEmbeddingModel",
    "TetnusEmbeddingModel",
    "SentenceTransformerModel",
    "OllamaEmbeddingModel",
    "SENTENCE_TRANSFORMERS_AVAILABLE",
    "OLLAMA_EMBEDDING_AVAILABLE",
]
