"""Logging configuration for fastapi-vite-assets."""

import logging

# Create package logger
logger = logging.getLogger("fastapi_vite_assets")

# Add NullHandler by default (library best practice)
# Applications can configure logging as needed
logger.addHandler(logging.NullHandler())

__all__ = ["logger"]
