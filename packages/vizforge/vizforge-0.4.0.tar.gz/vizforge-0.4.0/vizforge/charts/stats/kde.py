"""KDE (Kernel Density Estimation) Plot implementation for VizForge."""

from typing import Optional, List, Union
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats

from ...core.base import BaseChart
from ...core.theme import Theme


class KDEPlot(BaseChart):
    """
    Kernel Density Estimation Plot.

    Shows smooth probability density estimation of data.
    Perfect for distribution analysis, comparing groups, outlier detection.

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>>
        >>> # Single distribution
        >>> data = np.random.normal(100, 15, 1000)
        >>> vz.kde(data, title='Response Time Distribution')
    """

    def __init__(
        self,
        data: Union[np.ndarray, pd.Series, List],
        bandwidth: Optional[float] = None,
        fill: bool = True,
        rug: bool = False,
        title: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize KDE Plot.

        Args:
            data: Data array or series
            bandwidth: KDE bandwidth (None for auto)
            fill: Fill area under curve
            rug: Show rug plot (individual points)
            title: Chart title
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        self.data = np.array(data).flatten()
        self.bandwidth = bandwidth
        self.fill = fill
        self.rug = rug

        # Calculate KDE
        self.kde = stats.gaussian_kde(self.data, bw_method=self.bandwidth)
        self.x_range = np.linspace(self.data.min(), self.data.max(), 200)
        self.density = self.kde(self.x_range)

    def create_trace(self) -> List[go.Scatter]:
        """Create KDE trace."""
        traces = []

        # KDE curve
        kde_trace = go.Scatter(
            x=self.x_range,
            y=self.density,
            mode='lines',
            name='Density',
            line=dict(color='#3498db', width=2),
            fill='tozeroy' if self.fill else None,
            fillcolor='rgba(52, 152, 219, 0.3)' if self.fill else None
        )
        traces.append(kde_trace)

        # Rug plot (individual points)
        if self.rug:
            rug_trace = go.Scatter(
                x=self.data,
                y=np.zeros_like(self.data),
                mode='markers',
                name='Data Points',
                marker=dict(
                    symbol='line-ns',
                    size=10,
                    color='rgba(0, 0, 0, 0.3)',
                    line=dict(width=1)
                ),
                showlegend=False
            )
            traces.append(rug_trace)

        return traces

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure."""
        traces = self.create_trace()

        layout = go.Layout(
            title=self.title,
            xaxis=dict(title='Value'),
            yaxis=dict(title='Density'),
            hovermode='x unified',
            **self._get_theme_layout()
        )

        fig = go.Figure(data=traces, layout=layout)
        return fig


class KDE2D(BaseChart):
    """
    2D Kernel Density Estimation.

    Shows joint probability density of two variables.
    Perfect for bivariate analysis, correlation visualization.
    """

    def __init__(
        self,
        x: Union[np.ndarray, pd.Series, List],
        y: Union[np.ndarray, pd.Series, List],
        colorscale: str = 'Viridis',
        contours: bool = True,
        title: Optional[str] = None,
        **kwargs
    ):
        """Initialize 2D KDE Plot."""
        super().__init__(title=title, **kwargs)

        self.x = np.array(x).flatten()
        self.y = np.array(y).flatten()
        self.colorscale = colorscale
        self.contours = contours

    def create_trace(self) -> go.Histogram2dContour:
        """Create 2D KDE trace."""
        trace = go.Histogram2dContour(
            x=self.x,
            y=self.y,
            colorscale=self.colorscale,
            reversescale=False,
            showscale=True,
            contours=dict(
                showlabels=True,
                labelfont=dict(size=12, color='white')
            ) if self.contours else None
        )
        return trace

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure."""
        trace = self.create_trace()

        layout = go.Layout(
            title=self.title,
            xaxis=dict(title='X'),
            yaxis=dict(title='Y'),
            **self._get_theme_layout()
        )

        fig = go.Figure(data=[trace], layout=layout)
        return fig


def kde(
    data: Union[np.ndarray, pd.Series, List],
    bandwidth: Optional[float] = None,
    fill: bool = True,
    rug: bool = False,
    title: Optional[str] = None,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> KDEPlot:
    """
    Create a KDE plot.

    Args:
        data: Data array
        bandwidth: KDE bandwidth
        fill: Fill area
        rug: Show rug plot
        title: Chart title
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        KDEPlot instance

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>>
        >>> # Distribution comparison
        >>> data1 = np.random.normal(100, 15, 500)
        >>> data2 = np.random.normal(120, 20, 500)
        >>>
        >>> vz.kde(data1, title='Distribution A', fill=True, rug=True)
    """
    chart = KDEPlot(
        data=data,
        bandwidth=bandwidth,
        fill=fill,
        rug=rug,
        title=title,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart


def kde2d(
    x: Union[np.ndarray, pd.Series, List],
    y: Union[np.ndarray, pd.Series, List],
    colorscale: str = 'Viridis',
    contours: bool = True,
    title: Optional[str] = None,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> KDE2D:
    """
    Create a 2D KDE plot.

    Args:
        x: X data
        y: Y data
        colorscale: Color scale
        contours: Show contours
        title: Chart title
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        KDE2D instance

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>>
        >>> # Joint distribution
        >>> x = np.random.normal(0, 1, 1000)
        >>> y = x + np.random.normal(0, 0.5, 1000)
        >>>
        >>> vz.kde2d(x, y, title='Joint Distribution')
    """
    chart = KDE2D(
        x=x,
        y=y,
        colorscale=colorscale,
        contours=contours,
        title=title,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart
