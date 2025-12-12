"""Configuration management for SysMap."""

import os
from pathlib import Path
from typing import Any, Dict, Optional
import yaml


class Config:
    """Configuration manager for SysMap."""

    DEFAULT_CONFIG = {
        "scanners": {
            "winget": True,
            "pip": True,
            "npm": True,
            "brew": True,
            "chocolatey": True,
            "scoop": True,
            "snap": True,
            "flatpak": True,
        },
        "output": {
            "format": "markdown",
            "path": "SYSTEM_SUMMARY.md",
        },
        "features": {
            "check_updates": False,
            "security_scan": False,
        },
        "plugins": [],
    }

    def __init__(self, config_path: Optional[str] = None) -> None:
        """Initialize configuration from file or defaults."""
        self.config_path = config_path or self._find_config_file()
        self.data = self._load_config()

    def _find_config_file(self) -> Optional[str]:
        """Search for config file in standard locations."""
        search_paths = [
            Path.cwd() / ".sysmap.yaml",
            Path.cwd() / ".sysmap.yml",
            Path.cwd() / "sysmap.yaml",
            Path.home() / ".sysmap.yaml",
            Path.home() / ".config" / "sysmap" / "config.yaml",
        ]

        for path in search_paths:
            if path.exists():
                return str(path)

        return None

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or return defaults."""
        if self.config_path and os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    user_config = yaml.safe_load(f) or {}
                    # Merge with defaults
                    return self._merge_configs(self.DEFAULT_CONFIG, user_config)
            except (yaml.YAMLError, IOError):
                pass

        return self.DEFAULT_CONFIG.copy()

    def _merge_configs(self, default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge user config with defaults."""
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation."""
        keys = key.split(".")
        value = self.data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value using dot notation."""
        keys = key.split(".")
        config = self.data
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value

    def save(self, path: Optional[str] = None) -> None:
        """Save current configuration to file."""
        save_path = path or self.config_path or ".sysmap.yaml"
        with open(save_path, "w", encoding="utf-8") as f:
            yaml.dump(self.data, f, default_flow_style=False, sort_keys=False)

    @classmethod
    def create_default_config(cls, path: str = ".sysmap.yaml") -> None:
        """Create a default configuration file."""
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(cls.DEFAULT_CONFIG, f, default_flow_style=False, sort_keys=False)
