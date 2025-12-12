"""
Solar position calculation module using pvlib.

This module provides functions to calculate solar position angles
(azimuth and altitude/elevation) for photovoltaic data analysis.
"""

from typing import Union, Optional
import pandas as pd
import numpy as np

try:
    import pvlib

    PVLIB_AVAILABLE = True
except ImportError:
    PVLIB_AVAILABLE = False

from pvdata.utils.logger import get_logger
from pvdata.utils.decorators import log_execution, validate_args
from pvdata.utils.exceptions import PVDataError

logger = get_logger(__name__)


def calculate_sun_position(
    df: pd.DataFrame,
    time_col: str = "timestamp",
    lat_col: Union[str, float] = "lat",
    lon_col: Union[str, float] = "lon",
    altitude_col: Union[str, float, None] = None,
    timezone: str = "UTC",
    method: str = "nrel_numpy",
    inplace: bool = False,
) -> pd.DataFrame:
    """
    Calculate solar position angles (azimuth and altitude/elevation).

    This function uses pvlib's solar position algorithms to compute
    accurate solar angles for each timestamp and location in the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing time and location data
    time_col : str, default 'timestamp'
        Name of the timestamp column
    lat_col : str or float, default 'lat'
        Column name containing latitude values, or a fixed latitude value
    lon_col : str or float, default 'lon'
        Column name containing longitude values, or a fixed longitude value
    altitude_col : str, float, or None, default None
        Column name containing altitude/elevation above sea level in meters,
        or a fixed altitude value. If None, assumes sea level (0m).
    timezone : str, default 'UTC'
        Timezone of the timestamp data
    method : str, default 'nrel_numpy'
        Solar position calculation method. Options:
        - 'nrel_numpy': Fast vectorized NREL SPA (recommended)
        - 'nrel_numba': NREL SPA with numba acceleration
        - 'pyephem': PyEphem algorithm
        - 'ephemeris': Default ephemeris
    inplace : bool, default False
        If True, modify the DataFrame in place. If False, return a copy.

    Returns
    -------
    pd.DataFrame
        DataFrame with added solar position columns:
        - solar_azimuth: Solar azimuth angle (0-360°, North=0°, clockwise)
        - solar_altitude: Solar altitude/elevation angle (-90 to 90°, horizon=0°)
        - solar_elevation: Alias for solar_altitude
        - solar_zenith: Solar zenith angle (0-180°, zenith=0°)
        - is_daylight: Boolean indicating if sun is above horizon

    Raises
    ------
    PVDataError
        If pvlib is not installed or input validation fails

    Examples
    --------
    >>> import pvdata as pv
    >>> df = pv.read_parquet('weather.parquet')
    >>> df = pv.solar.calculate_sun_position(df,
    ...     time_col='timestamp',
    ...     lat_col='lat',
    ...     lon_col='lon',
    ...     altitude_col=100.0)  # 100m above sea level
    >>> print(df[['timestamp', 'solar_azimuth', 'solar_altitude']])

    With fixed location:
    >>> df = pv.solar.calculate_sun_position(df,
    ...     lat_col=22.5431,  # Shenzhen latitude
    ...     lon_col=114.0576,  # Shenzhen longitude
    ...     altitude_col=0.0)

    Notes
    -----
    - Requires pvlib-python to be installed: pip install pvlib
    - The calculation is vectorized and very fast even for large datasets
    - Altitude parameter affects the calculation due to atmospheric refraction
    - Solar azimuth: 0°=North, 90°=East, 180°=South, 270°=West
    - Solar altitude: Positive above horizon, negative below horizon
    """
    if not PVLIB_AVAILABLE:
        raise PVDataError(
            "pvlib is required for solar position calculation. "
            "Install it with: pip install pvlib"
        )

    # Create a copy if not inplace
    if not inplace:
        df = df.copy()

    logger.debug(f"Calculating solar position for {len(df)} records")

    # Validate and prepare time column
    if time_col not in df.columns:
        raise PVDataError(f"Time column '{time_col}' not found in DataFrame")

    times = df[time_col]
    if not pd.api.types.is_datetime64_any_dtype(times):
        logger.debug(f"Converting '{time_col}' to datetime")
        times = pd.to_datetime(times)

    # Handle timezone
    if times.dt.tz is None:
        logger.debug(f"Localizing times to timezone: {timezone}")
        times = times.dt.tz_localize(timezone)

    # Get latitude values
    if isinstance(lat_col, (int, float)):
        lats = lat_col
        logger.debug(f"Using fixed latitude: {lats}")
    else:
        if lat_col not in df.columns:
            raise PVDataError(f"Latitude column '{lat_col}' not found in DataFrame")
        lats = df[lat_col]

    # Get longitude values
    if isinstance(lon_col, (int, float)):
        lons = lon_col
        logger.debug(f"Using fixed longitude: {lons}")
    else:
        if lon_col not in df.columns:
            raise PVDataError(f"Longitude column '{lon_col}' not found in DataFrame")
        lons = df[lon_col]

    # Get altitude/elevation values
    if altitude_col is None:
        altitudes = 0.0
        logger.debug("Using sea level altitude (0m)")
    elif isinstance(altitude_col, (int, float)):
        altitudes = altitude_col
        logger.debug(f"Using fixed altitude: {altitudes}m")
    else:
        if altitude_col not in df.columns:
            raise PVDataError(f"Altitude column '{altitude_col}' not found in DataFrame")
        altitudes = df[altitude_col]

    # Calculate solar position using pvlib
    logger.debug(f"Using pvlib method: {method}")
    solar_position = pvlib.solarposition.get_solarposition(
        time=times, latitude=lats, longitude=lons, altitude=altitudes, method=method
    )

    # Add results to DataFrame
    df["solar_azimuth"] = solar_position["azimuth"].values
    df["solar_altitude"] = solar_position["apparent_elevation"].values
    df["solar_elevation"] = solar_position["apparent_elevation"].values  # Alias
    df["solar_zenith"] = solar_position["apparent_zenith"].values
    df["is_daylight"] = df["solar_altitude"] > 0

    logger.debug(
        f"Solar position calculated: "
        f"azimuth range [{df['solar_azimuth'].min():.1f}, {df['solar_azimuth'].max():.1f}], "
        f"altitude range [{df['solar_altitude'].min():.1f}, {df['solar_altitude'].max():.1f}]"
    )

    return df


