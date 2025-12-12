"""Jinja2 template helper functions for Vite asset injection."""

from jinja2 import pass_context
from markupsafe import Markup

from .config import ViteConfig
from .logger import logger
from .manifest import ViteManifest


class ViteTemplateHelpers:
    """Template helper functions for Vite integration."""

    def __init__(self, config: ViteConfig):
        """Initialize template helpers with configuration.

        Args:
            config: ViteConfig instance
        """
        self.config = config
        self._manifest: ViteManifest | None = None

    @property
    def manifest(self) -> ViteManifest:
        """Lazy-load the Vite manifest."""
        if self._manifest is None:
            self._manifest = ViteManifest(self.config.full_manifest_path)
        return self._manifest

    def vite_hmr_client(self) -> Markup:
        """Inject Vite HMR client in development mode.

        Returns:
            HTML script tag for Vite client in dev mode, empty string in production
        """
        if not self.config.is_dev_mode:
            return Markup("")

        dev_server = self.config.get_dev_server_host()
        return Markup(
            f'<script type="module" src="{dev_server}/@vite/client"></script>'
        )

    def vite_asset(self, path: str) -> Markup:
        """Inject Vite asset tags (script or link).

        In development: points to Vite dev server
        In production: reads from manifest and injects built files

        Args:
            path: Asset path (e.g., "src/main.ts")

        Returns:
            HTML tag(s) for the asset
        """
        if self.config.is_dev_mode:
            return self._dev_asset(path)
        return self._prod_asset(path)

    def _dev_asset(self, path: str) -> Markup:
        """Generate asset tag for development mode.

        Args:
            path: Asset path

        Returns:
            HTML tag pointing to Vite dev server
        """
        dev_server = self.config.get_dev_server_host()
        url = f"{dev_server}/{path}"

        if path.endswith(".css"):
            return Markup(f'<link rel="stylesheet" href="{url}">')
        else:
            return Markup(f'<script type="module" src="{url}"></script>')

    def _prod_asset(self, path: str) -> Markup:
        """Generate asset tag(s) for production mode.

        Args:
            path: Asset path

        Returns:
            HTML tag(s) for the built asset and its dependencies
        """
        chunk = self.manifest.get_chunk(path)

        if not chunk:
            logger.warning(
                f"Asset '{path}' not found in manifest. "
                f"Ensure it's listed in vite.config.ts build.rollupOptions.input"
            )
            return Markup("")

        tags = []
        file_path = chunk.get("file")
        static_prefix = self.config.static_url_prefix

        if file_path:
            if path.endswith(".css") or file_path.endswith(".css"):
                tags.append(
                    f'<link rel="stylesheet" href="{static_prefix}/{file_path}">'
                )
            else:
                tags.append(
                    f'<script type="module" src="{static_prefix}/{file_path}"></script>'
                )

        # Include CSS files referenced by this chunk
        if "css" in chunk:
            for css_file in chunk["css"]:
                tags.append(
                    f'<link rel="stylesheet" href="{static_prefix}/{css_file}">'
                )

        return Markup("\n    ".join(tags))

    def create_jinja_functions(self):
        """Create Jinja2-compatible functions.

        Returns:
            Dictionary of function names to callables
        """

        @pass_context
        def hmr_client(context):
            return self.vite_hmr_client()

        @pass_context
        def asset(context, path: str):
            return self.vite_asset(path)

        return {
            "vite_hmr_client": hmr_client,
            "vite_asset": asset,
        }
