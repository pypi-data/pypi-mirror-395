"""
Advanced analysis examples for GeoDataSim v0.2.0.

Demonstrates new features:
- Batch comparison
- Rankings and filtering
- Data export
- Statistical analysis
"""

from geodatasim import City
from geodatasim.analysis import (
    BatchAnalyzer, compare_cities,
    CityRankings, rank_cities,
    DataExporter, export_to_dataframe
)


def example_batch_comparison():
    """Example: Compare multiple cities at once."""
    print("=" * 70)
    print("EXAMPLE 1: Batch City Comparison")
    print("=" * 70)

    # Create batch analyzer
    cities = ["Istanbul", "Paris", "London", "Tokyo", "New York", "Dubai"]
    analyzer = BatchAnalyzer(cities)

    # Get as DataFrame
    print("\n📊 Cities as DataFrame:")
    df = analyzer.to_dataframe(['name', 'country', 'population', 'eco_gdp_per_capita'])
    print(df.to_string(index=False))

    # Compare specific metrics
    print("\n📈 Comparison by key metrics:")
    comparison = analyzer.compare(['population', 'eco_gdp_per_capita', 'eco_hdi'])
    print(comparison.to_string(index=False))

    # Summary statistics
    print("\n📋 Summary statistics:")
    stats = analyzer.summary_stats()
    for key, value in stats.items():
        print(f"   {key:25s}: {value}")

    # Find correlations
    print("\n🔗 Correlation (population vs GDP):")
    corr = analyzer.find_correlations('population', 'eco_gdp_per_capita')
    print(f"   Correlation coefficient: {corr:.3f}")

    print()


def example_rankings():
    """Example: City rankings and leaderboards."""
    print("=" * 70)
    print("EXAMPLE 2: City Rankings")
    print("=" * 70)

    rankings = CityRankings()

    # Top 10 by population
    print("\n👥 Top 10 Cities by Population:")
    top_pop = rankings.top_by_population(10)
    print(top_pop.to_string(index=False))

    # Top 10 by GDP
    print("\n💰 Top 10 Cities by GDP per Capita:")
    top_gdp = rankings.top_by_gdp(10)
    print(top_gdp.to_string(index=False))

    # Top 10 by HDI
    print("\n🎓 Top 10 Cities by Human Development Index:")
    top_hdi = rankings.top_by_hdi(10)
    print(top_hdi.to_string(index=False))

    # Filter cities
    print("\n🔍 Filtered: Large wealthy cities (pop>5M, GDP>$40k):")
    filtered = rankings.filter_cities(
        min_population=5_000_000,
        min_gdp=40000
    )
    print(filtered.to_string(index=False))

    print()


def example_regional_analysis():
    """Example: Regional analysis."""
    print("=" * 70)
    print("EXAMPLE 3: Regional Analysis")
    print("=" * 70)

    rankings = CityRankings()

    # Summary by region
    print("\n🌍 Summary by Region:")
    regional = rankings.summary_by_region()
    print(regional)

    # Cities in Europe
    print("\n🇪🇺 European Cities:")
    europe = rankings.by_region('Europe & Central Asia')
    print(europe.head(10).to_string(index=False))

    # Mediterranean climate cities
    print("\n🌞 Mediterranean Climate Cities (Csa):")
    mediterranean = rankings.by_climate_zone('Csa')
    print(mediterranean.to_string(index=False))

    print()


