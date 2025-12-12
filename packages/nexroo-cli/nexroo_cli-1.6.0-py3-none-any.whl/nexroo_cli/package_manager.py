import sys
import subprocess
import json
import compileall
import shutil
import site
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from loguru import logger
import importlib.metadata
import httpx


class PackageRegistry:
    GITHUB_ORG = "nexroo-ai"
    CACHE_FILE = Path.home() / ".nexroo" / "package_cache.json"
    CACHE_TTL = 3600  # 1 hour

    @classmethod
    def _fetch_from_github(cls) -> List[Dict]:
        try:
            url = f"https://api.github.com/orgs/{cls.GITHUB_ORG}/repos"
            response = httpx.get(url, params={"per_page": 100}, timeout=10.0)
            response.raise_for_status()

            repos = response.json()
            packages = []

            for repo in repos:
                name = repo["name"]
                if name.endswith("-rooms-pkg"):
                    packages.append({
                        "name": name,
                        "description": repo.get("description", ""),
                        "url": f"git+https://github.com/{cls.GITHUB_ORG}/{name}.git",
                        "stars": repo.get("stargazers_count", 0),
                        "updated_at": repo.get("updated_at", "")
                    })

            return packages
        except Exception as e:
            logger.warning(f"Failed to fetch packages from GitHub: {e}")
            return []

    @classmethod
    def _load_cache(cls) -> Optional[Dict]:
        if not cls.CACHE_FILE.exists():
            return None

        try:
            with open(cls.CACHE_FILE) as f:
                cache = json.load(f)

            cached_at = datetime.fromisoformat(cache["cached_at"])
            age = (datetime.now() - cached_at).total_seconds()

            if age < cls.CACHE_TTL:
                return cache

            return None
        except Exception:
            return None

    @classmethod
    def _save_cache(cls, packages: List[Dict]):
        try:
            cls.CACHE_FILE.parent.mkdir(exist_ok=True, parents=True)
            with open(cls.CACHE_FILE, 'w') as f:
                json.dump({
                    "cached_at": datetime.now().isoformat(),
                    "packages": packages
                }, f, indent=2)
        except Exception as e:
            logger.debug(f"Failed to save cache: {e}")

    @classmethod
    def get_packages(cls, refresh: bool = False) -> List[Dict]:
        if not refresh:
            cache = cls._load_cache()
            if cache:
                logger.debug("Using cached package list")
                return cache["packages"]

        logger.debug(f"Fetching packages from GitHub ({cls.GITHUB_ORG})...")
        packages = cls._fetch_from_github()

        if packages:
            cls._save_cache(packages)

        return packages

    @classmethod
    def get_package(cls, name: str) -> Optional[Dict]:
        packages = cls.get_packages()
        for pkg in packages:
            if pkg["name"] == name:
                return pkg
        return None

    @classmethod
    def search_packages(cls, query: str) -> List[Dict]:
        packages = cls.get_packages()
        query_lower = query.lower()
        return [
            pkg for pkg in packages
            if query_lower in pkg["name"].lower() or query_lower in pkg["description"].lower()
        ]


