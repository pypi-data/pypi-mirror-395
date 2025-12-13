"""Network Graph implementation for VizForge."""

from typing import Optional, Union, List, Dict
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from ...core.base import BaseChart
from ...core.theme import Theme


class NetworkGraph(BaseChart):
    """
    Network Graph visualization (force-directed).

    Creates interactive network graphs with nodes and edges.
    Perfect for social networks, dependency graphs, knowledge graphs.

    Examples:
        >>> import vizforge as vz
        >>>
        >>> # Define network
        >>> nodes = ['A', 'B', 'C', 'D', 'E']
        >>> edges = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'A')]
        >>>
        >>> vz.network_graph(nodes, edges, title='Social Network')
    """

    def __init__(
        self,
        nodes: Union[List, pd.DataFrame],
        edges: Union[List[tuple], pd.DataFrame],
        node_labels: Optional[List] = None,
        node_size: Union[int, List] = 10,
        node_color: Union[str, List] = None,
        edge_width: Union[int, List] = 1,
        layout: str = "spring",
        title: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize Network Graph.

        Args:
            nodes: List of node IDs or DataFrame
            edges: List of (source, target) tuples or DataFrame
            node_labels: Labels for nodes
            node_size: Node size(s)
            node_color: Node color(s)
            edge_width: Edge width(s)
            layout: Layout algorithm ('spring', 'circular', 'random')
            title: Chart title
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        self.nodes = nodes if isinstance(nodes, list) else nodes.tolist()
        self.edges = edges if isinstance(edges, list) else list(edges.itertuples(index=False, name=None))
        self.node_labels = node_labels or self.nodes
        self.node_size = node_size
        self.node_color = node_color
        self.edge_width = edge_width
        self.layout = layout

        # Create positions using spring layout simulation
        self.positions = self._calculate_positions()

    def _calculate_positions(self) -> Dict:
        """Calculate node positions based on layout algorithm."""
        n = len(self.nodes)

        if self.layout == "circular":
            # Circular layout
            angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
            x = np.cos(angles)
            y = np.sin(angles)
        elif self.layout == "random":
            # Random layout
            np.random.seed(42)
            x = np.random.randn(n)
            y = np.random.randn(n)
        else:  # spring layout (simple force-directed)
            # Simple spring layout simulation
            x = np.random.randn(n)
            y = np.random.randn(n)

            # Simulate forces (simplified)
            for _ in range(50):
                fx = np.zeros(n)
                fy = np.zeros(n)

                # Repulsion between all nodes
                for i in range(n):
                    for j in range(n):
                        if i != j:
                            dx = x[i] - x[j]
                            dy = y[i] - y[j]
                            dist = np.sqrt(dx*dx + dy*dy) + 0.01
                            fx[i] += dx / (dist**2)
                            fy[i] += dy / (dist**2)

                # Attraction along edges
                for source, target in self.edges:
                    i = self.nodes.index(source)
                    j = self.nodes.index(target)
                    dx = x[i] - x[j]
                    dy = y[i] - y[j]
                    fx[i] -= dx * 0.1
                    fy[i] -= dy * 0.1
                    fx[j] += dx * 0.1
                    fy[j] += dy * 0.1

                # Update positions
                x += fx * 0.01
                y += fy * 0.01

        return {node: (x[i], y[i]) for i, node in enumerate(self.nodes)}

    def create_trace(self) -> List[go.Scatter]:
        """Create Plotly Scatter traces for graph."""
        traces = []

        # Edge traces
        edge_x = []
        edge_y = []
        for source, target in self.edges:
            x0, y0 = self.positions[source]
            x1, y1 = self.positions[target]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            mode='lines',
            line=dict(width=self.edge_width if isinstance(self.edge_width, int) else 1, color='#888'),
            hoverinfo='none',
            showlegend=False
        )
        traces.append(edge_trace)

        # Node trace
        node_x = [self.positions[node][0] for node in self.nodes]
        node_y = [self.positions[node][1] for node in self.nodes]

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers+text',
            marker=dict(
                size=self.node_size if isinstance(self.node_size, int) else self.node_size,
                color=self.node_color if self.node_color else '#3498db',
                line=dict(width=2, color='white')
            ),
            text=self.node_labels,
            textposition="top center",
            hoverinfo='text',
            showlegend=False
        )
        traces.append(node_trace)

        return traces

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure."""
        traces = self.create_trace()

        layout = go.Layout(
            title=self.title,
            showlegend=False,
            hovermode='closest',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            **self._get_theme_layout()
        )

        fig = go.Figure(data=traces, layout=layout)
        return fig


def network_graph(
    nodes: Union[List, pd.DataFrame],
    edges: Union[List[tuple], pd.DataFrame],
    node_labels: Optional[List] = None,
    node_size: Union[int, List] = 10,
    node_color: Union[str, List] = None,
    edge_width: Union[int, List] = 1,
    layout: str = "spring",
    title: Optional[str] = None,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> NetworkGraph:
    """
    Create a network graph.

    Args:
        nodes: List of node IDs
        edges: List of (source, target) tuples
        node_labels: Node labels
        node_size: Node size
        node_color: Node color
        edge_width: Edge width
        layout: Layout algorithm
        title: Chart title
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        NetworkGraph instance

    Examples:
        >>> import vizforge as vz
        >>>
        >>> # Social network
        >>> nodes = ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
        >>> edges = [
        >>>     ('Alice', 'Bob'),
        >>>     ('Bob', 'Charlie'),
        >>>     ('Charlie', 'David'),
        >>>     ('David', 'Eve'),
        >>>     ('Eve', 'Alice')
        >>> ]
        >>>
        >>> vz.network_graph(nodes, edges, title='Friend Network')
    """
    chart = NetworkGraph(
        nodes=nodes,
        edges=edges,
        node_labels=node_labels,
        node_size=node_size,
        node_color=node_color,
        edge_width=edge_width,
        layout=layout,
        title=title,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart
