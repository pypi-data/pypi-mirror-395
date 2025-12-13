"""
Simple RAG Pipeline for permission-aware querying.

This module provides a simplified RAG implementation that uses
keyword-based intent parsing and EntityStore for retrieval.
"""

import json
import logging
import re
from typing import Any

from .config import AIConfig

logger = logging.getLogger(__name__)


class SimpleRagPipeline:
    """Simplified RAG pipeline using keyword-based retrieval."""

    def __init__(self, config: AIConfig, entity_store: Any, use_knowlogy: bool = False):
        """
        Initialize RAG pipeline.

        Args:
            config: AIConfig with model and prompt configuration
            entity_store: EntityStore instance for data retrieval
            use_knowlogy: Whether to integrate Knowlogy knowledge graph
        """
        self.config = config
        self.entity_store = entity_store
        self.generation_model = config.get_model()
        self.use_knowlogy = use_knowlogy

        if use_knowlogy:
            from .knowlogy_retriever import KnowlogyRetriever

            self.knowlogy_retriever = KnowlogyRetriever()
        else:
            self.knowlogy_retriever = None

    def run_query(self, query: str, user_context: str) -> dict[str, Any]:
        """
        Run end-to-end RAG query.

        Args:
            query: Natural language query
            user_context: User ID for permission checks (e.g., "user:alice")

        Returns:
            Dict with response_text, context_used, and metadata
        """
        logger.info(f"Running RAG query for user: {user_context}")

        try:
            # Step 1: Parse intent (simplified keyword extraction)
            intent = self._parse_intent(query)
            logger.debug(f"Parsed intent: {intent}")

            # Step 2: Retrieve authorized context
            context_chunks = self._retrieve_authorized_context(intent, user_context)

            # Step 2b: Add Knowlogy knowledge if enabled
            if self.use_knowlogy and self.knowlogy_retriever:
                knowledge_docs = self.knowlogy_retriever.retrieve(query, top_k=3)
                # Add knowledge to context
                for doc in knowledge_docs:
                    context_chunks.append(
                        {
                            "content": doc.content,
                            "metadata": doc.metadata,
                            "source": "knowlogy",
                        }
                    )

            logger.debug(f"Retrieved {len(context_chunks)} context chunks")

            # Step 3: Augment and generate
            response_text = self._generate_response(query, context_chunks)

            return {
                "response_text": response_text,
                "context_used": context_chunks,
                "intent": intent,
                "user_context": user_context,
                "knowlogy_enabled": self.use_knowlogy,
            }

        except Exception as e:
            logger.error(f"RAG query failed: {e}")
            return {
                "response_text": f"Error processing query: {str(e)}",
                "context_used": [],
                "intent": {},
                "error": str(e),
            }

    def _parse_intent(self, query: str) -> dict[str, Any]:
        """
        Simple keyword-based intent parsing.

        Extracts:
        - Entity names mentioned
        - Filter keywords (high, low, priority, status, etc.)

        Args:
            query: Natural language query

        Returns:
            Dict with extracted intent
        """
        intent = {
            "entities": [],
            "filters": {},
            "keywords": [],
        }

        # Extract entity names from enabled entities
        query_lower = query.lower()
        for entity_name in self.config.rag_enabled_entities:
            # Check singular and plural forms
            if (
                entity_name.lower() in query_lower
                or entity_name[:-1].lower() in query_lower
            ):
                intent["entities"].append(entity_name)

        # Extract common filter keywords
        priority_match = re.search(r"\b(high|low|medium)\s+priority\b", query_lower)
        if priority_match:
            intent["filters"]["priority"] = priority_match.group(1)

        status_match = re.search(
            r"\b(active|inactive|completed|pending)\b", query_lower
        )
        if status_match:
            intent["filters"]["status"] = status_match.group(1)

        # Extract general keywords (words longer than 3 chars, not stopwords)
        stopwords = {
            "what",
            "when",
            "where",
            "which",
            "show",
            "list",
            "get",
            "find",
            "the",
            "are",
        }
        words = re.findall(r"\b\w{4,}\b", query_lower)
        intent["keywords"] = [w for w in words if w not in stopwords]

        return intent

    def _retrieve_authorized_context(
        self, intent: dict[str, Any], user_context: str
    ) -> list[dict[str, Any]]:
        """
        Retrieve permission-aware context from EntityStore.

        Args:
            intent: Parsed intent dict
            user_context: User ID for permissions

        Returns:
            List of entity data dicts
        """
        context_chunks = []

        # Query each entity type mentioned
        for entity_name in intent["entities"]:
            try:
                # Use EntityStore's permission-aware get_entities
                # This automatically filters by user permissions
                entities = self.entity_store.get_entities(
                    entity_name=entity_name,
                    user_context=user_context,
                    limit=self.config.retrieval_k,
                )

                # Apply filter keywords if any
                if intent["filters"]:
                    entities = self._apply_filters(entities, intent["filters"])

                # Convert to context format
                for entity in entities:
                    context_chunks.append(
                        {
                            "entity_name": entity_name,
                            "entity_id": entity.get("id", "unknown"),
                            "data": entity,
                        }
                    )

            except Exception as e:
                logger.warning(f"Failed to retrieve {entity_name}: {e}")

        # Limit to retrieval_k total
        return context_chunks[: self.config.retrieval_k]

    def _apply_filters(
        self, entities: list[dict], filters: dict[str, str]
    ) -> list[dict]:
        """Apply simple field-based filters to entities."""
        filtered = []

        for entity in entities:
            match = True
            for field, value in filters.items():
                entity_value = entity.get(field, "").lower()
                if value.lower() not in entity_value:
                    match = False
                    break
            if match:
                filtered.append(entity)

        return filtered

    def _generate_response(
        self, query: str, context_chunks: list[dict[str, Any]]
    ) -> str:
        """
        Generate LLM response with context.

        Args:
            query: User query
            context_chunks: Retrieved context

        Returns:
            Generated response text
        """
        # Build context string
        context_parts = []
        for i, chunk in enumerate(context_chunks, 1):
            entity_name = chunk["entity_name"]
            data = chunk["data"]
            context_parts.append(f"[{i}] {entity_name}: {json.dumps(data, indent=2)}")

        context_str = (
            "\n\n".join(context_parts) if context_parts else "No relevant data found."
        )

        # Build system prompt
        system_prompt = self.config.system_prompt_template.format(
            context_str=context_str
        )

        # Generate response
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ]

        try:
            response = self.generation_model.generate(messages)
            return response
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return f"Error generating response: {str(e)}"


