"""Violin Plot implementation for VizForge."""

from typing import Optional, List, Union
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from ...core.base import BaseChart
from ...core.theme import Theme


class ViolinPlot(BaseChart):
    """
    Violin Plot visualization.

    Shows distribution of data with kernel density estimation.
    Perfect for comparing distributions, statistical analysis, A/B testing.

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>> import numpy as np
        >>>
        >>> # Compare distributions
        >>> df = pd.DataFrame({
        >>>     'group': ['A']*100 + ['B']*100 + ['C']*100,
        >>>     'value': np.concatenate([
        >>>         np.random.normal(100, 15, 100),
        >>>         np.random.normal(120, 20, 100),
        >>>         np.random.normal(110, 10, 100)
        >>>     ])
        >>> })
        >>>
        >>> vz.violin(df, x='group', y='value', title='Group Comparison')
    """

    def __init__(
        self,
        data: Union[pd.DataFrame, Dict],
        x: Optional[str] = None,
        y: Optional[str] = None,
        color: Optional[str] = None,
        box_visible: bool = True,
        points: str = 'outliers',  # 'all', 'outliers', False
        title: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize Violin Plot.

        Args:
            data: DataFrame or dict
            x: X-axis column (categories)
            y: Y-axis column (values)
            color: Color column
            box_visible: Show box plot inside violin
            points: Show points ('all', 'outliers', False)
            title: Chart title
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        self.data = data
        self.x = x
        self.y = y
        self.color = color
        self.box_visible = box_visible
        self.points = points

    def create_figure(self) -> go.Figure:
        """Create Plotly violin plot."""
        fig = px.violin(
            self.data,
            x=self.x,
            y=self.y,
            color=self.color,
            box=self.box_visible,
            points=self.points,
            title=self.title
        )

        # Apply theme
        fig.update_layout(**self._get_theme_layout())

        return fig


def violin(
    data: Union[pd.DataFrame, Dict],
    x: Optional[str] = None,
    y: Optional[str] = None,
    color: Optional[str] = None,
    box_visible: bool = True,
    points: str = 'outliers',
    title: Optional[str] = None,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> ViolinPlot:
    """
    Create a violin plot.

    Args:
        data: DataFrame or dict
        x: X-axis column
        y: Y-axis column
        color: Color column
        box_visible: Show box plot
        points: Show points setting
        title: Chart title
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        ViolinPlot instance

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>> import numpy as np
        >>>
        >>> # A/B test results
        >>> df = pd.DataFrame({
        >>>     'variant': ['Control']*200 + ['Treatment']*200,
        >>>     'conversion_rate': np.concatenate([
        >>>         np.random.normal(0.05, 0.02, 200),
        >>>         np.random.normal(0.07, 0.02, 200)
        >>>     ])
        >>> })
        >>>
        >>> vz.violin(df, x='variant', y='conversion_rate',
        >>>          title='A/B Test Results', box_visible=True)
    """
    chart = ViolinPlot(
        data=data,
        x=x,
        y=y,
        color=color,
        box_visible=box_visible,
        points=points,
        title=title,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart
