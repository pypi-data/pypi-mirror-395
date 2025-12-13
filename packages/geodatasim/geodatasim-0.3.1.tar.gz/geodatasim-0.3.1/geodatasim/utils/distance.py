"""Distance and geographic utilities."""

import math
from typing import List, Tuple


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two points on Earth.

    Uses the Haversine formula.

    Args:
        lat1: Latitude of first point
        lon1: Longitude of first point
        lat2: Latitude of second point
        lon2: Longitude of second point

    Returns:
        Distance in kilometers

    Examples:
        >>> # Distance from Istanbul to Ankara
        >>> dist = haversine_distance(41.0082, 28.9784, 39.9334, 32.8597)
        >>> print(f"{dist:.0f} km")  # ~350 km
    """
    # Earth's radius in kilometers
    R = 6371.0

    # Convert to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def find_nearby(origin_lat: float, origin_lon: float,
                points: List[Tuple[str, float, float]],
                max_distance_km: float = 100,
                limit: int = 10) -> List[Tuple[str, float]]:
    """
    Find nearby points within a certain distance.

    Args:
        origin_lat: Origin latitude
        origin_lon: Origin longitude
        points: List of (name, lat, lon) tuples
        max_distance_km: Maximum distance in kilometers
        limit: Maximum number of results

    Returns:
        List of (name, distance) tuples, sorted by distance

    Examples:
        >>> airports = [
        ...     ("IST", 41.2615, 28.7419),
        ...     ("SAW", 40.8989, 29.3092),
        ...     ("ESB", 40.1281, 32.9951),
        ... ]
        >>> nearby = find_nearby(41.0082, 28.9784, airports, max_distance_km=50)
        >>> print(nearby)  # [(IST, 34.2), (SAW, 25.1)]
    """
    results = []

    for name, lat, lon in points:
        distance = haversine_distance(origin_lat, origin_lon, lat, lon)

        if distance <= max_distance_km:
            results.append((name, distance))

    # Sort by distance
    results.sort(key=lambda x: x[1])

    return results[:limit]


def calculate_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the bearing (direction) from point 1 to point 2.

    Args:
        lat1: Latitude of first point
        lon1: Longitude of first point
        lat2: Latitude of second point
        lon2: Longitude of second point

    Returns:
        Bearing in degrees (0-360)

    Examples:
        >>> bearing = calculate_bearing(41.0082, 28.9784, 48.8566, 2.3522)
        >>> print(f"{bearing:.0f}°")  # Northwest direction
    """
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlon_rad = math.radians(lon2 - lon1)

    x = math.sin(dlon_rad) * math.cos(lat2_rad)
    y = math.cos(lat1_rad) * math.sin(lat2_rad) - \
        math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon_rad)

    bearing = math.atan2(x, y)
    bearing = math.degrees(bearing)

    # Normalize to 0-360
    bearing = (bearing + 360) % 360

    return bearing
