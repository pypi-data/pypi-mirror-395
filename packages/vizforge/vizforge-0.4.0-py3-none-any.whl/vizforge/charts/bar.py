"""Bar chart implementation for VizForge."""

from typing import Any, Optional, Union
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from ..core.base import BaseChart
from ..core.theme import Theme


class BarChart(BaseChart):
    """
    Bar chart visualization.

    Supports vertical and horizontal bars, grouped and stacked layouts.
    """

    def __init__(
        self,
        data: Optional[Union[pd.DataFrame, dict, list]] = None,
        x: Optional[Union[str, list, np.ndarray]] = None,
        y: Optional[Union[str, list, np.ndarray]] = None,
        title: Optional[str] = None,
        theme: Optional[Union[str, Theme]] = None,
        orientation: str = "v",
        barmode: str = "group",
        color: Optional[Union[str, list]] = None,
        **kwargs
    ):
        """
        Create a bar chart.

        Args:
            data: Data source (DataFrame, dict, or list)
            x: X-axis data or column name
            y: Y-axis data or column name
            title: Chart title
            theme: Theme name or Theme object
            orientation: 'v' for vertical, 'h' for horizontal
            barmode: 'group', 'stack', 'relative', or 'overlay'
            color: Column name for color grouping or list of colors
            **kwargs: Additional arguments

        Example:
            >>> bar = BarChart(data=df, x='category', y='value', title='Sales by Category')
            >>> bar.show()
        """
        super().__init__(title=title, theme=theme, **kwargs)
        self.orientation = orientation
        self.barmode = barmode
        self.color = color

        if data is not None:
            self.plot(data, x, y)

    def plot(
        self,
        data: Union[pd.DataFrame, dict, list],
        x: Optional[Union[str, list, np.ndarray]] = None,
        y: Optional[Union[str, list, np.ndarray]] = None,
        name: Optional[str] = None,
        **kwargs
    ) -> 'BarChart':
        """
        Plot data on the chart.

        Args:
            data: Data source
            x: X-axis data or column name
            y: Y-axis data or column name
            name: Series name
            **kwargs: Additional trace arguments

        Returns:
            Self for method chaining
        """
        # Create figure if not exists
        if self.fig is None:
            self.fig = self._create_figure()
            self.fig.update_layout(barmode=self.barmode)

        # Parse data
        if self.color and isinstance(data, pd.DataFrame) and isinstance(self.color, str):
            # Grouped bars by color column
            self._plot_grouped(data, x, y, self.color, **kwargs)
        else:
            # Simple bar chart
            x_data, y_data_list, names = self._parse_data(data, x, y, name)

            for y_data, trace_name in zip(y_data_list, names):
                if self.orientation == "v":
                    self.fig.add_trace(
                        go.Bar(
                            x=x_data,
                            y=y_data,
                            name=trace_name,
                            **kwargs
                        )
                    )
                else:
                    self.fig.add_trace(
                        go.Bar(
                            x=y_data,
                            y=x_data,
                            name=trace_name,
                            orientation='h',
                            **kwargs
                        )
                    )

        return self

    def _plot_grouped(
        self,
        data: pd.DataFrame,
        x: str,
        y: str,
        color: str,
        **kwargs
    ) -> None:
        """Plot grouped bars by color column."""
        groups = data[color].unique()

        for group in groups:
            group_data = data[data[color] == group]

            if self.orientation == "v":
                self.fig.add_trace(
                    go.Bar(
                        x=group_data[x],
                        y=group_data[y],
                        name=str(group),
                        **kwargs
                    )
                )
            else:
                self.fig.add_trace(
                    go.Bar(
                        x=group_data[y],
                        y=group_data[x],
                        name=str(group),
                        orientation='h',
                        **kwargs
                    )
                )

    def _parse_data(
        self,
        data: Union[pd.DataFrame, dict, list],
        x: Optional[Union[str, list, np.ndarray]],
        y: Optional[Union[str, list, np.ndarray]],
        name: Optional[str]
    ) -> tuple[Any, list[Any], list[str]]:
        """Parse different data formats into x, y, and names."""

        # Handle DataFrame
        if isinstance(data, pd.DataFrame):
            if isinstance(x, str):
                x_data = data[x].values
            elif x is None:
                x_data = data.index.values
            else:
                x_data = x

            if isinstance(y, str):
                y_data_list = [data[y].values]
                names = [name or y]
            elif isinstance(y, list) and all(isinstance(col, str) for col in y):
                # Multiple y columns
                y_data_list = [data[col].values for col in y]
                names = y if name is None else [f"{name} - {col}" for col in y]
            else:
                y_data_list = [y]
                names = [name or "trace"]

            return x_data, y_data_list, names

        # Handle dict
        elif isinstance(data, dict):
            if isinstance(x, str):
                x_data = data[x]
            else:
                x_data = x

            if isinstance(y, str):
                y_data_list = [data[y]]
                names = [name or y]
            elif isinstance(y, list) and all(isinstance(col, str) for col in y):
                y_data_list = [data[col] for col in y]
                names = y if name is None else [f"{name} - {col}" for col in y]
            else:
                y_data_list = [y]
                names = [name or "trace"]

            return x_data, y_data_list, names

        # Handle arrays/lists
        else:
            x_data = x
            y_data_list = [y]
            names = [name or "trace"]
            return x_data, y_data_list, names


def bar(
    data: Union[pd.DataFrame, dict, list],
    x: Optional[Union[str, list, np.ndarray]] = None,
    y: Optional[Union[str, list, np.ndarray]] = None,
    title: Optional[str] = None,
    theme: Optional[Union[str, Theme]] = None,
    orientation: str = "v",
    barmode: str = "group",
    color: Optional[Union[str, list]] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> BarChart:
    """
    Create and display a bar chart (convenience function).

    Args:
        data: Data source (DataFrame, dict, or list)
        x: X-axis data or column name
        y: Y-axis data or column name
        title: Chart title
        theme: Theme name or Theme object
        orientation: 'v' for vertical, 'h' for horizontal
        barmode: 'group', 'stack', 'relative', or 'overlay'
        color: Column name for color grouping
        show: Whether to display the chart
        export: Export filename (optional)
        **kwargs: Additional arguments

    Returns:
        BarChart object

    Example:
        >>> bar(df, x='category', y='value', title='Sales by Category')
        >>> bar(df, x='month', y='revenue', color='region', barmode='stack')
    """
    chart = BarChart(
        data=data,
        x=x,
        y=y,
        title=title,
        theme=theme,
        orientation=orientation,
        barmode=barmode,
        color=color,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart
