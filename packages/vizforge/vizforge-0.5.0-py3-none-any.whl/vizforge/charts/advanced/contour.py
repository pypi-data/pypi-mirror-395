"""Contour Plot implementation for VizForge."""

from typing import Optional, List, Union
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from ...core.base import BaseChart
from ...core.theme import Theme


class ContourPlot(BaseChart):
    """
    Contour Plot visualization.

    Shows 3D data as 2D contour lines.
    Perfect for topographic maps, optimization landscapes, density estimation.

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>>
        >>> # Create grid data
        >>> x = np.linspace(-5, 5, 50)
        >>> y = np.linspace(-5, 5, 50)
        >>> X, Y = np.meshgrid(x, y)
        >>> Z = np.sin(np.sqrt(X**2 + Y**2))
        >>>
        >>> vz.contour(x, y, Z, title='Wave Pattern')
    """

    def __init__(
        self,
        x: Union[np.ndarray, List],
        y: Union[np.ndarray, List],
        z: np.ndarray,
        colorscale: str = 'Viridis',
        contours_coloring: str = 'heatmap',  # 'heatmap', 'lines', 'none'
        show_lines: bool = True,
        show_labels: bool = True,
        title: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize Contour Plot.

        Args:
            x: X coordinates
            y: Y coordinates
            z: Z values (2D array)
            colorscale: Color scale
            contours_coloring: Contour coloring mode
            show_lines: Show contour lines
            show_labels: Show contour labels
            title: Chart title
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        self.x = x
        self.y = y
        self.z = z
        self.colorscale = colorscale
        self.contours_coloring = contours_coloring
        self.show_lines = show_lines
        self.show_labels = show_labels

    def create_trace(self) -> go.Contour:
        """Create contour trace."""
        contour = go.Contour(
            x=self.x,
            y=self.y,
            z=self.z,
            colorscale=self.colorscale,
            contours=dict(
                coloring=self.contours_coloring,
                showlabels=self.show_labels,
                labelfont=dict(size=12, color='white')
            ) if self.show_lines else None,
            line=dict(width=2) if self.show_lines else None,
            hovertemplate='X: %{x}<br>Y: %{y}<br>Z: %{z}<extra></extra>'
        )
        return contour

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure."""
        trace = self.create_trace()

        layout = go.Layout(
            title=self.title,
            xaxis=dict(title='X'),
            yaxis=dict(title='Y'),
            **self._get_theme_layout()
        )

        fig = go.Figure(data=[trace], layout=layout)
        return fig


class FilledContour(BaseChart):
    """
    Filled Contour Plot.

    Shows filled contour regions with color gradients.
    Perfect for heat maps, probability densities.
    """

    def __init__(
        self,
        x: Union[np.ndarray, List],
        y: Union[np.ndarray, List],
        z: np.ndarray,
        colorscale: str = 'Viridis',
        ncontours: int = 15,
        title: Optional[str] = None,
        **kwargs
    ):
        """Initialize Filled Contour."""
        super().__init__(title=title, **kwargs)

        self.x = x
        self.y = y
        self.z = z
        self.colorscale = colorscale
        self.ncontours = ncontours

    def create_trace(self) -> go.Contour:
        """Create filled contour trace."""
        contour = go.Contour(
            x=self.x,
            y=self.y,
            z=self.z,
            colorscale=self.colorscale,
            ncontours=self.ncontours,
            contours=dict(
                coloring='fill',
                showlines=True,
                showlabels=False
            )
        )
        return contour

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure."""
        trace = self.create_trace()

        layout = go.Layout(
            title=self.title,
            xaxis=dict(title='X'),
            yaxis=dict(title='Y'),
            **self._get_theme_layout()
        )

        fig = go.Figure(data=[trace], layout=layout)
        return fig


def contour(
    x: Union[np.ndarray, List],
    y: Union[np.ndarray, List],
    z: np.ndarray,
    colorscale: str = 'Viridis',
    contours_coloring: str = 'heatmap',
    show_lines: bool = True,
    show_labels: bool = True,
    title: Optional[str] = None,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> ContourPlot:
    """
    Create a contour plot.

    Args:
        x: X coordinates
        y: Y coordinates
        z: Z values
        colorscale: Color scale
        contours_coloring: Coloring mode
        show_lines: Show lines
        show_labels: Show labels
        title: Chart title
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        ContourPlot instance

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>>
        >>> # Optimization landscape
        >>> x = np.linspace(-3, 3, 100)
        >>> y = np.linspace(-3, 3, 100)
        >>> X, Y = np.meshgrid(x, y)
        >>> Z = (1 - X)**2 + 100 * (Y - X**2)**2  # Rosenbrock function
        >>>
        >>> vz.contour(x, y, Z, title='Rosenbrock Function',
        >>>           colorscale='RdYlBu')
    """
    chart = ContourPlot(
        x=x,
        y=y,
        z=z,
        colorscale=colorscale,
        contours_coloring=contours_coloring,
        show_lines=show_lines,
        show_labels=show_labels,
        title=title,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart


def filled_contour(
    x: Union[np.ndarray, List],
    y: Union[np.ndarray, List],
    z: np.ndarray,
    colorscale: str = 'Viridis',
    ncontours: int = 15,
    title: Optional[str] = None,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> FilledContour:
    """
    Create a filled contour plot.

    Args:
        x: X coordinates
        y: Y coordinates
        z: Z values
        colorscale: Color scale
        ncontours: Number of contours
        title: Chart title
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        FilledContour instance

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>>
        >>> x = np.linspace(0, 10, 50)
        >>> y = np.linspace(0, 10, 50)
        >>> X, Y = np.meshgrid(x, y)
        >>> Z = np.sin(X) * np.cos(Y)
        >>>
        >>> vz.filled_contour(x, y, Z, title='2D Pattern')
    """
    chart = FilledContour(
        x=x,
        y=y,
        z=z,
        colorscale=colorscale,
        ncontours=ncontours,
        title=title,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart
