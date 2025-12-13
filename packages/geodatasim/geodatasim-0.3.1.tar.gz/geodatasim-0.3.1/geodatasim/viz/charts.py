"""
Interactive visualization using Plotly.

Provides beautiful, interactive charts for city data analysis:
- Scatter plots
- Bar charts
- Heatmaps
- Radar charts
- Correlation matrices
- Geographic scatter

New in v0.3.0.
"""

from typing import List, Optional, Dict, Any, Union
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CityVisualizer:
    """
    Interactive visualization engine for city data.

    Uses Plotly for beautiful, interactive charts.
    """

    DEFAULT_TEMPLATE = 'plotly_white'
    DEFAULT_COLOR_SCALE = 'viridis'

    def __init__(self, template: str = None):
        """
        Initialize visualizer.

        Args:
            template: Plotly template ('plotly', 'plotly_white', 'plotly_dark', 'seaborn', 'ggplot2')
        """
        self.template = template or self.DEFAULT_TEMPLATE

    def scatter(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        color: Optional[str] = None,
        size: Optional[str] = None,
        hover_data: Optional[List[str]] = None,
        title: Optional[str] = None,
        log_x: bool = False,
        log_y: bool = False,
        **kwargs
    ) -> go.Figure:
        """
        Create interactive scatter plot.

        Args:
            df: DataFrame with city data
            x: Column for x-axis
            y: Column for y-axis
            color: Column for color grouping
            size: Column for marker size
            hover_data: Additional columns to show on hover
            title: Chart title
            log_x: Use log scale for x-axis
            log_y: Use log scale for y-axis

        Returns:
            Plotly Figure

        Example:
            >>> viz = CityVisualizer()
            >>> fig = viz.scatter(cities_df, x='population', y='gdp_per_capita',
            ...                   color='region', size='population')
            >>> fig.show()
        """
        hover_data = hover_data or ['name']

        fig = px.scatter(
            df,
            x=x,
            y=y,
            color=color,
            size=size,
            hover_data=hover_data,
            title=title or f"{y} vs {x}",
            template=self.template,
            log_x=log_x,
            log_y=log_y,
            **kwargs
        )

        fig.update_traces(marker=dict(line=dict(width=0.5, color='white')))

        return fig

    def bar(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        color: Optional[str] = None,
        title: Optional[str] = None,
        orientation: str = 'v',
        **kwargs
    ) -> go.Figure:
        """
        Create interactive bar chart.

        Args:
            df: DataFrame with city data
            x: Column for x-axis
            y: Column for y-axis
            color: Column for color grouping
            title: Chart title
            orientation: 'v' for vertical, 'h' for horizontal

        Returns:
            Plotly Figure
        """
        fig = px.bar(
            df,
            x=x,
            y=y,
            color=color,
            title=title or f"{y} by {x}",
            template=self.template,
            orientation=orientation,
            **kwargs
        )

        return fig

    def heatmap(
        self,
        df: pd.DataFrame,
        columns: Optional[List[str]] = None,
        title: str = "Correlation Heatmap",
        **kwargs
    ) -> go.Figure:
        """
        Create correlation heatmap.

        Args:
            df: DataFrame with city data
            columns: Columns to include (default: all numeric)
            title: Chart title

        Returns:
            Plotly Figure

        Example:
            >>> viz = CityVisualizer()
            >>> fig = viz.heatmap(cities_df, columns=['population', 'gdp', 'hdi'])
            >>> fig.show()
        """
        # Select numeric columns
        if columns:
            data = df[columns]
        else:
            data = df.select_dtypes(include=['number'])

        # Calculate correlation matrix
        corr_matrix = data.corr()

        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale=self.DEFAULT_COLOR_SCALE,
            zmid=0,
            text=corr_matrix.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Correlation"),
        ))

        fig.update_layout(
            title=title,
            template=self.template,
            xaxis=dict(side='bottom'),
            width=700,
            height=700
        )

        return fig

    def radar(
        self,
        df: pd.DataFrame,
        metrics: List[str],
        cities: Optional[List[str]] = None,
        title: str = "City Comparison Radar",
        **kwargs
    ) -> go.Figure:
        """
        Create radar chart for city comparison.

        Args:
            df: DataFrame with city data
            metrics: List of metrics to compare
            cities: List of city names to include (default: all)
            title: Chart title

        Returns:
            Plotly Figure

        Example:
            >>> viz = CityVisualizer()
            >>> fig = viz.radar(cities_df, metrics=['population', 'gdp', 'hdi'],
            ...                 cities=['Istanbul', 'Paris', 'Tokyo'])
            >>> fig.show()
        """
        if cities:
            plot_df = df[df['name'].isin(cities)]
        else:
            plot_df = df

        # Normalize metrics to 0-100 scale
        normalized = plot_df.copy()
        for metric in metrics:
            min_val = plot_df[metric].min()
            max_val = plot_df[metric].max()
            normalized[metric] = 100 * (plot_df[metric] - min_val) / (max_val - min_val)

        fig = go.Figure()

        for idx, row in normalized.iterrows():
            fig.add_trace(go.Scatterpolar(
                r=[row[metric] for metric in metrics] + [row[metrics[0]]],
                theta=metrics + [metrics[0]],
                fill='toself',
                name=row['name']
            ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            showlegend=True,
            title=title,
            template=self.template
        )

        return fig

    def geo_scatter(
        self,
        df: pd.DataFrame,
        lat: str = 'latitude',
        lon: str = 'longitude',
        color: Optional[str] = None,
        size: Optional[str] = None,
        hover_data: Optional[List[str]] = None,
        title: str = "Cities Map",
        **kwargs
    ) -> go.Figure:
        """
        Create geographic scatter plot.

        Args:
            df: DataFrame with city data
            lat: Latitude column name
            lon: Longitude column name
            color: Column for color grouping
            size: Column for marker size
            hover_data: Additional columns to show on hover
            title: Chart title

        Returns:
            Plotly Figure
        """
        hover_data = hover_data or ['name']

        fig = px.scatter_geo(
            df,
            lat=lat,
            lon=lon,
            color=color,
            size=size,
            hover_data=hover_data,
            title=title,
            template=self.template,
            **kwargs
        )

        return fig

    def histogram(
        self,
        df: pd.DataFrame,
        column: str,
        bins: int = 30,
        title: Optional[str] = None,
        **kwargs
    ) -> go.Figure:
        """
        Create histogram.

        Args:
            df: DataFrame with city data
            column: Column to plot
            bins: Number of bins
            title: Chart title

        Returns:
            Plotly Figure
        """
        fig = px.histogram(
            df,
            x=column,
            nbins=bins,
            title=title or f"Distribution of {column}",
            template=self.template,
            **kwargs
        )

        return fig

    def box(
        self,
        df: pd.DataFrame,
        y: str,
        x: Optional[str] = None,
        color: Optional[str] = None,
        title: Optional[str] = None,
        **kwargs
    ) -> go.Figure:
        """
        Create box plot.

        Args:
            df: DataFrame with city data
            y: Column for y-axis
            x: Column for x-axis grouping
            color: Column for color grouping
            title: Chart title

        Returns:
            Plotly Figure
        """
        fig = px.box(
            df,
            x=x,
            y=y,
            color=color,
            title=title or f"Distribution of {y}",
            template=self.template,
            **kwargs
        )

        return fig

    def line(
        self,
        df: pd.DataFrame,
        x: str,
        y: Union[str, List[str]],
        color: Optional[str] = None,
        title: Optional[str] = None,
        **kwargs
    ) -> go.Figure:
        """
        Create line chart.

        Args:
            df: DataFrame with data
            x: Column for x-axis
            y: Column(s) for y-axis
            color: Column for color grouping
            title: Chart title

        Returns:
            Plotly Figure
        """
        fig = px.line(
            df,
            x=x,
            y=y,
            color=color,
            title=title or f"{y} over {x}",
            template=self.template,
            **kwargs
        )

        return fig

    def sunburst(
        self,
        df: pd.DataFrame,
        path: List[str],
        values: str,
        title: str = "Hierarchical Data",
        **kwargs
    ) -> go.Figure:
        """
        Create sunburst chart for hierarchical data.

        Args:
            df: DataFrame with data
            path: List of columns defining hierarchy
            values: Column for segment sizes
            title: Chart title

        Returns:
            Plotly Figure

        Example:
            >>> # Show cities by region and country
            >>> fig = viz.sunburst(cities_df, path=['region', 'country', 'name'],
            ...                    values='population')
        """
        fig = px.sunburst(
            df,
            path=path,
            values=values,
            title=title,
            template=self.template,
            **kwargs
        )

        return fig


# Convenience functions

def quick_scatter(
    df: pd.DataFrame,
    x: str,
    y: str,
    **kwargs
) -> go.Figure:
    """
    Quick scatter plot.

    Example:
        >>> from geodatasim.viz import quick_scatter
        >>> fig = quick_scatter(cities_df, 'population', 'gdp_per_capita')
        >>> fig.show()
    """
    viz = CityVisualizer()
    return viz.scatter(df, x, y, **kwargs)


def quick_heatmap(df: pd.DataFrame, columns: Optional[List[str]] = None) -> go.Figure:
    """
    Quick correlation heatmap.

    Example:
        >>> from geodatasim.viz import quick_heatmap
        >>> fig = quick_heatmap(cities_df, ['population', 'gdp', 'hdi'])
        >>> fig.show()
    """
    viz = CityVisualizer()
    return viz.heatmap(df, columns)


def quick_radar(
    df: pd.DataFrame,
    metrics: List[str],
    cities: List[str]
) -> go.Figure:
    """
    Quick radar chart.

    Example:
        >>> from geodatasim.viz import quick_radar
        >>> fig = quick_radar(cities_df, ['population', 'gdp', 'hdi'],
        ...                   ['Istanbul', 'Paris', 'Tokyo'])
        >>> fig.show()
    """
    viz = CityVisualizer()
    return viz.radar(df, metrics, cities)


__all__ = [
    'CityVisualizer',
    'quick_scatter',
    'quick_heatmap',
    'quick_radar',
]
