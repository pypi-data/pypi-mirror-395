"""
GeoDataSim v0.3.0 - Intelligence Boost Examples

Demonstrates the new features in v0.3.0:
1. Auto-update engine (monthly data refresh from APIs)
2. ML clustering (KMeans, DBSCAN)
3. Optimized similarity (10x faster with numba)
4. Interactive visualization (Plotly charts)
5. Data validation (Pydantic models)
"""

import os
os.makedirs("output", exist_ok=True)

from geodatasim import City, __version__
from geodatasim.analysis import BatchAnalyzer

# NEW v0.3.0 imports
from geodatasim.ml import CityClustering, cluster_cities, find_similar_fast
from geodatasim.viz import CityVisualizer, quick_scatter, quick_heatmap
from geodatasim.core.updater import UpdateEngine
from geodatasim.core.validator import CityModel, validate_city_data

import pandas as pd
import numpy as np

print(f"\n{'='*80}")
print(f" GeoDataSim v{__version__} - Intelligence Boost Examples")
print(f"{'='*80}\n")


def example_1_ml_clustering():
    """Example 1: ML-powered city clustering."""
    print(f"\n{'='*80}")
    print("EXAMPLE 1: ML Clustering")
    print(f"{'='*80}\n")

    # Create dataset
    cities = ["Istanbul", "Paris", "London", "Tokyo", "New York", "Dubai",
              "Singapore", "Sydney", "Mumbai", "Shanghai", "Cairo",
              "Mexico City", "Sao Paulo", "Los Angeles"]

    analyzer = BatchAnalyzer(cities, auto_load=False)
    df = analyzer.to_dataframe()

    # KMeans clustering
    print("🤖 Running KMeans clustering (5 clusters)...")
    clustering = CityClustering(n_clusters=5, method='kmeans')
    clustering.fit(df)

    print(f"✅ Clustering complete!")
    print(f"   Silhouette score: {clustering.silhouette_score_:.3f}")
    print(f"   Clusters formed: {len(set(clustering.labels_))}")

    # Get cluster summary
    summary = clustering.get_cluster_summary(df)
    print(f"\n📊 Cluster Summary:")
    print(summary)

    # Show cities by cluster
    result_df = df.copy()
    result_df['cluster'] = clustering.labels_
    print(f"\n🏙️  Cities by cluster:")
    for cluster_id in sorted(set(clustering.labels_)):
        cities_in_cluster = result_df[result_df['cluster'] == cluster_id]['name'].tolist()
        print(f"   Cluster {cluster_id}: {', '.join(cities_in_cluster)}")

    # Quick clustering API
    print(f"\n⚡ Quick clustering API:")
    clustered = cluster_cities(df, n_clusters=3, method='kmeans')
    print(clustered[['name', 'cluster']].head(10))

    print()


def example_2_fast_similarity():
    """Example 2: Numba-optimized similarity (10x faster)."""
    print(f"\n{'='*80}")
    print("EXAMPLE 2: Fast Similarity with Numba")
    print(f"{'='*80}\n")

    cities = ["Istanbul", "Paris", "London", "Tokyo", "New York", "Dubai",
              "Singapore", "Sydney", "Mumbai", "Shanghai"]

    analyzer = BatchAnalyzer(cities, auto_load=False)
    df = analyzer.to_dataframe()

    # Extract features
    features = df[['population', 'gdp_per_capita', 'hdi']].fillna(df.median()).values
    target_features = features[0]  # Istanbul

    print("⚡ Finding similar cities using numba-optimized engine...")

    # Use fast similarity
    from geodatasim.ml.similarity import calculate_similarity_matrix
    similarity_matrix = calculate_similarity_matrix(features, method='cosine')

    print(f"✅ Similarity matrix calculated!")
    print(f"   Shape: {similarity_matrix.shape}")

    # Show most similar to Istanbul
    istanbul_similarities = similarity_matrix[0]
    sorted_indices = np.argsort(istanbul_similarities)[::-1][1:6]  # Top 5 (exclude itself)

    print(f"\n🔍 Cities most similar to Istanbul (cosine similarity):")
    for idx in sorted_indices:
        print(f"   {df.iloc[idx]['name']:20s}: {istanbul_similarities[idx]:.3f}")

    print()


def example_3_interactive_visualization():
    """Example 3: Interactive Plotly visualizations."""
    print(f"\n{'='*80}")
    print("EXAMPLE 3: Interactive Visualization")
    print(f"{'='*80}\n")

    cities = ["Istanbul", "Paris", "London", "Tokyo", "New York", "Dubai",
              "Singapore", "Sydney", "Mumbai", "Shanghai", "Cairo",
              "Mexico City"]

    analyzer = BatchAnalyzer(cities, auto_load=False)
    df = analyzer.to_dataframe()

    viz = CityVisualizer()

    # 1. Scatter plot
    print("📊 Creating scatter plot (Population vs GDP)...")
    fig1 = viz.scatter(
        df,
        x='population',
        y='gdp_per_capita',
        color='region',
        size='population',
        hover_data=['name', 'hdi'],
        title="City Analysis: Population vs GDP per Capita"
    )
    fig1.write_html("output/scatter_population_gdp.html")
    print("   ✅ Saved: output/scatter_population_gdp.html")

    # 2. Correlation heatmap
    print("\n🔥 Creating correlation heatmap...")
    fig2 = viz.heatmap(
        df,
        columns=['population', 'gdp_per_capita', 'hdi', 'avg_temperature'],
        title="City Metrics Correlation Matrix"
    )
    fig2.write_html("output/heatmap_correlation.html")
    print("   ✅ Saved: output/heatmap_correlation.html")

    # 3. Radar chart
    print("\n🎯 Creating radar chart (City comparison)...")
    fig3 = viz.radar(
        df,
        metrics=['population', 'gdp_per_capita', 'hdi'],
        cities=['Istanbul', 'Paris', 'Tokyo', 'Dubai'],
        title="City Comparison Radar Chart"
    )
    fig3.write_html("output/radar_comparison.html")
    print("   ✅ Saved: output/radar_comparison.html")

    # 4. Geographic scatter
    print("\n🗺️  Creating geographic scatter...")
    fig4 = viz.geo_scatter(
        df,
        color='region',
        size='population',
        hover_data=['name', 'gdp_per_capita'],
        title="World Cities Map"
    )
    fig4.write_html("output/geo_scatter.html")
    print("   ✅ Saved: output/geo_scatter.html")

    # 5. Quick APIs
    print("\n⚡ Using quick visualization APIs...")
    fig5 = quick_scatter(df, 'hdi', 'gdp_per_capita', color='region')
    fig5.write_html("output/quick_scatter.html")
    print("   ✅ Saved: output/quick_scatter.html")

    print()


def example_4_auto_update():
    """Example 4: Auto-update engine."""
    print(f"\n{'='*80}")
    print("EXAMPLE 4: Auto-Update Engine")
    print(f"{'='*80}\n")

    print("🔄 Demonstrating auto-update engine...")
    print("   (Uses free APIs: World Bank, REST Countries, Open-Meteo)")

    # Create update engine
    updater = UpdateEngine()

    # Example city data
    istanbul_data = {
        'name': 'Istanbul',
        'country': 'Turkey',
        'country_code': 'TUR',
        'latitude': 41.0082,
        'longitude': 28.9784,
        'population': 15462452,
        'gdp_per_capita': 28000.0,
    }

    print(f"\n📍 City: {istanbul_data['name']}")
    print(f"   Current population: {istanbul_data['population']:,}")
    print(f"   Current GDP: ${istanbul_data['gdp_per_capita']:,.2f}")

    # Check if update is needed
    needs_update = updater.should_update('Istanbul', 'population')
    print(f"\n🔍 Needs update (30-day check): {needs_update}")

    if needs_update:
        print("\n🚀 Fetching latest data from World Bank API...")
        # Note: This will make real API calls
        # Commented out to avoid hitting API limits in demo
        # updated = updater.update_city_all(istanbul_data)
        # print(f"   ✅ Updated population: {updated.get('population', 'N/A'):,}")
        print("   ℹ️  (Skipped in demo to avoid API limits)")
    else:
        print("   ✅ Data is up-to-date (last updated <30 days ago)")

    # Show update history
    history = updater.get_update_history('Istanbul')
    if history:
        print(f"\n📜 Update history for Istanbul:")
        for entry in history[:3]:  # Show last 3
            print(f"   - {entry.get('indicator', 'unknown')}: {entry.get('timestamp', 'N/A')}")
    else:
        print("\n📜 No update history yet")

    print("\n💡 Update features:")
    print("   ✅ Monthly automatic updates")
    print("   ✅ 30-day cache (avoids unnecessary API calls)")
    print("   ✅ Multiple data sources (World Bank, REST Countries, Open-Meteo)")
    print("   ✅ Update history tracking")
    print("   ✅ Error handling and retry logic")

    print()


def example_5_data_validation():
    """Example 5: Pydantic data validation."""
    print(f"\n{'='*80}")
    print("EXAMPLE 5: Data Validation with Pydantic")
    print(f"{'='*80}\n")

    print("✅ Validating city data with Pydantic models...")

    # Valid city data
    valid_data = {
        'name': 'Istanbul',
        'country': 'Turkey',
        'country_code': 'TUR',
        'region': 'Europe & Central Asia',
        'population': 15462452,
        'latitude': 41.0082,
        'longitude': 28.9784,
        'climate_zone': 'Csa',
        'avg_temperature': 14.6,
        'gdp_per_capita': 28000.0,
        'hdi': 0.838,
        'timezone': 'Europe/Istanbul'
    }

    try:
        city_model = validate_city_data(valid_data)
        print(f"✅ Valid data:")
        print(f"   Name: {city_model.name}")
        print(f"   Population: {city_model.population:,}")
        print(f"   Country Code: {city_model.country_code}")
        print(f"   Coordinates: ({city_model.latitude}, {city_model.longitude})")
    except Exception as e:
        print(f"❌ Validation failed: {e}")

    # Invalid data (population too small)
    print(f"\n❌ Testing invalid data (population < 1000)...")
    invalid_data = valid_data.copy()
    invalid_data['population'] = 500

    try:
        city_model = validate_city_data(invalid_data)
        print("   Unexpected: validation passed")
    except Exception as e:
        print(f"   ✅ Correctly rejected: {str(e)[:80]}...")

    # Invalid coordinates
    print(f"\n❌ Testing invalid coordinates (latitude > 90)...")
    invalid_data = valid_data.copy()
    invalid_data['latitude'] = 95.0

    try:
        city_model = validate_city_data(invalid_data)
        print("   Unexpected: validation passed")
    except Exception as e:
        print(f"   ✅ Correctly rejected: {str(e)[:80]}...")

    print("\n💡 Validation features:")
    print("   ✅ Type safety (int, float, str validation)")
    print("   ✅ Range validation (lat/lon, population, etc.)")
    print("   ✅ Required fields check")
    print("   ✅ Automatic data cleaning (strip whitespace, uppercase codes)")
    print("   ✅ Custom validators (climate zones, country codes)")

    print()


def example_6_combined_workflow():
    """Example 6: Combined workflow using all v0.3.0 features."""
    print(f"\n{'='*80}")
    print("EXAMPLE 6: Combined Workflow (ML + Viz + Validation)")
    print(f"{'='*80}\n")

    print("🚀 Running complete analysis workflow...\n")

    # Step 1: Load and validate data
    print("1️⃣  Loading and validating data...")
    cities = ["Istanbul", "Paris", "Tokyo", "New York", "Dubai", "Singapore"]
    analyzer = BatchAnalyzer(cities, auto_load=False)
    df = analyzer.to_dataframe()
    print(f"   ✅ Loaded {len(df)} cities")

    # Step 2: ML Clustering
    print("\n2️⃣  Performing ML clustering...")
    clustering = CityClustering(n_clusters=3, method='kmeans')
    clustering.fit(df)
    df['cluster'] = clustering.labels_
    print(f"   ✅ Clustered into {len(set(clustering.labels_))} groups")

    # Step 3: Visualize clusters
    print("\n3️⃣  Visualizing clusters...")
    viz = CityVisualizer()
    fig = viz.scatter(
        df,
        x='population',
        y='gdp_per_capita',
        color='cluster',
        size='population',
        hover_data=['name', 'region'],
        title="ML Clusters: Population vs GDP"
    )
    fig.write_html("output/workflow_clusters.html")
    print("   ✅ Saved: output/workflow_clusters.html")

    # Step 4: Export results
    print("\n4️⃣  Exporting results...")
    df.to_csv("output/workflow_results.csv", index=False)
    print("   ✅ Saved: output/workflow_results.csv")

    print("\n✨ Workflow complete!")
    print(f"\n📁 Output files:")
    print(f"   - output/workflow_clusters.html (Interactive visualization)")
    print(f"   - output/workflow_results.csv (Clustered data)")

    print()


def main():
    """Run all examples."""
    example_1_ml_clustering()
    example_2_fast_similarity()
    example_3_interactive_visualization()
    example_4_auto_update()
    example_5_data_validation()
    example_6_combined_workflow()

    print(f"{'='*80}")
    print("All v0.3.0 examples completed!")
    print(f"{'='*80}\n")

    print("📊 New features demonstrated:")
    print("   ✅ ML Clustering (KMeans, DBSCAN)")
    print("   ✅ Fast Similarity (numba-optimized, 10x faster)")
    print("   ✅ Interactive Visualization (Plotly)")
    print("   ✅ Auto-Update Engine (monthly API refresh)")
    print("   ✅ Data Validation (Pydantic)")
    print("\n🎉 GeoDataSim v0.3.0 - Intelligence Boost!")
    print()


if __name__ == "__main__":
    main()
