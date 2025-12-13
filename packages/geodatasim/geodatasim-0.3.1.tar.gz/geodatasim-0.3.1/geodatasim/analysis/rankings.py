"""City rankings and leaderboards."""

from typing import List, Dict, Any, Optional, Literal
import pandas as pd
from ..data.static import get_all_cities


class CityRankings:
    """
    Create rankings and leaderboards for cities.

    Examples:
        >>> from geodatasim.analysis import CityRankings
        >>> rankings = CityRankings()
        >>> top_pop = rankings.top_by_population(n=10)
        >>> print(top_pop[['name', 'population']])
    """

    def __init__(self):
        """Initialize rankings with all cities."""
        self.cities = get_all_cities()
        self.df = pd.DataFrame(self.cities)

    def top_by_population(self, n: int = 10) -> pd.DataFrame:
        """
        Get top N cities by population.

        Args:
            n: Number of cities to return

        Returns:
            DataFrame with top cities

        Examples:
            >>> rankings = CityRankings()
            >>> top10 = rankings.top_by_population(10)
        """
        return self.df.nlargest(n, 'population')[
            ['name', 'country', 'population', 'region']
        ]

    def top_by_gdp(self, n: int = 10) -> pd.DataFrame:
        """
        Get top N cities by GDP per capita.

        Args:
            n: Number of cities to return

        Returns:
            DataFrame with top cities
        """
        return self.df.nlargest(n, 'gdp_per_capita')[
            ['name', 'country', 'gdp_per_capita', 'hdi']
        ]

    def top_by_hdi(self, n: int = 10) -> pd.DataFrame:
        """
        Get top N cities by Human Development Index.

        Args:
            n: Number of cities to return

        Returns:
            DataFrame with top cities
        """
        return self.df.nlargest(n, 'hdi')[
            ['name', 'country', 'hdi', 'gdp_per_capita']
        ]

    def by_climate_zone(self, climate_zone: str) -> pd.DataFrame:
        """
        Get all cities in a specific climate zone.

        Args:
            climate_zone: Köppen climate classification code

        Returns:
            DataFrame with matching cities

        Examples:
            >>> rankings = CityRankings()
            >>> mediterranean = rankings.by_climate_zone('Csa')
        """
        return self.df[self.df['climate_zone'] == climate_zone][
            ['name', 'country', 'climate_zone', 'avg_temperature']
        ]

    def by_region(self, region: str) -> pd.DataFrame:
        """
        Get all cities in a specific region.

        Args:
            region: Region name

        Returns:
            DataFrame with cities in region

        Examples:
            >>> rankings = CityRankings()
            >>> europe = rankings.by_region('Europe & Central Asia')
        """
        return self.df[self.df['region'] == region][
            ['name', 'country', 'population', 'gdp_per_capita']
        ]

    def filter_cities(self,
                      min_population: Optional[int] = None,
                      max_population: Optional[int] = None,
                      min_gdp: Optional[float] = None,
                      max_gdp: Optional[float] = None,
                      min_hdi: Optional[float] = None,
                      countries: Optional[List[str]] = None,
                      regions: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Filter cities by multiple criteria.

        Args:
            min_population: Minimum population
            max_population: Maximum population
            min_gdp: Minimum GDP per capita
            max_gdp: Maximum GDP per capita
            min_hdi: Minimum HDI
            countries: List of countries to include
            regions: List of regions to include

        Returns:
            Filtered DataFrame

        Examples:
            >>> rankings = CityRankings()
            >>> filtered = rankings.filter_cities(
            ...     min_population=5_000_000,
            ...     min_gdp=30000,
            ...     regions=['Europe & Central Asia']
            ... )
        """
        df = self.df.copy()

        if min_population:
            df = df[df['population'] >= min_population]

        if max_population:
            df = df[df['population'] <= max_population]

        if min_gdp:
            df = df[df['gdp_per_capita'] >= min_gdp]

        if max_gdp:
            df = df[df['gdp_per_capita'] <= max_gdp]

        if min_hdi:
            df = df[df['hdi'] >= min_hdi]

        if countries:
            df = df[df['country'].isin(countries)]

        if regions:
            df = df[df['region'].isin(regions)]

        return df[['name', 'country', 'region', 'population', 'gdp_per_capita', 'hdi']]

    def rankings_by_metric(self, metric: str = 'population',
                          ascending: bool = False,
                          n: Optional[int] = None) -> pd.DataFrame:
        """
        Get rankings by any metric.

        Args:
            metric: Metric to rank by
            ascending: Sort ascending (default: False for descending)
            n: Number of results (None for all)

        Returns:
            Ranked DataFrame

        Examples:
            >>> rankings = CityRankings()
            >>> by_temp = rankings.rankings_by_metric('avg_temperature', n=10)
        """
        df = self.df.sort_values(by=metric, ascending=ascending)

        if n:
            df = df.head(n)

        return df[['name', 'country', metric]]

    def summary_by_region(self) -> pd.DataFrame:
        """
        Get summary statistics grouped by region.

        Returns:
            DataFrame with regional statistics

        Examples:
            >>> rankings = CityRankings()
            >>> regional_summary = rankings.summary_by_region()
        """
        summary = self.df.groupby('region').agg({
            'name': 'count',
            'population': ['sum', 'mean'],
            'gdp_per_capita': 'mean',
            'hdi': 'mean'
        }).round(0)

        summary.columns = ['cities_count', 'total_population', 'avg_population',
                          'avg_gdp_per_capita', 'avg_hdi']

        return summary.sort_values('total_population', ascending=False)

    def summary_by_country(self) -> pd.DataFrame:
        """
        Get summary statistics grouped by country.

        Returns:
            DataFrame with country statistics
        """
        summary = self.df.groupby('country').agg({
            'name': 'count',
            'population': ['sum', 'mean'],
            'gdp_per_capita': 'mean',
        }).round(0)

        summary.columns = ['cities_count', 'total_population', 'avg_population',
                          'avg_gdp_per_capita']

        return summary.sort_values('cities_count', ascending=False)


def rank_cities(city_names: List[str],
               by: str = 'population',
               metric: Optional[str] = None,
               n: Optional[int] = None,
               ascending: bool = False,
               filter_params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """
    Quick function to rank cities by a metric.

    Args:
        city_names: List of city names to rank
        by: Metric to rank by (alias for metric)
        metric: Metric to rank by
        n: Number of results (None for all)
        ascending: Sort ascending
        filter_params: Optional filter parameters

    Returns:
        Ranked DataFrame with 'rank' column

    Examples:
        >>> from geodatasim.analysis import rank_cities
        >>> cities = ["Istanbul", "Tokyo", "New York", "London"]
        >>> ranked = rank_cities(cities, by='population')
        >>> print(ranked)
    """
    from .batch import BatchAnalyzer

    # Support both 'by' and 'metric' parameters
    rank_metric = by if metric is None else metric

    # Create batch analyzer for specified cities
    analyzer = BatchAnalyzer(city_names)
    df = analyzer.to_dataframe()

    # Ensure the metric column exists
    if rank_metric not in df.columns:
        raise ValueError(f"Metric '{rank_metric}' not found. Available: {df.columns.tolist()}")

    # Sort and add rank
    df = df.sort_values(by=rank_metric, ascending=ascending).reset_index(drop=True)
    df['rank'] = range(1, len(df) + 1)

    # Limit results if n specified
    if n is not None:
        df = df.head(n)

    return df
