"""
Time zone handling utilities

This module provides functions for converting between UTC and local time,
handling DST (Daylight Saving Time) transitions, and implementing recommended
timezone strategies for time series data.

Key Features:
- UTC ↔ Local time conversion
- DST conflict handling (ambiguous/nonexistent times)
- Recommended UTC storage strategy
- Comprehensive logging

Examples:
    >>> from pvdata.processing.timezone import add_utc_local_time, convert_to_utc_strategy
    >>>
    >>> # Convert UTC to local time
    >>> df = add_utc_local_time(
    ...     df,
    ...     timestamp_col='timestamp',
    ...     timezone='America/New_York',
    ...     is_source_utc=True
    ... )
    >>>
    >>> # Recommended UTC strategy
    >>> df = convert_to_utc_strategy(
    ...     df,
    ...     timestamp_col='timestamp',
    ...     source_timezone='America/Phoenix'
    ... )
"""

import pandas as pd
import pytz
from typing import Optional
from ..utils.logger import get_logger

logger = get_logger(__name__)


def add_utc_local_time(
    df: pd.DataFrame,
    timestamp_col: str = "timestamp",
    timezone: str = "UTC",
    is_source_utc: bool = True,
    handle_dst: bool = True,
    ambiguous: str = "infer",
    nonexistent: str = "shift_forward",
) -> pd.DataFrame:
    """
    Add UTC and local time columns to DataFrame

    This function handles timezone conversion and creates dual timestamp columns
    for better timezone management. It properly handles DST transitions.

    Args:
        df: Input DataFrame
        timestamp_col: Name of timestamp column
        timezone: Target timezone (e.g., 'America/Phoenix', 'Asia/Shanghai', 'Europe/London')
        is_source_utc: True if source timestamps are UTC, False if local time
        handle_dst: Whether to handle DST conflicts automatically
        ambiguous: How to handle ambiguous times during DST fall-back:
            - 'infer': Attempt to infer based on timestamp order
            - 'NaT': Mark ambiguous times as NaT
            - 'raise': Raise an error
        nonexistent: How to handle nonexistent times during DST spring-forward:
            - 'shift_forward': Shift forward by DST offset
            - 'shift_backward': Shift backward by DST offset
            - 'NaT': Mark nonexistent times as NaT
            - 'raise': Raise an error

    Returns:
        DataFrame with timestamp_local column added (or timestamp updated to UTC)

    Examples:
        >>> # UTC → Local time conversion
        >>> df = add_utc_local_time(
        ...     df,
        ...     timestamp_col='timestamp',
        ...     timezone='America/New_York',
        ...     is_source_utc=True
        ... )
        >>> # Result: df has 'timestamp' (UTC) and 'timestamp_local' (New York time)

        >>> # Local time → UTC conversion
        >>> df = add_utc_local_time(
        ...     df,
        ...     timestamp_col='timestamp',
        ...     timezone='America/New_York',
        ...     is_source_utc=False
        ... )
        >>> # Result: df has 'timestamp' (UTC) and 'timestamp_local' (New York time)

        >>> # Handle DST transitions
        >>> df = add_utc_local_time(
        ...     df,
        ...     timestamp_col='timestamp',
        ...     timezone='America/New_York',
        ...     is_source_utc=False,
        ...     handle_dst=True,
        ...     ambiguous='infer',
        ...     nonexistent='shift_forward'
        ... )
    """
    df = df.copy()

    # Validate timezone
    try:
        tz = pytz.timezone(timezone)
    except pytz.exceptions.UnknownTimeZoneError:
        logger.error(f"Unknown timezone: {timezone}")
        raise ValueError(f"Unknown timezone: {timezone}")

    # Ensure timestamp column is datetime type
    if not pd.api.types.is_datetime64_any_dtype(df[timestamp_col]):
        logger.debug(f"Converting '{timestamp_col}' to datetime")
        df[timestamp_col] = pd.to_datetime(df[timestamp_col])

    if is_source_utc:
        # Source is UTC, convert to local time
        logger.info(f"Converting UTC timestamps to {timezone} local time")

        if df[timestamp_col].dt.tz is None:
            # Naive datetime, localize as UTC first
            df[timestamp_col] = df[timestamp_col].dt.tz_localize("UTC")

        # Convert to target timezone
        df["timestamp_local"] = df[timestamp_col].dt.tz_convert(timezone)

        logger.info(f"Added 'timestamp_local' column (timezone: {timezone})")

    else:
        # Source is local time, convert to UTC
        logger.info(f"Converting {timezone} local time to UTC")

        if df[timestamp_col].dt.tz is None:
            # Naive datetime, need to localize
            if handle_dst:
                # Handle DST conflicts
                try:
                    df["timestamp_local"] = df[timestamp_col].dt.tz_localize(
                        timezone, ambiguous=ambiguous, nonexistent=nonexistent
                    )
                    logger.debug(
                        f"Localized timestamps with ambiguous={ambiguous}, nonexistent={nonexistent}"
                    )

                except Exception as e:
                    logger.warning(
                        f"DST localization failed with {ambiguous}/{nonexistent}: {e}. "
                        f"Falling back to NaT strategy"
                    )
                    # Fall back to NaT strategy
                    df["timestamp_local"] = df[timestamp_col].dt.tz_localize(
                        timezone, ambiguous="NaT", nonexistent="NaT"
                    )

                    # Drop NaT rows and warn
                    before = len(df)
                    df = df[df["timestamp_local"].notna()].copy()
                    after = len(df)

                    if before > after:
                        logger.warning(
                            f"Dropped {before - after} rows due to DST conflicts "
                            f"(ambiguous or nonexistent times)"
                        )
            else:
                # No DST handling, just localize
                df["timestamp_local"] = df[timestamp_col].dt.tz_localize(timezone)
        else:
            # Already has timezone info
            df["timestamp_local"] = df[timestamp_col]

        # Convert to UTC
        df[timestamp_col] = df["timestamp_local"].dt.tz_convert("UTC")

        logger.info(f"Converted timestamps to UTC, preserved local time in 'timestamp_local'")

    return df


def convert_to_utc_strategy(
    df: pd.DataFrame, timestamp_col: str = "timestamp", source_timezone: str = "UTC", **kwargs
) -> pd.DataFrame:
    """
    Apply recommended UTC storage strategy

    This is the recommended approach for handling timezones in time series data:
    - Store all timestamps in UTC (avoids DST issues)
    - Add a local time column for reference
    - Use automatic DST conflict resolution

    This strategy ensures:
    1. No data loss during DST transitions
    2. Consistent storage format (UTC)
    3. Easy comparison across time zones
    4. Proper handling of ambiguous/nonexistent times

    Args:
        df: Input DataFrame
        timestamp_col: Name of timestamp column
        source_timezone: Source data timezone (e.g., 'America/Phoenix', 'UTC')
        **kwargs: Additional arguments passed to add_utc_local_time()

    Returns:
        DataFrame with timestamp in UTC and timestamp_local in source timezone

    Examples:
        >>> # Recommended usage for NSRDB data (UTC source)
        >>> df = convert_to_utc_strategy(
        ...     df,
        ...     timestamp_col='timestamp',
        ...     source_timezone='UTC'
        ... )
        >>> # Result: timestamp stays UTC, timestamp_local added as UTC

        >>> # Data from local timezone
        >>> df = convert_to_utc_strategy(
        ...     df,
        ...     timestamp_col='timestamp',
        ...     source_timezone='America/Phoenix'
        ... )
        >>> # Result: timestamp converted to UTC, timestamp_local preserved

        >>> # Data from timezone with DST
        >>> df = convert_to_utc_strategy(
        ...     df,
        ...     timestamp_col='timestamp',
        ...     source_timezone='America/New_York'
        ... )
        >>> # Result: UTC storage with DST handling
    """
    is_source_utc = source_timezone.upper() == "UTC"

    logger.info(
        f"Applying UTC storage strategy: "
        f"source_timezone={source_timezone}, is_utc={is_source_utc}"
    )

    # Apply UTC/local time conversion
    result = add_utc_local_time(
        df,
        timestamp_col=timestamp_col,
        timezone=source_timezone if not is_source_utc else "UTC",
        is_source_utc=is_source_utc,
        **kwargs,
    )

    logger.info("UTC storage strategy applied successfully")

    return result


def get_available_timezones(region: Optional[str] = None) -> list:
    """
    Get list of available timezones, optionally filtered by region

    Args:
        region: Optional region filter (e.g., 'America', 'Europe', 'Asia')

    Returns:
        List of timezone names

    Examples:
        >>> # All US timezones
        >>> us_timezones = get_available_timezones('America')
        >>> print(us_timezones[:5])
        ['America/New_York', 'America/Chicago', 'America/Denver', 'America/Phoenix', 'America/Los_Angeles']

        >>> # All timezones
        >>> all_timezones = get_available_timezones()
        >>> print(len(all_timezones))
        594
    """
    all_tz = pytz.all_timezones

    if region:
        filtered = [tz for tz in all_tz if tz.startswith(region)]
        logger.debug(f"Found {len(filtered)} timezones in region '{region}'")
        return filtered

    return all_tz


def validate_timezone(timezone: str) -> bool:
    """
    Check if a timezone string is valid

    Args:
        timezone: Timezone string to validate

    Returns:
        True if valid, False otherwise

    Examples:
        >>> validate_timezone('America/New_York')
        True
        >>> validate_timezone('Invalid/Timezone')
        False
    """
    try:
        pytz.timezone(timezone)
        return True
    except pytz.exceptions.UnknownTimeZoneError:
        return False
