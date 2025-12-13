"""Histogram implementation for VizForge."""

from typing import Optional, Union
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from ..core.base import BaseChart
from ..core.theme import Theme


class Histogram(BaseChart):
    """
    Histogram visualization.

    Distribution of numerical data using bins.
    """

    def __init__(
        self,
        data: Optional[Union[pd.DataFrame, list, np.ndarray]] = None,
        x: Optional[Union[str, list, np.ndarray]] = None,
        title: Optional[str] = None,
        theme: Optional[Union[str, Theme]] = None,
        nbins: Optional[int] = None,
        cumulative: bool = False,
        **kwargs
    ):
        """
        Create a histogram.

        Args:
            data: Data source
            x: Data column or array
            title: Chart title
            theme: Theme
            nbins: Number of bins
            cumulative: Cumulative histogram
            **kwargs: Additional arguments
        """
        super().__init__(title=title, theme=theme, **kwargs)
        self.nbins = nbins
        self.cumulative = cumulative

        if data is not None:
            self.plot(data, x)

    def plot(
        self,
        data: Union[pd.DataFrame, list, np.ndarray],
        x: Optional[Union[str, list, np.ndarray]] = None,
        name: Optional[str] = None,
        **kwargs
    ) -> 'Histogram':
        """Plot histogram data."""
        if self.fig is None:
            self.fig = self._create_figure()

        # Parse data
        x_data = self._parse_data(data, x)

        trace_kwargs = {
            'marker': {'color': self._theme.primary_color},
        }

        if self.nbins:
            trace_kwargs['nbinsx'] = self.nbins

        if self.cumulative:
            trace_kwargs['cumulative'] = {'enabled': True}

        trace_kwargs.update(kwargs)

        self.fig.add_trace(
            go.Histogram(
                x=x_data,
                name=name or "histogram",
                **trace_kwargs
            )
        )

        return self

    def _parse_data(self, data, x):
        """Parse data into array."""
        if isinstance(data, pd.DataFrame):
            return data[x].values if isinstance(x, str) else x
        elif isinstance(data, (list, np.ndarray)):
            return data
        else:
            return x


def histogram(
    data: Union[pd.DataFrame, list, np.ndarray],
    x: Optional[Union[str, list, np.ndarray]] = None,
    title: Optional[str] = None,
    theme: Optional[Union[str, Theme]] = None,
    nbins: Optional[int] = None,
    cumulative: bool = False,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> Histogram:
    """
    Create histogram (convenience function).

    Example:
        >>> histogram(df, x='age', title='Age Distribution', nbins=20)
        >>> histogram(df['price'], title='Price Distribution')
    """
    chart = Histogram(
        data=data,
        x=x,
        title=title,
        theme=theme,
        nbins=nbins,
        cumulative=cumulative,
        **kwargs
    )

    if export:
        chart.export(export)
    if show:
        chart.show()

    return chart