class PackageManager:
    def __init__(self):
        self.registry = PackageRegistry()
        self.config_dir = Path.home() / ".nexroo"
        self.config_dir.mkdir(exist_ok=True, parents=True)

        self.plugin_dir = self.config_dir / "plugins"
        self.plugin_dir.mkdir(exist_ok=True, parents=True)

        self.installed_file = self.config_dir / "installed_packages.json"
        self.system_python = self._detect_system_python()

    def _normalize_package_name(self, name: str) -> str:
        if name.endswith("-rooms-pkg"):
            return name
        return f"{name}-rooms-pkg"

    def _detect_system_python(self) -> Optional[Tuple[str, str]]:
        python_candidates = ['python3', 'python', 'python3.11', 'python3.12', 'python3.13']

        logger.debug(f"Searching for system Python among: {python_candidates}")
        for cmd in python_candidates:
            python_path = shutil.which(cmd)
            logger.debug(f"Checking '{cmd}': {python_path}")
            if python_path:
                try:
                    result = subprocess.run(
                        [python_path, '--version'],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        version_str = result.stdout.strip() or result.stderr.strip()
                        logger.debug(f"Found system Python: {python_path} ({version_str})")
                        return (python_path, version_str)
                except Exception as e:
                    logger.debug(f"Failed to check {python_path}: {e}")
                    continue

        logger.warning("No system Python installation found")
        return None

    def get_system_python_site_packages(self) -> Optional[str]:
        if not self.system_python:
            logger.debug("No system Python detected")
            return None

        python_path = self.system_python[0]
        logger.debug(f"Getting site-packages from: {python_path}")
        try:
            result = subprocess.run(
                [python_path, '-c', 'import sysconfig; print(sysconfig.get_path("purelib"))'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                site_packages = result.stdout.strip()
                logger.debug(f"System Python site-packages: {site_packages}")
                return site_packages
            else:
                logger.warning(f"Failed to get site-packages: {result.stderr}")
        except Exception as e:
            logger.warning(f"Failed to get site-packages: {e}")

        return None

    def _load_installed(self) -> Dict:
        if not self.installed_file.exists():
            return {}
        try:
            with open(self.installed_file) as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load installed packages: {e}")
            return {}

    def _save_installed(self, installed: Dict):
        try:
            with open(self.installed_file, 'w') as f:
                json.dump(installed, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save installed packages: {e}")

    def _is_in_plugin_dir(self, package_name: str) -> bool:
        pkg_dir = self.plugin_dir / package_name.replace("-", "_")
        if pkg_dir.exists() and pkg_dir.is_dir():
            return True

        dist_info_pattern = f"{package_name.replace('-', '_')}*.dist-info"
        matches = list(self.plugin_dir.glob(dist_info_pattern))
        return len(matches) > 0

    def is_installed(self, package_name: str) -> bool:
        if self._is_in_plugin_dir(package_name):
            return True

        try:
            importlib.metadata.version(package_name)
            return True
        except importlib.metadata.PackageNotFoundError:
            return False

    def get_installed_version(self, package_name: str) -> Optional[str]:
        try:
            return importlib.metadata.version(package_name)
        except importlib.metadata.PackageNotFoundError:
            installed = self._load_installed()
            if package_name in installed:
                return installed[package_name].get("version", "unknown")
            return None

    def get_installed_location(self, package_name: str) -> Optional[str]:
        if self._is_in_plugin_dir(package_name):
            return "plugin"

        try:
            dist = importlib.metadata.distribution(package_name)
            if str(self.plugin_dir) in str(dist._path):
                return "plugin"
            return "bundled"
        except importlib.metadata.PackageNotFoundError:
            return None

    def list_installed(self) -> List[Dict]:
        installed_meta = self._load_installed()
        result = []
        seen = set()

        for name, info in installed_meta.items():
            version = info.get("version", "unknown")
            try:
                dist = importlib.metadata.distribution(name)
                version = dist.version
            except importlib.metadata.PackageNotFoundError:
                pass

            result.append({
                "name": name,
                "version": version,
                "description": info.get("description", ""),
                "installed_at": info.get("installed_at", ""),
                "location": "installed"
            })
            seen.add(name)

        for dist in importlib.metadata.distributions():
            name = dist.metadata.get("Name", "")
            if name.endswith("-rooms-pkg") and name not in seen:
                version = dist.version
                description = dist.metadata.get("Summary", "")
                result.append({
                    "name": name,
                    "version": version,
                    "description": description,
                    "installed_at": "unknown",
                    "location": "bundled"
                })
                seen.add(name)

        return result

    async def install(self, package_name: str, version: Optional[str] = None,
                     url: Optional[str] = None, upgrade: bool = False) -> bool:
        package_name = self._normalize_package_name(package_name)

        if not self.system_python:
            logger.error("No system Python installation found")
            logger.info("Please install Python 3.11+ to use addon packages")
            logger.info("  Windows: https://www.python.org/downloads/")
            logger.info("  Linux: apt install python3 / yum install python3")
            logger.info("  macOS: brew install python3")
            return False

        package_info = self.registry.get_package(package_name)

        if not package_info and not url:
            logger.error(f"Package '{package_name}' not found in registry")
            logger.info("Run 'nexroo addon search' to see available packages")
            logger.info("Or provide a custom URL with --url")
            return False

        if self.is_installed(package_name) and not upgrade:
            current_version = self.get_installed_version(package_name)
            location = self.get_installed_location(package_name)
            logger.warning(f"Package '{package_name}' v{current_version} is already installed ({location})")
            logger.info("Use --upgrade to update the package")
            return False

        install_url = url or package_info["url"]

        python_path = self.system_python[0]
        cmd = [python_path, "-m", "pip", "install"]

        if upgrade:
            cmd.append("--upgrade")

        if version and not url:
            cmd.append(f"{package_name}=={version}")
        else:
            cmd.append(install_url)

        logger.info(f"Installing {package_name}...")
        logger.debug(f"Using Python: {python_path}")
        logger.debug(f"Command: {' '.join(cmd)}")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.debug(result.stdout)

            installed_version = self.get_installed_version(package_name) or "unknown"

            installed = self._load_installed()
            installed[package_name] = {
                "version": installed_version,
                "description": package_info["description"] if package_info else "",
                "installed_at": datetime.now().isoformat(),
                "source": install_url,
                "location": "system"
            }
            self._save_installed(installed)

            print(f"\n✓ Successfully installed {package_name.replace('-rooms-pkg', '')} v{installed_version}\n")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Installation failed: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Installation failed: {e}")
            return False

    async def uninstall(self, package_name: str, force: bool = False) -> bool:
        package_name = self._normalize_package_name(package_name)

        if not self.is_installed(package_name):
            logger.warning(f"Package '{package_name}' is not installed")
            return False

        if not force:
            logger.warning(f"Uninstall {package_name}?")
            response = input("Continue? [y/N]: ")
            if response.lower() != 'y':
                logger.info("Cancelled")
                return False

        logger.info(f"Uninstalling {package_name}...")

        try:
            if not self.system_python:
                logger.error("No system Python found")
                return False

            python_path = self.system_python[0]
            cmd = [python_path, "-m", "pip", "uninstall", "-y", package_name]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                logger.error(f"pip uninstall failed: {result.stderr}")
                return False

            installed = self._load_installed()
            if package_name in installed:
                del installed[package_name]
                self._save_installed(installed)

            print(f"\n✓ Successfully uninstalled {package_name.replace('-rooms-pkg', '')}\n")
            return True

        except Exception as e:
            logger.error(f"Uninstallation failed: {e}")
            return False

    async def update(self, package_name: str) -> bool:
        package_name = self._normalize_package_name(package_name)
        location = self.get_installed_location(package_name)

        if not location:
            logger.warning(f"Package '{package_name}' is not installed")
            return False

        if location == "bundled":
            logger.warning(f"Cannot update bundled package '{package_name}'")
            return False

        return await self.install(package_name, upgrade=True)

    async def update_all(self) -> Dict[str, bool]:
        installed = self.list_installed()
        plugin_packages = [pkg for pkg in installed if pkg["location"] == "plugin"]

        if not plugin_packages:
            logger.info("No plugin packages to update")
            return {}

        results = {}
        for pkg in plugin_packages:
            name = pkg["name"]
            logger.info(f"Updating {name}...")
            results[name] = await self.update(name)

        return results

    def get_plugin_dir(self) -> Path:
        return self.plugin_dir
