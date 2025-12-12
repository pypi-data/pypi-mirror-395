import geopandas as gpd
import rasterio
import os
from tqdm import tqdm
from fasrat import constants, geometry
import pandas as pd
import pickle
import numpy as np


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
    raster_path: str,
    output_path: str,
    geoid_column: str = None,
    output_format: str = "csv",
    long_format: bool = False,
) -> None:
    """
    Apply pre-computed raster weights to raster data for weighted spatial averaging.

    This function takes a weights file (generated by compute_raster_weights) and a raster file,
    then computes weighted averages for each geometry. Supports both time-series (multi-band) and single-time (single-band) data.

    Args:
        weights_path: Path to the weights parquet file (output from compute_raster_weights)
        raster_path: Path to the raster file (supports any format readable by rasterio)
        output_path: Path for the output file (CSV or parquet)
        geoid_column: Name of the column containing geometry IDs. If None, auto-detects (tries GEOID10, GEOID, GEO_ID, ID).
        output_format: Output format, either 'csv' or 'parquet'. Default is 'csv'.
        long_format: If True, time-series data is output in long format (rows = geoid x time combinations).
                     If False (default), time-series data is in wide format (rows = time, columns = geoids).
                     Has no effect on single-time data.

    Returns:
        None. Results are saved to the specified output file.

    Raises:
        FileNotFoundError: If weights file or raster file cannot be found
        ValueError: If geometry ID column cannot be determined
    """
    # Validate inputs
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"Weights file not found: {weights_path}")

    if not os.path.exists(raster_path):
        raise FileNotFoundError(f"Raster file not found: {raster_path}")

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

    # Open raster file using rasterio
    print("Opening raster file...")
    with rasterio.open(raster_path, "r") as src:
        # Read the raster data (masked=True returns a 3D masked array: (bands, rows, cols))
        print("Reading raster data...")
        raster_data = src.read(masked=True)

        # Determine if time-series or single-time data
        data_shape = raster_data.shape
        print(f"Data shape: {data_shape}")

        # rasterio always returns 3D: (bands, rows, cols)
        # If there's 1 band, it's single-time data
        # If there are multiple bands, each band represents a time step
        num_bands = data_shape[0]

        if num_bands == 1:
            # Single-time data (1 band)
            is_timeseries = False
            print("Detected single-time data (1 band)")
            # Squeeze to get 2D array for easier processing
            raster_data = raster_data[0, :, :]
        else:
            # Time-series data (multiple bands)
            is_timeseries = True
            num_times = num_bands
            print(f"Detected time-series data with {num_times} bands/time steps")
            # Use integer index for time since rasterio doesn't have time metadata
            time_index = np.arange(num_times)

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

                # Create mask for invalid values (masked or NaN)
                # Check each time slice for masked/NaN values
                invalid_mask = np.zeros(data_subset.shape[1:], dtype=bool)
                if np.ma.is_masked(data_subset):
                    # Combine masks across all time slices
                    invalid_mask |= np.any(data_subset.mask, axis=0)
                    data_subset = np.ma.filled(data_subset, np.nan)

                # Add NaN locations to the mask (check across time dimension)
                invalid_mask |= np.any(np.isnan(data_subset), axis=0)

                # Adjust weights: set invalid locations to 0
                adjusted_weight = weight.copy()
                adjusted_weight[invalid_mask] = 0

                # Renormalize weights to sum to 1
                weight_sum = np.sum(adjusted_weight)
                if weight_sum > 0:
                    adjusted_weight = adjusted_weight / weight_sum
                    # Set data to 0 where invalid (for clean computation)
                    data_subset = np.nan_to_num(data_subset, nan=0.0)
                    # Compute weighted sum across spatial dimensions
                    weighted_values = np.sum(data_subset * adjusted_weight, axis=(1, 2))
                    result_array[idx, :] = weighted_values
                else:
                    # All weights are zero (all data invalid)
                    result_array[idx, :] = np.nan
            else:
                data_subset = raster_data[row_start:row_stop, col_start:col_stop]

                # Create mask for invalid values (masked or NaN)
                invalid_mask = np.zeros(data_subset.shape, dtype=bool)
                if np.ma.is_masked(data_subset):
                    invalid_mask |= data_subset.mask
                    data_subset = np.ma.filled(data_subset, np.nan)

                # Add NaN locations to the mask
                invalid_mask |= np.isnan(data_subset)

                # Adjust weights: set invalid locations to 0
                adjusted_weight = weight.copy()
                adjusted_weight[invalid_mask] = 0

                # Renormalize weights to sum to 1
                weight_sum = np.sum(adjusted_weight)
                if weight_sum > 0:
                    adjusted_weight = adjusted_weight / weight_sum
                    # Set data to 0 where invalid (for clean computation)
                    data_subset = np.nan_to_num(data_subset, nan=0.0)
                    # Compute weighted sum
                    weighted_value = np.sum(data_subset * adjusted_weight)
                    result_array[idx] = weighted_value
                else:
                    # All weights are zero (all data invalid)
                    result_array[idx] = np.nan

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
