"""Boxplot implementation for VizForge."""

from typing import Optional, Union
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from ...core.base import BaseChart
from ...core.theme import Theme


class Boxplot(BaseChart):
    """
    Boxplot (box-and-whisker) visualization.

    Shows distribution quartiles, median, and outliers.
    """

    def __init__(
        self,
        data: Optional[Union[pd.DataFrame, dict, list]] = None,
        x: Optional[Union[str, list, np.ndarray]] = None,
        y: Optional[Union[str, list, np.ndarray]] = None,
        title: Optional[str] = None,
        theme: Optional[Union[str, Theme]] = None,
        orientation: str = "v",
        **kwargs
    ):
        """
        Create a boxplot.

        Args:
            data: Data source
            x: Categories (for grouped boxplots)
            y: Values
            title: Chart title
            theme: Theme
            orientation: 'v' (vertical) or 'h' (horizontal)
            **kwargs: Additional arguments
        """
        super().__init__(title=title, theme=theme, **kwargs)
        self.orientation = orientation

        if data is not None:
            self.plot(data, x, y)

    def plot(
        self,
        data: Union[pd.DataFrame, dict, list],
        x: Optional[Union[str, list, np.ndarray]] = None,
        y: Optional[Union[str, list, np.ndarray]] = None,
        name: Optional[str] = None,
        **kwargs
    ) -> 'Boxplot':
        """Plot boxplot data."""
        if self.fig is None:
            self.fig = self._create_figure()

        # Parse data
        x_data, y_data = self._parse_data(data, x, y)

        trace_kwargs = {
            'marker': {'color': self._theme.primary_color},
            'boxmean': 'sd',  # Show mean and standard deviation
        }
        trace_kwargs.update(kwargs)

        if self.orientation == "v":
            self.fig.add_trace(
                go.Box(
                    x=x_data,
                    y=y_data,
                    name=name or "boxplot",
                    **trace_kwargs
                )
            )
        else:
            self.fig.add_trace(
                go.Box(
                    x=y_data,
                    y=x_data,
                    name=name or "boxplot",
                    orientation='h',
                    **trace_kwargs
                )
            )

        return self

    def _parse_data(self, data, x, y):
        """Parse data into x, y."""
        if isinstance(data, pd.DataFrame):
            if y is None:
                # Single boxplot
                x_data = None
                y_data = data[x].values if isinstance(x, str) else x
            else:
                # Grouped boxplots
                x_data = data[x].values if isinstance(x, str) else x
                y_data = data[y].values if isinstance(y, str) else y
            return x_data, y_data

        elif isinstance(data, (list, np.ndarray)):
            return None, data

        else:
            return x, y


def boxplot(
    data: Union[pd.DataFrame, dict, list],
    x: Optional[Union[str, list, np.ndarray]] = None,
    y: Optional[Union[str, list, np.ndarray]] = None,
    title: Optional[str] = None,
    theme: Optional[Union[str, Theme]] = None,
    orientation: str = "v",
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> Boxplot:
    """
    Create boxplot (convenience function).

    Example:
        >>> # Single boxplot
        >>> boxplot(df, x='values', title='Value Distribution')
        >>>
        >>> # Grouped boxplots
        >>> boxplot(df, x='category', y='values', title='Values by Category')
    """
    chart = Boxplot(
        data=data,
        x=x,
        y=y,
        title=title,
        theme=theme,
        orientation=orientation,
        **kwargs
    )

    if export:
        chart.export(export)
    if show:
        chart.show()

    return chart
