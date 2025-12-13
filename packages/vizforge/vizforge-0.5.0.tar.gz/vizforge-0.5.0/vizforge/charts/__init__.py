"""Chart types for VizForge (2D, 3D, Geographic, Network, Real-time, Statistical, Advanced)."""

# 2D Charts
from .line import LineChart, line
from .bar import BarChart, bar
from .area import AreaChart, area
from .scatter import ScatterPlot, scatter
from .pie import PieChart, pie, donut
from .heatmap import Heatmap, heatmap
from .histogram import Histogram, histogram
from .boxplot import Boxplot, boxplot
from .radar import RadarChart, radar
from .waterfall import WaterfallChart, waterfall
from .funnel import FunnelChart, funnel
from .bubble import BubbleChart, bubble

# 3D Charts
from .threed import (
    SurfacePlot, surface,
    Scatter3D, scatter3d,
    Mesh3D, mesh3d,
    VolumePlot, volume,
    ConePlot, cone,
    IsosurfacePlot, isosurface,
)

# Geographic Charts
from .geo import (
    ChoroplethMap, choropleth,
    ScatterGeoMap, scattergeo,
    LineGeoMap, linegeo,
    DensityGeoMap, densitygeo,
    FlowMap, flowmap,
)

# Network Charts
from .network import (
    NetworkGraph, network_graph,
    SankeyDiagram, sankey,
    TreeDiagram, IcicleDiagram, tree, icicle,
    Dendrogram, ClusterHeatmap, dendrogram, cluster_heatmap,
)

# Real-time Charts
from .realtime import (
    StreamingLine, streaming_line,
    LiveHeatmap, live_heatmap,
    AnimatedScatter, animated_scatter,
    AnimatedBar, animated_bar,
    AnimatedChoropleth, animated_choropleth,
)

# Statistical Charts
from .stats import (
    ViolinPlot, violin,
    KDEPlot, KDE2D, kde, kde2d,
    RegressionPlot, regression,
    CorrelationMatrix, correlation_matrix,
    ROCCurve, MultiROCCurve, roc_curve_plot, multi_roc_curve,
    FeatureImportance, PermutationImportance, feature_importance, permutation_importance,
)

# Advanced Charts
from .advanced import (
    Treemap, treemap,
    Sunburst, sunburst,
    ParallelCoordinates, parallel_coordinates,
    ContourPlot, FilledContour, contour, filled_contour,
)

__all__ = [
    # 2D Chart Classes
    "LineChart",
    "BarChart",
    "AreaChart",
    "ScatterPlot",
    "PieChart",
    "Heatmap",
    "Histogram",
    "Boxplot",
    "RadarChart",
    "WaterfallChart",
    "FunnelChart",
    "BubbleChart",
    # 3D Chart Classes
    "SurfacePlot",
    "Scatter3D",
    "Mesh3D",
    "VolumePlot",
    "ConePlot",
    "IsosurfacePlot",
    # Geographic Chart Classes
    "ChoroplethMap",
    "ScatterGeoMap",
    "LineGeoMap",
    "DensityGeoMap",
    "FlowMap",
    # Network Chart Classes
    "NetworkGraph",
    "SankeyDiagram",
    "TreeDiagram",
    "IcicleDiagram",
    "Dendrogram",
    "ClusterHeatmap",
    # Real-time Chart Classes
    "StreamingLine",
    "LiveHeatmap",
    "AnimatedScatter",
    "AnimatedBar",
    "AnimatedChoropleth",
    # Statistical Chart Classes
    "ViolinPlot",
    "KDEPlot",
    "KDE2D",
    "RegressionPlot",
    "CorrelationMatrix",
    "ROCCurve",
    "MultiROCCurve",
    "FeatureImportance",
    "PermutationImportance",
    # Advanced Chart Classes
    "Treemap",
    "Sunburst",
    "ParallelCoordinates",
    "ContourPlot",
    "FilledContour",
    # 2D Functions
    "line",
    "bar",
    "area",
    "scatter",
    "pie",
    "donut",
    "heatmap",
    "histogram",
    "boxplot",
    "radar",
    "waterfall",
    "funnel",
    "bubble",
    # 3D Functions
    "surface",
    "scatter3d",
    "mesh3d",
    "volume",
    "cone",
    "isosurface",
    # Geographic Functions
    "choropleth",
    "scattergeo",
    "linegeo",
    "densitygeo",
    "flowmap",
    # Network Functions
    "network_graph",
    "sankey",
    "tree",
    "icicle",
    "dendrogram",
    "cluster_heatmap",
    # Real-time Functions
    "streaming_line",
    "live_heatmap",
    "animated_scatter",
    "animated_bar",
    "animated_choropleth",
    # Statistical Functions
    "violin",
    "kde",
    "kde2d",
    "regression",
    "correlation_matrix",
    "roc_curve_plot",
    "multi_roc_curve",
    "feature_importance",
    "permutation_importance",
    # Advanced Functions
    "treemap",
    "sunburst",
    "parallel_coordinates",
    "contour",
    "filled_contour",
]
