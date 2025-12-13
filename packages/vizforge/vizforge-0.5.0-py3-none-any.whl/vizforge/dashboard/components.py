"""Dashboard components for VizForge."""

from typing import Optional, List, Dict, Any, Callable
import plotly.graph_objects as go
from ..core.base import BaseChart


class DashboardComponent:
    """Base class for dashboard components."""

    def __init__(self, title: Optional[str] = None):
        """Initialize component."""
        self.title = title

    def render(self) -> go.Figure:
        """Render component as Plotly figure."""
        raise NotImplementedError


class ChartComponent(DashboardComponent):
    """
    Chart component for dashboards.

    Wraps a VizForge chart for dashboard use.
    """

    def __init__(self, chart: BaseChart, title: Optional[str] = None):
        """
        Initialize chart component.

        Args:
            chart: VizForge chart
            title: Component title
        """
        super().__init__(title or chart.title)
        self.chart = chart

    def render(self) -> go.Figure:
        """Render chart."""
        return self.chart.create_figure()


class KPICard(DashboardComponent):
    """
    KPI card component.

    Display key performance indicators with optional delta.
    """

    def __init__(
        self,
        label: str,
        value: Any,
        delta: Optional[float] = None,
        delta_reference: Optional[float] = None,
        prefix: str = "",
        suffix: str = "",
        format: str = ".2f"
    ):
        """
        Initialize KPI card.

        Args:
            label: KPI label
            value: Current value
            delta: Change amount
            delta_reference: Reference value for delta
            prefix: Value prefix (e.g., '$')
            suffix: Value suffix (e.g., '%')
            format: Number format string
        """
        super().__init__(label)
        self.value = value
        self.delta = delta
        self.delta_reference = delta_reference
        self.prefix = prefix
        self.suffix = suffix
        self.format = format

    def render(self) -> go.Figure:
        """Render KPI card."""
        # Format value
        if isinstance(self.value, (int, float)):
            formatted_value = f"{self.prefix}{self.value:{self.format}}{self.suffix}"
        else:
            formatted_value = str(self.value)

        # Create indicator
        mode = "number"
        indicator_args = {
            'mode': mode,
            'value': self.value if isinstance(self.value, (int, float)) else 0,
            'title': {'text': self.title},
            'number': {'prefix': self.prefix, 'suffix': self.suffix}
        }

        if self.delta is not None:
            indicator_args['mode'] = "number+delta"
            indicator_args['delta'] = {'reference': self.delta_reference or 0}

        indicator = go.Indicator(**indicator_args)

        fig = go.Figure(data=[indicator])
        fig.update_layout(height=200)

        return fig


class FilterComponent(DashboardComponent):
    """
    Filter component for interactive dashboards.

    Allow users to filter dashboard data.
    """

    def __init__(
        self,
        label: str,
        options: List[Any],
        default: Optional[Any] = None,
        multi_select: bool = False,
        callback: Optional[Callable] = None
    ):
        """
        Initialize filter component.

        Args:
            label: Filter label
            options: Available filter options
            default: Default selected value
            multi_select: Allow multiple selections
            callback: Function to call when filter changes
        """
        super().__init__(label)
        self.options = options
        self.default = default
        self.multi_select = multi_select
        self.callback = callback
        self.selected = default

    def update(self, value: Any):
        """Update filter value."""
        self.selected = value
        if self.callback:
            self.callback(value)

    def render(self) -> Dict:
        """Render filter metadata."""
        return {
            'type': 'filter',
            'label': self.label,
            'options': self.options,
            'selected': self.selected,
            'multi_select': self.multi_select
        }


class TextComponent(DashboardComponent):
    """
    Text component for dashboards.

    Display formatted text, markdown, or HTML.
    """

    def __init__(
        self,
        text: str,
        title: Optional[str] = None,
        font_size: int = 14,
        align: str = "left"
    ):
        """
        Initialize text component.

        Args:
            text: Text content
            title: Component title
            font_size: Font size
            align: Text alignment
        """
        super().__init__(title)
        self.text = text
        self.font_size = font_size
        self.align = align

    def render(self) -> go.Figure:
        """Render text as figure."""
        fig = go.Figure()

        fig.add_annotation(
            text=self.text,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=self.font_size),
            align=self.align
        )

        fig.update_layout(
            height=150,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )

        return fig


class MetricCard(KPICard):
    """
    Enhanced metric card with trend indicators.

    Similar to KPICard but with additional visual elements.
    """

    def __init__(
        self,
        label: str,
        value: Any,
        trend: Optional[List[float]] = None,
        delta: Optional[float] = None,
        **kwargs
    ):
        """
        Initialize metric card.

        Args:
            label: Metric label
            value: Current value
            trend: Historical trend data
            delta: Change amount
            **kwargs: Additional KPICard arguments
        """
        super().__init__(label, value, delta, **kwargs)
        self.trend = trend

    def render(self) -> go.Figure:
        """Render metric card with trend."""
        fig = super().render()

        # Add sparkline if trend data provided
        if self.trend:
            fig.add_trace(go.Scatter(
                y=self.trend,
                mode='lines',
                line=dict(color='lightgray', width=1),
                showlegend=False,
                hoverinfo='skip'
            ))

        return fig
