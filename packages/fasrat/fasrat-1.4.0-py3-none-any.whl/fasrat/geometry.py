import numpy as np
from typing import Union, List
import rasterio
from rasterio.windows import Window
from shapely.geometry import box
import pandas as pd


def get_larger_bounds(coord: list, raster_size: list, start_point: bool = True) -> list:
    """
    computes a +1 -1 bounding box for a given coordinate and raster size limit

    Args:
        coord (list): x y coordinate of the start point or end point
        raster_size (list): height x width of the raster (or shape)

    Returns:
        tuple: _description_
    """
    # check if the coordinate is already at the edge
    if start_point:
        coord = [max(0, c) for c in coord]

    else:
        coord = [min(c, r) for c, r in zip(coord, raster_size)]

    new_coord = []
    if start_point:
        for c in coord:
            if c == 0:
                new_c = c
            else:
                new_c = c - 1
            new_coord.append(new_c)
    else:
        for i, c in enumerate(coord):
            if c == raster_size[i]:
                new_c = c
            else:
                new_c = c + 1
            new_coord.append(new_c)
    return new_coord


def convert_bbox_coord_to_raster_index(
    bounding_box: tuple, raster_src: rasterio.io.DatasetReader
) -> Union[None, List[List[int]]]:

    row_start, col_start = raster_src.index(bounding_box[0], bounding_box[3])
    row_stop, col_stop = raster_src.index(bounding_box[2], bounding_box[1])
    row_start, row_stop = sorted([row_start, row_stop])
    col_start, col_stop = sorted([col_start, col_stop])

    row_start, col_start = get_larger_bounds(
        [row_start, col_start], raster_src.shape, start_point=True
    )
    row_stop, col_stop = get_larger_bounds(
        [row_stop, col_stop], raster_src.shape, start_point=False
    )
    # check if row start - row stop is above zero
    row_len = row_stop - row_start
    col_len = col_stop - col_start
    if row_len <= 0 or col_len <= 0:
        return None

    coords = [[row_start, row_stop], [col_start, col_stop]]
    return coords


def get_weight_matrix(row: pd.Series, src: rasterio.io.DatasetReader):
    # Get the reference geometry
    ref_geom = row["geometry"]
    bbox = row["raster_bbox_coords"]
    ref_area = row["area"]
    if bbox is None:
        return None
    try:
        # get window and tile
        window = Window.from_slices(*bbox)
        tile = src.read(1, window=window)
        tile_mask = src.dataset_mask(window=window)
        tile_mask = tile_mask == 0  # True = no data (0) False = data (255)
        # transforms the origin of the raster in the reference of the tile
        tile_affine = rasterio.windows.transform(window, src.transform)
        if tile_mask.all():
            print("All areas are masked (no observations in the raster)")
            return None

        # get ref_area
        # Initialize an array to store areas of intersection
        intersection_weight_matrix = np.zeros(tile.shape, dtype=float)

        # Loop through each pixel in the tile
        for r in range(tile.shape[0]):
            for c in range(tile.shape[1]):
                # Get pixel's x and y coordinates
                x, y = tile_affine * (c, r)

                if tile_mask[r, c]:
                    intersection_weight_matrix[r, c] = 0.0
                    continue

                # Create a Polygon geometry for the pixel
                pixel_geom = box(x, y, x + src.res[0], y - src.res[1])

                # Calculate the intersection between the pixel and the reference geometry
                intersection_geom = ref_geom.intersection(pixel_geom)

                # Calculate and store the area of the intersection
                intersection_weight_matrix[r, c] = intersection_geom.area / ref_area

        # renormalize the weight matrix
        sum_weights = intersection_weight_matrix.sum()
        if sum_weights == 0:
            return None
        intersection_weight_matrix = intersection_weight_matrix / sum_weights
        return intersection_weight_matrix
    except Exception as e:
        print(e)
        return None
