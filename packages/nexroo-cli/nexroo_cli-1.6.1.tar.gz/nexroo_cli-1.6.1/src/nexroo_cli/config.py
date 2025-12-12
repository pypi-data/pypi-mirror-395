import json
import os
from pathlib import Path
from typing import Optional, Dict, Any


class Config:
    CONFIG_DIR = Path.home() / ".nexroo"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    GITHUB_TOKEN_ENV_VAR = "NEXROO_CLI_GIT_PAT"

    def __init__(self):
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self._config = self._load()

    def _load(self) -> Dict[str, Any]:
        if self.CONFIG_FILE.exists():
            try:
                return json.loads(self.CONFIG_FILE.read_text())
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def _save(self):
        self.CONFIG_FILE.write_text(json.dumps(self._config, indent=2))

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    def set(self, key: str, value: Any):
        self._config[key] = value
        self._save()

    def delete(self, key: str) -> bool:
        if key in self._config:
            del self._config[key]
            self._save()
            return True
        return False

    def all(self) -> Dict[str, Any]:
        return self._config.copy()

    def get_engine_path(self) -> Optional[str]:
        return self.get("engine_path")

    def set_engine_path(self, path: str):
        self.set("engine_path", path)

    def get_github_token(self) -> Optional[str]:
        token = os.environ.get(self.GITHUB_TOKEN_ENV_VAR)
        if token:
            return token
        return self.get("github_token")

    def set_github_token(self, token: str):
        self.set("github_token", token)
