# 🌍 GeoDataSim v0.3.0 - Intelligence Boost

**World's most comprehensive city data platform with ML, auto-update, and visualization**

[![PyPI version](https://badge.fury.io/py/geodatasim.svg)](https://pypi.org/project/geodatasim/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Geographic + Socioeconomic + Climate intelligence library with **ML clustering**, **auto-update engine**, and **interactive visualization**. All data from free public APIs (World Bank, REST Countries, Open-Meteo).

---

## 🚀 What's NEW in v0.3.0 - Intelligence Boost

### 🤖 ML-Powered Intelligence
- **City Clustering** (KMeans, DBSCAN, Agglomerative)
- **10x Faster Similarity** (numba JIT optimization)
- **Advanced Feature Engineering** (sklearn integration)

### 📊 Interactive Visualization
- **Plotly Charts** (scatter, heatmap, radar, bar, geo)
- **Export to HTML** (interactive, shareable)
- **Quick visualization APIs**

### 🔄 Auto-Update Engine
- **Monthly data refresh** from World Bank API
- **30-day cache** (avoids unnecessary API calls)
- **Update history tracking**
- **No API key required** (100% free sources)

### ✅ Production-Ready Features
- **Pydantic validation** (type-safe data models)
- **Progress bars** (tqdm integration)
- **Enhanced geopy** distance calculations
- **Comprehensive error handling**

---

## 📦 Installation

```bash
pip install geodatasim
```

**Requirements**: Python 3.10+

---

## ⚡ Quick Start

### Basic Usage

```python
from geodatasim import City

# Create city with automatic data loading
istanbul = City("Istanbul")

print(f"Population: {istanbul.population:,}")
print(f"GDP per capita: ${istanbul.gdp_per_capita:,.2f}")
print(f"Climate: {istanbul.climate_zone} ({istanbul.avg_temperature}°C)")
print(f"HDI: {istanbul.hdi}")

# Find similar cities
similar = istanbul.find_similar(n=5)
for city in similar:
    print(f"  - {city.name}, {city.country}")
```

### 🆕 ML Clustering (v0.3.0)

```python
from geodatasim.ml import CityClustering, cluster_cities
from geodatasim.analysis import BatchAnalyzer

# Get data
analyzer = BatchAnalyzer(["Istanbul", "Paris", "Tokyo", "New York"])
df = analyzer.to_dataframe()

# Cluster cities
clustering = CityClustering(n_clusters=3, method='kmeans')
clustering.fit(df)

print(f"Silhouette score: {clustering.silhouette_score_:.3f}")
summary = clustering.get_cluster_summary(df)
print(summary)
```

### 🆕 Interactive Visualization (v0.3.0)

```python
from geodatasim.viz import CityVisualizer

viz = CityVisualizer()

# Scatter plot
fig = viz.scatter(df, x='population', y='gdp_per_capita',
                  color='region', size='population')
fig.show()  # Interactive in browser
fig.write_html("cities.html")

# Correlation heatmap
viz.heatmap(df, columns=['population', 'gdp', 'hdi']).show()

# Radar chart comparison
viz.radar(df, metrics=['population', 'gdp', 'hdi'],
          cities=['Istanbul', 'Paris', 'Tokyo']).show()
```

### 🆕 Auto-Update Engine (v0.3.0)

```python
from geodatasim.core.updater import UpdateEngine

engine = UpdateEngine()

# Check if update needed (30-day interval)
needs_update = engine.should_update('Istanbul', 'population')

# Update single city from APIs
updated = engine.update_city_all(city_data)

# Update all cities with progress bar
updated_cities = engine.update_all_cities(cities_list)
```

---

## 📊 Features

### v0.3.0 - Intelligence Boost 🆕
- 🤖 ML Clustering (KMeans, DBSCAN, Agglomerative)
- ⚡ 10x Faster Similarity (numba optimization)
- 📊 Interactive Visualization (plotly)
- 🔄 Auto-Update Engine (monthly refresh)
- ✅ Pydantic Validation
- 📈 Progress Bars (tqdm)

### v0.2.0 - Data Science Tools
- ✅ Batch Analysis
- ✅ Rankings & Filtering
- ✅ Export (CSV, Excel, JSON, Markdown)
- ✅ pandas Integration
- ✅ Statistical Analysis

### v0.1.0 - Core Features
- ✅ 46 cities from 36 countries
- ✅ 20+ data fields per city
- ✅ World Bank API integration
- ✅ Smart caching (90-day TTL)
- ✅ City similarity algorithm
- ✅ Distance calculations

---

## 📈 Data Sources

All from **free, public domain** sources:

| Source | Data | API Key Required |
|--------|------|------------------|
| **World Bank** | GDP, Population, HDI | ❌ No |
| **REST Countries** | Country metadata | ❌ No |
| **Open-Meteo** | Climate data | ❌ No |

✅ **Safe for commercial use** - All sources are public domain

---

## 🎯 Use Cases

**Data Science & ML**
```python
from geodatasim.ml import CityClustering
clustering = CityClustering(n_clusters=5)
clustering.fit(cities_df)
```

**Urban Planning**
```python
istanbul = City("Istanbul")
similar = istanbul.find_similar(min_population=5_000_000)
```

**Business Intelligence**
```python
from geodatasim.analysis import CityRankings
rankings = CityRankings()
wealthy_cities = rankings.filter_cities(min_gdp=40000)
```

**Interactive Dashboards**
```python
from geodatasim.viz import CityVisualizer
viz = CityVisualizer()
viz.scatter(df, 'population', 'gdp').show()
```

---

## 📖 Examples

```bash
# Test basic features
python test_v0_3_0.py

# Run comprehensive examples
python examples/v0_3_0_intelligence_boost.py
```

---

## 🛣️ Roadmap

**v0.4.0** - Performance (Polars, UMAP, PyArrow)
**v0.5.0** - Geo Intelligence (geopandas, folium)
**v1.0.0** - Complete Platform (100+ cities, predictions)

---

## 📄 License

MIT License

---

## 📬 Contact

**PyPI**: [pypi.org/project/geodatasim](https://pypi.org/project/geodatasim/)
**GitHub**: [github.com/teyfikoz/GeoDataSim](https://github.com/teyfikoz/GeoDataSim)

---

**GeoDataSim v0.3.0** 🚀
*ML · Visualization · Auto-Update · Intelligence*
