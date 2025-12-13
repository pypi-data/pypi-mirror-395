# GeoDataSim

**The Ultimate Geographic + Socioeconomic + Climate Intelligence Library**

Create intelligent city profiles with a single line of code. No API keys needed for most features, completely free and open-source.

## Features

- 🌍 **Geographic Intelligence** - Population, coordinates, timezones, regions
- 💰 **Economic Data** - GDP per capita, HDI, development indicators
- ✈️ **Travel Intelligence** - Nearby airports, distances, routes
- 🌤️ **Climate Data** - Weather patterns, climate zones, temperature ranges
- 🏙️ **City Similarity** - Find similar cities based on multiple dimensions
- 📊 **Rich Indicators** - 50+ socioeconomic indicators from World Bank
- 🔄 **Smart Caching** - Fast responses with intelligent data caching
- 🆓 **Mostly Free** - Uses public domain data sources (World Bank, OurAirports, UN)

## Quick Start

```python
from geodatasim import City

# Create a city profile
istanbul = City("Istanbul")

# Basic info
print(istanbul.population)          # 15,462,452
print(istanbul.country)             # Turkey
print(istanbul.coordinates)         # (41.0082, 28.9784)

# Economic indicators
print(istanbul.gdp_per_capita)      # From World Bank
print(istanbul.hdi)                 # Human Development Index

# Climate
print(istanbul.climate_zone)        # Mediterranean
print(istanbul.avg_temperature)     # 14.6°C

# Travel
print(istanbul.nearby_airports)     # [IST, SAW, ...]
print(istanbul.timezone)            # Europe/Istanbul

# Find similar cities
similar = istanbul.find_similar(n=5)
print(similar)  # [Athens, Barcelona, Rome, ...]
```

## Installation

```bash
# Basic installation (no API keys needed)
pip install geodatasim

# With real-time weather (requires free OpenWeather API key)
pip install geodatasim[weather]

# Full installation
pip install geodatasim[full]
```

## Data Sources

All data from legal, public domain sources:

- **[World Bank Open Data](https://data.worldbank.org)** - Economic indicators (Public Domain)
- **[OurAirports](https://ourairports.com/data/)** - Airport data (Public Domain, MIT License)
- **[Open-Meteo](https://open-meteo.com/)** - Climate data (Open Source, Free)
- **UN Data** - Country statistics (Open License)
- **Natural Earth** - Geographic boundaries (Public Domain)

## Features (v0.1.0)

### Core Features
- ✅ City class with 50+ attributes
- ✅ World Bank API integration (GDP, HDI, indicators)
- ✅ OurAirports integration (nearby airports)
- ✅ Climate zone classification
- ✅ City similarity algorithm
- ✅ Smart caching system (90-day cache)
- ✅ Built-in dataset for 500+ major cities

### Upcoming (v0.2.0+)
- 🔄 Real-time weather integration
- 🔄 UN Data indicators
- 🔄 Cost of living estimates
- 🔄 Safety indices
- 🔄 Cultural dimensions
- 🔄 Travel purpose integration (from travelpurpose library)
- 🔄 Ethnic diversity data (from ethnidata library)

## Use Cases

- 📊 **Data Science** - City embeddings for ML models
- 🗺️ **Urban Planning** - Compare cities, analyze development
- ✈️ **Travel Tech** - Destination recommendations, similarity search
- 💼 **Business Intelligence** - Market analysis, expansion planning
- 🎓 **Research** - Academic studies, geographic analysis
- 📱 **App Development** - Location-based features, personalization

## Architecture

```
GeoDataSim
├── Static Dataset (500+ cities, instant response)
├── Cached API Data (World Bank, 90-day refresh)
└── Real-time APIs (Optional, user's API key)
```

**Smart 3-Layer Strategy:**
1. **Built-in data** - Instant, no API calls
2. **Cached data** - Fast, updated quarterly
3. **Real-time data** - Optional, for fresh data

## Example: City Comparison

```python
from geodatasim import City

cities = [City(name) for name in ["Istanbul", "Barcelona", "Athens"]]

for city in cities:
    print(f"{city.name}:")
    print(f"  Population: {city.population:,}")
    print(f"  GDP/capita: ${city.gdp_per_capita:,.0f}")
    print(f"  Climate: {city.climate_zone}")
    print(f"  Airports: {len(city.nearby_airports)}")
    print()
```

## Example: Find Similar Cities

```python
from geodatasim import City

paris = City("Paris")

# Find similar cities based on:
# - Population size
# - Economic development
# - Climate zone
# - Geographic region
similar = paris.find_similar(n=10)

for i, city in enumerate(similar, 1):
    print(f"{i}. {city.name} (similarity: {city.similarity_score:.2%})")
```

## API Keys (Optional)

Most features work without any API keys. For real-time weather data:

```python
from geodatasim import Config

# Optional: Set API keys for enhanced features
Config.set_api_key("openweather", "your_free_api_key")
```

Get free API keys:
- OpenWeather: https://openweathermap.org/api (1,000 calls/day free)
- Open-Meteo: No API key needed! (Unlimited free)

## Performance

- **Built-in data**: < 1ms response time
- **Cached API data**: < 10ms response time
- **Real-time API**: < 500ms response time
- **City similarity**: < 100ms for 1000 cities

## Requirements

- Python >= 3.10
- requests >= 2.31.0
- pandas >= 2.0.0
- numpy >= 1.24.0

## License

MIT License - Free for commercial use

## Contributing

Contributions welcome! This library fills a real gap in the Python ecosystem.

## Links

- GitHub: https://github.com/teyfikoz/GeoDataSim
- PyPI: https://pypi.org/project/geodatasim/
- Documentation: https://github.com/teyfikoz/GeoDataSim/docs

---

**GeoDataSim v0.1.0: City Intelligence, Simplified.**

**Sources:**
- [World Bank Open Data API](https://api.worldbank.org)
- [OurAirports Open Data](https://ourairports.com/data/)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [Open-Meteo Weather API](https://open-meteo.com/)
