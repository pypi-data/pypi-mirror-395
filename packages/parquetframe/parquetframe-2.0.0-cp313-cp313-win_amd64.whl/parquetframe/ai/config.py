"""
AI Configuration for RAG system.
"""

from dataclasses import dataclass, field

from .models import BaseLanguageModel

DEFAULT_SYSTEM_PROMPT = """You are a helpful assistant with access to a database.
Answer the user's query based ONLY on the context provided below.
If the context does not contain the answer, state that you cannot answer based on the available information.
Do not make up information. Be concise and accurate.

Context:
---
{context_str}
---
"""

DEFAULT_INTENT_PROMPT = """Extract key information from the user's query.
Identify:
1. Entity names they're asking about
2. Any filters or conditions
3. Query type (app_data or permission_data)

Available entities: {entity_names}

User Query: "{query}"

Respond with a JSON object.
"""


@dataclass
class AIConfig:
    """Configuration for AI/RAG features."""

    # Model configuration
    models: list[BaseLanguageModel] = field(default_factory=list)
    default_generation_model: str | None = None
    default_intent_model: str | None = None

    # RAG configuration
    rag_enabled_entities: set[str] = field(default_factory=set)

    # Prompt templates (defaults)
    system_prompt_template: str = DEFAULT_SYSTEM_PROMPT
    intent_prompt_template: str = DEFAULT_INTENT_PROMPT

    # Enhanced prompt options
    use_enhanced_prompts: bool = False
    prompt_style: str = (
        "default"  # Options: default, analytical, conversational, code_gen
    )
    enable_multi_turn: bool = False
    conversation_history: list[dict] = field(default_factory=list)

    # Retrieval parameters
    retrieval_k: int = 5  # Target number of context items

    # Response configuration
    enable_response_citation: bool = True  # Include source references
    max_citation_count: int = 3  # Maximum sources to cite

    def __post_init__(self):
        """Initialize defaults."""
        if not self.default_generation_model and self.models:
            self.default_generation_model = self.models[0].model_name

        if not self.default_intent_model:
            self.default_intent_model = self.default_generation_model

        if not self.default_generation_model and not self.models:
            # Allow empty config for tests that might mock things later?
            # Or should we enforce at least one model if passed?
            # The failing test passed no args: AIConfig()
            # So we should be lenient here.
            pass
        elif self.default_generation_model:
            # Validate models exist if we have models
            if self.models:
                self.get_model(self.default_generation_model)
            if self.default_intent_model and self.models:
                self.get_model(self.default_intent_model)

    def get_model(self, model_name: str | None = None) -> BaseLanguageModel:
        """
        Get model by name.

        Args:
            model_name: Model name, or None for default generation model

        Returns:
            BaseLanguageModel instance

        Raises:
            ValueError: If model not found
        """
        target_name = model_name or self.default_generation_model

        for model in self.models:
            if model.model_name == target_name:
                return model

        raise ValueError(
            f"Model '{target_name}' not registered in AIConfig. "
            f"Available models: {[m.model_name for m in self.models]}"
        )

    def get_intent_model(self) -> BaseLanguageModel:
        """Get the model used for intent parsing."""
        return self.get_model(self.default_intent_model)

    def get_prompt_template(self, context_str: str, **kwargs) -> str:
        """
        Get appropriate prompt template based on configuration.

        Args:
            context_str: The context string to inject
            **kwargs: Additional template variables

        Returns:
            Formatted prompt string
        """
        if self.use_enhanced_prompts:
            from .enhanced_prompts import (
                ANALYTICAL_RAG_PROMPT,
                CODE_GEN_RAG_PROMPT,
                ENHANCED_RAG_SYSTEM_PROMPT,
                MULTI_TURN_RAG_PROMPT,
                PERMISSION_AWARE_PROMPT,
            )

            if self.prompt_style == "analytical":
                template = ANALYTICAL_RAG_PROMPT
            elif self.prompt_style == "code_gen":
                template = CODE_GEN_RAG_PROMPT
            elif self.prompt_style == "conversational" and self.enable_multi_turn:
                template = MULTI_TURN_RAG_PROMPT
                kwargs["conversation_history"] = self._format_history()
                kwargs["current_question"] = kwargs.get("query", "")
            elif self.prompt_style == "permission_aware":
                template = PERMISSION_AWARE_PROMPT
            else:
                template = ENHANCED_RAG_SYSTEM_PROMPT
        else:
            template = self.system_prompt_template

        return template.format(context_str=context_str, **kwargs)

    def _format_history(self) -> str:
        """Format conversation history for multi-turn prompts."""
        if not self.conversation_history:
            return "No previous conversation."

        history_lines = []
        for turn in self.conversation_history[-5:]:  # Last 5 turns
            history_lines.append(f"User: {turn.get('user', '')}")
            history_lines.append(f"Assistant: {turn.get('assistant', '')}")

        return "\n".join(history_lines)

    def add_to_history(self, user_message: str, assistant_response: str):
        """Add a turn to conversation history."""
        self.conversation_history.append(
            {"user": user_message, "assistant": assistant_response}
        )
        # Keep only last 10 turns
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]


__all__ = ["AIConfig", "DEFAULT_SYSTEM_PROMPT", "DEFAULT_INTENT_PROMPT"]
