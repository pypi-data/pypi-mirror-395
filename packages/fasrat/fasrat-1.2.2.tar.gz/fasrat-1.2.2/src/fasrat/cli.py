#!/usr/bin/env python3
"""
FASRAT CLI - Fast Area-weighted Spatial ReAggregation Tool

Command-line interface for computing area-weighted spatial reaggregation weights
between shapefile geometries and raster pixels, and applying them to NetCDF data.
"""
import click
import sys
from fasrat.process import compute_raster_weights, apply_raster_weights


@click.group()
def main():
    """
    FASRAT - Fast Area-weighted Spatial ReAggregation Tool

    A tool for spatial data aggregation with two main commands:

    - weights: Compute area-weighted intersection weights between geometries and rasters

    - convert: Apply pre-computed weights to NetCDF data for spatial averaging
    """
    pass


@main.command()
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
    help="Full path for the output parquet file (e.g., /path/to/output.parquet)",
)
@click.option(
    "--crs",
    "-c",
    default=None,
    type=str,
    help="Optional CRS string (e.g., 'EPSG:4326') to project the shapefile to. If not provided, uses the raster's CRS.",
)
def weights(shapefile, raster, output, crs):
    """
    Compute area-weighted intersection weights between shapefile geometries
    (e.g., census tracts, counties) and raster pixels.
    
    The output weights file can be used with the 'convert' command to aggregate
    raster data to the polygon level.
    
    Example:
    
        fasrat weights --shapefile ./shapefiles/us_tract_2010.shp \\
                       --raster ./data/tmmx_2010.nc \\
                       --output ./output/tract_weights.parquet
        
        # With custom CRS:
        
        fasrat weights --shapefile ./shapefiles/us_tract_2010.shp \\
                       --raster ./data/tmmx_2010.nc \\
                       --output ./output/tract_weights.parquet \\
                       --crs EPSG:4326
    """
    click.echo("=" * 60)
    click.echo("FASRAT - Computing Raster Weights")
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
        click.secho(
            "✓ Weight computation completed successfully!", fg="green", bold=True
        )
        click.echo("=" * 60)
    except Exception as e:
        click.echo("=" * 60)
        click.secho(f"✗ Error: {str(e)}", fg="red", bold=True, err=True)
        click.echo("=" * 60)
        sys.exit(1)


@main.command()
@click.option(
    "--weights",
    "-w",
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True),
    help="Path to the weights parquet file (output from 'weights' command)",
)
@click.option(
    "--netcdf",
    "-n",
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True),
    help="Path to the NetCDF file containing raster data",
)
@click.option(
    "--output",
    "-o",
    required=True,
    type=click.Path(file_okay=True, dir_okay=False, resolve_path=True),
    help="Path for the output file (CSV or parquet)",
)
@click.option(
    "--variable",
    "-v",
    default=None,
    type=str,
    help="NetCDF variable name to process. If not specified, auto-detects when only one variable exists.",
)
@click.option(
    "--geoid-col",
    "-g",
    default=None,
    type=str,
    help="Geometry ID column name in weights file. If not specified, auto-detects (tries GEOID10, GEOID, GEO_ID, ID).",
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["csv", "parquet"], case_sensitive=False),
    default="csv",
    help="Output format. Default is 'csv'.",
)
@click.option(
    "--long",
    "-l",
    is_flag=True,
    default=False,
    help="Output time-series data in long format (rows = geoid x time). Default is wide format (rows = time, columns = geoids).",
)
def convert(weights, netcdf, output, variable, geoid_col, format, long):
    """
    Apply pre-computed raster weights to NetCDF data for weighted spatial averaging.
    
    This command takes a weights file (from the 'weights' command) and a NetCDF raster file,
    then computes weighted averages for each geometry. Supports both time-series (daily/monthly)
    and single-time (annual) data.
    
    Example:
    
        fasrat convert --weights ./output/tract_weights.parquet \\
                       --netcdf ./data/pm25_2010.nc \\
                       --output ./output/pm25_tract_2010.csv
        
        # With long format for time-series:
        
        fasrat convert --weights ./output/tract_weights.parquet \\
                       --netcdf ./data/pm25_2010.nc \\
                       --output ./output/pm25_tract_2010.csv \\
                       --long
        
        # With specific variable and parquet output:
        
        fasrat convert --weights ./output/tract_weights.parquet \\
                       --netcdf ./data/pm25_2010.nc \\
                       --output ./output/pm25_tract_2010.parquet \\
                       --variable PM25 \\
                       --format parquet
    """
    click.echo("=" * 60)
    click.echo("FASRAT - Converting Raster to Weighted Averages")
    click.echo("=" * 60)
    click.echo(f"Weights file: {weights}")
    click.echo(f"NetCDF file: {netcdf}")
    click.echo(f"Output file: {output}")
    if variable:
        click.echo(f"NetCDF variable: {variable}")
    if geoid_col:
        click.echo(f"Geometry ID column: {geoid_col}")
    click.echo(f"Output format: {format}")
    click.echo(f"Time-series format: {'long' if long else 'wide'}")
    click.echo("=" * 60)

    try:
        apply_raster_weights(weights, netcdf, output, variable, geoid_col, format, long)
        click.echo("=" * 60)
        click.secho("✓ Conversion completed successfully!", fg="green", bold=True)
        click.echo("=" * 60)
    except Exception as e:
        click.echo("=" * 60)
        click.secho(f"✗ Error: {str(e)}", fg="red", bold=True, err=True)
        click.echo("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
