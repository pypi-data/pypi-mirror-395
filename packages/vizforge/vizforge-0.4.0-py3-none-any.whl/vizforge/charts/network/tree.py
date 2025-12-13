"""Tree Diagram implementation for VizForge."""

from typing import Optional, List, Dict, Union, Tuple
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from ...core.base import BaseChart
from ...core.theme import Theme


class TreeDiagram(BaseChart):
    """
    Tree Diagram visualization (hierarchical).

    Creates hierarchical tree structures with parent-child relationships.
    Perfect for org charts, file systems, taxonomies, decision trees.

    Examples:
        >>> import vizforge as vz
        >>>
        >>> # Organization chart
        >>> labels = ['CEO', 'CTO', 'CFO', 'Dev Team', 'Finance Team']
        >>> parents = ['', 'CEO', 'CEO', 'CTO', 'CFO']
        >>> values = [100, 50, 30, 25, 20]
        >>>
        >>> vz.tree(labels, parents, values, title='Org Structure')
    """

    def __init__(
        self,
        labels: List[str],
        parents: List[str],
        values: Optional[List[float]] = None,
        text: Optional[List[str]] = None,
        marker_colors: Optional[List[str]] = None,
        orientation: str = 'v',  # 'v' for vertical, 'h' for horizontal
        title: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize Tree Diagram.

        Args:
            labels: Node labels
            parents: Parent node labels (empty string for root)
            values: Node values (affects size)
            text: Additional text for nodes
            marker_colors: Node colors
            orientation: 'v' (top-down) or 'h' (left-right)
            title: Chart title
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        self.labels = labels
        self.parents = parents
        self.values = values or [1] * len(labels)
        self.text = text or labels
        self.marker_colors = marker_colors or self._generate_colors(len(labels))
        self.orientation = orientation

    def _generate_colors(self, n: int) -> List[str]:
        """Generate colors for nodes."""
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6',
                  '#1abc9c', '#e67e22', '#95a5a6', '#16a085', '#c0392b']
        return [colors[i % len(colors)] for i in range(n)]

    def create_trace(self) -> go.Treemap:
        """Create Plotly Treemap trace (tree representation)."""
        # Using Treemap for tree visualization
        treemap = go.Treemap(
            labels=self.labels,
            parents=self.parents,
            values=self.values,
            text=self.text,
            textposition="middle center",
            marker=dict(
                colors=self.marker_colors,
                line=dict(width=2, color='white')
            ),
            hovertemplate='<b>%{label}</b><br>Value: %{value}<extra></extra>'
        )
        return treemap

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure."""
        trace = self.create_trace()

        layout = go.Layout(
            title=self.title,
            **self._get_theme_layout()
        )

        fig = go.Figure(data=[trace], layout=layout)
        return fig


class IcicleDiagram(BaseChart):
    """
    Icicle Diagram visualization (vertical tree).

    Hierarchical visualization with rectangular partitions.
    Similar to treemap but with a vertical/horizontal flow.
    """

    def __init__(
        self,
        labels: List[str],
        parents: List[str],
        values: Optional[List[float]] = None,
        text: Optional[List[str]] = None,
        marker_colors: Optional[List[str]] = None,
        orientation: str = 'v',
        title: Optional[str] = None,
        **kwargs
    ):
        """Initialize Icicle Diagram."""
        super().__init__(title=title, **kwargs)

        self.labels = labels
        self.parents = parents
        self.values = values or [1] * len(labels)
        self.text = text or labels
        self.marker_colors = marker_colors
        self.orientation = orientation

    def create_trace(self) -> go.Icicle:
        """Create Plotly Icicle trace."""
        icicle = go.Icicle(
            labels=self.labels,
            parents=self.parents,
            values=self.values,
            text=self.text,
            textposition="middle center",
            marker=dict(
                colors=self.marker_colors,
                line=dict(width=2, color='white')
            ) if self.marker_colors else None,
            hovertemplate='<b>%{label}</b><br>Value: %{value}<extra></extra>'
        )
        return icicle

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure."""
        trace = self.create_trace()

        layout = go.Layout(
            title=self.title,
            **self._get_theme_layout()
        )

        fig = go.Figure(data=[trace], layout=layout)
        return fig


def tree(
    labels: List[str],
    parents: List[str],
    values: Optional[List[float]] = None,
    text: Optional[List[str]] = None,
    marker_colors: Optional[List[str]] = None,
    orientation: str = 'v',
    title: Optional[str] = None,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> TreeDiagram:
    """
    Create a tree diagram.

    Args:
        labels: Node labels
        parents: Parent labels (empty for root)
        values: Node values
        text: Node text
        marker_colors: Node colors
        orientation: 'v' or 'h'
        title: Chart title
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        TreeDiagram instance

    Examples:
        >>> import vizforge as vz
        >>>
        >>> # File system
        >>> labels = ['/', 'home', 'var', 'user1', 'user2', 'logs', 'data']
        >>> parents = ['', '/', '/', 'home', 'home', 'var', 'var']
        >>> values = [100, 40, 60, 20, 20, 30, 30]
        >>>
        >>> vz.tree(labels, parents, values, title='Directory Structure')
    """
    chart = TreeDiagram(
        labels=labels,
        parents=parents,
        values=values,
        text=text,
        marker_colors=marker_colors,
        orientation=orientation,
        title=title,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart


def icicle(
    labels: List[str],
    parents: List[str],
    values: Optional[List[float]] = None,
    text: Optional[List[str]] = None,
    marker_colors: Optional[List[str]] = None,
    orientation: str = 'v',
    title: Optional[str] = None,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> IcicleDiagram:
    """
    Create an icicle diagram.

    Args:
        labels: Node labels
        parents: Parent labels
        values: Node values
        text: Node text
        marker_colors: Node colors
        orientation: 'v' or 'h'
        title: Chart title
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        IcicleDiagram instance

    Examples:
        >>> import vizforge as vz
        >>>
        >>> # Product hierarchy
        >>> labels = ['Products', 'Electronics', 'Clothing',
        >>>          'Phones', 'Laptops', 'Shirts', 'Pants']
        >>> parents = ['', 'Products', 'Products',
        >>>           'Electronics', 'Electronics', 'Clothing', 'Clothing']
        >>>
        >>> vz.icicle(labels, parents, title='Product Categories')
    """
    chart = IcicleDiagram(
        labels=labels,
        parents=parents,
        values=values,
        text=text,
        marker_colors=marker_colors,
        orientation=orientation,
        title=title,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart
