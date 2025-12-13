"""Feature Importance Plot implementation for VizForge."""

from typing import Optional, List, Union, Dict
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from ...core.base import BaseChart
from ...core.theme import Theme


class FeatureImportance(BaseChart):
    """
    Feature Importance visualization.

    Shows relative importance of features in machine learning models.
    Perfect for model interpretation, feature selection, explainability.

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>>
        >>> # Random forest feature importance
        >>> features = ['age', 'income', 'education', 'experience', 'score']
        >>> importance = [0.35, 0.28, 0.18, 0.12, 0.07]
        >>>
        >>> vz.feature_importance(features, importance,
        >>>                      title='Feature Importance')
    """

    def __init__(
        self,
        features: Union[List[str], pd.Series],
        importance: Union[List[float], np.ndarray, pd.Series],
        orientation: str = 'h',  # 'h' or 'v'
        top_n: Optional[int] = None,
        show_values: bool = True,
        title: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize Feature Importance plot.

        Args:
            features: Feature names
            importance: Importance values
            orientation: 'h' (horizontal) or 'v' (vertical)
            top_n: Show only top N features
            show_values: Show importance values
            title: Chart title
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        # Create DataFrame and sort by importance
        df = pd.DataFrame({
            'feature': features,
            'importance': importance
        }).sort_values('importance', ascending=False)

        if top_n:
            df = df.head(top_n)

        self.features = df['feature'].tolist()
        self.importance = df['importance'].tolist()
        self.orientation = orientation
        self.show_values = show_values

    def create_trace(self) -> go.Bar:
        """Create feature importance bar trace."""
        if self.orientation == 'h':
            # Reverse for horizontal (top to bottom)
            features = self.features[::-1]
            importance = self.importance[::-1]

            bar = go.Bar(
                x=importance,
                y=features,
                orientation='h',
                marker=dict(
                    color=importance,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title='Importance')
                ),
                text=[f'{val:.3f}' for val in importance] if self.show_values else None,
                textposition='outside',
                hovertemplate='%{y}<br>Importance: %{x:.3f}<extra></extra>'
            )
        else:
            bar = go.Bar(
                x=self.features,
                y=self.importance,
                orientation='v',
                marker=dict(
                    color=self.importance,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title='Importance')
                ),
                text=[f'{val:.3f}' for val in self.importance] if self.show_values else None,
                textposition='outside',
                hovertemplate='%{x}<br>Importance: %{y:.3f}<extra></extra>'
            )

        return bar

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure."""
        trace = self.create_trace()

        layout = go.Layout(
            title=self.title,
            xaxis=dict(title='Importance' if self.orientation == 'h' else 'Features'),
            yaxis=dict(title='Features' if self.orientation == 'h' else 'Importance'),
            showlegend=False,
            **self._get_theme_layout()
        )

        fig = go.Figure(data=[trace], layout=layout)
        return fig


class PermutationImportance(BaseChart):
    """
    Permutation Feature Importance with error bars.

    Shows feature importance with uncertainty estimates.
    Perfect for robust feature selection.
    """

    def __init__(
        self,
        features: List[str],
        importance_mean: Union[List[float], np.ndarray],
        importance_std: Union[List[float], np.ndarray],
        orientation: str = 'h',
        top_n: Optional[int] = None,
        title: Optional[str] = None,
        **kwargs
    ):
        """Initialize Permutation Importance plot."""
        super().__init__(title=title, **kwargs)

        # Create DataFrame and sort
        df = pd.DataFrame({
            'feature': features,
            'mean': importance_mean,
            'std': importance_std
        }).sort_values('mean', ascending=False)

        if top_n:
            df = df.head(top_n)

        self.features = df['feature'].tolist()
        self.mean = df['mean'].tolist()
        self.std = df['std'].tolist()
        self.orientation = orientation

    def create_trace(self) -> go.Bar:
        """Create permutation importance trace with error bars."""
        if self.orientation == 'h':
            features = self.features[::-1]
            mean = self.mean[::-1]
            std = self.std[::-1]

            bar = go.Bar(
                x=mean,
                y=features,
                orientation='h',
                error_x=dict(type='data', array=std),
                marker=dict(color='#3498db'),
                hovertemplate='%{y}<br>Mean: %{x:.3f}<br>Std: %{error_x.array:.3f}<extra></extra>'
            )
        else:
            bar = go.Bar(
                x=self.features,
                y=self.mean,
                orientation='v',
                error_y=dict(type='data', array=self.std),
                marker=dict(color='#3498db'),
                hovertemplate='%{x}<br>Mean: %{y:.3f}<br>Std: %{error_y.array:.3f}<extra></extra>'
            )

        return bar

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure."""
        trace = self.create_trace()

        layout = go.Layout(
            title=self.title,
            xaxis=dict(title='Importance' if self.orientation == 'h' else 'Features'),
            yaxis=dict(title='Features' if self.orientation == 'h' else 'Importance'),
            showlegend=False,
            **self._get_theme_layout()
        )

        fig = go.Figure(data=[trace], layout=layout)
        return fig


def feature_importance(
    features: Union[List[str], pd.Series],
    importance: Union[List[float], np.ndarray, pd.Series],
    orientation: str = 'h',
    top_n: Optional[int] = None,
    show_values: bool = True,
    title: Optional[str] = None,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> FeatureImportance:
    """
    Create a feature importance plot.

    Args:
        features: Feature names
        importance: Importance values
        orientation: 'h' or 'v'
        top_n: Show top N
        show_values: Show values
        title: Chart title
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        FeatureImportance instance

    Examples:
        >>> import vizforge as vz
        >>> from sklearn.ensemble import RandomForestClassifier
        >>> from sklearn.datasets import make_classification
        >>>
        >>> # Train model and get importance
        >>> X, y = make_classification(n_samples=1000, n_features=20)
        >>> model = RandomForestClassifier()
        >>> model.fit(X, y)
        >>>
        >>> features = [f'Feature {i}' for i in range(20)]
        >>> importance = model.feature_importances_
        >>>
        >>> vz.feature_importance(features, importance, top_n=10,
        >>>                      title='Top 10 Features')
    """
    chart = FeatureImportance(
        features=features,
        importance=importance,
        orientation=orientation,
        top_n=top_n,
        show_values=show_values,
        title=title,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart


def permutation_importance(
    features: List[str],
    importance_mean: Union[List[float], np.ndarray],
    importance_std: Union[List[float], np.ndarray],
    orientation: str = 'h',
    top_n: Optional[int] = None,
    title: Optional[str] = None,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> PermutationImportance:
    """
    Create a permutation importance plot.

    Args:
        features: Feature names
        importance_mean: Mean importance
        importance_std: Std importance
        orientation: 'h' or 'v'
        top_n: Show top N
        title: Chart title
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        PermutationImportance instance

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>>
        >>> features = [f'Feature {i}' for i in range(15)]
        >>> mean = np.random.rand(15) * 0.1
        >>> std = np.random.rand(15) * 0.02
        >>>
        >>> vz.permutation_importance(features, mean, std,
        >>>                          title='Permutation Importance')
    """
    chart = PermutationImportance(
        features=features,
        importance_mean=importance_mean,
        importance_std=importance_std,
        orientation=orientation,
        top_n=top_n,
        title=title,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart
