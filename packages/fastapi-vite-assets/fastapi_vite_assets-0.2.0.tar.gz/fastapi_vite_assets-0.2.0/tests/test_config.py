"""Tests for ViteConfig."""

from pathlib import Path

from fastapi_vite_assets.config import ViteConfig


class TestViteConfig:
    """Test ViteConfig class."""

    def test_default_config(self):
        """Test default configuration values."""
        config = ViteConfig()

        assert config.assets_path == "dist"
        assert config.manifest_path == "dist/.vite/manifest.json"  # Auto-derived
        assert config.dev_server_url == "http://localhost:5173"
        assert config.static_url_prefix == "/static"
        assert config.auto_detect_dev is True
        assert config.force_dev_mode is None
        assert config.base_path == Path.cwd()
        assert config.validate_on_setup is True
        assert config.warn_on_missing_assets is True
        assert config.warn_on_missing_manifest is True
        assert config.strict_mode is False

    def test_custom_config(self):
        """Test custom configuration values."""
        config = ViteConfig(
            assets_path="web/dist",
            manifest_path="web/dist/.vite/manifest.json",
            dev_server_url="http://localhost:3000",
            static_url_prefix="/assets",
            base_path="/app",
        )

        assert config.assets_path == "web/dist"
        assert config.manifest_path == "web/dist/.vite/manifest.json"
        assert config.dev_server_url == "http://localhost:3000"
        assert config.static_url_prefix == "/assets"
        assert config.base_path == Path("/app")

    def test_is_dev_mode_default(self, monkeypatch):
        """Test is_dev_mode with default ENV."""
        config = ViteConfig()
        monkeypatch.delenv("ENV", raising=False)

        assert config.is_dev_mode is True  # Default is development

    def test_is_dev_mode_production(self, monkeypatch):
        """Test is_dev_mode with production ENV."""
        config = ViteConfig()
        monkeypatch.setenv("ENV", "production")

        assert config.is_dev_mode is False

    def test_is_dev_mode_forced(self, monkeypatch):
        """Test is_dev_mode with force_dev_mode."""
        monkeypatch.setenv("ENV", "production")

        config = ViteConfig(force_dev_mode=True)
        assert config.is_dev_mode is True

        config = ViteConfig(force_dev_mode=False)
        assert config.is_dev_mode is False

    def test_full_assets_path(self):
        """Test full_assets_path property."""
        config = ViteConfig(
            assets_path="web/dist",
            base_path="/app",
        )

        assert config.full_assets_path == Path("/app/web/dist")

    def test_full_manifest_path(self):
        """Test full_manifest_path property."""
        config = ViteConfig(
            manifest_path="web/dist/.vite/manifest.json",
            base_path="/app",
        )

        assert config.full_manifest_path == Path("/app/web/dist/.vite/manifest.json")

    def test_get_dev_server_host_from_env(self, monkeypatch):
        """Test get_dev_server_host with environment variables."""
        config = ViteConfig()

        monkeypatch.setenv("VITE_HOST", "0.0.0.0")
        monkeypatch.setenv("VITE_PORT", "8080")

        assert config.get_dev_server_host() == "http://0.0.0.0:8080"

    def test_get_dev_server_host_from_config(self, monkeypatch):
        """Test get_dev_server_host with config value."""
        monkeypatch.delenv("VITE_HOST", raising=False)
        monkeypatch.delenv("VITE_PORT", raising=False)

        config = ViteConfig(dev_server_url="http://localhost:3000")

        assert config.get_dev_server_host() == "http://localhost:3000"

    def test_auto_derive_manifest_path(self):
        """Test manifest_path auto-derivation from assets_path."""
        config = ViteConfig(assets_path="web/dist")

        assert config.manifest_path == "web/dist/.vite/manifest.json"

    def test_explicit_manifest_path_preserved(self):
        """Test that explicit manifest_path is preserved (not auto-derived)."""
        config = ViteConfig(
            assets_path="web/dist", manifest_path="custom/path/manifest.json"
        )

        assert config.manifest_path == "custom/path/manifest.json"

    def test_validate_in_dev_mode(self, monkeypatch, tmp_path):
        """Test validation is skipped in development mode."""
        monkeypatch.setenv("ENV", "development")
        config = ViteConfig(assets_path="nonexistent", base_path=tmp_path)

        issues = config.validate()
        assert len(issues) == 0  # No validation in dev mode

    def test_validate_missing_assets(self, monkeypatch, tmp_path):
        """Test validation detects missing assets directory."""
        monkeypatch.setenv("ENV", "production")
        config = ViteConfig(assets_path="nonexistent", base_path=tmp_path)

        issues = config.validate()
        assert len(issues) > 0
        assert any("Assets directory not found" in issue for issue in issues)

    def test_validate_missing_manifest(self, monkeypatch, tmp_path):
        """Test validation detects missing manifest file."""
        monkeypatch.setenv("ENV", "production")
        # Create assets directory but no manifest
        assets_dir = tmp_path / "dist"
        assets_dir.mkdir()

        config = ViteConfig(assets_path="dist", base_path=tmp_path)

        issues = config.validate()
        assert len(issues) > 0
        assert any("Manifest file not found" in issue for issue in issues)

    def test_validate_invalid_json(self, monkeypatch, tmp_path):
        """Test validation detects invalid JSON in manifest."""
        monkeypatch.setenv("ENV", "production")
        # Create assets directory and invalid manifest
        assets_dir = tmp_path / "dist" / ".vite"
        assets_dir.mkdir(parents=True)
        manifest_file = assets_dir / "manifest.json"
        manifest_file.write_text("invalid json{")

        config = ViteConfig(assets_path="dist", base_path=tmp_path)

        issues = config.validate()
        assert len(issues) > 0
        assert any("not valid JSON" in issue for issue in issues)

    def test_validate_valid_manifest(self, monkeypatch, tmp_path):
        """Test validation passes with valid manifest."""
        monkeypatch.setenv("ENV", "production")
        # Create assets directory and valid manifest
        assets_dir = tmp_path / "dist" / ".vite"
        assets_dir.mkdir(parents=True)
        manifest_file = assets_dir / "manifest.json"
        manifest_file.write_text('{"src/main.ts": {"file": "assets/main.js"}}')

        config = ViteConfig(assets_path="dist", base_path=tmp_path)

        issues = config.validate()
        assert len(issues) == 0  # No issues
