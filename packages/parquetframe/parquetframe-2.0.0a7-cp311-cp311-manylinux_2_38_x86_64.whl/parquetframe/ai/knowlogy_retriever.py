"""
Knowlogy Retriever for RAG Pipeline.

Retrieves concepts, formulas, and definitions from the Knowlogy knowledge graph
to ground LLM responses with verifiable, formal knowledge.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class Document:
    """A retrieved document with content and metadata."""

    content: str
    metadata: dict[str, Any]
    score: float = 1.0


class KnowlogyRetriever:
    """
    Retrieve concepts and formulas from Knowlogy knowledge graph.

    Example:
        >>> retriever = KnowlogyRetriever()
        >>> docs = retriever.retrieve("variance")
        >>> for doc in docs:
        ...     print(doc.content)
    """

    def __init__(self):
        """Initialize Knowlogy retriever."""
        pass

    def retrieve(self, query: str, top_k: int = 5) -> list[Document]:
        """
        Retrieve relevant knowledge from graph.

        Args:
            query: Search query
            top_k: Maximum number of results

        Returns:
            List of documents with concepts, formulas, and descriptions
        """
        from parquetframe import knowlogy

        documents = []

        # Search for concepts
        concepts = knowlogy.search(query)

        for concept in concepts[:top_k]:
            # Get associated formula if it exists
            try:
                formula = knowlogy.get_formula(concept.name)
                content = self._format_concept_with_formula(concept, formula)
            except Exception:
                # No formula found, just use concept
                content = self._format_concept(concept)

            doc = Document(
                content=content,
                metadata={
                    "concept_id": concept.id,
                    "concept_name": concept.name,
                    "domain": concept.domain,
                    "source": "knowlogy",
                },
            )
            documents.append(doc)

        return documents

    def _format_concept(self, concept) -> str:
        """Format concept without formula."""
        return f"""
**{concept.name}** ({concept.domain})

{concept.description}

Aliases: {", ".join(concept.aliases) if concept.aliases else "None"}
"""

    def _format_concept_with_formula(self, concept, formula) -> str:
        """Format concept with associated formula."""
        return f"""
**{concept.name}** ({concept.domain})

{concept.description}

**Formula (LaTeX):** {formula.latex}

**Symbolic:** {formula.symbolic}

**Variables:** {", ".join(formula.variables) if formula.variables else "None"}

Aliases: {", ".join(concept.aliases) if concept.aliases else "None"}
"""


__all__ = ["KnowlogyRetriever", "Document"]
