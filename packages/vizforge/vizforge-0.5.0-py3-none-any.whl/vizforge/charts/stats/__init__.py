"""Statistical chart types for VizForge."""

from .violin import ViolinPlot, violin
from .kde import KDEPlot, KDE2D, kde, kde2d
from .regression import RegressionPlot, regression
from .correlation import CorrelationMatrix, correlation_matrix
from .roc import ROCCurve, MultiROCCurve, roc_curve_plot, multi_roc_curve
from .feature_importance import (
    FeatureImportance, PermutationImportance,
    feature_importance, permutation_importance
)

__all__ = [
    # Classes
    "ViolinPlot",
    "KDEPlot",
    "KDE2D",
    "RegressionPlot",
    "CorrelationMatrix",
    "ROCCurve",
    "MultiROCCurve",
    "FeatureImportance",
    "PermutationImportance",
    # Functions
    "violin",
    "kde",
    "kde2d",
    "regression",
    "correlation_matrix",
    "roc_curve_plot",
    "multi_roc_curve",
    "feature_importance",
    "permutation_importance",
]
