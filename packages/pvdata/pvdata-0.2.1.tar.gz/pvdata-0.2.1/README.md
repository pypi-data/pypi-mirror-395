# pvdata - Photovoltaic Data Toolkit

[![Tests](https://github.com/pvdata/pvdata/workflows/Tests/badge.svg)](https://github.com/pvdata/pvdata/actions)
[![PyPI version](https://badge.fury.io/py/pvdata.svg)](https://badge.fury.io/py/pvdata)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

High-performance toolkit for photovoltaic (solar) data processing, storage, and analysis.

## Features

### Core Features
- **Extreme Performance**: 46x compression ratio, 17-64x read speedup
- **Optimized Storage**: Automatic data type optimization saves 75% memory
- **Easy to Use**: Simple, intuitive API with smart defaults
- **Complete Workflow**: From data collection to analysis
- **Battle-Tested**: Used in production for solar energy analysis

### NEW in v0.1.3 - NSRDB Data Collection
- **One-Line Data Fetching**: Get NSRDB data with a single function call
- **Global Coverage**: 10 predefined cities across 5 continents
- **Auto Dataset Selection**: Automatically chooses the best dataset for any location
- **Multi-Grid Support**: Fetch data for multiple nearby points simultaneously
- **Complete Pipeline**: UTC timezone handling, interpolation, physical constraints, solar angles
- **Geographic Tools**: Grid generation and distance calculations

## Installation

```bash
pip install pvdata
```

For development:
```bash
pip install pvdata[dev]
```

For all features:
```bash
pip install pvdata[all]
```

## Quick Start

### Data Storage and Processing

```python
import pvdata as pv

# Read CSV with automatic optimization
df = pv.read_csv('solar_data.csv')

# Write to Parquet (46x compression!)
pv.write_parquet(df, 'solar_data.parquet')

# Fast read (17x faster than CSV)
df = pv.read_parquet('solar_data.parquet')

# Read specific columns only (30x faster)
df = pv.read_parquet('solar_data.parquet', columns=['eff', 'Hour'])

# Batch convert directory
stats = pv.batch_convert('csv_dir/', 'parquet_dir/')
print(f"Compression ratio: {stats['compression_ratio']:.1f}x")
```

### NEW: NSRDB Data Collection (v0.1.3+)

Fetch solar irradiance data from NREL's NSRDB database with a single line of code:

```python
import pvdata as pv

# Fetch data for a predefined city (one line!)
df = pv.sources.nsrdb.fetch(
    city="Phoenix",
    year=2020,
    api_key="YOUR_API_KEY"  # Get free key at https://developer.nrel.gov/signup/
)

# Or use custom coordinates
df = pv.sources.nsrdb.fetch(
    lat=33.4484,
    lon=-112.0740,
    year=2020,
    dataset="auto",  # Automatically selects best dataset
    api_key="YOUR_API_KEY"
)

# Fetch multiple grid points around a location
dfs = pv.sources.nsrdb.fetch_multi_grid(
    city="Phoenix",
    year=2020,
    grid_pattern="10_point",  # 10 points in 20km radius
    api_key="YOUR_API_KEY"
)
```

**Supported Cities**: Phoenix, Chicago, Manaus, Lagos, London, Dubai, Fairbanks, Beijing, Mumbai, Sydney

**What you get automatically**:
- ✅ Optimal dataset selection (GOES, MSG, Himawari, Polar, SUNY India)
- ✅ UTC timezone handling (avoids DST issues)
- ✅ Interpolation to your target interval (default: 10min)
- ✅ Physical constraints applied (GHI ≥ 0, humidity ∈ [0,100], etc.)
- ✅ Solar angles calculated (altitude, azimuth, zenith)
- ✅ Metadata preserved (location, timezone, climate info)

## Performance Benchmarks

Based on real-world testing (14.39 MB CSV, 560K rows):

| Operation | CSV | Parquet | Speedup |
|-----------|-----|---------|---------|
| Storage | 14.39 MB | 0.31 MB | **46.6x** |
| Full read | 0.064s | 0.004s | **17.3x** |
| Column read | 0.064s | 0.002s | **30.3x** |
| Filtered read | 0.064s | 0.001s | **64x** |

## Documentation

- [User Guide](docs/USER_GUIDE.md) - Complete user manual
- [API Reference](docs/api/) - Detailed API documentation
  - [I/O Operations](docs/api/io.md)
  - [Time Series Processing](docs/api/timeseries.md)
  - [NSRDB Data Collection](docs/api/nsrdb.md) - NEW!
  - [Geographic Tools](docs/api/geo.md) - NEW!
- [Examples](examples/) - Code examples
  - [NSRDB Quick Start](examples/nsrdb_quickstart.py) - NEW!
- [Changelog](CHANGELOG.md) - Version history

## Requirements

- Python 3.8+
- pandas >= 1.5.0
- pyarrow >= 10.0.0
- numpy >= 1.21.0

## Development

```bash
# Clone repository
git clone https://github.com/pvdata/pvdata.git
cd pvdata

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/ tests/

# Type check
mypy src/pvdata
```

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use pvdata in your research, please cite:

```bibtex
@software{pvdata2025,
  title = {pvdata: High-performance photovoltaic data toolkit},
  author = {PVData Team},
  year = {2025},
  url = {https://github.com/pvdata/pvdata}
}
```

## Roadmap

### v0.1.3 (Current) ✅
- [x] Project structure
- [x] Core I/O operations (read, write, batch processing)
- [x] Data processing (time series resampling, aggregation)
- [x] Physical constraints and data quality tracking
- [x] Timezone handling (UTC strategy)
- [x] NSRDB data collection (10 global cities)
- [x] Geographic tools (grid generation, distance calculations)
- [x] Solar angle calculations
- [x] Test coverage: 85% (215/217 tests passing)

### v0.2.0 (Planned)
- [ ] Enhanced documentation
- [ ] More city configurations
- [ ] Additional data sources
- [ ] Performance optimizations
- [ ] Advanced analytics module

### v1.0.0 (Future)
- [ ] Distributed processing support
- [ ] Real-time data streaming
- [ ] Web API and dashboard
- [ ] Machine learning integration

## Support

- **Issues**: [GitHub Issues](https://github.com/pvdata/pvdata/issues)
- **Discussions**: [GitHub Discussions](https://github.com/pvdata/pvdata/discussions)
- **Email**: pvdata@example.com

## Acknowledgments

This project was developed to address the challenges of processing large-scale
photovoltaic data for building energy analysis.

---

**Made with ❤️ for the solar energy community**
