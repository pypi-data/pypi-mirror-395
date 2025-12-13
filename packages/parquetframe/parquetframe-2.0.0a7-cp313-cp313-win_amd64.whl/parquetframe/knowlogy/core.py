"""
Knowlogy Core Engine.

Manages the Knowledge Graph interaction.
"""

from .storage import Concept, Formula


class KnowlogyEngine:
    """
    Engine for interacting with the Knowlogy Knowledge Graph.
    """

    def __init__(self):
        """Initialize the engine."""
        # In the future, this might load embeddings or Rust extensions
        pass

    def search_concepts(self, query: str) -> list[Concept]:
        """
        Search for concepts by name or alias.

        Args:
            query: Search term

        Returns:
            List of matching Concept entities
        """
        query = query.lower()

        # Naive search for MVP (will be replaced by vector search later)
        # Get all concepts and filter in Python
        all_concepts = Concept.find_all()

        # Filter matching concepts
        matching = []
        for c in all_concepts:
            if query in c.name.lower():
                matching.append(c)
            elif hasattr(c, "aliases") and c.aliases:
                if any(query in alias.lower() for alias in c.aliases):
                    matching.append(c)

        return matching

    def get_formula(self, concept_name: str) -> Formula | None:
        """
        Get the primary formula for a concept.

        Args:
            concept_name: Name of the concept

        Returns:
            Formula entity or None
        """
        concepts = self.search_concepts(concept_name)
        if not concepts:
            return None

        # Get the first matching concept
        concept = concepts[0]

        # Traverse relationship to find formulas
        formulas = concept.formulas().execute()

        if formulas:
            return formulas[0]
        return None

    def add_concept(
        self,
        id: str,
        name: str,
        description: str,
        domain: str,
        aliases: list[str] = None,
    ) -> Concept:
        """
        Add a new concept to the graph.
        """
        concept = Concept(
            id=id,
            name=name,
            description=description,
            domain=domain,
            aliases=aliases or [],
        )
        concept.save()
        return concept

    def add_formula(
        self,
        id: str,
        name: str,
        latex: str,
        symbolic: str,
        concept_id: str,
        variables: list[str] = None,
    ) -> Formula:
        """
        Add a new formula to the graph.
        """
        formula = Formula(
            id=id,
            name=name,
            latex=latex,
            symbolic=symbolic,
            concept_id=concept_id,
            variables=variables or [],
        )
        formula.save()
        return formula

    def get_context_for_rag(self, query: str) -> str:
        """
        Retrieve structured context for RAG grounding.

        Args:
            query: User query

        Returns:
            Formatted string with definitions and formulas
        """
        concepts = self.search_concepts(query)
        if not concepts:
            return ""

        context_parts = []
        for concept in concepts[:3]:  # Limit to top 3 matches
            part = f"Concept: {concept.name}\nDefinition: {concept.description}"

            formulas = concept.formulas().execute()
            if formulas:
                part += "\nFormulas:"
                for f in formulas:
                    part += f"\n  - {f.name}: {f.latex}"

            context_parts.append(part)

        return "\n\n".join(context_parts)
