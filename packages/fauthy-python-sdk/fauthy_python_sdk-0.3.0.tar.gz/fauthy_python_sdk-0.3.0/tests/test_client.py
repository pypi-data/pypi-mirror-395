"""
Test the SDK.
"""

from unittest.mock import Mock

import pytest
import requests

from fauthy_sdk.client import FauthyClient


def test_client_initialization(mock_session):
    """Test client initialization with credentials."""
    client = FauthyClient(client_id="test_id", client_secret="test_secret")

    assert client.client_id == "test_id"
    assert client.client_secret == "test_secret"
    assert mock_session.headers["X-Client-ID"] == "test_id"
    assert mock_session.headers["X-Client-Secret"] == "test_secret"
    assert mock_session.headers["Content-Type"] == "application/json"
    assert mock_session.headers["Accept"] == "application/json"


def test_base_url(client):
    """Test that the base URL is correctly set."""
    assert client.BASE_URL == "https://api.fauthy.com/v1/management"


def test_get_request(mock_session, client):
    """Test GET request functionality."""
    # Setup mock response
    mock_response = Mock()
    mock_response.json.return_value = {"data": "test"}
    mock_session.request.return_value = mock_response

    # Make request
    response = client.get("test/endpoint", params={"key": "value"})

    # Verify request was made correctly
    mock_session.request.assert_called_once_with(
        method="GET",
        url="https://api.fauthy.com/v1/management/test/endpoint",
        json=None,
        params={"key": "value"},
        timeout=(5, 30),
    )
    assert response == mock_response


def test_post_request(mock_session, client):
    """Test POST request functionality."""
    # Setup mock response
    mock_response = Mock()
    mock_response.json.return_value = {"data": "test"}
    mock_session.request.return_value = mock_response

    # Make request
    data = {"key": "value"}
    response = client.post("test/endpoint", data=data)

    # Verify request was made correctly
    mock_session.request.assert_called_once_with(
        method="POST",
        url="https://api.fauthy.com/v1/management/test/endpoint",
        json=data,
        params=None,
        timeout=(5, 30),
    )
    assert response == mock_response


def test_put_request(mock_session, client):
    """Test PUT request functionality."""
    # Setup mock response
    mock_response = Mock()
    mock_response.json.return_value = {"data": "test"}
    mock_session.request.return_value = mock_response

    # Make request
    data = {"key": "value"}
    response = client.put("test/endpoint", data=data)

    # Verify request was made correctly
    mock_session.request.assert_called_once_with(
        method="PUT",
        url="https://api.fauthy.com/v1/management/test/endpoint",
        json=data,
        params=None,
        timeout=(5, 30),
    )
    assert response == mock_response


def test_delete_request(mock_session, client):
    """Test DELETE request functionality."""
    # Setup mock response
    mock_response = Mock()
    mock_response.json.return_value = {"data": "test"}
    mock_session.request.return_value = mock_response

    # Make request
    response = client.delete("test/endpoint")

    # Verify request was made correctly
    mock_session.request.assert_called_once_with(
        method="DELETE",
        url="https://api.fauthy.com/v1/management/test/endpoint",
        json=None,
        params=None,
        timeout=(5, 30),
    )
    assert response == mock_response


def test_request_error_handling(mock_session, client):
    """Test error handling for failed requests."""
    # Setup mock to raise an exception
    mock_session.request.side_effect = requests.exceptions.RequestException(
        "Test error"
    )

    # Verify that the exception is propagated
    with pytest.raises(requests.exceptions.RequestException) as exc_info:
        client.get("test/endpoint")

    assert str(exc_info.value) == "Test error"


def test_endpoint_url_construction(mock_session, client):
    """Test that endpoint URLs are constructed correctly."""
    # Setup mock response
    mock_response = Mock()
    mock_session.request.return_value = mock_response

    # Test with different endpoint formats
    test_cases = [
        ("endpoint", "https://api.fauthy.com/v1/management/endpoint"),
        ("/endpoint", "https://api.fauthy.com/v1/management/endpoint"),
        ("endpoint/", "https://api.fauthy.com/v1/management/endpoint/"),
        ("/endpoint/", "https://api.fauthy.com/v1/management/endpoint/"),
    ]

    for endpoint, expected_url in test_cases:
        client.get(endpoint)
        mock_session.request.assert_called_with(
            method="GET", url=expected_url, json=None, params=None, timeout=(5, 30)
        )
