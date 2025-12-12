"""Tests for SDK configuration management."""

from pathlib import Path
from unittest.mock import patch

import pytest

from armor.config import (
    DEFAULT_API_URL,
    Config,
    clear_config,
    get_config_path,
    load_config,
    save_config,
)


class TestConfig:
    """Tests for Config model."""

    def test_default_values(self):
        """Config has sensible defaults."""
        config = Config()
        assert config.api_key is None
        assert config.api_url == DEFAULT_API_URL
        assert config.timeout == 30
        assert config.retry_attempts == 3

    def test_custom_values(self):
        """Config accepts custom values."""
        config = Config(
            api_key="aa_live_test",  # pragma: allowlist secret
            api_url="https://custom.api.com",
            timeout=60,
            retry_attempts=5,
        )
        assert config.api_key == "aa_live_test"  # pragma: allowlist secret
        assert config.api_url == "https://custom.api.com"
        assert config.timeout == 60
        assert config.retry_attempts == 5


class TestGetConfigPath:
    """Tests for get_config_path function."""

    def test_returns_path_in_home_directory(self):
        """Config path is in user's home directory."""
        path = get_config_path()
        assert path.parent.name == ".armor"
        assert path.name == "config.yaml"
        assert str(Path.home()) in str(path)


class TestLoadConfig:
    """Tests for load_config function."""

    def test_loads_from_environment_variables(self, monkeypatch, tmp_path):
        """Environment variables take priority."""
        # Set env vars
        monkeypatch.setenv("ARMOR_API_KEY", "aa_live_env")  # pragma: allowlist secret
        monkeypatch.setenv("ARMOR_API_URL", "https://env.api.com")
        monkeypatch.setenv("ARMOR_TIMEOUT", "45")

        # Mock config path to temp directory
        config_file = tmp_path / "config.yaml"
        config_file.write_text("api_key: aa_live_file\napi_url: https://file.api.com")

        with patch("armor.config.get_config_path", return_value=config_file):
            config = load_config()

        # Env vars should win
        assert config.api_key == "aa_live_env"  # pragma: allowlist secret
        assert config.api_url == "https://env.api.com"
        assert config.timeout == 45

    def test_loads_from_config_file(self, monkeypatch, tmp_path):
        """Loads from config file when no env vars."""
        # Clear env vars
        monkeypatch.delenv("ARMOR_API_KEY", raising=False)
        monkeypatch.delenv("ARMOR_API_URL", raising=False)

        # Create config file
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            "api_key: aa_live_file_key\n"  # pragma: allowlist secret
            "api_url: https://file.api.com\n"
            "timeout: 60\n"
        )

        with patch("armor.config.get_config_path", return_value=config_file):
            config = load_config()

        assert config.api_key == "aa_live_file_key"  # pragma: allowlist secret
        assert config.api_url == "https://file.api.com"
        assert config.timeout == 60

    def test_uses_defaults_when_no_config(self, monkeypatch, tmp_path):
        """Uses defaults when no env vars or config file."""
        # Clear env vars
        monkeypatch.delenv("ARMOR_API_KEY", raising=False)
        monkeypatch.delenv("ARMOR_API_URL", raising=False)

        # Non-existent config file
        config_file = tmp_path / "nonexistent.yaml"

        with patch("armor.config.get_config_path", return_value=config_file):
            config = load_config()

        assert config.api_key is None
        assert config.api_url == DEFAULT_API_URL
        assert config.timeout == 30

    def test_handles_empty_config_file(self, monkeypatch, tmp_path):
        """Handles empty config file gracefully."""
        monkeypatch.delenv("ARMOR_API_KEY", raising=False)

        config_file = tmp_path / "config.yaml"
        config_file.write_text("")

        with patch("armor.config.get_config_path", return_value=config_file):
            config = load_config()

        assert config.api_key is None
        assert config.api_url == DEFAULT_API_URL

    def test_handles_malformed_yaml(self, monkeypatch, tmp_path):
        """Malformed YAML raises yaml.YAMLError."""
        import yaml

        monkeypatch.delenv("ARMOR_API_KEY", raising=False)

        config_file = tmp_path / "config.yaml"
        config_file.write_text("this is: not: valid: yaml: [")

        with patch("armor.config.get_config_path", return_value=config_file):
            # yaml.safe_load raises YAMLError for invalid YAML
            with pytest.raises(yaml.YAMLError):
                load_config()


