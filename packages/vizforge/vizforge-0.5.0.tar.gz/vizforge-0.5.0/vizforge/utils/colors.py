"""Color utility functions for VizForge."""

from typing import List, Tuple, Optional
import numpy as np


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    Convert hex color to RGB.

    Args:
        hex_color: Hex color string (e.g., '#3498db')

    Returns:
        RGB tuple (r, g, b)

    Examples:
        >>> hex_to_rgb('#3498db')
        (52, 152, 219)
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """
    Convert RGB to hex color.

    Args:
        r: Red value (0-255)
        g: Green value (0-255)
        b: Blue value (0-255)

    Returns:
        Hex color string

    Examples:
        >>> rgb_to_hex(52, 152, 219)
        '#3498db'
    """
    return f'#{r:02x}{g:02x}{b:02x}'


def generate_color_palette(
    n_colors: int,
    palette: str = 'default'
) -> List[str]:
    """
    Generate color palette.

    Args:
        n_colors: Number of colors needed
        palette: Palette name ('default', 'pastel', 'vibrant', 'cool', 'warm')

    Returns:
        List of hex colors

    Examples:
        >>> colors = generate_color_palette(5, palette='vibrant')
    """
    palettes = {
        'default': ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6',
                    '#1abc9c', '#e67e22', '#34495e', '#16a085', '#c0392b'],
        'pastel': ['#a8e6cf', '#ffd3b6', '#ffaaa5', '#ff8b94', '#c7ceea',
                   '#b4d7ed', '#f8b88b', '#faa1a1', '#d4a5a5', '#c9ada7'],
        'vibrant': ['#ff006e', '#fb5607', '#ffbe0b', '#8338ec', '#3a86ff',
                    '#06ffa5', '#ff4d6d', '#06d6a0', '#118ab2', '#ef476f'],
        'cool': ['#264653', '#2a9d8f', '#e76f51', '#f4a261', '#e9c46a',
                 '#219ebc', '#023047', '#8ecae6', '#126782', '#ffb703'],
        'warm': ['#f94144', '#f3722c', '#f8961e', '#f9844a', '#f9c74f',
                 '#90be6d', '#43aa8b', '#4d908e', '#577590', '#277da1']
    }

    base_colors = palettes.get(palette, palettes['default'])

    # If we need more colors than available, interpolate
    if n_colors <= len(base_colors):
        return base_colors[:n_colors]
    else:
        # Repeat and interpolate
        colors = []
        step = len(base_colors) / n_colors
        for i in range(n_colors):
            idx = int(i * step) % len(base_colors)
            colors.append(base_colors[idx])
        return colors


def color_scale(
    n_steps: int,
    start_color: str,
    end_color: str
) -> List[str]:
    """
    Generate color scale between two colors.

    Args:
        n_steps: Number of color steps
        start_color: Starting hex color
        end_color: Ending hex color

    Returns:
        List of interpolated hex colors

    Examples:
        >>> colors = color_scale(10, '#3498db', '#e74c3c')
    """
    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)

    colors = []
    for i in range(n_steps):
        ratio = i / (n_steps - 1) if n_steps > 1 else 0
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
        colors.append(rgb_to_hex(r, g, b))

    return colors
