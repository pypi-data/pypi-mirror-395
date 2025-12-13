"""
Model abstraction layer for RAG system.

Provides pluggable LLM interface supporting Ollama and other providers.
"""

from abc import ABC, abstractmethod


class BaseLanguageModel(ABC):
    """Abstract base class for language models."""

    def __init__(self, model_name: str, **kwargs):
        """
        Initialize language model.

        Args:
            model_name: Name/identifier of the model
            **kwargs: Provider-specific parameters
        """
        self.model_name = model_name
        self.generation_params = kwargs

    @abstractmethod
    def generate(self, messages: list[dict[str, str]]) -> str:
        """
        Generate response from structured messages.

        Args:
            messages: List of message dicts with 'role' and 'content' keys
                     e.g., [{"role": "user", "content": "Hello"}]

        Returns:
            Generated text response
        """
        pass

    @property
    @abstractmethod
    def provider(self) -> str:
        """Return provider name (e.g., 'ollama', 'openai')."""
        pass


# Ollama implementation
try:
    import ollama

    OLLAMA_AVAILABLE = True
except ImportError:
    ollama = None
    OLLAMA_AVAILABLE = False


class OllamaModel(BaseLanguageModel):
    """Ollama local LLM implementation."""

    def __init__(self, model_name: str, host: str | None = None, **kwargs):
        """
        Initialize Ollama model.

        Args:
            model_name: Ollama model name (e.g., 'llama2', 'mistral')
            host: Optional Ollama server host
            **kwargs: Generation parameters (temperature, top_p, etc.)
        """
        super().__init__(model_name, **kwargs)

        if not OLLAMA_AVAILABLE:
            raise ImportError(
                "Ollama package not installed. Install with: pip install ollama"
            )

        self.client_args = {}
        if host:
            self.client_args["host"] = host

    @property
    def provider(self) -> str:
        return "ollama"

    def generate(self, messages: list[dict[str, str]]) -> str:
        """
        Generate response using Ollama.

        Args:
            messages: Chat messages in OpenAI format

        Returns:
            Generated response text

        Raises:
            RuntimeError: If Ollama API call fails
        """
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=messages,
                options=self.generation_params,
                **self.client_args,
            )
            return response["message"]["content"]
        except Exception as e:
            raise RuntimeError(
                f"Ollama API error for model '{self.model_name}': {e}"
            ) from e


__all__ = ["BaseLanguageModel", "OllamaModel", "OLLAMA_AVAILABLE"]
