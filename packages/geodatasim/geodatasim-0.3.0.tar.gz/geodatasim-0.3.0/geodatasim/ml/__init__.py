"""
Machine Learning module for GeoDataSim.

Provides intelligent city analysis:
- Clustering (KMeans, DBSCAN, Agglomerative)
- Fast similarity calculations (numba-optimized)
- Feature engineering and preprocessing

New in v0.3.0.
"""

from .clustering import (
    CityClustering,
    cluster_cities,
    find_similar_cluster,
)

from .similarity import (
    FastSimilarityEngine,
    find_similar_fast,
    calculate_similarity_matrix,
    normalize_features,
    standardize_features,
)

__all__ = [
    # Clustering
    'CityClustering',
    'cluster_cities',
    'find_similar_cluster',
    # Similarity
    'FastSimilarityEngine',
    'find_similar_fast',
    'calculate_similarity_matrix',
    'normalize_features',
    'standardize_features',
]
