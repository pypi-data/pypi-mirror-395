"""
Tests for solar position calculation module.
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timezone

try:
    import pvlib

    PVLIB_AVAILABLE = True
except ImportError:
    PVLIB_AVAILABLE = False


@unittest.skipIf(not PVLIB_AVAILABLE, "pvlib not installed")
class TestSolarPosition(unittest.TestCase):
    """Test solar position calculation functions."""

    def setUp(self):
        """Set up test data."""
        # Create sample time series for Shenzhen
        self.times = pd.date_range(
            "2020-01-01 00:00:00", "2020-01-01 23:00:00", freq="1H", tz="UTC"
        )
        self.df = pd.DataFrame(
            {
                "timestamp": self.times,
                "lat": 22.5431,  # Shenzhen
                "lon": 114.0576,
                "altitude_m": 0.0,
            }
        )

    def test_calculate_sun_position_basic(self):
        """Test basic solar position calculation."""
        from pvdata.solar import calculate_sun_position

        result = calculate_sun_position(self.df, time_col="timestamp", lat_col="lat", lon_col="lon")

        # Check that new columns were added
        self.assertIn("solar_azimuth", result.columns)
        self.assertIn("solar_altitude", result.columns)
        self.assertIn("solar_elevation", result.columns)
        self.assertIn("solar_zenith", result.columns)
        self.assertIn("is_daylight", result.columns)

        # Check value ranges
        self.assertTrue((result["solar_azimuth"] >= 0).all())
        self.assertTrue((result["solar_azimuth"] <= 360).all())
        self.assertTrue((result["solar_altitude"] >= -90).all())
        self.assertTrue((result["solar_altitude"] <= 90).all())

        # Check that altitude and elevation are the same (values only)
        np.testing.assert_array_equal(
            result["solar_altitude"].values, result["solar_elevation"].values
        )

        # Check zenith = 90 - altitude relationship
        np.testing.assert_array_almost_equal(
            result["solar_zenith"].values, 90 - result["solar_altitude"].values, decimal=5
        )

    def test_calculate_sun_position_with_altitude(self):
        """Test calculation with altitude parameter."""
        from pvdata.solar import calculate_sun_position

        # With altitude
        result_alt = calculate_sun_position(
            self.df, time_col="timestamp", lat_col="lat", lon_col="lon", altitude_col="altitude_m"
        )

        # Without altitude
        result_no_alt = calculate_sun_position(
            self.df, time_col="timestamp", lat_col="lat", lon_col="lon", altitude_col=None
        )

        # Results should be very similar but not identical
        # (altitude affects atmospheric refraction)
        self.assertTrue(
            np.allclose(
                result_alt["solar_altitude"].values,
                result_no_alt["solar_altitude"].values,
                atol=0.1,  # Within 0.1 degree
            )
        )

    def test_calculate_sun_position_fixed_location(self):
        """Test with fixed latitude and longitude values."""
        from pvdata.solar import calculate_sun_position

        result = calculate_sun_position(
            self.df,
            time_col="timestamp",
            lat_col=22.5431,  # Fixed values
            lon_col=114.0576,
            altitude_col=100.0,  # 100m elevation
        )

        self.assertIn("solar_azimuth", result.columns)
        self.assertIn("solar_altitude", result.columns)

    def test_add_solar_angles(self):
        """Test convenience function for fixed location."""
        from pvdata.solar import add_solar_angles

        result = add_solar_angles(
            self.df, lat=22.5431, lon=114.0576, altitude=100.0, time_col="timestamp"
        )

        self.assertIn("solar_azimuth", result.columns)
        self.assertIn("solar_altitude", result.columns)

    def test_zenith_to_altitude(self):
        """Test zenith to altitude conversion."""
        from pvdata.solar import zenith_to_altitude

        # Single value
        self.assertEqual(zenith_to_altitude(0), 90)
        self.assertEqual(zenith_to_altitude(90), 0)
        self.assertEqual(zenith_to_altitude(45), 45)

        # Series
        zenith_series = pd.Series([0, 45, 90, 135, 180])
        altitude_series = zenith_to_altitude(zenith_series)
        expected = pd.Series([90, 45, 0, -45, -90])
        pd.testing.assert_series_equal(altitude_series, expected)

        # Array
        zenith_array = np.array([0, 45, 90])
        altitude_array = zenith_to_altitude(zenith_array)
        np.testing.assert_array_equal(altitude_array, [90, 45, 0])

    def test_altitude_to_zenith(self):
        """Test altitude to zenith conversion."""
        from pvdata.solar import altitude_to_zenith

        # Single value
        self.assertEqual(altitude_to_zenith(90), 0)
        self.assertEqual(altitude_to_zenith(0), 90)
        self.assertEqual(altitude_to_zenith(45), 45)

        # Roundtrip
        from pvdata.solar import zenith_to_altitude

        values = [0, 30, 60, 90, 120, 150, 180]
        for zenith in values:
            altitude = zenith_to_altitude(zenith)
            zenith_back = altitude_to_zenith(altitude)
            self.assertAlmostEqual(zenith, zenith_back)

    def test_daylight_detection(self):
        """Test daylight detection."""
        from pvdata.solar import calculate_sun_position

        result = calculate_sun_position(self.df, time_col="timestamp", lat_col="lat", lon_col="lon")

        # Check that is_daylight matches altitude > 0
        expected_daylight = (result["solar_altitude"] > 0).values
        np.testing.assert_array_equal(result["is_daylight"].values, expected_daylight)

        # There should be both day and night times in 24 hours
        self.assertTrue(result["is_daylight"].any())
        self.assertFalse(result["is_daylight"].all())

    def test_inplace_modification(self):
        """Test inplace parameter."""
        from pvdata.solar import calculate_sun_position

        df_copy = self.df.copy()

        # Not inplace (default)
        result = calculate_sun_position(
            df_copy, time_col="timestamp", lat_col="lat", lon_col="lon", inplace=False
        )

        # Original should not be modified
        self.assertNotIn("solar_azimuth", df_copy.columns)
        # Result should have new columns
        self.assertIn("solar_azimuth", result.columns)

        # Inplace
        df_copy2 = self.df.copy()
        result2 = calculate_sun_position(
            df_copy2, time_col="timestamp", lat_col="lat", lon_col="lon", inplace=True
        )

        # Original should be modified
        self.assertIn("solar_azimuth", df_copy2.columns)
        # Should return the same object
        self.assertIs(result2, df_copy2)

    def test_different_methods(self):
        """Test different calculation methods."""
        from pvdata.solar import calculate_sun_position

        methods = ["nrel_numpy", "nrel_numba", "ephemeris"]

        results = {}
        for method in methods:
            try:
                result = calculate_sun_position(
                    self.df.head(5),  # Small sample
                    time_col="timestamp",
                    lat_col="lat",
                    lon_col="lon",
                    method=method,
                )
                results[method] = result
            except Exception:
                # Some methods might not be available
                pass

        # If we got results, they should be very similar
        if len(results) >= 2:
            methods_list = list(results.keys())
            result1 = results[methods_list[0]]
            result2 = results[methods_list[1]]

            np.testing.assert_allclose(
                result1["solar_altitude"].values,
                result2["solar_altitude"].values,
                atol=0.01,  # Within 0.01 degree
            )

    def test_error_handling(self):
        """Test error handling."""
        from pvdata.solar import calculate_sun_position
        from pvdata.utils.exceptions import PVDataError

        # Missing time column
        with self.assertRaises(PVDataError):
            calculate_sun_position(self.df, time_col="nonexistent", lat_col="lat", lon_col="lon")

        # Missing lat column
        with self.assertRaises(PVDataError):
            calculate_sun_position(
                self.df, time_col="timestamp", lat_col="nonexistent", lon_col="lon"
            )

        # Missing lon column
        with self.assertRaises(PVDataError):
            calculate_sun_position(
                self.df, time_col="timestamp", lat_col="lat", lon_col="nonexistent"
            )


class TestSolarPositionWithoutPvlib(unittest.TestCase):
    """Test behavior when pvlib is not available."""

    @unittest.skipIf(PVLIB_AVAILABLE, "pvlib is installed")
    def test_error_without_pvlib(self):
        """Test that helpful error is raised when pvlib not installed."""
        from pvdata.solar import calculate_sun_position
        from pvdata.utils.exceptions import PVDataError

        df = pd.DataFrame(
            {
                "timestamp": pd.date_range("2020-01-01", periods=10, freq="1H"),
                "lat": 22.5431,
                "lon": 114.0576,
            }
        )

        with self.assertRaises(PVDataError) as cm:
            calculate_sun_position(df, time_col="timestamp")

        self.assertIn("pvlib", str(cm.exception).lower())
        self.assertIn("pip install", str(cm.exception).lower())


class TestSolarIntegration(unittest.TestCase):
    """Integration tests with other pvdata modules."""

    @unittest.skipIf(not PVLIB_AVAILABLE, "pvlib not installed")
    def test_with_parquet_io(self):
        """Test solar calculation with parquet IO."""
        import tempfile
        import os
        from pvdata.solar import calculate_sun_position
        from pvdata.io import write_parquet, read_parquet

        # Create test data
        df = pd.DataFrame(
            {
                "timestamp": pd.date_range("2020-01-01", periods=100, freq="1H", tz="UTC"),
                "lat": 22.5431,
                "lon": 114.0576,
                "temperature": np.random.randn(100) + 25,
            }
        )

        # Add solar position
        df = calculate_sun_position(df, time_col="timestamp", lat_col="lat", lon_col="lon")

        # Write to parquet
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test.parquet")
            write_parquet(df, file_path)

            # Read back
            df_read = read_parquet(file_path)

            # Check that solar columns are preserved
            self.assertIn("solar_azimuth", df_read.columns)
            self.assertIn("solar_altitude", df_read.columns)

            # Values should match (allowing dtype optimization)
            pd.testing.assert_frame_equal(df, df_read, check_dtype=False)


if __name__ == "__main__":
    unittest.main()
