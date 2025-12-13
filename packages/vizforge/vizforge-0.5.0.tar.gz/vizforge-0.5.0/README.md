# VizForge

**Production-grade data visualization library with ZERO AI dependencies**

Create beautiful, interactive visualizations with a single line of code. No API keys, no paid services, just pure visualization power.

## Features (v0.5.0)

- 🎨 **Beautiful by Default** - Professional themes out of the box
- ⚡ **Simple API** - One-line visualizations: `vz.line(data, x, y)`
- 📊 **48 Chart Types** - 12 2D + 6 3D + 5 Geographic + 6 Network + 5 Real-time + 9 Statistical + 5 Advanced
- 🎛️ **Dashboard Builder** - Create multi-chart dashboards with KPIs ✨ NEW
- 💾 **Advanced Export** - HTML, PNG, SVG, PDF export ✨ NEW
- 🛠️ **Data Utilities** - Clean, aggregate, normalize data ✨ NEW
- ⚙️ **Configuration System** - Global settings and preferences ✨ NEW
- 🌍 **3D & Geographic** - Surface plots, scatter3D, choropleth maps
- 🔗 **Network & Graphs** - Network graphs, Sankey, trees, dendrograms
- 📈 **Real-time & Animated** - Streaming data, live dashboards, animated transitions
- 📊 **Statistical Analysis** - Violin plots, KDE, regression, ROC curves
- 🎭 **Theme System** - 5 built-in themes + custom themes
- 🚀 **No AI Dependencies** - Completely free, no API keys needed
- 📈 **Performance** - Handle 100K+ data points efficiently

## Installation

```bash
# Basic installation
pip install vizforge

# With static image export (PNG, SVG, PDF)
pip install vizforge[export]

# Full installation (all optional dependencies)
pip install vizforge[full]
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
vz.violin(data, x='category', y='value', title='Distribution')

# Network visualization
nodes = ['A', 'B', 'C', 'D']
edges = [('A', 'B'), ('B', 'C'), ('C', 'D')]
vz.network_graph(nodes, edges, title='Network')

# Export to PNG
chart.export('output.png', width=1920, height=1080)
```

## New in v0.5.0 ✨

### Dashboard Builder

```python
import vizforge as vz

# Create dashboard
dashboard = vz.Dashboard(title="Sales Dashboard", rows=2, cols=2)

# Add charts
dashboard.add_chart(line_chart, row=1, col=1, title="Sales Trend")
dashboard.add_chart(bar_chart, row=1, col=2, title="By Category")

# Add KPIs
dashboard.add_kpi("Revenue", "$1.2M", row=2, col=1, delta="+15%")
dashboard.add_kpi("Orders", "5,432", row=2, col=2, delta="+8%")

# Display
dashboard.show()

# Export
dashboard.export('dashboard.html')
```

### Advanced Export

```python
import vizforge as vz

# Export to various formats
chart.export('output.html')  # Interactive HTML
chart.export('output.png', width=1920, height=1080)  # PNG
chart.export('output.svg')  # Vector SVG
chart.export('output.pdf')  # PDF document

# Batch export
exporter = vz.BatchExporter()
exporter.add_chart(chart1.create_figure(), 'chart1')
exporter.add_chart(chart2.create_figure(), 'chart2')
exporter.export_all('output_dir/', format='png')
```

### Data Utilities

```python
import vizforge as vz

# Clean data
df = vz.clean_data(df, fill_na='mean', drop_duplicates=True)

# Aggregate data
df_agg = vz.aggregate_data(df, group_by='category',
                           agg_column='sales', agg_func='sum')

# Detect outliers
df = vz.detect_outliers(df, 'price', method='iqr')
df_clean = df[~df['outlier']]

# Normalize data
df_norm = vz.normalize_data(df, columns=['value1', 'value2'])

# Resample time series
df_daily = vz.resample_timeseries(df, 'date', freq='D')
```

### Configuration System

```python
import vizforge as vz

# Set global config
vz.set_config(
    default_theme='dark',
    export_width=1920,
    export_height=1080,
    auto_show=False
)

# Get current config
config = vz.get_config()
print(config.get('default_theme'))

# Save/load config
config.save_to_file('vizforge_config.json')
config.load_from_file('vizforge_config.json')
```

## Chart Types (48 Total)

### 2D Charts (12)
- **Line Chart** - `vz.line()` - Time series, multi-line
- **Bar Chart** - `vz.bar()` - Grouped, stacked
- **Scatter Plot** - `vz.scatter()` - 2D scatter
- **Pie Chart** - `vz.pie()` / `vz.donut()` - Proportions
- **Histogram** - `vz.histogram()` - Distributions
- **Boxplot** - `vz.boxplot()` - Quartiles
- **Heatmap** - `vz.heatmap()` - Correlation
- **Area Chart** - `vz.area()` - Filled areas
- **Waterfall** - `vz.waterfall()` - Sequential changes
- **Funnel** - `vz.funnel()` - Conversion stages
- **Radar** - `vz.radar()` - Multivariate
- **Bubble** - `vz.bubble()` - 3-variable scatter

### 3D Charts (6)
- **Surface Plot** - `vz.surface()` - 3D surfaces
- **Scatter3D** - `vz.scatter3d()` - 3D scatter
- **Mesh3D** - `vz.mesh3d()` - 3D geometry
- **Volume Plot** - `vz.volume()` - Volumetric data
- **Cone Plot** - `vz.cone()` - Vector fields
- **Isosurface** - `vz.isosurface()` - Level sets

### Geographic Charts (5)
- **Choropleth Map** - `vz.choropleth()` - Color-coded regions
- **Scatter Geo** - `vz.scattergeo()` - Points on map
- **Line Geo** - `vz.linegeo()` - Routes on map
- **Density Geo** - `vz.densitygeo()` - Heatmap on map
- **Flow Map** - `vz.flowmap()` - Origin-destination flows

### Network Charts (6)
- **Network Graph** - `vz.network_graph()` - Force-directed
- **Sankey Diagram** - `vz.sankey()` - Flow diagrams
- **Tree Diagram** - `vz.tree()` - Hierarchical trees
- **Icicle Diagram** - `vz.icicle()` - Vertical hierarchies
- **Dendrogram** - `vz.dendrogram()` - Clustering trees
- **Cluster Heatmap** - `vz.cluster_heatmap()` - Heatmap with dendrograms

### Real-time Charts (5)
- **Streaming Line** - `vz.streaming_line()` - Live data streams
- **Live Heatmap** - `vz.live_heatmap()` - Real-time heatmaps
- **Animated Scatter** - `vz.animated_scatter()` - Time-series animation
- **Animated Bar** - `vz.animated_bar()` - Bar race charts
- **Animated Choropleth** - `vz.animated_choropleth()` - Geographic animation

### Statistical Charts (9)
- **Violin Plot** - `vz.violin()` - Distribution with KDE
- **KDE Plot** - `vz.kde()` - Kernel density estimation
- **KDE 2D** - `vz.kde2d()` - 2D density
- **Regression Plot** - `vz.regression()` - Scatter with regression
- **Correlation Matrix** - `vz.correlation_matrix()` - Feature correlations
- **ROC Curve** - `vz.roc_curve_plot()` - Classification metrics
- **Multi ROC** - `vz.multi_roc_curve()` - Model comparison
- **Feature Importance** - `vz.feature_importance()` - ML feature importance
- **Permutation Importance** - `vz.permutation_importance()` - With uncertainty

### Advanced Charts (5)
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

## Complete Example: Executive Dashboard

```python
import vizforge as vz
import pandas as pd
import numpy as np

# Generate sample data
dates = pd.date_range('2024-01-01', periods=365)
sales_data = pd.DataFrame({
    'date': dates,
    'revenue': np.random.randint(10000, 50000, 365),
    'category': np.random.choice(['A', 'B', 'C'], 365)
})

# Create charts
sales_trend = vz.line(sales_data, x='date', y='revenue',
                      title='Revenue Trend', show=False)
category_breakdown = vz.pie(sales_data.groupby('category')['revenue'].sum(),
                            title='Revenue by Category', show=False)

# Create dashboard
dashboard = vz.Dashboard(title="Executive Dashboard", rows=2, cols=2, theme='corporate')

# Add components
dashboard.add_chart(sales_trend, row=1, col=1, title="Sales Trend")
dashboard.add_chart(category_breakdown, row=1, col=2, title="Category Mix")
dashboard.add_kpi("Total Revenue", "$12.5M", row=2, col=1, delta="+18.5%")
dashboard.add_kpi("Avg Order Value", "$485", row=2, col=2, delta="+5.2%")

# Export and display
dashboard.export('executive_dashboard.html')
dashboard.show()
```

## Why VizForge?

| Feature | VizForge v0.5.0 | Plotly | Matplotlib | Seaborn | Tableau |
|---------|-----------------|--------|------------|---------|---------|
| Easy API | ✅ | ⚠️ | ❌ | ✅ | ✅ |
| Interactive | ✅ | ✅ | ❌ | ❌ | ✅ |
| Static Export | ✅ | ✅ | ✅ | ✅ | ✅ |
| Dashboard Builder | ✅ | ⚠️ | ❌ | ❌ | ✅ |
| Data Utilities | ✅ | ❌ | ❌ | ⚠️ | ✅ |
| Configuration | ✅ | ⚠️ | ⚠️ | ❌ | ✅ |
| Geographic | ✅ | ✅ | ⚠️ | ❌ | ✅ |
| Network Graphs | ✅ | ✅ | ⚠️ | ❌ | ⚠️ |
| Real-time | ✅ | ✅ | ❌ | ❌ | ✅ |
| Statistical | ✅ | ⚠️ | ✅ | ✅ | ✅ |
| No Cost | ✅ | ✅ | ✅ | ✅ | ❌ |
| Learning Curve | Low | Medium | High | Medium | Medium |

## Performance

- Efficiently handles 100K+ data points
- WebGL rendering for scatter plots
- Automatic data aggregation
- Lazy loading for large datasets
- Caching for computed layouts
- Optimized export pipeline

## Requirements

- Python >= 3.10
- pandas >= 2.0.0
- numpy >= 1.24.0
- plotly >= 5.18.0
- scipy >= 1.10.0
- scikit-learn >= 1.3.0

**Optional:**
- kaleido >= 0.2.1 (for PNG, SVG, PDF export)

## Installation Options

```bash
# Basic
pip install vizforge

# With static export
pip install vizforge[export]

# With geographic charts
pip install vizforge[geo]

# With statistical charts
pip install vizforge[stats]

# Everything
pip install vizforge[full]
```

## Version History

- **v0.5.0** (Latest) - Dashboard Builder, Advanced Export, Data Utilities, Configuration System
- **v0.4.0** - Network, Real-time, Statistical, Advanced charts (48 total)
- **v0.3.0** - 3D and Geographic charts (23 total)
- **v0.2.0** - All 2D charts (12 total)
- **v0.1.0** - Initial release (5 basic charts)

## License

MIT License - Free for commercial use

## Contributing

Contributions welcome! Please open an issue or pull request.

## Documentation

See `examples/` directory for comprehensive examples.

## Support

- GitHub Issues: https://github.com/teyfikoz/VizForge/issues
- Documentation: https://github.com/teyfikoz/VizForge/docs

---

**VizForge v0.5.0: Professional Data Visualization, Simplified.**
