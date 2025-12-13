"""Version information for GeoDataSim."""

__version__ = "0.3.1"
__version_info__ = (0, 3, 1)

# Feature flags v0.2.0
WORLDBANK_ENABLED = True  # ✅ World Bank API integration
STATIC_DATASET_ENABLED = True  # ✅ 46 cities built-in
CACHING_ENABLED = True  # ✅ Smart caching system
SIMILARITY_ENABLED = True  # ✅ City similarity algorithm
DISTANCE_ENABLED = True  # ✅ Geographic distance calculations
BATCH_ANALYSIS_ENABLED = True  # ✅ Batch comparison of multiple cities
RANKINGS_ENABLED = True  # ✅ City rankings and leaderboards
EXPORT_ENABLED = True  # ✅ Export to CSV, Excel, JSON, Markdown
PANDAS_INTEGRATION = True  # ✅ Full pandas DataFrame support
STATISTICAL_ANALYSIS = True  # ✅ Statistical analysis tools

# NEW in v0.3.0 - INTELLIGENCE BOOST
AUTO_UPDATE_ENABLED = True  # ✅ Monthly automatic data updates
ML_CLUSTERING_ENABLED = True  # ✅ ML-powered city clustering (sklearn)
ML_SIMILARITY_ENABLED = True  # ✅ Enhanced similarity with numba
VISUALIZATION_ENABLED = True  # ✅ Interactive charts (plotly)
PYDANTIC_VALIDATION = True  # ✅ Data validation with pydantic
GEOPY_DISTANCE = True  # ✅ Enhanced distance calculations
PROGRESS_BARS = True  # ✅ Professional progress indicators (tqdm)

# Coming in future versions
POLARS_BACKEND = False  # v0.4.0 - Polars for 10-50x performance
UMAP_EMBEDDINGS = False  # v0.4.0 - 2D/3D city embeddings
PARQUET_EXPORT = False  # v0.4.0 - PyArrow parquet support
GEOPANDAS_INTEGRATION = False  # v0.5.0 - Shapefile/GeoJSON support
FOLIUM_MAPS = False  # v0.5.0 - Interactive HTML maps
WHO_DATA_ENABLED = False  # v0.5.0 - WHO health indicators
PREDICTIVE_MODELING = False  # v1.0.0 - GDP/population forecasting
VIZFORGE_INTEGRATION = False  # v1.0.0 - VizForge library integration
