"""
Knowlogy Storage Layer.

Defines the GraphAr-compliant entities for the Knowledge Graph using
ParquetFrame's Entity Framework.
"""

from dataclasses import dataclass, field

from parquetframe.entity import entity, rel


@entity(storage_path="./data/knowlogy/concepts", primary_key="id")
@dataclass
class Concept:
    """
    A conceptual node in the Knowledge Graph.

    Represents an abstract idea (e.g., "Arithmetic Mean", "Newton's Second Law").
    """

    id: str  # e.g., "wd:Q12345" or "pf:concept:mean"
    name: str
    description: str
    domain: str  # e.g., "Statistics", "Physics"
    aliases: list[str] = field(default_factory=list)

    @rel("Formula", foreign_key="concept_id", reverse=True)
    def formulas(self):
        """Formulas that define or calculate this concept."""
        pass

    @rel("Concept", foreign_key="parent_id")
    def parent(self):
        """Parent concept (IS_A relationship)."""
        pass


@entity(storage_path="./data/knowlogy/formulas", primary_key="id")
@dataclass
class Formula:
    """
    A mathematical formula node.

    Represents a specific equation (e.g., "x_bar = sum(x) / n").
    """

    id: str  # e.g., "pf:formula:mean_sample"
    name: str
    latex: str  # LaTeX representation
    symbolic: str  # SymPy or computer-readable representation
    concept_id: str  # Link to the Concept this formula defines
    variables: list[str] = field(default_factory=list)  # List of variable symbols used

    @rel("Concept", foreign_key="concept_id")
    def concept(self):
        """The concept this formula belongs to."""
        pass


@entity(storage_path="./data/knowlogy/applications", primary_key="id")
@dataclass
class Application:
    """
    A real-world application of a concept.
    """

    id: str
    name: str
    description: str
    concept_id: str

    @rel("Concept", foreign_key="concept_id")
    def concept(self):
        """The concept applied here."""
        pass
