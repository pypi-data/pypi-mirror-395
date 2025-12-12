import sys
import importlib
from pathlib import Path
from typing import Dict, Optional, Any
from loguru import logger


class AddonLoader:
    def __init__(self, plugin_dir: Optional[Path] = None):
        self.plugin_dir = plugin_dir or Path.home() / ".nexroo" / "plugins"
        self.cache: Dict[str, Any] = {}
        self._initialized = False

    def _init_sys_path(self):
        if self._initialized:
            return

        if self.plugin_dir.exists() and str(self.plugin_dir) not in sys.path:
            sys.path.insert(0, str(self.plugin_dir))
            logger.debug(f"Added {self.plugin_dir} to sys.path")

        self._initialized = True

    def _is_bundled(self, name: str) -> bool:
        try:
            spec = importlib.util.find_spec(name)
            if spec and spec.origin:
                return "frozen" in spec.origin or ".exe" in spec.origin
            return False
        except (ImportError, ValueError, AttributeError):
            return False

    def _is_in_plugin_dir(self, name: str) -> bool:
        module_name = name.replace("-", "_")
        plugin_path = self.plugin_dir / module_name
        return plugin_path.exists()

    def load(self, name: str, lazy: bool = True) -> Optional[Any]:
        if name in self.cache:
            logger.debug(f"Loaded {name} from cache")
            return self.cache[name]

        self._init_sys_path()

        module_name = name.replace("-", "_")

        try:
            if self._is_bundled(module_name):
                logger.debug(f"Loading {name} (bundled)")
                module = importlib.import_module(module_name)
            elif self._is_in_plugin_dir(name):
                logger.debug(f"Loading {name} (plugin)")
                module = importlib.import_module(module_name)
            else:
                logger.debug(f"Loading {name} (system)")
                module = importlib.import_module(module_name)

            self.cache[name] = module
            return module

        except ImportError as e:
            logger.error(f"Failed to load addon '{name}': {e}")
            return None

    def preload(self, names: list[str]):
        for name in names:
            try:
                self.load(name)
                logger.debug(f"Preloaded {name}")
            except Exception as e:
                logger.debug(f"Failed to preload {name}: {e}")

    def clear_cache(self):
        self.cache.clear()

    def is_loaded(self, name: str) -> bool:
        return name in self.cache
