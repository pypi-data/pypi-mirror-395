"""Theme system for VizForge visualizations."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Theme:
    """
    VizForge theme configuration.

    Attributes:
        name: Theme name
        background_color: Background color (hex or rgb)
        paper_color: Paper/canvas color
        text_color: Text color
        grid_color: Grid line color
        primary_color: Primary accent color
        secondary_color: Secondary accent color
        success_color: Success/positive color
        warning_color: Warning color
        error_color: Error/negative color
        color_palette: List of colors for multi-series charts
        font_family: Font family
        font_size: Base font size
        title_font_size: Title font size
        axis_font_size: Axis label font size
        line_width: Default line width
        marker_size: Default marker size
        opacity: Default opacity
        border_radius: Border radius for elements
    """

    name: str = "default"
    background_color: str = "#ffffff"
    paper_color: str = "#ffffff"
    text_color: str = "#2c3e50"
    grid_color: str = "#e0e0e0"

    # Accent colors
    primary_color: str = "#3498db"
    secondary_color: str = "#e74c3c"
    success_color: str = "#2ecc71"
    warning_color: str = "#f39c12"
    error_color: str = "#e74c3c"

    # Color palettes for multi-series
    color_palette: list[str] = field(default_factory=lambda: [
        "#3498db", "#e74c3c", "#2ecc71", "#f39c12",
        "#9b59b6", "#1abc9c", "#34495e", "#e67e22"
    ])

    # Typography
    font_family: str = "Arial, sans-serif"
    font_size: int = 12
    title_font_size: int = 18
    axis_font_size: int = 11

    # Styling
    line_width: float = 2.0
    marker_size: int = 8
    opacity: float = 1.0
    border_radius: int = 4

    def to_plotly_layout(self) -> dict:
        """Convert theme to Plotly layout configuration."""
        return {
            'paper_bgcolor': self.paper_color,
            'plot_bgcolor': self.background_color,
            'font': {
                'family': self.font_family,
                'size': self.font_size,
                'color': self.text_color,
            },
            'title': {
                'font': {
                    'size': self.title_font_size,
                    'color': self.text_color,
                }
            },
            'xaxis': {
                'gridcolor': self.grid_color,
                'linecolor': self.grid_color,
                'tickfont': {'size': self.axis_font_size},
            },
            'yaxis': {
                'gridcolor': self.grid_color,
                'linecolor': self.grid_color,
                'tickfont': {'size': self.axis_font_size},
            },
            'colorway': self.color_palette,
        }


# Built-in themes
DEFAULT_THEME = Theme(
    name="default",
    background_color="#ffffff",
    paper_color="#ffffff",
    text_color="#2c3e50",
    grid_color="#e0e0e0",
    primary_color="#3498db",
    color_palette=[
        "#3498db", "#e74c3c", "#2ecc71", "#f39c12",
        "#9b59b6", "#1abc9c", "#34495e", "#e67e22"
    ]
)

DARK_THEME = Theme(
    name="dark",
    background_color="#1e1e1e",
    paper_color="#121212",
    text_color="#e0e0e0",
    grid_color="#333333",
    primary_color="#00d9ff",
    secondary_color="#ff006e",
    color_palette=[
        "#00d9ff", "#ff006e", "#00ff9f", "#ffbe0b",
        "#c77dff", "#06ffa5", "#7209b7", "#fb5607"
    ]
)

MINIMAL_THEME = Theme(
    name="minimal",
    background_color="#ffffff",
    paper_color="#ffffff",
    text_color="#000000",
    grid_color="#d3d3d3",
    primary_color="#000000",
    secondary_color="#666666",
    color_palette=[
        "#000000", "#404040", "#666666", "#808080",
        "#999999", "#b3b3b3", "#cccccc", "#e0e0e0"
    ],
    line_width=1.5,
)

CORPORATE_THEME = Theme(
    name="corporate",
    background_color="#f8f9fa",
    paper_color="#ffffff",
    text_color="#212529",
    grid_color="#dee2e6",
    primary_color="#0056b3",
    secondary_color="#6c757d",
    success_color="#28a745",
    warning_color="#ffc107",
    error_color="#dc3545",
    color_palette=[
        "#0056b3", "#6c757d", "#28a745", "#ffc107",
        "#dc3545", "#17a2b8", "#6f42c1", "#fd7e14"
    ],
    font_family="Segoe UI, Roboto, sans-serif",
)

SCIENTIFIC_THEME = Theme(
    name="scientific",
    background_color="#ffffff",
    paper_color="#ffffff",
    text_color="#000000",
    grid_color="#cccccc",
    primary_color="#1f77b4",
    color_palette=[
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",
        "#9467bd", "#8c564b", "#e377c2", "#7f7f7f",
        "#bcbd22", "#17becf"
    ],
    font_family="Times New Roman, serif",
    font_size=11,
    line_width=1.5,
)

# Theme registry
_THEMES = {
    "default": DEFAULT_THEME,
    "dark": DARK_THEME,
    "minimal": MINIMAL_THEME,
    "corporate": CORPORATE_THEME,
    "scientific": SCIENTIFIC_THEME,
}

# Current active theme
_CURRENT_THEME = DEFAULT_THEME


def get_theme(name: Optional[str] = None) -> Theme:
    """
    Get a theme by name or return current theme.

    Args:
        name: Theme name (default, dark, minimal, corporate, scientific)

    Returns:
        Theme object

    Example:
        >>> theme = get_theme("dark")
        >>> theme.background_color
        '#1e1e1e'
    """
    if name is None:
        return _CURRENT_THEME

    if name not in _THEMES:
        raise ValueError(
            f"Unknown theme '{name}'. Available: {', '.join(_THEMES.keys())}"
        )

    return _THEMES[name]


def set_theme(theme: str | Theme) -> None:
    """
    Set the global theme for all charts.

    Args:
        theme: Theme name (str) or Theme object

    Example:
        >>> set_theme("dark")
        >>> set_theme(Theme(background_color="#000000"))
    """
    global _CURRENT_THEME

    if isinstance(theme, str):
        _CURRENT_THEME = get_theme(theme)
    elif isinstance(theme, Theme):
        _CURRENT_THEME = theme
        # Register custom theme
        _THEMES[theme.name] = theme
    else:
        raise TypeError("Theme must be a string or Theme object")


def register_theme(theme: Theme) -> None:
    """
    Register a custom theme.

    Args:
        theme: Theme object to register

    Example:
        >>> custom = Theme(name="custom", background_color="#f0f0f0")
        >>> register_theme(custom)
        >>> set_theme("custom")
    """
    _THEMES[theme.name] = theme


def list_themes() -> list[str]:
    """
    List all available theme names.

    Returns:
        List of theme names

    Example:
        >>> list_themes()
        ['default', 'dark', 'minimal', 'corporate', 'scientific']
    """
    return list(_THEMES.keys())