__all__ = ["SimpleRagPipeline"]


class VectorRagPipeline(SimpleRagPipeline):
    """
    Enhanced RAG pipeline with vector embeddings and semantic search.

    This extends SimpleRagPipeline to add:
    - Vector embeddings for semantic similarity
    - Hybrid retrieval (keyword + vector search)
    - Entity indexing capabilities
    """

    def __init__(
        self,
        config: AIConfig,
        entity_store: Any,
        vector_store: Any,
        embedding_model: Any,
    ):
        """
        Initialize vector-enabled RAG pipeline.

        Args:
            config: AIConfig with model and prompt configuration
            entity_store: EntityStore instance for data retrieval
            vector_store: Vector store for embeddings (e.g., SQLiteVectorStore)
            embedding_model: Embedding model (e.g., TetnusEmbeddingModel)
        """
        super().__init__(config, entity_store)
        self.vector_store = vector_store
        self.embedding_model = embedding_model

        logger.info(f"Initialized VectorRagPipeline with {embedding_model.model_name}")

    def index_entities(self, entity_names: list[str] | None = None):
        """
        Index entities for vector search.

        This method:
        1. Retrieves all entities (bypassing permissions for indexing)
        2. Converts to text
        3. Generates embeddings
        4. Stores in vector database

        Args:
            entity_names: List of entity names to index.
                         If None, index all RAG-enabled entities.
        """
        if entity_names is None:
            entity_names = list(self.config.rag_enabled_entities)

        logger.info(f"Indexing {len(entity_names)} entity types...")

        total_indexed = 0

        for entity_name in entity_names:
            if entity_name not in self.config.rag_enabled_entities:
                logger.warning(f"Skipping {entity_name} - not in RAG-enabled entities")
                continue

            try:
                # Get all entities (without permission filtering for indexing)
                entities = self.entity_store.get_all_entities(entity_name)

                if not entities:
                    logger.warning(f"No {entity_name} entities found")
                    continue

                # Prepare batch for embedding
                chunks = []
                texts = []

                for entity in entities:
                    entity_id = entity.get("id", f"unknown-{len(chunks)}")
                    text = self._entity_to_text(entity)

                    chunk_id = f"{entity_name}:{entity_id}"
                    chunks.append(
                        {
                            "chunk_id": chunk_id,
                            "entity_name": entity_name,
                            "entity_id": str(entity_id),
                            "content": text,
                        }
                    )
                    texts.append(text)

                # Generate embeddings in batch
                logger.info(f"Embedding {len(texts)} {entity_name}...")
                embeddings = self.embedding_model.embed_batch(texts)

                # Add vectors to chunks
                for chunk, embedding in zip(chunks, embeddings, strict=False):
                    chunk["vector"] = embedding

                # Store in vector DB
                self.vector_store.add_batch(chunks)
                total_indexed += len(chunks)

                logger.info(f"Indexed {len(chunks)} {entity_name} entities")

            except Exception as e:
                logger.error(f"Failed to index {entity_name}: {e}")

        logger.info(f"Indexing complete. Total: {total_indexed} chunks indexed.")

    def _entity_to_text(self, entity: dict[str, Any]) -> str:
        """
        Convert entity dict to text for embedding.

        Args:
            entity: Entity data dict

        Returns:
            Text representation
        """
        # Simple concatenation of all fields
        parts = []
        for key, value in entity.items():
            if value is not None:
                parts.append(f"{key}: {value}")

        return " | ".join(parts)

    def _retrieve_authorized_context(
        self, intent: dict[str, Any], user_context: str
    ) -> list[dict[str, Any]]:
        """
        Hybrid retrieval with vector search and permission filtering.

        Combines:
        1. Vector similarity search
        2. Permission filtering
        3. Keyword filtering from intent

        Args:
            intent: Parsed intent dict
            user_context: User ID for permissions

        Returns:
            List of authorized entity chunks
        """
        # Extract query for vector search
        # Use original query if available, otherwise reconstruct from keywords
        query_text = intent.get("query_text", " ".join(intent.get("keywords", [])))

        if not query_text:
            # Fall back to keyword-based retrieval
            logger.debug("No query text for vector search, using keyword retrieval")
            return super()._retrieve_authorized_context(intent, user_context)

        # Step 1: Vector search
        logger.debug(f"Performing vector search for: {query_text}")
        query_embedding = self.embedding_model.embed(query_text)

        # Retrieve more candidates than needed for permission filtering
        candidate_k = self.config.retrieval_k * 3

        # Filter by entity if specified in intent
        entity_filter = None
        if len(intent.get("entities", [])) == 1:
            entity_filter = intent["entities"][0]

        candidates = self.vector_store.search(
            query_vector=query_embedding,
            top_k=candidate_k,
            entity_filter=entity_filter,
        )

        # Step 2: Permission filtering
        authorized_chunks = []

        for chunk_id, score, content, metadata in candidates:
            entity_name = metadata["entity_name"]
            entity_id = metadata["entity_id"]

            # Check permission
            try:
                # Format permission check
                permission_obj = f"{entity_name}:{entity_id}"

                # Use EntityStore's check method if available
                if hasattr(self.entity_store, "check"):
                    has_access = self.entity_store.check(
                        user_context, "view", permission_obj
                    )
                else:
                    # Fallback: assume access (for demo/testing)
                    has_access = True
                    logger.warning(
                        "EntityStore has no check method - allowing all access"
                    )

                if has_access:
                    authorized_chunks.append(
                        {
                            "chunk_id": chunk_id,
                            "entity_name": entity_name,
                            "entity_id": entity_id,
                            "content": content,
                            "score": score,
                            "data": {
                                "id": entity_id,
                                "content": content,
                            },
                        }
                    )

                # Stop if we have enough
                if len(authorized_chunks) >= self.config.retrieval_k:
                    break

            except Exception as e:
                logger.warning(f"Permission check failed for {chunk_id}: {e}")

        logger.info(
            f"Vector search: {len(candidates)} candidates → "
            f"{len(authorized_chunks)} authorized"
        )

        return authorized_chunks

    def run_query(self, query: str, user_context: str) -> dict[str, Any]:
        """
        Run RAG query with vector search.

        Extends parent method to:
        - Store original query for vector search
        - Include similarity scores in results

        Args:
            query: Natural language query
            user_context: User ID for permission checks

        Returns:
            Dict with response_text, context_used, scores, etc.
        """
        logger.info(f"Running vector RAG query for user: {user_context}")

        try:
            # Parse intent and add original query
            intent = self._parse_intent(query)
            intent["query_text"] = query  # Add for vector search
            logger.debug(f"Parsed intent: {intent}")

            # Retrieve with vector search
            context_chunks = self._retrieve_authorized_context(intent, user_context)
            logger.debug(f"Retrieved {len(context_chunks)} context chunks")

            # Generate response
            response_text = self._generate_response(query, context_chunks)

            return {
                "response_text": response_text,
                "context_used": context_chunks,
                "intent": intent,
                "user_context": user_context,
                "search_method": "vector",
            }

        except Exception as e:
            logger.error(f"Vector RAG query failed: {e}")
            return {
                "response_text": f"Error processing query: {str(e)}",
                "context_used": [],
                "intent": {},
                "error": str(e),
            }


__all__ = ["SimpleRagPipeline", "VectorRagPipeline"]
