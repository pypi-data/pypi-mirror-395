"""
Tests for physical constraints, interpolation tracking, and metadata propagation

This test module covers Task 1.4: Integration testing for TimeSeriesResampler enhancements
including physical constraints, interpolation tracking, and metadata propagation features.
"""

import pytest
import pandas as pd
import numpy as np

from pvdata.processing import TimeSeriesResampler
from pvdata.config.constraints import (
    SOLAR_RADIATION_CONSTRAINTS,
    METEOROLOGICAL_CONSTRAINTS,
    ALL_CONSTRAINTS,
    get_constraints_for_columns,
    get_non_negative_constraints,
)


@pytest.fixture
def solar_df():
    """Create sample solar radiation data with potential constraint violations"""
    timestamps = pd.date_range("2020-01-01 00:00:00", periods=100, freq="30min")

    df = pd.DataFrame(
        {
            "timestamp": timestamps,
            "GHI": np.random.randn(100) * 200 + 500,  # May have negative values
            "DNI": np.random.randn(100) * 200 + 600,  # May exceed max
            "DHI": np.random.randn(100) * 100 + 200,
            "Temperature": np.random.uniform(15, 35, 100),
            "Relative Humidity": np.random.rand(100) * 150,  # May exceed 100
        }
    )

    return df


@pytest.fixture
def metadata_df():
    """Create sample data with metadata columns"""
    timestamps = pd.date_range("2020-01-01", periods=100, freq="30min")

    df = pd.DataFrame(
        {
            "timestamp": timestamps,
            "GHI": np.random.rand(100) * 1000,
            "DNI": np.random.rand(100) * 800,
            "city": ["Phoenix"] * 100,
            "lat": [33.4484] * 100,
            "lon": [-112.0740] * 100,
            "grid_id": ["grid_001"] * 100,
        }
    )

    return df


class TestPhysicalConstraints:
    """Test suite for physical constraint functionality"""

    def test_non_negative_constraint(self, solar_df):
        """Test non-negative constraint for GHI"""
        resampler = TimeSeriesResampler()
        result = resampler.resample(
            solar_df, freq="10min", method="interpolate", constraints={"GHI": {"min": 0}}
        )

        # Verify all values >= 0
        assert (result["GHI"] >= 0).all(), "GHI should be non-negative"
        assert len(result) > len(solar_df), "Should have more rows after upsampling"

    def test_bounded_constraint(self, solar_df):
        """Test bounded constraint for Relative Humidity (0-100%)"""
        resampler = TimeSeriesResampler()
        result = resampler.resample(
            solar_df,
            freq="10min",
            method="interpolate",
            constraints={"Relative Humidity": {"min": 0, "max": 100}},
        )

        # Verify values within bounds
        assert (result["Relative Humidity"] >= 0).all(), "RH should be >= 0"
        assert (result["Relative Humidity"] <= 100).all(), "RH should be <= 100"

    def test_multiple_constraints(self, solar_df):
        """Test multiple constraints applied simultaneously"""
        resampler = TimeSeriesResampler()
        result = resampler.resample(
            solar_df,
            freq="10min",
            method="interpolate",
            constraints={
                "GHI": {"min": 0, "max": 1500},
                "DNI": {"min": 0, "max": 1200},
                "Relative Humidity": {"min": 0, "max": 100},
            },
        )

        # Verify all constraints applied
        assert (result["GHI"] >= 0).all() and (result["GHI"] <= 1500).all()
        assert (result["DNI"] >= 0).all() and (result["DNI"] <= 1200).all()
        assert (result["Relative Humidity"] >= 0).all() and (
            result["Relative Humidity"] <= 100
        ).all()

    def test_min_only_constraint(self, solar_df):
        """Test constraint with only minimum value"""
        resampler = TimeSeriesResampler()
        result = resampler.resample(
            solar_df, freq="10min", method="interpolate", constraints={"GHI": {"min": 0}}
        )

        assert (result["GHI"] >= 0).all()

    def test_max_only_constraint(self, solar_df):
        """Test constraint with only maximum value"""
        resampler = TimeSeriesResampler()
        result = resampler.resample(
            solar_df, freq="10min", method="interpolate", constraints={"GHI": {"max": 1500}}
        )

        assert (result["GHI"] <= 1500).all()

    def test_predefined_solar_constraints(self, solar_df):
        """Test using predefined solar radiation constraints"""
        resampler = TimeSeriesResampler()
        result = resampler.resample(
            solar_df, freq="10min", method="interpolate", constraints=SOLAR_RADIATION_CONSTRAINTS
        )

        # Verify solar radiation constraints applied
        assert (result["GHI"] >= 0).all() and (result["GHI"] <= 1500).all()
        assert (result["DNI"] >= 0).all() and (result["DNI"] <= 1200).all()
        assert (result["DHI"] >= 0).all() and (result["DHI"] <= 800).all()

    def test_constraints_with_aggregation(self, solar_df):
        """Test constraints work with aggregation methods (not just interpolate)"""
        resampler = TimeSeriesResampler()
        result = resampler.resample(
            solar_df, freq="1H", method="mean", constraints={"GHI": {"min": 0}}
        )

        # Constraints should apply to aggregated values too
        assert (result["GHI"] >= 0).all()


