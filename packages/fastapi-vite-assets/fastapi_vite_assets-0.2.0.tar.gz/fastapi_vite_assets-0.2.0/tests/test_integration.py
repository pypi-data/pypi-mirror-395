"""Integration tests for setup_vite."""

from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from fastapi_vite_assets import ViteConfig, setup_vite


class TestIntegration:
    """Test integration with FastAPI."""

    @pytest.fixture
    def app(self):
        """Create FastAPI application."""
        return FastAPI()

    @pytest.fixture
    def templates(self, tmp_path):
        """Create Jinja2Templates instance."""
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()
        return Jinja2Templates(directory=str(templates_dir))

    @pytest.fixture
    def manifest_path(self):
        """Get path to test manifest file."""
        return Path(__file__).parent / "fixtures" / "manifest.json"

    def test_setup_vite_registers_functions(self, app, templates, tmp_path):
        """Test that setup_vite registers template functions."""
        config = ViteConfig(
            base_path=tmp_path,
            force_dev_mode=True,
            validate_on_setup=False,  # Skip validation for this test
        )

        setup_vite(app, templates, config)

        assert "vite_hmr_client" in templates.env.globals
        assert "vite_asset" in templates.env.globals
        assert callable(templates.env.globals["vite_hmr_client"])
        assert callable(templates.env.globals["vite_asset"])

    def test_setup_vite_with_defaults(self, app, templates):
        """Test setup_vite with default configuration."""
        setup_vite(app, templates)

        assert "vite_hmr_client" in templates.env.globals
        assert "vite_asset" in templates.env.globals

    def test_setup_vite_mounts_static_files(
        self, app, templates, manifest_path, tmp_path
    ):
        """Test that setup_vite mounts static files when assets exist."""
        # Create dist directory
        dist_dir = tmp_path / "web" / "dist"
        dist_dir.mkdir(parents=True)

        config = ViteConfig(
            assets_path="web/dist",
            base_path=tmp_path,
            force_dev_mode=False,
        )

        setup_vite(app, templates, config)

        # Check that static files route was mounted
        routes = [route.path for route in app.routes]
        assert "/static" in routes

    def test_setup_vite_skips_static_if_no_dist(self, app, templates, tmp_path):
        """Test that setup_vite doesn't mount static files if dist doesn't exist."""
        config = ViteConfig(
            assets_path="web/dist",
            base_path=tmp_path,
            force_dev_mode=False,
        )

        setup_vite(app, templates, config)

        # Check that static files route was NOT mounted
        routes = [route.path for route in app.routes]
        assert "/static" not in routes

    def test_template_functions_work_in_jinja(self, app, templates, tmp_path):
        """Test that registered functions work in Jinja2 templates."""
        config = ViteConfig(
            base_path=tmp_path,
            force_dev_mode=True,
            dev_server_url="http://localhost:5173",
        )

        setup_vite(app, templates, config)

        # Create a test template
        template_content = """
        {{ vite_hmr_client() }}
        {{ vite_asset("src/main.ts") }}
        {{ vite_asset("src/style.css") }}
        """

        template = templates.env.from_string(template_content)
        result = template.render()

        assert "/@vite/client" in result
        assert "src/main.ts" in result
        assert "src/style.css" in result
        assert '<script type="module"' in result
        assert '<link rel="stylesheet"' in result

    def test_production_mode_with_manifest(self, app, templates, manifest_path):
        """Test production mode with actual manifest file."""
        config = ViteConfig(
            assets_path="fixtures",
            manifest_path="fixtures/manifest.json",
            base_path=manifest_path.parent.parent,
            force_dev_mode=False,
        )

        setup_vite(app, templates, config)

        # Create a test template
        template_content = """
        {{ vite_hmr_client() }}
        {{ vite_asset("src/main.ts") }}
        {{ vite_asset("src/style.css") }}
        {{ vite_asset("src/app.tsx") }}
        """

        template = templates.env.from_string(template_content)
        result = template.render()

        # HMR client should not be present in production
        assert "/@vite/client" not in result

        # Should have production asset paths
        assert "/static/assets/main-D2jVR6rk.js" in result
        assert "/static/assets/style-tzKEmwoM.css" in result
        assert "/static/assets/app-BxYz123.js" in result
        assert "/static/assets/app-styles-Abc456.css" in result

    def test_custom_static_prefix(self, app, templates, manifest_path):
        """Test custom static URL prefix."""
        config = ViteConfig(
            assets_path="fixtures",
            manifest_path="fixtures/manifest.json",
            base_path=manifest_path.parent.parent,
            static_url_prefix="/assets",
            force_dev_mode=False,
        )

        setup_vite(app, templates, config)

        template_content = "{{ vite_asset('src/main.ts') }}"
        template = templates.env.from_string(template_content)
        result = template.render()

        assert "/assets/assets/main-D2jVR6rk.js" in result

    def test_validation_warns_missing_assets(
        self, app, templates, tmp_path, monkeypatch, caplog
    ):
        """Test that validation warns about missing assets in production."""
        import logging

        caplog.set_level(logging.WARNING)
        monkeypatch.setenv("ENV", "production")

        config = ViteConfig(
            assets_path="nonexistent",
            base_path=tmp_path,
            validate_on_setup=True,
        )

        setup_vite(app, templates, config)

        # Check that warning was logged
        assert any(
            "Assets directory not found" in record.message for record in caplog.records
        )

    def test_strict_mode_raises_on_missing_assets(
        self, app, templates, tmp_path, monkeypatch
    ):
        """Test that strict mode raises exception for missing assets."""
        monkeypatch.setenv("ENV", "production")

        config = ViteConfig(
            assets_path="nonexistent",
            base_path=tmp_path,
            strict_mode=True,
        )

        with pytest.raises(ValueError, match="Vite configuration error"):
            setup_vite(app, templates, config)

    def test_validation_skipped_in_dev_mode(
        self, app, templates, tmp_path, monkeypatch, caplog
    ):
        """Test that validation is skipped in development mode."""
        import logging

        caplog.set_level(logging.WARNING)
        monkeypatch.setenv("ENV", "development")

        config = ViteConfig(
            assets_path="nonexistent",
            base_path=tmp_path,
            validate_on_setup=True,
        )

        setup_vite(app, templates, config)

        # No warnings should be logged in dev mode
        assert not any(
            "Assets directory not found" in record.message for record in caplog.records
        )

    def test_auto_derived_manifest_path(self, app, templates, tmp_path):
        """Test that manifest_path is auto-derived from assets_path."""
        config = ViteConfig(
            assets_path="web/dist",
            base_path=tmp_path,
            force_dev_mode=True,
            validate_on_setup=False,
        )

        assert config.manifest_path == "web/dist/.vite/manifest.json"
        setup_vite(app, templates, config)

        # Should work without explicit manifest_path
        assert "vite_asset" in templates.env.globals
