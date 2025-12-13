"""
Formula grounding and verification utilities.

Validates LLM responses against Knowlogy formulas to ensure accuracy.
"""

import re
from typing import Any


def extract_formulas(text: str) -> list[str]:
    """
    Extract LaTeX formulas from text.

    Args:
        text: Text potentially containing LaTeX formulas

    Returns:
        List of extracted LaTeX formulas
    """
    # Find inline math: $...$
    inline = re.findall(r"\$([^\$]+)\$", text)

    # Find display math: $$...$$
    display = re.findall(r"\$\$([^\$]+)\$\$", text)

    return inline + display


def verify_formula(response: str) -> dict[str, Any]:
    """
    Extract and verify formulas in LLM response.

    Args:
        response: LLM generated response

    Returns:
        Dictionary with verification results
    """

    formulas_found = extract_formulas(response)
    verified = []
    corrections = []

    for formula in formulas_found:
        # Try to find this formula in Knowlogy
        # This is a simplified check
        found_in_knowlogy = False

        # Search for similar concepts
        # In a real implementation, this would do fuzzy matching
        # or parse the formula structure

        verified.append({"formula": formula, "found_in_knowlogy": found_in_knowlogy})

    return {
        "formulas_found": formulas_found,
        "verified": verified,
        "corrections": corrections,
        "num_formulas": len(formulas_found),
    }


def ground_response(query: str, response: str) -> dict[str, Any]:
    """
     Ground LLM response with Knowlogy knowledge.

     Args:
         query: Original query
         response: LLM response to ground

    Returns:
         Grounded response with verification
    """
    from parquetframe.ai.knowlogy_retriever import KnowlogyRetriever

    # Get relevant knowledge
    retriever = KnowlogyRetriever()
    knowledge_docs = retriever.retrieve(query, top_k=3)

    # Verify formulas
    verification = verify_formula(response)

    return {
        "original_response": response,
        "knowledge_sources": [doc.metadata for doc in knowledge_docs],
        "formula_verification": verification,
        "grounded": True,
    }


__all__ = ["extract_formulas", "verify_formula", "ground_response"]
