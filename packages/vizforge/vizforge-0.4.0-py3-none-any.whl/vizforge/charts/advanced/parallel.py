"""Parallel Coordinates Plot implementation for VizForge."""

from typing import Optional, List, Union
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from ...core.base import BaseChart
from ...core.theme import Theme


class ParallelCoordinates(BaseChart):
    """
    Parallel Coordinates Plot.

    Shows multivariate data with parallel axes.
    Perfect for high-dimensional data visualization, clustering, outlier detection.

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>> import numpy as np
        >>>
        >>> # Multi-feature analysis
        >>> df = pd.DataFrame({
        >>>     'feature1': np.random.randn(100),
        >>>     'feature2': np.random.randn(100),
        >>>     'feature3': np.random.randn(100),
        >>>     'feature4': np.random.randn(100),
        >>>     'class': np.random.choice(['A', 'B', 'C'], 100)
        >>> })
        >>>
        >>> vz.parallel_coordinates(df, color='class',
        >>>                        title='Multi-dimensional Analysis')
    """

    def __init__(
        self,
        data: pd.DataFrame,
        dimensions: Optional[List[str]] = None,
        color: Optional[str] = None,
        colorscale: str = 'Viridis',
        title: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize Parallel Coordinates.

        Args:
            data: DataFrame
            dimensions: List of dimension columns (None = all numeric)
            color: Column for coloring lines
            colorscale: Color scale
            title: Chart title
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        self.data = data

        # Auto-detect numeric columns if dimensions not specified
        if dimensions is None:
            self.dimensions = data.select_dtypes(include=[np.number]).columns.tolist()
        else:
            self.dimensions = dimensions

        self.color = color
        self.colorscale = colorscale

    def create_trace(self) -> go.Parcoords:
        """Create parallel coordinates trace."""
        # Build dimension specs
        dims = []
        for col in self.dimensions:
            dims.append(dict(
                label=col,
                values=self.data[col]
            ))

        # Color configuration
        if self.color:
            if self.data[self.color].dtype == 'object':
                # Categorical color - convert to numeric
                color_map = {val: i for i, val in enumerate(self.data[self.color].unique())}
                color_values = self.data[self.color].map(color_map)
            else:
                color_values = self.data[self.color]

            line = dict(
                color=color_values,
                colorscale=self.colorscale,
                showscale=True,
                cmin=color_values.min(),
                cmax=color_values.max()
            )
        else:
            line = dict(color='blue')

        parcoords = go.Parcoords(
            dimensions=dims,
            line=line
        )

        return parcoords

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure."""
        trace = self.create_trace()

        layout = go.Layout(
            title=self.title,
            **self._get_theme_layout()
        )

        fig = go.Figure(data=[trace], layout=layout)
        return fig


def parallel_coordinates(
    data: pd.DataFrame,
    dimensions: Optional[List[str]] = None,
    color: Optional[str] = None,
    colorscale: str = 'Viridis',
    title: Optional[str] = None,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> ParallelCoordinates:
    """
    Create a parallel coordinates plot.

    Args:
        data: DataFrame
        dimensions: Dimension columns
        color: Color column
        colorscale: Color scale
        title: Chart title
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        ParallelCoordinates instance

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>> from sklearn.datasets import load_iris
        >>>
        >>> # Iris dataset
        >>> iris = load_iris()
        >>> df = pd.DataFrame(iris.data, columns=iris.feature_names)
        >>> df['species'] = iris.target
        >>>
        >>> vz.parallel_coordinates(
        >>>     df,
        >>>     dimensions=iris.feature_names,
        >>>     color='species',
        >>>     title='Iris Dataset Analysis'
        >>> )
    """
    chart = ParallelCoordinates(
        data=data,
        dimensions=dimensions,
        color=color,
        colorscale=colorscale,
        title=title,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart
