"""Version information for GeoDataSim."""

__version__ = "0.1.0"
__version_info__ = (0, 1, 0)

# Feature flags
WORLDBANK_ENABLED = True  # ✅ World Bank API integration
STATIC_DATASET_ENABLED = True  # ✅ 50+ cities built-in
CACHING_ENABLED = True  # ✅ Smart caching system
SIMILARITY_ENABLED = True  # ✅ City similarity algorithm
DISTANCE_ENABLED = True  # ✅ Geographic distance calculations

# Coming in future versions
OPENWEATHER_ENABLED = False  # v0.2.0 - Real-time weather
AIRPORTS_ENABLED = False  # v0.2.0 - Airport data
UN_DATA_ENABLED = False  # v0.2.0 - UN statistics
WHO_DATA_ENABLED = False  # v0.3.0 - WHO health indicators
TRAVEL_PURPOSE_INTEGRATION = False  # v0.3.0 - travelpurpose library
ETHNIDATA_INTEGRATION = False  # v0.3.0 - ethnidata library
