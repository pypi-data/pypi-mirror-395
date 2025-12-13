"""
Basic VizForge Examples

Demonstrates core functionality of VizForge library.
"""

import pandas as pd
import numpy as np
import vizforge as vz


def example_line_chart():
    """Simple line chart example."""
    print("Creating line chart...")

    # Create sample data
    dates = pd.date_range('2024-01-01', periods=30)
    data = pd.DataFrame({
        'date': dates,
        'sales': np.random.randint(100, 200, 30) + np.arange(30) * 2
    })

    # Create line chart
    vz.line(
        data,
        x='date',
        y='sales',
        title='Daily Sales Trend',
        theme='default'
    )


def example_multi_line_chart():
    """Multi-line comparison chart."""
    print("Creating multi-line chart...")

    dates = pd.date_range('2024-01-01', periods=30)
    data = pd.DataFrame({
        'date': dates,
        'product_a': np.random.randint(80, 150, 30) + np.arange(30) * 2,
        'product_b': np.random.randint(90, 160, 30) + np.arange(30) * 1.5,
        'product_c': np.random.randint(70, 140, 30) + np.arange(30) * 2.5,
    })

    vz.line(
        data,
        x='date',
        y=['product_a', 'product_b', 'product_c'],
        title='Product Sales Comparison',
        theme='dark'
    )


def example_bar_chart():
    """Simple bar chart example."""
    print("Creating bar chart...")

    data = pd.DataFrame({
        'category': ['A', 'B', 'C', 'D', 'E'],
        'value': [23, 45, 56, 78, 32]
    })

    vz.bar(
        data,
        x='category',
        y='value',
        title='Sales by Category',
        theme='corporate'
    )


def example_grouped_bar_chart():
    """Grouped bar chart with multiple series."""
    print("Creating grouped bar chart...")

    data = pd.DataFrame({
        'month': ['Jan', 'Feb', 'Mar', 'Apr'] * 3,
        'revenue': [120, 150, 180, 200, 110, 140, 170, 190, 130, 160, 190, 210],
        'region': ['North'] * 4 + ['South'] * 4 + ['West'] * 4
    })

    vz.bar(
        data,
        x='month',
        y='revenue',
        color='region',
        title='Regional Revenue by Month',
        barmode='group',
        theme='minimal'
    )


def example_scatter_plot():
    """Simple scatter plot example."""
    print("Creating scatter plot...")

    np.random.seed(42)
    data = pd.DataFrame({
        'age': np.random.randint(18, 70, 100),
        'income': np.random.randint(20000, 150000, 100)
    })

    vz.scatter(
        data,
        x='age',
        y='income',
        title='Age vs Income',
        theme='scientific'
    )


def example_bubble_chart():
    """Bubble chart with size encoding."""
    print("Creating bubble chart...")

    np.random.seed(42)
    data = pd.DataFrame({
        'x': np.random.randn(50),
        'y': np.random.randn(50),
        'size': np.random.randint(10, 100, 50),
        'category': np.random.choice(['A', 'B', 'C'], 50)
    })

    vz.scatter(
        data,
        x='x',
        y='y',
        size='size',
        color='category',
        title='Bubble Chart Example',
        theme='dark'
    )


def example_pie_chart():
    """Simple pie chart example."""
    print("Creating pie chart...")

    data = pd.DataFrame({
        'company': ['Company A', 'Company B', 'Company C', 'Company D', 'Company E'],
        'market_share': [30, 25, 20, 15, 10]
    })

    vz.pie(
        data,
        values='market_share',
        names='company',
        title='Market Share Distribution',
        theme='default'
    )


def example_donut_chart():
    """Donut chart example."""
    print("Creating donut chart...")

    # Dictionary format
    data = {
        'Product A': 35,
        'Product B': 25,
        'Product C': 20,
        'Product D': 20
    }

    vz.donut(
        data,
        title='Product Revenue Distribution',
        theme='corporate'
    )


def example_themes():
    """Demonstrate different themes."""
    print("Demonstrating themes...")

    data = pd.DataFrame({
        'x': list(range(10)),
        'y': [2, 4, 3, 5, 7, 6, 8, 9, 11, 10]
    })

    themes = ['default', 'dark', 'minimal', 'corporate', 'scientific']

    for theme in themes:
        print(f"  - {theme} theme")
        vz.line(
            data,
            x='x',
            y='y',
            title=f'Line Chart - {theme.title()} Theme',
            theme=theme
        )


def example_export():
    """Demonstrate export functionality."""
    print("Creating and exporting chart...")

    data = pd.DataFrame({
        'x': list(range(10)),
        'y': [2, 4, 3, 5, 7, 6, 8, 9, 11, 10]
    })

    # Create chart and export to HTML (PNG requires kaleido)
    chart = vz.line(
        data,
        x='x',
        y='y',
        title='Export Example',
        show=False
    )

    # Export to HTML
    chart.export('output.html')
    print("  Exported to output.html")


def example_custom_styling():
    """Demonstrate custom styling options."""
    print("Creating chart with custom styling...")

    data = pd.DataFrame({
        'x': list(range(20)),
        'y': np.cumsum(np.random.randn(20))
    })

    chart = vz.LineChart(
        data,
        x='x',
        y='y',
        title='Custom Styled Chart',
        theme='dark',
        width=1200,
        height=600
    )

    # Additional customization
    chart.update_xaxis(title="Time Steps", showgrid=True)
    chart.update_yaxis(title="Cumulative Value", showgrid=True)

    chart.show()


if __name__ == "__main__":
    print("VizForge Basic Examples")
    print("=" * 50)

    # Run examples
    example_line_chart()
    example_multi_line_chart()
    example_bar_chart()
    example_grouped_bar_chart()
    example_scatter_plot()
    example_bubble_chart()
    example_pie_chart()
    example_donut_chart()
    example_themes()
    example_export()
    example_custom_styling()

    print("\nAll examples completed!")
