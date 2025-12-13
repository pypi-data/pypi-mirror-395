"""Cone plot implementation for VizForge."""

from typing import Optional, Union, List
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from ...core.base import BaseChart
from ...core.theme import Theme


class ConePlot(BaseChart):
    """
    3D Cone plot visualization (vector field).

    Creates 3D vector field visualizations using cones.
    Perfect for fluid dynamics, electromagnetic fields, and wind patterns.

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>>
        >>> # Vector field
        >>> x, y, z = np.mgrid[-1:1:8j, -1:1:8j, -1:1:8j]
        >>> u = -y
        >>> v = x
        >>> w = np.zeros_like(x)
        >>>
        >>> vz.cone(x, y, z, u, v, w, title='Rotation Field')
    """

    def __init__(
        self,
        x: Union[np.ndarray, List],
        y: Union[np.ndarray, List],
        z: Union[np.ndarray, List],
        u: Union[np.ndarray, List],
        v: Union[np.ndarray, List],
        w: Union[np.ndarray, List],
        title: Optional[str] = None,
        colorscale: str = "Viridis",
        sizemode: str = "absolute",
        sizeref: float = 1.0,
        **kwargs
    ):
        """
        Initialize Cone plot.

        Args:
            x: X positions
            y: Y positions
            z: Z positions
            u: X component of vector
            v: Y component of vector
            w: Z component of vector
            title: Chart title
            colorscale: Color scale
            sizemode: 'absolute' or 'scaled'
            sizeref: Size reference value
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        self.x = x
        self.y = y
        self.z = z
        self.u = u
        self.v = v
        self.w = w
        self.colorscale = colorscale
        self.sizemode = sizemode
        self.sizeref = sizeref

    def create_trace(self) -> go.Cone:
        """Create Plotly Cone trace."""

        trace = go.Cone(
            x=self.x.flatten() if hasattr(self.x, 'flatten') else self.x,
            y=self.y.flatten() if hasattr(self.y, 'flatten') else self.y,
            z=self.z.flatten() if hasattr(self.z, 'flatten') else self.z,
            u=self.u.flatten() if hasattr(self.u, 'flatten') else self.u,
            v=self.v.flatten() if hasattr(self.v, 'flatten') else self.v,
            w=self.w.flatten() if hasattr(self.w, 'flatten') else self.w,
            colorscale=self.colorscale,
            sizemode=self.sizemode,
            sizeref=self.sizeref,
            name=self.title or "Cone"
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
                aspectmode='data'
            ),
            **self._get_theme_layout()
        )

        fig = go.Figure(data=[trace], layout=layout)
        return fig


def cone(
    x: Union[np.ndarray, List],
    y: Union[np.ndarray, List],
    z: Union[np.ndarray, List],
    u: Union[np.ndarray, List],
    v: Union[np.ndarray, List],
    w: Union[np.ndarray, List],
    title: Optional[str] = None,
    colorscale: str = "Viridis",
    sizemode: str = "absolute",
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> ConePlot:
    """
    Create a 3D cone (vector field) plot.

    Args:
        x: X positions
        y: Y positions
        z: Z positions
        u: X vector components
        v: Y vector components
        w: Z vector components
        title: Chart title
        colorscale: Color scale
        sizemode: 'absolute' or 'scaled'
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        ConePlot instance

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>>
        >>> # Circular flow
        >>> x, y, z = np.mgrid[-1:1:10j, -1:1:10j, -1:1:10j]
        >>> u = -y
        >>> v = x
        >>> w = np.zeros_like(x)
        >>>
        >>> vz.cone(x, y, z, u, v, w, title='Circular Flow')
    """
    chart = ConePlot(
        x=x, y=y, z=z, u=u, v=v, w=w,
        title=title,
        colorscale=colorscale,
        sizemode=sizemode,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart
