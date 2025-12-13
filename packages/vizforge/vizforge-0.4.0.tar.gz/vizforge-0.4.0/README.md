# VizForge

**Production-grade data visualization library with ZERO AI dependencies**

Create beautiful, interactive visualizations with a single line of code. No API keys, no paid services, just pure visualization power.

## Features (v0.4.0)

- 🎨 **Beautiful by Default** - Professional themes out of the box
- ⚡ **Simple API** - One-line visualizations: `vz.line(data, x, y)`
- 📊 **48 Chart Types** - 12 2D + 6 3D + 5 Geographic + 6 Network + 5 Real-time + 9 Statistical + 5 Advanced
- 🌍 **3D & Geographic** - Surface plots, scatter3D, choropleth maps, flow maps
- 🔗 **Network & Graphs** - Network graphs, Sankey, trees, dendrograms
- 📈 **Real-time & Animated** - Streaming data, live dashboards, animated transitions
- 📊 **Statistical Analysis** - Violin plots, KDE, regression, ROC curves, feature importance
- 🎭 **Theme System** - 5 built-in themes + custom themes
- 💾 **Export Anywhere** - HTML export (PNG, SVG, PDF coming soon)
- 🚀 **No AI Dependencies** - Completely free, no API keys needed
- 📈 **Performance** - Handle 100K+ data points efficiently

## Installation

```bash
pip install vizforge
```

## Quick Start

```python
import vizforge as vz
import pandas as pd
import numpy as np

# Line chart
data = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=30),
    'sales': np.random.randint(100, 200, 30)
})
vz.line(data, x='date', y='sales', title='Daily Sales')

# Statistical analysis
vz.violin(data, x='category', y='value', title='Distribution by Category')

# Network visualization
nodes = ['A', 'B', 'C', 'D']
edges = [('A', 'B'), ('B', 'C'), ('C', 'D')]
vz.network_graph(nodes, edges, title='Network')
```

## Chart Types (48 in v0.4.0)

### 2D Charts (12)
**Basic:**
- **Line Chart** - `vz.line()` - Time series, multi-line
- **Bar Chart** - `vz.bar()` - Grouped, stacked
- **Scatter Plot** - `vz.scatter()` - 2D scatter with colors
- **Pie Chart** - `vz.pie()` / `vz.donut()` - Proportions

**Statistical:**
- **Histogram** - `vz.histogram()` - Distribution with bins
- **Boxplot** - `vz.boxplot()` - Quartiles, outliers
- **Heatmap** - `vz.heatmap()` - Correlation matrices
- **Area Chart** - `vz.area()` - Filled areas, stacking

**Business:**
- **Waterfall** - `vz.waterfall()` - Sequential changes
- **Funnel** - `vz.funnel()` - Conversion stages
- **Radar** - `vz.radar()` - Multivariate data
- **Bubble** - `vz.bubble()` - 3-variable scatter

### 3D Charts (6)
- **Surface Plot** - `vz.surface()` - 3D surfaces, mathematical functions
- **Scatter3D** - `vz.scatter3d()` - 3D scatter with size/color
- **Mesh3D** - `vz.mesh3d()` - 3D geometry, CAD models
- **Volume Plot** - `vz.volume()` - Volumetric data, medical imaging
- **Cone Plot** - `vz.cone()` - Vector fields, fluid dynamics
- **Isosurface** - `vz.isosurface()` - Level sets, molecular orbitals

### Geographic Charts (5)
- **Choropleth Map** - `vz.choropleth()` - Color-coded regions
- **Scatter Geo** - `vz.scattergeo()` - Points on map
- **Line Geo** - `vz.linegeo()` - Routes, paths on map
- **Density Geo** - `vz.densitygeo()` - Heatmap on map
- **Flow Map** - `vz.flowmap()` - Origin-destination flows

### Network Charts (6) ✨ NEW
- **Network Graph** - `vz.network_graph()` - Force-directed graphs
- **Sankey Diagram** - `vz.sankey()` - Flow diagrams
- **Tree Diagram** - `vz.tree()` - Hierarchical trees
- **Icicle Diagram** - `vz.icicle()` - Vertical hierarchies
- **Dendrogram** - `vz.dendrogram()` - Clustering trees
- **Cluster Heatmap** - `vz.cluster_heatmap()` - Heatmap with dendrograms

### Real-time Charts (5) ✨ NEW
- **Streaming Line** - `vz.streaming_line()` - Live data streams
- **Live Heatmap** - `vz.live_heatmap()` - Real-time heatmaps
- **Animated Scatter** - `vz.animated_scatter()` - Time-series animation
- **Animated Bar** - `vz.animated_bar()` - Bar race charts
- **Animated Choropleth** - `vz.animated_choropleth()` - Geographic animation

### Statistical Charts (9) ✨ NEW
- **Violin Plot** - `vz.violin()` - Distribution with KDE
- **KDE Plot** - `vz.kde()` - Kernel density estimation
- **KDE 2D** - `vz.kde2d()` - 2D density estimation
- **Regression Plot** - `vz.regression()` - Scatter with regression line
- **Correlation Matrix** - `vz.correlation_matrix()` - Feature correlations
- **ROC Curve** - `vz.roc_curve_plot()` - Classification metrics
- **Multi ROC** - `vz.multi_roc_curve()` - Model comparison
- **Feature Importance** - `vz.feature_importance()` - ML feature importance
- **Permutation Importance** - `vz.permutation_importance()` - With uncertainty

