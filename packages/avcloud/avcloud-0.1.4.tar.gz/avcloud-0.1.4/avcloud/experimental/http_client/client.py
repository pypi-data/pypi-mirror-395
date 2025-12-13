"""Simple HTTP client using httpx."""

import logging
import os
from typing import Any, Dict, Optional, Union

import httpx

from avcloud import __version__

logger = logging.getLogger(__name__)

DEFAULT_HEADERS = {"x-uber-client-version": __version__, "x-uber-client-name": "avcloud"}


class HTTPClient:
    """A simple HTTP client wrapper around httpx."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        headers: Optional[Dict[str, str]] = None,
        follow_redirects: bool = True,
    ):
        """
        Initialize the HTTP client.

        Args:
            base_url: Base URL for all requests
            timeout: Request timeout in seconds
            headers: Default headers to include in all requests
            follow_redirects: Whether to follow redirects
        """
        self.base_url = base_url.rstrip("/") if base_url else None
        self.timeout = timeout
        self.default_headers = self._compile_headers(headers)
        self.follow_redirects = follow_redirects

    def _compile_headers(
        self, additional_headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, str]:
        default_headers = DEFAULT_HEADERS.copy()
        if additional_headers:
            default_headers.update(additional_headers)
        return default_headers

    def _get_client(self) -> httpx.Client:
        """Create and return an httpx client with configured settings."""
        return httpx.Client(timeout=self.timeout, follow_redirects=self.follow_redirects)

    def _build_url(self, endpoint: str) -> str:
        """Build the full URL from base_url and endpoint."""
        if self.base_url:
            return f"{self.base_url}/{endpoint.lstrip('/')}"
        return endpoint

    def _make_request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """
        Make an HTTP request.

        Args:
            method: HTTP method (GET, POST, etc.)
            url: Request URL
            **kwargs: Additional arguments to pass to httpx

        Returns:
            httpx.Response object

        Raises:
            httpx.HTTPError: If the request fails
        """
        # Merge default headers with request headers
        request_headers = kwargs.get("headers") or {}
        headers = {**self.default_headers, **request_headers}
        kwargs["headers"] = headers

        with self._get_client() as client:
            logger.debug(f"Making {method} request to {url}")
            response = client.request(method, url, **kwargs)
            response.raise_for_status()
            return response

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        """
        Make a GET request.

        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Request headers

        Returns:
            httpx.Response object
        """
        url = self._build_url(endpoint)
        return self._make_request("GET", url, params=params, headers=headers)

    def post(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        """
        Make a POST request.

        Args:
            endpoint: API endpoint
            data: Form data or raw data
            json: JSON data
            headers: Request headers

        Returns:
            httpx.Response object
        """
        url = self._build_url(endpoint)
        return self._make_request("POST", url, data=data, json=json, headers=headers)

    def put(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        """
        Make a PUT request.

        Args:
            endpoint: API endpoint
            data: Form data or raw data
            json: JSON data
            headers: Request headers

        Returns:
            httpx.Response object
        """
        url = self._build_url(endpoint)
        return self._make_request("PUT", url, data=data, json=json, headers=headers)

    def patch(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        """
        Make a PATCH request.

        Args:
            endpoint: API endpoint
            data: Form data or raw data
            json: JSON data
            headers: Request headers

        Returns:
            httpx.Response object
        """
        url = self._build_url(endpoint)
        return self._make_request("PATCH", url, data=data, json=json, headers=headers)

    def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> httpx.Response:
        """
        Make a DELETE request.

        Args:
            endpoint: API endpoint
            headers: Request headers

        Returns:
            httpx.Response object
        """
        url = self._build_url(endpoint)
        return self._make_request("DELETE", url, headers=headers)
