"""Batch operations for comparing multiple cities."""

from typing import List, Dict, Any, Optional
import pandas as pd
from ..core.city import City


class BatchAnalyzer:
    """
    Analyze and compare multiple cities at once.

    Examples:
        >>> from geodatasim.analysis import BatchAnalyzer
        >>> analyzer = BatchAnalyzer(["Istanbul", "Paris", "Tokyo", "New York"])
        >>> df = analyzer.to_dataframe()
        >>> print(df[['name', 'population', 'gdp_per_capita']])
    """

    def __init__(self, city_names: List[str], auto_load: bool = True):
        """
        Initialize batch analyzer.

        Args:
            city_names: List of city names
            auto_load: Load API data for all cities (default: True)
        """
        self.cities = [City(name, auto_load=auto_load) for name in city_names]

    def to_dataframe(self, fields: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Convert cities to pandas DataFrame.

        Args:
            fields: Optional list of fields to include

        Returns:
            pandas DataFrame with city data

        Examples:
            >>> analyzer = BatchAnalyzer(["Istanbul", "London"])
            >>> df = analyzer.to_dataframe(['name', 'population', 'gdp_per_capita'])
        """
        data = []

        for city in self.cities:
            city_dict = city.to_dict()

            # Flatten nested dicts
            flat_dict = {
                'name': city_dict['name'],
                'country': city_dict['country'],
                'country_code': city_dict['country_code'],
                'region': city_dict['region'],
                'population': city_dict['population'],
                'timezone': city_dict['timezone'],
            }

            # Add coordinates
            if city_dict.get('coordinates'):
                flat_dict['latitude'] = city_dict['coordinates']['latitude']
                flat_dict['longitude'] = city_dict['coordinates']['longitude']

            # Add economic data
            if city_dict.get('economic'):
                for key, value in city_dict['economic'].items():
                    flat_dict[f'eco_{key}'] = value

            # Add climate data
            if city_dict.get('climate'):
                for key, value in city_dict['climate'].items():
                    flat_dict[f'climate_{key}'] = value

            data.append(flat_dict)

        df = pd.DataFrame(data)

        # Filter fields if specified
        if fields:
            available_fields = [f for f in fields if f in df.columns]
            df = df[available_fields]

        return df

    def compare(self, metrics: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Compare cities across specified metrics.

        Args:
            metrics: List of metrics to compare (default: key metrics)

        Returns:
            DataFrame with comparison

        Examples:
            >>> analyzer = BatchAnalyzer(["Istanbul", "Paris", "Tokyo"])
            >>> comparison = analyzer.compare(['population', 'eco_gdp_per_capita'])
        """
        if metrics is None:
            metrics = ['population', 'eco_gdp_per_capita', 'eco_hdi',
                      'eco_life_expectancy', 'climate_avg_temperature']

        df = self.to_dataframe()

        # Select only requested metrics + name
        available_metrics = ['name'] + [m for m in metrics if m in df.columns]
        return df[available_metrics].sort_values(
            by=metrics[0] if metrics else 'population',
            ascending=False
        )

    def summary_stats(self) -> Dict[str, Any]:
        """
        Get summary statistics for the batch.

        Returns:
            Dictionary with summary stats

        Examples:
            >>> analyzer = BatchAnalyzer(["Istanbul", "Paris", "Tokyo"])
            >>> stats = analyzer.summary_stats()
            >>> print(stats['total_population'])
        """
        df = self.to_dataframe()

        stats = {
            'total_cities': len(self.cities),
            'countries': df['country'].nunique() if 'country' in df else 0,
            'regions': df['region'].nunique() if 'region' in df else 0,
        }

        # Population stats
        if 'population' in df:
            stats['total_population'] = int(df['population'].sum())
            stats['avg_population'] = int(df['population'].mean())
            stats['max_population_city'] = df.loc[df['population'].idxmax(), 'name']

        # GDP stats
        if 'eco_gdp_per_capita' in df:
            stats['avg_gdp_per_capita'] = float(df['eco_gdp_per_capita'].mean())
            stats['max_gdp_city'] = df.loc[df['eco_gdp_per_capita'].idxmax(), 'name']
            stats['min_gdp_city'] = df.loc[df['eco_gdp_per_capita'].idxmin(), 'name']

        return stats

    def find_correlations(self, metric1: str = 'population',
                         metric2: str = 'eco_gdp_per_capita') -> float:
        """
        Find correlation between two metrics.

        Args:
            metric1: First metric
            metric2: Second metric

        Returns:
            Correlation coefficient

        Examples:
            >>> analyzer = BatchAnalyzer(["Istanbul", "Paris", "Tokyo", "New York"])
            >>> corr = analyzer.find_correlations('population', 'eco_gdp_per_capita')
            >>> print(f"Correlation: {corr:.3f}")
        """
        df = self.to_dataframe()

        if metric1 in df and metric2 in df:
            return df[[metric1, metric2]].corr().iloc[0, 1]

        return 0.0

    def group_by_region(self) -> Dict[str, List[str]]:
        """
        Group cities by region.

        Returns:
            Dictionary of region -> [cities]

        Examples:
            >>> analyzer = BatchAnalyzer(["Istanbul", "Paris", "Tokyo"])
            >>> by_region = analyzer.group_by_region()
        """
        df = self.to_dataframe()

        groups = {}
        for _, row in df.iterrows():
            region = row.get('region', 'Unknown')
            if region not in groups:
                groups[region] = []
            groups[region].append(row['name'])

        return groups

    def get_statistics(self, columns: List[str]) -> Dict[str, Dict[str, float]]:
        """
        Get statistical summary for specified columns.

        Args:
            columns: List of column names to analyze

        Returns:
            Dictionary with statistics for each column
        """
        df = self.to_dataframe()
        stats = {}

        for col in columns:
            if col in df.columns:
                stats[col] = {
                    'mean': float(df[col].mean()),
                    'median': float(df[col].median()),
                    'std': float(df[col].std()),
                    'min': float(df[col].min()),
                    'max': float(df[col].max()),
                    'count': int(df[col].count())
                }

        return stats

    def get_correlation(self, columns: List[str]) -> pd.DataFrame:
        """
        Calculate correlation matrix for specified columns.

        Args:
            columns: List of column names

        Returns:
            DataFrame with correlation matrix
        """
        df = self.to_dataframe()

        # Select only columns that exist
        available = [c for c in columns if c in df.columns]

        if len(available) < 2:
            raise ValueError(f"Need at least 2 columns. Available: {df.columns.tolist()}")

        return df[available].corr()


def compare_cities(city_names: List[str],
                  metrics: Optional[List[str]] = None,
                  as_dataframe: bool = True) -> pd.DataFrame:
    """
    Quick function to compare multiple cities.

    Args:
        city_names: List of city names
        metrics: List of metrics to compare
        as_dataframe: Return as DataFrame (vs dict)

    Returns:
        DataFrame or dict with comparison

    Examples:
        >>> from geodatasim.analysis import compare_cities
        >>> df = compare_cities(["Istanbul", "Paris", "Tokyo", "New York"])
        >>> print(df)
    """
    analyzer = BatchAnalyzer(city_names, auto_load=False)

    if as_dataframe:
        return analyzer.compare(metrics)
    else:
        return analyzer.to_dataframe(metrics).to_dict('records')
