"""Version information for GeoDataSim."""

__version__ = "0.2.0"
__version_info__ = (0, 2, 0)

# Feature flags v0.2.0
WORLDBANK_ENABLED = True  # ✅ World Bank API integration
STATIC_DATASET_ENABLED = True  # ✅ 46 cities built-in
CACHING_ENABLED = True  # ✅ Smart caching system
SIMILARITY_ENABLED = True  # ✅ City similarity algorithm
DISTANCE_ENABLED = True  # ✅ Geographic distance calculations

# NEW in v0.2.0
BATCH_ANALYSIS_ENABLED = True  # ✅ Batch comparison of multiple cities
RANKINGS_ENABLED = True  # ✅ City rankings and leaderboards
EXPORT_ENABLED = True  # ✅ Export to CSV, Excel, JSON, Markdown
PANDAS_INTEGRATION = True  # ✅ Full pandas DataFrame support
STATISTICAL_ANALYSIS = True  # ✅ Statistical analysis tools

# Coming in future versions
OPENWEATHER_ENABLED = False  # v0.3.0 - Real-time weather
AIRPORTS_ENABLED = False  # v0.3.0 - Airport data
UN_DATA_ENABLED = False  # v0.3.0 - UN statistics
VISUALIZATION_ENABLED = False  # v0.3.0 - Built-in charts
WHO_DATA_ENABLED = False  # v0.4.0 - WHO health indicators
TRAVEL_PURPOSE_INTEGRATION = False  # v0.4.0 - travelpurpose library
ETHNIDATA_INTEGRATION = False  # v0.4.0 - ethnidata library
