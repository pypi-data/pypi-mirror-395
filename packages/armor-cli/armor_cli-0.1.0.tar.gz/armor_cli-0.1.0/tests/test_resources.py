"""Tests for SDK resource classes."""

from unittest.mock import MagicMock

import pytest

from armor.exceptions import StalenessError


class TestAssetsResource:
    """Tests for AssetsResource."""

    @pytest.fixture
    def mock_client(self):
        """Create mock client."""
        client = MagicMock()
        return client

    def test_list_assets(self, mock_client):
        """List assets makes correct API call."""
        from armor.resources.assets import AssetsResource

        mock_client._request.return_value = {
            "data": {
                "data": [
                    {
                        "id": "1",
                        "qualified_name": "snowflake.prod.orders",
                        "name": "orders",
                        "asset_type": "table",
                    }
                ]
            },
        }

        resource = AssetsResource(mock_client)
        assets = resource.list()

        mock_client._request.assert_called_once_with(
            "GET", "/sdk/assets", params={"limit": 50, "offset": 0}
        )
        assert len(assets) == 1
        assert assets[0].qualified_name == "snowflake.prod.orders"

    def test_list_assets_with_filters(self, mock_client):
        """List assets passes filter parameters."""
        from armor.resources.assets import AssetsResource

        mock_client._request.return_value = {"data": {"data": []}}

        resource = AssetsResource(mock_client)
        resource.list(source="snowflake", asset_type="table", limit=10)

        mock_client._request.assert_called_once()
        call_args = mock_client._request.call_args
        call_params = call_args[1]["params"]
        assert call_params["source"] == "snowflake"
        assert call_params["asset_type"] == "table"
        assert call_params["limit"] == 10

    def test_get_asset(self, mock_client):
        """Get single asset by qualified name."""
        from armor.resources.assets import AssetsResource

        mock_client._request.return_value = {
            "data": {
                "id": "1",
                "qualified_name": "snowflake.prod.orders",
                "name": "orders",
                "asset_type": "table",
            }
        }

        resource = AssetsResource(mock_client)
        asset = resource.get("snowflake.prod.orders")

        mock_client._request.assert_called_once_with(
            "GET", "/sdk/assets/snowflake.prod.orders", params=None
        )
        assert asset.qualified_name == "snowflake.prod.orders"


class TestFreshnessResource:
    """Tests for FreshnessResource."""

    @pytest.fixture
    def mock_client(self):
        """Create mock client."""
        client = MagicMock()
        return client

    def test_get_freshness(self, mock_client):
        """Get freshness status for asset."""
        from armor.resources.freshness import FreshnessResource

        mock_client._request.return_value = {
            "data": {
                "asset_id": "1",
                "qualified_name": "snowflake.prod.orders",
                "status": "fresh",
                "is_stale": False,
                "checked_at": "2024-12-04T10:00:00Z",
            }
        }

        resource = FreshnessResource(mock_client)
        status = resource.get("snowflake.prod.orders")

        assert status.is_stale is False
        assert status.qualified_name == "snowflake.prod.orders"

    def test_require_fresh_passes_when_fresh(self, mock_client):
        """require_fresh doesn't raise when data is fresh."""
        from armor.resources.freshness import FreshnessResource

        mock_client._request.return_value = {
            "data": {
                "asset_id": "1",
                "qualified_name": "snowflake.prod.orders",
                "status": "fresh",
                "is_stale": False,
                "hours_since_update": 2.0,
                "staleness_threshold_hours": 24,
                "checked_at": "2024-12-04T10:00:00Z",
            }
        }

        resource = FreshnessResource(mock_client)
        # Should not raise
        status = resource.require_fresh("snowflake.prod.orders")
        assert status.is_stale is False

    def test_require_fresh_raises_when_stale(self, mock_client):
        """require_fresh raises StalenessError when data is stale."""
        from armor.resources.freshness import FreshnessResource

        mock_client._request.return_value = {
            "data": {
                "asset_id": "1",
                "qualified_name": "snowflake.prod.orders",
                "status": "stale",
                "is_stale": True,
                "hours_since_update": 30.0,
                "staleness_threshold_hours": 24,
                "checked_at": "2024-12-04T10:00:00Z",
            }
        }

        resource = FreshnessResource(mock_client)

        with pytest.raises(StalenessError) as exc_info:
            resource.require_fresh("snowflake.prod.orders")

        assert exc_info.value.asset == "snowflake.prod.orders"
        assert exc_info.value.threshold_hours == 24

    def test_refresh_triggers_check(self, mock_client):
        """Refresh triggers freshness check."""
        from armor.resources.freshness import FreshnessResource

        mock_client._request.return_value = {"data": {"job_id": "job_123", "status": "pending"}}

        resource = FreshnessResource(mock_client)
        result = resource.refresh("snowflake.prod.orders")

        mock_client._request.assert_called_once_with(
            "POST",
            "/sdk/freshness/snowflake.prod.orders/refresh",
            json=None,
        )
        assert result["job_id"] == "job_123"

    def test_summary(self, mock_client):
        """Get freshness summary."""
        from armor.resources.freshness import FreshnessResource

        mock_client._request.return_value = {
            "data": {
                "total_assets": 100,
                "fresh_count": 95,
                "stale_count": 3,
                "unknown_count": 1,
                "disabled_count": 1,
                "freshness_rate": 95.0,
            }
        }

        resource = FreshnessResource(mock_client)
        summary = resource.summary()

        assert summary.total_assets == 100
        assert summary.fresh_count == 95
        assert summary.stale_count == 3


