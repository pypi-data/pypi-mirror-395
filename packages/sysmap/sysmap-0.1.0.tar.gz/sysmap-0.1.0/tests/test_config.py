"""Tests for configuration module."""

import pytest
import tempfile
import yaml
from pathlib import Path
from sysmap.core.config import Config


class TestConfig:
    """Test Config class."""

    def test_default_config(self):
        """Test loading default configuration."""
        config = Config()
        assert config.get("scanners.winget") is True
        assert config.get("scanners.pip") is True
        assert config.get("output.format") == "markdown"

    def test_load_from_file(self, tmp_path):
        """Test loading configuration from file."""
        config_file = tmp_path / ".sysmap.yaml"
        config_data = {
            "scanners": {
                "winget": False,
                "pip": True,
            },
            "output": {
                "format": "json",
            },
        }

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        config = Config(str(config_file))
        assert config.get("scanners.winget") is False
        assert config.get("scanners.pip") is True
        assert config.get("output.format") == "json"

    def test_get_nested_value(self):
        """Test getting nested configuration values."""
        config = Config()
        value = config.get("scanners.winget")
        assert value is True

        value = config.get("nonexistent.key", "default")
        assert value == "default"

    def test_set_value(self):
        """Test setting configuration values."""
        config = Config()
        config.set("scanners.winget", False)
        assert config.get("scanners.winget") is False

    def test_save_config(self, tmp_path):
        """Test saving configuration to file."""
        config_file = tmp_path / "test_config.yaml"
        config = Config()
        config.set("scanners.winget", False)
        config.save(str(config_file))

        # Load and verify
        with open(config_file) as f:
            data = yaml.safe_load(f)

        assert data["scanners"]["winget"] is False

    def test_create_default_config(self, tmp_path):
        """Test creating default configuration file."""
        config_file = tmp_path / "default.yaml"
        Config.create_default_config(str(config_file))

        assert config_file.exists()

        with open(config_file) as f:
            data = yaml.safe_load(f)

        assert "scanners" in data
        assert "output" in data
