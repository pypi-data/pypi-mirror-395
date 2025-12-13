"""Choropleth map implementation for VizForge."""

from typing import Optional, Union, List
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from ...core.base import BaseChart
from ...core.theme import Theme


class ChoroplethMap(BaseChart):
    """
    Choropleth map visualization.

    Creates color-coded geographical regions based on data values.
    Perfect for showing regional statistics, election results, demographics.

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>>
        >>> # Country data
        >>> df = pd.DataFrame({
        >>>     'country': ['USA', 'CHN', 'JPN', 'DEU', 'IND'],
        >>>     'gdp': [21.4, 14.3, 5.1, 3.8, 2.9]
        >>> })
        >>>
        >>> vz.choropleth(df, locations='country',
        >>>               values='gdp', title='GDP by Country')
    """

    def __init__(
        self,
        data: Union[pd.DataFrame, dict, None] = None,
        locations: Optional[Union[str, List]] = None,
        values: Optional[Union[str, List, np.ndarray]] = None,
        locationmode: str = "ISO-3",
        title: Optional[str] = None,
        colorscale: str = "Viridis",
        show_colorbar: bool = True,
        scope: str = "world",
        projection: str = "natural earth",
        **kwargs
    ):
        """
        Initialize Choropleth map.

        Args:
            data: DataFrame or dict
            locations: Location codes (country/state codes)
            values: Values to color-code
            locationmode: 'ISO-3', 'USA-states', 'country names'
            title: Chart title
            colorscale: Color scale
            show_colorbar: Show color bar
            scope: Map scope ('world', 'usa', 'europe', 'asia', etc.)
            projection: Map projection type
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        self.data = data
        self.locations_col = locations
        self.values_col = values
        self.locationmode = locationmode
        self.colorscale = colorscale
        self.show_colorbar = show_colorbar
        self.scope = scope
        self.projection = projection

        # Extract values
        self.locations_vals = self._extract_values(locations)
        self.values_vals = self._extract_values(values)

    def _extract_values(self, col):
        """Extract values from DataFrame or direct input."""
        if col is None:
            return None

        if isinstance(self.data, pd.DataFrame) and isinstance(col, str):
            return self.data[col].values
        else:
            return col

    def create_trace(self) -> go.Choropleth:
        """Create Plotly Choropleth trace."""

        trace = go.Choropleth(
            locations=self.locations_vals,
            z=self.values_vals,
            locationmode=self.locationmode,
            colorscale=self.colorscale,
            showscale=self.show_colorbar,
            name=self.title or "Choropleth"
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
                showlakes=True,
                lakecolor='rgb(255, 255, 255)'
            ),
            **self._get_theme_layout()
        )

        fig = go.Figure(data=[trace], layout=layout)
        return fig


def choropleth(
    data: Union[pd.DataFrame, dict, None] = None,
    locations: Optional[Union[str, List]] = None,
    values: Optional[Union[str, List, np.ndarray]] = None,
    locationmode: str = "ISO-3",
    title: Optional[str] = None,
    colorscale: str = "Viridis",
    show_colorbar: bool = True,
    scope: str = "world",
    projection: str = "natural earth",
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> ChoroplethMap:
    """
    Create a choropleth map.

    Args:
        data: DataFrame or dict
        locations: Location column or values
        values: Value column or values
        locationmode: Location identifier type
        title: Chart title
        colorscale: Color scale
        show_colorbar: Show color bar
        scope: Map scope
        projection: Projection type
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        ChoroplethMap instance

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>>
        >>> # World GDP
        >>> df = pd.DataFrame({
        >>>     'country': ['USA', 'CHN', 'JPN', 'DEU', 'IND'],
        >>>     'gdp': [21.4, 14.3, 5.1, 3.8, 2.9]
        >>> })
        >>>
        >>> vz.choropleth(df, locations='country', values='gdp',
        >>>               title='GDP by Country', colorscale='Blues')
        >>>
        >>> # USA states
        >>> df_states = pd.DataFrame({
        >>>     'state': ['CA', 'TX', 'FL', 'NY'],
        >>>     'population': [39.5, 29.0, 21.5, 19.5]
        >>> })
        >>>
        >>> vz.choropleth(df_states, locations='state',
        >>>               values='population',
        >>>               locationmode='USA-states',
        >>>               scope='usa')
    """
    chart = ChoroplethMap(
        data=data,
        locations=locations,
        values=values,
        locationmode=locationmode,
        title=title,
        colorscale=colorscale,
        show_colorbar=show_colorbar,
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
