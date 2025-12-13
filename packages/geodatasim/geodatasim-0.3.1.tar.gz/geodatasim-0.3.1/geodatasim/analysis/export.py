"""Data export utilities."""

from typing import List, Optional, Union
import pandas as pd
import json
from pathlib import Path
from ..core.city import City


class DataExporter:
    """
    Export city data to various formats.

    Supports: CSV, Excel, JSON, Markdown

    Examples:
        >>> from geodatasim import City
        >>> from geodatasim.analysis import DataExporter
        >>>
        >>> cities = [City("Istanbul"), City("Paris"), City("Tokyo")]
        >>> exporter = DataExporter(cities)
        >>> exporter.to_csv("cities.csv")
        >>> exporter.to_excel("cities.xlsx")
    """

    def __init__(self, cities: Union[List[City], List[str]]):
        """
        Initialize exporter.

        Args:
            cities: List of City objects or city names
        """
        if isinstance(cities[0], str):
            self.cities = [City(name, auto_load=False) for name in cities]
        else:
            self.cities = cities

    def to_dataframe(self, fields: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Convert to pandas DataFrame.

        Args:
            fields: Optional list of fields to include

        Returns:
            pandas DataFrame
        """
        data = []

        for city in self.cities:
            city_dict = city.to_dict()

            # Flatten the dict
            flat_dict = {
                'name': city_dict['name'],
                'country': city_dict['country'],
                'country_code': city_dict['country_code'],
                'region': city_dict['region'],
                'population': city_dict['population'],
                'timezone': city_dict['timezone'],
            }

            # Add coordinates
            if city_dict.get('coordinates'):
                flat_dict['latitude'] = city_dict['coordinates']['latitude']
                flat_dict['longitude'] = city_dict['coordinates']['longitude']

            # Add economic data
            if city_dict.get('economic'):
                for key, value in city_dict['economic'].items():
                    flat_dict[key] = value

            # Add climate data
            if city_dict.get('climate'):
                for key, value in city_dict['climate'].items():
                    flat_dict[f'climate_{key}'] = value

            data.append(flat_dict)

        df = pd.DataFrame(data)

        if fields:
            available = [f for f in fields if f in df.columns]
            df = df[available]

        return df

    def to_csv(self, filepath: str, **kwargs):
        """
        Export to CSV file.

        Args:
            filepath: Output file path
            **kwargs: Additional arguments for pandas to_csv

        Examples:
            >>> exporter = DataExporter([City("Istanbul"), City("Paris")])
            >>> exporter.to_csv("cities.csv")
        """
        df = self.to_dataframe()
        df.to_csv(filepath, index=False, **kwargs)

    def to_excel(self, filepath: str, sheet_name: str = 'Cities', **kwargs):
        """
        Export to Excel file.

        Args:
            filepath: Output file path
            sheet_name: Name of Excel sheet
            **kwargs: Additional arguments for pandas to_excel

        Examples:
            >>> exporter = DataExporter([City("Istanbul"), City("Paris")])
            >>> exporter.to_excel("cities.xlsx")
        """
        df = self.to_dataframe()
        df.to_excel(filepath, sheet_name=sheet_name, index=False, **kwargs)

    def to_json(self, filepath: str, orient: str = 'records', **kwargs):
        """
        Export to JSON file.

        Args:
            filepath: Output file path
            orient: JSON orientation (records, index, columns, etc.)
            **kwargs: Additional arguments for pandas to_json

        Examples:
            >>> exporter = DataExporter([City("Istanbul"), City("Paris")])
            >>> exporter.to_json("cities.json")
        """
        df = self.to_dataframe()
        df.to_json(filepath, orient=orient, **kwargs)

    def to_markdown(self, filepath: str, **kwargs) -> str:
        """
        Export to Markdown table.

        Args:
            filepath: Output file path
            **kwargs: Additional arguments for pandas to_markdown

        Returns:
            Markdown string

        Examples:
            >>> exporter = DataExporter([City("Istanbul"), City("Paris")])
            >>> exporter.to_markdown("cities.md")
        """
        df = self.to_dataframe()
        markdown = df.to_markdown(index=False, **kwargs)

        if filepath:
            with open(filepath, 'w') as f:
                f.write(markdown)

        return markdown

    def to_html(self, filepath: str, **kwargs):
        """
        Export to HTML table.

        Args:
            filepath: Output file path
            **kwargs: Additional arguments for pandas to_html

        Examples:
            >>> exporter = DataExporter([City("Istanbul"), City("Paris")])
            >>> exporter.to_html("cities.html")
        """
        df = self.to_dataframe()
        html = df.to_html(index=False, **kwargs)

        with open(filepath, 'w') as f:
            f.write(html)


def export_to_dataframe(city_names: List[str],
                       fields: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Quick function to export cities to DataFrame.

    Args:
        city_names: List of city names
        fields: Optional fields to include

    Returns:
        pandas DataFrame

    Examples:
        >>> from geodatasim.analysis import export_to_dataframe
        >>> df = export_to_dataframe(["Istanbul", "Paris", "Tokyo"])
        >>> print(df.head())
    """
    exporter = DataExporter(city_names)
    return exporter.to_dataframe(fields)
