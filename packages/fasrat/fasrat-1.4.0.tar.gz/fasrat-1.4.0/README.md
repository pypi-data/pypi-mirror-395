# FASRAT

**Fast Area-weighted Spatial ReAggregation Tool**

FASRAT is a Python command-line tool for computing area-weighted intersection weights between shapefile geometries (e.g., census tracts, counties, or other polygons) and raster pixels. This is particularly useful for spatially aggregating raster data (such as climate data, satellite imagery, or other gridded datasets) to polygon boundaries.

## Features

- 🗺️ Compute precise area-weighted intersections between vector polygons and raster grids
- 🚀 Fast processing with progress bars for large datasets
- 🎯 Automatically filters to contiguous US states (excludes Alaska, Hawaii, Puerto Rico)
- 💾 Outputs weight matrices in HDF5 format for efficient storage and reuse
- 🔧 Simple command-line interface with clear parameter validation

## Installation

### Option 1: Install from PyPI (Recommended)

Once published to PyPI, you can install FASRAT using pip:

```bash
pip install fasrat
```

### Option 2: Install from Source

#### Using pip

```bash
# Clone or download the repository
cd /path/to/FASRAT

# Install in development mode
pip install -e .

# Or install normally
pip install .
```

#### Using uv (Recommended for development)

FASRAT supports `uv` for Python environment management:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Navigate to the FASRAT directory
cd /path/to/FASRAT

# Install the package with uv
uv pip install -e .
```

This will install FASRAT and all its dependencies, and make the `fasrat` command available in your environment.

### Option 3: Install from GitHub

```bash
pip install git+https://github.com/yourusername/fasrat.git
```

## Usage

### Command-Line Interface

FASRAT provides two main commands:

#### 1. Computing Weights

First, compute the area-weighted intersection weights between your shapefile and raster grid:

```bash
fasrat weights --shapefile <SHAPEFILE_PATH> --raster <RASTER_FILE> --output <OUTPUT_FILE>
```

**Parameters:**

- `--shapefile` or `-s`: Path to your shapefile (.shp file)
- `--raster` or `-r`: Path to a sample raster file (any format supported by rasterio)
- `--output` or `-o`: Full path for the output parquet file (e.g., `/path/to/weights.parquet`)
- `--crs` or `-c`: Optional CRS string (e.g., 'EPSG:4326') to project the shapefile to

**Example:**

```bash
fasrat weights --shapefile ../shapefiles/us_tract_2010/US_tract_2010.shp \
               --raster /data/climate/tmmx_2010.nc \
               --output ./output/tract_weights.parquet
```

#### 2. Converting Raster Data

Apply the pre-computed weights to raster data for spatial averaging:

```bash
fasrat convert --weights <WEIGHTS_FILE> --raster <RASTER_FILE> --output <OUTPUT_FILE>
```

**Parameters:**

- `--weights` or `-w`: Path to the weights parquet file (from the weights command)
- `--raster` or `-r`: Path to the raster file to process (any format supported by rasterio)
- `--output` or `-o`: Path for the output file (CSV or parquet)
- `--geoid-col` or `-g`: Geometry ID column name (auto-detects if not specified)
- `--format` or `-f`: Output format ('csv' or 'parquet', default is 'csv')
- `--long` or `-l`: Output time-series data in long format (default is wide format)

**Example:**

```bash
# Convert raster data to tract-level averages
fasrat convert --weights ./output/tract_weights.parquet \
               --raster ./data/pm25_2010.nc \
               --output ./output/pm25_tract_2010.csv

# With long format for time-series data
fasrat convert --weights ./output/tract_weights.parquet \
               --raster ./data/pm25_2010.nc \
               --output ./output/pm25_tract_2010.csv \
               --long

# Output as parquet
fasrat convert --weights ./output/tract_weights.parquet \
               --raster ./data/pm25_2010.nc \
               --output ./output/pm25_tract_2010.parquet \
               --format parquet
