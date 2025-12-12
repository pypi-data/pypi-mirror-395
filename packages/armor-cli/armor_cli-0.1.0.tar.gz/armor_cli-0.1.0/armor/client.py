"""Main client for the Armor SDK."""

from __future__ import annotations

from typing import Any

import httpx

from armor.config import load_config
from armor.exceptions import (
    ArmorError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from armor.resources.alerts import AlertsResource
from armor.resources.api_keys import APIKeysResource
from armor.resources.assets import AssetsResource
from armor.resources.freshness import FreshnessResource
from armor.resources.lineage import LineageResource
from armor.resources.schema import SchemaResource


class Client:
    """AnomalyArmor API client.

    The main entry point for interacting with the AnomalyArmor API.

    Example:
        >>> from armor import Client
        >>>
        >>> # Using environment variable ARMOR_API_KEY
        >>> client = Client()
        >>>
        >>> # Or pass the API key directly
        >>> client = Client(api_key="aa_live_...")
        >>>
        >>> # List assets
        >>> assets = client.assets.list()
        >>> for asset in assets:
        ...     print(asset.qualified_name)
    """

    def __init__(
        self,
        api_key: str | None = None,
        api_url: str | None = None,
        timeout: int | None = None,
    ) -> None:
        """Initialize the client.

        Args:
            api_key: API key for authentication. If not provided, will load from
                     environment variable ARMOR_API_KEY or config file.
            api_url: Base URL for API requests. Defaults to production API.
            timeout: Request timeout in seconds. Defaults to 30.
        """
        # Load config (environment > file > defaults)
        config = load_config()

        # Override with explicit parameters
        self._api_key = api_key or config.api_key
        self._api_url = (api_url or config.api_url).rstrip("/")
        self._timeout = timeout or config.timeout

        if not self._api_key:
            raise AuthenticationError(
                "No API key provided. Set ARMOR_API_KEY environment variable, "
                "pass api_key parameter, or run 'armor auth login'."
            )

        # Create HTTP client
        self._http = httpx.Client(
            base_url=self._api_url,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
                "User-Agent": "armor-cli/0.1.0",
            },
            timeout=self._timeout,
        )

        # Initialize resource namespaces
        self.assets = AssetsResource(self)
        self.freshness = FreshnessResource(self)
        self.schema = SchemaResource(self)
        self.lineage = LineageResource(self)
        self.alerts = AlertsResource(self)
        self.api_keys = APIKeysResource(self)

    def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, DELETE, etc.)
            path: API path (relative to base URL)
            params: Query parameters
            json: JSON body for POST/PUT requests

        Returns:
            Response data

        Raises:
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            NotFoundError: If resource is not found
            ValidationError: If request validation fails
            ServerError: For other server errors
        """
        try:
            response = self._http.request(
                method=method,
                url=path,
                params=params,
                json=json,
            )
        except httpx.TimeoutException:
            raise ArmorError("Request timed out")
        except httpx.NetworkError as e:
            raise ArmorError(f"Network error: {e}")

        return self._handle_response(response)

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """Handle API response and raise appropriate exceptions."""
        # Parse response
        try:
            data = response.json()
        except Exception:
            data = {"message": response.text}

        # Success
        if response.status_code < 400:
            return data if isinstance(data, dict) else {}

        # Extract error info
        error = data.get("error", {})
        message = error.get("message") or data.get("message") or "Request failed"
        details = error.get("details", {})

        # Handle specific error codes
        if response.status_code == 401:
            raise AuthenticationError(message, details)

        if response.status_code == 403:
            raise AuthenticationError(f"Forbidden: {message}", details)

        if response.status_code == 404:
            raise NotFoundError(message, details=details)

        if response.status_code == 422:
            raise ValidationError(message, details=details)

        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            raise RateLimitError(message, retry_after=retry_after, details=details)

        # Generic server error
        raise ServerError(message, status_code=response.status_code, details=details)

    def close(self) -> None:
        """Close the HTTP client."""
        self._http.close()

    def __enter__(self) -> "Client":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
