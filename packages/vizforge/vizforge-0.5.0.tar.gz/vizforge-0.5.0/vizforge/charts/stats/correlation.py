"""Correlation Matrix implementation for VizForge."""

from typing import Optional, List, Union
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
import numpy as np

from ...core.base import BaseChart
from ...core.theme import Theme


class CorrelationMatrix(BaseChart):
    """
    Correlation Matrix visualization.

    Shows correlation coefficients between variables with heatmap.
    Perfect for feature selection, multicollinearity detection, EDA.

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>> import numpy as np
        >>>
        >>> # Feature correlation
        >>> df = pd.DataFrame({
        >>>     'feature1': np.random.randn(100),
        >>>     'feature2': np.random.randn(100),
        >>>     'feature3': np.random.randn(100),
        >>>     'target': np.random.randn(100)
        >>> })
        >>>
        >>> vz.correlation_matrix(df, title='Feature Correlations')
    """

    def __init__(
        self,
        data: pd.DataFrame,
        method: str = 'pearson',  # 'pearson', 'spearman', 'kendall'
        colorscale: str = 'RdBu',
        show_values: bool = True,
        dendrograms: bool = False,
        title: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize Correlation Matrix.

        Args:
            data: DataFrame
            method: Correlation method
            colorscale: Color scale
            show_values: Show correlation values
            dendrograms: Show hierarchical clustering
            title: Chart title
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        self.data = data
        self.method = method
        self.colorscale = colorscale
        self.show_values = show_values
        self.dendrograms = dendrograms

        # Calculate correlation matrix
        self.corr_matrix = data.corr(method=method)

    def create_trace(self) -> go.Heatmap:
        """Create correlation heatmap trace."""
        # Prepare annotations for values
        annotations = []
        if self.show_values:
            for i, row in enumerate(self.corr_matrix.values):
                for j, value in enumerate(row):
                    annotations.append(
                        dict(
                            x=self.corr_matrix.columns[j],
                            y=self.corr_matrix.index[i],
                            text=f'{value:.2f}',
                            showarrow=False,
                            font=dict(color='white' if abs(value) > 0.5 else 'black')
                        )
                    )

        heatmap = go.Heatmap(
            z=self.corr_matrix.values,
            x=self.corr_matrix.columns,
            y=self.corr_matrix.index,
            colorscale=self.colorscale,
            zmid=0,
            zmin=-1,
            zmax=1,
            text=self.corr_matrix.values,
            hovertemplate='%{x} vs %{y}<br>Correlation: %{z:.3f}<extra></extra>',
            colorbar=dict(title='Correlation')
        )

        return heatmap, annotations

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure."""
        if self.dendrograms:
            # Use figure_factory for dendrogram clustering
            fig = ff.create_dendrogram(
                self.corr_matrix.values,
                labels=self.corr_matrix.columns.tolist()
            )
            # This is complex - simplified version without dendrograms for now
            pass

        heatmap, annotations = self.create_trace()

        layout = go.Layout(
            title=self.title,
            xaxis=dict(title='Features'),
            yaxis=dict(title='Features'),
            annotations=annotations if self.show_values else None,
            **self._get_theme_layout()
        )

        fig = go.Figure(data=[heatmap], layout=layout)
        return fig


def correlation_matrix(
    data: pd.DataFrame,
    method: str = 'pearson',
    colorscale: str = 'RdBu',
    show_values: bool = True,
    dendrograms: bool = False,
    title: Optional[str] = None,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> CorrelationMatrix:
    """
    Create a correlation matrix.

    Args:
        data: DataFrame
        method: Correlation method
        colorscale: Color scale
        show_values: Show values
        dendrograms: Show dendrograms
        title: Chart title
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        CorrelationMatrix instance

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>> import numpy as np
        >>>
        >>> # Stock correlations
        >>> stocks = pd.DataFrame({
        >>>     'AAPL': np.random.randn(252),
        >>>     'GOOGL': np.random.randn(252),
        >>>     'MSFT': np.random.randn(252),
        >>>     'AMZN': np.random.randn(252),
        >>>     'TSLA': np.random.randn(252)
        >>> })
        >>>
        >>> vz.correlation_matrix(stocks, method='pearson',
        >>>                      title='Stock Price Correlations')
    """
    chart = CorrelationMatrix(
        data=data,
        method=method,
        colorscale=colorscale,
        show_values=show_values,
        dendrograms=dendrograms,
        title=title,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart
