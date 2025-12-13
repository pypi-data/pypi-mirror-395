"""
Dashboard as Code (DaC) module.

Declarative framework for building interactive data dashboards.
"""

from .dashboard import Dashboard, Page
from .layout import Column, Container, Row
from .parser import GizaParser
from .widgets import Chart, Markdown, Metric, Table, Widget

__all__ = [
    "Dashboard",
    "Page",
    "Row",
    "Column",
    "Container",
    "Widget",
    "Chart",
    "Table",
    "Metric",
    "Markdown",
    "GizaParser",
]
