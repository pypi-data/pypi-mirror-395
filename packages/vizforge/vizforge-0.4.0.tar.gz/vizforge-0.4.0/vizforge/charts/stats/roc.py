"""ROC Curve implementation for VizForge."""

from typing import Optional, List, Union, Tuple
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc, roc_auc_score

from ...core.base import BaseChart
from ...core.theme import Theme


class ROCCurve(BaseChart):
    """
    ROC (Receiver Operating Characteristic) Curve.

    Shows classification model performance across different thresholds.
    Perfect for binary classification evaluation, model comparison.

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>>
        >>> # Binary classification results
        >>> y_true = np.random.randint(0, 2, 1000)
        >>> y_scores = np.random.rand(1000)
        >>>
        >>> vz.roc_curve(y_true, y_scores, title='Model Performance')
    """

    def __init__(
        self,
        y_true: Union[np.ndarray, List],
        y_scores: Union[np.ndarray, List],
        model_name: str = 'Model',
        show_diagonal: bool = True,
        title: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize ROC Curve.

        Args:
            y_true: True binary labels
            y_scores: Predicted scores/probabilities
            model_name: Model name for legend
            show_diagonal: Show random classifier diagonal
            title: Chart title
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        self.y_true = np.array(y_true)
        self.y_scores = np.array(y_scores)
        self.model_name = model_name
        self.show_diagonal = show_diagonal

        # Calculate ROC curve
        self.fpr, self.tpr, self.thresholds = roc_curve(self.y_true, self.y_scores)
        self.auc_score = auc(self.fpr, self.tpr)

    def create_trace(self) -> List[go.Scatter]:
        """Create ROC curve traces."""
        traces = []

        # ROC curve
        roc_trace = go.Scatter(
            x=self.fpr,
            y=self.tpr,
            mode='lines',
            name=f'{self.model_name} (AUC = {self.auc_score:.3f})',
            line=dict(color='#3498db', width=2),
            hovertemplate='FPR: %{x:.3f}<br>TPR: %{y:.3f}<extra></extra>'
        )
        traces.append(roc_trace)

        # Diagonal (random classifier)
        if self.show_diagonal:
            diagonal = go.Scatter(
                x=[0, 1],
                y=[0, 1],
                mode='lines',
                name='Random (AUC = 0.500)',
                line=dict(color='#95a5a6', width=1, dash='dash'),
                showlegend=True
            )
            traces.append(diagonal)

        return traces

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure."""
        traces = self.create_trace()

        layout = go.Layout(
            title=self.title,
            xaxis=dict(
                title='False Positive Rate',
                range=[0, 1]
            ),
            yaxis=dict(
                title='True Positive Rate',
                range=[0, 1]
            ),
            hovermode='closest',
            **self._get_theme_layout()
        )

        fig = go.Figure(data=traces, layout=layout)

        # Add square aspect ratio
        fig.update_yaxes(scaleanchor="x", scaleratio=1)

        return fig


class MultiROCCurve(BaseChart):
    """
    Multiple ROC Curves for model comparison.

    Shows multiple ROC curves on the same plot.
    Perfect for comparing multiple classifiers.
    """

    def __init__(
        self,
        models: List[Tuple[str, np.ndarray, np.ndarray]],  # (name, y_true, y_scores)
        show_diagonal: bool = True,
        title: Optional[str] = None,
        **kwargs
    ):
        """Initialize Multiple ROC Curves."""
        super().__init__(title=title, **kwargs)

        self.models = models
        self.show_diagonal = show_diagonal

        # Calculate ROC curves for all models
        self.roc_data = []
        for name, y_true, y_scores in models:
            fpr, tpr, _ = roc_curve(y_true, y_scores)
            auc_score = auc(fpr, tpr)
            self.roc_data.append((name, fpr, tpr, auc_score))

    def create_trace(self) -> List[go.Scatter]:
        """Create multiple ROC curve traces."""
        traces = []

        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']

        # ROC curves
        for i, (name, fpr, tpr, auc_score) in enumerate(self.roc_data):
            trace = go.Scatter(
                x=fpr,
                y=tpr,
                mode='lines',
                name=f'{name} (AUC = {auc_score:.3f})',
                line=dict(color=colors[i % len(colors)], width=2)
            )
            traces.append(trace)

        # Diagonal
        if self.show_diagonal:
            diagonal = go.Scatter(
                x=[0, 1],
                y=[0, 1],
                mode='lines',
                name='Random (AUC = 0.500)',
                line=dict(color='#95a5a6', width=1, dash='dash')
            )
            traces.append(diagonal)

        return traces

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure."""
        traces = self.create_trace()

        layout = go.Layout(
            title=self.title,
            xaxis=dict(title='False Positive Rate', range=[0, 1]),
            yaxis=dict(title='True Positive Rate', range=[0, 1]),
            hovermode='closest',
            **self._get_theme_layout()
        )

        fig = go.Figure(data=traces, layout=layout)
        fig.update_yaxes(scaleanchor="x", scaleratio=1)

        return fig


def roc_curve_plot(
    y_true: Union[np.ndarray, List],
    y_scores: Union[np.ndarray, List],
    model_name: str = 'Model',
    show_diagonal: bool = True,
    title: Optional[str] = None,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> ROCCurve:
    """
    Create a ROC curve.

    Args:
        y_true: True labels
        y_scores: Predicted scores
        model_name: Model name
        show_diagonal: Show diagonal
        title: Chart title
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        ROCCurve instance

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>> from sklearn.datasets import make_classification
        >>> from sklearn.linear_model import LogisticRegression
        >>>
        >>> # Generate data and train model
        >>> X, y = make_classification(n_samples=1000, random_state=42)
        >>> model = LogisticRegression()
        >>> model.fit(X, y)
        >>> y_scores = model.predict_proba(X)[:, 1]
        >>>
        >>> vz.roc_curve_plot(y, y_scores,
        >>>                  model_name='Logistic Regression',
        >>>                  title='ROC Curve Analysis')
    """
    chart = ROCCurve(
        y_true=y_true,
        y_scores=y_scores,
        model_name=model_name,
        show_diagonal=show_diagonal,
        title=title,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart


def multi_roc_curve(
    models: List[Tuple[str, np.ndarray, np.ndarray]],
    show_diagonal: bool = True,
    title: Optional[str] = None,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> MultiROCCurve:
    """
    Create multiple ROC curves for comparison.

    Args:
        models: List of (name, y_true, y_scores) tuples
        show_diagonal: Show diagonal
        title: Chart title
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        MultiROCCurve instance

    Examples:
        >>> import vizforge as vz
        >>> import numpy as np
        >>>
        >>> # Compare multiple models
        >>> y_true = np.random.randint(0, 2, 1000)
        >>> models = [
        >>>     ('Model A', y_true, np.random.rand(1000)),
        >>>     ('Model B', y_true, np.random.rand(1000)),
        >>>     ('Model C', y_true, np.random.rand(1000))
        >>> ]
        >>>
        >>> vz.multi_roc_curve(models, title='Model Comparison')
    """
    chart = MultiROCCurve(
        models=models,
        show_diagonal=show_diagonal,
        title=title,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart
