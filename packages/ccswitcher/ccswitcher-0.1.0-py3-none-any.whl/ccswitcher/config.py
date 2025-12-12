"""Configuration management for CCswitcher."""

import os
from pathlib import Path
from typing import Dict, Optional

import yaml


class Config:
    """Manages CCswitcher configuration."""

    def __init__(self):
        self.config_dir = Path.home() / ".config" / "ccswitcher"
        self.config_file = self.config_dir / "settings.yml"
        self.claude_dir = Path.home() / ".claude"
        self.claude_settings = self.claude_dir / "settings.json"
        self._ensure_config_dir()

    def _ensure_config_dir(self):
        """Create config directory if it doesn't exist."""
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def load_config(self) -> Dict[str, str]:
        """Load configuration from settings.yml."""
        if not self.config_file.exists():
            return {}

        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f) or {}

    def save_config(self, config: Dict[str, str]):
        """Save configuration to settings.yml."""
        with open(self.config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

    def add_profile(self, name: str, path: str):
        """Add or update a profile in the configuration."""
        config = self.load_config()
        expanded_path = os.path.expanduser(path)
        config[name] = expanded_path
        self.save_config(config)

    def get_profile_path(self, name: str) -> Optional[str]:
        """Get the path for a profile."""
        config = self.load_config()
        return config.get(name)

    def list_profiles(self) -> Dict[str, str]:
        """List all configured profiles."""
        return self.load_config()
