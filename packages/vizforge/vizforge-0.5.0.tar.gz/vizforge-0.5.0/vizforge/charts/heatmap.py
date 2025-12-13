"""Heatmap implementation for VizForge."""

from typing import Optional, Union
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from ..core.base import BaseChart
from ..core.theme import Theme


class Heatmap(BaseChart):
    """
    Heatmap visualization.

    Color-coded matrix, useful for correlation matrices, pivot tables, etc.
    """

    def __init__(
        self,
        data: Optional[Union[pd.DataFrame, np.ndarray, list]] = None,
        x: Optional[Union[str, list]] = None,
        y: Optional[Union[str, list]] = None,
        z: Optional[Union[str, np.ndarray]] = None,
        title: Optional[str] = None,
        theme: Optional[Union[str, Theme]] = None,
        colorscale: str = "Viridis",
        show_values: bool = False,
        **kwargs
    ):
        """
        Create a heatmap.

        Args:
            data: Data source (DataFrame, 2D array, or dict)
            x: X-axis labels or column name
            y: Y-axis labels or column name
            z: Values (2D array) or column name
            title: Chart title
            theme: Theme name or Theme object
            colorscale: Color scale ('Viridis', 'RdBu', 'Greens', etc.)
            show_values: Whether to show values in cells
            **kwargs: Additional arguments
        """
        super().__init__(title=title, theme=theme, **kwargs)
        self.colorscale = colorscale
        self.show_values = show_values

        if data is not None:
            self.plot(data, x, y, z)

    def plot(
        self,
        data: Union[pd.DataFrame, np.ndarray, list],
        x: Optional[Union[str, list]] = None,
        y: Optional[Union[str, list]] = None,
        z: Optional[Union[str, np.ndarray]] = None,
        **kwargs
    ) -> 'Heatmap':
        """Plot heatmap data."""
        if self.fig is None:
            self.fig = self._create_figure()

        # Parse data
        x_data, y_data, z_data = self._parse_data(data, x, y, z)

        # Create heatmap trace
        trace_kwargs = {
            'colorscale': self.colorscale,
            'showscale': True,
        }

        if self.show_values:
            trace_kwargs['text'] = z_data
            trace_kwargs['texttemplate'] = '%{text:.2f}'

        trace_kwargs.update(kwargs)

        self.fig.add_trace(
            go.Heatmap(
                x=x_data,
                y=y_data,
                z=z_data,
                **trace_kwargs
            )
        )

        # Adjust layout for better heatmap display
        self.fig.update_layout(
            xaxis={'side': 'bottom'},
            yaxis={'scaleanchor': 'x'}
        )

        return self

    def _parse_data(self, data, x, y, z):
        """Parse data into x, y, z format."""
        if isinstance(data, pd.DataFrame):
            if z is None:
                # Treat DataFrame as matrix
                z_data = data.values
                x_data = list(data.columns)
                y_data = list(data.index)
            else:
                # Pivot table format
                if isinstance(x, str) and isinstance(y, str) and isinstance(z, str):
                    pivot = data.pivot(index=y, columns=x, values=z)
                    z_data = pivot.values
                    x_data = list(pivot.columns)
                    y_data = list(pivot.index)
                else:
                    z_data = data[z].values if isinstance(z, str) else z
                    x_data = data[x].values if isinstance(x, str) else x
                    y_data = data[y].values if isinstance(y, str) else y

            return x_data, y_data, z_data

        elif isinstance(data, np.ndarray):
            z_data = data
            x_data = x if x is not None else list(range(data.shape[1]))
            y_data = y if y is not None else list(range(data.shape[0]))
            return x_data, y_data, z_data

        elif isinstance(data, list):
            z_data = np.array(data)
            x_data = x if x is not None else list(range(len(data[0])))
            y_data = y if y is not None else list(range(len(data)))
            return x_data, y_data, z_data

        else:
            return x, y, z


def heatmap(
    data: Union[pd.DataFrame, np.ndarray, list],
    x: Optional[Union[str, list]] = None,
    y: Optional[Union[str, list]] = None,
    z: Optional[Union[str, np.ndarray]] = None,
    title: Optional[str] = None,
    theme: Optional[Union[str, Theme]] = None,
    colorscale: str = "Viridis",
    show_values: bool = False,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> Heatmap:
    """
    Create heatmap (convenience function).

    Args:
        data: Data source
        x: X-axis labels
        y: Y-axis labels
        z: Values matrix
        title: Chart title
        theme: Theme
        colorscale: Color scale
        show_values: Show values in cells
        show: Display chart
        export: Export filename
        **kwargs: Additional arguments

    Returns:
        Heatmap object

    Example:
        >>> # Correlation matrix
        >>> heatmap(df.corr(), title='Correlation Matrix', colorscale='RdBu')
        >>>
        >>> # Custom heatmap
        >>> heatmap(data, x='month', y='product', z='sales', show_values=True)
    """
    chart = Heatmap(
        data=data,
        x=x,
        y=y,
        z=z,
        title=title,
        theme=theme,
        colorscale=colorscale,
        show_values=show_values,
        **kwargs
    )

    if export:
        chart.export(export)
    if show:
        chart.show()

    return chart