class TestSaveConfig:
    """Tests for save_config function."""

    def test_saves_api_key_to_file(self, tmp_path):
        """Saves API key to config file."""
        config_file = tmp_path / "config.yaml"

        config = Config(api_key="aa_live_save_test")  # pragma: allowlist secret

        with patch("armor.config.get_config_path", return_value=config_file):
            save_config(config)

        assert config_file.exists()
        content = config_file.read_text()
        assert "aa_live_save_test" in content  # pragma: allowlist secret

    def test_saves_custom_api_url(self, tmp_path):
        """Saves custom API URL to config file."""
        config_file = tmp_path / "config.yaml"

        config = Config(
            api_key="aa_live_test",  # pragma: allowlist secret
            api_url="https://custom.api.com",
        )

        with patch("armor.config.get_config_path", return_value=config_file):
            save_config(config)

        content = config_file.read_text()
        assert "https://custom.api.com" in content

    def test_does_not_save_default_api_url(self, tmp_path):
        """Does not save default API URL (to keep config minimal)."""
        config_file = tmp_path / "config.yaml"

        config = Config(
            api_key="aa_live_test",  # pragma: allowlist secret
            api_url=DEFAULT_API_URL,  # Default
        )

        with patch("armor.config.get_config_path", return_value=config_file):
            save_config(config)

        content = config_file.read_text()
        assert DEFAULT_API_URL not in content

    def test_sets_secure_permissions(self, tmp_path):
        """Config file has secure permissions (0600)."""
        config_file = tmp_path / "config.yaml"

        config = Config(api_key="aa_live_test")  # pragma: allowlist secret

        with patch("armor.config.get_config_path", return_value=config_file):
            save_config(config)

        # Check permissions (Unix only)
        mode = config_file.stat().st_mode & 0o777
        assert mode == 0o600


class TestClearConfig:
    """Tests for clear_config function."""

    def test_removes_config_file(self, tmp_path):
        """Removes config file on logout."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("api_key: test")

        with patch("armor.config.get_config_path", return_value=config_file):
            clear_config()

        assert not config_file.exists()

    def test_handles_nonexistent_file(self, tmp_path):
        """Handles nonexistent config file gracefully."""
        config_file = tmp_path / "nonexistent.yaml"

        with patch("armor.config.get_config_path", return_value=config_file):
            # Should not raise
            clear_config()


class TestConfigPriority:
    """Tests for configuration priority (env > file > defaults)."""

    def test_env_overrides_file(self, monkeypatch, tmp_path):
        """Environment variables override file config."""
        # Set env var
        monkeypatch.setenv("ARMOR_API_KEY", "aa_live_env_wins")  # pragma: allowlist secret

        # Create config file with different value
        config_file = tmp_path / "config.yaml"
        config_file.write_text("api_key: aa_live_file_loses")  # pragma: allowlist secret

        with patch("armor.config.get_config_path", return_value=config_file):
            config = load_config()

        assert config.api_key == "aa_live_env_wins"  # pragma: allowlist secret

    def test_file_overrides_defaults(self, monkeypatch, tmp_path):
        """File config overrides defaults."""
        monkeypatch.delenv("ARMOR_API_KEY", raising=False)

        config_file = tmp_path / "config.yaml"
        config_file.write_text("timeout: 120\n")

        with patch("armor.config.get_config_path", return_value=config_file):
            config = load_config()

        # File value (120) overrides default (30)
        assert config.timeout == 120