@log_execution(level="info")
def add_solar_angles(
    df: pd.DataFrame,
    lat: float,
    lon: float,
    altitude: float = 0.0,
    time_col: str = "timestamp",
    timezone: str = "UTC",
    method: str = "nrel_numpy",
    inplace: bool = False,
) -> pd.DataFrame:
    """
    Add solar angles to a time series DataFrame at a fixed location.

    This is a convenience function for the common case of calculating
    solar position for a single location (e.g., a single weather station
    or PV installation).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with time series data
    lat : float
        Latitude in decimal degrees (-90 to 90)
    lon : float
        Longitude in decimal degrees (-180 to 180)
    altitude : float, default 0.0
        Altitude/elevation above sea level in meters
    time_col : str, default 'timestamp'
        Name of the timestamp column
    timezone : str, default 'UTC'
        Timezone of the timestamp data
    method : str, default 'nrel_numpy'
        Solar position calculation method
    inplace : bool, default False
        If True, modify the DataFrame in place

    Returns
    -------
    pd.DataFrame
        DataFrame with solar position columns added

    Examples
    --------
    >>> import pvdata as pv
    >>> df = pv.read_parquet('station_data.parquet')
    >>> df = pv.solar.add_solar_angles(df,
    ...     lat=22.5431,  # Shenzhen
    ...     lon=114.0576,
    ...     altitude=100.0)  # 100m elevation
    >>> print(df[['timestamp', 'solar_azimuth', 'solar_altitude']])
    """
    return calculate_sun_position(
        df=df,
        time_col=time_col,
        lat_col=lat,
        lon_col=lon,
        altitude_col=altitude,
        timezone=timezone,
        method=method,
        inplace=inplace,
    )


def zenith_to_altitude(
    zenith: Union[float, pd.Series, np.ndarray],
) -> Union[float, pd.Series, np.ndarray]:
    """
    Convert solar zenith angle to altitude/elevation angle.

    The zenith angle is measured from directly overhead (zenith),
    while altitude is measured from the horizon.

    Relationship: altitude = 90° - zenith

    Parameters
    ----------
    zenith : float, pd.Series, or np.ndarray
        Solar zenith angle(s) in degrees (0-180°)
        - 0° = sun directly overhead (zenith)
        - 90° = sun at horizon
        - 180° = sun directly below (nadir)

    Returns
    -------
    float, pd.Series, or np.ndarray
        Solar altitude/elevation angle(s) in degrees (-90 to 90°)
        - 90° = sun directly overhead
        - 0° = sun at horizon
        - -90° = sun directly below

    Examples
    --------
    >>> import pvdata as pv
    >>> df = pv.read_parquet('weather.parquet')
    >>> df['solar_altitude'] = pv.solar.zenith_to_altitude(df['Solar Zenith'])

    Single value:
    >>> altitude = pv.solar.zenith_to_altitude(45.0)
    >>> print(altitude)  # 45.0

    Notes
    -----
    This is useful for converting NSRDB's "Solar Zenith" to the more
    commonly used altitude/elevation angle.
    """
    return 90 - zenith


def altitude_to_zenith(
    altitude: Union[float, pd.Series, np.ndarray],
) -> Union[float, pd.Series, np.ndarray]:
    """
    Convert solar altitude/elevation angle to zenith angle.

    Inverse of zenith_to_altitude.

    Relationship: zenith = 90° - altitude

    Parameters
    ----------
    altitude : float, pd.Series, or np.ndarray
        Solar altitude/elevation angle(s) in degrees (-90 to 90°)

    Returns
    -------
    float, pd.Series, or np.ndarray
        Solar zenith angle(s) in degrees (0-180°)

    Examples
    --------
    >>> import pvdata as pv
    >>> zenith = pv.solar.altitude_to_zenith(45.0)
    >>> print(zenith)  # 45.0
    """
    return 90 - altitude
