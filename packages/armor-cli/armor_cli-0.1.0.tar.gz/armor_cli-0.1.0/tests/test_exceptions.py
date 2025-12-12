"""Tests for SDK exceptions."""

from armor.exceptions import (
    ArmorError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    StalenessError,
    ValidationError,
)


class TestArmorError:
    """Tests for base ArmorError."""

    def test_basic_error(self):
        """Basic error with message."""
        error = ArmorError("Something went wrong")
        assert str(error) == "Something went wrong"

    def test_error_with_details(self):
        """Error with additional details."""
        error = ArmorError("Error", details={"key": "value"})
        assert error.details == {"key": "value"}


class TestAuthenticationError:
    """Tests for AuthenticationError."""

    def test_auth_error(self):
        """Authentication error with message."""
        error = AuthenticationError("Invalid API key")
        assert "Invalid API key" in str(error)
        assert isinstance(error, ArmorError)


class TestAuthorizationError:
    """Tests for AuthorizationError."""

    def test_authorization_error(self):
        """Authorization error with scope info."""
        error = AuthorizationError(
            "Insufficient scope",
            required_scope="read-write",
            current_scope="read-only",
        )
        assert error.required_scope == "read-write"
        assert error.current_scope == "read-only"


class TestNotFoundError:
    """Tests for NotFoundError."""

    def test_not_found_error(self):
        """Not found error with resource info."""
        error = NotFoundError("Asset not found", details={"asset_id": "test"})
        assert "Asset not found" in str(error)
        assert error.details["asset_id"] == "test"


class TestRateLimitError:
    """Tests for RateLimitError."""

    def test_rate_limit_error(self):
        """Rate limit error with retry info."""
        error = RateLimitError("Rate limited", retry_after=30)
        assert error.retry_after == 30
        assert "Rate limited" in str(error)

    def test_default_retry_after(self):
        """Default retry_after is None when not specified."""
        error = RateLimitError("Rate limited")
        assert error.retry_after is None


class TestValidationError:
    """Tests for ValidationError."""

    def test_validation_error(self):
        """Validation error with field details."""
        error = ValidationError(
            "Invalid request",
            details={"field": "limit", "error": "must be positive"},
        )
        assert "Invalid request" in str(error)
        assert error.details["field"] == "limit"


class TestServerError:
    """Tests for ServerError."""

    def test_server_error(self):
        """Server error with status code."""
        error = ServerError("Internal error", status_code=500)
        assert error.status_code == 500
        assert "Internal error" in str(error)


class TestStalenessError:
    """Tests for StalenessError."""

    def test_staleness_error(self):
        """Staleness error with asset info."""
        error = StalenessError(
            asset="snowflake.prod.orders",
            hours_since_update=26.5,
            threshold_hours=24,
        )

        assert error.asset == "snowflake.prod.orders"
        assert error.hours_since_update == 26.5
        assert error.threshold_hours == 24
        assert "stale" in str(error).lower()

    def test_staleness_error_minimal(self):
        """StalenessError with just asset name."""
        error = StalenessError(asset="test")
        assert error.asset == "test"
        assert error.hours_since_update is None
        assert "stale" in str(error).lower()

    def test_staleness_error_in_exception_chain(self):
        """StalenessError inherits from ArmorError."""
        error = StalenessError(asset="test")
        assert isinstance(error, ArmorError)
