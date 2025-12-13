"""Core City class - main interface for GeoDataSim."""

from typing import Optional, List, Dict, Any
from ..models.indicators import EconomicIndicators, ClimateProfile, CityProfile
from ..models.geographic import Coordinates, Airport
from ..api.worldbank import WorldBankAPI
from ..utils.similarity import CitySimilarity
from ..utils.distance import haversine_distance
from ..data.static import CITIES_DATABASE, get_city_data, search_city
from .config import get_config


class City:
    """
    Main City class for accessing geographic, economic, and climate data.

    Examples:
        >>> from geodatasim import City
        >>> istanbul = City("Istanbul")
        >>> print(istanbul.population)
        >>> print(istanbul.gdp_per_capita)
        >>> similar = istanbul.find_similar(n=5)
    """

    def __init__(self, name: str, country: Optional[str] = None, auto_load: bool = True):
        """
        Initialize a City object.

        Args:
            name: City name (e.g., "Istanbul", "Paris")
            country: Optional country name for disambiguation
            auto_load: Automatically load data from APIs (default: True)

        Examples:
            >>> city = City("Paris")
            >>> city = City("Paris", country="France")
            >>> city = City("Istanbul", auto_load=False)  # Don't load API data
        """
        self.name = name
        self.country = country
        self._config = get_config()

        # Initialize APIs
        self._worldbank_api = WorldBankAPI()

        # Data containers
        self._static_data: Optional[Dict[str, Any]] = None
        self._economic_data: Optional[EconomicIndicators] = None
        self._climate_data: Optional[ClimateProfile] = None

        # Load static data first
        self._load_static_data()

        # Load API data if requested
        if auto_load:
            self._load_api_data()

    def _load_static_data(self):
        """Load static data from built-in dataset."""
        self._static_data = get_city_data(self.name, self.country)

        if not self._static_data:
            # City not found in database
            if self._config.get('show_warnings', True):
                print(f"Warning: '{self.name}' not found in static database. "
                      "Limited data will be available.")

    def _load_api_data(self):
        """Load data from external APIs (World Bank, etc.)."""
        if not self.country_code:
            return

        # Get economic indicators from World Bank
        indicators = self._worldbank_api.get_country_indicators(
            self.country_code,
            indicators=[
                'gdp_per_capita', 'gdp_growth', 'inflation',
                'unemployment', 'life_expectancy', 'literacy_rate',
                'population_total', 'population_growth', 'urban_population',
            ]
        )

        # Create EconomicIndicators object
        self._economic_data = EconomicIndicators(
            gdp_per_capita=indicators.get('gdp_per_capita'),
            gdp_growth=indicators.get('gdp_growth'),
            inflation_rate=indicators.get('inflation'),
            unemployment_rate=indicators.get('unemployment'),
            life_expectancy=indicators.get('life_expectancy'),
            mean_years_schooling=indicators.get('literacy_rate'),
        )

    # ==================== BASIC PROPERTIES ====================

    @property
    def population(self) -> Optional[int]:
        """City population."""
        if self._static_data:
            return self._static_data.get('population')
        return None

    @property
    def country_name(self) -> Optional[str]:
        """Country name."""
        if self.country:
            return self.country
        if self._static_data:
            return self._static_data.get('country')
        return None

    @property
    def country_code(self) -> Optional[str]:
        """ISO3 country code."""
        if self._static_data:
            return self._static_data.get('country_code')
        return None

    @property
    def coordinates(self) -> Optional[Coordinates]:
        """Geographic coordinates as Coordinates object."""
        if self._static_data:
            lat = self._static_data.get('latitude')
            lon = self._static_data.get('longitude')
            if lat is not None and lon is not None:
                return Coordinates(lat, lon)
        return None

    @property
    def latitude(self) -> Optional[float]:
        """Latitude."""
        if self._static_data:
            return self._static_data.get('latitude')
        return None

    @property
    def longitude(self) -> Optional[float]:
        """Longitude."""
        if self._static_data:
            return self._static_data.get('longitude')
        return None

    @property
    def timezone(self) -> Optional[str]:
        """Timezone (e.g., 'Europe/Istanbul')."""
        if self._static_data:
            return self._static_data.get('timezone')
        return None

    @property
    def region(self) -> Optional[str]:
        """Geographic region."""
        if self._static_data:
            return self._static_data.get('region')
        return None

    # ==================== ECONOMIC PROPERTIES ====================

    @property
    def gdp_per_capita(self) -> Optional[float]:
        """GDP per capita in current US$."""
        if self._economic_data and self._economic_data.gdp_per_capita:
            return self._economic_data.gdp_per_capita
        if self._static_data:
            return self._static_data.get('gdp_per_capita')
        return None

    @property
    def gdp_growth(self) -> Optional[float]:
        """GDP growth rate (annual %)."""
        if self._economic_data:
            return self._economic_data.gdp_growth
        return None

    @property
    def hdi(self) -> Optional[float]:
        """Human Development Index (0-1)."""
        if self._economic_data and self._economic_data.hdi:
            return self._economic_data.hdi
        if self._static_data:
            return self._static_data.get('hdi')
        return None

    @property
    def life_expectancy(self) -> Optional[float]:
        """Life expectancy at birth (years)."""
        if self._economic_data:
            return self._economic_data.life_expectancy
        return None

    @property
    def unemployment_rate(self) -> Optional[float]:
        """Unemployment rate (% of labor force)."""
        if self._economic_data:
            return self._economic_data.unemployment_rate
        return None

    # ==================== CLIMATE PROPERTIES ====================

    @property
    def climate_zone(self) -> Optional[str]:
        """Köppen climate classification."""
        if self._static_data:
            return self._static_data.get('climate_zone')
        return None

    @property
    def avg_temperature(self) -> Optional[float]:
        """Average annual temperature (°C)."""
        if self._static_data:
            return self._static_data.get('avg_temperature')
        return None

    # ==================== METHODS ====================

    def distance_to(self, other: 'City') -> Optional[float]:
        """
        Calculate distance to another city.

        Args:
            other: Another City object

        Returns:
            Distance in kilometers

        Examples:
            >>> istanbul = City("Istanbul")
            >>> ankara = City("Ankara")
            >>> dist = istanbul.distance_to(ankara)
            >>> print(f"{dist:.0f} km")
        """
        if not (self.coordinates and other.coordinates):
            return None

        return haversine_distance(
            self.latitude, self.longitude,
            other.latitude, other.longitude
        )

    def find_similar(self, n: int = 10, min_population: Optional[int] = None) -> List['City']:
        """
        Find similar cities based on multiple dimensions.

        Args:
            n: Number of similar cities to return
            min_population: Minimum population filter (optional)

        Returns:
            List of similar City objects, sorted by similarity

        Examples:
            >>> istanbul = City("Istanbul")
            >>> similar = istanbul.find_similar(n=5)
            >>> for city in similar:
            ...     print(f"{city.name}: {city.similarity_score:.1%}")
        """
        from ..data.static import get_all_cities

        # Get all cities
        all_cities = get_all_cities()

        # Filter
        candidates = []
        for city_data in all_cities:
            # Skip self
            if city_data['name'] == self.name:
                continue

            # Apply population filter
            if min_population and city_data.get('population', 0) < min_population:
                continue

            candidates.append(city_data)

        # Calculate similarity
        calculator = CitySimilarity()
        self_data = self._to_dict()

        similarities = []
        for candidate in candidates:
            similarity_score = calculator.calculate_similarity(self_data, candidate)
            similarities.append((candidate, similarity_score))

        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Create City objects
        result = []
        for city_data, score in similarities[:n]:
            city = City(city_data['name'], country=city_data.get('country'), auto_load=False)
            city.similarity_score = score  # Attach score
            result.append(city)

        return result

    def _to_dict(self) -> Dict[str, Any]:
        """Convert city data to dictionary for similarity calculation."""
        return {
            'name': self.name,
            'country': self.country_name,
            'population': self.population,
            'gdp_per_capita': self.gdp_per_capita,
            'climate_zone': self.climate_zone,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'hdi': self.hdi,
        }

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary with all available data.

        Returns:
            Dictionary with all city data

        Examples:
            >>> city = City("Paris")
            >>> data = city.to_dict()
            >>> print(data['population'])
        """
        return {
            'name': self.name,
            'country': self.country_name,
            'country_code': self.country_code,
            'region': self.region,
            'population': self.population,
            'coordinates': {
                'latitude': self.latitude,
                'longitude': self.longitude,
            } if self.coordinates else None,
            'timezone': self.timezone,
            'economic': {
                'gdp_per_capita': self.gdp_per_capita,
                'gdp_growth': self.gdp_growth,
                'hdi': self.hdi,
                'life_expectancy': self.life_expectancy,
                'unemployment_rate': self.unemployment_rate,
            } if self._economic_data else None,
            'climate': {
                'climate_zone': self.climate_zone,
                'avg_temperature': self.avg_temperature,
            } if self.climate_zone else None,
        }

    def __repr__(self) -> str:
        """String representation."""
        location = f"{self.name}, {self.country_name}" if self.country_name else self.name
        pop = f", pop: {self.population:,}" if self.population else ""
        return f"City({location}{pop})"

    def __str__(self) -> str:
        """String representation."""
        return self.name
