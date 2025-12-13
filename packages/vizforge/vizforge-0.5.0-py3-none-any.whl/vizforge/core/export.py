"""Export utilities for VizForge charts."""

import os
from typing import Optional, Union, Literal
import plotly.graph_objects as go

# Try to import kaleido for static exports
try:
    import kaleido
    KALEIDO_AVAILABLE = True
except ImportError:
    KALEIDO_AVAILABLE = False


class ExportError(Exception):
    """Exception raised for export-related errors."""
    pass


class ChartExporter:
    """
    Handle export of charts to various formats.

    Supports HTML, PNG, SVG, PDF, and JSON formats.
    """

    SUPPORTED_FORMATS = ['html', 'png', 'svg', 'pdf', 'json']

    def __init__(self, figure: go.Figure):
        """
        Initialize exporter with a Plotly figure.

        Args:
            figure: Plotly Figure object to export
        """
        self.figure = figure

    def export(
        self,
        filepath: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        scale: float = 1.0,
        format: Optional[str] = None
    ) -> None:
        """
        Export chart to file.

        Args:
            filepath: Output file path
            width: Width in pixels (for static formats)
            height: Height in pixels (for static formats)
            scale: Scale factor for resolution
            format: Force specific format (auto-detected from filepath if None)

        Raises:
            ExportError: If export fails or format not supported
        """
        # Detect format from filepath
        if format is None:
            format = self._detect_format(filepath)

        # Validate format
        if format not in self.SUPPORTED_FORMATS:
            raise ExportError(
                f"Unsupported format: {format}. "
                f"Supported formats: {', '.join(self.SUPPORTED_FORMATS)}"
            )

        # Route to appropriate export method
        if format == 'html':
            self._export_html(filepath)
        elif format == 'json':
            self._export_json(filepath)
        elif format in ['png', 'svg', 'pdf']:
            self._export_static(filepath, format, width, height, scale)

    def _detect_format(self, filepath: str) -> str:
        """Detect format from file extension."""
        ext = os.path.splitext(filepath)[1].lower().lstrip('.')
        if not ext:
            raise ExportError("File path must have an extension")
        return ext

    def _export_html(self, filepath: str) -> None:
        """Export as interactive HTML."""
        self.figure.write_html(filepath)

    def _export_json(self, filepath: str) -> None:
        """Export as JSON."""
        self.figure.write_json(filepath)

    def _export_static(
        self,
        filepath: str,
        format: str,
        width: Optional[int],
        height: Optional[int],
        scale: float
    ) -> None:
        """
        Export as static image (PNG, SVG, PDF).

        Requires kaleido package.
        """
        if not KALEIDO_AVAILABLE:
            raise ExportError(
                f"Static export to {format.upper()} requires kaleido. "
                "Install with: pip install kaleido"
            )

        # Default dimensions
        if width is None:
            width = 1200
        if height is None:
            height = 800

        # Export using kaleido
        self.figure.write_image(
            filepath,
            format=format,
            width=width,
            height=height,
            scale=scale
        )


def export_chart(
    figure: go.Figure,
    filepath: str,
    width: Optional[int] = None,
    height: Optional[int] = None,
    scale: float = 1.0,
    format: Optional[str] = None
) -> None:
    """
    Export a Plotly figure to file.

    Convenience function for exporting charts.

    Args:
        figure: Plotly Figure to export
        filepath: Output file path
        width: Width in pixels (for static formats)
        height: Height in pixels (for static formats)
        scale: Scale factor for resolution
        format: Force specific format (auto-detected if None)

    Examples:
        >>> import vizforge as vz
        >>> chart = vz.line(data, x='date', y='value')
        >>> vz.export_chart(chart.create_figure(), 'output.png', width=1920, height=1080)
        >>> vz.export_chart(chart.create_figure(), 'output.pdf')
        >>> vz.export_chart(chart.create_figure(), 'output.svg')
    """
    exporter = ChartExporter(figure)
    exporter.export(filepath, width, height, scale, format)


class BatchExporter:
    """Export multiple charts at once."""

    def __init__(self):
        """Initialize batch exporter."""
        self.charts = []

    def add_chart(self, figure: go.Figure, name: str):
        """Add a chart to export batch."""
        self.charts.append((figure, name))

    def export_all(
        self,
        output_dir: str,
        format: str = 'html',
        width: Optional[int] = None,
        height: Optional[int] = None,
        scale: float = 1.0
    ) -> None:
        """
        Export all added charts to directory.

        Args:
            output_dir: Output directory path
            format: Export format
            width: Width in pixels
            height: Height in pixels
            scale: Scale factor
        """
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Export each chart
        for figure, name in self.charts:
            filepath = os.path.join(output_dir, f"{name}.{format}")
            exporter = ChartExporter(figure)
            exporter.export(filepath, width, height, scale, format)

    def clear(self):
        """Clear all charts from batch."""
        self.charts = []
