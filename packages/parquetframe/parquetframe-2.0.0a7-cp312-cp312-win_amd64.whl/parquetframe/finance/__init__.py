"""
Financial analysis functionality for ParquetFrame.

Provides .fin accessor for technical indicators and financial analysis.
"""

# Import accessor to register it
from .accessor import FinAccessor, FinanceAccessor

__all__ = ["FinanceAccessor", "FinAccessor"]
