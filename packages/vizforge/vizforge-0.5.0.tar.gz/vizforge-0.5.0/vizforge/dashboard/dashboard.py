"""Dashboard builder for VizForge."""

from typing import List, Dict, Optional, Union, Tuple
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

from ..core.base import BaseChart
from ..core.theme import Theme, get_theme


class DashboardLayout:
    """Layout configurations for dashboards."""

    GRID = "grid"
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"
    CUSTOM = "custom"


class Dashboard:
    """
    Interactive dashboard builder.

    Combine multiple charts, KPIs, and filters into a single dashboard.
    Perfect for executive reports, analytics dashboards, monitoring.

    Examples:
        >>> import vizforge as vz
        >>>
        >>> # Create dashboard
        >>> dashboard = vz.Dashboard(title="Sales Dashboard", rows=2, cols=2)
        >>>
        >>> # Add charts
        >>> dashboard.add_chart(chart1, row=1, col=1)
        >>> dashboard.add_chart(chart2, row=1, col=2)
        >>> dashboard.add_kpi("Revenue", "$1.2M", row=2, col=1)
        >>>
        >>> # Display
        >>> dashboard.show()
    """

    def __init__(
        self,
        title: str = "Dashboard",
        rows: int = 2,
        cols: int = 2,
        theme: Optional[str] = None,
        layout: str = DashboardLayout.GRID,
        height: int = 800,
        width: Optional[int] = None,
        **kwargs
    ):
        """
        Initialize Dashboard.

        Args:
            title: Dashboard title
            rows: Number of rows
            cols: Number of columns
            theme: Theme name
            layout: Layout type
            height: Dashboard height
            width: Dashboard width
            **kwargs: Additional arguments
        """
        self.title = title
        self.rows = rows
        self.cols = cols
        self.theme = get_theme(theme)
        self.layout_type = layout
        self.height = height
        self.width = width
        self.kwargs = kwargs

        # Components storage
        self.components = []
        self.kpis = []
        self.filters = []

        # Create subplot figure
        self._create_subplots()

    def _create_subplots(self):
        """Create subplot structure."""
        self.fig = make_subplots(
            rows=self.rows,
            cols=self.cols,
            subplot_titles=[None] * (self.rows * self.cols),
            vertical_spacing=0.1,
            horizontal_spacing=0.1
        )

        # Apply theme
        self._apply_theme()

    def _apply_theme(self):
        """Apply theme to dashboard."""
        self.fig.update_layout(
            title=self.title,
            showlegend=True,
            height=self.height,
            width=self.width,
            template=self.theme.plotly_template,
            font=dict(
                family=self.theme.font_family,
                size=self.theme.font_size,
                color=self.theme.text_color
            ),
            paper_bgcolor=self.theme.background_color,
            plot_bgcolor=self.theme.background_color
        )

    def add_chart(
        self,
        chart: Union[BaseChart, go.Figure],
        row: int,
        col: int,
        title: Optional[str] = None
    ):
        """
        Add chart to dashboard.

        Args:
            chart: VizForge chart or Plotly figure
            row: Row position (1-indexed)
            col: Column position (1-indexed)
            title: Subplot title
        """
        # Get figure from chart
        if isinstance(chart, BaseChart):
            fig = chart.create_figure()
        else:
            fig = chart

        # Add traces to subplot
        for trace in fig.data:
            self.fig.add_trace(trace, row=row, col=col)

        # Update subplot title
        if title:
            subplot_idx = (row - 1) * self.cols + (col - 1)
            self.fig.layout.annotations[subplot_idx].text = title

        self.components.append({
            'type': 'chart',
            'row': row,
            'col': col,
            'title': title
        })

    def add_kpi(
        self,
        label: str,
        value: Union[str, float, int],
        row: int,
        col: int,
        delta: Optional[Union[str, float]] = None,
        delta_color: str = "green"
    ):
        """
        Add KPI card to dashboard.

        Args:
            label: KPI label
            value: KPI value
            row: Row position
            col: Column position
            delta: Change indicator
            delta_color: Delta color
        """
        # Create KPI indicator
        indicator = go.Indicator(
            mode="number+delta" if delta else "number",
            value=float(value) if isinstance(value, (int, float)) else 0,
            title={'text': label},
            delta={'reference': delta} if delta else None,
            domain={'x': [0, 1], 'y': [0, 1]}
        )

        self.fig.add_trace(indicator, row=row, col=col)

        self.kpis.append({
            'label': label,
            'value': value,
            'row': row,
            'col': col
        })

    def add_text(
        self,
        text: str,
        row: int,
        col: int,
        font_size: int = 14
    ):
        """
        Add text annotation to dashboard.

        Args:
            text: Text content
            row: Row position
            col: Column position
            font_size: Font size
        """
        # Calculate position
        x_pos = (col - 0.5) / self.cols
        y_pos = 1 - (row - 0.5) / self.rows

        self.fig.add_annotation(
            text=text,
            x=x_pos,
            y=y_pos,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=font_size)
        )

    def set_column_widths(self, widths: List[float]):
        """
        Set custom column widths.

        Args:
            widths: List of width ratios (must sum to 1)
        """
        if len(widths) != self.cols:
            raise ValueError(f"Must provide {self.cols} width values")
        if abs(sum(widths) - 1.0) > 0.01:
            raise ValueError("Widths must sum to 1.0")

        self.fig.update_layout(
            grid={'columns': self.cols, 'rows': self.rows}
        )

    def set_row_heights(self, heights: List[float]):
        """
        Set custom row heights.

        Args:
            heights: List of height ratios (must sum to 1)
        """
        if len(heights) != self.rows:
            raise ValueError(f"Must provide {self.rows} height values")
        if abs(sum(heights) - 1.0) > 0.01:
            raise ValueError("Heights must sum to 1.0")

    def show(self):
        """Display dashboard."""
        self.fig.show()

    def export(self, filepath: str, **kwargs):
        """
        Export dashboard to file.

        Args:
            filepath: Output file path
            **kwargs: Additional export arguments
        """
        from ..core.export import export_chart
        export_chart(self.fig, filepath, **kwargs)

    def to_html(self, filepath: str):
        """Export dashboard as HTML."""
        self.fig.write_html(filepath)


def create_dashboard(
    title: str = "Dashboard",
    rows: int = 2,
    cols: int = 2,
    theme: Optional[str] = None,
    **kwargs
) -> Dashboard:
    """
    Create a new dashboard.

    Args:
        title: Dashboard title
        rows: Number of rows
        cols: Number of columns
        theme: Theme name
        **kwargs: Additional arguments

    Returns:
        Dashboard instance

    Examples:
        >>> import vizforge as vz
        >>>
        >>> # Create 2x2 dashboard
        >>> dashboard = vz.create_dashboard("Sales Dashboard", rows=2, cols=2)
        >>>
        >>> # Add components
        >>> dashboard.add_chart(line_chart, row=1, col=1, title="Sales Trend")
        >>> dashboard.add_chart(bar_chart, row=1, col=2, title="By Category")
        >>> dashboard.add_kpi("Total Revenue", "$1.2M", row=2, col=1, delta="+15%")
        >>> dashboard.add_kpi("Total Orders", "5,432", row=2, col=2, delta="+8%")
        >>>
        >>> # Show
        >>> dashboard.show()
    """
    return Dashboard(title=title, rows=rows, cols=cols, theme=theme, **kwargs)
