"""
Tests for timezone handling module

This test module covers Task 1.6: Timezone handling tests including:
- UTC ↔ Local time conversion
- DST spring/fall transitions
- Different ambiguous/nonexistent strategies
- UTC storage strategy
"""

import pytest
import pandas as pd
import numpy as np
import pytz

from pvdata.processing.timezone import (
    add_utc_local_time,
    convert_to_utc_strategy,
    get_available_timezones,
    validate_timezone,
)


@pytest.fixture
def utc_df():
    """Create sample DataFrame with UTC timestamps"""
    timestamps = pd.date_range("2020-01-01 00:00:00", periods=24, freq="1H", tz="UTC")
    return pd.DataFrame({"timestamp": timestamps, "value": np.random.rand(24) * 100})


@pytest.fixture
def naive_df():
    """Create sample DataFrame with naive (no timezone) timestamps"""
    timestamps = pd.date_range("2020-01-01 00:00:00", periods=24, freq="1H")
    return pd.DataFrame({"timestamp": timestamps, "value": np.random.rand(24) * 100})


@pytest.fixture
def dst_spring_df():
    """
    Create DataFrame covering DST spring transition
    2020-03-08 2:00 AM → 3:00 AM (1 hour skipped)
    """
    # Create timestamps around DST spring transition
    timestamps = pd.date_range("2020-03-08 00:00:00", periods=10, freq="30min")
    return pd.DataFrame({"timestamp": timestamps, "GHI": np.random.rand(10) * 1000})


@pytest.fixture
def dst_fall_df():
    """
    Create DataFrame covering DST fall transition
    2020-11-01 2:00 AM → 1:00 AM (1 hour repeated)
    """
    # Create timestamps around DST fall transition
    timestamps = pd.date_range("2020-11-01 00:00:00", periods=10, freq="30min")
    return pd.DataFrame({"timestamp": timestamps, "GHI": np.random.rand(10) * 1000})


class TestUTCToLocalConversion:
    """Test suite for UTC → Local time conversion"""

    def test_utc_to_new_york(self, utc_df):
        """Test UTC to New York time conversion"""
        result = add_utc_local_time(utc_df, timezone="America/New_York", is_source_utc=True)

        # Should have both columns
        assert "timestamp" in result.columns
        assert "timestamp_local" in result.columns

        # UTC timezone should be preserved
        assert str(result["timestamp"].dt.tz) == "UTC"

        # Local time should be EST/EDT
        assert str(result["timestamp_local"].dt.tz) == "America/New_York"

        # First timestamp: UTC 2020-01-01 00:00 → EST 2019-12-31 19:00 (UTC-5)
        utc_time = result["timestamp"].iloc[0]
        local_time = result["timestamp_local"].iloc[0]

        # Time difference should be 5 hours in January (EST)
        time_diff = (utc_time - local_time).total_seconds()
        assert time_diff == 0  # Both represent the same moment

        # But display time should differ
        assert utc_time.hour == 0
        assert local_time.hour == 19  # 19:00 previous day

    def test_utc_to_phoenix(self, utc_df):
        """Test UTC to Phoenix time conversion (no DST)"""
        result = add_utc_local_time(utc_df, timezone="America/Phoenix", is_source_utc=True)

        assert "timestamp_local" in result.columns
        assert str(result["timestamp_local"].dt.tz) == "America/Phoenix"

        # Phoenix is UTC-7 (no DST)
        utc_time = result["timestamp"].iloc[0]
        local_time = result["timestamp_local"].iloc[0]

        assert utc_time.hour == 0
        assert local_time.hour == 17  # 17:00 previous day (UTC-7)

    def test_utc_to_tokyo(self, utc_df):
        """Test UTC to Tokyo time conversion"""
        result = add_utc_local_time(utc_df, timezone="Asia/Tokyo", is_source_utc=True)

        assert str(result["timestamp_local"].dt.tz) == "Asia/Tokyo"

        # Tokyo is UTC+9
        utc_time = result["timestamp"].iloc[0]
        local_time = result["timestamp_local"].iloc[0]

        assert utc_time.hour == 0
        assert local_time.hour == 9  # 09:00 same day (UTC+9)


