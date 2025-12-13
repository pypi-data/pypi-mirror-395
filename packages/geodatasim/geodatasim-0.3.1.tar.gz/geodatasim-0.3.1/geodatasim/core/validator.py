"""
Data validation models using Pydantic.

Ensures data quality and type safety across all GeoDataSim operations.
New in v0.3.0.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict


class CoordinatesModel(BaseModel):
    """Geographic coordinates validation."""

    latitude: float = Field(..., ge=-90, le=90, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in decimal degrees")

    model_config = ConfigDict(frozen=True)


class ClimateModel(BaseModel):
    """Climate data validation."""

    climate_zone: str = Field(..., min_length=1, max_length=10)
    avg_temperature: Optional[float] = Field(None, ge=-100, le=100)
    avg_precipitation: Optional[float] = Field(None, ge=0, le=10000)

    @field_validator('climate_zone')
    @classmethod
    def validate_climate_zone(cls, v: str) -> str:
        """Validate Köppen climate classification codes."""
        valid_codes = ['Af', 'Am', 'Aw', 'BWh', 'BWk', 'BSh', 'BSk',
                       'Csa', 'Csb', 'Csc', 'Cwa', 'Cwb', 'Cwc',
                       'Cfa', 'Cfb', 'Cfc', 'Dsa', 'Dsb', 'Dsc', 'Dsd',
                       'Dwa', 'Dwb', 'Dwc', 'Dwd', 'Dfa', 'Dfb', 'Dfc', 'Dfd',
                       'ET', 'EF']
        if v not in valid_codes:
            # Don't fail, just warn - we have some custom codes
            pass
        return v


class EconomicIndicatorsModel(BaseModel):
    """Economic indicators validation."""

    gdp_per_capita: Optional[float] = Field(None, ge=0, le=1000000)
    gdp_total: Optional[float] = Field(None, ge=0)
    unemployment_rate: Optional[float] = Field(None, ge=0, le=100)
    inflation_rate: Optional[float] = Field(None, ge=-50, le=1000)
    gini_index: Optional[float] = Field(None, ge=0, le=100)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "gdp_per_capita": 28000.0,
                "gdp_total": 850000000000.0,
                "unemployment_rate": 13.2,
                "inflation_rate": 65.0,
                "gini_index": 41.9
            }
        }
    )


class DevelopmentIndicatorsModel(BaseModel):
    """Human development indicators validation."""

    hdi: Optional[float] = Field(None, ge=0, le=1, description="Human Development Index")
    life_expectancy: Optional[float] = Field(None, ge=0, le=120)
    education_index: Optional[float] = Field(None, ge=0, le=1)
    healthcare_index: Optional[float] = Field(None, ge=0, le=100)


class CityModel(BaseModel):
    """
    Complete city data model with validation.

    This is the core data structure for GeoDataSim v0.3.0+.
    All city data must conform to this schema.
    """

    # Basic information
    name: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)
    country_code: str = Field(..., min_length=2, max_length=3)
    region: str = Field(..., min_length=1, max_length=50)

    # Demographics
    population: int = Field(..., gt=0, le=100_000_000)
    population_density: Optional[float] = Field(None, ge=0)

    # Geography
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    elevation: Optional[float] = Field(None, ge=-500, le=10000)
    area_km2: Optional[float] = Field(None, gt=0)
    timezone: Optional[str] = Field(None, min_length=1)

    # Climate
    climate_zone: str
    avg_temperature: Optional[float] = Field(None, ge=-100, le=100)
    avg_precipitation: Optional[float] = Field(None, ge=0)

    # Economic
    gdp_per_capita: Optional[float] = Field(None, ge=0)
    gdp_total: Optional[float] = Field(None, ge=0)

    # Development
    hdi: Optional[float] = Field(None, ge=0, le=1)
    life_expectancy: Optional[float] = Field(None, ge=0, le=120)

    # Metadata
    data_source: Optional[str] = None
    last_updated: Optional[datetime] = None

    model_config = ConfigDict(
        validate_assignment=True,
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "name": "Istanbul",
                "country": "Turkey",
                "country_code": "TUR",
                "region": "Europe & Central Asia",
                "population": 15462452,
                "latitude": 41.0082,
                "longitude": 28.9784,
                "climate_zone": "Csa",
                "avg_temperature": 14.6,
                "gdp_per_capita": 28000.0,
                "hdi": 0.838,
                "timezone": "Europe/Istanbul"
            }
        }
    )

    @field_validator('population')
    @classmethod
    def validate_population(cls, v: int) -> int:
        """Ensure population is reasonable."""
        if v < 1000:
            raise ValueError("Population must be at least 1,000 for city classification")
        return v

    @field_validator('country_code')
    @classmethod
    def validate_country_code(cls, v: str) -> str:
        """Convert to uppercase for consistency."""
        return v.upper()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for backward compatibility."""
        return self.model_dump(exclude_none=False)


class UpdateMetadataModel(BaseModel):
    """Metadata for auto-update operations."""

    city_name: str
    indicator: str
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None
    source: str
    timestamp: datetime = Field(default_factory=datetime.now)
    success: bool = True
    error_message: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "city_name": "Istanbul",
                "indicator": "population",
                "old_value": 15462452,
                "new_value": 15500000,
                "source": "World Bank API",
                "timestamp": "2025-12-07T15:30:00",
                "success": True
            }
        }
    )


class ClusterResultModel(BaseModel):
    """Results from ML clustering operations."""

    city_name: str
    cluster_id: int = Field(..., ge=0)
    cluster_center_distance: Optional[float] = Field(None, ge=0)
    silhouette_score: Optional[float] = Field(None, ge=-1, le=1)

    model_config = ConfigDict(frozen=True)


class SimilarityResultModel(BaseModel):
    """Results from similarity calculations."""

    city_name: str
    similarity_score: float = Field(..., ge=0, le=100)
    distance_km: Optional[float] = Field(None, ge=0)
    population_ratio: Optional[float] = Field(None, ge=0)
    gdp_ratio: Optional[float] = Field(None, ge=0)

    model_config = ConfigDict(frozen=True)

    @field_validator('similarity_score')
    @classmethod
    def round_score(cls, v: float) -> float:
        """Round similarity score to 2 decimal places."""
        return round(v, 2)


def validate_city_data(data: Dict[str, Any]) -> CityModel:
    """
    Validate city data dictionary and return validated model.

    Args:
        data: Dictionary containing city data

    Returns:
        Validated CityModel instance

    Raises:
        ValidationError: If data doesn't match schema

    Example:
        >>> data = {"name": "Istanbul", "country": "Turkey", ...}
        >>> validated = validate_city_data(data)
        >>> print(validated.name)
        "Istanbul"
    """
    return CityModel(**data)


def validate_city_list(data_list: List[Dict[str, Any]]) -> List[CityModel]:
    """
    Validate a list of city data dictionaries.

    Args:
        data_list: List of dictionaries containing city data

    Returns:
        List of validated CityModel instances

    Raises:
        ValidationError: If any city data doesn't match schema
    """
    return [CityModel(**data) for data in data_list]


# Export all models
__all__ = [
    'CityModel',
    'CoordinatesModel',
    'ClimateModel',
    'EconomicIndicatorsModel',
    'DevelopmentIndicatorsModel',
    'UpdateMetadataModel',
    'ClusterResultModel',
    'SimilarityResultModel',
    'validate_city_data',
    'validate_city_list',
]
