"""Waterfall chart implementation for VizForge."""

from typing import Optional, Union
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from ..core.base import BaseChart
from ..core.theme import Theme


class WaterfallChart(BaseChart):
    """
    Waterfall chart visualization.

    Shows cumulative effect of sequential positive/negative values.
    """

    def __init__(
        self,
        data: Optional[Union[pd.DataFrame, dict]] = None,
        x: Optional[Union[str, list]] = None,
        y: Optional[Union[str, list, np.ndarray]] = None,
        title: Optional[str] = None,
        theme: Optional[Union[str, Theme]] = None,
        **kwargs
    ):
        """
        Create a waterfall chart.

        Args:
            data: Data source
            x: Categories or column name
            y: Values or column name
            title: Chart title
            theme: Theme
            **kwargs: Additional arguments
        """
        super().__init__(title=title, theme=theme, **kwargs)

        if data is not None:
            self.plot(data, x, y)

    def plot(
        self,
        data: Union[pd.DataFrame, dict],
        x: Optional[Union[str, list]] = None,
        y: Optional[Union[str, list, np.ndarray]] = None,
        **kwargs
    ) -> 'WaterfallChart':
        """Plot waterfall chart data."""
        if self.fig is None:
            self.fig = self._create_figure()

        # Parse data
        x_data, y_data = self._parse_data(data, x, y)

        # Determine measure types (relative, total, etc.)
        measures = self._determine_measures(y_data)

        trace_kwargs = {
            'increasing': {'marker': {'color': self._theme.success_color}},
            'decreasing': {'marker': {'color': self._theme.error_color}},
            'totals': {'marker': {'color': self._theme.primary_color}},
        }
        trace_kwargs.update(kwargs)

        self.fig.add_trace(
            go.Waterfall(
                x=x_data,
                y=y_data,
                measure=measures,
                **trace_kwargs
            )
        )

        return self

    def _parse_data(self, data, x, y):
        """Parse data into x, y."""
        if isinstance(data, pd.DataFrame):
            x_data = data[x].values if isinstance(x, str) else x
            y_data = data[y].values if isinstance(y, str) else y
            return list(x_data), list(y_data)

        elif isinstance(data, dict):
            if x is None and y is None:
                # Dict format: {category: value}
                x_data = list(data.keys())
                y_data = list(data.values())
            else:
                x_data = data[x] if isinstance(x, str) else x
                y_data = data[y] if isinstance(y, str) else y
            return x_data, y_data

        else:
            return x, y

    def _determine_measures(self, y_data):
        """Determine measure types (relative/total)."""
        # By default, all are relative except last (total)
        measures = ['relative'] * (len(y_data) - 1) + ['total']
        return measures


def waterfall(
    data: Union[pd.DataFrame, dict],
    x: Optional[Union[str, list]] = None,
    y: Optional[Union[str, list, np.ndarray]] = None,
    title: Optional[str] = None,
    theme: Optional[Union[str, Theme]] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> WaterfallChart:
    """
    Create waterfall chart (convenience function).

    Example:
        >>> # Financial analysis
        >>> data = {
        ...     'Revenue': 100,
        ...     'Costs': -30,
        ...     'Expenses': -20,
        ...     'Profit': 50
        ... }
        >>> waterfall(data, title='P&L Waterfall')
        >>>
        >>> # DataFrame format
        >>> waterfall(df, x='category', y='value', title='Sequential Changes')
    """
    chart = WaterfallChart(
        data=data,
        x=x,
        y=y,
        title=title,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)
    if show:
        chart.show()

    return chart
