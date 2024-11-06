import pytest
import requests
from unittest.mock import patch
from meal_max.utils.random_utils import get_random

RANDOM_NUMBER = 0.42  # Mocked random number for consistent test results

@pytest.fixture
def mock_random_org_response(mocker):
    # Create a mock response object
    mock_response = mocker.Mock()
    # Set the response text to the mocked random number
    mock_response.text = f"{RANDOM_NUMBER}"
    mocker.patch("requests.get", return_value=mock_response)
    return mock_response

def test_get_random(mock_random_org_response):
    """Test retrieving a random number from random.org."""
    # Call get_random and check the returned value
    result = get_random()

    # Assert that the result is the mocked random number
    assert result == RANDOM_NUMBER, f"Expected random number {RANDOM_NUMBER}, but got {result}"

    # Verify that the correct URL was called
    requests.get.assert_called_once_with(
        "https://www.random.org/decimal-fractions/?num=1&dec=2&col=1&format=plain&rnd=new",
        timeout=5
    )

def test_get_random_timeout(mocker):
    """Simulate a timeout error."""
    # Mock requests.get to raise a Timeout exception
    mocker.patch("requests.get", side_effect=requests.exceptions.Timeout)

    # Expect a RuntimeError to be raised due to the timeout
    with pytest.raises(RuntimeError, match="Request to random.org timed out."):
        get_random()

def test_get_random_request_failure(mocker):
    """Simulate a general request failure."""
    # Mock requests.get to raise a generic RequestException
    mocker.patch("requests.get", side_effect=requests.exceptions.RequestException("Connection error"))

    # Expect a RuntimeError to be raised due to the request failure
    with pytest.raises(RuntimeError, match="Request to random.org failed: Connection error"):
        get_random()

def test_get_random_invalid_response(mock_random_org_response):
    """Simulate an invalid response from random.org (non-numeric)."""
    # Set the mock response text to a non-numeric string
    mock_random_org_response.text = "invalid_response"

    # Expect a ValueError to be raised due to the invalid response format
    with pytest.raises(ValueError, match="Invalid response from random.org: invalid_response"):
        get_random()
