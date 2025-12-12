import geopandas as gpd
import rasterio
import os
from tqdm import tqdm
from fasrat import constants, geometry
import pandas as pd
import pickle
import numpy as np
import netCDF4 as nc


def compute_raster_weights(
    shapefile_path: str, raster_path: str, output_path: str, crs: str = None
) -> None:
    """
    Compute area-weighted spatial reaggregation weights between shapefile geometries and raster pixels.

    This function takes a shapefile containing polygon geometries (e.g., census tracts) and a raster file,
    then computes the area-weighted intersection between each polygon and the raster pixels it overlaps.
    The output is a weight matrix for each polygon that can be used to aggregate raster values to the
    polygon level.

    Args:
        shapefile_path: Path to the shapefile (.shp file)
        raster_path: Path to the sample raster file (.nc format)
        output_path: Full path for the output HDF5 file (including filename and .h5 extension)
        crs: Optional CRS string (e.g., "EPSG:4326") to project the shapefile to.
             If None, uses the CRS from the raster file.

    Returns:
        None. Results are saved to the specified HDF5 file.

    Raises:
        FileNotFoundError: If shapefile or raster file cannot be found
        ValueError: If the file is not a valid .shp file
    """
    # progress bar setting
    tqdm.pandas()

    # Validate inputs
    if not os.path.exists(shapefile_path):
        raise FileNotFoundError(f"Shapefile not found: {shapefile_path}")

    if not shapefile_path.endswith(".shp"):
        raise ValueError(f"File must be a .shp file: {shapefile_path}")

    if not os.path.exists(raster_path):
        raise FileNotFoundError(f"Raster file not found: {raster_path}")

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Load shapefile
    print("Loading shapefile...")
    gdf = gpd.read_file(shapefile_path)

    # Get only the contiguous US (filtering out Alaska, Hawaii, Puerto Rico)
    # Check if STATEFP10 column exists (2010 census), otherwise try other common state FIPS columns
    state_col = None
    for col in ["STATEFP10", "STATEFP", "STATE_FIPS", "STFIPS"]:
        if col in gdf.columns:
            state_col = col
            break

    if state_col:
        print(f"Filtering to contiguous US states using column: {state_col}")
        gdf_contiguous_us = gdf[~gdf[state_col].isin(constants.NON_CONTIGUOUS_STATES)]
        print(f"Filtered from {len(gdf)} to {len(gdf_contiguous_us)} geometries")
    else:
        print("Warning: No state FIPS column found. Processing all geometries.")
        gdf_contiguous_us = gdf

    # Load raster file and convert CRS
    print("Computing raster weights for each geometry...")
    with rasterio.open(raster_path) as raster_data:
        # Use provided CRS if available, otherwise use raster CRS
        if crs:
            target_crs = crs
            print(f"Using provided CRS: {target_crs}")
            if raster_data.crs and raster_data.crs != target_crs:
                raise ValueError(
                    f"Provided CRS {target_crs} does not match raster CRS {raster_data.crs}."
                )
        else:
            target_crs = raster_data.crs
            if target_crs is None:
                raise ValueError("Raster has no CRS and no CRS was provided.")
            print(f"Using raster CRS: {target_crs}")

        gdf_contiguous_us.to_crs(target_crs, inplace=True)

        # Compute bounding boxes for each geometry
        gdf_contiguous_us["bounds"] = gdf_contiguous_us["geometry"].apply(
            lambda x: x.bounds
        )

        print("Computing bounding box raster indices for each geometry...")
        # Compute raster indices for each geometry
        gdf_contiguous_us["raster_bbox_coords"] = gdf_contiguous_us["bounds"].apply(
            geometry.convert_bbox_coord_to_raster_index, args=(raster_data,)
        )

        # Compute area for each geometry
        gdf_contiguous_us["area"] = gdf_contiguous_us["geometry"].area

        print("Computing weight matrix for each geometry...")
        # Compute weight matrix for each geometry (with progress bar)
        gdf_contiguous_us["weight"] = gdf_contiguous_us.progress_apply(
            geometry.get_weight_matrix, axis=1, args=(raster_data,)
        )

    print("Saving to file...")
    # Determine which ID column to use
    id_col = None
    for col in ["GEOID10", "GEOID", "GEO_ID", "ID"]:
        if col in gdf_contiguous_us.columns:
            id_col = col
            break

    # Build the columns to save
    cols_to_save = ["raster_bbox_coords", "weight", "area", "bounds"]
    if id_col:
        cols_to_save.append(id_col)

    # Drop geometry column and save to pandas df
    df_weights = pd.DataFrame(gdf_contiguous_us.loc[:, cols_to_save])
    df_weights["weight"] = df_weights["weight"].apply(pickle.dumps)

    # Save to HDF5 file
    df_weights.to_parquet(
        output_path,
        index=False,
    )

    print(f"Done! Results saved to: {output_path}")
    print(f"Processed {len(df_weights)} geometries")


