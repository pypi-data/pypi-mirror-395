"""Vite manifest reader for production builds."""

import json
from pathlib import Path
from typing import Dict, Optional

from .logger import logger


class ViteManifest:
    """Handles reading and parsing the Vite manifest file."""

    def __init__(self, manifest_path: Path):
        """Initialize the manifest reader.

        Args:
            manifest_path: Path to the manifest.json file
        """
        self.manifest_path = manifest_path
        self._manifest: Optional[Dict] = None

    def load(self) -> Dict:
        """Load and parse the manifest file.

        Returns:
            Dictionary containing the manifest data, or empty dict if file doesn't exist
        """
        if not self.manifest_path.exists():
            logger.debug(
                f"Manifest file not found: {self.manifest_path}. "
                f"Returning empty manifest (OK in development mode)."
            )
            return {}

        try:
            with open(self.manifest_path, "r") as f:
                self._manifest = json.load(f)

            entry_count = len(self._manifest) if self._manifest else 0
            logger.debug(
                f"Loaded manifest with {entry_count} entries from {self.manifest_path}"
            )

            return self._manifest

        except json.JSONDecodeError as e:
            logger.error(
                f"Failed to parse manifest at {self.manifest_path}: {e}. "
                f"Returning empty manifest."
            )
            return {}

    def get_chunk(self, entry: str) -> Optional[Dict]:
        """Get a specific chunk from the manifest.

        Args:
            entry: Entry name (e.g., "src/main.ts")

        Returns:
            Chunk data dictionary or None if not found
        """
        if self._manifest is None:
            self.load()

        return self._manifest.get(entry) if self._manifest else None
