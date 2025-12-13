"""
Layout components for Dashboard as Code.
"""

import uuid
from abc import ABC, abstractmethod


class LayoutElement(ABC):
    """Base class for all layout elements."""

    def __init__(
        self, css_class: str | None = None, style: dict[str, str] | None = None
    ):
        self.id = str(uuid.uuid4())
        self.css_class = css_class or ""
        self.style = style or {}

    @abstractmethod
    def render(self) -> str:
        """Render the element to HTML."""
        pass

    def _render_style(self) -> str:
        if not self.style:
            return ""
        return ' style="' + "; ".join(f"{k}: {v}" for k, v in self.style.items()) + '"'


class Container(LayoutElement):
    """A container that holds other elements."""

    def __init__(self, children: list[LayoutElement] | None = None, **kwargs):
        super().__init__(**kwargs)
        self.children = children or []

    def add(self, element: LayoutElement):
        self.children.append(element)
        return self

    def render(self) -> str:
        content = "\n".join(child.render() for child in self.children)
        return f'<div class="dac-container {self.css_class}"{self._render_style()}>\n{content}\n</div>'


class Row(Container):
    """A row in the grid layout."""

    def render(self) -> str:
        content = "\n".join(child.render() for child in self.children)
        return f'<div class="dac-row {self.css_class}"{self._render_style()}>\n{content}\n</div>'


class Column(Container):
    """A column in the grid layout."""

    def __init__(self, width: int = 12, **kwargs):
        """
        Args:
            width: Width in grid units (1-12).
        """
        super().__init__(**kwargs)
        self.width = width

    def render(self) -> str:
        content = "\n".join(child.render() for child in self.children)
        return f'<div class="dac-col-{self.width} {self.css_class}"{self._render_style()}>\n{content}\n</div>'