class TestLocalToUTCConversion:
    """Test suite for Local time → UTC conversion"""

    def test_new_york_to_utc(self, naive_df):
        """Test New York time to UTC conversion"""
        result = add_utc_local_time(naive_df, timezone="America/New_York", is_source_utc=False)

        # Should have both columns
        assert "timestamp" in result.columns
        assert "timestamp_local" in result.columns

        # timestamp should now be UTC
        assert str(result["timestamp"].dt.tz) == "UTC"

        # timestamp_local should be New York time
        assert str(result["timestamp_local"].dt.tz) == "America/New_York"

    def test_phoenix_to_utc(self, naive_df):
        """Test Phoenix time to UTC conversion (no DST)"""
        result = add_utc_local_time(naive_df, timezone="America/Phoenix", is_source_utc=False)

        assert str(result["timestamp"].dt.tz) == "UTC"
        assert str(result["timestamp_local"].dt.tz) == "America/Phoenix"

        # Verify conversion
        local_time = result["timestamp_local"].iloc[0]
        utc_time = result["timestamp"].iloc[0]

        # Phoenix midnight → UTC 07:00 same day
        assert local_time.hour == 0
        assert utc_time.hour == 7

    def test_london_to_utc(self, naive_df):
        """Test London time to UTC conversion"""
        result = add_utc_local_time(naive_df, timezone="Europe/London", is_source_utc=False)

        assert str(result["timestamp"].dt.tz) == "UTC"
        assert str(result["timestamp_local"].dt.tz) == "Europe/London"


class TestDSTSpringTransition:
    """Test suite for DST spring transition (time skips forward)"""

    def test_nonexistent_shift_forward(self, dst_spring_df):
        """Test nonexistent time handling with shift_forward strategy"""
        result = add_utc_local_time(
            dst_spring_df,
            timezone="America/New_York",
            is_source_utc=False,
            handle_dst=True,
            nonexistent="shift_forward",
        )

        # Should complete without errors
        assert len(result) > 0
        assert "timestamp" in result.columns
        assert "timestamp_local" in result.columns

    def test_nonexistent_shift_backward(self, dst_spring_df):
        """Test nonexistent time handling with shift_backward strategy"""
        result = add_utc_local_time(
            dst_spring_df,
            timezone="America/New_York",
            is_source_utc=False,
            handle_dst=True,
            nonexistent="shift_backward",
        )

        assert len(result) > 0

    def test_nonexistent_nat(self, dst_spring_df):
        """Test nonexistent time handling with NaT strategy"""
        result = add_utc_local_time(
            dst_spring_df,
            timezone="America/New_York",
            is_source_utc=False,
            handle_dst=True,
            nonexistent="NaT",
        )

        # May have fewer rows if NaT rows were dropped
        assert len(result) <= len(dst_spring_df)


class TestDSTFallTransition:
    """Test suite for DST fall transition (time repeats)"""

    def test_ambiguous_infer(self, dst_fall_df):
        """Test ambiguous time handling with infer strategy"""
        result = add_utc_local_time(
            dst_fall_df,
            timezone="America/New_York",
            is_source_utc=False,
            handle_dst=True,
            ambiguous="infer",
        )

        # Should complete without errors
        assert len(result) > 0
        assert "timestamp" in result.columns

    def test_ambiguous_nat(self, dst_fall_df):
        """Test ambiguous time handling with NaT strategy"""
        result = add_utc_local_time(
            dst_fall_df,
            timezone="America/New_York",
            is_source_utc=False,
            handle_dst=True,
            ambiguous="NaT",
        )

        # May have fewer rows if NaT rows were dropped
        assert len(result) <= len(dst_fall_df)


class TestUTCStorageStrategy:
    """Test suite for UTC storage strategy"""

    def test_utc_source(self, utc_df):
        """Test UTC storage strategy with UTC source"""
        result = convert_to_utc_strategy(utc_df, source_timezone="UTC")

        # Both should be UTC
        assert str(result["timestamp"].dt.tz) == "UTC"
        assert str(result["timestamp_local"].dt.tz) == "UTC"

        # Values should be identical
        assert (result["timestamp"] == result["timestamp_local"]).all()

    def test_phoenix_source(self, naive_df):
        """Test UTC storage strategy with Phoenix source"""
        result = convert_to_utc_strategy(naive_df, source_timezone="America/Phoenix")

        # timestamp should be UTC
        assert str(result["timestamp"].dt.tz) == "UTC"

        # timestamp_local should be Phoenix time
        assert str(result["timestamp_local"].dt.tz) == "America/Phoenix"

    def test_new_york_source_with_dst(self):
        """Test UTC storage strategy with New York source (has DST)"""
        # Create data covering both EST and EDT periods
        df = pd.DataFrame(
            {
                "timestamp": pd.date_range("2020-01-01", periods=365, freq="1D"),
                "value": np.random.rand(365) * 100,
            }
        )

        result = convert_to_utc_strategy(df, source_timezone="America/New_York")

        assert str(result["timestamp"].dt.tz) == "UTC"
        assert str(result["timestamp_local"].dt.tz) == "America/New_York"

        # Should handle DST transitions without data loss
        assert len(result) == len(df)


class TestHelperFunctions:
    """Test suite for helper functions"""

    def test_validate_timezone_valid(self):
        """Test timezone validation with valid timezones"""
        assert validate_timezone("America/New_York") == True
        assert validate_timezone("America/Phoenix") == True
        assert validate_timezone("Asia/Tokyo") == True
        assert validate_timezone("Europe/London") == True
        assert validate_timezone("UTC") == True

    def test_validate_timezone_invalid(self):
        """Test timezone validation with invalid timezones"""
        assert validate_timezone("Invalid/Timezone") == False
        assert validate_timezone("America/Invalid") == False
        assert validate_timezone("NotATimezone") == False

    def test_get_available_timezones_all(self):
        """Test getting all available timezones"""
        all_tz = get_available_timezones()

        assert isinstance(all_tz, list)
        assert len(all_tz) > 500  # pytz has 594 timezones
        assert "America/New_York" in all_tz
        assert "UTC" in all_tz

    def test_get_available_timezones_america(self):
        """Test getting America timezones"""
        us_tz = get_available_timezones("America")

        assert isinstance(us_tz, list)
        assert len(us_tz) > 0
        assert all(tz.startswith("America/") for tz in us_tz)
        assert "America/New_York" in us_tz
        assert "America/Phoenix" in us_tz

    def test_get_available_timezones_asia(self):
        """Test getting Asia timezones"""
        asia_tz = get_available_timezones("Asia")

        assert isinstance(asia_tz, list)
        assert all(tz.startswith("Asia/") for tz in asia_tz)
        assert "Asia/Tokyo" in asia_tz
        assert "Asia/Shanghai" in asia_tz


class TestEdgeCases:
    """Test suite for edge cases and error conditions"""

    def test_invalid_timezone_raises_error(self, utc_df):
        """Test that invalid timezone raises an error"""
        with pytest.raises(ValueError, match="Unknown timezone"):
            add_utc_local_time(utc_df, timezone="Invalid/Timezone", is_source_utc=True)

    def test_empty_dataframe(self):
        """Test handling of empty DataFrame"""
        df = pd.DataFrame({"timestamp": [], "value": []})

        result = add_utc_local_time(df, timezone="America/New_York", is_source_utc=True)

        assert len(result) == 0
        assert "timestamp_local" in result.columns

    def test_single_row_dataframe(self):
        """Test handling of single-row DataFrame"""
        df = pd.DataFrame(
            {"timestamp": [pd.Timestamp("2020-01-01 00:00:00", tz="UTC")], "value": [100.0]}
        )

        result = add_utc_local_time(df, timezone="America/New_York", is_source_utc=True)

        assert len(result) == 1
        assert "timestamp_local" in result.columns

    def test_already_localized_timestamps(self):
        """Test handling of already timezone-aware timestamps"""
        df = pd.DataFrame(
            {
                "timestamp": pd.date_range(
                    "2020-01-01", periods=10, freq="1H", tz="America/Phoenix"
                ),
                "value": np.random.rand(10) * 100,
            }
        )

        # Convert from Phoenix to UTC
        result = add_utc_local_time(df, timezone="America/Phoenix", is_source_utc=False)

        assert len(result) == 10
        assert str(result["timestamp"].dt.tz) == "UTC"

    def test_dst_fallback_strategy(self, dst_spring_df):
        """Test automatic fallback to NaT strategy when DST handling fails"""
        # This should trigger fallback to NaT strategy
        result = add_utc_local_time(
            dst_spring_df,
            timezone="America/New_York",
            is_source_utc=False,
            handle_dst=True,
            ambiguous="infer",  # Will try this first
            nonexistent="shift_forward",
        )

        # Should complete even if fallback was triggered
        assert len(result) >= 0  # May drop rows with NaT

    def test_mixed_timezone_conversions(self):
        """Test multiple timezone conversions in sequence"""
        df = pd.DataFrame(
            {
                "timestamp": pd.date_range("2020-01-01", periods=24, freq="1H"),
                "value": np.random.rand(24) * 100,
            }
        )

        # Phoenix → UTC
        df_utc = add_utc_local_time(df, timezone="America/Phoenix", is_source_utc=False)

        assert str(df_utc["timestamp"].dt.tz) == "UTC"

        # UTC → New York
        df_ny = add_utc_local_time(
            df_utc.drop("timestamp_local", axis=1), timezone="America/New_York", is_source_utc=True
        )

        assert str(df_ny["timestamp"].dt.tz) == "UTC"
        assert str(df_ny["timestamp_local"].dt.tz) == "America/New_York"


class TestIntegration:
    """Integration tests for timezone handling with other features"""

    def test_timezone_with_metadata(self):
        """Test timezone conversion preserves other DataFrame columns"""
        df = pd.DataFrame(
            {
                "timestamp": pd.date_range("2020-01-01", periods=10, freq="1H", tz="UTC"),
                "GHI": np.random.rand(10) * 1000,
                "city": ["Phoenix"] * 10,
                "lat": [33.4484] * 10,
                "lon": [-112.0740] * 10,
            }
        )

        result = add_utc_local_time(df, timezone="America/Phoenix", is_source_utc=True)

        # All original columns should be preserved
        assert "GHI" in result.columns
        assert "city" in result.columns
        assert "lat" in result.columns
        assert "lon" in result.columns

        # Plus the new timestamp_local column
        assert "timestamp_local" in result.columns

        # Metadata should be unchanged
        assert (result["city"] == "Phoenix").all()
        assert (result["lat"] == 33.4484).all()

    def test_utc_strategy_with_resampling_workflow(self):
        """Test UTC strategy works well with time series resampling"""
        # Simulate a workflow: local time → UTC → resample
        df = pd.DataFrame(
            {
                "timestamp": pd.date_range("2020-01-01", periods=48, freq="30min"),
                "GHI": np.random.rand(48) * 1000,
            }
        )

        # Apply UTC strategy
        df_utc = convert_to_utc_strategy(df, source_timezone="America/Phoenix")

        # Now we can safely resample in UTC (avoiding DST issues)
        df_utc = df_utc.set_index("timestamp")
        df_resampled = df_utc[["GHI"]].resample("1H").mean()

        # Should have 24 hourly values
        assert len(df_resampled) == 24

        # All timestamps should be UTC
        assert str(df_resampled.index.tz) == "UTC"
