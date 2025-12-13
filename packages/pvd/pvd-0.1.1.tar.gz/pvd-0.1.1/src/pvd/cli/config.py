"""
Configuration management for Paved CLI.
Handles storing and retrieving user credentials and platform settings.
"""
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any


class Config:
    """Manages CLI configuration stored in ~/.paved/config.json"""

    def __init__(self):
        self.config_dir = Path.home() / ".paved"
        self.config_file = self.config_dir / "config.json"
        self._ensure_config_dir()
        self._config = self._load_config()

    def _ensure_config_dir(self):
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def _load_config(self) -> Dict[str, Any]:
        if not self.config_file.exists():
            return {}
        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}

    def _save_config(self):
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, "w") as f:
            json.dump(self._config, f, indent=2)
        try:
            os.chmod(self.config_file, 0o600)
        except Exception:
            pass

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    def set(self, key: str, value: Any):
        self._config[key] = value
        self._save_config()

    def remove(self, key: str):
        if key in self._config:
            del self._config[key]
            self._save_config()

    def clear(self):
        self._config = {}
        self._save_config()

    @property
    def api_key(self) -> Optional[str]:
        return self.get("api_key")

    @api_key.setter
    def api_key(self, value: str):
        self.set("api_key", value)

    @property
    def platform_url(self) -> str:
        return self.get("platform_url", "https://app.hipaved.com")

    @platform_url.setter
    def platform_url(self, value: str):
        self.set("platform_url", value)

    @property
    def user_email(self) -> Optional[str]:
        return self.get("user_email")

    @user_email.setter
    def user_email(self, value: str):
        self.set("user_email", value)

    @property
    def user_id(self) -> Optional[str]:
        return self.get("user_id")

    @user_id.setter
    def user_id(self, value: str):
        self.set("user_id", value)

    def is_authenticated(self) -> bool:
        return self.api_key is not None and self.user_email is not None


# Global config instance
config = Config()
