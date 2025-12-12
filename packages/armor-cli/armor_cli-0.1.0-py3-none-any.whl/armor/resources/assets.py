"""Assets resource for the Armor SDK."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from armor.models import Asset
from armor.resources.base import BaseResource

if TYPE_CHECKING:
    pass


class AssetsResource(BaseResource):
    """Resource for interacting with assets.

    Example:
        >>> from armor import Client
        >>> client = Client()
        >>>
        >>> # List all assets
        >>> assets = client.assets.list()
        >>>
        >>> # List with filters
        >>> pg_assets = client.assets.list(source="postgresql")
        >>>
        >>> # Get a specific asset
        >>> asset = client.assets.get("postgresql.mydb.public.users")
    """

    def list(
        self,
        source: str | None = None,
        asset_type: str | None = None,
        search: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Asset]:
        """List assets with optional filters.

        Args:
            source: Filter by source type (e.g., "postgresql", "databricks")
            asset_type: Filter by asset type (e.g., "table", "view")
            search: Search in asset names
            limit: Maximum number of assets to return (default 50, max 100)
            offset: Number of assets to skip for pagination

        Returns:
            List of Asset objects
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if source:
            params["source"] = source
        if asset_type:
            params["asset_type"] = asset_type
        if search:
            params["search"] = search

        response = self._get("/assets", params=params)
        data = response.get("data", {}).get("data", [])
        return [Asset.model_validate(item) for item in data]

    def get(self, asset_id: str) -> Asset:
        """Get a specific asset by ID or qualified name.

        Args:
            asset_id: Asset UUID or qualified name (e.g., "postgresql.mydb.public.users")

        Returns:
            Asset object

        Raises:
            NotFoundError: If asset is not found
        """
        response = self._get(f"/assets/{asset_id}")
        return Asset.model_validate(response.get("data", {}))
