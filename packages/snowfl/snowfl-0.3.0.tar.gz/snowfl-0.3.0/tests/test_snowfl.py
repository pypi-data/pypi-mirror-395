import json
from unittest.mock import patch

import pytest

from snowfl.snowfl import ApiError, FetchError, Snowfl


@pytest.fixture
def snowfl_instance():
    return Snowfl()


def test_initialize_with_valid_key(snowfl_instance):
    # Call the initialize method
    snowfl_instance.initialize()

    # Assert that the API key is set correctly
    assert snowfl_instance.api_key is not None


@patch("snowfl.snowfl.get_api_key")
def test_initialize_with_none_key(mock_get_api_key, snowfl_instance):
    # Configure the mock to return None (simulating failure to obtain an API key)
    mock_get_api_key.return_value = None

    # Use pytest to check if the ApiError exception is raised
    with pytest.raises(ApiError, match="Failed to obtain API key."):
        snowfl_instance.initialize()


@patch("requests.get")
def test_parse_with_valid_response(mock_get, snowfl_instance):
    # Configure the mock to return a valid response
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = json.dumps({"key": "value"})

    # Call the parse method
    result = snowfl_instance.parse("query")

    # Assert that the result is as expected
    assert result == {"status": 200, "message": "OK", "data": {"key": "value"}}


@patch("requests.get")
def test_parse_with_invalid_response(mock_get, snowfl_instance):
    # Configure the mock to return an invalid response
    mock_get.return_value.status_code = 404

    # Use pytest to check if the FetchError exception is raised
    with pytest.raises(FetchError, match="Failed to fetch data, HTTP status: 404"):
        snowfl_instance.parse("query")


def test_parse_with_short_query(snowfl_instance):
    # Use pytest to check if the FetchError exception is raised
    with pytest.raises(FetchError, match="Query should be of length >= 3"):
        snowfl_instance.parse("q")


def test_str(snowfl_instance):
    # Call the __str__ method and assert that it returns the correct string
    assert str(snowfl_instance) == "Snowfl API Wrapper"


def test_repr(snowfl_instance):
    # Call the __repr__ method and assert that it returns the correct string
    assert repr(snowfl_instance) == "Snowfl()"