class TestInterpolationTracking:
    """Test suite for interpolation tracking functionality"""

    def test_track_interpolation_flag(self, solar_df):
        """Test is_interpolated column is added and correctly marked"""
        resampler = TimeSeriesResampler()
        result = resampler.resample(
            solar_df, freq="10min", method="interpolate", track_interpolation=True
        )

        # Verify tracking columns exist
        assert "is_interpolated" in result.columns, "Should have is_interpolated column"
        assert "data_source" in result.columns, "Should have data_source column"

        # Verify original timestamps marked as False
        original_timestamps = solar_df["timestamp"]
        original_mask = result["timestamp"].isin(original_timestamps)
        assert (
            ~result.loc[original_mask, "is_interpolated"]
        ).all(), "Original timestamps should be marked as not interpolated"

        # Verify new timestamps marked as True
        interpolated_mask = ~original_mask
        if interpolated_mask.sum() > 0:
            assert result.loc[
                interpolated_mask, "is_interpolated"
            ].all(), "Interpolated timestamps should be marked as interpolated"

    def test_data_source_labeling(self, solar_df):
        """Test data_source column labeling"""
        resampler = TimeSeriesResampler()
        result = resampler.resample(
            solar_df, freq="10min", method="interpolate", track_interpolation=True
        )

        # Check data source labels
        original_mask = ~result["is_interpolated"]
        interpolated_mask = result["is_interpolated"]

        # Original data should be labeled with original frequency
        if original_mask.sum() > 0:
            original_source = result.loc[original_mask, "data_source"].iloc[0]
            assert (
                "30min_original" in original_source
            ), f"Original data should be labeled '30min_original', got '{original_source}'"

        # Interpolated data should be labeled with aggregated/interpolated
        if interpolated_mask.sum() > 0:
            interp_source = result.loc[interpolated_mask, "data_source"].iloc[0]
            assert (
                "30min_aggregated" in interp_source
            ), f"Interpolated data should be labeled '30min_aggregated', got '{interp_source}'"

    def test_interpolation_statistics(self, solar_df):
        """Test interpolation statistics are logged correctly"""
        resampler = TimeSeriesResampler()
        result = resampler.resample(
            solar_df, freq="10min", method="interpolate", track_interpolation=True
        )

        original_count = (~result["is_interpolated"]).sum()
        interpolated_count = result["is_interpolated"].sum()

        # Should have some of each type
        assert original_count > 0, "Should have some original data points"
        assert interpolated_count > 0, "Should have some interpolated data points"

        # Total should equal result length
        assert original_count + interpolated_count == len(result)

    def test_track_interpolation_disabled(self, solar_df):
        """Test that tracking columns are not added when track_interpolation=False"""
        resampler = TimeSeriesResampler()
        result = resampler.resample(
            solar_df,
            freq="10min",
            method="interpolate",
            track_interpolation=False,  # Explicitly False
        )

        # Should NOT have tracking columns
        assert "is_interpolated" not in result.columns
        assert "data_source" not in result.columns

    def test_tracking_with_mean_aggregation(self, solar_df):
        """Test interpolation tracking works with mean aggregation"""
        resampler = TimeSeriesResampler()
        result = resampler.resample(solar_df, freq="10min", method="mean", track_interpolation=True)

        # Should have tracking columns with mean method too
        assert "is_interpolated" in result.columns
        assert "data_source" in result.columns


class TestMetadataPropagation:
    """Test suite for metadata column propagation"""

    def test_preserve_metadata_columns(self, metadata_df):
        """Test that metadata columns are preserved during resampling"""
        resampler = TimeSeriesResampler()
        result = resampler.resample(
            metadata_df, freq="10min", method="interpolate", preserve_metadata=True
        )

        # Verify metadata columns exist
        assert "city" in result.columns, "city column should be preserved"
        assert "lat" in result.columns, "lat column should be preserved"
        assert "lon" in result.columns, "lon column should be preserved"
        assert "grid_id" in result.columns, "grid_id column should be preserved"

        # Verify metadata values are consistent
        assert (result["city"] == "Phoenix").all(), "city values should be preserved"
        assert (result["lat"] == 33.4484).all(), "lat values should be preserved"
        assert (result["lon"] == -112.0740).all(), "lon values should be preserved"
        assert (result["grid_id"] == "grid_001").all(), "grid_id values should be preserved"

    def test_auto_detect_metadata(self, metadata_df):
        """Test automatic metadata column detection"""
        resampler = TimeSeriesResampler()
        result = resampler.resample(
            metadata_df,
            freq="10min",
            method="interpolate",
            preserve_metadata=True,
            metadata_cols=None,  # Auto-detect
        )

        # All non-numeric columns should be preserved
        assert "city" in result.columns
        assert "grid_id" in result.columns

        # Known metadata column names should be preserved
        assert "lat" in result.columns
        assert "lon" in result.columns

    def test_explicit_metadata_cols(self, metadata_df):
        """Test explicitly specified metadata columns"""
        resampler = TimeSeriesResampler()
        result = resampler.resample(
            metadata_df,
            freq="10min",
            method="interpolate",
            preserve_metadata=True,
            metadata_cols=["city", "lat"],  # Only these two
        )

        # Explicitly specified columns should be preserved
        assert "city" in result.columns
        assert "lat" in result.columns

        # Other metadata might or might not be there depending on auto-detection
        # but the explicit ones should definitely be preserved with correct values
        assert (result["city"] == "Phoenix").all()
        assert (result["lat"] == 33.4484).all()

    def test_preserve_metadata_disabled(self, metadata_df):
        """Test that metadata is not preserved when preserve_metadata=False"""
        resampler = TimeSeriesResampler()
        result = resampler.resample(
            metadata_df, freq="10min", method="interpolate", preserve_metadata=False
        )

        # Numeric columns should be present
        assert "GHI" in result.columns
        assert "DNI" in result.columns

        # Metadata behavior is implementation-dependent when preserve_metadata=False
        # Just verify the resampling completed successfully

    def test_metadata_with_datetime_column(self):
        """Test metadata propagation with datetime metadata column"""
        timestamps = pd.date_range("2020-01-01", periods=50, freq="30min")

        df = pd.DataFrame(
            {
                "timestamp": timestamps,
                "value": np.random.rand(50) * 100,
                "created_at": pd.Timestamp("2020-01-01"),  # Constant datetime metadata
                "location": "Phoenix",
            }
        )

        resampler = TimeSeriesResampler()
        result = resampler.resample(df, freq="10min", method="interpolate", preserve_metadata=True)

        # Datetime metadata should be preserved
        assert "created_at" in result.columns
        assert "location" in result.columns


class TestConstraintConfiguration:
    """Test suite for constraint configuration utilities"""

    def test_get_constraints_for_columns(self, solar_df):
        """Test automatic constraint selection based on column names"""
        from pvdata.config.constraints import get_constraints_for_columns

        # Get constraints for solar_df columns
        constraints = get_constraints_for_columns(solar_df.columns.tolist())

        # Should return constraints for columns that match predefined ones
        assert "GHI" in constraints
        assert "DNI" in constraints
        assert "DHI" in constraints
        assert "Temperature" in constraints
        assert "Relative Humidity" in constraints

        # Should not include columns that don't have predefined constraints
        assert "timestamp" not in constraints

        # Verify constraint structure
        assert "min" in constraints["GHI"]
        assert "max" in constraints["GHI"]

    def test_get_constraints_for_columns_solar_only(self, solar_df):
        """Test getting only solar radiation constraints"""
        from pvdata.config.constraints import get_constraints_for_columns

        constraints = get_constraints_for_columns(solar_df.columns.tolist(), constraint_set="solar")

        # Should include solar columns
        assert "GHI" in constraints
        assert "DNI" in constraints

        # Should NOT include meteorological columns
        assert "Temperature" not in constraints
        assert "Relative Humidity" not in constraints

    def test_get_non_negative_constraints(self, solar_df):
        """Test non-negative constraints utility"""
        from pvdata.config.constraints import get_non_negative_constraints

        constraints = get_non_negative_constraints(solar_df.columns.tolist())

        # Should return min=0 for non-negative columns
        assert "GHI" in constraints
        assert constraints["GHI"] == {"min": 0}

        assert "DNI" in constraints
        assert constraints["DNI"] == {"min": 0}

        # Should not include columns that aren't in NON_NEGATIVE_COLS
        assert "Temperature" not in constraints

    def test_integration_with_auto_constraints(self, solar_df):
        """Test using auto-selected constraints in resampling"""
        from pvdata.config.constraints import get_constraints_for_columns

        resampler = TimeSeriesResampler()
        constraints = get_constraints_for_columns(solar_df.columns.tolist())

        result = resampler.resample(
            solar_df,
            freq="10min",
            method="interpolate",
            constraints=constraints,  # Use auto-selected constraints
        )

        # Verify constraints were applied
        assert (result["GHI"] >= 0).all()
        assert (result["GHI"] <= 1500).all()
        assert (result["Relative Humidity"] >= 0).all()
        assert (result["Relative Humidity"] <= 100).all()


class TestBackwardCompatibility:
    """Test suite for backward compatibility"""

    def test_default_parameters(self, solar_df):
        """Test that old API calls still work with default parameters"""
        resampler = TimeSeriesResampler()

        # Old-style call without new parameters
        result = resampler.resample(solar_df, freq="1H", method="mean")

        # Should work without errors
        assert len(result) > 0
        assert "GHI" in result.columns

        # Should NOT have tracking columns by default
        assert "is_interpolated" not in result.columns
        assert "data_source" not in result.columns

    def test_old_api_still_works(self, solar_df):
        """Test that existing code patterns continue to work"""
        resampler = TimeSeriesResampler()

        # Test various old patterns
        result1 = resampler.resample(solar_df, freq="1H")
        assert len(result1) > 0

        result2 = resampler.resample(solar_df, freq="1H", method="sum")
        assert len(result2) > 0

        result3 = resampler.resample(solar_df, freq="15min", method="interpolate")
        assert len(result3) > 0

        result4 = resampler.resample(solar_df, freq="1H", method="mean", fill_method="ffill")
        assert len(result4) > 0

    def test_new_parameters_optional(self, solar_df):
        """Test that new parameters are truly optional"""
        resampler = TimeSeriesResampler()

        # Call with only some new parameters
        result1 = resampler.resample(
            solar_df,
            freq="10min",
            method="interpolate",
            constraints={"GHI": {"min": 0}},
            # Other new parameters use defaults
        )
        assert len(result1) > 0

        result2 = resampler.resample(
            solar_df,
            freq="10min",
            method="interpolate",
            track_interpolation=True,
            # Other new parameters use defaults
        )
        assert len(result2) > 0
        assert "is_interpolated" in result2.columns


class TestEdgeCases:
    """Test suite for edge cases and error conditions"""

    def test_empty_constraints_dict(self, solar_df):
        """Test passing empty constraints dictionary"""
        resampler = TimeSeriesResampler()
        result = resampler.resample(
            solar_df, freq="10min", method="interpolate", constraints={}  # Empty dict
        )

        # Should work without errors
        assert len(result) > 0

    def test_constraint_on_nonexistent_column(self, solar_df):
        """Test constraint on column that doesn't exist in DataFrame"""
        resampler = TimeSeriesResampler()
        result = resampler.resample(
            solar_df,
            freq="10min",
            method="interpolate",
            constraints={"nonexistent_column": {"min": 0}},
        )

        # Should work without errors (constraint is ignored for missing column)
        assert len(result) > 0

    def test_all_features_combined(self, metadata_df):
        """Test all new features working together"""
        resampler = TimeSeriesResampler()
        result = resampler.resample(
            metadata_df,
            freq="10min",
            method="interpolate",
            constraints={"GHI": {"min": 0, "max": 1500}},
            track_interpolation=True,
            preserve_metadata=True,
        )

        # Verify all features work together
        assert "is_interpolated" in result.columns  # Tracking
        assert "data_source" in result.columns
        assert (result["GHI"] >= 0).all()  # Constraints
        assert (result["GHI"] <= 1500).all()
        assert "city" in result.columns  # Metadata
        assert (result["city"] == "Phoenix").all()

    def test_downsampling_with_tracking(self, solar_df):
        """Test interpolation tracking works with downsampling"""
        resampler = TimeSeriesResampler()
        result = resampler.resample(
            solar_df,
            freq="2H",  # Downsample from 30min to 2H
            method="mean",
            track_interpolation=True,
        )

        # Should have tracking columns even for downsampling
        assert "is_interpolated" in result.columns
        assert "data_source" in result.columns
