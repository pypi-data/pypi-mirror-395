"""Sankey Diagram implementation for VizForge."""

from typing import Optional, List, Dict, Union
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from ...core.base import BaseChart
from ...core.theme import Theme


class SankeyDiagram(BaseChart):
    """
    Sankey Diagram visualization.

    Shows flow quantities between nodes with proportional link widths.
    Perfect for material flow, energy transfer, process flows, budget allocation.

    Examples:
        >>> import vizforge as vz
        >>>
        >>> # Energy flow
        >>> nodes = ['Coal', 'Gas', 'Solar', 'Electricity', 'Heat']
        >>> sources = [0, 1, 2, 3]
        >>> targets = [3, 3, 3, 4]
        >>> values = [50, 30, 20, 100]
        >>>
        >>> vz.sankey(nodes, sources, targets, values, title='Energy Flow')
    """

    def __init__(
        self,
        nodes: Union[List[str], Dict],
        sources: List[int],
        targets: List[int],
        values: List[float],
        node_colors: Optional[List[str]] = None,
        link_colors: Optional[List[str]] = None,
        title: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize Sankey Diagram.

        Args:
            nodes: List of node labels or dict with node properties
            sources: List of source node indices
            targets: List of target node indices
            values: List of flow values
            node_colors: Colors for nodes
            link_colors: Colors for links
            title: Chart title
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        self.node_labels = nodes if isinstance(nodes, list) else nodes.get('label', [])
        self.sources = sources
        self.targets = targets
        self.values = values
        self.node_colors = node_colors or self._generate_node_colors(len(self.node_labels))
        self.link_colors = link_colors or self._generate_link_colors(len(sources))

    def _generate_node_colors(self, n: int) -> List[str]:
        """Generate colors for nodes."""
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6',
                  '#1abc9c', '#e67e22', '#34495e', '#16a085', '#c0392b']
        return [colors[i % len(colors)] for i in range(n)]

    def _generate_link_colors(self, n: int) -> List[str]:
        """Generate semi-transparent colors for links."""
        base_colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
        return [f'rgba({int(base_colors[i % len(base_colors)][1:3], 16)}, '
                f'{int(base_colors[i % len(base_colors)][3:5], 16)}, '
                f'{int(base_colors[i % len(base_colors)][5:7], 16)}, 0.4)'
                for i in range(n)]

    def create_trace(self) -> go.Sankey:
        """Create Plotly Sankey trace."""
        sankey = go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="white", width=2),
                label=self.node_labels,
                color=self.node_colors
            ),
            link=dict(
                source=self.sources,
                target=self.targets,
                value=self.values,
                color=self.link_colors
            )
        )
        return sankey

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure."""
        trace = self.create_trace()

        layout = go.Layout(
            title=self.title,
            font=dict(size=12),
            **self._get_theme_layout()
        )

        fig = go.Figure(data=[trace], layout=layout)
        return fig


def sankey(
    nodes: Union[List[str], Dict],
    sources: List[int],
    targets: List[int],
    values: List[float],
    node_colors: Optional[List[str]] = None,
    link_colors: Optional[List[str]] = None,
    title: Optional[str] = None,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> SankeyDiagram:
    """
    Create a Sankey diagram.

    Args:
        nodes: List of node labels
        sources: Source node indices
        targets: Target node indices
        values: Flow values
        node_colors: Node colors
        link_colors: Link colors
        title: Chart title
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        SankeyDiagram instance

    Examples:
        >>> import vizforge as vz
        >>>
        >>> # Budget allocation
        >>> nodes = ['Budget', 'Marketing', 'R&D', 'Operations',
        >>>          'Digital', 'Traditional', 'Products', 'Services']
        >>> sources = [0, 0, 0, 1, 1, 2, 2]
        >>> targets = [1, 2, 3, 4, 5, 6, 7]
        >>> values = [300, 200, 500, 180, 120, 100, 100]
        >>>
        >>> vz.sankey(nodes, sources, targets, values,
        >>>          title='Budget Flow Analysis')
    """
    chart = SankeyDiagram(
        nodes=nodes,
        sources=sources,
        targets=targets,
        values=values,
        node_colors=node_colors,
        link_colors=link_colors,
        title=title,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart
