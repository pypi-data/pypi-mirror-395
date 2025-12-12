"""Configuration management for the Armor SDK and CLI."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

# Default API URL - use this constant throughout the SDK
DEFAULT_API_URL = "https://api.anomalyarmor.ai/api/v1"


class Config(BaseModel):
    """SDK configuration."""

    api_key: str | None = Field(None, description="API key for authentication")
    api_url: str = Field(
        DEFAULT_API_URL,
        description="Base URL for API requests",
    )
    timeout: int = Field(30, description="Request timeout in seconds")
    retry_attempts: int = Field(3, description="Number of retry attempts")


def get_config_path() -> Path:
    """Get the path to the config file."""
    config_dir = Path.home() / ".armor"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.yaml"


def load_config() -> Config:
    """Load configuration from file and environment.

    Priority (highest to lowest):
    1. Environment variables (ARMOR_API_KEY, ARMOR_API_URL)
    2. Config file (~/.armor/config.yaml)
    3. Defaults
    """
    config_path = get_config_path()

    # Load from file if exists
    file_config: dict[str, Any] = {}
    if config_path.exists():
        with open(config_path) as f:
            file_config = yaml.safe_load(f) or {}

    # Build config with environment overrides
    return Config(
        api_key=os.environ.get("ARMOR_API_KEY", file_config.get("api_key")),
        api_url=os.environ.get(
            "ARMOR_API_URL",
            file_config.get("api_url", DEFAULT_API_URL),
        ),
        timeout=int(os.environ.get("ARMOR_TIMEOUT", file_config.get("timeout", 30))),
        retry_attempts=int(
            os.environ.get("ARMOR_RETRY_ATTEMPTS", file_config.get("retry_attempts", 3))
        ),
    )


def save_config(config: Config) -> None:
    """Save configuration to file with secure permissions.

    The config file contains sensitive API keys and is created with
    mode 0600 (owner read/write only) to prevent other users from
    reading the credentials.
    """
    config_path = get_config_path()

    # Only save non-sensitive, non-default values
    data: dict[str, Any] = {}
    if config.api_key:
        data["api_key"] = config.api_key
    if config.api_url != DEFAULT_API_URL:
        data["api_url"] = config.api_url

    # Write with restrictive permissions (0600 = owner read/write only)
    # This prevents other users on the system from reading the API key
    with open(config_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False)

    # Set file permissions to 0600 (rw-------)
    config_path.chmod(0o600)


def clear_config() -> None:
    """Clear stored configuration (logout)."""
    config_path = get_config_path()
    if config_path.exists():
        config_path.unlink()
