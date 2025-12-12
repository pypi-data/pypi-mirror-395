"""Alerts resource for the Armor SDK."""

from __future__ import annotations

import builtins
from typing import Any

from armor.models import Alert, AlertRule, AlertSummary
from armor.resources.base import BaseResource


class AlertsResource(BaseResource):
    """Resource for interacting with alerts.

    Example:
        >>> from armor import Client
        >>> client = Client()
        >>>
        >>> # Get summary
        >>> summary = client.alerts.summary()
        >>> if summary.unresolved_alerts > 0:
        ...     print(f"You have {summary.unresolved_alerts} unresolved alerts")
        >>>
        >>> # List critical alerts
        >>> critical = client.alerts.list(severity="critical")
        >>>
        >>> # List alert rules
        >>> rules = client.alerts.rules()
    """

    def summary(self) -> AlertSummary:
        """Get a summary of alerts and rules.

        Returns:
            AlertSummary with counts
        """
        response = self._get("/alerts/summary")
        return AlertSummary.model_validate(response.get("data", {}))

    def list(
        self,
        status: str | None = None,
        severity: str | None = None,
        asset_id: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> builtins.list[Alert]:
        """List alerts with optional filters.

        Args:
            status: Filter by status ("triggered", "acknowledged", "resolved")
            severity: Filter by severity ("info", "warning", "critical")
            asset_id: Filter by asset UUID or qualified name
            limit: Maximum number of results (default 50, max 100)
            offset: Number of results to skip

        Returns:
            List of Alert objects
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if status:
            params["status"] = status
        if severity:
            params["severity"] = severity
        if asset_id:
            params["asset_id"] = asset_id

        response = self._get("/alerts", params=params)
        data = response.get("data", {}).get("data", [])
        return [Alert.model_validate(item) for item in data]

    def rules(
        self,
        enabled_only: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> builtins.list[AlertRule]:
        """List alert rules.

        Args:
            enabled_only: Only return enabled rules
            limit: Maximum number of results (default 50, max 100)
            offset: Number of results to skip

        Returns:
            List of AlertRule objects
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if enabled_only:
            params["enabled_only"] = True

        response = self._get("/alerts/rules", params=params)
        data = response.get("data", {}).get("data", [])
        return [AlertRule.model_validate(item) for item in data]
