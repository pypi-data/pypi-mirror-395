"""Data models for city indicators."""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class EconomicIndicators:
    """Economic indicators for a city/country."""

    gdp_per_capita: Optional[float] = None
    gdp_growth: Optional[float] = None
    inflation_rate: Optional[float] = None
    unemployment_rate: Optional[float] = None
    poverty_rate: Optional[float] = None
    gini_index: Optional[float] = None  # Income inequality

    # Human development
    hdi: Optional[float] = None  # Human Development Index
    life_expectancy: Optional[float] = None
    mean_years_schooling: Optional[float] = None

    # Additional indicators
    trade_percent_gdp: Optional[float] = None
    government_expenditure: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'gdp_per_capita': self.gdp_per_capita,
            'gdp_growth': self.gdp_growth,
            'inflation_rate': self.inflation_rate,
            'unemployment_rate': self.unemployment_rate,
            'poverty_rate': self.poverty_rate,
            'gini_index': self.gini_index,
            'hdi': self.hdi,
            'life_expectancy': self.life_expectancy,
            'mean_years_schooling': self.mean_years_schooling,
            'trade_percent_gdp': self.trade_percent_gdp,
            'government_expenditure': self.government_expenditure,
        }


@dataclass
class ClimateProfile:
    """Climate profile for a city."""

    climate_zone: Optional[str] = None  # Köppen climate classification
    avg_temperature: Optional[float] = None  # Celsius
    avg_temperature_summer: Optional[float] = None
    avg_temperature_winter: Optional[float] = None
    avg_precipitation: Optional[float] = None  # mm/year
    avg_humidity: Optional[float] = None  # percentage

    # Extreme values
    record_high_temp: Optional[float] = None
    record_low_temp: Optional[float] = None

    # Seasons
    wet_season_months: Optional[list] = None
    dry_season_months: Optional[list] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'climate_zone': self.climate_zone,
            'avg_temperature': self.avg_temperature,
            'avg_temperature_summer': self.avg_temperature_summer,
            'avg_temperature_winter': self.avg_temperature_winter,
            'avg_precipitation': self.avg_precipitation,
            'avg_humidity': self.avg_humidity,
            'record_high_temp': self.record_high_temp,
            'record_low_temp': self.record_low_temp,
            'wet_season_months': self.wet_season_months,
            'dry_season_months': self.dry_season_months,
        }


@dataclass
class CityProfile:
    """Complete city profile combining all data."""

    # Basic info
    name: str
    country: str
    country_code: Optional[str] = None
    region: Optional[str] = None

    # Demographics
    population: Optional[int] = None
    population_density: Optional[float] = None  # per km²
    urban_population_percent: Optional[float] = None

    # Geographic
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    elevation: Optional[float] = None  # meters
    area_km2: Optional[float] = None
    timezone: Optional[str] = None

    # Indicators
    economic: Optional[EconomicIndicators] = None
    climate: Optional[ClimateProfile] = None

    # Additional
    languages: Optional[list] = None
    currency: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'country': self.country,
            'country_code': self.country_code,
            'region': self.region,
            'population': self.population,
            'population_density': self.population_density,
            'urban_population_percent': self.urban_population_percent,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'elevation': self.elevation,
            'area_km2': self.area_km2,
            'timezone': self.timezone,
            'economic': self.economic.to_dict() if self.economic else None,
            'climate': self.climate.to_dict() if self.climate else None,
            'languages': self.languages,
            'currency': self.currency,
        }
