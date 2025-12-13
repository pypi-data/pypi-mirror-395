"""Density geo map implementation for VizForge."""

from typing import Optional, Union, List
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from ...core.base import BaseChart
from ...core.theme import Theme


class DensityGeoMap(BaseChart):
    """
    Density geo map visualization.

    Creates density/heatmap on geographical maps.
    Perfect for population density, crime hotspots, temperature maps.

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>> import numpy as np
        >>>
        >>> # Population density
        >>> df = pd.DataFrame({
        >>>     'lat': np.random.uniform(35, 45, 1000),
        >>>     'lon': np.random.uniform(-120, -70, 1000)
        >>> })
        >>>
        >>> vz.densitygeo(df, lat='lat', lon='lon',
        >>>               title='Population Density')
    """

    def __init__(
        self,
        data: Union[pd.DataFrame, dict, None] = None,
        lat: Optional[Union[str, List, np.ndarray]] = None,
        lon: Optional[Union[str, List, np.ndarray]] = None,
        z: Optional[Union[str, List, np.ndarray]] = None,
        title: Optional[str] = None,
        radius: int = 10,
        colorscale: str = "Hot",
        scope: str = "world",
        projection: str = "natural earth",
        **kwargs
    ):
        """
        Initialize Density Geo map.

        Args:
            data: DataFrame or dict
            lat: Latitude column or values
            lon: Longitude column or values
            z: Intensity values (optional)
            title: Chart title
            radius: Heatmap radius
            colorscale: Color scale
            scope: Map scope
            projection: Projection type
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        self.data = data
        self.lat_col = lat
        self.lon_col = lon
        self.z_col = z
        self.radius = radius
        self.colorscale = colorscale
        self.scope = scope
        self.projection = projection

        # Extract values
        self.lat_vals = self._extract_values(lat)
        self.lon_vals = self._extract_values(lon)
        self.z_vals = self._extract_values(z)

    def _extract_values(self, col):
        """Extract values from DataFrame or direct input."""
        if col is None:
            return None

        if isinstance(self.data, pd.DataFrame) and isinstance(col, str):
            return self.data[col].values
        else:
            return col

    def create_trace(self) -> go.Densitymapbox:
        """Create Plotly Densitymapbox trace."""

        trace_args = {
            'lat': self.lat_vals,
            'lon': self.lon_vals,
            'radius': self.radius,
            'colorscale': self.colorscale,
            'showscale': True,
        }

        if self.z_vals is not None:
            trace_args['z'] = self.z_vals

        trace = go.Densitymapbox(**trace_args)

        return trace

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure."""
        trace = self.create_trace()

        # Calculate center
        center_lat = np.mean(self.lat_vals)
        center_lon = np.mean(self.lon_vals)

        layout = go.Layout(
            title=self.title,
            mapbox=dict(
                style='open-street-map',
                center=dict(lat=center_lat, lon=center_lon),
                zoom=3
            ),
            **self._get_theme_layout()
        )

        fig = go.Figure(data=[trace], layout=layout)
        return fig


def densitygeo(
    data: Union[pd.DataFrame, dict, None] = None,
    lat: Optional[Union[str, List, np.ndarray]] = None,
    lon: Optional[Union[str, List, np.ndarray]] = None,
    z: Optional[Union[str, List, np.ndarray]] = None,
    title: Optional[str] = None,
    radius: int = 10,
    colorscale: str = "Hot",
    scope: str = "world",
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> DensityGeoMap:
    """
    Create a density geo map (heatmap on map).

    Args:
        data: DataFrame or dict
        lat: Latitude column or values
        lon: Longitude column or values
        z: Intensity values (optional)
        title: Chart title
        radius: Heatmap radius
        colorscale: Color scale
        scope: Map scope
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        DensityGeoMap instance

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>> import numpy as np
        >>>
        >>> # Crime hotspots
        >>> df = pd.DataFrame({
        >>>     'lat': np.random.normal(40.7, 0.1, 500),
        >>>     'lon': np.random.normal(-74.0, 0.1, 500),
        >>>     'severity': np.random.randint(1, 10, 500)
        >>> })
        >>>
        >>> vz.densitygeo(df, lat='lat', lon='lon', z='severity',
        >>>               title='Crime Density Map',
        >>>               radius=15)
    """
    chart = DensityGeoMap(
        data=data,
        lat=lat,
        lon=lon,
        z=z,
        title=title,
        radius=radius,
        colorscale=colorscale,
        scope=scope,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart
