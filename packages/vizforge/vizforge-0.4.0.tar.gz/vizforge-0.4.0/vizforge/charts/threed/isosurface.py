"""Isosurface plot implementation for VizForge."""

from typing import Optional, Union, List
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from ...core.base import BaseChart
from ...core.theme import Theme


class IsosurfacePlot(BaseChart):
    """
    3D Isosurface plot visualization.

    Creates isosurface visualizations for 3D scalar fields.
    Perfect for medical imaging, molecular orbitals, and level sets.

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>>
        >>> # 3D scalar field
        >>> X, Y, Z = np.mgrid[-5:5:40j, -5:5:40j, -5:5:40j]
        >>> values = np.sin(X) + np.cos(Y) + np.sin(Z)
        >>>
        >>> vz.isosurface(X, Y, Z, values, title='Isosurface')
    """

    def __init__(
        self,
        x: Union[np.ndarray, List],
        y: Union[np.ndarray, List],
        z: Union[np.ndarray, List],
        values: Union[np.ndarray, List],
        title: Optional[str] = None,
        isomin: Optional[float] = None,
        isomax: Optional[float] = None,
        colorscale: str = "Viridis",
        opacity: float = 0.7,
        surface_count: int = 2,
        caps: Optional[dict] = None,
        **kwargs
    ):
        """
        Initialize Isosurface plot.

        Args:
            x: X coordinates (3D array)
            y: Y coordinates (3D array)
            z: Z coordinates (3D array)
            values: Scalar values (3D array)
            title: Chart title
            isomin: Minimum isosurface value
            isomax: Maximum isosurface value
            colorscale: Color scale
            opacity: Surface opacity (0-1)
            surface_count: Number of isosurfaces
            caps: Caps configuration dict
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

        # Auto-calculate isomin/isomax if not provided
        flat_values = values.flatten() if hasattr(values, 'flatten') else np.array(values).flatten()
        self.isomin = isomin if isomin is not None else float(np.min(flat_values))
        self.isomax = isomax if isomax is not None else float(np.max(flat_values))

        self.caps = caps or dict(x=dict(show=False), y=dict(show=False), z=dict(show=False))

    def create_trace(self) -> go.Isosurface:
        """Create Plotly Isosurface trace."""

        trace = go.Isosurface(
            x=self.x.flatten() if hasattr(self.x, 'flatten') else self.x,
            y=self.y.flatten() if hasattr(self.y, 'flatten') else self.y,
            z=self.z.flatten() if hasattr(self.z, 'flatten') else self.z,
            value=self.values.flatten() if hasattr(self.values, 'flatten') else self.values,
            isomin=self.isomin,
            isomax=self.isomax,
            colorscale=self.colorscale,
            opacity=self.opacity,
            surface_count=self.surface_count,
            caps=self.caps,
            name=self.title or "Isosurface"
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
                zaxis=dict(title="Z"),
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.3)
                )
            ),
            **self._get_theme_layout()
        )

        fig = go.Figure(data=[trace], layout=layout)
        return fig


def isosurface(
    x: Union[np.ndarray, List],
    y: Union[np.ndarray, List],
    z: Union[np.ndarray, List],
    values: Union[np.ndarray, List],
    title: Optional[str] = None,
    isomin: Optional[float] = None,
    isomax: Optional[float] = None,
    colorscale: str = "Viridis",
    opacity: float = 0.7,
    surface_count: int = 2,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> IsosurfacePlot:
    """
    Create a 3D isosurface plot.

    Args:
        x: X coordinates (3D array)
        y: Y coordinates (3D array)
        z: Z coordinates (3D array)
        values: Scalar values (3D array)
        title: Chart title
        isomin: Minimum iso value
        isomax: Maximum iso value
        colorscale: Color scale
        opacity: Surface opacity
        surface_count: Number of isosurfaces
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        IsosurfacePlot instance

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>>
        >>> # 3D wave function
        >>> X, Y, Z = np.mgrid[-5:5:40j, -5:5:40j, -5:5:40j]
        >>> values = np.sin(X) + np.cos(Y) + np.sin(Z)
        >>>
        >>> vz.isosurface(X, Y, Z, values,
        >>>               title='Wave Isosurface',
        >>>               surface_count=3)
    """
    chart = IsosurfacePlot(
        x=x, y=y, z=z, values=values,
        title=title,
        isomin=isomin,
        isomax=isomax,
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
