"""
GeoDataSim - Geographic + Socioeconomic + Climate Intelligence Library

Create intelligent city profiles with a single line of code.
All data from public domain sources (World Bank, OurAirports, UN).

Quick Start:
    >>> from geodatasim import City
    >>> istanbul = City("Istanbul")
    >>> print(istanbul.population, istanbul.gdp_per_capita)
    >>> similar = istanbul.find_similar(n=5)
"""

__version__ = "0.1.0"

from .core.city import City
from .core.config import Config, get_config, set_config
from .models.indicators import EconomicIndicators, ClimateProfile
from .utils.similarity import CitySimilarity

__all__ = [
    "__version__",
    "City",
    "Config",
    "get_config",
    "set_config",
    "EconomicIndicators",
    "ClimateProfile",
    "CitySimilarity",
]
