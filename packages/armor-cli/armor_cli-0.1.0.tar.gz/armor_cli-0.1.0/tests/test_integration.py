"""End-to-end integration tests for the Armor SDK.

These tests verify the complete flow from API key creation to SDK usage.
They use mocks to simulate the backend but test the full SDK stack.
"""

from unittest.mock import MagicMock, patch

import pytest

from armor import Client
from armor.exceptions import AuthenticationError, StalenessError


class TestE2EFlow:
    """End-to-end flow tests: Create API key -> SDK auth -> Query -> Check freshness."""

    @pytest.fixture
    def mock_http_client(self):
        """Create a mock HTTP client that simulates backend responses."""
        with patch("armor.client.httpx.Client") as mock_http:
            mock_instance = MagicMock()
            mock_http.return_value = mock_instance
            yield mock_instance

    def test_full_flow_api_key_to_freshness_check(self, mock_http_client):
        """Complete flow: Create client -> Query assets -> Check freshness."""
        # Setup mock responses for each step
        responses = []

        # Step 1: List assets
        assets_response = MagicMock()
        assets_response.status_code = 200
        assets_response.json.return_value = {
            "data": {
                "data": [
                    {
                        "id": "asset-1",
                        "qualified_name": "snowflake.prod.warehouse.orders",
                        "name": "orders",
                        "asset_type": "table",
                        "source_type": "snowflake",
                        "is_active": True,
                    }
                ]
            }
        }
        responses.append(assets_response)

        # Step 2: Get freshness
        freshness_response = MagicMock()
        freshness_response.status_code = 200
        freshness_response.json.return_value = {
            "data": {
                "asset_id": "asset-1",
                "qualified_name": "snowflake.prod.warehouse.orders",
                "status": "fresh",
                "is_stale": False,
                "hours_since_update": 2.5,
                "staleness_threshold_hours": 24,
                "checked_at": "2024-12-04T10:00:00Z",
            }
        }
        responses.append(freshness_response)

        # Configure mock to return responses in sequence
        mock_http_client.request.side_effect = responses

        # Execute the flow
        # Create client (no HTTP requests in constructor)
        client = Client(api_key="aa_live_test_key")  # pragma: allowlist secret

        # Step 1: List assets
        assets = client.assets.list(source="snowflake", limit=10)
        assert len(assets) == 1
        assert assets[0].qualified_name == "snowflake.prod.warehouse.orders"

        # Step 2: Check freshness - is_stale=False means data is fresh
        status = client.freshness.require_fresh("snowflake.prod.warehouse.orders")
        assert status.is_stale is False
        assert status.hours_since_update == 2.5

    def test_full_flow_with_stale_data_raises_error(self, mock_http_client):
        """Flow raises StalenessError when data is stale."""
        # Setup mock response for stale data
        freshness_response = MagicMock()
        freshness_response.status_code = 200
        freshness_response.json.return_value = {
            "data": {
                "asset_id": "asset-1",
                "qualified_name": "snowflake.prod.warehouse.orders",
                "status": "stale",
                "is_stale": True,
                "hours_since_update": 26.5,
                "staleness_threshold_hours": 24,
                "checked_at": "2024-12-04T10:00:00Z",
            }
        }
        mock_http_client.request.return_value = freshness_response

        client = Client(api_key="aa_live_test_key")  # pragma: allowlist secret

        with pytest.raises(StalenessError) as exc_info:
            client.freshness.require_fresh("snowflake.prod.warehouse.orders")

        assert exc_info.value.asset == "snowflake.prod.warehouse.orders"
        assert exc_info.value.hours_since_update == 26.5
        assert exc_info.value.threshold_hours == 24

    def test_full_flow_with_custom_threshold(self, mock_http_client):
        """Flow with custom max_age_hours threshold."""
        # Data is 10 hours old, default threshold 24h (fresh), custom 8h (stale)
        freshness_response = MagicMock()
        freshness_response.status_code = 200
        freshness_response.json.return_value = {
            "data": {
                "asset_id": "asset-1",
                "qualified_name": "snowflake.prod.warehouse.orders",
                "status": "fresh",
                "is_stale": False,
                "hours_since_update": 10.0,
                "staleness_threshold_hours": 24,
                "checked_at": "2024-12-04T10:00:00Z",
            }
        }
        mock_http_client.request.return_value = freshness_response

        client = Client(api_key="aa_live_test_key")  # pragma: allowlist secret

        # With custom threshold of 8 hours, 10 hour old data should be stale
        with pytest.raises(StalenessError) as exc_info:
            client.freshness.require_fresh(
                "snowflake.prod.warehouse.orders",
                max_age_hours=8.0,
            )

        assert exc_info.value.hours_since_update == 10.0
        assert exc_info.value.threshold_hours == 8.0


