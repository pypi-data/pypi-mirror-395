"""Base resource class for API resources."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from armor.client import Client

# SDK API prefix - all SDK endpoints are under /sdk to avoid conflicts with UI endpoints
SDK_PREFIX = "/sdk"


class BaseResource:
    """Base class for API resources."""

    def __init__(self, client: "Client") -> None:
        self._client = client

    def _get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make a GET request."""
        return self._client._request("GET", f"{SDK_PREFIX}{path}", params=params)

    def _post(
        self,
        path: str,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make a POST request."""
        return self._client._request("POST", f"{SDK_PREFIX}{path}", json=json)

    def _delete(
        self,
        path: str,
    ) -> dict[str, Any]:
        """Make a DELETE request."""
        return self._client._request("DELETE", f"{SDK_PREFIX}{path}")
