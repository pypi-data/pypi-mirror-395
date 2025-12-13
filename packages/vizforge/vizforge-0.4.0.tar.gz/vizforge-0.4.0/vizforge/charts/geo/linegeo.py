"""Line geo map implementation for VizForge."""

from typing import Optional, Union, List
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from ...core.base import BaseChart
from ...core.theme import Theme


class LineGeoMap(BaseChart):
    """
    Line geo map visualization.

    Creates line plots on geographical maps.
    Perfect for flight routes, shipping lanes, migration paths.

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>>
        >>> # Flight routes
        >>> df = pd.DataFrame({
        >>>     'start_lat': [40.7, 51.5],
        >>>     'start_lon': [-74.0, -0.1],
        >>>     'end_lat': [35.7, -33.9],
        >>>     'end_lon': [139.7, 151.2]
        >>> })
        >>>
        >>> vz.linegeo(df, start_lat='start_lat', start_lon='start_lon',
        >>>            end_lat='end_lat', end_lon='end_lon')
    """

    def __init__(
        self,
        data: Union[pd.DataFrame, dict, None] = None,
        start_lat: Optional[Union[str, List, np.ndarray]] = None,
        start_lon: Optional[Union[str, List, np.ndarray]] = None,
        end_lat: Optional[Union[str, List, np.ndarray]] = None,
        end_lon: Optional[Union[str, List, np.ndarray]] = None,
        title: Optional[str] = None,
        line_width: int = 2,
        line_color: str = 'red',
        scope: str = "world",
        projection: str = "natural earth",
        **kwargs
    ):
        """
        Initialize Line Geo map.

        Args:
            data: DataFrame or dict
            start_lat: Start latitude
            start_lon: Start longitude
            end_lat: End latitude
            end_lon: End longitude
            title: Chart title
            line_width: Line width
            line_color: Line color
            scope: Map scope
            projection: Projection type
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        self.data = data
        self.line_width = line_width
        self.line_color = line_color
        self.scope = scope
        self.projection = projection

        # Extract values
        self.start_lat_vals = self._extract_values(start_lat)
        self.start_lon_vals = self._extract_values(start_lon)
        self.end_lat_vals = self._extract_values(end_lat)
        self.end_lon_vals = self._extract_values(end_lon)

    def _extract_values(self, col):
        """Extract values from DataFrame or direct input."""
        if col is None:
            return None

        if isinstance(self.data, pd.DataFrame) and isinstance(col, str):
            return self.data[col].values
        else:
            return col

    def create_trace(self) -> List[go.Scattergeo]:
        """Create Plotly Scattergeo traces for lines."""

        traces = []

        for i in range(len(self.start_lat_vals)):
            trace = go.Scattergeo(
                lat=[self.start_lat_vals[i], self.end_lat_vals[i]],
                lon=[self.start_lon_vals[i], self.end_lon_vals[i]],
                mode='lines',
                line=dict(width=self.line_width, color=self.line_color),
                showlegend=False
            )
            traces.append(trace)

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


def linegeo(
    data: Union[pd.DataFrame, dict, None] = None,
    start_lat: Optional[Union[str, List, np.ndarray]] = None,
    start_lon: Optional[Union[str, List, np.ndarray]] = None,
    end_lat: Optional[Union[str, List, np.ndarray]] = None,
    end_lon: Optional[Union[str, List, np.ndarray]] = None,
    title: Optional[str] = None,
    line_width: int = 2,
    line_color: str = 'red',
    scope: str = "world",
    projection: str = "natural earth",
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> LineGeoMap:
    """
    Create a line geo map (routes).

    Args:
        data: DataFrame or dict
        start_lat: Start latitude
        start_lon: Start longitude
        end_lat: End latitude
        end_lon: End longitude
        title: Chart title
        line_width: Line width
        line_color: Line color
        scope: Map scope
        projection: Projection type
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        LineGeoMap instance

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>>
        >>> # Flight routes
        >>> df = pd.DataFrame({
        >>>     'origin_lat': [40.7, 51.5, 35.7],
        >>>     'origin_lon': [-74.0, -0.1, 139.7],
        >>>     'dest_lat': [51.5, 35.7, -33.9],
        >>>     'dest_lon': [-0.1, 139.7, 151.2]
        >>> })
        >>>
        >>> vz.linegeo(df,
        >>>            start_lat='origin_lat',
        >>>            start_lon='origin_lon',
        >>>            end_lat='dest_lat',
        >>>            end_lon='dest_lon',
        >>>            title='Flight Routes')
    """
    chart = LineGeoMap(
        data=data,
        start_lat=start_lat,
        start_lon=start_lon,
        end_lat=end_lat,
        end_lon=end_lon,
        title=title,
        line_width=line_width,
        line_color=line_color,
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
