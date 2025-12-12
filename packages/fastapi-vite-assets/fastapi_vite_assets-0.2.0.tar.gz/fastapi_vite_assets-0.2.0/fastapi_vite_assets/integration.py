"""FastAPI integration for Vite."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .config import ViteConfig
from .logger import logger
from .template_helpers import ViteTemplateHelpers


def setup_vite(
    app: FastAPI,
    templates: Jinja2Templates,
    config: ViteConfig | None = None,
) -> ViteTemplateHelpers:
    """Setup Vite integration with FastAPI.

    This function:
    1. Validates configuration (if enabled)
    2. Registers Jinja2 template functions for asset injection
    3. Mounts static file serving for production builds
    4. Logs configuration and any issues

    Args:
        app: FastAPI application instance
        templates: Jinja2Templates instance
        config: ViteConfig instance (uses defaults if None)

    Returns:
        ViteTemplateHelpers instance for advanced usage

    Raises:
        ValueError: If config.strict_mode=True and validation fails

    Example:
        ```python
        from fastapi import FastAPI
        from fastapi.templating import Jinja2Templates
        from fastapi_vite import ViteConfig, setup_vite

        app = FastAPI()
        templates = Jinja2Templates(directory="templates")

        vite = ViteConfig(assets_path="web/dist")

        setup_vite(app, templates, vite)
        ```
    """
    if config is None:
        config = ViteConfig()

    # Log setup
    mode = "development" if config.is_dev_mode else "production"
    logger.debug(
        f"Setting up Vite integration: mode={mode}, "
        f"assets={config.full_assets_path}, "
        f"manifest={config.full_manifest_path}"
    )

    # Validate configuration
    if config.validate_on_setup:
        issues = config.validate()
        if issues:
            for issue in issues:
                if config.strict_mode:
                    raise ValueError(f"Vite configuration error: {issue}")
                else:
                    logger.warning(issue)

    # Create template helpers
    helpers = ViteTemplateHelpers(config)

    # Register Jinja2 functions
    template_functions = helpers.create_jinja_functions()
    templates.env.globals.update(template_functions)
    logger.debug("Registered Jinja2 template functions: vite_hmr_client, vite_asset")

    # Mount static files for production
    if config.full_assets_path.exists():
        app.mount(
            config.static_url_prefix,
            StaticFiles(directory=str(config.full_assets_path)),
            name="static",
        )
        logger.info(
            f"Mounted static files: {config.static_url_prefix} -> {config.full_assets_path}"
        )
    else:
        if not config.is_dev_mode:
            logger.warning(
                f"Assets directory not found: {config.full_assets_path}. "
                f"Static files will not be served. Did you run 'npm run build'?"
            )
        else:
            logger.debug(
                f"Assets directory not found (OK in dev mode): {config.full_assets_path}"
            )

    return helpers
