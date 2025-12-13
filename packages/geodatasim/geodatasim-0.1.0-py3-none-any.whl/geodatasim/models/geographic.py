"""Geographic data models."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Coordinates:
    """Geographic coordinates."""

    latitude: float
    longitude: float

    def __post_init__(self):
        """Validate coordinates."""
        if not -90 <= self.latitude <= 90:
            raise ValueError(f"Invalid latitude: {self.latitude}")
        if not -180 <= self.longitude <= 180:
            raise ValueError(f"Invalid longitude: {self.longitude}")

    def to_tuple(self) -> tuple:
        """Return as (lat, lon) tuple."""
        return (self.latitude, self.longitude)

    def __str__(self) -> str:
        """String representation."""
        return f"({self.latitude:.4f}, {self.longitude:.4f})"


@dataclass
class Airport:
    """Airport information."""

    code: str  # IATA code (e.g., 'IST')
    icao: Optional[str] = None  # ICAO code (e.g., 'LTFM')
    name: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    elevation_ft: Optional[int] = None
    type: Optional[str] = None  # 'large_airport', 'medium_airport', etc.

    @property
    def coordinates(self) -> Optional[Coordinates]:
        """Get coordinates as Coordinates object."""
        if self.latitude is not None and self.longitude is not None:
            return Coordinates(self.latitude, self.longitude)
        return None

    def __str__(self) -> str:
        """String representation."""
        return f"{self.code} - {self.name}" if self.name else self.code
