"""
Core Dashboard classes.
"""

from .layout import Container
from .renderer import HtmlRenderer


class Page(Container):
    """A single page in the dashboard."""

    def __init__(self, title: str = "Page", **kwargs):
        super().__init__(**kwargs)
        self.title = title


class Dashboard:
    """Top-level dashboard container."""

    def __init__(self, title: str = "Dashboard"):
        self.title = title
        self.pages: list[Page] = []

    def add_page(self, page: Page):
        self.pages.append(page)
        return self

    def render(self) -> str:
        """Render the dashboard to HTML string."""
        # For MVP, just render the first page or stack them
        content = ""
        for page in self.pages:
            content += page.render()

        renderer = HtmlRenderer(title=self.title)
        return renderer.render(content)

    def save(self, filename: str):
        """Save dashboard to an HTML file."""
        html = self.render()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
