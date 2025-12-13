"""
Widget components for Dashboard as Code.
"""

from typing import Any

import pandas as pd

from .layout import LayoutElement


class Widget(LayoutElement):
    """Base class for widgets."""

    pass


class Markdown(Widget):
    """Markdown text widget."""

    def __init__(self, content: str, **kwargs):
        super().__init__(**kwargs)
        self.content = content

    def render(self) -> str:
        # In a real implementation, we would use a markdown library here.
        # For now, simple text wrapping or basic HTML injection if the user provides it.
        # Ideally, we'd use `markdown` package.
        import markdown

        html_content = markdown.markdown(self.content)
        return f'<div class="dac-widget dac-markdown {self.css_class}"{self._render_style()}>\n{html_content}\n</div>'


class Metric(Widget):
    """KPI Metric widget."""

    def __init__(
        self,
        label: str,
        value: Any,
        delta: str | None = None,
        delta_color: str = "normal",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.label = label
        self.value = str(value)
        self.delta = delta
        self.delta_color = delta_color  # normal, inverse, off

    def render(self) -> str:
        delta_html = ""
        if self.delta:
            color_class = "dac-text-neutral"
            if self.delta.startswith("+"):
                color_class = (
                    "dac-text-green" if self.delta_color == "normal" else "dac-text-red"
                )
            elif self.delta.startswith("-"):
                color_class = (
                    "dac-text-red" if self.delta_color == "normal" else "dac-text-green"
                )

            delta_html = (
                f'<span class="dac-metric-delta {color_class}">{self.delta}</span>'
            )

        return f"""
        <div class="dac-widget dac-metric {self.css_class}"{self._render_style()}>
            <div class="dac-metric-label">{self.label}</div>
            <div class="dac-metric-value">{self.value}</div>
            {delta_html}
        </div>
        """


class Table(Widget):
    """DataFrame Table widget."""

    def __init__(self, df: pd.DataFrame, page_size: int = 10, **kwargs):
        super().__init__(**kwargs)
        self.df = df
        self.page_size = page_size

    def render(self) -> str:
        # Simple HTML table for now. In production, use DataTables or similar.
        html_table = self.df.head(self.page_size).to_html(
            classes="dac-table", border=0, index=False
        )
        return f'<div class="dac-widget dac-table-container {self.css_class}"{self._render_style()}>\n{html_table}\n</div>'


class Chart(Widget):
    """Chart widget wrapping visualization libraries."""

    def __init__(
        self, figure: Any, library: str = "auto", height: str = "400px", **kwargs
    ):
        """
        Args:
            figure: The chart object (matplotlib, plotly, altair, or raw HTML).
            library: 'plotly', 'altair', 'matplotlib', or 'auto'.
            height: CSS height.
        """
        super().__init__(**kwargs)
        self.figure = figure
        self.library = library
        self.height = height
        if "height" not in self.style:
            self.style["height"] = height

    def render(self) -> str:
        content = ""

        # Basic Plotly support
        if hasattr(self.figure, "to_html"):
            # Likely Plotly or Altair
            content = self.figure.to_html(full_html=False, include_plotlyjs="cdn")
        else:
            content = str(self.figure)

        return f'<div class="dac-widget dac-chart {self.css_class}"{self._render_style()}>\n{content}\n</div>'
