"""3D Scatter plot implementation for VizForge."""

from typing import Optional, Union, List
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from ...core.base import BaseChart
from ...core.theme import Theme


class Scatter3D(BaseChart):
    """
    3D Scatter plot visualization.

    Creates 3D scatter plots with optional size and color encoding.
    Perfect for exploring multi-dimensional data relationships.

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>>
        >>> df = pd.DataFrame({
        >>>     'x': np.random.randn(100),
        >>>     'y': np.random.randn(100),
        >>>     'z': np.random.randn(100),
        >>>     'size': np.random.randint(5, 20, 100)
        >>> })
        >>>
        >>> vz.scatter3d(df, x='x', y='y', z='z', size='size')
    """

    def __init__(
        self,
        data: Union[pd.DataFrame, dict, None] = None,
        x: Optional[Union[str, List, np.ndarray]] = None,
        y: Optional[Union[str, List, np.ndarray]] = None,
        z: Optional[Union[str, List, np.ndarray]] = None,
        size: Optional[Union[str, List, np.ndarray]] = None,
        color: Optional[Union[str, List, np.ndarray]] = None,
        text: Optional[Union[str, List, np.ndarray]] = None,
        title: Optional[str] = None,
        marker_size: int = 8,
        colorscale: str = "Viridis",
        opacity: float = 0.8,
        **kwargs
    ):
        """
        Initialize 3D Scatter plot.

        Args:
            data: DataFrame or dict containing data
            x: X column name or values
            y: Y column name or values
            z: Z column name or values
            size: Size column name or values
            color: Color column name or values
            text: Text column name or values (for hover)
            title: Chart title
            marker_size: Default marker size
            colorscale: Color scale name
            opacity: Marker opacity (0-1)
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        self.data = data
        self.x_col = x
        self.y_col = y
        self.z_col = z
        self.size_col = size
        self.color_col = color
        self.text_col = text
        self.marker_size = marker_size
        self.colorscale = colorscale
        self.opacity = opacity

        # Extract actual values
        self.x_vals, self.y_vals, self.z_vals = self._extract_xyz()
        self.size_vals = self._extract_values(size)
        self.color_vals = self._extract_values(color)
        self.text_vals = self._extract_values(text)

    def _extract_xyz(self):
        """Extract x, y, z values from data or direct input."""
        if isinstance(self.data, pd.DataFrame):
            x = self.data[self.x_col].values if isinstance(self.x_col, str) else self.x_col
            y = self.data[self.y_col].values if isinstance(self.y_col, str) else self.y_col
            z = self.data[self.z_col].values if isinstance(self.z_col, str) else self.z_col
        else:
            x = self.x_col
            y = self.y_col
            z = self.z_col

        return x, y, z

    def _extract_values(self, col):
        """Extract values for size/color/text."""
        if col is None:
            return None

        if isinstance(self.data, pd.DataFrame) and isinstance(col, str):
            return self.data[col].values
        else:
            return col

    def create_trace(self) -> go.Scatter3d:
        """Create Plotly Scatter3d trace."""

        marker_dict = {
            'size': self.size_vals if self.size_vals is not None else self.marker_size,
            'opacity': self.opacity
        }

        if self.color_vals is not None:
            marker_dict['color'] = self.color_vals
            marker_dict['colorscale'] = self.colorscale
            marker_dict['showscale'] = True

        trace = go.Scatter3d(
            x=self.x_vals,
            y=self.y_vals,
            z=self.z_vals,
            mode='markers',
            marker=marker_dict,
            text=self.text_vals,
            name=self.title or "Scatter3D"
        )

        return trace

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure."""
        trace = self.create_trace()

        layout = go.Layout(
            title=self.title,
            scene=dict(
                xaxis=dict(title=str(self.x_col) if isinstance(self.x_col, str) else "X"),
                yaxis=dict(title=str(self.y_col) if isinstance(self.y_col, str) else "Y"),
                zaxis=dict(title=str(self.z_col) if isinstance(self.z_col, str) else "Z")
            ),
            **self._get_theme_layout()
        )

        fig = go.Figure(data=[trace], layout=layout)
        return fig


def scatter3d(
    data: Union[pd.DataFrame, dict, None] = None,
    x: Optional[Union[str, List, np.ndarray]] = None,
    y: Optional[Union[str, List, np.ndarray]] = None,
    z: Optional[Union[str, List, np.ndarray]] = None,
    size: Optional[Union[str, List, np.ndarray]] = None,
    color: Optional[Union[str, List, np.ndarray]] = None,
    text: Optional[Union[str, List, np.ndarray]] = None,
    title: Optional[str] = None,
    marker_size: int = 8,
    colorscale: str = "Viridis",
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> Scatter3D:
    """
    Create a 3D scatter plot.

    Args:
        data: DataFrame or dict
        x: X column or values
        y: Y column or values
        z: Z column or values
        size: Size column or values
        color: Color column or values
        text: Text column or values
        title: Chart title
        marker_size: Default marker size
        colorscale: Color scale
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        Scatter3D instance

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>> import numpy as np
        >>>
        >>> # Basic 3D scatter
        >>> df = pd.DataFrame({
        >>>     'x': np.random.randn(100),
        >>>     'y': np.random.randn(100),
        >>>     'z': np.random.randn(100)
        >>> })
        >>> vz.scatter3d(df, x='x', y='y', z='z')
        >>>
        >>> # With color and size
        >>> df['category'] = np.random.choice(['A', 'B', 'C'], 100)
        >>> df['value'] = np.random.randint(5, 20, 100)
        >>> vz.scatter3d(df, x='x', y='y', z='z',
        >>>              color='category', size='value')
    """
    chart = Scatter3D(
        data=data, x=x, y=y, z=z,
        size=size, color=color, text=text,
        title=title,
        marker_size=marker_size,
        colorscale=colorscale,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart
