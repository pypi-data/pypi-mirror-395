"""Exception classes for the Armor SDK."""

from __future__ import annotations

from typing import Any


class ArmorError(Exception):
    """Base exception for all Armor SDK errors."""

    def __init__(
        self,
        message: str,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}

    def __str__(self) -> str:
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message


class AuthenticationError(ArmorError):
    """Raised when authentication fails."""

    def __init__(
        self,
        message: str = "Authentication failed",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, code="UNAUTHORIZED", details=details)


class AuthorizationError(ArmorError):
    """Raised when authorization fails (valid auth but insufficient permissions)."""

    def __init__(
        self,
        message: str = "Authorization failed",
        required_scope: str | None = None,
        current_scope: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, code="FORBIDDEN", details=details)
        self.required_scope = required_scope
        self.current_scope = current_scope


class RateLimitError(ArmorError):
    """Raised when rate limit is exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: int | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, code="RATE_LIMIT_EXCEEDED", details=details)
        self.retry_after = retry_after


class NotFoundError(ArmorError):
    """Raised when a resource is not found."""

    def __init__(
        self,
        message: str = "Resource not found",
        resource_type: str | None = None,
        resource_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, code="NOT_FOUND", details=details)
        self.resource_type = resource_type
        self.resource_id = resource_id


class ValidationError(ArmorError):
    """Raised when request validation fails."""

    def __init__(
        self,
        message: str = "Validation error",
        field_errors: dict[str, str] | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, code="VALIDATION_ERROR", details=details)
        self.field_errors = field_errors or {}


class ServerError(ArmorError):
    """Raised when the server returns an error."""

    def __init__(
        self,
        message: str = "Server error",
        status_code: int = 500,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, code="SERVER_ERROR", details=details)
        self.status_code = status_code


class StalenessError(ArmorError):
    """Raised when data freshness requirement is not met.

    This exception is raised by require_fresh() when an asset's data
    is older than the specified threshold.

    Attributes:
        asset: The qualified name of the stale asset
        hours_since_update: Hours since the last update
        threshold_hours: The freshness threshold that was exceeded
    """

    def __init__(
        self,
        asset: str,
        hours_since_update: float | None = None,
        threshold_hours: float | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        if hours_since_update is not None and threshold_hours is not None:
            message = (
                f"Asset '{asset}' is stale: "
                f"{hours_since_update:.1f}h since last update "
                f"(threshold: {threshold_hours:.1f}h)"
            )
        else:
            message = f"Asset '{asset}' is stale"
        super().__init__(message, code="DATA_STALE", details=details)
        self.asset = asset
        self.asset_id = asset  # Alias for backwards compatibility
        self.hours_since_update = hours_since_update
        self.threshold_hours = threshold_hours


# Backwards compatibility alias
DataStaleError = StalenessError