class TestAlertsResource:
    """Tests for AlertsResource."""

    @pytest.fixture
    def mock_client(self):
        """Create mock client."""
        client = MagicMock()
        return client

    def test_list_alerts(self, mock_client):
        """List alerts makes correct API call."""
        from armor.resources.alerts import AlertsResource

        mock_client._request.return_value = {
            "data": {
                "data": [
                    {
                        "id": "alert_1",
                        "message": "Test alert",
                        "severity": "warning",
                        "status": "triggered",
                        "triggered_at": "2024-12-04T10:00:00Z",
                    }
                ]
            },
        }

        resource = AlertsResource(mock_client)
        alerts = resource.list()

        assert len(alerts) == 1
        assert alerts[0].severity == "warning"

    def test_list_alerts_with_status_filter(self, mock_client):
        """List alerts filters by status."""
        from armor.resources.alerts import AlertsResource

        mock_client._request.return_value = {"data": {"data": []}}

        resource = AlertsResource(mock_client)
        resource.list(status="triggered")

        call_args = mock_client._request.call_args
        call_params = call_args[1]["params"]
        assert call_params["status"] == "triggered"

    def test_summary(self, mock_client):
        """Get alerts summary."""
        from armor.resources.alerts import AlertsResource

        mock_client._request.return_value = {
            "data": {
                "total_rules": 50,
                "active_rules": 45,
                "recent_alerts": 10,
                "unresolved_alerts": 3,
            }
        }

        resource = AlertsResource(mock_client)
        summary = resource.summary()

        assert summary.total_rules == 50
        assert summary.active_rules == 45


class TestLineageResource:
    """Tests for LineageResource."""

    @pytest.fixture
    def mock_client(self):
        """Create mock client."""
        client = MagicMock()
        return client

    def test_get_lineage(self, mock_client):
        """Get lineage for asset."""
        from armor.resources.lineage import LineageResource

        mock_client._request.return_value = {
            "data": {
                "root": {
                    "id": "1",
                    "qualified_name": "snowflake.prod.orders",
                    "name": "orders",
                },
                "upstream": [{"id": "2", "qualified_name": "raw.orders", "name": "orders"}],
                "downstream": [{"id": "3", "qualified_name": "mart.orders", "name": "orders"}],
                "edges": [],
            }
        }

        resource = LineageResource(mock_client)
        lineage = resource.get("snowflake.prod.orders")

        assert len(lineage.upstream) == 1
        assert len(lineage.downstream) == 1

    def test_get_lineage_with_depth(self, mock_client):
        """Get lineage with custom depth."""
        from armor.resources.lineage import LineageResource

        mock_client._request.return_value = {
            "data": {
                "root": {
                    "id": "1",
                    "qualified_name": "snowflake.prod.orders",
                    "name": "orders",
                },
                "upstream": [],
                "downstream": [],
                "edges": [],
            }
        }

        resource = LineageResource(mock_client)
        resource.get("snowflake.prod.orders", depth=3)

        call_args = mock_client._request.call_args
        call_params = call_args[1]["params"]
        assert call_params["depth"] == 3


class TestSchemaResource:
    """Tests for SchemaResource."""

    @pytest.fixture
    def mock_client(self):
        """Create mock client."""
        client = MagicMock()
        return client

    def test_summary(self, mock_client):
        """Get schema summary."""
        from armor.resources.schema import SchemaResource

        mock_client._request.return_value = {
            "data": {
                "total_changes": 100,
                "unacknowledged": 5,
                "critical_count": 2,
                "warning_count": 10,
                "info_count": 88,
            }
        }

        resource = SchemaResource(mock_client)
        summary = resource.summary()

        assert summary.total_changes == 100
        assert summary.unacknowledged == 5

    def test_list_changes(self, mock_client):
        """List schema changes."""
        from armor.resources.schema import SchemaResource

        mock_client._request.return_value = {
            "data": {
                "data": [
                    {
                        "id": "change_1",
                        "asset_id": "asset_1",
                        "qualified_name": "snowflake.prod.orders",
                        "change_type": "column_added",
                        "severity": "info",
                        "column_name": "new_col",
                        "detected_at": "2024-12-04T10:00:00Z",
                    }
                ]
            },
        }

        resource = SchemaResource(mock_client)
        changes = resource.changes()

        assert len(changes) == 1
        assert changes[0].change_type == "column_added"
