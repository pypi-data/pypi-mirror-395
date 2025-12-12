import os
import sys
import platform
import subprocess
from pathlib import Path
from typing import Optional, Dict
import httpx
from loguru import logger


class BinaryInstaller:
    GITHUB_REPO = "nexroo-ai/nexroo-cli"
    CACHE_DIR = Path.home() / ".nexroo" / "cache"

    def __init__(self):
        self.platform = self._detect_platform()
        self.python_tag = self._get_python_tag()
        self.version_file = Path.home() / ".nexroo" / ".engine_version"

    def _detect_platform(self) -> str:
        system = platform.system().lower()
        if system == "linux":
            return "linux"
        elif system == "darwin":
            return "macos"
        elif system == "windows":
            return "windows"
        else:
            raise Exception(f"Unsupported platform: {system}")

    def _get_python_tag(self) -> str:
        return f"cp{sys.version_info.major}{sys.version_info.minor}"

    def _get_platform_wheel_pattern(self) -> str:
        if self.platform == "linux":
            return "linux"
        elif self.platform == "macos":
            return "macosx"
        elif self.platform == "windows":
            return "win"

    async def get_latest_release_info(self) -> Dict[str, str]:
        """Get the latest Engine release from public GitHub releases."""
        url = f"https://api.github.com/repos/{self.GITHUB_REPO}/releases"

        async with httpx.AsyncClient(follow_redirects=True) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                releases = response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise Exception(
                        "Repository not found or no releases available.\n"
                        "Check https://github.com/nexroo-ai/nexroo-cli/releases"
                    )
                raise

        # Find the latest release that starts with "Engine "
        engine_release = None
        for release in releases:
            if release.get("name", "").startswith("Engine "):
                engine_release = release
                break

        if not engine_release:
            raise Exception(
                "No Engine releases found.\n"
                "Check https://github.com/nexroo-ai/nexroo-cli/releases"
            )

        platform_pattern = self._get_platform_wheel_pattern()
        python_tag = self.python_tag

        for asset in engine_release.get("assets", []):
            asset_name = asset["name"]
            if (asset_name.endswith(".whl") and
                platform_pattern in asset_name.lower() and
                python_tag in asset_name):
                return {
                    "version": engine_release["tag_name"],
                    "download_url": asset["browser_download_url"],
                    "filename": asset_name
                }

        raise Exception(f"No wheel found for platform: {self.platform}, Python: {python_tag}")

    async def get_latest_release_url(self) -> str:
        info = await self.get_latest_release_info()
        return info["download_url"]

    def _save_version(self, version: str):
        self.version_file.write_text(version.strip())

    def _get_installed_version(self) -> Optional[str]:
        if self.version_file.exists():
            return self.version_file.read_text().strip()
        return None

    async def download_package(self, url: str, version: str, filename: str) -> Path:
        logger.info(f"Downloading nexroo-engine for {self.platform}...")

        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)

        temp_path = self.CACHE_DIR / filename

        async with httpx.AsyncClient(follow_redirects=True) as client:
            async with client.stream("GET", url) as response:
                response.raise_for_status()

                total = int(response.headers.get("content-length", 0))
                downloaded = 0

                with open(temp_path, "wb") as f:
                    async for chunk in response.aiter_bytes(chunk_size=8192):
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total > 0:
                            percent = (downloaded / total) * 100
                            logger.debug(f"Progress: {percent:.1f}%")

        package_path = self.CACHE_DIR / filename

        if package_path.exists() and package_path != temp_path:
            package_path.unlink()

        if temp_path != package_path:
            temp_path.rename(package_path)

        logger.debug(f"Package downloaded: {filename}")
        return package_path

    def _install_package(self, package_path: Path, version: str):
        logger.info("Installing nexroo-engine...")
        logger.debug(f"Installing from: {package_path}")
        logger.debug(f"File exists: {package_path.exists()}")
        logger.debug(f"File name: {package_path.name}")

        cmd = [sys.executable, "-m", "pip", "install", "--force-reinstall", str(package_path)]
        logger.debug(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            logger.error(f"pip stdout: {result.stdout}")
            logger.error(f"pip stderr: {result.stderr}")
            raise Exception(f"Failed to install nexroo-engine\n{result.stderr}")

        self._save_version(version)

    async def install(self) -> bool:
        if self.is_installed():
            logger.info("nexroo-engine already installed")
            return True

        release_info = await self.get_latest_release_info()
        package_path = await self.download_package(
            release_info["download_url"],
            release_info["version"],
            release_info["filename"]
        )
        self._install_package(package_path, release_info["version"])

        package_path.unlink()
        return True

    def is_installed(self) -> bool:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", "nexroo-engine"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0

    async def update(self) -> bool:
        logger.info("Checking for updates...")

        current_version = self._get_installed_version()
        release_info = await self.get_latest_release_info()
        latest_version = release_info["version"]

        if current_version == latest_version:
            logger.info(f"Already up to date ({current_version})")
            return True

        logger.info(f"Updating from {current_version or 'unknown'} to {latest_version}")

        package_path = await self.download_package(
            release_info["download_url"],
            latest_version,
            release_info["filename"]
        )
        self._install_package(package_path, latest_version)

        package_path.unlink()
        return True

    def uninstall(self):
        if self.is_installed():
            result = subprocess.run(
                [sys.executable, "-m", "pip", "uninstall", "-y", "nexroo-engine"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                logger.info("nexroo-engine uninstalled")
                if self.version_file.exists():
                    self.version_file.unlink()
            else:
                logger.error("Failed to uninstall nexroo-engine")
        else:
            logger.info("nexroo-engine not found")
