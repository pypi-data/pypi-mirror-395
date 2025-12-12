"""
NSRDB API Client

Provides functions to fetch data from NREL's NSRDB API.
"""

import time
from io import StringIO
from typing import Dict, List, Optional

import pandas as pd
import requests

from ...utils.decorators import retry
from ...utils.logger import get_logger
from .datasets import get_dataset_attributes

logger = get_logger(__name__)

# NSRDB API configuration
NSRDB_BASE_URL = "https://developer.nrel.gov/api/nsrdb/v2/solar"

# Default contact information for API requests
DEFAULT_EMAIL = "research.user@university.edu"
DEFAULT_FULL_NAME = "Solar Data Researcher"
DEFAULT_AFFILIATION = "Research Institution"
DEFAULT_REASON = "Solar energy research and analysis"


class NSRDBClient:
    """
    Client for NSRDB API

    Handles API authentication, rate limiting, and data fetching.

    Examples:
        >>> client = NSRDBClient(api_key="your_api_key_here")
        >>> df = client.fetch_data(
        ...     lat=33.4484,
        ...     lon=-112.0740,
        ...     year=2020,
        ...     dataset="nsrdb-GOES-aggregated-v4-0-0-download"
        ... )
    """

    def __init__(
        self,
        api_key: str,
        email: str = DEFAULT_EMAIL,
        full_name: str = DEFAULT_FULL_NAME,
        affiliation: str = DEFAULT_AFFILIATION,
        reason: str = DEFAULT_REASON,
    ):
        """
        Initialize NSRDB client.

        Args:
            api_key: NREL API key (get from https://developer.nrel.gov/signup/)
            email: Email address for API requests
            full_name: Full name for API requests
            affiliation: Institution affiliation
            reason: Reason for data access
        """
        self.api_key = api_key
        self.email = email
        self.full_name = full_name
        self.affiliation = affiliation
        self.reason = reason

    @retry(max_attempts=3, delay=5.0, backoff=1.0, exceptions=(requests.RequestException, IOError))
    def fetch_data(
        self,
        lat: float,
        lon: float,
        year: int,
        dataset: str,
        interval: Optional[int] = None,
        attributes: Optional[List[str]] = None,
        use_utc: bool = True,
        leap_day: bool = True,
        timeout: int = 300,
    ) -> pd.DataFrame:
        """
        Fetch NSRDB data for a single location and year.

        Args:
            lat: Latitude (-90 to 90)
            lon: Longitude (-180 to 180)
            year: Year to fetch
            dataset: Dataset name (e.g., 'nsrdb-GOES-aggregated-v4-0-0-download')
            interval: Time interval in minutes (10, 15, 30, 60). If None, uses dataset default
            attributes: List of attributes to fetch. If None, uses all available for dataset
            use_utc: Use UTC time (recommended to avoid DST issues)
            leap_day: Include leap day in data
            timeout: Request timeout in seconds

        Returns:
            DataFrame with NSRDB data

        Raises:
            requests.RequestException: If API request fails after retries
            ValueError: If invalid parameters provided

        Examples:
            >>> client = NSRDBClient(api_key="your_key")
            >>> df = client.fetch_data(
            ...     lat=33.4484,
            ...     lon=-112.0740,
            ...     year=2020,
            ...     dataset="nsrdb-GOES-aggregated-v4-0-0-download",
            ...     interval=30
            ... )
        """
        # Validate inputs
        if not -90 <= lat <= 90:
            raise ValueError(f"Latitude must be between -90 and 90, got {lat}")
        if not -180 <= lon <= 180:
            raise ValueError(f"Longitude must be between -180 and 180, got {lon}")

        # Create WKT point
        wkt = f"POINT({lon:.4f} {lat:.4f})"

        # Build URL
        url = f"{NSRDB_BASE_URL}/{dataset}.csv"

        # Get attributes for this dataset if not provided
        if attributes is None:
            attributes = get_dataset_attributes(dataset)

        # Build request parameters
        # SUNY India dataset requires minimal parameters (doesn't support utc, interval, attributes)
        if dataset == "suny-india-download":
            params = {
                "api_key": self.api_key,
                "wkt": wkt,
                "names": str(year),
                "email": self.email,
            }
            logger.warning(
                f"SUNY India dataset: Using minimal parameter set (no UTC/attributes/interval)"
            )
        else:
            # Standard parameter set for other datasets
            params = {
                "api_key": self.api_key,
                "wkt": wkt,
                "names": str(year),
                "email": self.email,
                "full_name": self.full_name,
                "affiliation": self.affiliation,
                "reason": self.reason,
                "mailing_list": "false",
            }

            # Add optional parameters
            if interval is not None:
                params["interval"] = interval
            if attributes:
                params["attributes"] = ",".join(attributes)
            if use_utc:
                params["utc"] = "true"
            if leap_day:
                params["leap_day"] = "true"

        # Make API request
        logger.info(
            f"Fetching data: year={year}, dataset={dataset}, "
            f"lat={lat:.4f}, lon={lon:.4f}, interval={interval}"
        )

        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()

        # Parse CSV (skip first 2 rows which are metadata)
        df = pd.read_csv(StringIO(response.text), skiprows=2)

        logger.info(f"Fetched {len(df):,} records for year {year}")

        return df


def fetch_nsrdb_data(
    lat: float,
    lon: float,
    year: int,
    dataset: str,
    api_key: str,
    interval: Optional[int] = None,
    attributes: Optional[List[str]] = None,
    use_utc: bool = True,
    leap_day: bool = True,
    timeout: int = 300,
    **kwargs,
) -> pd.DataFrame:
    """
    Convenience function to fetch NSRDB data without creating a client.

    Args:
        lat: Latitude
        lon: Longitude
        year: Year to fetch
        dataset: Dataset name
        api_key: NREL API key
        interval: Time interval in minutes
        attributes: List of attributes to fetch
        use_utc: Use UTC time
        leap_day: Include leap day
        timeout: Request timeout
        **kwargs: Additional parameters passed to NSRDBClient

    Returns:
        DataFrame with NSRDB data

    Examples:
        >>> df = fetch_nsrdb_data(
        ...     lat=33.4484,
        ...     lon=-112.0740,
        ...     year=2020,
        ...     dataset="nsrdb-GOES-aggregated-v4-0-0-download",
        ...     api_key="your_key",
        ...     interval=30
        ... )
    """
    client = NSRDBClient(api_key=api_key, **kwargs)
    return client.fetch_data(
        lat=lat,
        lon=lon,
        year=year,
        dataset=dataset,
        interval=interval,
        attributes=attributes,
        use_utc=use_utc,
        leap_day=leap_day,
        timeout=timeout,
    )
