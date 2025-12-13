"""Treemap implementation for VizForge."""

from typing import Optional, List, Union
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from ...core.base import BaseChart
from ...core.theme import Theme


class Treemap(BaseChart):
    """
    Treemap visualization.

    Shows hierarchical data as nested rectangles.
    Perfect for disk usage, budget allocation, market share analysis.

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>>
        >>> # Market share
        >>> df = pd.DataFrame({
        >>>     'category': ['Tech', 'Tech', 'Finance', 'Finance'],
        >>>     'company': ['Apple', 'Google', 'JPM', 'Goldman'],
        >>>     'value': [2000, 1500, 800, 600]
        >>> })
        >>>
        >>> vz.treemap(df, labels='company', parents='category',
        >>>           values='value', title='Market Share')
    """

    def __init__(
        self,
        data: Union[pd.DataFrame, Dict],
        labels: str,
        parents: str,
        values: Optional[str] = None,
        colors: Optional[str] = None,
        colorscale: str = 'Viridis',
        title: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize Treemap.

        Args:
            data: DataFrame with hierarchical data
            labels: Column for labels
            parents: Column for parent labels
            values: Column for values (sizes)
            colors: Column for colors
            colorscale: Color scale
            title: Chart title
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        if isinstance(data, dict):
            data = pd.DataFrame(data)

        self.data = data
        self.labels = labels
        self.parents = parents
        self.values = values
        self.colors = colors
        self.colorscale = colorscale

    def create_trace(self) -> go.Treemap:
        """Create treemap trace."""
        treemap = go.Treemap(
            labels=self.data[self.labels],
            parents=self.data[self.parents],
            values=self.data[self.values] if self.values else None,
            marker=dict(
                colors=self.data[self.colors] if self.colors else None,
                colorscale=self.colorscale if self.colors else None,
                showscale=True if self.colors else False
            ),
            textposition="middle center",
            hovertemplate='<b>%{label}</b><br>Value: %{value}<extra></extra>'
        )
        return treemap

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure."""
        trace = self.create_trace()

        layout = go.Layout(
            title=self.title,
            **self._get_theme_layout()
        )

        fig = go.Figure(data=[trace], layout=layout)
        return fig


def treemap(
    data: Union[pd.DataFrame, Dict],
    labels: str,
    parents: str,
    values: Optional[str] = None,
    colors: Optional[str] = None,
    colorscale: str = 'Viridis',
    title: Optional[str] = None,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> Treemap:
    """
    Create a treemap.

    Args:
        data: DataFrame
        labels: Labels column
        parents: Parents column
        values: Values column
        colors: Colors column
        colorscale: Color scale
        title: Chart title
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        Treemap instance

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>>
        >>> # Budget allocation
        >>> df = pd.DataFrame({
        >>>     'label': ['Budget', 'Marketing', 'R&D', 'Operations',
        >>>              'Digital', 'TV', 'Software', 'Hardware'],
        >>>     'parent': ['', 'Budget', 'Budget', 'Budget',
        >>>               'Marketing', 'Marketing', 'R&D', 'R&D'],
        >>>     'value': [1000, 300, 400, 300, 180, 120, 250, 150]
        >>> })
        >>>
        >>> vz.treemap(df, labels='label', parents='parent',
        >>>           values='value', title='Budget Breakdown')
    """
    chart = Treemap(
        data=data,
        labels=labels,
        parents=parents,
        values=values,
        colors=colors,
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
