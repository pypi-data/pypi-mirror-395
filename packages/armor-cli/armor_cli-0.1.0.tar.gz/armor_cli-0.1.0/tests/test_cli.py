"""Tests for the Armor CLI."""

from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from armor.cli import app

runner = CliRunner()


class TestCLIAuth:
    """Tests for auth commands."""

    def test_auth_login_with_key(self):
        """Login with explicit API key."""
        with patch("armor.cli.save_config") as mock_save:
            with patch("armor.Client") as mock_client_class:
                # Mock the Client to not raise errors
                mock_client = MagicMock()
                mock_client_class.return_value = mock_client
                mock_client.api_keys.usage.return_value = {"current_count": 1}

                result = runner.invoke(
                    app,
                    [
                        "auth",
                        "login",
                        "--api-key",
                        "aa_live_test",
                    ],  # pragma: allowlist secret
                )

                assert result.exit_code == 0
                mock_save.assert_called_once()

    def test_auth_status_authenticated(self):
        """Status shows authenticated when key exists."""
        with patch("armor.cli.load_config") as mock_load:
            mock_load.return_value = MagicMock(
                api_key="aa_live_test_key_12345",  # pragma: allowlist secret
                api_url="https://api.anomalyarmor.ai/api/v1",
            )
            result = runner.invoke(app, ["auth", "status"])

            assert result.exit_code == 0
            assert "Authenticated" in result.output

    def test_auth_status_not_authenticated(self):
        """Status shows not authenticated when no key."""
        with patch("armor.cli.load_config") as mock_load:
            mock_load.return_value = MagicMock(api_key=None)
            result = runner.invoke(app, ["auth", "status"])

            # Exit code 2 for auth error
            assert result.exit_code == 2
            assert "Not authenticated" in result.output

    def test_auth_logout(self):
        """Logout clears stored credentials."""
        with patch("armor.cli.clear_config") as mock_clear:
            result = runner.invoke(app, ["auth", "logout"])

            assert result.exit_code == 0
            mock_clear.assert_called_once()


class TestCLIAssets:
    """Tests for assets commands."""

    @pytest.fixture
    def mock_client(self):
        """Create mock client."""
        with patch("armor.cli.get_client") as mock_get:
            client = MagicMock()
            mock_get.return_value = client
            yield client

    def test_assets_list(self, mock_client):
        """List assets command."""
        mock_client.assets.list.return_value = [
            MagicMock(
                qualified_name="snowflake.prod.orders",
                asset_type="table",
                source_type="snowflake",
                is_active=True,
            )
        ]

        result = runner.invoke(app, ["assets", "list"])

        assert result.exit_code == 0
        assert "snowflake.prod.orders" in result.output

    def test_assets_list_with_source_filter(self, mock_client):
        """List assets with source filter."""
        mock_client.assets.list.return_value = []

        runner.invoke(app, ["assets", "list", "--source", "snowflake"])

        mock_client.assets.list.assert_called_once()
        call_kwargs = mock_client.assets.list.call_args[1]
        assert call_kwargs.get("source") == "snowflake"

    def test_assets_get(self, mock_client):
        """Get single asset."""
        mock_client.assets.get.return_value = MagicMock(
            id="asset-1",
            qualified_name="snowflake.prod.orders",
            asset_type="table",
            source_type="snowflake",
            is_active=True,
            description=None,
        )

        result = runner.invoke(app, ["assets", "get", "snowflake.prod.orders"])

        assert result.exit_code == 0
        assert "snowflake.prod.orders" in result.output


class TestCLIFreshness:
    """Tests for freshness commands."""

    @pytest.fixture
    def mock_client(self):
        """Create mock client."""
        with patch("armor.cli.get_client") as mock_get:
            client = MagicMock()
            mock_get.return_value = client
            yield client

    def test_freshness_summary(self, mock_client):
        """Freshness summary command."""
        mock_client.freshness.summary.return_value = MagicMock(
            total_assets=100,
            fresh_count=95,
            stale_count=5,
            unknown_count=0,
            freshness_rate=95.0,
        )

        result = runner.invoke(app, ["freshness", "summary"])

        assert result.exit_code == 0
        assert "95" in result.output

    def test_freshness_get(self, mock_client):
        """Get freshness for asset."""
        mock_client.freshness.get.return_value = MagicMock(
            qualified_name="snowflake.prod.orders",
            status="fresh",
            is_stale=False,
            hours_since_update=2.5,
            staleness_threshold_hours=24,
            last_update_time=None,
        )

        result = runner.invoke(app, ["freshness", "get", "snowflake.prod.orders"])

        assert result.exit_code == 0

    def test_freshness_check_fresh_exit_0(self, mock_client):
        """Check freshness exits 0 when fresh."""
        mock_client.freshness.require_fresh.return_value = MagicMock(
            qualified_name="snowflake.prod.orders",
            status="fresh",
            is_stale=False,
            hours_since_update=2.0,
        )

        result = runner.invoke(app, ["freshness", "check", "snowflake.prod.orders"])

        assert result.exit_code == 0

    def test_freshness_check_stale_exit_1(self, mock_client):
        """Check freshness exits 1 when stale."""
        from armor.exceptions import StalenessError

        mock_client.freshness.require_fresh.side_effect = StalenessError(
            asset="snowflake.prod.orders",
            hours_since_update=26.0,
            threshold_hours=24,
        )

        result = runner.invoke(app, ["freshness", "check", "snowflake.prod.orders"])

        assert result.exit_code == 1

    def test_freshness_refresh(self, mock_client):
        """Trigger freshness refresh."""
        mock_client.freshness.refresh.return_value = {
            "job_id": "job_123",
            "status": "pending",
        }

        result = runner.invoke(app, ["freshness", "refresh", "snowflake.prod.orders"])

        assert result.exit_code == 0


class TestCLIAlerts:
    """Tests for alerts commands."""

    @pytest.fixture
    def mock_client(self):
        """Create mock client."""
        with patch("armor.cli.get_client") as mock_get:
            client = MagicMock()
            mock_get.return_value = client
            yield client

    def test_alerts_summary(self, mock_client):
        """Alerts summary command."""
        mock_client.alerts.summary.return_value = MagicMock(
            total_rules=50,
            active_rules=45,
            recent_alerts=10,
            unresolved_alerts=3,
        )

        result = runner.invoke(app, ["alerts", "summary"])

        assert result.exit_code == 0

    def test_alerts_list(self, mock_client):
        """List alerts command."""
        mock_client.alerts.list.return_value = [
            MagicMock(
                id="alert_1",
                severity="warning",
                status="triggered",
                message="Data is stale",
                qualified_name="snowflake.prod.orders",
            )
        ]

        result = runner.invoke(app, ["alerts", "list"])

        assert result.exit_code == 0

    def test_alerts_list_triggered(self, mock_client):
        """List triggered alerts."""
        mock_client.alerts.list.return_value = []

        runner.invoke(app, ["alerts", "list", "--status", "triggered"])

        mock_client.alerts.list.assert_called_once()
        call_kwargs = mock_client.alerts.list.call_args[1]
        assert call_kwargs.get("status") == "triggered"


class TestCLIAPIKeys:
    """Tests for API keys commands."""

    @pytest.fixture
    def mock_client(self):
        """Create mock client."""
        with patch("armor.cli.get_client") as mock_get:
            client = MagicMock()
            mock_get.return_value = client
            yield client

    def test_api_keys_list(self, mock_client):
        """List API keys command."""
        mock_key = MagicMock()
        mock_key.name = "Test Key"
        mock_key.display_key = "aa_live_abc...xyz1"
        mock_key.scope = "read-only"
        mock_key.is_active = True
        mock_key.last_used_at = None
        mock_client.api_keys.list.return_value = [mock_key]

        result = runner.invoke(app, ["api-keys", "list"])

        assert result.exit_code == 0
        assert "Test Key" in result.output

    def test_api_keys_create(self, mock_client):
        """Create API key command."""
        mock_client.api_keys.create.return_value = MagicMock(
            key="aa_live_new_key_12345",  # pragma: allowlist secret
            id="key_456",
            name="New Key",
            scope="read-only",
        )

        result = runner.invoke(
            app, ["api-keys", "create", "--name", "New Key", "--scope", "read-only"]
        )

        assert result.exit_code == 0
        mock_client.api_keys.create.assert_called_once()

    def test_api_keys_revoke(self, mock_client):
        """Revoke API key command."""
        mock_client.api_keys.revoke.return_value = None

        result = runner.invoke(app, ["api-keys", "revoke", "key_123", "--yes"])

        assert result.exit_code == 0
        mock_client.api_keys.revoke.assert_called_once()


class TestCLIErrorHandling:
    """Tests for CLI error handling."""

    @pytest.fixture
    def mock_client(self):
        """Create mock client."""
        with patch("armor.cli.get_client") as mock_get:
            client = MagicMock()
            mock_get.return_value = client
            yield client

    def test_auth_error_exit_2(self, mock_client):
        """Authentication error exits with code 2."""
        from armor.exceptions import AuthenticationError

        mock_client.assets.list.side_effect = AuthenticationError("Invalid key")

        result = runner.invoke(app, ["assets", "list"])

        assert result.exit_code == 2  # EXIT_AUTH_ERROR

    def test_not_found_error_exit_3(self, mock_client):
        """Not found error exits with code 3."""
        from armor.exceptions import NotFoundError

        mock_client.assets.get.side_effect = NotFoundError("Asset not found")

        result = runner.invoke(app, ["assets", "get", "nonexistent"])

        assert result.exit_code == 3

    def test_rate_limit_error_exit_4(self, mock_client):
        """Rate limit error exits with code 4."""
        from armor.exceptions import RateLimitError

        mock_client.assets.list.side_effect = RateLimitError("Rate limited", retry_after=30)

        result = runner.invoke(app, ["assets", "list"])

        assert result.exit_code == 4  # EXIT_RATE_LIMIT
        assert "30" in result.output or "Retry" in result.output
