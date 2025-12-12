"""
Fauthy SDK Client

This module provides a client for interacting with the Fauthy API.
"""

import logging
from typing import Any, Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from fauthy_sdk.management import ManagementMixin

logger = logging.getLogger(__name__)


class FauthyClient(ManagementMixin):
    """Client for interacting with the Fauthy API."""

    BASE_URL = "https://api-v2.fauthy.com/management"

    def __init__(self, client_id: str, client_secret: str):
        """
        Initialize the Fauthy client.

        Args:
            client_id (str): Your Fauthy client ID
            client_secret (str): Your Fauthy client secret
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = requests.Session()
        self.session.headers.update(
            {
                "X-Client-ID": self.client_id,
                "X-Client-Secret": self.client_secret,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

        # Configure the session with proper timeouts, connection pooling, and retry logic
        # This helps prevent "Connection reset by peer" errors
        retry_strategy = Retry(
            total=3,  # Total number of retries
            backoff_factor=1,  # Wait 1, 2, 4 seconds between retries
            status_forcelist=[429, 500, 502, 503, 504],  # Retry on these status codes
            allowed_methods=["GET", "POST", "PUT", "DELETE"],  # Methods to retry
            raise_on_status=False,  # Don't raise on status, let requests handle it
        )
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,  # Number of connection pools to cache
            pool_maxsize=20,  # Maximum number of connections to save in the pool
            pool_block=False,  # Don't block if pool is full, raise exception instead
        )

        # Mount the adapter to the session
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """
        Make an HTTP request to the Fauthy API.

        This method includes timeout configuration to prevent requests from hanging
        indefinitely and helps with connection resets.

        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE)
            endpoint (str): API endpoint to call
            data (Optional[Dict[str, Any]]): Request body data
            params (Optional[Dict[str, Any]]): URL parameters

        Returns:
            requests.Response: The API response

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        timeout = (5, 30)  # (connect timeout, read timeout) in seconds

        try:
            response = self.session.request(
                method=method, url=url, json=data, params=params, timeout=timeout
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.warning(
                "Fauthy API request failed: %s %s - %s", method, endpoint, str(e)
            )
            raise

    def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """Make a GET request to the Fauthy API."""
        return self._make_request("GET", endpoint, params=params)

    def post(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """Make a POST request to the Fauthy API."""
        return self._make_request("POST", endpoint, data=data)

    def put(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """Make a PUT request to the Fauthy API."""
        return self._make_request("PUT", endpoint, data=data)

    def delete(self, endpoint: str) -> requests.Response:
        """Make a DELETE request to the Fauthy API."""
        return self._make_request("DELETE", endpoint)