```

### Getting Help

```bash
fasrat --help
fasrat weights --help
fasrat convert --help
```

## Using FASRAT Programmatically

In addition to the command-line interface, you can use FASRAT as a Python library in your own scripts:

```python
from fasrat import compute_raster_weights, apply_raster_weights

# Step 1: Compute weights
compute_raster_weights(
    shapefile_path="./shapefiles/us_tract_2010/US_tract_2010.shp",
    raster_path="./data/tmmx_2010.nc",
    output_path="./output/tract_weights.parquet"
)

# Step 2: Apply weights to raster data
apply_raster_weights(
    weights_path="./output/tract_weights.parquet",
    raster_path="./data/pm25_2010.nc",
    output_path="./output/pm25_tract_2010.csv",
    output_format="csv",
    long_format=False
)
```

This is useful when you want to integrate FASRAT into a larger data processing pipeline or automate batch processing.

## Input File Formats

### Shapefile

Provide the path to the `.shp` file. The shapefile should be a standard ESRI Shapefile format with associated files in the same directory:
- `.shp` - the main geometry file (this is what you provide to the CLI)
- `.shx` - shape index file
- `.dbf` - attribute database file
- `.prj` - projection information (recommended)

If your shapefile includes a state FIPS code column (e.g., `STATEFP10`, `STATEFP`, `STATE_FIPS`), the tool will automatically filter to contiguous US states.

### Raster File

The raster file can be in any format supported by rasterio (NetCDF `.nc`, GeoTIFF `.tif`, etc.). The tool uses this file to:
1. Determine the coordinate reference system (CRS) for spatial alignment
2. Extract pixel resolution and dimensions
3. Compute the intersection weights between polygons and pixels
4. Read and aggregate raster data values

For multi-band rasters, each band is treated as a time step. Single-band rasters are treated as single-time data.

## Output Format

### Weights File

FASRAT outputs a parquet file containing a pandas DataFrame with the following columns:

- `raster_bbox_coords`: Bounding box coordinates in raster index space for each polygon
- `weight`: A NumPy array (weight matrix) representing the area-weighted intersection between the polygon and each overlapping raster pixel. Weights sum to 1.0 for each polygon.
- `area`: The total area of each polygon (in the raster's CRS units)
- `bounds`: The geographic bounding box of each polygon
- `GEOID10` (or similar): The identifier from the original shapefile (if available)

### Converted Data File

The `convert` command outputs aggregated data in CSV or parquet format:

**Single-band rasters:**
- Rows = geometry IDs
- Columns = geometry ID column and 'value'

**Multi-band rasters (wide format, default):**
- Rows = time steps (band indices)
- Columns = geometry IDs

**Multi-band rasters (long format, with --long flag):**
- Rows = geometry ID × time combinations
- Columns = 'time', geometry ID column, 'value'

## How It Works

1. **Load Shapefile**: Reads the vector polygon data
2. **Filter Geometries**: Filters to contiguous US states (if state FIPS column exists)
3. **CRS Alignment**: Reprojects polygons to match the raster's coordinate system
4. **Bounding Box Computation**: Calculates the raster pixel indices that overlap each polygon
5. **Weight Matrix Calculation**: For each polygon, computes the area-weighted intersection with each overlapping raster pixel
6. **Normalization**: Ensures weights sum to 1.0 for each polygon
7. **Output**: Saves the weight matrices to HDF5 format for efficient reuse

## Requirements

- Python >= 3.9
- geopandas >= 1.0.1
- rasterio >= 1.4.3
- pandas >= 2.3.3
- numpy >= 2.0.2
- shapely >= 2.0.7
- tqdm >= 4.67.1
- click >= 8.1.7
- pyarrow (for parquet support)

## License

See the LICENSE file for details.

## Building and Publishing

### Building the Package

To build the package for distribution:

```bash
# Install build tools
pip install build

# Build the package
python -m build
```

This will create both `.tar.gz` (source distribution) and `.whl` (wheel) files in the `dist/` directory.

### Publishing to PyPI

```bash
# Install twine
pip install twine

# Upload to TestPyPI first (recommended)
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Citation

If you use FASRAT in your research, please cite it appropriately.
