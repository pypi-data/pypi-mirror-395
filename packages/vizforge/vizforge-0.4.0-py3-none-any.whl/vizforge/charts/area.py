"""Area chart implementation for VizForge."""

from typing import Optional, Union
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from ..core.base import BaseChart
from ..core.theme import Theme


class AreaChart(BaseChart):
    """
    Area chart visualization.

    Filled area under line, useful for showing cumulative values over time.
    """

    def __init__(
        self,
        data: Optional[Union[pd.DataFrame, dict, list]] = None,
        x: Optional[Union[str, list, np.ndarray]] = None,
        y: Optional[Union[str, list, np.ndarray]] = None,
        title: Optional[str] = None,
        theme: Optional[Union[str, Theme]] = None,
        stackgroup: Optional[str] = None,
        **kwargs
    ):
        """
        Create an area chart.

        Args:
            data: Data source
            x: X-axis data or column name
            y: Y-axis data or column name (can be list for stacked)
            title: Chart title
            theme: Theme name or Theme object
            stackgroup: Stack group name (for stacked area charts)
            **kwargs: Additional arguments
        """
        super().__init__(title=title, theme=theme, **kwargs)
        self.stackgroup = stackgroup

        if data is not None:
            self.plot(data, x, y)

    def plot(
        self,
        data: Union[pd.DataFrame, dict, list],
        x: Optional[Union[str, list, np.ndarray]] = None,
        y: Optional[Union[str, list, np.ndarray]] = None,
        name: Optional[str] = None,
        **kwargs
    ) -> 'AreaChart':
        """Plot area chart data."""
        if self.fig is None:
            self.fig = self._create_figure()

        # Parse data similar to LineChart
        x_data, y_data_list, names = self._parse_data(data, x, y, name)

        # Add area traces
        for y_data, trace_name in zip(y_data_list, names):
            trace_kwargs = {
                'fill': 'tozeroy',
                'line': {'width': self._theme.line_width},
                'marker': {'size': self._theme.marker_size},
            }

            if self.stackgroup:
                trace_kwargs['stackgroup'] = self.stackgroup

            trace_kwargs.update(kwargs)

            self.fig.add_trace(
                go.Scatter(
                    x=x_data,
                    y=y_data,
                    name=trace_name,
                    mode='lines',
                    **trace_kwargs
                )
            )

        return self

    def _parse_data(self, data, x, y, name):
        """Parse data into x, y, names."""
        if isinstance(data, pd.DataFrame):
            x_data = data[x].values if isinstance(x, str) else (x if x is not None else data.index.values)

            if isinstance(y, str):
                y_data_list = [data[y].values]
                names = [name or y]
            elif isinstance(y, list):
                y_data_list = [data[col].values for col in y]
                names = y
            else:
                y_data_list = [y]
                names = [name or "trace"]

            return x_data, y_data_list, names

        elif isinstance(data, dict):
            x_data = data[x] if isinstance(x, str) else x
            y_data_list = [data[y] if isinstance(y, str) else y]
            names = [name or (y if isinstance(y, str) else "trace")]
            return x_data, y_data_list, names

        else:
            return x, [y], [name or "trace"]


def area(
    data: Union[pd.DataFrame, dict, list],
    x: Optional[Union[str, list, np.ndarray]] = None,
    y: Optional[Union[str, list, np.ndarray]] = None,
    title: Optional[str] = None,
    theme: Optional[Union[str, Theme]] = None,
    stacked: bool = False,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> AreaChart:
    """
    Create area chart (convenience function).

    Args:
        data: Data source
        x: X-axis data
        y: Y-axis data
        title: Chart title
        theme: Theme
        stacked: Whether to stack areas
        show: Display chart
        export: Export filename
        **kwargs: Additional arguments

    Returns:
        AreaChart object

    Example:
        >>> area(df, x='date', y='sales', title='Sales Over Time')
        >>> area(df, x='date', y=['product_a', 'product_b'], stacked=True)
    """
    chart = AreaChart(
        data=data,
        x=x,
        y=y,
        title=title,
        theme=theme,
        stackgroup='one' if stacked else None,
        **kwargs
    )

    if export:
        chart.export(export)
    if show:
        chart.show()

    return chart
