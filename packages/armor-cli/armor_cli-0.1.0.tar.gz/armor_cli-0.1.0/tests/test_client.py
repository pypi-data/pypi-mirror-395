"""Tests for the Armor SDK Client."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from armor.client import Client
from armor.exceptions import (
    ArmorError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)


class TestClientInitialization:
    """Tests for client initialization."""

    def test_init_with_api_key(self):
        """Client initializes with explicit API key."""
        with patch("armor.client.httpx.Client"):
            client = Client(api_key="aa_live_test_key")  # pragma: allowlist secret
            assert client._api_key == "aa_live_test_key"  # pragma: allowlist secret

    def test_init_from_env_var(self, monkeypatch):
        """Client loads API key from environment variable."""
        monkeypatch.setenv("ARMOR_API_KEY", "aa_live_env_key")  # pragma: allowlist secret
        with patch("armor.client.httpx.Client"):
            client = Client()
            assert client._api_key == "aa_live_env_key"  # pragma: allowlist secret

    def test_init_without_api_key_raises(self, monkeypatch):
        """Client raises error when no API key available."""
        monkeypatch.delenv("ARMOR_API_KEY", raising=False)
        with patch("armor.config.load_config") as mock_config:
            mock_config.return_value = MagicMock(
                api_key=None, api_url="https://api.example.com", timeout=30
            )
            with pytest.raises(AuthenticationError):
                Client()

    def test_init_with_custom_url(self):
        """Client accepts custom API URL."""
        with patch("armor.client.httpx.Client"):
            # pragma: allowlist secret
            client = Client(api_key="aa_live_key", api_url="https://custom.api.com")
            assert client._api_url == "https://custom.api.com"

    def test_init_strips_trailing_slash(self):
        """API URL trailing slash is stripped."""
        with patch("armor.client.httpx.Client"):
            # pragma: allowlist secret
            client = Client(api_key="aa_live_key", api_url="https://api.com/")
            assert client._api_url == "https://api.com"

    def test_init_creates_resource_namespaces(self):
        """Client creates all resource namespaces."""
        with patch("armor.client.httpx.Client"):
            client = Client(api_key="aa_live_key")  # pragma: allowlist secret
            assert hasattr(client, "assets")
            assert hasattr(client, "freshness")
            assert hasattr(client, "schema")
            assert hasattr(client, "lineage")
            assert hasattr(client, "alerts")
            assert hasattr(client, "api_keys")


class TestClientHTTPHandling:
    """Tests for HTTP request handling."""

    @pytest.fixture
    def mock_client(self):
        """Create a client with mocked HTTP."""
        with patch("armor.client.httpx.Client") as mock_http:
            client = Client(api_key="aa_live_test_key")  # pragma: allowlist secret
            client._http = mock_http.return_value
            yield client

    def test_handles_401_as_auth_error(self, mock_client):
        """401 responses raise AuthenticationError."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": {"message": "Invalid API key"}}
        mock_client._http.request.return_value = mock_response

        with pytest.raises(AuthenticationError):
            mock_client._request("GET", "/test")

    def test_handles_403_as_forbidden(self, mock_client):
        """403 responses raise AuthenticationError."""
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.json.return_value = {"error": {"message": "Insufficient scope"}}
        mock_client._http.request.return_value = mock_response

        with pytest.raises(AuthenticationError) as exc_info:
            mock_client._request("GET", "/test")
        assert "Forbidden" in str(exc_info.value)

    def test_handles_404_as_not_found(self, mock_client):
        """404 responses raise NotFoundError."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"error": {"message": "Asset not found"}}
        mock_client._http.request.return_value = mock_response

        with pytest.raises(NotFoundError):
            mock_client._request("GET", "/test")

    def test_handles_422_as_validation_error(self, mock_client):
        """422 responses raise ValidationError."""
        mock_response = MagicMock()
        mock_response.status_code = 422
        mock_response.json.return_value = {"error": {"message": "Invalid parameter"}}
        mock_client._http.request.return_value = mock_response

        with pytest.raises(ValidationError):
            mock_client._request("GET", "/test")

    def test_handles_429_as_rate_limit_error(self, mock_client):
        """429 responses raise RateLimitError with retry_after."""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.json.return_value = {"error": {"message": "Rate limit exceeded"}}
        mock_response.headers = {"Retry-After": "30"}
        mock_client._http.request.return_value = mock_response

        with pytest.raises(RateLimitError) as exc_info:
            mock_client._request("GET", "/test")
        assert exc_info.value.retry_after == 30

    def test_handles_500_as_server_error(self, mock_client):
        """500 responses raise ServerError."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": {"message": "Internal error"}}
        mock_client._http.request.return_value = mock_response

        with pytest.raises(ServerError):
            mock_client._request("GET", "/test")

    def test_handles_timeout(self, mock_client):
        """Timeout raises ArmorError."""
        mock_client._http.request.side_effect = httpx.TimeoutException("Timeout")

        with pytest.raises(ArmorError) as exc_info:
            mock_client._request("GET", "/test")
        assert "timed out" in str(exc_info.value)

    def test_handles_network_error(self, mock_client):
        """Network error raises ArmorError."""
        mock_client._http.request.side_effect = httpx.NetworkError("Connection failed")

        with pytest.raises(ArmorError) as exc_info:
            mock_client._request("GET", "/test")
        assert "Network error" in str(exc_info.value)

    def test_successful_response_returns_data(self, mock_client):
        """Successful response returns parsed JSON."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"name": "test"}}
        mock_client._http.request.return_value = mock_response

        result = mock_client._request("GET", "/test")
        assert result == {"data": {"name": "test"}}


class TestClientContextManager:
    """Tests for client context manager support."""

    def test_context_manager_closes_client(self):
        """Client is closed when exiting context."""
        with patch("armor.client.httpx.Client") as mock_http:
            mock_instance = mock_http.return_value

            # pragma: allowlist secret
            with Client(api_key="aa_live_key") as _client:
                pass

            mock_instance.close.assert_called_once()

    def test_close_method(self):
        """Close method closes HTTP client."""
        with patch("armor.client.httpx.Client") as mock_http:
            mock_instance = mock_http.return_value
            client = Client(api_key="aa_live_key")  # pragma: allowlist secret
            client.close()
            mock_instance.close.assert_called_once()
