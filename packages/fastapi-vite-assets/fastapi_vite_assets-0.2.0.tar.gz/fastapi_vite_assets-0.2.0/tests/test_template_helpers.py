"""Tests for template helper functions."""

from pathlib import Path

import pytest
from markupsafe import Markup

from fastapi_vite_assets.config import ViteConfig
from fastapi_vite_assets.template_helpers import ViteTemplateHelpers


class TestViteTemplateHelpers:
    """Test ViteTemplateHelpers class."""

    @pytest.fixture
    def manifest_path(self):
        """Get path to test manifest file."""
        return Path(__file__).parent / "fixtures" / "manifest.json"

    @pytest.fixture
    def dev_config(self, tmp_path):
        """Create dev mode configuration."""
        return ViteConfig(
            assets_path="web/dist",
            manifest_path="web/dist/.vite/manifest.json",
            base_path=tmp_path,
            force_dev_mode=True,
        )

    @pytest.fixture
    def prod_config(self, manifest_path):
        """Create production mode configuration."""
        return ViteConfig(
            assets_path="fixtures",
            manifest_path="fixtures/manifest.json",
            base_path=manifest_path.parent.parent,
            force_dev_mode=False,
        )

    def test_vite_hmr_client_dev_mode(self, dev_config):
        """Test HMR client injection in development mode."""
        helpers = ViteTemplateHelpers(dev_config)
        result = helpers.vite_hmr_client()

        assert isinstance(result, Markup)
        assert '<script type="module"' in str(result)
        assert "/@vite/client" in str(result)
        assert "http://localhost:5173" in str(result)

    def test_vite_hmr_client_prod_mode(self, prod_config):
        """Test HMR client injection in production mode."""
        helpers = ViteTemplateHelpers(prod_config)
        result = helpers.vite_hmr_client()

        assert isinstance(result, Markup)
        assert str(result) == ""

    def test_vite_hmr_client_custom_server(self, tmp_path, monkeypatch):
        """Test HMR client with custom server URL."""
        monkeypatch.setenv("VITE_HOST", "0.0.0.0")
        monkeypatch.setenv("VITE_PORT", "3000")

        config = ViteConfig(
            base_path=tmp_path,
            force_dev_mode=True,
        )
        helpers = ViteTemplateHelpers(config)
        result = helpers.vite_hmr_client()

        assert "http://0.0.0.0:3000" in str(result)

    def test_vite_asset_dev_mode_js(self, dev_config):
        """Test JavaScript asset injection in development mode."""
        helpers = ViteTemplateHelpers(dev_config)
        result = helpers.vite_asset("src/main.ts")

        assert isinstance(result, Markup)
        assert '<script type="module"' in str(result)
        assert 'src="http://localhost:5173/src/main.ts"' in str(result)

    def test_vite_asset_dev_mode_css(self, dev_config):
        """Test CSS asset injection in development mode."""
        helpers = ViteTemplateHelpers(dev_config)
        result = helpers.vite_asset("src/style.css")

        assert isinstance(result, Markup)
        assert '<link rel="stylesheet"' in str(result)
        assert 'href="http://localhost:5173/src/style.css"' in str(result)

    def test_vite_asset_prod_mode_js(self, prod_config):
        """Test JavaScript asset injection in production mode."""
        helpers = ViteTemplateHelpers(prod_config)
        result = helpers.vite_asset("src/main.ts")

        assert isinstance(result, Markup)
        assert '<script type="module"' in str(result)
        assert 'src="/static/assets/main-D2jVR6rk.js"' in str(result)

    def test_vite_asset_prod_mode_css(self, prod_config):
        """Test CSS asset injection in production mode."""
        helpers = ViteTemplateHelpers(prod_config)
        result = helpers.vite_asset("src/style.css")

        assert isinstance(result, Markup)
        assert '<link rel="stylesheet"' in str(result)
        assert 'href="/static/assets/style-tzKEmwoM.css"' in str(result)

    def test_vite_asset_prod_mode_with_css_deps(self, prod_config):
        """Test asset with CSS dependencies in production mode."""
        helpers = ViteTemplateHelpers(prod_config)
        result = helpers.vite_asset("src/app.tsx")

        result_str = str(result)
        assert isinstance(result, Markup)
        # Should include main JS file
        assert '<script type="module"' in result_str
        assert 'src="/static/assets/app-BxYz123.js"' in result_str
        # Should include CSS dependency
        assert '<link rel="stylesheet"' in result_str
        assert 'href="/static/assets/app-styles-Abc456.css"' in result_str

    def test_vite_asset_prod_mode_missing(self, prod_config):
        """Test missing asset in production mode."""
        helpers = ViteTemplateHelpers(prod_config)
        result = helpers.vite_asset("src/nonexistent.ts")

        assert isinstance(result, Markup)
        assert str(result) == ""

    def test_vite_asset_prod_mode_custom_prefix(self, manifest_path):
        """Test asset with custom static URL prefix."""
        config = ViteConfig(
            assets_path="fixtures",
            manifest_path="fixtures/manifest.json",
            base_path=manifest_path.parent.parent,
            static_url_prefix="/assets",
            force_dev_mode=False,
        )
        helpers = ViteTemplateHelpers(config)
        result = helpers.vite_asset("src/main.ts")

        assert 'src="/assets/assets/main-D2jVR6rk.js"' in str(result)

    def test_create_jinja_functions(self, dev_config):
        """Test creating Jinja2-compatible functions."""
        helpers = ViteTemplateHelpers(dev_config)
        functions = helpers.create_jinja_functions()

        assert "vite_hmr_client" in functions
        assert "vite_asset" in functions
        assert callable(functions["vite_hmr_client"])
        assert callable(functions["vite_asset"])

    def test_jinja_functions_work(self, dev_config):
        """Test that Jinja2 functions work with context."""
        helpers = ViteTemplateHelpers(dev_config)
        functions = helpers.create_jinja_functions()

        # Simulate calling with Jinja2 context
        context = {}
        hmr_result = functions["vite_hmr_client"](context)
        asset_result = functions["vite_asset"](context, "src/main.ts")

        assert isinstance(hmr_result, Markup)
        assert isinstance(asset_result, Markup)
        assert "/@vite/client" in str(hmr_result)
        assert "src/main.ts" in str(asset_result)

    def test_missing_asset_logs_warning(self, prod_config, caplog):
        """Test that missing assets in production log warnings."""
        import logging

        caplog.set_level(logging.WARNING)
        helpers = ViteTemplateHelpers(prod_config)
        result = helpers.vite_asset("src/nonexistent.ts")

        assert str(result) == ""
        assert any(
            "Asset 'src/nonexistent.ts' not found" in record.message
            for record in caplog.records
        )
        assert any("vite.config.ts" in record.message for record in caplog.records)
