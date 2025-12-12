"""AnomalyArmor SDK for Python.

The armor SDK provides programmatic access to AnomalyArmor's data observability platform.

Quick Start:
    >>> from armor import Client
    >>> client = Client(api_key="aa_live_...")
    >>>
    >>> # List assets
    >>> assets = client.assets.list()
    >>> for asset in assets:
    ...     print(asset.qualified_name)
    >>>
    >>> # Check freshness
    >>> freshness = client.freshness.get("postgresql.mydb.public.users")
    >>> if freshness.is_stale:
    ...     print(f"Stale for {freshness.hours_since_update} hours")

Environment Variables:
    ARMOR_API_KEY: Your API key (alternative to passing in code)
    ARMOR_API_URL: API base URL (default: https://api.anomalyarmor.ai/api/v1)
"""

from armor.client import Client
from armor.exceptions import (
    ArmorError,
    AuthenticationError,
    DataStaleError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from armor.models import (
    Alert,
    Asset,
    FreshnessStatus,
    LineageGraph,
    SchemaChange,
)

__version__ = "0.1.0"

__all__ = [
    "Client",
    # Exceptions
    "ArmorError",
    "AuthenticationError",
    "DataStaleError",
    "NotFoundError",
    "RateLimitError",
    "ValidationError",
    # Models
    "Asset",
    "FreshnessStatus",
    "SchemaChange",
    "LineageGraph",
    "Alert",
]
