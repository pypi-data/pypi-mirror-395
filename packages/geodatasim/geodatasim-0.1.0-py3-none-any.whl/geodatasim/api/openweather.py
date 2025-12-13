"""OpenWeather API integration (optional feature)."""

from typing import Optional, Dict, Any
from ..core.config import get_config


class OpenWeatherAPI:
    """
    OpenWeather API integration for real-time weather data.

    Requires free API key: https://openweathermap.org/api
    Free tier: 1,000 calls/day, 60 calls/minute

    Note: This is an optional feature. City class works without it.
    """

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenWeather API client.

        Args:
            api_key: OpenWeather API key (optional, can be set in config)
        """
        self.config = get_config()
        self.api_key = api_key or self.config.get_api_key('openweather')

        if not self.api_key:
            if self.config.get('show_warnings', True):
                print("Warning: OpenWeather API key not set. Weather features disabled.")
                print("Get a free API key at: https://openweathermap.org/api")

    def get_current_weather(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """
        Get current weather for coordinates.

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            Weather data dictionary or None

        Note: Requires API key to be set.
        """
        if not self.api_key:
            return None

        # Implementation would go here
        # For v0.1.0, this is a placeholder
        raise NotImplementedError("Weather API integration coming in v0.2.0")
