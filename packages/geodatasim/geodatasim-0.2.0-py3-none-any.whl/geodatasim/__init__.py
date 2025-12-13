"""
GeoDataSim - Geographic + Socioeconomic + Climate Intelligence Library

Create intelligent city profiles with a single line of code.
All data from public domain sources (World Bank, OurAirports, UN).

v0.2.0: Now with Batch Analysis + Rankings + Export + pandas Integration!

Quick Start:
    >>> from geodatasim import City
    >>> istanbul = City("Istanbul")
    >>> print(istanbul.population, istanbul.gdp_per_capita)
    >>> similar = istanbul.find_similar(n=5)

New in v0.2.0:
    >>> from geodatasim.analysis import BatchAnalyzer, CityRankings, DataExporter
    >>> analyzer = BatchAnalyzer(["Istanbul", "Paris", "Tokyo"])
    >>> df = analyzer.to_dataframe()
    >>> analyzer.to_csv("cities.csv")
"""

from .version import __version__

from .core.city import City
from .core.config import Config, get_config, set_config
from .models.indicators import EconomicIndicators, ClimateProfile
from .utils.similarity import CitySimilarity

# New in v0.2.0: Analysis tools
try:
    from .analysis import (
        BatchAnalyzer,
        compare_cities,
        CityRankings,
        rank_cities,
        DataExporter,
        export_to_dataframe,
    )
    _ANALYSIS_AVAILABLE = True
except ImportError:
    _ANALYSIS_AVAILABLE = False

__all__ = [
    "__version__",
    # Core
    "City",
    "Config",
    "get_config",
    "set_config",
    # Models
    "EconomicIndicators",
    "ClimateProfile",
    "CitySimilarity",
]

# Add analysis tools if available
if _ANALYSIS_AVAILABLE:
    __all__.extend([
        "BatchAnalyzer",
        "compare_cities",
        "CityRankings",
        "rank_cities",
        "DataExporter",
        "export_to_dataframe",
    ])