def example_data_export():
    """Example: Export data to various formats."""
    print("=" * 70)
    print("EXAMPLE 4: Data Export")
    print("=" * 70)

    # Select cities to export
    cities = ["Istanbul", "Paris", "Tokyo", "New York", "Dubai",
              "Singapore", "Sydney", "London", "Barcelona", "Mumbai"]

    exporter = DataExporter(cities)

    # Export to CSV
    print("\n💾 Exporting to CSV...")
    exporter.to_csv("output/cities_data.csv")
    print("   ✅ Saved to: output/cities_data.csv")

    # Export to Excel
    print("\n📊 Exporting to Excel...")
    exporter.to_excel("output/cities_data.xlsx", sheet_name="Cities")
    print("   ✅ Saved to: output/cities_data.xlsx")

    # Export to JSON
    print("\n📋 Exporting to JSON...")
    exporter.to_json("output/cities_data.json", orient='records', indent=2)
    print("   ✅ Saved to: output/cities_data.json")

    # Export to Markdown
    print("\n📝 Exporting to Markdown...")
    exporter.to_markdown("output/cities_data.md")
    print("   ✅ Saved to: output/cities_data.md")

    # Quick DataFrame export
    print("\n⚡ Quick DataFrame export:")
    df = export_to_dataframe(["Istanbul", "Paris", "Tokyo"])
    print(df[['name', 'country', 'population']].to_string(index=False))

    print()


def example_advanced_filtering():
    """Example: Advanced filtering and analysis."""
    print("=" * 70)
    print("EXAMPLE 5: Advanced Filtering")
    print("=" * 70)

    rankings = CityRankings()

    # Complex filter
    print("\n🎯 Complex Filter: European cities, pop 2-10M, high HDI:")
    filtered = rankings.filter_cities(
        min_population=2_000_000,
        max_population=10_000_000,
        min_hdi=0.90,
        regions=['Europe & Central Asia']
    )
    print(filtered.to_string(index=False))

    # Rank by temperature
    print("\n🌡️  Warmest Cities:")
    warmest = rankings.rankings_by_metric('avg_temperature', ascending=False, n=10)
    print(warmest.to_string(index=False))

    # Rank by temperature (coldest)
    print("\n❄️  Coldest Cities:")
    coldest = rankings.rankings_by_metric('avg_temperature', ascending=True, n=10)
    print(coldest.to_string(index=False))

    print()


def example_similarity_with_batch():
    """Example: Find similar cities using batch operations."""
    print("=" * 70)
    print("EXAMPLE 6: Similarity Analysis")
    print("=" * 70)

    # Reference city
    istanbul = City("Istanbul")

    print(f"\n🔍 Cities most similar to {istanbul.name}:")
    similar = istanbul.find_similar(n=10)

    # Create batch for comparison
    similar_names = [city.name for city in similar]
    analyzer = BatchAnalyzer(similar_names + ["Istanbul"])

    # Compare them
    comparison = analyzer.compare(['population', 'eco_gdp_per_capita', 'climate_avg_temperature'])
    print(comparison.to_string(index=False))

    print()


def example_statistical_analysis():
    """Example: Statistical analysis of cities."""
    print("=" * 70)
    print("EXAMPLE 7: Statistical Analysis")
    print("=" * 70)

    # All major cities
    cities = ["Istanbul", "Paris", "London", "Tokyo", "New York", "Dubai",
              "Singapore", "Sydney", "Mumbai", "Shanghai", "Cairo",
              "Mexico City", "Sao Paulo", "Los Angeles", "Chicago"]

    analyzer = BatchAnalyzer(cities)
    df = analyzer.to_dataframe()

    # Basic statistics
    print("\n📊 Population Statistics:")
    print(df['population'].describe())

    print("\n💰 GDP per Capita Statistics:")
    print(df['eco_gdp_per_capita'].describe())

    # Group by region
    print("\n🌍 Average GDP by Region:")
    by_region = analyzer.group_by_region()
    for region, city_list in by_region.items():
        print(f"   {region:35s}: {len(city_list)} cities")

    print()


def main():
    """Run all examples."""
    import os
    os.makedirs("output", exist_ok=True)

    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 12 + "GeoDataSim v0.2.0 - Advanced Analysis" + " " * 18 + "║")
    print("╚" + "═" * 68 + "╝")
    print()

    example_batch_comparison()
    example_rankings()
    example_regional_analysis()
    example_data_export()
    example_advanced_filtering()
    example_similarity_with_batch()
    example_statistical_analysis()

    print("=" * 70)
    print("All examples completed!")
    print("=" * 70)
    print("\n✅ Check the 'output/' directory for exported files")
    print("📊 Data exported to: CSV, Excel, JSON, Markdown")
    print()


if __name__ == "__main__":
    main()
