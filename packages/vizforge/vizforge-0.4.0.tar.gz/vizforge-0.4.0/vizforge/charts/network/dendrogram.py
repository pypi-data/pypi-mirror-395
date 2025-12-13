"""Dendrogram implementation for VizForge."""

from typing import Optional, List, Dict, Union
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
import numpy as np

from ...core.base import BaseChart
from ...core.theme import Theme


class Dendrogram(BaseChart):
    """
    Dendrogram visualization (hierarchical clustering).

    Shows hierarchical clustering of data points or features.
    Perfect for clustering analysis, phylogenetic trees, similarity analysis.

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>>
        >>> # Feature clustering
        >>> data = np.random.randn(10, 5)
        >>> labels = [f'Sample {i}' for i in range(10)]
        >>>
        >>> vz.dendrogram(data, labels, title='Hierarchical Clustering')
    """

    def __init__(
        self,
        data: Union[np.ndarray, pd.DataFrame, List[List[float]]],
        labels: Optional[List[str]] = None,
        orientation: str = 'bottom',  # 'bottom', 'top', 'left', 'right'
        linkagefun: callable = None,
        distfun: callable = None,
        color_threshold: Optional[float] = None,
        title: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize Dendrogram.

        Args:
            data: Data matrix (samples x features) or distance matrix
            labels: Sample labels
            orientation: Dendrogram orientation
            linkagefun: Linkage function for hierarchical clustering
            distfun: Distance function
            color_threshold: Threshold for coloring clusters
            title: Chart title
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        # Convert data to numpy array
        if isinstance(data, pd.DataFrame):
            self.data = data.values
            self.labels = labels or data.index.tolist()
        else:
            self.data = np.array(data)
            self.labels = labels or [f'Sample {i}' for i in range(len(data))]

        self.orientation = orientation
        self.linkagefun = linkagefun
        self.distfun = distfun
        self.color_threshold = color_threshold

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure using figure_factory."""
        # Use Plotly's figure_factory for dendrogram
        fig = ff.create_dendrogram(
            self.data,
            orientation=self.orientation,
            labels=self.labels,
            linkagefun=self.linkagefun,
            distfun=self.distfun,
            color_threshold=self.color_threshold
        )

        # Update layout with theme and title
        fig.update_layout(
            title=self.title,
            xaxis_title='Samples' if self.orientation in ['bottom', 'top'] else 'Distance',
            yaxis_title='Distance' if self.orientation in ['bottom', 'top'] else 'Samples',
            **self._get_theme_layout()
        )

        return fig


class ClusterHeatmap(BaseChart):
    """
    Clustered Heatmap with dendrograms.

    Combines heatmap with hierarchical clustering dendrograms.
    Perfect for gene expression analysis, feature correlation with clustering.
    """

    def __init__(
        self,
        data: Union[np.ndarray, pd.DataFrame],
        row_labels: Optional[List[str]] = None,
        col_labels: Optional[List[str]] = None,
        colorscale: str = 'RdBu',
        show_dendrograms: str = 'both',  # 'both', 'row', 'col', 'none'
        title: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize Clustered Heatmap.

        Args:
            data: Data matrix
            row_labels: Row labels
            col_labels: Column labels
            colorscale: Color scale
            show_dendrograms: Which dendrograms to show
            title: Chart title
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        if isinstance(data, pd.DataFrame):
            self.data = data.values
            self.row_labels = row_labels or data.index.tolist()
            self.col_labels = col_labels or data.columns.tolist()
        else:
            self.data = np.array(data)
            self.row_labels = row_labels or [f'Row {i}' for i in range(data.shape[0])]
            self.col_labels = col_labels or [f'Col {i}' for i in range(data.shape[1])]

        self.colorscale = colorscale
        self.show_dendrograms = show_dendrograms

    def create_figure(self) -> go.Figure:
        """Create clustered heatmap with dendrograms."""
        # Create dendrograms if needed
        if self.show_dendrograms in ['both', 'row']:
            # Row dendrogram
            row_dendro = ff.create_dendrogram(
                self.data,
                orientation='left',
                labels=self.row_labels
            )
            row_order = [int(x) for x in row_dendro['layout']['yaxis']['ticktext']]
        else:
            row_order = list(range(len(self.row_labels)))

        if self.show_dendrograms in ['both', 'col']:
            # Column dendrogram
            col_dendro = ff.create_dendrogram(
                self.data.T,
                orientation='bottom',
                labels=self.col_labels
            )
            col_order = [int(x) for x in col_dendro['layout']['xaxis']['ticktext']]
        else:
            col_order = list(range(len(self.col_labels)))

        # Reorder data based on clustering
        ordered_data = self.data[row_order, :][:, col_order]
        ordered_row_labels = [self.row_labels[i] for i in row_order]
        ordered_col_labels = [self.col_labels[i] for i in col_order]

        # Create heatmap
        heatmap = go.Heatmap(
            z=ordered_data,
            x=ordered_col_labels,
            y=ordered_row_labels,
            colorscale=self.colorscale,
            hovertemplate='Row: %{y}<br>Col: %{x}<br>Value: %{z}<extra></extra>'
        )

        fig = go.Figure(data=[heatmap])

        fig.update_layout(
            title=self.title,
            xaxis_title='Features',
            yaxis_title='Samples',
            **self._get_theme_layout()
        )

        return fig


def dendrogram(
    data: Union[np.ndarray, pd.DataFrame, List[List[float]]],
    labels: Optional[List[str]] = None,
    orientation: str = 'bottom',
    linkagefun: callable = None,
    distfun: callable = None,
    color_threshold: Optional[float] = None,
    title: Optional[str] = None,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> Dendrogram:
    """
    Create a dendrogram.

    Args:
        data: Data matrix or distance matrix
        labels: Sample labels
        orientation: Dendrogram orientation
        linkagefun: Linkage function
        distfun: Distance function
        color_threshold: Color threshold
        title: Chart title
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        Dendrogram instance

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>>
        >>> # Customer segmentation
        >>> customer_data = np.random.randn(20, 5)
        >>> customer_labels = [f'Customer {i}' for i in range(20)]
        >>>
        >>> vz.dendrogram(
        >>>     customer_data,
        >>>     labels=customer_labels,
        >>>     title='Customer Clustering',
        >>>     orientation='left'
        >>> )
    """
    chart = Dendrogram(
        data=data,
        labels=labels,
        orientation=orientation,
        linkagefun=linkagefun,
        distfun=distfun,
        color_threshold=color_threshold,
        title=title,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart


def cluster_heatmap(
    data: Union[np.ndarray, pd.DataFrame],
    row_labels: Optional[List[str]] = None,
    col_labels: Optional[List[str]] = None,
    colorscale: str = 'RdBu',
    show_dendrograms: str = 'both',
    title: Optional[str] = None,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> ClusterHeatmap:
    """
    Create a clustered heatmap.

    Args:
        data: Data matrix
        row_labels: Row labels
        col_labels: Column labels
        colorscale: Color scale
        show_dendrograms: 'both', 'row', 'col', or 'none'
        title: Chart title
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        ClusterHeatmap instance

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>>
        >>> # Gene expression
        >>> expression_data = np.random.randn(50, 20)
        >>> genes = [f'Gene {i}' for i in range(50)]
        >>> samples = [f'Sample {i}' for i in range(20)]
        >>>
        >>> vz.cluster_heatmap(
        >>>     expression_data,
        >>>     row_labels=genes,
        >>>     col_labels=samples,
        >>>     title='Gene Expression Clustering'
        >>> )
    """
    chart = ClusterHeatmap(
        data=data,
        row_labels=row_labels,
        col_labels=col_labels,
        colorscale=colorscale,
        show_dendrograms=show_dendrograms,
        title=title,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart
