"""
Visualization module for GeoDataSim.

Provides interactive, beautiful charts using Plotly:
- Scatter plots
- Bar charts
- Heatmaps
- Radar charts
- Geographic visualizations

New in v0.3.0.
"""

from .charts import (
    CityVisualizer,
    quick_scatter,
    quick_heatmap,
    quick_radar,
)

__all__ = [
    'CityVisualizer',
    'quick_scatter',
    'quick_heatmap',
    'quick_radar',
]
