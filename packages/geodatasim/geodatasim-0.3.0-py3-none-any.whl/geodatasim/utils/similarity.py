"""City similarity calculation."""

import math
from typing import List, Dict, Any, Optional


class CitySimilarity:
    """
    Calculate similarity between cities based on multiple dimensions.

    Uses weighted scoring across:
    - Population size
    - Economic development
    - Climate
    - Geographic proximity
    - Development indicators
    """

    DEFAULT_WEIGHTS = {
        'population': 0.2,
        'gdp_per_capita': 0.3,
        'climate': 0.2,
        'geographic': 0.15,
        'development': 0.15,
    }

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        """
        Initialize similarity calculator.

        Args:
            weights: Custom weights for each dimension (must sum to 1.0)
        """
        self.weights = weights or self.DEFAULT_WEIGHTS

        # Validate weights sum to 1.0
        total = sum(self.weights.values())
        if not math.isclose(total, 1.0, rel_tol=0.01):
            raise ValueError(f"Weights must sum to 1.0, got {total}")

    def calculate_similarity(self, city1: Dict[str, Any], city2: Dict[str, Any]) -> float:
        """
        Calculate similarity score between two cities.

        Args:
            city1: First city data dictionary
            city2: Second city data dictionary

        Returns:
            Similarity score (0.0 to 1.0)
        """
        scores = []

        # Population similarity
        if city1.get('population') and city2.get('population'):
            pop_score = self._population_similarity(
                city1['population'],
                city2['population']
            )
            scores.append(('population', pop_score))

        # Economic similarity
        if city1.get('gdp_per_capita') and city2.get('gdp_per_capita'):
            gdp_score = self._economic_similarity(
                city1['gdp_per_capita'],
                city2['gdp_per_capita']
            )
            scores.append(('gdp_per_capita', gdp_score))

        # Climate similarity
        if city1.get('climate_zone') and city2.get('climate_zone'):
            climate_score = self._climate_similarity(
                city1['climate_zone'],
                city2['climate_zone']
            )
            scores.append(('climate', climate_score))

        # Geographic proximity
        if (city1.get('latitude') and city1.get('longitude') and
            city2.get('latitude') and city2.get('longitude')):
            geo_score = self._geographic_similarity(
                city1['latitude'], city1['longitude'],
                city2['latitude'], city2['longitude']
            )
            scores.append(('geographic', geo_score))

        # Development indicators
        if city1.get('hdi') and city2.get('hdi'):
            dev_score = self._development_similarity(
                city1['hdi'],
                city2['hdi']
            )
            scores.append(('development', dev_score))

        # Calculate weighted average
        if not scores:
            return 0.0

        weighted_sum = sum(score * self.weights.get(dimension, 0)
                          for dimension, score in scores)

        # Normalize by sum of weights for available dimensions
        total_weight = sum(self.weights.get(dimension, 0)
                          for dimension, _ in scores)

        return weighted_sum / total_weight if total_weight > 0 else 0.0

    def _population_similarity(self, pop1: int, pop2: int) -> float:
        """
        Calculate population similarity (0-1).

        Uses logarithmic scale to handle wide population ranges.
        """
        if pop1 <= 0 or pop2 <= 0:
            return 0.0

        log_pop1 = math.log10(pop1)
        log_pop2 = math.log10(pop2)

        # Maximum difference of 3 orders of magnitude (1000x difference = 0 similarity)
        max_diff = 3.0
        diff = abs(log_pop1 - log_pop2)

        return max(0.0, 1.0 - (diff / max_diff))

    def _economic_similarity(self, gdp1: float, gdp2: float) -> float:
        """Calculate economic similarity based on GDP per capita."""
        if gdp1 <= 0 or gdp2 <= 0:
            return 0.0

        # Use logarithmic scale
        log_gdp1 = math.log10(max(1, gdp1))
        log_gdp2 = math.log10(max(1, gdp2))

        # Maximum difference of 2.5 orders of magnitude
        max_diff = 2.5
        diff = abs(log_gdp1 - log_gdp2)

        return max(0.0, 1.0 - (diff / max_diff))

    def _climate_similarity(self, climate1: str, climate2: str) -> float:
        """Calculate climate similarity based on Köppen classification."""
        if climate1 == climate2:
            return 1.0

        # Extract first letter (main climate type)
        main1 = climate1[0] if climate1 else ''
        main2 = climate2[0] if climate2 else ''

        if main1 == main2:
            # Same main climate type
            return 0.7
        else:
            # Different climate types
            return 0.2

    def _geographic_similarity(self, lat1: float, lon1: float,
                               lat2: float, lon2: float) -> float:
        """Calculate geographic proximity similarity."""
        from .distance import haversine_distance

        distance_km = haversine_distance(lat1, lon1, lat2, lon2)

        # Maximum meaningful distance: 5000 km
        max_distance = 5000

        return max(0.0, 1.0 - (distance_km / max_distance))

    def _development_similarity(self, hdi1: float, hdi2: float) -> float:
        """Calculate development similarity based on HDI."""
        if hdi1 <= 0 or hdi2 <= 0:
            return 0.0

        # HDI is already 0-1 scale
        diff = abs(hdi1 - hdi2)

        # Maximum difference of 0.3 for meaningful similarity
        max_diff = 0.3

        return max(0.0, 1.0 - (diff / max_diff))


def calculate_similarity(city1: Dict[str, Any], city2: Dict[str, Any],
                        weights: Optional[Dict[str, float]] = None) -> float:
    """
    Convenience function to calculate city similarity.

    Args:
        city1: First city data dictionary
        city2: Second city data dictionary
        weights: Optional custom weights

    Returns:
        Similarity score (0.0 to 1.0)

    Examples:
        >>> istanbul = {'population': 15000000, 'gdp_per_capita': 28000}
        >>> barcelona = {'population': 5600000, 'gdp_per_capita': 36000}
        >>> similarity = calculate_similarity(istanbul, barcelona)
        >>> print(f"Similarity: {similarity:.1%}")
    """
    calculator = CitySimilarity(weights)
    return calculator.calculate_similarity(city1, city2)
