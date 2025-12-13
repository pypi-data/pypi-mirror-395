"""
GeoDataSim - Geographic + Socioeconomic + Climate Intelligence Library

World's most comprehensive city data platform with ML, auto-update, and visualization.
All data from public domain sources (World Bank, REST Countries, Open-Meteo).

v0.3.0: Intelligence Boost - ML + Auto-Update + Visualization!

Quick Start:
    >>> from geodatasim import City
    >>> istanbul = City("Istanbul")
    >>> print(istanbul.population, istanbul.gdp_per_capita)
    >>> similar = istanbul.find_similar(n=5)

NEW in v0.3.0:
    >>> # Auto-update from APIs
    >>> from geodatasim.core.updater import update_city_data
    >>> updated = update_city_data(istanbul_data)

    >>> # ML Clustering
    >>> from geodatasim.ml import CityClustering
    >>> clustering = CityClustering(n_clusters=5)
    >>> clustering.fit(cities_df)

    >>> # Interactive Visualization
    >>> from geodatasim.viz import CityVisualizer
    >>> viz = CityVisualizer()
    >>> viz.scatter(cities_df, 'population', 'gdp_per_capita').show()

v0.2.0 Features:
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

# v0.2.0: Analysis tools
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

# NEW in v0.3.0: ML, Auto-Update, Visualization
try:
    from .ml import (
        CityClustering,
        cluster_cities,
        find_similar_cluster,
        FastSimilarityEngine,
        find_similar_fast,
    )
    _ML_AVAILABLE = True
except ImportError:
    _ML_AVAILABLE = False

try:
    from .viz import (
        CityVisualizer,
        quick_scatter,
        quick_heatmap,
        quick_radar,
    )
    _VIZ_AVAILABLE = True
except ImportError:
    _VIZ_AVAILABLE = False

try:
    from .core.updater import (
        UpdateEngine,
        update_city_data,
        update_all_cities_data,
    )
    _UPDATER_AVAILABLE = True
except ImportError:
    _UPDATER_AVAILABLE = False

try:
    from .core.validator import (
        CityModel,
        validate_city_data,
    )
    _VALIDATOR_AVAILABLE = True
except ImportError:
    _VALIDATOR_AVAILABLE = False

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

# Add v0.2.0 analysis tools if available
if _ANALYSIS_AVAILABLE:
    __all__.extend([
        "BatchAnalyzer",
        "compare_cities",
        "CityRankings",
        "rank_cities",
        "DataExporter",
        "export_to_dataframe",
    ])

# Add v0.3.0 ML tools if available
if _ML_AVAILABLE:
    __all__.extend([
        "CityClustering",
        "cluster_cities",
        "find_similar_cluster",
        "FastSimilarityEngine",
        "find_similar_fast",
    ])

# Add v0.3.0 visualization tools if available
if _VIZ_AVAILABLE:
    __all__.extend([
        "CityVisualizer",
        "quick_scatter",
        "quick_heatmap",
        "quick_radar",
    ])

# Add v0.3.0 updater tools if available
if _UPDATER_AVAILABLE:
    __all__.extend([
        "UpdateEngine",
        "update_city_data",
        "update_all_cities_data",
    ])

# Add v0.3.0 validator tools if available
if _VALIDATOR_AVAILABLE:
    __all__.extend([
        "CityModel",
        "validate_city_data",
    ])
