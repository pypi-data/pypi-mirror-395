"""Pie chart implementation for VizForge."""

from typing import Any, Optional, Union
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from ..core.base import BaseChart
from ..core.theme import Theme


class PieChart(BaseChart):
    """
    Pie chart visualization.

    Supports pie charts, donut charts, and sunburst charts for hierarchical data.
    """

    def __init__(
        self,
        data: Optional[Union[pd.DataFrame, dict, list]] = None,
        values: Optional[Union[str, list, np.ndarray]] = None,
        names: Optional[Union[str, list, np.ndarray]] = None,
        title: Optional[str] = None,
        theme: Optional[Union[str, Theme]] = None,
        hole: float = 0.0,
        **kwargs
    ):
        """
        Create a pie chart.

        Args:
            data: Data source (DataFrame, dict, or list)
            values: Values data or column name
            names: Names/labels data or column name
            title: Chart title
            theme: Theme name or Theme object
            hole: Size of center hole (0.0 for pie, 0.3-0.5 for donut)
            **kwargs: Additional arguments

        Example:
            >>> pie = PieChart(data=df, values='market_share', names='company')
            >>> pie.show()
        """
        super().__init__(title=title, theme=theme, **kwargs)
        self.hole = hole

        if data is not None:
            self.plot(data, values, names)

    def plot(
        self,
        data: Union[pd.DataFrame, dict, list],
        values: Optional[Union[str, list, np.ndarray]] = None,
        names: Optional[Union[str, list, np.ndarray]] = None,
        **kwargs
    ) -> 'PieChart':
        """
        Plot data on the chart.

        Args:
            data: Data source
            values: Values data or column name
            names: Names/labels data or column name
            **kwargs: Additional trace arguments

        Returns:
            Self for method chaining
        """
        # Create figure if not exists
        if self.fig is None:
            self.fig = self._create_figure()

        # Parse data
        values_data, names_data = self._parse_data(data, values, names)

        # Add pie trace
        self.fig.add_trace(
            go.Pie(
                values=values_data,
                labels=names_data,
                hole=self.hole,
                marker=dict(
                    colors=self._theme.color_palette,
                    line=dict(color='white', width=2)
                ),
                textposition='inside',
                textinfo='percent+label',
                **kwargs
            )
        )

        return self

    def _parse_data(
        self,
        data: Union[pd.DataFrame, dict, list],
        values: Optional[Union[str, list, np.ndarray]],
        names: Optional[Union[str, list, np.ndarray]]
    ) -> tuple[Any, Any]:
        """Parse different data formats into values and names."""

        if isinstance(data, pd.DataFrame):
            values_data = data[values].values if isinstance(values, str) else values
            names_data = data[names].values if isinstance(names, str) else names

            return values_data, names_data

        elif isinstance(data, dict):
            if isinstance(values, str) and isinstance(names, str):
                values_data = data[values]
                names_data = data[names]
            else:
                # Assume dict is {name: value}
                names_data = list(data.keys())
                values_data = list(data.values())

            return values_data, names_data

        else:
            return values, names


def pie(
    data: Union[pd.DataFrame, dict, list],
    values: Optional[Union[str, list, np.ndarray]] = None,
    names: Optional[Union[str, list, np.ndarray]] = None,
    title: Optional[str] = None,
    theme: Optional[Union[str, Theme]] = None,
    hole: float = 0.0,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> PieChart:
    """
    Create and display a pie chart (convenience function).

    Args:
        data: Data source (DataFrame, dict, or list)
        values: Values data or column name
        names: Names/labels data or column name
        title: Chart title
        theme: Theme name or Theme object
        hole: Size of center hole (0.0 for pie, 0.3-0.5 for donut)
        show: Whether to display the chart
        export: Export filename (optional)
        **kwargs: Additional arguments

    Returns:
        PieChart object

    Example:
        >>> pie(df, values='market_share', names='company', title='Market Share')
        >>> pie({'A': 30, 'B': 25, 'C': 45}, title='Distribution')
        >>> pie(df, values='revenue', names='product', hole=0.4)  # Donut chart
    """
    chart = PieChart(
        data=data,
        values=values,
        names=names,
        title=title,
        theme=theme,
        hole=hole,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart


def donut(
    data: Union[pd.DataFrame, dict, list],
    values: Optional[Union[str, list, np.ndarray]] = None,
    names: Optional[Union[str, list, np.ndarray]] = None,
    title: Optional[str] = None,
    theme: Optional[Union[str, Theme]] = None,
    hole: float = 0.4,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> PieChart:
    """
    Create and display a donut chart (convenience function).

    Args:
        data: Data source (DataFrame, dict, or list)
        values: Values data or column name
        names: Names/labels data or column name
        title: Chart title
        theme: Theme name or Theme object
        hole: Size of center hole (default: 0.4)
        show: Whether to display the chart
        export: Export filename (optional)
        **kwargs: Additional arguments

    Returns:
        PieChart object

    Example:
        >>> donut(df, values='market_share', names='company', title='Market Share')
    """
    return pie(
        data=data,
        values=values,
        names=names,
        title=title,
        theme=theme,
        hole=hole,
        show=show,
        export=export,
        **kwargs
    )