class TestAirflowIntegration:
    """Tests simulating Airflow DAG usage patterns."""

    @pytest.fixture
    def mock_http_client(self):
        """Create a mock HTTP client."""
        with patch("armor.client.httpx.Client") as mock_http:
            mock_instance = MagicMock()
            mock_http.return_value = mock_instance
            yield mock_instance

    def test_airflow_preflight_check_passes(self, mock_http_client):
        """Airflow preflight pattern: check passes when data is fresh."""
        # Simulate fresh data
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {
            "data": {
                "asset_id": "asset-1",
                "qualified_name": "snowflake.prod.warehouse.orders",
                "status": "fresh",
                "is_stale": False,
                "hours_since_update": 1.5,
                "staleness_threshold_hours": 24,
                "checked_at": "2024-12-04T10:00:00Z",
            }
        }
        mock_http_client.request.return_value = response

        def airflow_preflight_check():
            """Simulates Airflow task: check freshness before running pipeline."""
            client = Client(api_key="aa_live_test")  # pragma: allowlist secret
            client.freshness.require_fresh("snowflake.prod.warehouse.orders")
            return True

        # Should complete without raising
        result = airflow_preflight_check()
        assert result is True

    def test_airflow_preflight_check_fails_when_stale(self, mock_http_client):
        """Airflow preflight pattern: check fails when data is stale."""
        # Simulate stale data
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {
            "data": {
                "asset_id": "asset-1",
                "qualified_name": "snowflake.prod.warehouse.orders",
                "status": "stale",
                "is_stale": True,
                "hours_since_update": 30.0,
                "staleness_threshold_hours": 24,
                "checked_at": "2024-12-04T10:00:00Z",
            }
        }
        mock_http_client.request.return_value = response

        def airflow_preflight_check():
            """Simulates Airflow task: check freshness before running pipeline."""
            client = Client(api_key="aa_live_test")  # pragma: allowlist secret
            try:
                client.freshness.require_fresh("snowflake.prod.warehouse.orders")
                return 0  # Success
            except StalenessError:
                return 1  # Failure exit code

        # Should return failure exit code
        result = airflow_preflight_check()
        assert result == 1

    def test_airflow_multi_source_check(self, mock_http_client):
        """Airflow pattern: check multiple upstream sources."""
        responses = []

        # First source: fresh
        r1 = MagicMock()
        r1.status_code = 200
        r1.json.return_value = {
            "data": {
                "asset_id": "1",
                "qualified_name": "snowflake.prod.warehouse.orders",
                "status": "fresh",
                "is_stale": False,
                "hours_since_update": 1.0,
                "staleness_threshold_hours": 24,
                "checked_at": "2024-12-04T10:00:00Z",
            }
        }
        responses.append(r1)

        # Second source: fresh
        r2 = MagicMock()
        r2.status_code = 200
        r2.json.return_value = {
            "data": {
                "asset_id": "2",
                "qualified_name": "snowflake.prod.warehouse.customers",
                "status": "fresh",
                "is_stale": False,
                "hours_since_update": 2.0,
                "staleness_threshold_hours": 24,
                "checked_at": "2024-12-04T10:00:00Z",
            }
        }
        responses.append(r2)

        mock_http_client.request.side_effect = responses

        def check_all_upstream(assets: list[str]) -> list[str]:
            """Check all upstream sources, return list of stale ones."""
            client = Client(api_key="aa_live_test")  # pragma: allowlist secret
            stale = []
            for asset in assets:
                try:
                    client.freshness.require_fresh(asset)
                except StalenessError:
                    stale.append(asset)
            return stale

        stale_assets = check_all_upstream(
            [
                "snowflake.prod.warehouse.orders",
                "snowflake.prod.warehouse.customers",
            ]
        )

        assert stale_assets == []  # All fresh

    def test_airflow_gate_pattern_with_exception_handling(self, mock_http_client):
        """Airflow gate pattern with proper exception handling."""
        # Simulate auth error (invalid key)
        response = MagicMock()
        response.status_code = 401
        response.json.return_value = {"error": {"message": "Invalid API key"}}
        mock_http_client.request.return_value = response

        def airflow_task_with_error_handling():
            """Airflow task with proper error handling."""
            try:
                client = Client(api_key="aa_live_invalid")  # pragma: allowlist secret
                client.freshness.require_fresh("snowflake.prod.warehouse.orders")
                return {"status": "success"}
            except StalenessError as e:
                return {"status": "stale", "message": str(e)}
            except AuthenticationError as e:
                return {"status": "auth_error", "message": str(e)}
            except Exception as e:
                return {"status": "error", "message": str(e)}

        result = airflow_task_with_error_handling()
        assert result["status"] == "auth_error"
