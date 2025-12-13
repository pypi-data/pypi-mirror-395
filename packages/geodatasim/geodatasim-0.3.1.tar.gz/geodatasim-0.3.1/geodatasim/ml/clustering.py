"""
Machine Learning clustering for cities.

Provides intelligent city grouping using sklearn algorithms:
- KMeans clustering
- DBSCAN (density-based clustering)
- Agglomerative clustering

New in v0.3.0.
"""

from typing import List, Dict, Optional, Tuple, Any
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score
import logging

from ..core.validator import ClusterResultModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CityClustering:
    """
    ML-powered city clustering engine.

    Groups cities into intelligent clusters based on multiple features:
    - Population
    - GDP per capita
    - Climate
    - Geographic location
    - Development indicators
    """

    DEFAULT_FEATURES = [
        'population',
        'gdp_per_capita',
        'hdi',
        'latitude',
        'longitude',
        'avg_temperature'
    ]

    def __init__(
        self,
        n_clusters: int = 5,
        method: str = 'kmeans',
        features: Optional[List[str]] = None,
        random_state: int = 42
    ):
        """
        Initialize clustering engine.

        Args:
            n_clusters: Number of clusters (for kmeans/agglomerative)
            method: Clustering method ('kmeans', 'dbscan', 'agglomerative')
            features: List of features to use for clustering
            random_state: Random seed for reproducibility
        """
        self.n_clusters = n_clusters
        self.method = method.lower()
        self.features = features or self.DEFAULT_FEATURES
        self.random_state = random_state

        self.scaler = StandardScaler()
        self.model = None
        self.labels_ = None
        self.cluster_centers_ = None
        self.silhouette_score_ = None

    def fit(self, cities_df: pd.DataFrame) -> 'CityClustering':
        """
        Fit clustering model on city data.

        Args:
            cities_df: DataFrame with city data

        Returns:
            Self (fitted clustering model)
        """
        # Extract features
        X = self._extract_features(cities_df)

        # Standardize features
        X_scaled = self.scaler.fit_transform(X)

        # Select and fit clustering algorithm
        if self.method == 'kmeans':
            self.model = KMeans(
                n_clusters=self.n_clusters,
                random_state=self.random_state,
                n_init=10
            )
        elif self.method == 'dbscan':
            self.model = DBSCAN(eps=0.5, min_samples=3)
        elif self.method == 'agglomerative':
            self.model = AgglomerativeClustering(n_clusters=self.n_clusters)
        else:
            raise ValueError(f"Unknown clustering method: {self.method}")

        # Fit model
        self.model.fit(X_scaled)
        self.labels_ = self.model.labels_

        # Get cluster centers (if available)
        if hasattr(self.model, 'cluster_centers_'):
            self.cluster_centers_ = self.model.cluster_centers_

        # Calculate silhouette score
        if len(set(self.labels_)) > 1:  # Need at least 2 clusters
            self.silhouette_score_ = silhouette_score(X_scaled, self.labels_)

        logger.info(f"Clustering complete: {len(set(self.labels_))} clusters formed")
        if self.silhouette_score_:
            logger.info(f"Silhouette score: {self.silhouette_score_:.3f}")

        return self

    def fit_transform(self, cities_df: pd.DataFrame) -> pd.DataFrame:
        """
        Fit clustering model and return DataFrame with cluster labels.

        Args:
            cities_df: DataFrame with city data

        Returns:
            DataFrame with 'cluster' column added
        """
        self.fit(cities_df)

        result_df = cities_df.copy()
        result_df['cluster'] = self.labels_

        return result_df

    def predict(self, cities_df: pd.DataFrame) -> np.ndarray:
        """
        Predict cluster labels for new cities.

        Args:
            cities_df: DataFrame with city data

        Returns:
            Array of cluster labels
        """
        if self.model is None:
            raise ValueError("Model not fitted. Call fit() first.")

        X = self._extract_features(cities_df)
        X_scaled = self.scaler.transform(X)

        if hasattr(self.model, 'predict'):
            return self.model.predict(X_scaled)
        else:
            # For DBSCAN, need to use fit_predict on all data
            raise NotImplementedError("DBSCAN doesn't support predict on new data")

    def get_cluster_summary(self, cities_df: pd.DataFrame) -> pd.DataFrame:
        """
        Get summary statistics for each cluster.

        Args:
            cities_df: DataFrame with city data

        Returns:
            DataFrame with cluster summaries
        """
        if self.labels_ is None:
            raise ValueError("Model not fitted. Call fit() first.")

        df = cities_df.copy()
        df['cluster'] = self.labels_

        summary = df.groupby('cluster').agg({
            'name': 'count',
            'population': ['mean', 'median'],
            'gdp_per_capita': ['mean', 'median'],
            'hdi': ['mean', 'median'],
        }).round(2)

        summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
        summary = summary.rename(columns={'name_count': 'city_count'})

        return summary

    def get_city_clusters(self, cities_df: pd.DataFrame) -> List[ClusterResultModel]:
        """
        Get cluster assignments for all cities.

        Args:
            cities_df: DataFrame with city data

        Returns:
            List of ClusterResultModel instances
        """
        if self.labels_ is None:
            raise ValueError("Model not fitted. Call fit() first.")

        results = []

        for idx, (_, city) in enumerate(cities_df.iterrows()):
            cluster_id = int(self.labels_[idx])

            # Calculate distance to cluster center (if available)
            distance = None
            if self.cluster_centers_ is not None:
                X = self._extract_features(cities_df.iloc[[idx]])
                X_scaled = self.scaler.transform(X)
                center = self.cluster_centers_[cluster_id]
                distance = float(np.linalg.norm(X_scaled[0] - center))

            result = ClusterResultModel(
                city_name=city['name'],
                cluster_id=cluster_id,
                cluster_center_distance=distance,
                silhouette_score=self.silhouette_score_
            )
            results.append(result)

        return results

    def find_optimal_clusters(
        self,
        cities_df: pd.DataFrame,
        max_clusters: int = 10
    ) -> Tuple[int, List[float]]:
        """
        Find optimal number of clusters using elbow method.

        Args:
            cities_df: DataFrame with city data
            max_clusters: Maximum number of clusters to test

        Returns:
            Tuple of (optimal_k, inertia_scores)
        """
        X = self._extract_features(cities_df)
        X_scaled = self.scaler.fit_transform(X)

        inertias = []

        for k in range(2, max_clusters + 1):
            kmeans = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
            kmeans.fit(X_scaled)
            inertias.append(kmeans.inertia_)

        # Simple elbow detection (find maximum decrease)
        decreases = np.diff(inertias)
        optimal_k = np.argmin(decreases) + 2  # +2 because we start from k=2

        logger.info(f"Optimal number of clusters: {optimal_k}")

        return optimal_k, inertias

    def _extract_features(self, cities_df: pd.DataFrame) -> np.ndarray:
        """
        Extract and clean features for clustering.

        Args:
            cities_df: DataFrame with city data

        Returns:
            NumPy array of features
        """
        # Get available features
        available_features = [f for f in self.features if f in cities_df.columns]

        if not available_features:
            raise ValueError(f"No valid features found. Available columns: {cities_df.columns.tolist()}")

        # Extract features
        X = cities_df[available_features].copy()

        # Handle missing values
        X = X.fillna(X.median())

        return X.values


# Convenience functions

def cluster_cities(
    cities_df: pd.DataFrame,
    n_clusters: int = 5,
    method: str = 'kmeans'
) -> pd.DataFrame:
    """
    Quick city clustering.

    Args:
        cities_df: DataFrame with city data
        n_clusters: Number of clusters
        method: Clustering method

    Returns:
        DataFrame with 'cluster' column added

    Example:
        >>> from geodatasim.ml import cluster_cities
        >>> clustered = cluster_cities(cities_df, n_clusters=5)
        >>> print(clustered[['name', 'cluster']])
    """
    clustering = CityClustering(n_clusters=n_clusters, method=method)
    clustering.fit(cities_df)

    result_df = cities_df.copy()
    result_df['cluster'] = clustering.labels_

    return result_df


def find_similar_cluster(
    target_city: str,
    cities_df: pd.DataFrame,
    n_clusters: int = 5
) -> List[str]:
    """
    Find cities in the same cluster as target city.

    Args:
        target_city: Name of target city
        cities_df: DataFrame with city data
        n_clusters: Number of clusters

    Returns:
        List of city names in same cluster

    Example:
        >>> from geodatasim.ml import find_similar_cluster
        >>> similar = find_similar_cluster("Istanbul", cities_df)
        >>> print(similar)
        ['Istanbul', 'Athens', 'Budapest', 'Prague']
    """
    clustering = CityClustering(n_clusters=n_clusters)
    clustering.fit(cities_df)

    result_df = cities_df.copy()
    result_df['cluster'] = clustering.labels_

    # Find target city's cluster
    target_cluster = result_df[result_df['name'] == target_city]['cluster'].iloc[0]

    # Get all cities in that cluster
    similar_cities = result_df[result_df['cluster'] == target_cluster]['name'].tolist()

    return similar_cities


__all__ = [
    'CityClustering',
    'cluster_cities',
    'find_similar_cluster',
]
