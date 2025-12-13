"""Real-time Streaming Chart implementation for VizForge."""

from typing import Optional, List, Dict, Callable, Union
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

from ...core.base import BaseChart
from ...core.theme import Theme


class StreamingLine(BaseChart):
    """
    Real-time Streaming Line Chart.

    Continuously updates with new data points in real-time.
    Perfect for live monitoring, sensor data, stock prices, system metrics.

    Examples:
        >>> import vizforge as vz
        >>> import time
        >>>
        >>> # Create streaming chart
        >>> chart = vz.streaming_line(
        >>>     data_source=lambda: np.random.randn(),
        >>>     window_size=100,
        >>>     update_interval=100,  # ms
        >>>     title='Live Sensor Data'
        >>> )
    """

    def __init__(
        self,
        data_source: Optional[Callable] = None,
        initial_data: Optional[Union[List, pd.Series]] = None,
        window_size: int = 100,
        update_interval: int = 1000,  # milliseconds
        x_label: str = 'Time',
        y_label: str = 'Value',
        line_color: str = '#3498db',
        fill_area: bool = False,
        title: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize Streaming Line Chart.

        Args:
            data_source: Callable that returns new data point
            initial_data: Initial data to display
            window_size: Number of points to display
            update_interval: Update interval in milliseconds
            x_label: X-axis label
            y_label: Y-axis label
            line_color: Line color
            fill_area: Fill area under line
            title: Chart title
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        self.data_source = data_source
        self.window_size = window_size
        self.update_interval = update_interval
        self.x_label = x_label
        self.y_label = y_label
        self.line_color = line_color
        self.fill_area = fill_area

        # Initialize data buffers
        if initial_data is not None:
            self.y_data = list(initial_data)[-window_size:]
        else:
            self.y_data = []

        self.x_data = list(range(len(self.y_data)))

    def add_point(self, value: float):
        """Add new data point to the stream."""
        self.y_data.append(value)
        self.x_data.append(len(self.x_data))

        # Keep only window_size points
        if len(self.y_data) > self.window_size:
            self.y_data = self.y_data[-self.window_size:]
            self.x_data = list(range(len(self.y_data)))

    def create_trace(self) -> go.Scatter:
        """Create Plotly Scatter trace."""
        trace = go.Scatter(
            x=self.x_data,
            y=self.y_data,
            mode='lines+markers',
            line=dict(color=self.line_color, width=2),
            marker=dict(size=4, color=self.line_color),
            fill='tozeroy' if self.fill_area else None,
            fillcolor=f'rgba({int(self.line_color[1:3], 16)}, '
                      f'{int(self.line_color[3:5], 16)}, '
                      f'{int(self.line_color[5:7], 16)}, 0.2)' if self.fill_area else None,
            name='Stream'
        )
        return trace

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure with animation."""
        trace = self.create_trace()

        layout = go.Layout(
            title=self.title,
            xaxis=dict(
                title=self.x_label,
                range=[0, self.window_size] if self.window_size else None
            ),
            yaxis=dict(title=self.y_label),
            hovermode='x unified',
            **self._get_theme_layout()
        )

        fig = go.Figure(data=[trace], layout=layout)

        # Add update menu for play/pause
        fig.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    direction="left",
                    buttons=[
                        dict(
                            args=[None, {"frame": {"duration": self.update_interval, "redraw": True}}],
                            label="▶ Play",
                            method="animate"
                        ),
                        dict(
                            args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                            label="⏸ Pause",
                            method="animate"
                        )
                    ],
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.11,
                    xanchor="left",
                    y=1.15,
                    yanchor="top"
                )
            ]
        )

        return fig


class LiveHeatmap(BaseChart):
    """
    Real-time Live Heatmap.

    Updates heatmap data in real-time.
    Perfect for correlation matrices, network traffic, system load.
    """

    def __init__(
        self,
        data_source: Optional[Callable] = None,
        initial_data: Optional[np.ndarray] = None,
        colorscale: str = 'Viridis',
        update_interval: int = 1000,
        title: Optional[str] = None,
        **kwargs
    ):
        """Initialize Live Heatmap."""
        super().__init__(title=title, **kwargs)

        self.data_source = data_source
        self.colorscale = colorscale
        self.update_interval = update_interval

        if initial_data is not None:
            self.data = initial_data
        else:
            self.data = np.zeros((10, 10))

    def update_data(self, new_data: np.ndarray):
        """Update heatmap data."""
        self.data = new_data

    def create_trace(self) -> go.Heatmap:
        """Create Plotly Heatmap trace."""
        heatmap = go.Heatmap(
            z=self.data,
            colorscale=self.colorscale,
            hovertemplate='Row: %{y}<br>Col: %{x}<br>Value: %{z}<extra></extra>'
        )
        return heatmap

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure."""
        trace = self.create_trace()

        layout = go.Layout(
            title=self.title,
            **self._get_theme_layout()
        )

        fig = go.Figure(data=[trace], layout=layout)
        return fig


def streaming_line(
    data_source: Optional[Callable] = None,
    initial_data: Optional[Union[List, pd.Series]] = None,
    window_size: int = 100,
    update_interval: int = 1000,
    x_label: str = 'Time',
    y_label: str = 'Value',
    line_color: str = '#3498db',
    fill_area: bool = False,
    title: Optional[str] = None,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> StreamingLine:
    """
    Create a real-time streaming line chart.

    Args:
        data_source: Function that returns new data point
        initial_data: Initial data
        window_size: Display window size
        update_interval: Update interval (ms)
        x_label: X-axis label
        y_label: Y-axis label
        line_color: Line color
        fill_area: Fill area under line
        title: Chart title
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        StreamingLine instance

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>>
        >>> # Stock price monitor
        >>> def get_price():
        >>>     return 100 + np.random.randn() * 5
        >>>
        >>> chart = vz.streaming_line(
        >>>     data_source=get_price,
        >>>     window_size=200,
        >>>     update_interval=500,
        >>>     title='Live Stock Price',
        >>>     fill_area=True
        >>> )
    """
    chart = StreamingLine(
        data_source=data_source,
        initial_data=initial_data,
        window_size=window_size,
        update_interval=update_interval,
        x_label=x_label,
        y_label=y_label,
        line_color=line_color,
        fill_area=fill_area,
        title=title,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart


def live_heatmap(
    data_source: Optional[Callable] = None,
    initial_data: Optional[np.ndarray] = None,
    colorscale: str = 'Viridis',
    update_interval: int = 1000,
    title: Optional[str] = None,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> LiveHeatmap:
    """
    Create a real-time live heatmap.

    Args:
        data_source: Function that returns new heatmap data
        initial_data: Initial data
        colorscale: Color scale
        update_interval: Update interval (ms)
        title: Chart title
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        LiveHeatmap instance

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>>
        >>> # Network traffic monitor
        >>> def get_traffic():
        >>>     return np.random.rand(10, 10) * 100
        >>>
        >>> chart = vz.live_heatmap(
        >>>     data_source=get_traffic,
        >>>     title='Network Traffic Monitor'
        >>> )
    """
    chart = LiveHeatmap(
        data_source=data_source,
        initial_data=initial_data,
        colorscale=colorscale,
        update_interval=update_interval,
        title=title,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart
