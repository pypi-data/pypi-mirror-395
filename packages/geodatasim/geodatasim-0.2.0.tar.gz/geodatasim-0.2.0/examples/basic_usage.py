"""
Basic usage examples for GeoDataSim.

Run this file to see GeoDataSim in action!
"""

from geodatasim import City, set_config


def example_basic():
    """Basic city data retrieval."""
    print("=" * 60)
    print("EXAMPLE 1: Basic City Data")
    print("=" * 60)

    # Create a city object
    istanbul = City("Istanbul")

    # Access basic info
    print(f"\nCity: {istanbul.name}")
    print(f"Country: {istanbul.country_name}")
    print(f"Population: {istanbul.population:,}")
    print(f"Coordinates: {istanbul.coordinates}")
    print(f"Timezone: {istanbul.timezone}")
    print()


def example_economic_data():
    """Economic and development indicators."""
    print("=" * 60)
    print("EXAMPLE 2: Economic Indicators")
    print("=" * 60)

    cities = ["Istanbul", "London", "Tokyo", "New York"]

    for city_name in cities:
        city = City(city_name)
        print(f"\n{city.name}, {city.country_name}:")
        print(f"  GDP per capita: ${city.gdp_per_capita:,.0f}" if city.gdp_per_capita else "  GDP: N/A")
        print(f"  HDI: {city.hdi:.3f}" if city.hdi else "  HDI: N/A")
        print(f"  Life expectancy: {city.life_expectancy:.1f} years" if city.life_expectancy else "  Life exp: N/A")

    print()


def example_distance():
    """Calculate distances between cities."""
    print("=" * 60)
    print("EXAMPLE 3: Distance Calculation")
    print("=" * 60)

    istanbul = City("Istanbul")
    cities = [City(name) for name in ["Ankara", "Athens", "Rome", "Paris"]]

    print(f"\nDistances from {istanbul.name}:\n")

    for city in cities:
        distance = istanbul.distance_to(city)
        if distance:
            print(f"  → {city.name:15s}: {distance:6.0f} km")

    print()


def example_similarity():
    """Find similar cities."""
    print("=" * 60)
    print("EXAMPLE 4: Find Similar Cities")
    print("=" * 60)

    istanbul = City("Istanbul")

    print(f"\nCities similar to {istanbul.name}:\n")

    similar_cities = istanbul.find_similar(n=10)

    for i, city in enumerate(similar_cities, 1):
        similarity_score = getattr(city, 'similarity_score', 0)
        print(f"  {i:2d}. {city.name:20s} ({city.country_name:20s}) - {similarity_score:.1%} similar")

    print()


def example_city_comparison():
    """Compare multiple cities."""
    print("=" * 60)
    print("EXAMPLE 5: City Comparison")
    print("=" * 60)

    cities = [City(name) for name in ["Barcelona", "Athens", "Istanbul", "Lisbon"]]

    print("\nMediterranean Cities Comparison:\n")
    print(f"{'City':<15} {'Population':>12} {'GDP/capita':>12} {'Climate':>10} {'HDI':>6}")
    print("-" * 60)

    for city in cities:
        pop = f"{city.population:,}" if city.population else "N/A"
        gdp = f"${city.gdp_per_capita:,.0f}" if city.gdp_per_capita else "N/A"
        climate = city.climate_zone or "N/A"
        hdi = f"{city.hdi:.3f}" if city.hdi else "N/A"

        print(f"{city.name:<15} {pop:>12} {gdp:>12} {climate:>10} {hdi:>6}")

    print()


def example_climate():
    """Climate data."""
    print("=" * 60)
    print("EXAMPLE 6: Climate Data")
    print("=" * 60)

    cities = [City(name) for name in ["Singapore", "Oslo", "Dubai", "Sydney"]]

    print("\nClimate Diversity:\n")

    for city in cities:
        climate = city.climate_zone or "Unknown"
        temp = f"{city.avg_temperature:.1f}°C" if city.avg_temperature else "N/A"

        print(f"  {city.name:15s}: {climate:5s} climate, avg temp: {temp}")

    print()


def example_data_export():
    """Export city data to dictionary."""
    print("=" * 60)
    print("EXAMPLE 7: Data Export")
    print("=" * 60)

    paris = City("Paris")

    print(f"\nFull data for {paris.name}:\n")

    data = paris.to_dict()

    import json
    print(json.dumps(data, indent=2))

    print()


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "GeoDataSim v0.1.0 - Example Usage" + " " * 14 + "║")
    print("╚" + "═" * 58 + "╝")
    print()

    # Disable warnings for cleaner output
    set_config(show_warnings=False)

    # Run examples
    example_basic()
    example_economic_data()
    example_distance()
    example_similarity()
    example_city_comparison()
    example_climate()
    example_data_export()

    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)
    print("\nTry creating your own City objects:")
    print("  >>> from geodatasim import City")
    print("  >>> city = City('Your City')")
    print("  >>> print(city.to_dict())")
    print()


if __name__ == "__main__":
    main()
