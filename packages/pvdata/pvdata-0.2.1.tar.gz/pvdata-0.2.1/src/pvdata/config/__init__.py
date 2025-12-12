"""
Configuration management for pvdata

This module provides configuration presets and utilities for optimizing
Parquet storage and data type management, as well as physical constraints
for time series data.
"""

from pvdata.config.parquet import ParquetConfig, ParquetConfigPreset
from pvdata.config.dtype_mapper import DTypeMapper
from pvdata.config.manager import ConfigManager, config
from pvdata.config.constraints import (
    SOLAR_RADIATION_CONSTRAINTS,
    METEOROLOGICAL_CONSTRAINTS,
    SOLAR_ANGLE_CONSTRAINTS,
    ALL_CONSTRAINTS,
    NON_NEGATIVE_COLS,
    get_constraints_for_columns,
    get_non_negative_constraints,
)

__all__ = [
    "ParquetConfig",
    "ParquetConfigPreset",
    "DTypeMapper",
    "ConfigManager",
    "config",
    "SOLAR_RADIATION_CONSTRAINTS",
    "METEOROLOGICAL_CONSTRAINTS",
    "SOLAR_ANGLE_CONSTRAINTS",
    "ALL_CONSTRAINTS",
    "NON_NEGATIVE_COLS",
    "get_constraints_for_columns",
    "get_non_negative_constraints",
]