def apply_raster_weights(
    weights_path: str,
    nc_path: str,
    output_path: str,
    nc_variable: str = None,
    geoid_column: str = None,
    output_format: str = "csv",
    long_format: bool = False,
) -> None:
    """
    Apply pre-computed raster weights to NetCDF data for weighted spatial averaging.

    This function takes a weights file (generated by compute_raster_weights) and a NetCDF raster file,
    then computes weighted averages for each geometry. Supports both time-series (3D) and single-time (2D) data.

    Args:
        weights_path: Path to the weights parquet file (output from compute_raster_weights)
        nc_path: Path to the NetCDF file containing raster data
        output_path: Path for the output file (CSV or parquet)
        nc_variable: Name of the NetCDF variable to process. If None, auto-detects if only one variable exists.
        geoid_column: Name of the column containing geometry IDs. If None, auto-detects (tries GEOID10, GEOID, GEO_ID, ID).
        output_format: Output format, either 'csv' or 'parquet'. Default is 'csv'.
        long_format: If True, time-series data is output in long format (rows = geoid x time combinations).
                     If False (default), time-series data is in wide format (rows = time, columns = geoids).
                     Has no effect on single-time data.

    Returns:
        None. Results are saved to the specified output file.

    Raises:
        FileNotFoundError: If weights file or NetCDF file cannot be found
        ValueError: If NetCDF variable cannot be determined or is invalid
    """
    # Validate inputs
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"Weights file not found: {weights_path}")

    if not os.path.exists(nc_path):
        raise FileNotFoundError(f"NetCDF file not found: {nc_path}")

    if output_format not in ["csv", "parquet"]:
        raise ValueError(
            f"Output format must be 'csv' or 'parquet', got: {output_format}"
        )

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Load weights file
    print("Loading raster weights...")
    df_weights = pd.read_parquet(weights_path)

    # Unpickle the weight column
    print("Unpickling weight matrices...")
    df_weights["weight"] = df_weights["weight"].apply(pickle.loads)

    # Determine geometry ID column
    if geoid_column:
        if geoid_column not in df_weights.columns:
            raise ValueError(
                f"Specified geometry ID column '{geoid_column}' not found in weights file"
            )
        id_col = geoid_column
    else:
        # Auto-detect
        id_col = None
        for col in ["GEOID10", "GEOID", "GEO_ID", "ID"]:
            if col in df_weights.columns:
                id_col = col
                break
        if id_col is None:
            raise ValueError(
                "Could not auto-detect geometry ID column. Please specify using --geoid-col. "
                "Available columns: " + ", ".join(df_weights.columns)
            )

    print(f"Using geometry ID column: {id_col}")

    # Open NetCDF file and determine variable
    print("Opening NetCDF file...")
    with nc.Dataset(nc_path, "r") as nc_data:
        # Get all data variables (exclude dimensions)
        all_vars = list(nc_data.variables.keys())
        dim_vars = list(nc_data.dimensions.keys())
        data_vars = [v for v in all_vars if v not in dim_vars]

        # Determine which variable to use
        if nc_variable:
            if nc_variable not in nc_data.variables:
                raise ValueError(
                    f"Specified NetCDF variable '{nc_variable}' not found. "
                    f"Available variables: {', '.join(all_vars)}"
                )
            var_name = nc_variable
        else:
            # Auto-detect
            if len(data_vars) == 0:
                raise ValueError(
                    f"No data variables found in NetCDF file. Available variables: {', '.join(all_vars)}"
                )
            elif len(data_vars) == 1:
                var_name = data_vars[0]
                print(f"Auto-detected NetCDF variable: {var_name}")
            else:
                raise ValueError(
                    f"Multiple data variables found in NetCDF file. Please specify one using --variable. "
                    f"Available data variables: {', '.join(data_vars)}"
                )

        # Read the raster data
        print(f"Reading NetCDF variable '{var_name}'...")
        raster_data = nc_data.variables[var_name][:]

        # Determine if time-series or single-time data
        data_shape = raster_data.shape
        print(f"Data shape: {data_shape}")

        if len(data_shape) == 3:
            # Time-series data (time, rows, cols)
            is_timeseries = True
            num_times = data_shape[0]
            print(f"Detected time-series data with {num_times} time steps")

            # Try to get time information for creating date index
            time_var = None
            for possible_time_var in [
                "time",
                "Time",
                "TIME",
                "date",
                "Date",
                "day",
                "month",
                "Day",
                "Month",
            ]:
                if possible_time_var in nc_data.variables:
                    time_var = possible_time_var
                    break

            if time_var:
                try:
                    time_data = nc_data.variables[time_var]
                    time_index = nc.num2date(
                        time_data[:],
                        units=time_data.units,
                        calendar=getattr(time_data, "calendar", "standard"),
                    )
                    print(f"Using time variable '{time_var}' for date index")
                except Exception as e:
                    print(
                        f"Warning: Could not parse time variable: {e}. Using integer index instead."
                    )
                    time_index = np.arange(num_times)
            else:
                print("Warning: No time variable found. Using integer index.")
                time_index = np.arange(num_times)

        elif len(data_shape) == 2:
            # Single-time data (rows, cols)
            is_timeseries = False
            print("Detected single-time data")
        else:
            raise ValueError(
                f"Unexpected data shape: {data_shape}. Expected 2D (rows, cols) or 3D (time, rows, cols)"
            )

        # Get number of geometries
        num_geoms = len(df_weights)

        # Create placeholder numpy array
        if is_timeseries:
            result_array = np.zeros((num_geoms, num_times))
        else:
            result_array = np.zeros(num_geoms)

        # Loop through each geometry and compute weighted average
        print("Computing weighted averages for each geometry...")
        for idx, row in tqdm(df_weights.iterrows(), total=num_geoms):
            # Get raster bbox coordinates and weight matrix
            raster_bbox_coords = row["raster_bbox_coords"]
            weight = row["weight"]

            # Handle None or missing weight
            if weight is None or (isinstance(weight, float) and np.isnan(weight)):
                if is_timeseries:
                    result_array[idx, :] = np.nan
                else:
                    result_array[idx] = np.nan
                continue

            # Extract bbox coordinates
            (row_start, row_stop), (col_start, col_stop) = raster_bbox_coords

            # Get subset of raster data
            if is_timeseries:
                data_subset = raster_data[:, row_start:row_stop, col_start:col_stop]
                # Handle masked arrays - fill masked values with 0
                if np.ma.is_masked(data_subset):
                    data_subset = np.ma.filled(data_subset, 0)
                data_subset[np.isnan(data_subset)] = 0
                # Compute weighted sum across spatial dimensions
                weighted_values = np.sum(data_subset * weight, axis=(1, 2))
                result_array[idx, :] = weighted_values
            else:
                data_subset = raster_data[row_start:row_stop, col_start:col_stop]
                # Handle masked arrays - fill masked values with 0
                if np.ma.is_masked(data_subset):
                    data_subset = np.ma.filled(data_subset, 0)
                data_subset[np.isnan(data_subset)] = 0
                # Compute weighted sum
                weighted_value = np.sum(data_subset * weight)
                result_array[idx] = weighted_value

    # Create output DataFrame
    print("Creating output DataFrame...")
    geoid_list = df_weights[id_col].tolist()

    if is_timeseries:
        if long_format:
            # Long format: rows = geoid x time combinations
            # Create a DataFrame in wide format first, then melt it
            df_wide = pd.DataFrame(result_array.T, columns=geoid_list, index=time_index)
            df_wide.index.name = "time"
            df_output = df_wide.reset_index().melt(
                id_vars=["time"], var_name=id_col, value_name="value"
            )
        else:
            # Wide format: rows = time, columns = geometry IDs
            df_output = pd.DataFrame(
                result_array.T, columns=geoid_list, index=time_index
            )
    else:
        # Single-time data: rows = geometry IDs, single value column
        df_output = pd.DataFrame({id_col: geoid_list, "value": result_array})

    # Save to file
    print(f"Saving results to {output_path}...")
    if output_format == "csv":
        df_output.to_csv(output_path, index=not long_format if is_timeseries else False)
    else:
        df_output.to_parquet(
            output_path, index=not long_format if is_timeseries else False
        )

    print(f"Done! Results saved to: {output_path}")
    print(f"Processed {num_geoms} geometries")
    if is_timeseries:
        print(f"Time steps: {num_times}")
