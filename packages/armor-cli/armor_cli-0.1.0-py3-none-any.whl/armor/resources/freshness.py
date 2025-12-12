"""Freshness resource for the Armor SDK."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from armor.models import FreshnessStatus, FreshnessSummary
from armor.resources.base import BaseResource

if TYPE_CHECKING:
    pass


class FreshnessResource(BaseResource):
    """Resource for interacting with freshness monitoring.

    Example:
        >>> from armor import Client
        >>> client = Client()
        >>>
        >>> # Get overall summary
        >>> summary = client.freshness.summary()
        >>> print(f"Freshness rate: {summary.freshness_rate}%")
        >>>
        >>> # Check specific asset
        >>> status = client.freshness.get("postgresql.mydb.public.users")
        >>> if status.is_stale:
        ...     print(f"Stale for {status.hours_since_update} hours")
        >>>
        >>> # List all stale assets
        >>> stale = client.freshness.list(status="stale")
    """

    def summary(self) -> FreshnessSummary:
        """Get a summary of freshness across all assets.

        Returns:
            FreshnessSummary with counts and rates
        """
        response = self._get("/freshness/summary")
        return FreshnessSummary.model_validate(response.get("data", {}))

    def get(self, asset_id: str) -> FreshnessStatus:
        """Get freshness status for a specific asset.

        Args:
            asset_id: Asset UUID or qualified name

        Returns:
            FreshnessStatus object

        Raises:
            NotFoundError: If asset is not found
        """
        response = self._get(f"/freshness/{asset_id}")
        return FreshnessStatus.model_validate(response.get("data", {}))

    def list(
        self,
        status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[FreshnessStatus]:
        """List freshness status for all assets.

        Args:
            status: Filter by status ("fresh", "stale", "unknown", "disabled")
            limit: Maximum number of results (default 50, max 100)
            offset: Number of results to skip

        Returns:
            List of FreshnessStatus objects
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if status:
            params["status"] = status

        response = self._get("/freshness", params=params)
        data = response.get("data", {}).get("data", [])
        return [FreshnessStatus.model_validate(item) for item in data]

    def require_fresh(
        self,
        asset_id: str,
        max_age_hours: float | None = None,
    ) -> FreshnessStatus:
        """Require an asset to be fresh, raising an error if stale.

        This is the recommended way to gate downstream processes on data freshness.
        Use in CI/CD pipelines or before running analytics.

        Args:
            asset_id: Asset UUID or qualified name
            max_age_hours: Maximum acceptable age in hours. If not provided,
                          uses the asset's configured threshold.

        Returns:
            FreshnessStatus object if fresh

        Raises:
            DataStaleError: If asset is stale (hours > max_age_hours)
            NotFoundError: If asset is not found

        Example:
            >>> from armor import Client
            >>> from armor.exceptions import DataStaleError
            >>>
            >>> client = Client()
            >>> try:
            ...     client.freshness.require_fresh("postgresql.mydb.public.users")
            ...     # Run downstream process
            ... except DataStaleError as e:
            ...     print(f"Data is stale: {e.hours_since_update}h old")
            ...     sys.exit(1)
        """
        from armor.exceptions import StalenessError

        status = self.get(asset_id)

        # Determine the threshold to use
        threshold = max_age_hours
        if threshold is None:
            threshold = status.staleness_threshold_hours or 24.0  # Default to 24h

        # Check if stale
        if status.is_stale or (
            status.hours_since_update is not None and status.hours_since_update > threshold
        ):
            raise StalenessError(
                asset=asset_id,
                hours_since_update=status.hours_since_update or 0.0,
                threshold_hours=threshold,
            )

        return status

    def refresh(self, asset_id: str) -> dict[str, Any]:
        """Trigger a freshness check for an asset.

        Args:
            asset_id: Asset UUID or qualified name

        Returns:
            Dictionary with job_id, status, and message

        Raises:
            NotFoundError: If asset is not found
            PermissionError: If API key doesn't have write scope
        """
        response = self._post(f"/freshness/{asset_id}/refresh")
        data = response.get("data", {})
        return data if isinstance(data, dict) else {}
