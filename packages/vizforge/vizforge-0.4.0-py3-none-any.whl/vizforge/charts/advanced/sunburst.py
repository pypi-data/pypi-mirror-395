"""Sunburst Chart implementation for VizForge."""

from typing import Optional, List, Union
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from ...core.base import BaseChart
from ...core.theme import Theme


class Sunburst(BaseChart):
    """
    Sunburst Chart visualization.

    Shows hierarchical data as concentric rings.
    Perfect for disk usage, budget allocation, organizational structure.

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>>
        >>> # Department structure
        >>> df = pd.DataFrame({
        >>>     'label': ['Company', 'Engineering', 'Sales', 'Frontend', 'Backend'],
        >>>     'parent': ['', 'Company', 'Company', 'Engineering', 'Engineering'],
        >>>     'value': [100, 50, 50, 25, 25]
        >>> })
        >>>
        >>> vz.sunburst(df, labels='label', parents='parent',
        >>>            values='value', title='Organization')
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
        Initialize Sunburst Chart.

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

    def create_trace(self) -> go.Sunburst:
        """Create sunburst trace."""
        sunburst = go.Sunburst(
            labels=self.data[self.labels],
            parents=self.data[self.parents],
            values=self.data[self.values] if self.values else None,
            marker=dict(
                colors=self.data[self.colors] if self.colors else None,
                colorscale=self.colorscale if self.colors else None,
                showscale=True if self.colors else False,
                line=dict(width=2, color='white')
            ),
            hovertemplate='<b>%{label}</b><br>Value: %{value}<br>Percent: %{percentParent}<extra></extra>',
            branchvalues="total"
        )
        return sunburst

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure."""
        trace = self.create_trace()

        layout = go.Layout(
            title=self.title,
            **self._get_theme_layout()
        )

        fig = go.Figure(data=[trace], layout=layout)
        return fig


def sunburst(
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
) -> Sunburst:
    """
    Create a sunburst chart.

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
        Sunburst instance

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>>
        >>> # File system usage
        >>> df = pd.DataFrame({
        >>>     'path': ['/', '/home', '/var', '/home/user', '/var/log'],
        >>>     'parent': ['', '/', '/', '/home', '/var'],
        >>>     'size': [1000, 600, 400, 500, 300]
        >>> })
        >>>
        >>> vz.sunburst(df, labels='path', parents='parent',
        >>>            values='size', title='Disk Usage')
    """
    chart = Sunburst(
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
