# tests/unit/test_retry_logic.py
"""
Unit tests for retry logic in CenDatHelper.

These tests verify that the retry mechanisms for both data fetching
and geometry fetching work correctly, including:
- Status code detection
- Connection error handling
- Worker reduction and exponential backoff
- Retry limits
"""

import pytest
from unittest.mock import patch, Mock, MagicMock
import requests

from cendat import CenDatHelper


# --- Fixtures ---


@pytest.fixture
def cdh():
    """Returns a fresh CenDatHelper instance for each test."""
    return CenDatHelper()


# --- Mock Response Helpers ---


def make_mock_response(status_code, json_data=None, raise_for_status=False):
    """Creates a mock requests.Response object."""
    response = Mock()
    response.status_code = status_code
    response.json.return_value = json_data
    if raise_for_status:
        error = requests.exceptions.HTTPError()
        error.response = response
        response.raise_for_status.side_effect = error
    else:
        response.raise_for_status.return_value = None
    return response


def make_connection_error():
    """Creates a connection error with no response object."""
    error = requests.exceptions.ConnectionError("Connection aborted")
    error.response = None
    return error


# --- Tests for _get_json_from_url_with_status ---


class TestGetJsonFromUrlWithStatus:
    """Tests for _get_json_from_url_with_status method."""

    @patch("requests.get")
    def test_returns_data_and_status_on_success(self, mock_get, cdh):
        """Successful request returns (data, 200)."""
        mock_response = make_mock_response(200, json_data=[["col1"], ["val1"]])
        mock_get.return_value = mock_response

        data, status = cdh._get_json_from_url_with_status("http://test.com")

        assert data == [["col1"], ["val1"]]
        assert status == 200

    @patch("requests.get")
    def test_returns_none_with_status_on_server_error(self, mock_get, cdh):
        """Server error (500) returns (None, 500)."""
        mock_response = make_mock_response(500, raise_for_status=True)
        mock_get.return_value = mock_response
        mock_get.return_value.raise_for_status.side_effect = (
            requests.exceptions.HTTPError(response=mock_response)
        )

        data, status = cdh._get_json_from_url_with_status("http://test.com")

        assert data is None
        assert status == 500

    @patch("requests.get")
    def test_returns_none_with_429_on_rate_limit(self, mock_get, cdh):
        """Rate limit (429) returns (None, 429)."""
        mock_response = make_mock_response(429, raise_for_status=True)
        mock_get.return_value = mock_response
        mock_get.return_value.raise_for_status.side_effect = (
            requests.exceptions.HTTPError(response=mock_response)
        )

        data, status = cdh._get_json_from_url_with_status("http://test.com")

        assert data is None
        assert status == 429

    @patch("requests.get")
    def test_returns_none_none_on_connection_error(self, mock_get, cdh):
        """Connection error (BrokenPipe, OSError) returns (None, None)."""
        mock_get.side_effect = make_connection_error()

        data, status = cdh._get_json_from_url_with_status("http://test.com")

        assert data is None
        assert status is None


# --- Tests for _get_gdf_from_url_with_status ---


class TestGetGdfFromUrlWithStatus:
    """Tests for _get_gdf_from_url_with_status method."""

    @patch("requests.get")
    def test_returns_count_and_status_on_success(self, mock_get, cdh):
        """Successful count request returns (count, 200)."""
        mock_response = make_mock_response(200, json_data={"count": 42})
        mock_get.return_value = mock_response

        result, status = cdh._get_gdf_from_url_with_status(
            layer_id=1, where_clause="TEST='1'", count_only=True
        )

        assert result == 42
        assert status == 200

    @patch("requests.get")
    def test_returns_gdf_and_status_on_success(self, mock_get, cdh):
        """Successful geometry request returns (GeoDataFrame, 200)."""
        mock_response = make_mock_response(
            200,
            json_data={
                "features": [
                    {"type": "Feature", "properties": {"GEOID": "1"}, "geometry": None}
                ]
            },
        )
        mock_get.return_value = mock_response

        result, status = cdh._get_gdf_from_url_with_status(
            layer_id=1, where_clause="TEST='1'"
        )

        assert status == 200
        assert len(result) == 1
        assert "GEOID" in result.columns

    @patch("requests.get")
    def test_returns_empty_gdf_with_none_on_connection_error(self, mock_get, cdh):
        """Connection error returns (empty GeoDataFrame, None)."""
        mock_get.side_effect = make_connection_error()

        result, status = cdh._get_gdf_from_url_with_status(
            layer_id=1, where_clause="TEST='1'"
        )

        assert status is None
        assert len(result) == 0  # Empty GeoDataFrame

    @patch("requests.get")
    def test_returns_zero_with_none_on_connection_error_count_only(self, mock_get, cdh):
        """Connection error with count_only returns (0, None)."""
        mock_get.side_effect = make_connection_error()

        result, status = cdh._get_gdf_from_url_with_status(
            layer_id=1, where_clause="TEST='1'", count_only=True
        )

        assert status is None
        assert result == 0


# --- Tests for _data_fetching retry behavior ---


class TestDataFetchingRetry:
    """Tests for _data_fetching retry behavior."""

    @patch.object(CenDatHelper, "_get_json_from_url_with_status")
    def test_retries_on_high_failure_rate(self, mock_fetch, cdh):
        """Triggers retry when >10% of requests fail with server errors."""
        # Set up the helper with minimal required state
        cdh.params = [{"schema": None, "data": []}]

        # First call fails with None status (connection error)
        # Second call succeeds
        mock_fetch.side_effect = [
            (None, None),  # First attempt fails
            ([["col1"], ["val1"]], 200),  # Retry succeeds
        ]

        tasks = [("http://test.com", {"get": "TEST"}, {"param_index": 0})]

        with patch("time.sleep"):  # Don't actually sleep
            cdh._data_fetching(
                tasks=tasks, max_workers=1, auto_retry=True, max_retries=3
            )

        # Should have called twice (initial + 1 retry)
        assert mock_fetch.call_count == 2

    @patch.object(CenDatHelper, "_get_json_from_url_with_status")
    def test_respects_max_retries_limit(self, mock_fetch, cdh):
        """Stops retrying after max_retries is reached."""
        cdh.params = [{"schema": None, "data": []}]

        # Always fail with connection error
        mock_fetch.return_value = (None, None)

        tasks = [("http://test.com", {"get": "TEST"}, {"param_index": 0})]

        with patch("time.sleep"):
            cdh._data_fetching(
                tasks=tasks, max_workers=1, auto_retry=True, max_retries=2
            )

        # Initial + 2 retries = 3 calls
        assert mock_fetch.call_count == 3

    @patch.object(CenDatHelper, "_get_json_from_url_with_status")
    def test_does_not_retry_when_disabled(self, mock_fetch, cdh):
        """Does not retry when auto_retry=False."""
        cdh.params = [{"schema": None, "data": []}]

        mock_fetch.return_value = (None, None)

        tasks = [("http://test.com", {"get": "TEST"}, {"param_index": 0})]

        cdh._data_fetching(tasks=tasks, max_workers=1, auto_retry=False)

        # Only one call, no retries
        assert mock_fetch.call_count == 1


# --- Tests for _geometry_fetching retry behavior ---


class TestGeometryFetchingRetry:
    """Tests for _geometry_fetching retry behavior."""

    @patch.object(CenDatHelper, "_get_gdf_from_url_with_status")
    def test_preflight_retries_on_connection_error(self, mock_fetch, cdh):
        """Pre-flight count requests retry on connection errors."""
        cdh.params = [{}]

        # First fails (connection error), second succeeds with count=0
        mock_fetch.side_effect = [
            (0, None),  # Connection error
            (0, 200),  # Retry succeeds, no geometries
        ]

        tasks = [
            {
                "param_index": 0,
                "layer_id": 1,
                "where_clause": "TEST='1'",
                "map_server": "test",
            }
        ]

        with patch("time.sleep"):
            cdh._geometry_fetching(
                tasks=tasks, max_workers=1, auto_retry=True, max_retries=3
            )

        # Should have retried the pre-flight
        assert mock_fetch.call_count == 2

    @patch.object(CenDatHelper, "_get_gdf_from_url_with_status")
    def test_geometry_fetch_respects_max_retries(self, mock_fetch, cdh):
        """Geometry fetching stops after max_retries."""
        import geopandas as gpd

        cdh.params = [{}]

        # Always fail
        mock_fetch.return_value = (0, None)

        tasks = [
            {
                "param_index": 0,
                "layer_id": 1,
                "where_clause": "TEST='1'",
                "map_server": "test",
            }
        ]

        with patch("time.sleep"):
            cdh._geometry_fetching(
                tasks=tasks, max_workers=1, auto_retry=True, max_retries=2
            )

        # 1 initial + 2 retries = 3
        assert mock_fetch.call_count == 3
