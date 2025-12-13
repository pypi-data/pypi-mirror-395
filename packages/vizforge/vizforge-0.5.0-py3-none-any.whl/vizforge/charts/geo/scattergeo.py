"""Scatter geo map implementation for VizForge."""

from typing import Optional, Union, List
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from ...core.base import BaseChart
from ...core.theme import Theme


class ScatterGeoMap(BaseChart):
    """
    Scatter geo map visualization.

    Creates scatter plots on geographical maps.
    Perfect for showing city locations, earthquake data, store locations.

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>>
        >>> # City locations
        >>> df = pd.DataFrame({
        >>>     'city': ['NYC', 'LA', 'Chicago'],
        >>>     'lat': [40.7, 34.0, 41.9],
        >>>     'lon': [-74.0, -118.2, -87.6],
        >>>     'pop': [8.3, 3.9, 2.7]
        >>> })
        >>>
        >>> vz.scattergeo(df, lat='lat', lon='lon', size='pop')
    """

    def __init__(
        self,
        data: Union[pd.DataFrame, dict, None] = None,
        lat: Optional[Union[str, List, np.ndarray]] = None,
        lon: Optional[Union[str, List, np.ndarray]] = None,
        size: Optional[Union[str, List, np.ndarray]] = None,
        color: Optional[Union[str, List, np.ndarray]] = None,
        text: Optional[Union[str, List, np.ndarray]] = None,
        title: Optional[str] = None,
        marker_size: int = 8,
        colorscale: str = "Viridis",
        scope: str = "world",
        projection: str = "natural earth",
        **kwargs
    ):
        """
        Initialize Scatter Geo map.

        Args:
            data: DataFrame or dict
            lat: Latitude column or values
            lon: Longitude column or values
            size: Size column or values
            color: Color column or values
            text: Text column or values
            title: Chart title
            marker_size: Default marker size
            colorscale: Color scale
            scope: Map scope
            projection: Projection type
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        self.data = data
        self.lat_col = lat
        self.lon_col = lon
        self.size_col = size
        self.color_col = color
        self.text_col = text
        self.marker_size = marker_size
        self.colorscale = colorscale
        self.scope = scope
        self.projection = projection

        # Extract values
        self.lat_vals = self._extract_values(lat)
        self.lon_vals = self._extract_values(lon)
        self.size_vals = self._extract_values(size)
        self.color_vals = self._extract_values(color)
        self.text_vals = self._extract_values(text)

    def _extract_values(self, col):
        """Extract values from DataFrame or direct input."""
        if col is None:
            return None

        if isinstance(self.data, pd.DataFrame) and isinstance(col, str):
            return self.data[col].values
        else:
            return col

    def create_trace(self) -> go.Scattergeo:
        """Create Plotly Scattergeo trace."""

        marker_dict = {
            'size': self.size_vals if self.size_vals is not None else self.marker_size,
        }

        if self.color_vals is not None:
            marker_dict['color'] = self.color_vals
            marker_dict['colorscale'] = self.colorscale
            marker_dict['showscale'] = True

        trace = go.Scattergeo(
            lat=self.lat_vals,
            lon=self.lon_vals,
            mode='markers',
            marker=marker_dict,
            text=self.text_vals,
            name=self.title or "ScatterGeo"
        )

        return trace

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure."""
        trace = self.create_trace()

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

        fig = go.Figure(data=[trace], layout=layout)
        return fig


def scattergeo(
    data: Union[pd.DataFrame, dict, None] = None,
    lat: Optional[Union[str, List, np.ndarray]] = None,
    lon: Optional[Union[str, List, np.ndarray]] = None,
    size: Optional[Union[str, List, np.ndarray]] = None,
    color: Optional[Union[str, List, np.ndarray]] = None,
    text: Optional[Union[str, List, np.ndarray]] = None,
    title: Optional[str] = None,
    marker_size: int = 8,
    colorscale: str = "Viridis",
    scope: str = "world",
    projection: str = "natural earth",
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> ScatterGeoMap:
    """
    Create a scatter geo map.

    Args:
        data: DataFrame or dict
        lat: Latitude column or values
        lon: Longitude column or values
        size: Size column or values
        color: Color column or values
        text: Text/labels
        title: Chart title
        marker_size: Default marker size
        colorscale: Color scale
        scope: Map scope
        projection: Projection type
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        ScatterGeoMap instance

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>>
        >>> # Major cities
        >>> df = pd.DataFrame({
        >>>     'city': ['NYC', 'London', 'Tokyo', 'Sydney'],
        >>>     'lat': [40.7, 51.5, 35.7, -33.9],
        >>>     'lon': [-74.0, -0.1, 139.7, 151.2],
        >>>     'population': [8.3, 8.9, 13.9, 5.3]
        >>> })
        >>>
        >>> vz.scattergeo(df, lat='lat', lon='lon',
        >>>               size='population', text='city',
        >>>               title='Major Cities')
    """
    chart = ScatterGeoMap(
        data=data,
        lat=lat,
        lon=lon,
        size=size,
        color=color,
        text=text,
        title=title,
        marker_size=marker_size,
        colorscale=colorscale,
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
