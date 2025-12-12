"""
NSRDB Data Source Module

Provides high-level API for fetching and processing NSRDB data.

Quick Start:
    >>> import pvdata as pv
    >>>
    >>> # Fetch single location
    >>> df = pv.sources.nsrdb.fetch(
    ...     city="Phoenix",
    ...     year=2020,
    ...     api_key="your_api_key"
    ... )
    >>>
    >>> # Fetch multiple grid points
    >>> dfs = pv.sources.nsrdb.fetch_multi_grid(
    ...     city="Phoenix",
    ...     year=2020,
    ...     grid_pattern="10_point",
    ...     api_key="your_api_key"
    ... )

Available Cities:
    Phoenix, Chicago, Manaus, Lagos, London, Dubai,
    Fairbanks, Beijing, Mumbai, Sydney
"""

from .api import NSRDBClient, fetch_nsrdb_data
from .datasets import (
    ATTRIBUTES,
    CITIES,
    CITY_DATASET_CONFIG,
    DATASET_COVERAGE,
    SUNY_INDIA_ATTRIBUTES,
    auto_select_dataset,
    get_dataset_attributes,
)
from .pipeline import fetch, fetch_multi_grid

__all__ = [
    # High-level API
    "fetch",
    "fetch_multi_grid",
    # Low-level API
    "NSRDBClient",
    "fetch_nsrdb_data",
    # Configuration
    "CITIES",
    "CITY_DATASET_CONFIG",
    "DATASET_COVERAGE",
    "ATTRIBUTES",
    "SUNY_INDIA_ATTRIBUTES",
    # Utilities
    "auto_select_dataset",
    "get_dataset_attributes",
]
