"""
NSRDB Dataset Configurations

Provides configuration for different NSRDB datasets and city metadata.
"""

from typing import Dict, List, TypedDict


class CityConfig(TypedDict):
    """Configuration for a city location"""

    country: str
    lat: float
    lon: float
    altitude: int
    timezone: str
    climate: str


class DatasetConfig(TypedDict):
    """Configuration for NSRDB dataset"""

    dataset: str
    interval: int
    years: List[int]
    use_suny_attributes: bool


# City metadata (complete configuration)
CITIES: Dict[str, CityConfig] = {
    "Phoenix": {
        "country": "USA",
        "lat": 33.4484,
        "lon": -112.0740,
        "altitude": 331,
        "timezone": "America/Phoenix",
        "climate": "BWh - Hot desert",
    },
    "Chicago": {
        "country": "USA",
        "lat": 41.8781,
        "lon": -87.6298,
        "altitude": 181,
        "timezone": "America/Chicago",
        "climate": "Dfa - Humid continental",
    },
    "Manaus": {
        "country": "Brazil",
        "lat": -3.1190,
        "lon": -60.0217,
        "altitude": 92,
        "timezone": "America/Manaus",
        "climate": "Af - Tropical rainforest",
    },
    "Lagos": {
        "country": "Nigeria",
        "lat": 6.5244,
        "lon": 3.3792,
        "altitude": 41,
        "timezone": "Africa/Lagos",
        "climate": "Aw - Tropical savanna",
    },
    "London": {
        "country": "UK",
        "lat": 51.5074,
        "lon": -0.1278,
        "altitude": 11,
        "timezone": "Europe/London",
        "climate": "Cfb - Oceanic",
    },
    "Dubai": {
        "country": "UAE",
        "lat": 25.2048,
        "lon": 55.2708,
        "altitude": 16,
        "timezone": "Asia/Dubai",
        "climate": "BWh - Hot desert",
    },
    "Fairbanks": {
        "country": "USA",
        "lat": 64.8378,
        "lon": -147.7164,
        "altitude": 136,
        "timezone": "America/Anchorage",
        "climate": "Dfc - Subarctic",
    },
    "Beijing": {
        "country": "China",
        "lat": 39.9042,
        "lon": 116.4074,
        "altitude": 43,
        "timezone": "Asia/Shanghai",
        "climate": "Dwa - Continental monsoon",
    },
    "Mumbai": {
        "country": "India",
        "lat": 19.0760,
        "lon": 72.8777,
        "altitude": 14,
        "timezone": "Asia/Kolkata",
        "climate": "Am - Tropical monsoon",
    },
    "Sydney": {
        "country": "Australia",
        "lat": -33.8688,
        "lon": 151.2093,
        "altitude": 58,
        "timezone": "Australia/Sydney",
        "climate": "Cfa - Humid subtropical",
    },
}

# Best dataset configuration for each city (from analyze_nsrdb_datasets.py)
CITY_DATASET_CONFIG: Dict[str, DatasetConfig] = {
    "Phoenix": {
        "dataset": "nsrdb-GOES-aggregated-v4-0-0-download",
        "interval": 30,
        "years": list(range(2012, 2023)),
        "use_suny_attributes": False,
    },
    "Chicago": {
        "dataset": "nsrdb-GOES-aggregated-v4-0-0-download",
        "interval": 30,
        "years": list(range(2012, 2023)),
        "use_suny_attributes": False,
    },
    "Manaus": {
        "dataset": "nsrdb-GOES-aggregated-v4-0-0-download",
        "interval": 30,
        "years": list(range(2012, 2023)),
        "use_suny_attributes": False,
    },
    "Lagos": {
        "dataset": "nsrdb-msg-v1-0-0-download",
        "interval": 15,
        "years": list(range(2012, 2023)),
        "use_suny_attributes": False,
    },
    "London": {
        "dataset": "nsrdb-msg-v1-0-0-download",
        "interval": 15,
        "years": list(range(2012, 2023)),
        "use_suny_attributes": False,
    },
    "Dubai": {
        "dataset": "nsrdb-msg-v1-0-0-download",
        "interval": 15,
        "years": list(range(2012, 2023)),
        "use_suny_attributes": False,
    },
    "Fairbanks": {
        "dataset": "nsrdb-polar-v4-0-0-download",
        "interval": 60,
        "years": list(range(2013, 2023)),  # Note: Missing 2012
        "use_suny_attributes": False,
    },
    "Beijing": {
        "dataset": "himawari-download",
        "interval": 10,
        "years": list(range(2016, 2021)),  # Note: Only 2016-2020
        "use_suny_attributes": False,
    },
    "Sydney": {
        "dataset": "himawari-download",
        "interval": 10,
        "years": list(range(2016, 2021)),  # Note: Only 2016-2020
        "use_suny_attributes": False,
    },
    "Mumbai": {
        "dataset": "suny-india-download",
        "interval": 60,
        "years": list(range(2012, 2015)),  # Note: Only 2012-2014
        "use_suny_attributes": True,  # SUNY India uses simplified attributes
    },
}

# Standard attributes (supported by most datasets)
ATTRIBUTES = [
    "ghi",
    "dni",
    "dhi",
    "air_temperature",
    "dew_point",
    "relative_humidity",
    "wind_speed",
    "wind_direction",
    "surface_pressure",
    "surface_albedo",
    "solar_zenith_angle",
    "clearsky_ghi",
    "clearsky_dni",
    "clearsky_dhi",
    "cloud_type",
]

# SUNY India dataset's simplified attributes (doesn't support clearsky and cloud_type)
SUNY_INDIA_ATTRIBUTES = [
    "ghi",
    "dni",
    "dhi",
    "air_temperature",
    "dew_point",
    "relative_humidity",
    "wind_speed",
    "wind_direction",
    "surface_pressure",
    "surface_albedo",
]

# Dataset geographic coverage
DATASET_COVERAGE = {
    "nsrdb-GOES-aggregated-v4-0-0-download": {
        "name": "GOES",
        "description": "Americas",
        "lat_range": (-90, 90),
        "lon_range": (-180, -20),
    },
    "nsrdb-msg-v1-0-0-download": {
        "name": "MSG",
        "description": "Europe, Africa, Middle East",
        "lat_range": (-90, 90),
        "lon_range": (-20, 60),
    },
    "himawari-download": {
        "name": "Himawari",
        "description": "Asia, Australia",
        "lat_range": (-90, 90),
        "lon_range": (60, 180),
    },
    "nsrdb-polar-v4-0-0-download": {
        "name": "Polar",
        "description": "Polar regions (>60° latitude)",
        "lat_range": (60, 90),  # Also includes (-90, -60)
        "lon_range": (-180, 180),
    },
    "suny-india-download": {
        "name": "SUNY India",
        "description": "India region",
        "lat_range": (5, 40),
        "lon_range": (65, 100),
    },
}


def auto_select_dataset(lat: float, lon: float) -> str:
    """
    Automatically select the best dataset based on latitude and longitude.

    Args:
        lat: Latitude
        lon: Longitude

    Returns:
        Dataset name string

    Examples:
        >>> auto_select_dataset(33.4484, -112.0740)  # Phoenix
        'nsrdb-GOES-aggregated-v4-0-0-download'

        >>> auto_select_dataset(19.0760, 72.8777)  # Mumbai
        'suny-india-download'
    """
    # Polar regions (latitude > 60 or < -60)
    if abs(lat) > 60:
        return "nsrdb-polar-v4-0-0-download"

    # India region
    if 5 <= lat <= 40 and 65 <= lon <= 100:
        return "suny-india-download"

    # Asia/Australia (Himawari)
    if 60 <= lon <= 180 or -180 <= lon < -160:
        return "himawari-download"

    # Europe/Africa/Middle East (MSG)
    if -20 <= lon < 60:
        return "nsrdb-msg-v1-0-0-download"

    # Americas (GOES)
    if -180 <= lon < -20:
        return "nsrdb-GOES-aggregated-v4-0-0-download"

    # Default to GOES
    return "nsrdb-GOES-aggregated-v4-0-0-download"


def get_dataset_attributes(dataset: str) -> List[str]:
    """
    Get the attribute list for a specific dataset.

    Args:
        dataset: Dataset name

    Returns:
        List of attribute names

    Examples:
        >>> get_dataset_attributes('suny-india-download')
        ['ghi', 'dni', 'dhi', ...]  # Simplified list without clearsky
    """
    if dataset == "suny-india-download":
        return SUNY_INDIA_ATTRIBUTES.copy()
    return ATTRIBUTES.copy()
