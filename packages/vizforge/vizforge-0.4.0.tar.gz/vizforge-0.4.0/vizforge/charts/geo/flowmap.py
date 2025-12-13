"""Flow map implementation for VizForge."""

from typing import Optional, Union, List
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from ...core.base import BaseChart
from ...core.theme import Theme


class FlowMap(BaseChart):
    """
    Flow map visualization (Origin-Destination flows).

    Creates flow visualizations showing movement between locations.
    Perfect for migration, trade flows, commuting patterns.

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>>
        >>> # Migration flows
        >>> df = pd.DataFrame({
        >>>     'origin_lat': [40.7, 51.5, 35.7],
        >>>     'origin_lon': [-74.0, -0.1, 139.7],
        >>>     'dest_lat': [51.5, 35.7, -33.9],
        >>>     'dest_lon': [-0.1, 139.7, 151.2],
        >>>     'flow': [1000, 800, 600]
        >>> })
        >>>
        >>> vz.flowmap(df, origin_lat='origin_lat',
        >>>            origin_lon='origin_lon',
        >>>            dest_lat='dest_lat',
        >>>            dest_lon='dest_lon',
        >>>            flow='flow')
    """

    def __init__(
        self,
        data: Union[pd.DataFrame, dict, None] = None,
        origin_lat: Optional[Union[str, List, np.ndarray]] = None,
        origin_lon: Optional[Union[str, List, np.ndarray]] = None,
        dest_lat: Optional[Union[str, List, np.ndarray]] = None,
        dest_lon: Optional[Union[str, List, np.ndarray]] = None,
        flow: Optional[Union[str, List, np.ndarray]] = None,
        title: Optional[str] = None,
        line_color: str = 'blue',
        opacity: float = 0.6,
        scope: str = "world",
        projection: str = "natural earth",
        **kwargs
    ):
        """
        Initialize Flow map.

        Args:
            data: DataFrame or dict
            origin_lat: Origin latitude
            origin_lon: Origin longitude
            dest_lat: Destination latitude
            dest_lon: Destination longitude
            flow: Flow volume (for line width)
            title: Chart title
            line_color: Line color
            opacity: Line opacity
            scope: Map scope
            projection: Projection type
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        self.data = data
        self.line_color = line_color
        self.opacity = opacity
        self.scope = scope
        self.projection = projection

        # Extract values
        self.origin_lat_vals = self._extract_values(origin_lat)
        self.origin_lon_vals = self._extract_values(origin_lon)
        self.dest_lat_vals = self._extract_values(dest_lat)
        self.dest_lon_vals = self._extract_values(dest_lon)
        self.flow_vals = self._extract_values(flow)

        # Normalize flow for line width
        if self.flow_vals is not None:
            max_flow = np.max(self.flow_vals)
            self.flow_widths = (self.flow_vals / max_flow) * 5 + 1  # 1-6 range
        else:
            self.flow_widths = [2] * len(self.origin_lat_vals)

    def _extract_values(self, col):
        """Extract values from DataFrame or direct input."""
        if col is None:
            return None

        if isinstance(self.data, pd.DataFrame) and isinstance(col, str):
            return self.data[col].values
        else:
            return col

    def create_trace(self) -> List[go.Scattergeo]:
        """Create Plotly Scattergeo traces for flows."""

        traces = []

        for i in range(len(self.origin_lat_vals)):
            # Flow line
            trace = go.Scattergeo(
                lat=[self.origin_lat_vals[i], self.dest_lat_vals[i]],
                lon=[self.origin_lon_vals[i], self.dest_lon_vals[i]],
                mode='lines',
                line=dict(
                    width=self.flow_widths[i],
                    color=self.line_color
                ),
                opacity=self.opacity,
                showlegend=False
            )
            traces.append(trace)

            # Destination marker
            marker_trace = go.Scattergeo(
                lat=[self.dest_lat_vals[i]],
                lon=[self.dest_lon_vals[i]],
                mode='markers',
                marker=dict(
                    size=self.flow_widths[i] * 2,
                    color=self.line_color,
                    symbol='arrow',
                    angleref='previous'
                ),
                opacity=self.opacity,
                showlegend=False
            )
            traces.append(marker_trace)

        return traces

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure."""
        traces = self.create_trace()

        layout = go.Layout(
            title=self.title,
            geo=dict(
                scope=self.scope,
                projection=dict(type=self.projection),
                showland=True,
                landcolor='rgb(243, 243, 243)',
                coastlinecolor='rgb(204, 204, 204)'
            ),
            **self._get_theme_layout()
        )

        fig = go.Figure(data=traces, layout=layout)
        return fig


def flowmap(
    data: Union[pd.DataFrame, dict, None] = None,
    origin_lat: Optional[Union[str, List, np.ndarray]] = None,
    origin_lon: Optional[Union[str, List, np.ndarray]] = None,
    dest_lat: Optional[Union[str, List, np.ndarray]] = None,
    dest_lon: Optional[Union[str, List, np.ndarray]] = None,
    flow: Optional[Union[str, List, np.ndarray]] = None,
    title: Optional[str] = None,
    line_color: str = 'blue',
    opacity: float = 0.6,
    scope: str = "world",
    projection: str = "natural earth",
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> FlowMap:
    """
    Create a flow map (origin-destination flows).

    Args:
        data: DataFrame or dict
        origin_lat: Origin latitude
        origin_lon: Origin longitude
        dest_lat: Destination latitude
        dest_lon: Destination longitude
        flow: Flow volume
        title: Chart title
        line_color: Line color
        opacity: Line opacity
        scope: Map scope
        projection: Projection type
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        FlowMap instance

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>>
        >>> # Trade flows
        >>> df = pd.DataFrame({
        >>>     'from_city': ['NYC', 'London', 'Tokyo'],
        >>>     'from_lat': [40.7, 51.5, 35.7],
        >>>     'from_lon': [-74.0, -0.1, 139.7],
        >>>     'to_city': ['London', 'Tokyo', 'Sydney'],
        >>>     'to_lat': [51.5, 35.7, -33.9],
        >>>     'to_lon': [-0.1, 139.7, 151.2],
        >>>     'volume': [5000, 3000, 2000]
        >>> })
        >>>
        >>> vz.flowmap(df,
        >>>            origin_lat='from_lat',
        >>>            origin_lon='from_lon',
        >>>            dest_lat='to_lat',
        >>>            dest_lon='to_lon',
        >>>            flow='volume',
        >>>            title='Global Trade Flows')
    """
    chart = FlowMap(
        data=data,
        origin_lat=origin_lat,
        origin_lon=origin_lon,
        dest_lat=dest_lat,
        dest_lon=dest_lon,
        flow=flow,
        title=title,
        line_color=line_color,
        opacity=opacity,
        scope=scope,
        projection=projection,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart
