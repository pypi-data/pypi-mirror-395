"""Basic tests for FASRAT package."""

import pytest
import fasrat
from fasrat.geometry import get_larger_bounds, convert_bbox_coord_to_raster_index
from fasrat.constants import NON_CONTIGUOUS_STATES


def test_version():
    """Test that the package has a version."""
    assert hasattr(fasrat, "__version__")
    assert isinstance(fasrat.__version__, str)
    assert len(fasrat.__version__) > 0


def test_imports():
    """Test that main functions can be imported."""
    from fasrat import compute_raster_weights

    assert callable(compute_raster_weights)


def test_constants():
    """Test that constants are defined correctly."""
    assert isinstance(NON_CONTIGUOUS_STATES, list)
    assert len(NON_CONTIGUOUS_STATES) > 0
    # Check some known non-contiguous states
    assert "02" in NON_CONTIGUOUS_STATES
    assert "15" in NON_CONTIGUOUS_STATES


class TestGeometry:
    """Tests for geometry module functions."""

    def test_get_larger_bounds_start_point_at_edge(self):
        """Test get_larger_bounds with start point at edge (0,0)."""
        coord = [0, 0]
        raster_size = [100, 100]
        result = get_larger_bounds(coord, raster_size, start_point=True)
        assert result == [0, 0], "Should stay at edge when already at 0"

    def test_get_larger_bounds_start_point_interior(self):
        """Test get_larger_bounds with start point in interior."""
        coord = [10, 20]
        raster_size = [100, 100]
        result = get_larger_bounds(coord, raster_size, start_point=True)
        assert result == [9, 19], "Should subtract 1 from interior coordinates"

    def test_get_larger_bounds_end_point_at_edge(self):
        """Test get_larger_bounds with end point at edge."""
        coord = [100, 100]
        raster_size = [100, 100]
        result = get_larger_bounds(coord, raster_size, start_point=False)
        assert result == [100, 100], "Should stay at edge when already at max"

    def test_get_larger_bounds_end_point_interior(self):
        """Test get_larger_bounds with end point in interior."""
        coord = [10, 20]
        raster_size = [100, 100]
        result = get_larger_bounds(coord, raster_size, start_point=False)
        assert result == [11, 21], "Should add 1 to interior coordinates"

    def test_get_larger_bounds_negative_coords(self):
        """Test get_larger_bounds with negative coordinates."""
        coord = [-5, -10]
        raster_size = [100, 100]
        result = get_larger_bounds(coord, raster_size, start_point=True)
        assert result == [0, 0], "Should clamp negative coords to 0"

    def test_get_larger_bounds_exceeding_coords(self):
        """Test get_larger_bounds with coordinates exceeding raster size."""
        coord = [150, 200]
        raster_size = [100, 100]
        result = get_larger_bounds(coord, raster_size, start_point=False)
        assert result == [100, 100], "Should clamp to max raster size"


def test_cli_import():
    """Test that CLI can be imported."""
    from fasrat.cli import main

    assert callable(main)
