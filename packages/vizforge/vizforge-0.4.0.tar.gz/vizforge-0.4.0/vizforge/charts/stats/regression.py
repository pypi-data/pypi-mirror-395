"""Regression Plot implementation for VizForge."""

from typing import Optional, List, Union
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from scipy import stats

from ...core.base import BaseChart
from ...core.theme import Theme


class RegressionPlot(BaseChart):
    """
    Regression Plot visualization.

    Shows scatter plot with regression line and confidence interval.
    Perfect for trend analysis, prediction visualization, correlation analysis.

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>> import numpy as np
        >>>
        >>> # Sales vs advertising
        >>> df = pd.DataFrame({
        >>>     'advertising': np.random.randint(1000, 10000, 100),
        >>>     'sales': lambda df: df['advertising'] * 0.5 + np.random.normal(0, 500, 100)
        >>> })
        >>>
        >>> vz.regression(df, x='advertising', y='sales',
        >>>              title='Sales vs Advertising Spend')
    """

    def __init__(
        self,
        data: Union[pd.DataFrame, Dict],
        x: str,
        y: str,
        order: int = 1,  # Polynomial order
        ci: int = 95,  # Confidence interval
        show_equation: bool = True,
        title: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize Regression Plot.

        Args:
            data: DataFrame
            x: X-axis column
            y: Y-axis column
            order: Polynomial order (1=linear, 2=quadratic, etc.)
            ci: Confidence interval (%)
            show_equation: Show regression equation
            title: Chart title
            **kwargs: Additional arguments
        """
        super().__init__(title=title, **kwargs)

        if isinstance(data, dict):
            data = pd.DataFrame(data)

        self.data = data
        self.x = x
        self.y = y
        self.order = order
        self.ci = ci
        self.show_equation = show_equation

        # Calculate regression
        self.x_vals = data[x].values
        self.y_vals = data[y].values
        self._fit_regression()

    def _fit_regression(self):
        """Fit regression model."""
        # Polynomial regression
        self.coeffs = np.polyfit(self.x_vals, self.y_vals, self.order)
        self.poly = np.poly1d(self.coeffs)

        # Prediction
        self.x_pred = np.linspace(self.x_vals.min(), self.x_vals.max(), 100)
        self.y_pred = self.poly(self.x_pred)

        # R-squared
        ss_res = np.sum((self.y_vals - self.poly(self.x_vals))**2)
        ss_tot = np.sum((self.y_vals - np.mean(self.y_vals))**2)
        self.r_squared = 1 - (ss_res / ss_tot)

        # Confidence interval (simplified)
        residuals = self.y_vals - self.poly(self.x_vals)
        std_error = np.std(residuals)
        z_score = stats.norm.ppf(1 - (1 - self.ci/100) / 2)
        self.ci_lower = self.y_pred - z_score * std_error
        self.ci_upper = self.y_pred + z_score * std_error

    def create_trace(self) -> List[go.Scatter]:
        """Create regression plot traces."""
        traces = []

        # Scatter points
        scatter = go.Scatter(
            x=self.x_vals,
            y=self.y_vals,
            mode='markers',
            name='Data',
            marker=dict(size=8, color='#3498db', opacity=0.6)
        )
        traces.append(scatter)

        # Regression line
        regression_line = go.Scatter(
            x=self.x_pred,
            y=self.y_pred,
            mode='lines',
            name=f'Regression (R²={self.r_squared:.3f})',
            line=dict(color='#e74c3c', width=2)
        )
        traces.append(regression_line)

        # Confidence interval
        ci_upper = go.Scatter(
            x=self.x_pred,
            y=self.ci_upper,
            mode='lines',
            name=f'{self.ci}% CI',
            line=dict(width=0),
            showlegend=False
        )
        ci_lower = go.Scatter(
            x=self.x_pred,
            y=self.ci_lower,
            mode='lines',
            fill='tonexty',
            fillcolor='rgba(231, 76, 60, 0.2)',
            line=dict(width=0),
            name=f'{self.ci}% CI',
            showlegend=True
        )
        traces.extend([ci_upper, ci_lower])

        return traces

    def create_figure(self) -> go.Figure:
        """Create complete Plotly figure."""
        traces = self.create_trace()

        # Build equation string
        equation = ""
        if self.show_equation:
            if self.order == 1:
                equation = f"y = {self.coeffs[0]:.2f}x + {self.coeffs[1]:.2f}"
            else:
                terms = [f"{self.coeffs[i]:.2f}x^{self.order-i}"
                        for i in range(self.order)]
                terms.append(f"{self.coeffs[-1]:.2f}")
                equation = "y = " + " + ".join(terms)

        layout = go.Layout(
            title=f"{self.title}<br><sub>{equation}</sub>" if self.show_equation else self.title,
            xaxis=dict(title=self.x),
            yaxis=dict(title=self.y),
            hovermode='closest',
            **self._get_theme_layout()
        )

        fig = go.Figure(data=traces, layout=layout)
        return fig


def regression(
    data: Union[pd.DataFrame, Dict],
    x: str,
    y: str,
    order: int = 1,
    ci: int = 95,
    show_equation: bool = True,
    title: Optional[str] = None,
    theme: Optional[str] = None,
    show: bool = True,
    export: Optional[str] = None,
    **kwargs
) -> RegressionPlot:
    """
    Create a regression plot.

    Args:
        data: DataFrame
        x: X-axis column
        y: Y-axis column
        order: Polynomial order
        ci: Confidence interval
        show_equation: Show equation
        title: Chart title
        theme: Theme name
        show: Whether to display
        export: Export path
        **kwargs: Additional arguments

    Returns:
        RegressionPlot instance

    Examples:
        >>> import vizforge as vz
        >>> import pandas as pd
        >>> import numpy as np
        >>>
        >>> # Housing price prediction
        >>> df = pd.DataFrame({
        >>>     'sqft': np.random.randint(800, 3000, 200),
        >>>     'price': lambda df: df['sqft'] * 150 + np.random.normal(0, 20000, 200)
        >>> })
        >>>
        >>> vz.regression(df, x='sqft', y='price',
        >>>              title='House Price vs Square Footage',
        >>>              show_equation=True)
    """
    chart = RegressionPlot(
        data=data,
        x=x,
        y=y,
        order=order,
        ci=ci,
        show_equation=show_equation,
        title=title,
        theme=theme,
        **kwargs
    )

    if export:
        chart.export(export)

    if show:
        chart.show()

    return chart