### Advanced Charts (5) ✨ NEW
- **Treemap** - `vz.treemap()` - Hierarchical rectangles
- **Sunburst** - `vz.sunburst()` - Hierarchical rings
- **Parallel Coordinates** - `vz.parallel_coordinates()` - Multi-dimensional
- **Contour Plot** - `vz.contour()` - 2D contour lines
- **Filled Contour** - `vz.filled_contour()` - Filled contours

## Themes

```python
# Built-in themes
vz.set_theme("default")    # Modern, colorful
vz.set_theme("dark")       # Dark background, neon accents
vz.set_theme("minimal")    # Clean, monochrome
vz.set_theme("corporate")  # Professional, conservative
vz.set_theme("scientific") # Publication-ready

# Custom theme
custom = vz.Theme(
    background_color="#ffffff",
    text_color="#333333",
    primary_color="#3498db",
    font_family="Arial"
)
vz.set_theme(custom)
```

## Examples

### Network Graph
```python
import vizforge as vz

# Social network
nodes = ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
edges = [
    ('Alice', 'Bob'),
    ('Bob', 'Charlie'),
    ('Charlie', 'David'),
    ('David', 'Eve'),
    ('Eve', 'Alice')
]

vz.network_graph(nodes, edges, layout='spring',
                title='Friend Network')
```

### Statistical Analysis
```python
import vizforge as vz
import pandas as pd
import numpy as np

# A/B Test Results
df = pd.DataFrame({
    'variant': ['Control']*200 + ['Treatment']*200,
    'conversion_rate': np.concatenate([
        np.random.normal(0.05, 0.02, 200),
        np.random.normal(0.07, 0.02, 200)
    ])
})

vz.violin(df, x='variant', y='conversion_rate',
         title='A/B Test Results', box_visible=True)
```

### Real-time Streaming
```python
import vizforge as vz
import numpy as np

# Live sensor data
def get_sensor_reading():
    return np.random.randn()

chart = vz.streaming_line(
    data_source=get_sensor_reading,
    window_size=200,
    update_interval=100,  # ms
    title='Live Sensor Data',
    fill_area=True
)
```

### Machine Learning
```python
import vizforge as vz
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

# Train model
X, y = make_classification(n_samples=1000, n_features=20)
model = RandomForestClassifier()
model.fit(X, y)

# Feature importance
features = [f'Feature {i}' for i in range(20)]
importance = model.feature_importances_

vz.feature_importance(features, importance, top_n=10,
                     title='Top 10 Features')

# ROC Curve
y_scores = model.predict_proba(X)[:, 1]
vz.roc_curve_plot(y, y_scores,
                 model_name='Random Forest',
                 title='Model Performance')
```

### Animated Charts
```python
import vizforge as vz
import pandas as pd
import numpy as np

# Evolution over time
years = list(range(2010, 2024))
data = pd.DataFrame({
    'year': years * 5,
    'company': ['A', 'B', 'C', 'D', 'E'] * 14,
    'revenue': np.random.randint(100, 1000, 70),
    'profit': np.random.randint(10, 200, 70),
    'employees': np.random.randint(50, 500, 70)
})

vz.animated_scatter(
    data, x='revenue', y='profit',
    animation_frame='year', size='employees',
    color='company', title='Company Growth 2010-2023'
)
```

## Philosophy

> "Visualization should be easy. The code should disappear, and the story should emerge."

VizForge believes that:
- Beautiful visualizations shouldn't require complex code
- Themes should be globally consistent
- Export should be effortless
- No visualization library should require AI or paid APIs

## Why VizForge?

| Feature | VizForge | Plotly | Matplotlib | Seaborn |
|---------|----------|--------|------------|---------|
| Easy API | ✅ | ⚠️ | ❌ | ✅ |
| Interactive | ✅ | ✅ | ❌ | ❌ |
| Static Export | ✅ | ✅ | ✅ | ✅ |
| Themes | ✅ | ⚠️ | ⚠️ | ✅ |
| Geographic | ✅ | ✅ | ⚠️ | ❌ |
| Network Graphs | ✅ | ✅ | ⚠️ | ❌ |
| Real-time | ✅ | ✅ | ❌ | ❌ |
| Statistical | ✅ | ⚠️ | ✅ | ✅ |
| One-line Plots | ✅ | ❌ | ⚠️ | ✅ |
| Learning Curve | Low | Medium | High | Medium |

## Performance

- Efficiently handles 100K+ data points
- WebGL rendering for scatter plots
- Automatic data aggregation
- Lazy loading for large datasets
- Caching for computed layouts

## Requirements

- Python >= 3.10
- pandas >= 2.0.0
- numpy >= 1.24.0
- plotly >= 5.18.0
- scipy >= 1.10.0
- scikit-learn >= 1.3.0

## License

MIT License - Free for commercial use

## Contributing

Contributions welcome! Please open an issue or pull request.

## Documentation

See `examples/` directory for comprehensive examples.

---

**VizForge: Forge Beautiful Visualizations, Effortlessly.**
