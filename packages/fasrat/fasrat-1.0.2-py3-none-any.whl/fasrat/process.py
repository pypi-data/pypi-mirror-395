import geopandas as gpd
import rasterio
import os
from tqdm import tqdm
from fasrat import constants, geometry
import pandas as pd
import pickle


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
