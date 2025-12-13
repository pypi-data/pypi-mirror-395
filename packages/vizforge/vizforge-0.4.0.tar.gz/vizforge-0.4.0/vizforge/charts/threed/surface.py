"""3D Surface plot implementation for VizForge."""

from typing import Optional, Union, List
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from ...core.base import BaseChart
from ...core.theme import Theme


class SurfacePlot(BaseChart):
    """
    3D Surface plot visualization.

    Creates 3D surface plots from matrix data or function evaluations.
    Ideal for visualizing mathematical functions, terrain data, or any 2D grid data.

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>>
        >>> # Create mesh grid
        >>> x = np.linspace(-5, 5, 50)
        >>> y = np.linspace(-5, 5, 50)
        >>> X, Y = np.meshgrid(x, y)
        >>> Z = np.sin(np.sqrt(X**2 + Y**2))
        >>>
        >>> # Create surface plot
        >>> vz.surface(X, Y, Z, title='3D Surface')
    """

    def __init__(
        self,
        x: Union[np.ndarray, List],
        y: Union[np.ndarray, List],
        z: Union[np.ndarray, List, pd.DataFrame],
        title: Optional[str] = None,
        colorscale: str = "Viridis",
        show_colorbar: bool = True,
        contours: bool = False,
        opacity: float = 1.0,
        lighting: Optional[dict] = None,
        **kwargs
    ):
        """
        Initialize 3D Surface plot.

        Args:
            x: X coordinates (1D array or meshgrid)
            y: Y coordinates (1D array or meshgrid)
            z: Z values (2D array/matrix)
            title: Chart title
            colorscale: Color scale name
            show_colorbar: Whether to show color bar
            contours: Whether to show contour lines
            opacity: Surface opacity (0-1)
            lighting: Custom lighting dict
            **kwargs: Additional Plotly surface arguments
        """
        super().__init__(title=title, **kwargs)

        self.x = x
        self.y = y
        self.z = z
        self.colorscale = colorscale
        self.show_colorbar = show_colorbar
        self.contours = contours
        self.opacity = opacity
        self.lighting = lighting or {
            'ambient': 0.4,
            'diffuse': 0.5,
            'fresnel': 0.2,
            'specular': 0.05,
            'roughness': 0.5
        }

    def create_trace(self) -> go.Surface:
        """Create Plotly Surface trace."""

        contours_dict = {}
        if self.contours:
            contours_dict = {
                'z': {'show': True, 'usecolormap': True, 'highlightcolor': "limegreen", 'project': {'z': True}}
            }

        trace = go.Surface(
            x=self.x,
            y=self.y,
            z=self.z,
            colorscale=self.colorscale,
            showscale=self.show_colorbar,
            opacity=self.opacity,
            lighting=self.lighting,
            contours=contours_dict if contours_dict else None,
            name=self.title or "Surface"
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


def surface(
    x: Union[np.ndarray, List],
    y: Union[np.ndarray, List],
    z: Union[np.ndarray, List, pd.DataFrame],
    title: Optional[str] = None,
    colorscale: str = "Viridis",
    show_colorbar: bool = True,
    contours: bool = False,
    opacity: float = 1.0,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> SurfacePlot:
    """
    Create a 3D surface plot.

    Args:
        x: X coordinates
        y: Y coordinates
        z: Z values (2D matrix)
        title: Chart title
        colorscale: Color scale ('Viridis', 'Plasma', 'Rainbow', etc.)
        show_colorbar: Show color bar
        contours: Show contour lines
        opacity: Surface opacity (0-1)
        theme: Theme name
        show: Whether to display chart immediately
        export: Export path (if provided)
        **kwargs: Additional arguments

    Returns:
        SurfacePlot instance

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>>
        >>> # Mathematical function
        >>> x = np.linspace(-5, 5, 50)
        >>> y = np.linspace(-5, 5, 50)
        >>> X, Y = np.meshgrid(x, y)
        >>> Z = np.sin(np.sqrt(X**2 + Y**2))
        >>>
        >>> vz.surface(X, Y, Z, title='Sine Wave Surface')
        >>>
        >>> # With contours
        >>> vz.surface(X, Y, Z, contours=True, colorscale='Plasma')
    """
    chart = SurfacePlot(
        x=x, y=y, z=z,
        title=title,
        colorscale=colorscale,
        show_colorbar=show_colorbar,
        contours=contours,
        opacity=opacity,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart
