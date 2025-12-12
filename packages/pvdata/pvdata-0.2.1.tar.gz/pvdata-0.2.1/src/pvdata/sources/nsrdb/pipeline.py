"""
NSRDB Data Pipeline

Provides high-level functions to fetch and process NSRDB data.
"""

import os
from typing import Dict, List, Optional, Union

import pandas as pd

from ...config.constraints import SOLAR_RADIATION_CONSTRAINTS, METEOROLOGICAL_CONSTRAINTS
from ...processing import TimeSeriesResampler
from ...processing.timezone import add_utc_local_time
from ...solar import calculate_sun_position
from ...utils.logger import get_logger
from ... import geo
from .api import fetch_nsrdb_data
from .datasets import (
    CITIES,
    CITY_DATASET_CONFIG,
    CityConfig,
    DatasetConfig,
    auto_select_dataset,
)

logger = get_logger(__name__)


def fetch(
    city: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    year: int = 2020,
    dataset: str = "auto",
    api_key: Optional[str] = None,
    target_interval: str = "10min",
    apply_constraints: bool = True,
    calculate_solar: bool = True,
    output_file: Optional[str] = None,
    **kwargs,
) -> pd.DataFrame:
    """
    Fetch and process NSRDB data for a single location and year.

    This is the main entry point for NSRDB data acquisition. It handles:
    - API data fetching
    - Timezone conversion (UTC strategy)
    - Interpolation to target interval
    - Physical constraints application
    - Solar angle calculation
    - Metadata enrichment

    Args:
        city: City name (e.g., "Phoenix"). If provided, uses predefined coordinates
        lat: Latitude (-90 to 90). Required if city not provided
        lon: Longitude (-180 to 180). Required if city not provided
        year: Year to fetch (e.g., 2020)
        dataset: Dataset name or "auto" for automatic selection
        api_key: NREL API key. Required. Get from https://developer.nrel.gov/signup/
        target_interval: Target time interval for output ("10min", "30min", "1h")
        apply_constraints: Apply physical constraints during interpolation
        calculate_solar: Calculate solar angles (altitude, azimuth, etc.)
        output_file: Optional file path to save output as Parquet
        **kwargs: Additional parameters passed to API client

    Returns:
        Processed DataFrame with NSRDB data

    Raises:
        ValueError: If invalid parameters provided
        RuntimeError: If data fetch or processing fails

    Examples:
        >>> # Fetch Phoenix 2020 data using predefined city
        >>> df = fetch(
        ...     city="Phoenix",
        ...     year=2020,
        ...     api_key="your_api_key"
        ... )

        >>> # Fetch custom location
        >>> df = fetch(
        ...     lat=33.4484,
        ...     lon=-112.0740,
        ...     year=2020,
        ...     dataset="auto",
        ...     api_key="your_api_key",
        ...     target_interval="10min"
        ... )

        >>> # Fetch and save to file
        >>> df = fetch(
        ...     city="Beijing",
        ...     year=2019,
        ...     api_key="your_api_key",
        ...     output_file="beijing_2019.parquet"
        ... )
    """
    # Validate inputs
    if api_key is None:
        raise ValueError(
            "api_key is required. Get your free API key from "
            "https://developer.nrel.gov/signup/"
        )

    # Resolve location
    if city is not None:
        if city not in CITIES:
            raise ValueError(
                f"Unknown city: {city}. "
                f"Available cities: {', '.join(CITIES.keys())}"
            )
        city_config = CITIES[city]
        lat = city_config["lat"]
        lon = city_config["lon"]
        altitude = city_config["altitude"]
        timezone = city_config["timezone"]
        logger.info(f"Using predefined city: {city} ({lat:.4f}, {lon:.4f})")

        # Use predefined dataset configuration if available
        if city in CITY_DATASET_CONFIG and dataset == "auto":
            dataset_config = CITY_DATASET_CONFIG[city]
            dataset = dataset_config["dataset"]
            interval = dataset_config["interval"]
            use_suny = dataset_config.get("use_suny_attributes", False)
            logger.info(
                f"Using predefined dataset config: {dataset} ({interval}min)"
            )
    else:
        if lat is None or lon is None:
            raise ValueError("Either city or (lat, lon) must be provided")
        altitude = kwargs.pop("altitude", 0)
        timezone = kwargs.pop("timezone", "UTC")
        use_suny = False

        # Auto-select dataset if needed
        if dataset == "auto":
            dataset = auto_select_dataset(lat, lon)
            logger.info(f"Auto-selected dataset: {dataset}")

        # Guess interval based on dataset
        if dataset == "himawari-download":
            interval = 10
        elif dataset == "nsrdb-msg-v1-0-0-download":
            interval = 15
        elif dataset in ["nsrdb-GOES-aggregated-v4-0-0-download"]:
            interval = 30
        else:
            interval = 60

    # Fetch raw data from NSRDB API
    logger.info(
        f"Fetching data: year={year}, dataset={dataset}, "
        f"interval={interval}min, lat={lat:.4f}, lon={lon:.4f}"
    )

    df = fetch_nsrdb_data(
        lat=lat,
        lon=lon,
        year=year,
        dataset=dataset,
        api_key=api_key,
        interval=interval if not use_suny else None,
        **kwargs,
    )

    logger.info(f"Fetched {len(df):,} records")

    # Add metadata
    if city:
        df["city"] = city
        df["country"] = city_config["country"]
        df["climate"] = city_config["climate"]

    df["lat"] = lat
    df["lon"] = lon
    df["altitude_m"] = altitude
    df["timezone"] = timezone

    # Create timestamp
    df["timestamp"] = pd.to_datetime(
        df[["Year", "Month", "Day", "Hour", "Minute"]]
    )

    # Handle timezone (UTC strategy)
    if use_suny:
        # SUNY India returns local time (IST), need to localize
        logger.info(f"SUNY India dataset: localizing to {timezone}")
        try:
            df["timestamp"] = df["timestamp"].dt.tz_localize(
                timezone, ambiguous="infer", nonexistent="shift_forward"
            )
            df["timestamp_local"] = df["timestamp"]
        except Exception as e:
            logger.warning(f"Localization failed, using NaT fallback: {e}")
            df["timestamp"] = df["timestamp"].dt.tz_localize(
                timezone, ambiguous="NaT", nonexistent="shift_forward"
            )
            df["timestamp_local"] = df["timestamp"]
            df = df[df["timestamp"].notna()].copy()
            logger.warning(
                f"Dropped {len(df) - len(df[df['timestamp'].notna()])} "
                f"rows with NaT timestamps"
            )
    else:
        # Other datasets return UTC time
        df["timestamp"] = df["timestamp"].dt.tz_localize("UTC")
        df["timestamp_local"] = df["timestamp"].dt.tz_convert(timezone)

    # Interpolate to target interval if needed
    if target_interval and interval != _interval_to_minutes(target_interval):
        logger.info(
            f"Interpolating from {interval}min to {target_interval}"
        )

        resampler = TimeSeriesResampler(timestamp_column="timestamp")

        # Build constraints if requested
        constraints = None
        if apply_constraints:
            constraints = {
                **SOLAR_RADIATION_CONSTRAINTS,
                **METEOROLOGICAL_CONSTRAINTS,
            }

        df = resampler.resample(
            df,
            freq=target_interval,
            method="interpolate",
            constraints=constraints,
            track_interpolation=True,
            preserve_metadata=True,
        )

        logger.info(f"Interpolation complete: {len(df):,} records")

    # Calculate solar angles if requested
    if calculate_solar:
        logger.info("Calculating solar angles...")
        df = calculate_sun_position(
            df,
            time_col="timestamp",
            lat_col="lat",
            lon_col="lon",
            altitude_col="altitude_m",
            timezone=None,  # timestamp already has timezone
            inplace=True,
        )
        logger.info("Solar angle calculation complete")

    # Save to file if requested
    if output_file:
        # Import write_parquet lazily to avoid circular import
        from ...io import write_parquet

        write_parquet(df, output_file)
        logger.info(f"Saved to {output_file}")

    return df


