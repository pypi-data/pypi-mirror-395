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

FASRAT provides a simple CLI with three required parameters:

```bash
fasrat --shapefile <SHAPEFILE_PATH> --raster <RASTER_FILE> --output <OUTPUT_FILE>
```

**Parameters:**

- `--shapefile` or `-s`: Path to your shapefile (.shp file)
- `--raster` or `-r`: Path to a sample raster file in NetCDF format (.nc)
- `--output` or `-o`: Full path for the output HDF5 file (e.g., `/path/to/weights.h5`)

### Example

```bash
fasrat --shapefile ../shapefiles/us_tract_2010/US_tract_2010.shp \
       --raster /data/climate/tmmx_2010.nc \
       --output ./output/tract_weights.h5
```

Or using short options:

```bash
fasrat -s ../shapefiles/us_tract_2010/US_tract_2010.shp \
       -r /data/climate/tmmx_2010.nc \
       -o ./output/tract_weights.h5
```

### Getting Help

```bash
fasrat --help
```

## Using FASRAT Programmatically

In addition to the command-line interface, you can use FASRAT as a Python library in your own scripts:

```python
from fasrat import compute_raster_weights

# Compute weights
compute_raster_weights(
    shapefile_path="./shapefiles/us_tract_2010/US_tract_2010.shp",
    raster_path="./data/tmmx_2010.nc",
    output_path="./output/tract_weights.h5"
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

The raster file should be in NetCDF format (`.nc`). The tool uses this file to:
1. Determine the coordinate reference system (CRS) for spatial alignment
2. Extract pixel resolution and dimensions
3. Compute the intersection weights between polygons and pixels

The raster file can contain any variable - the tool only uses the spatial metadata and grid structure.

## Output Format

FASRAT outputs an HDF5 file containing a pandas DataFrame with the following columns:

- `raster_bbox_coords`: Bounding box coordinates in raster index space for each polygon
- `weight`: A NumPy array (weight matrix) representing the area-weighted intersection between the polygon and each overlapping raster pixel. Weights sum to 1.0 for each polygon.
- `area`: The total area of each polygon (in the raster's CRS units)
- `bounds`: The geographic bounding box of each polygon
- `GEOID10` (or similar): The identifier from the original shapefile (if available)

### Using the Output

You can read and use the output weights like this:

```python
import pandas as pd
import rasterio
import numpy as np

# Load the weights
weights_df = pd.read_hdf('tract_weights.h5', key='weights')

# Load your raster data
with rasterio.open('your_raster.nc') as src:
    for idx, row in weights_df.iterrows():
        if row['weight'] is None:
            continue
        
        # Get the raster subset
        bbox = row['raster_bbox_coords']
        window = rasterio.windows.Window.from_slices(*bbox)
        raster_data = src.read(1, window=window)
        
        # Apply weights to aggregate
        weighted_value = np.sum(raster_data * row['weight'])
        print(f"Polygon {idx}: {weighted_value}")
```

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
- netcdf4 >= 1.7.2
- tqdm >= 4.67.1
- click >= 8.1.7

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
