"""Radar (spider) chart implementation for VizForge."""

from typing import Optional, Union
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from ..core.base import BaseChart
from ..core.theme import Theme


class RadarChart(BaseChart):
    """
    Radar (spider/star) chart visualization.

    Multivariate data on radial axes, useful for comparing multiple variables.
    """

    def __init__(
        self,
        data: Optional[Union[pd.DataFrame, dict]] = None,
        r: Optional[Union[str, list, np.ndarray]] = None,
        theta: Optional[Union[str, list]] = None,
        title: Optional[str] = None,
        theme: Optional[Union[str, Theme]] = None,
        fill: str = "toself",
        **kwargs
    ):
        """
        Create a radar chart.

        Args:
            data: Data source
            r: Radial values or column name
            theta: Angular categories or column name
            title: Chart title
            theme: Theme
            fill: Fill mode ('toself', 'tonext', 'none')
            **kwargs: Additional arguments
        """
        super().__init__(title=title, theme=theme, **kwargs)
        self.fill = fill

        if data is not None:
            self.plot(data, r, theta)

    def plot(
        self,
        data: Union[pd.DataFrame, dict],
        r: Optional[Union[str, list, np.ndarray]] = None,
        theta: Optional[Union[str, list]] = None,
        name: Optional[str] = None,
        **kwargs
    ) -> 'RadarChart':
        """Plot radar chart data."""
        if self.fig is None:
            self.fig = self._create_figure()

        # Parse data
        r_data, theta_data = self._parse_data(data, r, theta)

        trace_kwargs = {
            'fill': self.fill,
            'line': {'width': self._theme.line_width},
        }
        trace_kwargs.update(kwargs)

        self.fig.add_trace(
            go.Scatterpolar(
                r=r_data,
                theta=theta_data,
                name=name or "radar",
                **trace_kwargs
            )
        )

        # Update layout for radar
        self.fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    gridcolor=self._theme.grid_color,
                )
            )
        )

        return self

    def _parse_data(self, data, r, theta):
        """Parse data into r, theta."""
        if isinstance(data, pd.DataFrame):
            if isinstance(r, str) and isinstance(theta, str):
                r_data = data[r].values
                theta_data = data[theta].values
            elif r is None and theta is None:
                # Use all columns as categories
                r_data = data.iloc[0].values
                theta_data = list(data.columns)
            else:
                r_data = r
                theta_data = theta
            return r_data, theta_data

        elif isinstance(data, dict):
            if r is None and theta is None:
                # Dict format: {category: value}
                theta_data = list(data.keys())
                r_data = list(data.values())
            else:
                r_data = data[r] if isinstance(r, str) else r
                theta_data = data[theta] if isinstance(theta, str) else theta
            return r_data, theta_data

        else:
            return r, theta


def radar(
    data: Union[pd.DataFrame, dict],
    r: Optional[Union[str, list, np.ndarray]] = None,
    theta: Optional[Union[str, list]] = None,
    title: Optional[str] = None,
    theme: Optional[Union[str, Theme]] = None,
    fill: str = "toself",
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> RadarChart:
    """
    Create radar chart (convenience function).

    Example:
        >>> # Dict format
        >>> radar({'Speed': 8, 'Power': 6, 'Defense': 7, 'Magic': 9})
        >>>
        >>> # DataFrame format
        >>> radar(df, r='value', theta='category', title='Performance')
    """
    chart = RadarChart(
        data=data,
        r=r,
        theta=theta,
        title=title,
        theme=theme,
        fill=fill,
        **kwargs
    )

    if export:
        chart.export(export)
    if show:
        chart.show()

    return chart
