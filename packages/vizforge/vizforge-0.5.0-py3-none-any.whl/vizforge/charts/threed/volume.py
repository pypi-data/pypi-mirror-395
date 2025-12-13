"""Volume plot implementation for VizForge."""

from typing import Optional, Union, List
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from ...core.base import BaseChart
from ...core.theme import Theme


class VolumePlot(BaseChart):
    """
    3D Volume plot visualization.

    Creates volumetric data visualizations using isosurfaces.
    Perfect for medical imaging, fluid dynamics, and 3D scalar fields.

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>>
        >>> # Create 3D volume data
        >>> X, Y, Z = np.mgrid[-5:5:40j, -5:5:40j, -5:5:40j]
        >>> values = np.sin(X) * np.cos(Y) * np.sin(Z)
        >>>
        >>> vz.volume(X, Y, Z, values, title='3D Volume')
    """

    def __init__(
        self,
        x: Union[np.ndarray, List],
        y: Union[np.ndarray, List],
        z: Union[np.ndarray, List],
        values: Union[np.ndarray, List],
        title: Optional[str] = None,
        colorscale: str = "Viridis",
        opacity: float = 0.1,
        surface_count: int = 15,
        **kwargs
    ):
        """
        Initialize Volume plot.

        Args:
            x: X coordinates (3D array)
            y: Y coordinates (3D array)
            z: Z coordinates (3D array)
            values: Scalar values at each point (3D array)
            title: Chart title
            colorscale: Color scale
            opacity: Volume opacity (0-1)
            surface_count: Number of isosurfaces
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        self.x = x
        self.y = y
        self.z = z
        self.values = values
        self.colorscale = colorscale
        self.opacity = opacity
        self.surface_count = surface_count

    def create_trace(self) -> go.Volume:
        """Create Plotly Volume trace."""

        trace = go.Volume(
            x=self.x.flatten(),
            y=self.y.flatten(),
            z=self.z.flatten(),
            value=self.values.flatten(),
            colorscale=self.colorscale,
            opacity=self.opacity,
            surface_count=self.surface_count,
            name=self.title or "Volume"
        )

        return trace

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure."""
        trace = self.create_trace()

        layout = go.Layout(
            title=self.title,
            scene=dict(
                xaxis=dict(title="X"),
                yaxis=dict(title="Y"),
                zaxis=dict(title="Z")
            ),
            **self._get_theme_layout()
        )

        fig = go.Figure(data=[trace], layout=layout)
        return fig


def volume(
    x: Union[np.ndarray, List],
    y: Union[np.ndarray, List],
    z: Union[np.ndarray, List],
    values: Union[np.ndarray, List],
    title: Optional[str] = None,
    colorscale: str = "Viridis",
    opacity: float = 0.1,
    surface_count: int = 15,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> VolumePlot:
    """
    Create a 3D volume plot.

    Args:
        x: X coordinates (3D array)
        y: Y coordinates (3D array)
        z: Z coordinates (3D array)
        values: Scalar values (3D array)
        title: Chart title
        colorscale: Color scale
        opacity: Volume opacity
        surface_count: Number of isosurfaces
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        VolumePlot instance

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>>
        >>> # 3D Gaussian
        >>> X, Y, Z = np.mgrid[-5:5:40j, -5:5:40j, -5:5:40j]
        >>> values = np.exp(-(X**2 + Y**2 + Z**2))
        >>>
        >>> vz.volume(X, Y, Z, values, title='3D Gaussian')
    """
    chart = VolumePlot(
        x=x, y=y, z=z, values=values,
        title=title,
        colorscale=colorscale,
        opacity=opacity,
        surface_count=surface_count,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart
