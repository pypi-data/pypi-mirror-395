"""Animated Chart implementation for VizForge."""

from typing import Optional, List, Dict, Union
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from ...core.base import BaseChart
from ...core.theme import Theme


class AnimatedScatter(BaseChart):
    """
    Animated Scatter Plot.

    Shows evolution of data over time with smooth animations.
    Perfect for time-series scatter, bubble chart animations, data transitions.

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>>
        >>> # Gapminder-style animation
        >>> df = pd.DataFrame({
        >>>     'year': [2000]*3 + [2010]*3 + [2020]*3,
        >>>     'country': ['A', 'B', 'C']*3,
        >>>     'gdp': [1000, 2000, 1500, 1500, 2500, 2000, 2000, 3000, 2500],
        >>>     'life_exp': [65, 70, 68, 70, 75, 72, 75, 80, 77],
        >>>     'population': [100, 200, 150]*3
        >>> })
        >>>
        >>> vz.animated_scatter(df, x='gdp', y='life_exp',
        >>>                    animation_frame='year', size='population',
        >>>                    color='country', title='Development Over Time')
    """

    def __init__(
        self,
        data: pd.DataFrame,
        x: str,
        y: str,
        animation_frame: str,
        size: Optional[str] = None,
        color: Optional[str] = None,
        hover_name: Optional[str] = None,
        animation_duration: int = 1000,
        title: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize Animated Scatter.

        Args:
            data: DataFrame with animation frames
            x: X-axis column
            y: Y-axis column
            animation_frame: Column for animation frames
            size: Column for marker size
            color: Column for marker color
            hover_name: Column for hover labels
            animation_duration: Frame duration in ms
            title: Chart title
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        self.data = data
        self.x = x
        self.y = y
        self.animation_frame = animation_frame
        self.size = size
        self.color = color
        self.hover_name = hover_name
        self.animation_duration = animation_duration

    def create_figure(self) -> go.Figure:
        """Create animated scatter plot using Plotly Express."""
        fig = px.scatter(
            self.data,
            x=self.x,
            y=self.y,
            animation_frame=self.animation_frame,
            size=self.size,
            color=self.color,
            hover_name=self.hover_name,
            title=self.title,
            range_x=[self.data[self.x].min() * 0.9, self.data[self.x].max() * 1.1],
            range_y=[self.data[self.y].min() * 0.9, self.data[self.y].max() * 1.1]
        )

        # Update animation settings
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = self.animation_duration
        fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = self.animation_duration // 2

        # Apply theme
        fig.update_layout(**self._get_theme_layout())

        return fig


class AnimatedBar(BaseChart):
    """
    Animated Bar Chart.

    Shows ranking/value changes over time with bar race animations.
    Perfect for rankings, competitions, sales evolution.
    """

    def __init__(
        self,
        data: pd.DataFrame,
        x: str,
        y: str,
        animation_frame: str,
        color: Optional[str] = None,
        orientation: str = 'v',
        animation_duration: int = 1000,
        title: Optional[str] = None,
        **kwargs
    ):
        """Initialize Animated Bar Chart."""
        super().__init__(title=title, **kwargs)

        self.data = data
        self.x = x
        self.y = y
        self.animation_frame = animation_frame
        self.color = color
        self.orientation = orientation
        self.animation_duration = animation_duration

    def create_figure(self) -> go.Figure:
        """Create animated bar chart."""
        fig = px.bar(
            self.data,
            x=self.x,
            y=self.y,
            animation_frame=self.animation_frame,
            color=self.color,
            orientation=self.orientation,
            title=self.title,
            range_x=[0, self.data[self.x].max() * 1.1] if self.orientation == 'h' else None,
            range_y=[0, self.data[self.y].max() * 1.1] if self.orientation == 'v' else None
        )

        # Update animation settings
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = self.animation_duration
        fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = self.animation_duration // 2

        # Apply theme
        fig.update_layout(**self._get_theme_layout())

        return fig


class AnimatedChoropleth(BaseChart):
    """
    Animated Choropleth Map.

    Geographic data evolution over time.
    Perfect for pandemic spread, election results, demographic changes.
    """

    def __init__(
        self,
        data: pd.DataFrame,
        locations: str,
        values: str,
        animation_frame: str,
        locationmode: str = "ISO-3",
        colorscale: str = "Viridis",
        scope: str = "world",
        title: Optional[str] = None,
        **kwargs
    ):
        """Initialize Animated Choropleth."""
        super().__init__(title=title, **kwargs)

        self.data = data
        self.locations = locations
        self.values = values
        self.animation_frame = animation_frame
        self.locationmode = locationmode
        self.colorscale = colorscale
        self.scope = scope

    def create_figure(self) -> go.Figure:
        """Create animated choropleth map."""
        fig = px.choropleth(
            self.data,
            locations=self.locations,
            locationmode=self.locationmode,
            color=self.values,
            animation_frame=self.animation_frame,
            color_continuous_scale=self.colorscale,
            scope=self.scope,
            title=self.title
        )

        # Apply theme
        fig.update_layout(**self._get_theme_layout())

        return fig


def animated_scatter(
    data: pd.DataFrame,
    x: str,
    y: str,
    animation_frame: str,
    size: Optional[str] = None,
    color: Optional[str] = None,
    hover_name: Optional[str] = None,
    animation_duration: int = 1000,
    title: Optional[str] = None,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> AnimatedScatter:
    """
    Create an animated scatter plot.

    Args:
        data: DataFrame with data
        x: X-axis column
        y: Y-axis column
        animation_frame: Animation frame column
        size: Size column
        color: Color column
        hover_name: Hover name column
        animation_duration: Frame duration (ms)
        title: Chart title
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        AnimatedScatter instance

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>> import numpy as np
        >>>
        >>> # Evolution of metrics
        >>> years = list(range(2010, 2024))
        >>> data = pd.DataFrame({
        >>>     'year': years * 5,
        >>>     'company': ['A', 'B', 'C', 'D', 'E'] * 14,
        >>>     'revenue': np.random.randint(100, 1000, 70),
        >>>     'profit': np.random.randint(10, 200, 70),
        >>>     'employees': np.random.randint(50, 500, 70)
        >>> })
        >>>
        >>> vz.animated_scatter(
        >>>     data, x='revenue', y='profit',
        >>>     animation_frame='year', size='employees',
        >>>     color='company', title='Company Growth 2010-2023'
        >>> )
    """
    chart = AnimatedScatter(
        data=data,
        x=x,
        y=y,
        animation_frame=animation_frame,
        size=size,
        color=color,
        hover_name=hover_name,
        animation_duration=animation_duration,
        title=title,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart


def animated_bar(
    data: pd.DataFrame,
    x: str,
    y: str,
    animation_frame: str,
    color: Optional[str] = None,
    orientation: str = 'v',
    animation_duration: int = 1000,
    title: Optional[str] = None,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> AnimatedBar:
    """
    Create an animated bar chart (bar race).

    Args:
        data: DataFrame with data
        x: X-axis column
        y: Y-axis column
        animation_frame: Animation frame column
        color: Color column
        orientation: 'v' or 'h'
        animation_duration: Frame duration (ms)
        title: Chart title
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        AnimatedBar instance

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>>
        >>> # Sales ranking over months
        >>> data = pd.DataFrame({
        >>>     'month': ['Jan']*5 + ['Feb']*5 + ['Mar']*5,
        >>>     'salesperson': ['Alice', 'Bob', 'Charlie', 'David', 'Eve']*3,
        >>>     'sales': [100, 90, 85, 80, 75, 110, 95, 88, 82, 78, 120, 100, 90, 85, 80]
        >>> })
        >>>
        >>> vz.animated_bar(data, x='salesperson', y='sales',
        >>>                animation_frame='month',
        >>>                title='Sales Race Q1 2024')
    """
    chart = AnimatedBar(
        data=data,
        x=x,
        y=y,
        animation_frame=animation_frame,
        color=color,
        orientation=orientation,
        animation_duration=animation_duration,
        title=title,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart


def animated_choropleth(
    data: pd.DataFrame,
    locations: str,
    values: str,
    animation_frame: str,
    locationmode: str = "ISO-3",
    colorscale: str = "Viridis",
    scope: str = "world",
    title: Optional[str] = None,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> AnimatedChoropleth:
    """
    Create an animated choropleth map.

    Args:
        data: DataFrame with data
        locations: Location column
        values: Values column
        animation_frame: Animation frame column
        locationmode: Location mode
        colorscale: Color scale
        scope: Map scope
        title: Chart title
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        AnimatedChoropleth instance

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>>
        >>> # Pandemic spread over time
        >>> data = pd.DataFrame({
        >>>     'date': ['2020-03-01']*3 + ['2020-04-01']*3,
        >>>     'country': ['USA', 'ITA', 'CHN']*2,
        >>>     'cases': [100, 200, 300, 1000, 2000, 500]
        >>> })
        >>>
        >>> vz.animated_choropleth(
        >>>     data, locations='country', values='cases',
        >>>     animation_frame='date',
        >>>     title='COVID-19 Spread'
        >>> )
    """
    chart = AnimatedChoropleth(
        data=data,
        locations=locations,
        values=values,
        animation_frame=animation_frame,
        locationmode=locationmode,
        colorscale=colorscale,
        scope=scope,
        title=title,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart
