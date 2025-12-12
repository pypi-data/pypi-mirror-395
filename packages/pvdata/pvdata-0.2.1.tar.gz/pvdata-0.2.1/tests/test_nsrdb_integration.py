"""
Integration tests for NSRDB module

Tests the complete data fetching pipeline.
"""

import pytest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
from pvdata.sources.nsrdb import (
    fetch,
    fetch_multi_grid,
    CITIES,
    CITY_DATASET_CONFIG,
    auto_select_dataset,
)
from pvdata.geo import generate_grid, haversine_distance


class TestDatasetConfiguration:
    """Test dataset configuration and selection"""

    def test_cities_configuration(self):
        """Test that all predefined cities have required fields"""
        required_fields = ["country", "lat", "lon", "altitude", "timezone", "climate"]

        for city_name, config in CITIES.items():
            for field in required_fields:
                assert field in config, f"{city_name} missing {field}"

            # Validate coordinate ranges
            assert -90 <= config["lat"] <= 90, f"{city_name} has invalid latitude"
            assert (
                -180 <= config["lon"] <= 180
            ), f"{city_name} has invalid longitude"

    def test_dataset_configuration(self):
        """Test that all cities have dataset configuration"""
        for city_name in CITIES.keys():
            assert (
                city_name in CITY_DATASET_CONFIG
            ), f"{city_name} missing dataset config"

            config = CITY_DATASET_CONFIG[city_name]
            assert "dataset" in config
            assert "interval" in config
            assert "years" in config
            assert isinstance(config["years"], list)
            assert len(config["years"]) > 0

    def test_auto_select_dataset(self):
        """Test automatic dataset selection based on coordinates"""
        # Phoenix (Americas - GOES)
        assert (
            auto_select_dataset(33.4484, -112.0740)
            == "nsrdb-GOES-aggregated-v4-0-0-download"
        )

        # Mumbai (India - SUNY India)
        assert auto_select_dataset(19.0760, 72.8777) == "suny-india-download"

        # London (Europe - MSG)
        assert (
            auto_select_dataset(51.5074, -0.1278) == "nsrdb-msg-v1-0-0-download"
        )

        # Beijing (Asia - Himawari)
        assert auto_select_dataset(39.9042, 116.4074) == "himawari-download"

        # Fairbanks (Polar)
        assert (
            auto_select_dataset(64.8378, -147.7164)
            == "nsrdb-polar-v4-0-0-download"
        )


class TestGeoUtilities:
    """Test geographic utilities"""

    def test_generate_grid_10_point(self):
        """Test 10-point grid generation"""
        grids = generate_grid(
            center_lat=33.4484, center_lon=-112.0740, pattern="10_point", radius_km=20
        )

        assert len(grids) == 10
        assert grids[0]["grid_id"] == 0
        assert grids[0]["description"] == "center"
        assert grids[0]["lat"] == 33.4484
        assert grids[0]["lon"] == -112.0740

        # Check that all 8 directions exist
        directions = [g["description"] for g in grids[1:9]]
        for direction in ["N_", "NE_", "E_", "SE_", "S_", "SW_", "W_", "NW_"]:
            assert any(direction in d for d in directions)

    def test_generate_grid_5_point(self):
        """Test 5-point grid generation"""
        grids = generate_grid(
            center_lat=33.4484, center_lon=-112.0740, pattern="5_point", radius_km=10
        )

        assert len(grids) == 5
        assert grids[0]["description"] == "center"

        # Check cardinal directions
        descriptions = [g["description"] for g in grids]
        assert any("N_" in d for d in descriptions)
        assert any("E_" in d for d in descriptions)
        assert any("S_" in d for d in descriptions)
        assert any("W_" in d for d in descriptions)

    def test_generate_grid_9_point(self):
        """Test 9-point grid generation"""
        grids = generate_grid(
            center_lat=33.4484, center_lon=-112.0740, pattern="9_point", radius_km=15
        )

        assert len(grids) == 9
        assert grids[0]["description"] == "center"

    def test_haversine_distance(self):
        """Test distance calculation"""
        # Distance should be symmetric
        d1 = haversine_distance(33.4484, -112.0740, 41.8781, -87.6298)
        d2 = haversine_distance(41.8781, -87.6298, 33.4484, -112.0740)
        assert abs(d1 - d2) < 0.001

        # Distance to self should be 0
        d = haversine_distance(33.4484, -112.0740, 33.4484, -112.0740)
        assert d < 0.001

        # Phoenix to Chicago should be ~2200-2400 km
        d = haversine_distance(33.4484, -112.0740, 41.8781, -87.6298)
        assert 2200 < d < 2400


class TestNSRDBIntegration:
    """Test NSRDB data fetching pipeline (mocked)"""

    @patch("pvdata.sources.nsrdb.api.requests.get")
    def test_fetch_with_mock_api(self, mock_get):
        """Test fetch function with mocked API response"""
        # Create mock CSV response
        mock_csv = """Source,Location ID,City,State,Country,Latitude,Longitude,Time Zone,Elevation,Local Time Zone,Clearsky DHI Units,Clearsky DNI Units,Clearsky GHI Units,Dew Point Units,DHI Units,DNI Units,GHI Units,Solar Zenith Angle Units,Temperature Units,Pressure Units,Relative Humidity Units,Precipitable Water Units,Wind Direction Units,Wind Speed Units,Cloud Type -15,Cloud Type 0,Cloud Type 1,Cloud Type 2,Cloud Type 3,Cloud Type 4,Cloud Type 5,Cloud Type 6,Cloud Type 7,Cloud Type 8,Cloud Type 9,Cloud Type 10,Cloud Type 11,Cloud Type 12,Fill Flag 0,Fill Flag 1,Fill Flag 2,Fill Flag 3,Fill Flag 4,Fill Flag 5,Surface Albedo Units,Version
NSRDB,94018,,Arizona,United States,33.45,-112.07,-7,331,-7,w/m2,w/m2,w/m2,c,w/m2,w/m2,w/m2,Degree,c,mbar,%,cm,Degree,m/s,N/A,Clear,Probably Clear,Fog,Water,Super-Cooled Water,Mixed,Opaque Ice,Cirrus,Overlapping,Overshooting,Unknown,Dust,Smoke,N/A,Missing Image,Low Irradiance,Exceeds Clearsky,Stale,Fill Flag 5,N/A,v3.2.0
Year,Month,Day,Hour,Minute,GHI,DNI,DHI,Clearsky GHI,Clearsky DNI,Clearsky DHI,Cloud Type,Dew Point,Solar Zenith Angle,Fill Flag,Surface Albedo,Wind Speed,Precipitable Water,Wind Direction,Relative Humidity,Temperature,Pressure
2020,1,1,0,0,0,0,0,0,0,0,0,0.5,121.95,0,0.169998,2.4,0.76,109,58,9.7,994
2020,1,1,0,30,0,0,0,0,0,0,0,0.5,129.07,0,0.169998,2.4,0.76,109,58,9.7,994
2020,1,1,1,0,0,0,0,0,0,0,0,0.5,136.05,0,0.169998,2.4,0.76,109,58,9.7,994"""

        mock_response = Mock()
        mock_response.text = mock_csv
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Test fetch with city
        df = fetch(
            city="Phoenix",
            year=2020,
            api_key="test_key",
            target_interval="30min",
            apply_constraints=False,
            calculate_solar=False,
        )

        assert len(df) > 0
        assert "timestamp" in df.columns
        assert "GHI" in df.columns
        assert "city" in df.columns
        assert df["city"].iloc[0] == "Phoenix"

    def test_fetch_validation(self):
        """Test fetch input validation"""
        # Should raise error if no api_key
        with pytest.raises(ValueError, match="api_key is required"):
            fetch(city="Phoenix", year=2020)

        # Should raise error if unknown city
        with pytest.raises(ValueError, match="Unknown city"):
            fetch(city="UnknownCity", year=2020, api_key="test")

        # Should raise error if neither city nor coordinates
        with pytest.raises(ValueError, match="Either city or"):
            fetch(year=2020, api_key="test")


class TestBackwardCompatibility:
    """Test backward compatibility with existing code"""

    def test_old_api_still_works(self):
        """Test that existing TimeSeriesResampler API still works"""
        from pvdata.processing import TimeSeriesResampler

        # Create test data
        df = pd.DataFrame(
            {
                "timestamp": pd.date_range("2020-01-01", periods=100, freq="30min"),
                "GHI": [100.0] * 100,
            }
        )

        resampler = TimeSeriesResampler(timestamp_column="timestamp")

        # Old API (without new parameters) should still work
        result = resampler.resample(df, freq="10min", method="interpolate")

        assert len(result) > len(df)
        assert "timestamp" in result.columns
        assert "GHI" in result.columns


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