def fetch_multi_grid(
    city: str,
    year: int,
    api_key: str,
    grid_pattern: str = "10_point",
    radius_km: float = 20,
    target_interval: str = "10min",
    apply_constraints: bool = True,
    calculate_solar: bool = True,
    output_dir: Optional[str] = None,
    **kwargs,
) -> List[pd.DataFrame]:
    """
    Fetch NSRDB data for multiple grid points around a city.

    Args:
        city: City name (must be in predefined cities)
        year: Year to fetch
        api_key: NREL API key
        grid_pattern: Grid pattern ("10_point", "5_point", "9_point")
        radius_km: Grid radius in kilometers
        target_interval: Target time interval
        apply_constraints: Apply physical constraints
        calculate_solar: Calculate solar angles
        output_dir: Optional directory to save outputs
        **kwargs: Additional parameters

    Returns:
        List of DataFrames, one per grid point

    Examples:
        >>> # Fetch 10-point grid around Phoenix
        >>> dfs = fetch_multi_grid(
        ...     city="Phoenix",
        ...     year=2020,
        ...     api_key="your_key",
        ...     grid_pattern="10_point",
        ...     radius_km=20
        ... )
        >>> len(dfs)
        10
    """
    if city not in CITIES:
        raise ValueError(
            f"Unknown city: {city}. Available: {', '.join(CITIES.keys())}"
        )

    city_config = CITIES[city]

    # Generate grid points
    logger.info(
        f"Generating {grid_pattern} grid around {city} "
        f"(radius={radius_km}km)"
    )
    grids = geo.generate_grid(
        center_lat=city_config["lat"],
        center_lon=city_config["lon"],
        pattern=grid_pattern,
        radius_km=radius_km,
    )

    logger.info(f"Processing {len(grids)} grid points")

    results = []
    for i, grid in enumerate(grids):
        logger.info(
            f"Grid {i+1}/{len(grids)}: {grid['description']} "
            f"({grid['lat']:.4f}, {grid['lon']:.4f})"
        )

        # Determine output file if directory provided
        out_file = None
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            out_file = os.path.join(
                output_dir,
                f"{city}_grid{grid['grid_id']}_{year}_{target_interval}.parquet",
            )

        df = fetch(
            lat=grid["lat"],
            lon=grid["lon"],
            year=year,
            api_key=api_key,
            target_interval=target_interval,
            apply_constraints=apply_constraints,
            calculate_solar=calculate_solar,
            output_file=out_file,
            **kwargs,
        )

        # Add grid metadata
        df["grid_id"] = grid["grid_id"]
        df["grid_desc"] = grid["description"]

        results.append(df)

    logger.info(f"Completed {len(results)} grid points")
    return results


def _interval_to_minutes(interval: str) -> int:
    """
    Convert interval string to minutes.

    Examples:
        >>> _interval_to_minutes("10min")
        10
        >>> _interval_to_minutes("1h")
        60
    """
    interval = interval.lower()
    if interval.endswith("min"):
        return int(interval[:-3])
    elif interval.endswith("h"):
        return int(interval[:-1]) * 60
    else:
        raise ValueError(f"Unknown interval format: {interval}")
