"""Configuration management for DumpConfluence"""

import json
import os
import platform
from pathlib import Path
from typing import Dict, List, Optional


class ConfigManager:
    """Manage profiles and configuration"""

    def __init__(self) -> None:
        # Determine config directory based on OS
        if platform.system() == "Windows":
            config_home = Path(
                os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")
            )
        else:
            config_home = Path(
                os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")
            )

        self.config_dir = config_home / "dumpconfluence"
        self.config_file = self.config_dir / "config.json"

        # Create config directory if it doesn't exist
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Load existing config or create empty
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file) as f:
                    return json.load(f)
            except Exception:
                return {"profiles": {}}
        return {"profiles": {}}

    def _save_config(self) -> None:
        """Save configuration to file"""
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=2)

    def save_profile(self, name: str, url: str, email: str, token: str) -> None:
        """Save a profile with credentials"""
        self.config["profiles"][name] = {"url": url, "email": email, "token": token}
        self._save_config()

    def load_profile(self, name: str) -> Optional[Dict]:
        """Load a profile by name"""
        return self.config["profiles"].get(name)

    def remove_profile(self, name: str) -> bool:
        """Remove a profile"""
        if name in self.config["profiles"]:
            del self.config["profiles"][name]
            self._save_config()
            return True
        return False

    def list_profiles(self) -> List[str]:
        """List all profile names"""
        return list(self.config["profiles"].keys())

    def set_default_profile(self, name: str) -> bool:
        """Set a profile as default"""
        if name in self.config["profiles"]:
            self.config["default_profile"] = name
            self._save_config()
            return True
        return False

    def get_default_profile(self) -> Optional[str]:
        """Get the default profile name"""
        return self.config.get("default_profile")

    def get_auto_profile(self) -> Optional[Dict]:
        """Get profile to use automatically (single profile or default)"""
        profiles = self.list_profiles()

        # If only one profile exists, use it
        if len(profiles) == 1:
            return self.load_profile(profiles[0])

        # If multiple profiles, use default if set
        default = self.get_default_profile()
        if default:
            return self.load_profile(default)

        return None
