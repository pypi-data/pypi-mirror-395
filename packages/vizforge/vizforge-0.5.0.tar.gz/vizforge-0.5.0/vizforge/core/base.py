"""Base chart class for all VizForge visualizations."""

from typing import Any, Optional
import plotly.graph_objects as go
from .theme import get_theme, Theme


class BaseChart:
    """
    Base class for all VizForge charts.

    Provides common functionality for creating, customizing,
    and exporting visualizations.
    """

    def __init__(
        self,
        title: Optional[str] = None,
        theme: Optional[str | Theme] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        **kwargs
    ):
        """
        Initialize a base chart.

        Args:
            title: Chart title
            theme: Theme name or Theme object
            width: Chart width in pixels
            height: Chart height in pixels
            **kwargs: Additional keyword arguments
        """
        self.title = title
        self._theme = self._resolve_theme(theme)
        self.width = width
        self.height = height
        self.fig: Optional[go.Figure] = None
        self._kwargs = kwargs

    def _resolve_theme(self, theme: Optional[str | Theme]) -> Theme:
        """Resolve theme to Theme object."""
        if theme is None:
            return get_theme()
        elif isinstance(theme, str):
            return get_theme(theme)
        elif isinstance(theme, Theme):
            return theme
        else:
            raise TypeError("Theme must be None, string, or Theme object")

    def _create_figure(self) -> go.Figure:
        """Create a new Plotly figure with theme applied."""
        fig = go.Figure()

        # Apply theme layout
        theme_layout = self._theme.to_plotly_layout()
        fig.update_layout(**theme_layout)

        # Apply title
        if self.title:
            fig.update_layout(title=self.title)

        # Apply dimensions
        if self.width:
            fig.update_layout(width=self.width)
        if self.height:
            fig.update_layout(height=self.height)

        return fig

    def update_layout(self, **kwargs) -> 'BaseChart':
        """
        Update chart layout.

        Args:
            **kwargs: Plotly layout parameters

        Returns:
            Self for method chaining

        Example:
            >>> chart.update_layout(title="New Title", height=600)
        """
        if self.fig is None:
            raise RuntimeError("Chart not created yet")

        self.fig.update_layout(**kwargs)
        return self

    def update_xaxis(self, **kwargs) -> 'BaseChart':
        """
        Update x-axis configuration.

        Args:
            **kwargs: Plotly xaxis parameters

        Returns:
            Self for method chaining

        Example:
            >>> chart.update_xaxis(title="Time", tickangle=45)
        """
        if self.fig is None:
            raise RuntimeError("Chart not created yet")

        self.fig.update_xaxes(**kwargs)
        return self

    def update_yaxis(self, **kwargs) -> 'BaseChart':
        """
        Update y-axis configuration.

        Args:
            **kwargs: Plotly yaxis parameters

        Returns:
            Self for method chaining

        Example:
            >>> chart.update_yaxis(title="Revenue", tickformat="$,.0f")
        """
        if self.fig is None:
            raise RuntimeError("Chart not created yet")

        self.fig.update_yaxes(**kwargs)
        return self

    def show(self) -> None:
        """
        Display the chart.

        Opens the chart in a web browser or Jupyter notebook.

        Example:
            >>> chart.show()
        """
        if self.fig is None:
            raise RuntimeError("Chart not created yet")

        self.fig.show()

    def export(
        self,
        filename: str,
        format: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        scale: float = 1.0
    ) -> None:
        """
        Export chart to file.

        Args:
            filename: Output filename
            format: Output format (png, svg, html, pdf). Auto-detected from filename if not specified
            width: Export width in pixels
            height: Export height in pixels
            scale: Scale factor for raster images

        Example:
            >>> chart.export("output.png", width=1920, height=1080)
            >>> chart.export("chart.html")
        """
        if self.fig is None:
            raise RuntimeError("Chart not created yet")

        # Auto-detect format from filename
        if format is None:
            if '.' in filename:
                format = filename.split('.')[-1].lower()
            else:
                raise ValueError("Cannot detect format from filename. Specify format parameter.")

        # Handle different export formats
        if format in ['png', 'jpg', 'jpeg', 'svg', 'pdf', 'webp']:
            self._export_static(filename, format, width, height, scale)
        elif format in ['html', 'htm']:
            self._export_html(filename)
        elif format == 'json':
            self._export_json(filename)
        else:
            raise ValueError(f"Unsupported export format: {format}")

    def _export_static(
        self,
        filename: str,
        format: str,
        width: Optional[int],
        height: Optional[int],
        scale: float
    ) -> None:
        """Export to static image format."""
        try:
            self.fig.write_image(
                filename,
                format=format,
                width=width or self.width,
                height=height or self.height,
                scale=scale
            )
        except Exception as e:
            if "kaleido" in str(e).lower():
                raise ImportError(
                    "Static image export requires kaleido. "
                    "Install with: pip install kaleido"
                ) from e
            raise

    def _export_html(self, filename: str) -> None:
        """Export to interactive HTML."""
        self.fig.write_html(filename)

    def _export_json(self, filename: str) -> None:
        """Export chart configuration to JSON."""
        import json
        with open(filename, 'w') as f:
            json.dump(self.fig.to_dict(), f, indent=2)

    def to_html(self, **kwargs) -> str:
        """
        Get HTML representation of the chart.

        Args:
            **kwargs: Additional arguments for to_html

        Returns:
            HTML string

        Example:
            >>> html = chart.to_html(include_plotlyjs='cdn')
        """
        if self.fig is None:
            raise RuntimeError("Chart not created yet")

        return self.fig.to_html(**kwargs)

    def to_dict(self) -> dict:
        """
        Get dictionary representation of the chart.

        Returns:
            Chart configuration as dictionary

        Example:
            >>> config = chart.to_dict()
        """
        if self.fig is None:
            raise RuntimeError("Chart not created yet")

        return self.fig.to_dict()

    def to_json(self) -> str:
        """
        Get JSON representation of the chart.

        Returns:
            Chart configuration as JSON string

        Example:
            >>> json_str = chart.to_json()
        """
        if self.fig is None:
            raise RuntimeError("Chart not created yet")

        return self.fig.to_json()
