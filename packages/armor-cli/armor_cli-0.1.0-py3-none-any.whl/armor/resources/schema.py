"""Schema resource for the Armor SDK."""

from __future__ import annotations

from typing import Any

from armor.models import SchemaChange, SchemaSummary
from armor.resources.base import BaseResource


class SchemaResource(BaseResource):
    """Resource for interacting with schema drift monitoring.

    Example:
        >>> from armor import Client
        >>> client = Client()
        >>>
        >>> # Get summary
        >>> summary = client.schema.summary()
        >>> if summary.critical_count > 0:
        ...     print(f"Warning: {summary.critical_count} critical changes!")
        >>>
        >>> # List unacknowledged changes
        >>> changes = client.schema.changes(unacknowledged_only=True)
        >>>
        >>> # Get changes for specific asset
        >>> asset_schema = client.schema.get("postgresql.mydb.public.users")
    """

    def summary(self) -> SchemaSummary:
        """Get a summary of schema changes across all assets.

        Returns:
            SchemaSummary with counts by severity
        """
        response = self._get("/schema/summary")
        return SchemaSummary.model_validate(response.get("data", {}))

    def changes(
        self,
        asset_id: str | None = None,
        severity: str | None = None,
        unacknowledged_only: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> list[SchemaChange]:
        """List schema changes with optional filters.

        Args:
            asset_id: Filter by asset UUID or qualified name
            severity: Filter by severity ("critical", "warning", "info")
            unacknowledged_only: Only return unacknowledged changes
            limit: Maximum number of results (default 50, max 100)
            offset: Number of results to skip

        Returns:
            List of SchemaChange objects
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if asset_id:
            params["asset_id"] = asset_id
        if severity:
            params["severity"] = severity
        if unacknowledged_only:
            params["unacknowledged_only"] = True

        response = self._get("/schema/changes", params=params)
        data = response.get("data", {}).get("data", [])
        return [SchemaChange.model_validate(item) for item in data]

    def get(self, asset_id: str) -> dict[str, Any]:
        """Get current schema and recent changes for an asset.

        Args:
            asset_id: Asset UUID or qualified name

        Returns:
            Dict with asset_id, qualified_name, recent_changes, total_unacknowledged

        Raises:
            NotFoundError: If asset is not found
        """
        response = self._get(f"/schema/{asset_id}")
        data = response.get("data", {})
        return data if isinstance(data, dict) else {}
