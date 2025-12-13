# tests/unit/test_response.py
"""
Unit tests for CenDatResponse class.

These tests verify edge cases and additional functionality of the
CenDatResponse class including:
- GeoDataFrame conversion with different join strategies
- Destring functionality for numeric conversion
- Empty response handling
- __repr__ and __getitem__ methods
"""

import pytest
from unittest.mock import Mock, patch
import numpy as np
import geopandas as gpd
from shapely.geometry import Point

from cendat import CenDatResponse


# --- Fixtures ---


@pytest.fixture
def empty_response():
    """Returns a CenDatResponse with no data."""
    return CenDatResponse([])


@pytest.fixture
def single_result_response():
    """Returns a CenDatResponse with one result."""
    return CenDatResponse(
        [
            {
                "product": "Test Product",
                "vintage": [2023],
                "sumlev": "150",
                "desc": "block group",
                "schema": ["GEO_ID", "VALUE"],
                "data": [["1500000US010010001001", "100"], ["1500000US010010001002", "200"]],
                "geometry": gpd.GeoDataFrame(),
            }
        ]
    )


@pytest.fixture
def response_with_geometry():
    """Returns a CenDatResponse with geometry data."""
    gdf = gpd.GeoDataFrame(
        {
            "GEOID": ["010010001001", "010010001002"],
            "NAME": ["Block 1", "Block 2"],
            "geometry": [Point(0, 0), Point(1, 1)],
        }
    )
    return CenDatResponse(
        [
            {
                "product": "Test Product",
                "vintage": [2023],
                "sumlev": "150",
                "desc": "block group",
                "schema": ["GEO_ID", "VALUE"],
                "names": ["VALUE"],  # Required for destring to work on VALUE column
                "data": [
                    ["1500000US010010001001", "100"],
                    ["1500000US010010001002", "200"],
                ],
                "geometry": gdf,
            }
        ]
    )


@pytest.fixture
def response_with_numeric_strings():
    """Returns a CenDatResponse with string numbers for destring testing.
    
    Note: destring only works on columns identified in 'names' list.
    """
    return CenDatResponse(
        [
            {
                "product": "Test Product",
                "vintage": [2023],
                "sumlev": "040",
                "desc": "state",
                "schema": ["GEO_ID", "POP", "INCOME"],
                "names": ["POP", "INCOME"],  # Required for destring to work
                "data": [
                    ["0400000US01", "12345", "50000.50"],
                    ["0400000US02", "67890", "75000.25"],
                ],
                "geometry": gpd.GeoDataFrame(),
            }
        ]
    )


# --- Tests for empty responses ---


class TestEmptyResponse:
    """Tests for handling empty responses."""

    def test_to_polars_returns_empty_list(self, empty_response):
        """to_polars returns empty list when no data."""
        result = empty_response.to_polars()
        assert result == []

    def test_to_polars_concat_returns_none_or_empty(self, empty_response):
        """to_polars with concat handles empty gracefully."""
        result = empty_response.to_polars(concat=True)
        # Should return None or empty list
        assert result is None or result == []

    def test_to_pandas_returns_empty_list(self, empty_response):
        """to_pandas returns empty list when no data."""
        result = empty_response.to_pandas()
        assert result == []

    def test_repr_shows_zero_results(self, empty_response):
        """__repr__ shows 0 results for empty response."""
        repr_str = repr(empty_response)
        assert "0" in repr_str or "empty" in repr_str.lower()


# --- Tests for __repr__ and __getitem__ ---


class TestDunderMethods:
    """Tests for __repr__ and __getitem__ methods."""

    def test_repr_contains_result_count(self, single_result_response):
        """__repr__ shows the number of results."""
        repr_str = repr(single_result_response)
        assert "1" in repr_str  # Should mention 1 result

    def test_getitem_returns_correct_dict(self, single_result_response):
        """__getitem__ returns the correct result dictionary."""
        result = single_result_response[0]
        assert isinstance(result, dict)
        assert result["product"] == "Test Product"
        assert result["vintage"] == [2023]

    def test_getitem_raises_on_invalid_index(self, single_result_response):
        """__getitem__ raises IndexError for invalid index."""
        with pytest.raises(IndexError):
            _ = single_result_response[99]


# --- Tests for destring functionality ---


class TestDestringFunctionality:
    """Tests for destring parameter in to_polars and to_pandas."""

    def test_to_polars_destring_converts_numbers(self, response_with_numeric_strings):
        """to_polars with destring=True converts string numbers."""
        dfs = response_with_numeric_strings.to_polars(destring=True)
        df = dfs[0]

        # Check that numeric columns are not strings
        # (exact type depends on polars inference)
        pop_col = df["POP"]
        assert pop_col[0] != "12345"  # Should be numeric, not string

    def test_to_pandas_destring_converts_numbers(self, response_with_numeric_strings):
        """to_pandas with destring=True converts string numbers."""
        dfs = response_with_numeric_strings.to_pandas(destring=True)
        df = dfs[0]

        # Check first value is numeric (numpy types)
        pop_val = df["POP"].iloc[0]
        assert isinstance(pop_val, (int, float, np.number))
        assert pop_val == 12345


# --- Tests for to_gpd ---


class TestToGpd:
    """Tests for to_gpd conversion."""

    def test_to_gpd_left_join_includes_all_data(self, response_with_geometry):
        """to_gpd with left join includes all data rows."""
        gdf = response_with_geometry.to_gpd(join_strategy="left")
        assert len(gdf) == 2
        assert "VALUE" in gdf.columns
        assert "geometry" in gdf.columns

    def test_to_gpd_inner_join_only_matches(self, response_with_geometry):
        """to_gpd with inner join only includes matching rows."""
        gdf = response_with_geometry.to_gpd(join_strategy="inner")
        # All rows should match since our fixture has matching GEOIDs
        assert len(gdf) == 2

    def test_to_gpd_with_missing_geometry_returns_empty(self, single_result_response):
        """to_gpd with empty geometry returns empty or data-only."""
        gdf = single_result_response.to_gpd(join_strategy="inner")
        # Inner join with no geometry matches should be empty
        assert len(gdf) == 0

    def test_to_gpd_with_destring(self, response_with_geometry):
        """to_gpd with destring=True converts numeric strings."""
        gdf = response_with_geometry.to_gpd(destring=True)
        val = gdf["VALUE"].iloc[0]
        assert isinstance(val, (int, float, np.number))
