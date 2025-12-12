"""
FASRAT - Fast Area-weighted Spatial ReAggregation Tool

A Python package for computing area-weighted spatial reaggregation weights
between shapefile geometries and raster pixels.
"""

try:
    from ._version import __version__
except ImportError:
    # Fallback version for development installations without setuptools-scm
    __version__ = "0.0.0+unknown"

from .geometry import *
from .constants import *
from .process import compute_raster_weights

__all__ = ["compute_raster_weights", "NON_CONTIGUOUS_STATES", "__version__"]
