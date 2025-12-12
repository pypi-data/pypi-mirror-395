"""API Keys resource for the Armor SDK."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from armor.models import APIKey, CreatedAPIKey

if TYPE_CHECKING:
    from armor.client import Client


class APIKeysResource:
    """Resource for managing API keys.

    Note: This resource does NOT extend BaseResource because API key endpoints
    are at /api-keys, not under the /sdk prefix used by other SDK endpoints.

    Example:
        >>> from armor import Client
        >>> client = Client()
        >>>
        >>> # List API keys
        >>> keys = client.api_keys.list()
        >>>
        >>> # Create a new key
        >>> new_key = client.api_keys.create(name="Airflow Production", scope="read-only")
        >>> print(f"Key: {new_key.key}")  # Only shown once!
        >>>
        >>> # Revoke a key
        >>> client.api_keys.revoke(key_id)
    """

    def __init__(self, client: "Client") -> None:
        self._client = client

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make a GET request directly (no /sdk prefix)."""
        return self._client._request("GET", path, params=params)

    def _post(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make a POST request directly (no /sdk prefix)."""
        return self._client._request("POST", path, json=json)

    def _delete(self, path: str) -> dict[str, Any]:
        """Make a DELETE request directly (no /sdk prefix)."""
        return self._client._request("DELETE", path)

    def list(
        self,
        include_revoked: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> list[APIKey]:
        """List API keys for your organization.

        Args:
            include_revoked: Include revoked keys in results
            limit: Maximum number of results (default 50, max 100)
            offset: Number of results to skip

        Returns:
            List of APIKey objects
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if include_revoked:
            params["include_revoked"] = True

        response = self._get("/api-keys", params=params)
        data = response.get("data", {}).get("keys", [])
        return [APIKey.model_validate(item) for item in data]

    def create(
        self,
        name: str,
        scope: str = "read-only",
    ) -> CreatedAPIKey:
        """Create a new API key.

        IMPORTANT: The full key is only returned in this response.
        Store it securely - you won't be able to retrieve it again.

        Args:
            name: Human-readable name for the key
            scope: Permission scope ("read-only", "read-write", "admin")

        Returns:
            CreatedAPIKey object including the full key

        Raises:
            ValidationError: If parameters are invalid
            ArmorError: If you've reached your organization's key limit
        """
        response = self._post("/api-keys", json={"name": name, "scope": scope})
        return CreatedAPIKey.model_validate(response.get("data", {}))

    def get(self, key_id: str) -> APIKey:
        """Get details of a specific API key.

        Args:
            key_id: Public UUID of the key

        Returns:
            APIKey object (without full key)

        Raises:
            NotFoundError: If key is not found
        """
        response = self._get(f"/api-keys/{key_id}")
        return APIKey.model_validate(response.get("data", {}))

    def revoke(self, key_id: str) -> APIKey:
        """Revoke an API key.

        Revoked keys can no longer be used for authentication.
        This action cannot be undone.

        Args:
            key_id: Public UUID of the key to revoke

        Returns:
            Updated APIKey object

        Raises:
            NotFoundError: If key is not found
        """
        response = self._delete(f"/api-keys/{key_id}")
        return APIKey.model_validate(response.get("data", {}))

    def usage(self) -> dict[str, Any]:
        """Get API key usage and limits.

        Returns:
            Dict with current_count, max_keys, rate_limit_per_min, burst_limit, can_create
        """
        response = self._get("/api-keys/usage")
        data = response.get("data", {})
        return data if isinstance(data, dict) else {}
