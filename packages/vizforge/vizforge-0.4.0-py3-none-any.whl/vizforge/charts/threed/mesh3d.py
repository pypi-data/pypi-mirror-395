"""3D Mesh plot implementation for VizForge."""

from typing import Optional, Union, List
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from ...core.base import BaseChart
from ...core.theme import Theme


class Mesh3D(BaseChart):
    """
    3D Mesh plot visualization.

    Creates 3D mesh plots from vertices and faces.
    Perfect for 3D geometry, CAD models, and molecular structures.

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>>
        >>> # Create a cube
        >>> vertices = [[0,0,0], [1,0,0], [1,1,0], [0,1,0],
        >>>             [0,0,1], [1,0,1], [1,1,1], [0,1,1]]
        >>> faces = [[0,1,2], [0,2,3], [0,1,5], [0,5,4],
        >>>          [0,3,7], [0,7,4], [6,5,1], [6,1,2],
        >>>          [6,2,3], [6,3,7], [6,7,4], [6,4,5]]
        >>>
        >>> vz.mesh3d(vertices, faces, title='3D Cube')
    """

    def __init__(
        self,
        vertices: Union[List, np.ndarray],
        faces: Optional[Union[List, np.ndarray]] = None,
        x: Optional[Union[List, np.ndarray]] = None,
        y: Optional[Union[List, np.ndarray]] = None,
        z: Optional[Union[List, np.ndarray]] = None,
        i: Optional[Union[List, np.ndarray]] = None,
        j: Optional[Union[List, np.ndarray]] = None,
        k: Optional[Union[List, np.ndarray]] = None,
        title: Optional[str] = None,
        colorscale: str = "Viridis",
        opacity: float = 0.8,
        flatshading: bool = False,
        **kwargs
    ):
        """
        Initialize 3D Mesh plot.

        Args:
            vertices: List of [x, y, z] vertices or separate x/y/z arrays
            faces: List of triangular faces (indices into vertices)
            x: X coordinates (alternative to vertices)
            y: Y coordinates
            z: Z coordinates
            i: Face indices (i component)
            j: Face indices (j component)
            k: Face indices (k component)
            title: Chart title
            colorscale: Color scale
            opacity: Mesh opacity (0-1)
            flatshading: Use flat shading
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        # Extract coordinates
        if vertices is not None and x is None:
            vertices = np.array(vertices)
            self.x = vertices[:, 0]
            self.y = vertices[:, 1]
            self.z = vertices[:, 2]
        else:
            self.x = x
            self.y = y
            self.z = z

        # Extract face indices
        if faces is not None and i is None:
            faces = np.array(faces)
            self.i = faces[:, 0]
            self.j = faces[:, 1]
            self.k = faces[:, 2]
        else:
            self.i = i
            self.j = j
            self.k = k

        self.colorscale = colorscale
        self.opacity = opacity
        self.flatshading = flatshading

    def create_trace(self) -> go.Mesh3d:
        """Create Plotly Mesh3d trace."""

        trace = go.Mesh3d(
            x=self.x,
            y=self.y,
            z=self.z,
            i=self.i,
            j=self.j,
            k=self.k,
            colorscale=self.colorscale,
            opacity=self.opacity,
            flatshading=self.flatshading,
            name=self.title or "Mesh3D"
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


def mesh3d(
    vertices: Union[List, np.ndarray],
    faces: Optional[Union[List, np.ndarray]] = None,
    title: Optional[str] = None,
    colorscale: str = "Viridis",
    opacity: float = 0.8,
    flatshading: bool = False,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> Mesh3D:
    """
    Create a 3D mesh plot.

    Args:
        vertices: Array of [x, y, z] coordinates
        faces: Array of triangular face indices
        title: Chart title
        colorscale: Color scale
        opacity: Mesh opacity (0-1)
        flatshading: Use flat shading
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        Mesh3D instance

    Examples:
        >>> import vizforge as vz
        >>>
        >>> # Cube vertices
        >>> vertices = [
        >>>     [0,0,0], [1,0,0], [1,1,0], [0,1,0],
        >>>     [0,0,1], [1,0,1], [1,1,1], [0,1,1]
        >>> ]
        >>>
        >>> # Cube faces (triangles)
        >>> faces = [
        >>>     [0,1,2], [0,2,3],  # bottom
        >>>     [4,5,6], [4,6,7],  # top
        >>>     [0,1,5], [0,5,4],  # front
        >>>     [2,3,7], [2,7,6],  # back
        >>>     [0,3,7], [0,7,4],  # left
        >>>     [1,2,6], [1,6,5]   # right
        >>> ]
        >>>
        >>> vz.mesh3d(vertices, faces, title='3D Cube')
    """
    chart = Mesh3D(
        vertices=vertices,
        faces=faces,
        title=title,
        colorscale=colorscale,
        opacity=opacity,
        flatshading=flatshading,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart
