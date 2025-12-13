"""World Bank API integration."""

import requests
from typing import Optional, Dict, Any, List
from ..core.config import get_config
from ..utils.cache import cache_response


class WorldBankAPI:
    """
    World Bank Open Data API integration.

    Free API with no authentication required.
    API Docs: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation
    """

    BASE_URL = "https://api.worldbank.org/v2"

    # Most useful indicators for cities/countries
    INDICATORS = {
        # Economic
        'gdp_per_capita': 'NY.GDP.PCAP.CD',  # GDP per capita (current US$)
        'gdp_growth': 'NY.GDP.MKTP.KD.ZG',   # GDP growth (annual %)
        'inflation': 'FP.CPI.TOTL.ZG',       # Inflation, consumer prices
        'unemployment': 'SL.UEM.TOTL.ZS',    # Unemployment, total (% of labor force)
        'poverty_ratio': 'SI.POV.DDAY',      # Poverty headcount ratio

        # Human Development
        'life_expectancy': 'SP.DYN.LE00.IN',  # Life expectancy at birth
        'literacy_rate': 'SE.ADT.LITR.ZS',    # Literacy rate, adult
        'school_enrollment': 'SE.PRM.NENR',   # School enrollment, primary

        # Demographics
        'population_total': 'SP.POP.TOTL',    # Population, total
        'population_growth': 'SP.POP.GROW',   # Population growth (annual %)
        'urban_population': 'SP.URB.TOTL.IN.ZS',  # Urban population (% of total)
        'population_density': 'EN.POP.DNST',  # Population density (people per sq. km)

        # Infrastructure
        'internet_users': 'IT.NET.USER.ZS',   # Internet users (% of population)
        'mobile_subscriptions': 'IT.CEL.SETS.P2',  # Mobile subscriptions per 100 people
        'electric_power': 'EG.USE.ELEC.KH.PC',  # Electric power consumption

        # Trade & Business
        'trade_percent_gdp': 'NE.TRD.GNFS.ZS',  # Trade (% of GDP)
        'fdi_inflows': 'BX.KLT.DINV.WD.GD.ZS',  # FDI, net inflows (% of GDP)

        # Environment
        'co2_emissions': 'EN.ATM.CO2E.PC',    # CO2 emissions (metric tons per capita)
        'forest_area': 'AG.LND.FRST.ZS',      # Forest area (% of land area)
    }

    def __init__(self):
        """Initialize World Bank API client."""
        self.config = get_config()
        self.session = requests.Session()
        self.timeout = self.config.get('timeout_seconds', 10)

    @cache_response(ttl_days=90)
    def get_country_data(self, country_code: str, indicator: str,
                         year: Optional[int] = None) -> Optional[float]:
        """
        Get country data for a specific indicator.

        Args:
            country_code: ISO 3166-1 alpha-2 or alpha-3 country code (e.g., 'US', 'USA')
            indicator: World Bank indicator code (use INDICATORS dict)
            year: Specific year (optional, gets most recent if not specified)

        Returns:
            Indicator value or None if not available

        Examples:
            >>> api = WorldBankAPI()
            >>> gdp = api.get_country_data('TR', 'NY.GDP.PCAP.CD')
            >>> print(f"Turkey GDP per capita: ${gdp:,.0f}")
        """
        try:
            # Build URL
            url = f"{self.BASE_URL}/country/{country_code}/indicator/{indicator}"

            # Parameters
            params = {
                'format': 'json',
                'per_page': 100 if not year else 1,
            }

            if year:
                params['date'] = year

            # Make request
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()

            # World Bank API returns [metadata, data] array
            if len(data) < 2 or not data[1]:
                return None

            # Get most recent value
            for entry in data[1]:
                if entry.get('value') is not None:
                    return float(entry['value'])

            return None

        except Exception as e:
            if self.config.get('show_warnings', True):
                print(f"Warning: World Bank API error for {country_code}/{indicator}: {e}")
            return None

    @cache_response(ttl_days=90)
    def get_country_indicators(self, country_code: str,
                                indicators: Optional[List[str]] = None,
                                year: Optional[int] = None) -> Dict[str, Any]:
        """
        Get multiple indicators for a country.

        Args:
            country_code: ISO country code
            indicators: List of indicator keys (from INDICATORS dict) or None for all
            year: Specific year or None for most recent

        Returns:
            Dictionary of indicator values

        Examples:
            >>> api = WorldBankAPI()
            >>> data = api.get_country_indicators('TR', ['gdp_per_capita', 'life_expectancy'])
            >>> print(data)
        """
        if indicators is None:
            indicators = list(self.INDICATORS.keys())

        results = {}

        for indicator_key in indicators:
            if indicator_key not in self.INDICATORS:
                if self.config.get('show_warnings', True):
                    print(f"Warning: Unknown indicator '{indicator_key}'")
                continue

            indicator_code = self.INDICATORS[indicator_key]
            value = self.get_country_data(country_code, indicator_code, year)
            results[indicator_key] = value

        return results

    @cache_response(ttl_days=180)
    def get_countries(self) -> List[Dict[str, Any]]:
        """
        Get list of all countries.

        Returns:
            List of country dictionaries with codes, names, regions

        Examples:
            >>> api = WorldBankAPI()
            >>> countries = api.get_countries()
            >>> turkey = [c for c in countries if c['code'] == 'TUR'][0]
        """
        try:
            url = f"{self.BASE_URL}/country"
            params = {
                'format': 'json',
                'per_page': 500,
            }

            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()

            if len(data) < 2 or not data[1]:
                return []

            countries = []
            for entry in data[1]:
                # Filter out aggregates (regions, income groups, etc.)
                if entry.get('capitalCity'):  # Only actual countries have capitals
                    countries.append({
                        'code': entry['id'],
                        'iso2code': entry['iso2Code'],
                        'name': entry['name'],
                        'region': entry.get('region', {}).get('value'),
                        'income_level': entry.get('incomeLevel', {}).get('value'),
                        'capital': entry.get('capitalCity'),
                        'longitude': entry.get('longitude'),
                        'latitude': entry.get('latitude'),
                    })

            return countries

        except Exception as e:
            if self.config.get('show_warnings', True):
                print(f"Warning: World Bank API error getting countries: {e}")
            return []

    def search_country(self, query: str) -> Optional[str]:
        """
        Search for country code by name.

        Args:
            query: Country name or partial name

        Returns:
            ISO3 country code or None if not found

        Examples:
            >>> api = WorldBankAPI()
            >>> code = api.search_country("Turkey")
            >>> print(code)  # 'TUR'
        """
        countries = self.get_countries()
        query_lower = query.lower()

        # Exact match first
        for country in countries:
            if country['name'].lower() == query_lower:
                return country['code']

        # Partial match
        for country in countries:
            if query_lower in country['name'].lower():
                return country['code']

        return None
