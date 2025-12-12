"""
Physical constraint definitions for time series data

This module provides predefined physical constraints for meteorological and solar data,
ensuring that interpolated or resampled values remain within realistic bounds.

Examples:
    >>> from pvdata.config.constraints import SOLAR_RADIATION_CONSTRAINTS
    >>> from pvdata.processing import TimeSeriesResampler
    >>>
    >>> resampler = TimeSeriesResampler()
    >>> df_resampled = resampler.resample(
    ...     df,
    ...     freq='10min',
    ...     method='interpolate',
    ...     constraints=SOLAR_RADIATION_CONSTRAINTS
    ... )
"""

from typing import Dict, List, Optional

# Solar radiation constraints (W/m²)
SOLAR_RADIATION_CONSTRAINTS = {
    "GHI": {"min": 0, "max": 1500},  # Global Horizontal Irradiance
    "DNI": {"min": 0, "max": 1200},  # Direct Normal Irradiance
    "DHI": {"min": 0, "max": 800},  # Diffuse Horizontal Irradiance
    "Clearsky GHI": {"min": 0, "max": 1500},
    "Clearsky DNI": {"min": 0, "max": 1200},
    "Clearsky DHI": {"min": 0, "max": 800},
    "Global Horizontal Irradiance": {"min": 0, "max": 1500},
    "Direct Normal Irradiance": {"min": 0, "max": 1200},
    "Diffuse Horizontal Irradiance": {"min": 0, "max": 800},
}

# Meteorological variable constraints
METEOROLOGICAL_CONSTRAINTS = {
    "Temperature": {"min": -80, "max": 60},  # °C
    "Dew Point": {"min": -80, "max": 50},  # °C
    "Relative Humidity": {"min": 0, "max": 100},  # %
    "Wind Speed": {"min": 0, "max": 100},  # m/s
    "Wind Direction": {"min": 0, "max": 360},  # degrees
    "Surface Pressure": {"min": 500, "max": 1100},  # mbar
    "Pressure": {"min": 500, "max": 1100},  # mbar
    "Surface Albedo": {"min": 0, "max": 1},  # dimensionless (0-1)
    "Albedo": {"min": 0, "max": 1},  # dimensionless (0-1)
    "Precipitable Water": {"min": 0, "max": 100},  # cm
    "Cloud Type": {"min": 0, "max": 12},  # categorical (0-12)
}

# Solar angle constraints
SOLAR_ANGLE_CONSTRAINTS = {
    "Solar Zenith Angle": {"min": 0, "max": 180},  # degrees
    "Solar Azimuth Angle": {"min": 0, "max": 360},  # degrees
    "Solar Altitude": {"min": -90, "max": 90},  # degrees
    "Solar Elevation": {"min": -90, "max": 90},  # degrees
    "solar_zenith": {"min": 0, "max": 180},  # degrees
    "solar_azimuth": {"min": 0, "max": 360},  # degrees
    "solar_altitude": {"min": -90, "max": 90},  # degrees
    "solar_elevation": {"min": -90, "max": 90},  # degrees
}

# Combined constraints dictionary
ALL_CONSTRAINTS = {
    **SOLAR_RADIATION_CONSTRAINTS,
    **METEOROLOGICAL_CONSTRAINTS,
    **SOLAR_ANGLE_CONSTRAINTS,
}

# Non-negative columns (common pattern)
NON_NEGATIVE_COLS = [
    "GHI",
    "DNI",
    "DHI",
    "Clearsky GHI",
    "Clearsky DNI",
    "Clearsky DHI",
    "Global Horizontal Irradiance",
    "Direct Normal Irradiance",
    "Diffuse Horizontal Irradiance",
    "Wind Speed",
    "Precipitable Water",
]


def get_constraints_for_columns(
    columns: List[str], constraint_set: Optional[str] = "all"
) -> Dict[str, Dict[str, float]]:
    """
    Automatically select constraints based on column names

    Args:
        columns: List of column names from DataFrame
        constraint_set: Which constraint set to use:
            - "all": All predefined constraints (default)
            - "solar": Only solar radiation constraints
            - "meteorological": Only meteorological constraints
            - "angles": Only solar angle constraints

    Returns:
        Dictionary of constraints applicable to the given columns

    Examples:
        >>> import pandas as pd
        >>> from pvdata.config.constraints import get_constraints_for_columns
        >>>
        >>> # Automatically select constraints for specific columns
        >>> df_columns = ['timestamp', 'GHI', 'DNI', 'Temperature', 'city']
        >>> constraints = get_constraints_for_columns(df_columns)
        >>> print(constraints)
        {'GHI': {'min': 0, 'max': 1500}, 'DNI': {'min': 0, 'max': 1200},
         'Temperature': {'min': -80, 'max': 60}}

        >>> # Use only solar radiation constraints
        >>> solar_constraints = get_constraints_for_columns(df_columns, constraint_set='solar')
        >>> print(solar_constraints)
        {'GHI': {'min': 0, 'max': 1500}, 'DNI': {'min': 0, 'max': 1200}}
    """
    # Select constraint dictionary based on set
    if constraint_set == "solar":
        constraint_dict = SOLAR_RADIATION_CONSTRAINTS
    elif constraint_set == "meteorological":
        constraint_dict = METEOROLOGICAL_CONSTRAINTS
    elif constraint_set == "angles":
        constraint_dict = SOLAR_ANGLE_CONSTRAINTS
    else:  # "all" or any other value
        constraint_dict = ALL_CONSTRAINTS

    # Filter constraints to only include columns present in the input
    selected_constraints = {}
    for col in columns:
        if col in constraint_dict:
            selected_constraints[col] = constraint_dict[col]

    return selected_constraints


def get_non_negative_constraints(columns: List[str]) -> Dict[str, Dict[str, float]]:
    """
    Get minimum=0 constraints for non-negative columns

    This is a convenience function for quickly applying non-negative constraints
    to common radiation and meteorological variables.

    Args:
        columns: List of column names from DataFrame

    Returns:
        Dictionary of {'column': {'min': 0}} for non-negative columns

    Examples:
        >>> from pvdata.config.constraints import get_non_negative_constraints
        >>>
        >>> df_columns = ['timestamp', 'GHI', 'DNI', 'Temperature', 'city']
        >>> constraints = get_non_negative_constraints(df_columns)
        >>> print(constraints)
        {'GHI': {'min': 0}, 'DNI': {'min': 0}}
    """
    constraints = {}
    for col in columns:
        if col in NON_NEGATIVE_COLS:
            constraints[col] = {"min": 0}

    return constraints
