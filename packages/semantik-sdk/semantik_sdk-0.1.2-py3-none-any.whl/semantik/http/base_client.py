"""Base HTTP client for Semantik API requests."""

import os
from typing import Any, Dict, Optional
import requests
from requests.exceptions import RequestException


class ApiError(Exception):
    """Exception raised for API errors."""

    def __init__(
        self,
        status: int,
        path: str,
        message: str,
        response: Optional[Dict[str, Any]] = None,
    ):
        self.status = status
        self.path = path
        self.response = response
        super().__init__(message)


class SemantikConfig:
    """Configuration for Semantik client."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key
        self.base_url = base_url


class BaseClient:
    """Base HTTP client for making authenticated requests to the Semantik API."""

    def __init__(self, config: Optional[SemantikConfig] = None):
        """
        Initialize the base client.

        Args:
            config: Optional configuration. If not provided, reads from environment variables.

        Raises:
            ValueError: If API key is not provided and SEMANTIK_API_KEY is not set.
        """
        config = config or SemantikConfig()

        # Use provided api_key, or fall back to environment variable
        api_key = config.api_key or os.getenv("SEMANTIK_API_KEY")

        if not api_key:
            raise ValueError(
                "API key is required. Either:\n"
                "  1. Set SEMANTIK_API_KEY environment variable in your .env file, or\n"
                "  2. Pass api_key='sk_...' to the Semantik constructor."
            )

        self.api_key = api_key
        self.base_url = (
            config.base_url
            or os.getenv("SEMANTIK_BASE_URL")
            or "https://gateway.semantikmatch.com"
        )

    def request(
        self,
        path: str,
        method: str = "GET",
        body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Make an authenticated request to the API.

        Args:
            path: API path (e.g., '/api/v2/programs')
            method: HTTP method (GET, POST, etc.)
            body: Request body as dictionary (will be JSON encoded)
            headers: Additional headers to include

        Returns:
            Response data as dictionary

        Raises:
            ApiError: If the API returns an error status code
            RequestException: If the request fails
        """
        url = f"{self.base_url}{path}"
        request_headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            **(headers or {}),
        }

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=request_headers,
                json=body,
                timeout=30,
            )

            # Parse response
            try:
                response_data = response.json() if response.text else None
            except ValueError:
                response_data = response.text

            # Check for errors
            if response.status_code >= 200 and response.status_code < 300:
                return response_data

            # Raise API error
            error_message = (
                response_data.get("message") if isinstance(response_data, dict) else None
            ) or f"Request failed with status {response.status_code}"

            raise ApiError(
                status=response.status_code,
                path=path,
                message=error_message,
                response=response_data,
            )

        except RequestException as e:
            raise Exception(f"Request failed: {str(e)}") from e

