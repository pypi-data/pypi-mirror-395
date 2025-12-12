#!/usr/bin/env python3
"""
FASRAT CLI - Fast Area-weighted Spatial ReAggregation Tool

Command-line interface for computing area-weighted spatial reaggregation weights
between shapefile geometries and raster pixels.
"""
import click
import sys
from fasrat.process import compute_raster_weights


@click.command()
@click.option(
    "--shapefile",
    "-s",
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True),
    help="Path to the shapefile (.shp file)",
)
@click.option(
    "--raster",
    "-r",
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True),
    help="Path to the sample raster file (.nc format)",
)
@click.option(
    "--output",
    "-o",
    required=True,
    type=click.Path(file_okay=True, dir_okay=False, resolve_path=True),
    help="Full path for the output HDF5 file (e.g., /path/to/output.h5)",
)
@click.option(
    "--crs",
    "-c",
    default=None,
    type=str,
    help="Optional CRS string (e.g., 'EPSG:4326') to project the shapefile to. If not provided, uses the raster's CRS.",
)
def main(shapefile, raster, output, crs):
    """
    FASRAT - Fast Area-weighted Spatial ReAggregation Tool
    
    Compute area-weighted intersection weights between shapefile geometries
    (e.g., census tracts, counties) and raster pixels. The output can be used
    to aggregate raster data to the polygon level.
    
    Example:
        fasrat --shapefile ./shapefiles/us_tract_2010/US_tract_2010.shp \\
               --raster ./data/tmmx_2010.nc \\
               --output ./output/tract_weights.h5
        
        # With custom CRS:
        fasrat --shapefile ./shapefiles/us_tract_2010/US_tract_2010.shp \\
               --raster ./data/tmmx_2010.nc \\
               --output ./output/tract_weights.h5 \\
               --crs EPSG:4326
    """
    click.echo("=" * 60)
    click.echo("FASRAT - Fast Area-weighted Spatial ReAggregation Tool")
    click.echo("=" * 60)
    click.echo(f"Shapefile: {shapefile}")
    click.echo(f"Raster file: {raster}")
    click.echo(f"Output file: {output}")
    if crs:
        click.echo(f"Target CRS: {crs}")
    click.echo("=" * 60)

    try:
        compute_raster_weights(shapefile, raster, output, crs)
        click.echo("=" * 60)
        click.secho("✓ Processing completed successfully!", fg="green", bold=True)
        click.echo("=" * 60)
    except Exception as e:
        click.echo("=" * 60)
        click.secho(f"✗ Error: {str(e)}", fg="red", bold=True, err=True)
        click.echo("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
