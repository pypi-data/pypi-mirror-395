"""
Auto-update engine for GeoDataSim.

Automatically fetches fresh data from free public APIs:
- World Bank API (GDP, population, HDI)
- REST Countries API (country metadata)
- Open-Meteo API (climate data)

New in v0.3.0 - Monthly automatic updates.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import logging

import requests
from tqdm import tqdm

from ..utils.cache import get_cache_dir
from .validator import UpdateMetadataModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UpdateEngine:
    """
    Automatic data update engine.

    Fetches fresh data from free public APIs and updates city database.
    Runs monthly or on-demand.
    """

    # Free API endpoints (no authentication required)
    API_SOURCES = {
        'worldbank': {
            'base_url': 'https://api.worldbank.org/v2',
            'indicators': {
                'population': 'SP.POP.TOTL',
                'gdp_per_capita': 'NY.GDP.PCAP.CD',
                'gdp_total': 'NY.GDP.MKTP.CD',
                'life_expectancy': 'SP.DYN.LE00.IN',
                'unemployment': 'SL.UEM.TOTL.NE.ZS',
                'inflation': 'FP.CPI.TOTL.ZG',
            },
            'format': 'json',
            'per_page': 100,
        },
        'restcountries': {
            'base_url': 'https://restcountries.com/v3.1',
        },
        'open_meteo': {
            'base_url': 'https://api.open-meteo.com/v1',
        }
    }

    UPDATE_INTERVAL_DAYS = 30  # Monthly updates

    def __init__(self, cache_dir: Optional[Path] = None):
        """
        Initialize update engine.

        Args:
            cache_dir: Directory for caching update metadata
        """
        self.cache_dir = cache_dir or get_cache_dir() / 'updates'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.cache_dir / 'update_metadata.json'
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'GeoDataSim/0.3.0'})

    def should_update(self, city_name: str, indicator: str) -> bool:
        """
        Check if data should be updated based on last update time.

        Args:
            city_name: Name of city
            indicator: Data indicator (e.g., 'population', 'gdp_per_capita')

        Returns:
            True if update is needed (>30 days since last update)
        """
        metadata = self._load_metadata()
        key = f"{city_name}:{indicator}"

        if key not in metadata:
            return True

        last_update = datetime.fromisoformat(metadata[key]['timestamp'])
        days_since_update = (datetime.now() - last_update).days

        return days_since_update >= self.UPDATE_INTERVAL_DAYS

    def update_city_population(self, city_name: str, country_code: str) -> Optional[Tuple[int, UpdateMetadataModel]]:
        """
        Fetch latest population data from World Bank API.

        Args:
            city_name: Name of city
            country_code: ISO country code (e.g., 'TUR', 'USA')

        Returns:
            Tuple of (population, metadata) or None if failed
        """
        if not self.should_update(city_name, 'population'):
            logger.info(f"Population data for {city_name} is up-to-date")
            return None

        indicator = self.API_SOURCES['worldbank']['indicators']['population']
        url = f"{self.API_SOURCES['worldbank']['base_url']}/country/{country_code}/indicator/{indicator}"

        params = {
            'format': 'json',
            'per_page': 10,
            'date': f"{datetime.now().year-1}:{datetime.now().year}"  # Last 2 years
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if len(data) > 1 and data[1]:
                # Get most recent value
                latest = data[1][0]
                population = int(latest['value']) if latest['value'] else None

                if population:
                    metadata = UpdateMetadataModel(
                        city_name=city_name,
                        indicator='population',
                        new_value=population,
                        source='World Bank API',
                        success=True
                    )

                    self._save_metadata(city_name, 'population', metadata)
                    logger.info(f"Updated {city_name} population: {population:,}")
                    return population, metadata

        except Exception as e:
            logger.error(f"Failed to update population for {city_name}: {e}")
            metadata = UpdateMetadataModel(
                city_name=city_name,
                indicator='population',
                source='World Bank API',
                success=False,
                error_message=str(e)
            )
            return None

        return None

    def update_city_gdp(self, city_name: str, country_code: str) -> Optional[Tuple[float, UpdateMetadataModel]]:
        """
        Fetch latest GDP per capita from World Bank API.

        Args:
            city_name: Name of city
            country_code: ISO country code

        Returns:
            Tuple of (gdp_per_capita, metadata) or None if failed
        """
        if not self.should_update(city_name, 'gdp_per_capita'):
            logger.info(f"GDP data for {city_name} is up-to-date")
            return None

        indicator = self.API_SOURCES['worldbank']['indicators']['gdp_per_capita']
        url = f"{self.API_SOURCES['worldbank']['base_url']}/country/{country_code}/indicator/{indicator}"

        params = {
            'format': 'json',
            'per_page': 10,
            'date': f"{datetime.now().year-1}:{datetime.now().year}"
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if len(data) > 1 and data[1]:
                latest = data[1][0]
                gdp = float(latest['value']) if latest['value'] else None

                if gdp:
                    metadata = UpdateMetadataModel(
                        city_name=city_name,
                        indicator='gdp_per_capita',
                        new_value=gdp,
                        source='World Bank API',
                        success=True
                    )

                    self._save_metadata(city_name, 'gdp_per_capita', metadata)
                    logger.info(f"Updated {city_name} GDP per capita: ${gdp:,.2f}")
                    return gdp, metadata

        except Exception as e:
            logger.error(f"Failed to update GDP for {city_name}: {e}")
            return None

        return None

    def update_city_climate(self, city_name: str, latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
        """
        Fetch climate data from Open-Meteo API.

        Args:
            city_name: Name of city
            latitude: Latitude coordinate
            longitude: Longitude coordinate

        Returns:
            Dictionary with climate data or None if failed
        """
        if not self.should_update(city_name, 'climate'):
            logger.info(f"Climate data for {city_name} is up-to-date")
            return None

        url = f"{self.API_SOURCES['open_meteo']['base_url']}/forecast"

        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current_weather': 'true',
            'timezone': 'auto'
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'current_weather' in data:
                climate_data = {
                    'temperature': data['current_weather'].get('temperature'),
                    'windspeed': data['current_weather'].get('windspeed'),
                    'timestamp': datetime.now().isoformat()
                }

                metadata = UpdateMetadataModel(
                    city_name=city_name,
                    indicator='climate',
                    new_value=climate_data,
                    source='Open-Meteo API',
                    success=True
                )

                self._save_metadata(city_name, 'climate', metadata)
                logger.info(f"Updated {city_name} climate data")
                return climate_data

        except Exception as e:
            logger.error(f"Failed to update climate for {city_name}: {e}")
            return None

        return None

    def update_city_all(self, city_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update all available indicators for a city.

        Args:
            city_data: Dictionary containing city data (name, country_code, lat, lon)

        Returns:
            Updated city data dictionary
        """
        city_name = city_data['name']
        country_code = city_data.get('country_code', city_data.get('iso3', ''))

        logger.info(f"\n🔄 Updating data for {city_name}...")

        updated_data = city_data.copy()

        # Update population
        pop_result = self.update_city_population(city_name, country_code)
        if pop_result:
            population, _ = pop_result
            updated_data['population'] = population

        # Update GDP
        gdp_result = self.update_city_gdp(city_name, country_code)
        if gdp_result:
            gdp, _ = gdp_result
            updated_data['gdp_per_capita'] = gdp

        # Update climate
        if 'latitude' in city_data and 'longitude' in city_data:
            climate_result = self.update_city_climate(
                city_name,
                city_data['latitude'],
                city_data['longitude']
            )
            if climate_result:
                updated_data['current_climate'] = climate_result

        updated_data['last_updated'] = datetime.now().isoformat()

        return updated_data

    def update_all_cities(self, cities: List[Dict[str, Any]], show_progress: bool = True) -> List[Dict[str, Any]]:
        """
        Update all cities in the database.

        Args:
            cities: List of city data dictionaries
            show_progress: Show progress bar

        Returns:
            List of updated city data dictionaries
        """
        logger.info(f"\n🚀 Starting auto-update for {len(cities)} cities...")

        updated_cities = []
        iterator = tqdm(cities, desc="Updating cities", disable=not show_progress)

        for city in iterator:
            if show_progress:
                iterator.set_description(f"Updating {city['name']}")

            updated_city = self.update_city_all(city)
            updated_cities.append(updated_city)

        logger.info(f"\n✅ Update complete! Updated {len(updated_cities)} cities")

        return updated_cities

    def _load_metadata(self) -> Dict[str, Any]:
        """Load update metadata from cache."""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_metadata(self, city_name: str, indicator: str, metadata: UpdateMetadataModel):
        """Save update metadata to cache."""
        all_metadata = self._load_metadata()
        key = f"{city_name}:{indicator}"
        all_metadata[key] = metadata.model_dump(mode='json')

        with open(self.metadata_file, 'w') as f:
            json.dump(all_metadata, f, indent=2, default=str)

    def get_update_history(self, city_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get update history for all cities or specific city.

        Args:
            city_name: Optional city name to filter

        Returns:
            List of update metadata dictionaries
        """
        metadata = self._load_metadata()

        if city_name:
            return [v for k, v in metadata.items() if k.startswith(f"{city_name}:")]
        else:
            return list(metadata.values())

    def clear_metadata(self):
        """Clear all update metadata (forces fresh updates)."""
        if self.metadata_file.exists():
            self.metadata_file.unlink()
        logger.info("Update metadata cleared")


# Convenience functions

def update_city_data(city_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a single city's data from APIs.

    Args:
        city_data: City data dictionary

    Returns:
        Updated city data

    Example:
        >>> istanbul_data = {"name": "Istanbul", "country_code": "TUR", ...}
        >>> updated = update_city_data(istanbul_data)
        >>> print(updated['population'])
    """
    engine = UpdateEngine()
    return engine.update_city_all(city_data)


def update_all_cities_data(cities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Update all cities from APIs.

    Args:
        cities: List of city data dictionaries

    Returns:
        List of updated city data

    Example:
        >>> cities = [{"name": "Istanbul", ...}, {"name": "Paris", ...}]
        >>> updated = update_all_cities_data(cities)
    """
    engine = UpdateEngine()
    return engine.update_all_cities(cities)


def force_update_city(city_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Force update a city's data (ignores update interval).

    Args:
        city_data: City data dictionary

    Returns:
        Updated city data
    """
    engine = UpdateEngine()
    engine.clear_metadata()  # Clear cache to force update
    return engine.update_city_all(city_data)


__all__ = [
    'UpdateEngine',
    'update_city_data',
    'update_all_cities_data',
    'force_update_city',
]
