"""Lineage resource for the Armor SDK."""

from __future__ import annotations

from armor.models import LineageGraph, LineageNode
from armor.resources.base import BaseResource


class LineageResource(BaseResource):
    """Resource for interacting with data lineage.

    Example:
        >>> from armor import Client
        >>> client = Client()
        >>>
        >>> # Get lineage for an asset
        >>> lineage = client.lineage.get("postgresql.mydb.public.users")
        >>> print(f"Root: {lineage.root.qualified_name}")
        >>> for upstream in lineage.upstream:
        ...     print(f"  Depends on: {upstream.qualified_name}")
        >>>
        >>> # List all assets with lineage
        >>> roots = client.lineage.list()
    """

    def get(
        self,
        asset_id: str,
        depth: int = 1,
        direction: str = "both",
    ) -> LineageGraph:
        """Get lineage graph for an asset.

        Args:
            asset_id: Asset UUID or qualified name
            depth: How many levels of lineage to fetch (1-5)
            direction: Direction to traverse ("upstream", "downstream", "both")

        Returns:
            LineageGraph with root, upstream, downstream, and edges

        Raises:
            NotFoundError: If asset is not found
        """
        params = {"depth": depth, "direction": direction}
        response = self._get(f"/lineage/{asset_id}", params=params)
        return LineageGraph.model_validate(response.get("data", {}))

    def list(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> list[LineageNode]:
        """List all assets that have lineage information.

        Args:
            limit: Maximum number of results (default 50, max 100)
            offset: Number of results to skip

        Returns:
            List of LineageNode objects (assets with lineage)
        """
        params = {"limit": limit, "offset": offset}
        response = self._get("/lineage", params=params)
        data = response.get("data", {}).get("data", [])
        return [LineageNode.model_validate(item) for item in data]
