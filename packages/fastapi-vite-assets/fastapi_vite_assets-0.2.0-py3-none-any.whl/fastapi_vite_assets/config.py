"""Configuration for FastAPI Vite integration."""

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .logger import logger


@dataclass
class ViteConfig:
    """Configuration for Vite integration.

    Args:
        assets_path: Path to the Vite build output directory (default: "dist")
        manifest_path: Path to the Vite manifest.json file (auto-derived from assets_path if None)
        dev_server_url: URL of the Vite dev server (default: "http://localhost:5173")
        static_url_prefix: URL prefix for serving static assets in production (default: "/static")
        auto_detect_dev: Automatically detect dev mode from ENV variable (default: True)
        force_dev_mode: Force development mode regardless of ENV (default: None)
        base_path: Base path to resolve relative paths from (default: current working directory)
        validate_on_setup: Validate configuration during setup_vite() (default: True)
        warn_on_missing_assets: Warn if assets directory missing in production (default: True)
        warn_on_missing_manifest: Warn if manifest file missing in production (default: True)
        strict_mode: Raise exceptions instead of warnings for validation errors (default: False)
    """

    assets_path: str = "dist"
    manifest_path: Optional[str] = None
    dev_server_url: str = "http://localhost:5173"
    static_url_prefix: str = "/static"
    auto_detect_dev: bool = True
    force_dev_mode: Optional[bool] = None
    base_path: Optional[Path] = None
    validate_on_setup: bool = True
    warn_on_missing_assets: bool = True
    warn_on_missing_manifest: bool = True
    strict_mode: bool = False

    def __post_init__(self):
        """Initialize computed properties."""
        if self.base_path is None:
            self.base_path = Path.cwd()
        elif isinstance(self.base_path, str):
            self.base_path = Path(self.base_path)

        # Auto-derive manifest_path if not provided
        if self.manifest_path is None:
            self.manifest_path = f"{self.assets_path}/.vite/manifest.json"
            logger.debug(f"Auto-derived manifest_path: {self.manifest_path}")

    @property
    def is_dev_mode(self) -> bool:
        """Check if running in development mode."""
        if self.force_dev_mode is not None:
            return self.force_dev_mode

        if self.auto_detect_dev:
            return os.getenv("ENV", "development") == "development"

        return False

    @property
    def full_assets_path(self) -> Path:
        """Get the full path to assets directory."""
        assert self.base_path is not None  # Always set in __post_init__
        return self.base_path / self.assets_path

    @property
    def full_manifest_path(self) -> Path:
        """Get the full path to manifest file."""
        assert self.base_path is not None  # Always set in __post_init__
        assert self.manifest_path is not None  # Always set in __post_init__
        return self.base_path / self.manifest_path

    def get_dev_server_host(self) -> str:
        """Get Vite dev server host from env or config."""
        if "VITE_HOST" in os.environ:
            host = os.getenv("VITE_HOST", "localhost")
            port = os.getenv("VITE_PORT", "5173")
            return f"http://{host}:{port}"
        return self.dev_server_url

    def validate(self) -> list[str]:
        """Validate configuration in production mode.

        Returns:
            List of issue messages (empty if no issues)
        """
        issues: list[str] = []

        # Only validate in production mode
        if self.is_dev_mode:
            logger.debug("Skipping validation in development mode")
            return issues

        # Check assets directory
        if not self.full_assets_path.exists():
            issues.append(
                f"Assets directory not found: {self.full_assets_path}. "
                f"Run 'npm run build' to generate production assets."
            )
        elif not self.full_assets_path.is_dir():
            issues.append(
                f"Assets path exists but is not a directory: {self.full_assets_path}"
            )

        # Check manifest file
        if not self.full_manifest_path.exists():
            issues.append(
                f"Manifest file not found: {self.full_manifest_path}. "
                f"Ensure vite.config.ts has 'build.manifest: true'"
            )
        elif not self.full_manifest_path.is_file():
            issues.append(
                f"Manifest path exists but is not a file: {self.full_manifest_path}"
            )
        else:
            # Validate JSON format
            try:
                with open(self.full_manifest_path) as f:
                    data = json.load(f)
                    if not isinstance(data, dict):
                        issues.append(
                            f"Manifest file is not a JSON object: {self.full_manifest_path}"
                        )
            except json.JSONDecodeError as e:
                issues.append(
                    f"Manifest file is not valid JSON: {self.full_manifest_path}. "
                    f"Error: {e}"
                )

        return issues
