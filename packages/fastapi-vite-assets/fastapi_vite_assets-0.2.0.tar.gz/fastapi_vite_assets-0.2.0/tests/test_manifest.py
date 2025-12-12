"""Tests for ViteManifest."""

from pathlib import Path

import pytest

from fastapi_vite_assets.manifest import ViteManifest


class TestViteManifest:
    """Test ViteManifest class."""

    @pytest.fixture
    def manifest_path(self):
        """Get path to test manifest file."""
        return Path(__file__).parent / "fixtures" / "manifest.json"

    @pytest.fixture
    def manifest(self, manifest_path):
        """Create ViteManifest instance."""
        return ViteManifest(manifest_path)

    def test_load_manifest(self, manifest):
        """Test loading manifest file."""
        data = manifest.load()

        assert isinstance(data, dict)
        assert "src/main.ts" in data
        assert "src/style.css" in data
        assert "src/app.tsx" in data

    def test_load_nonexistent_manifest(self, tmp_path):
        """Test loading non-existent manifest file."""
        manifest = ViteManifest(tmp_path / "nonexistent.json")
        data = manifest.load()

        assert data == {}

    def test_get_chunk_exists(self, manifest):
        """Test getting an existing chunk."""
        chunk = manifest.get_chunk("src/main.ts")

        assert chunk is not None
        assert chunk["file"] == "assets/main-D2jVR6rk.js"
        assert chunk["name"] == "main"
        assert chunk["isEntry"] is True

    def test_get_chunk_with_css(self, manifest):
        """Test getting a chunk that includes CSS."""
        chunk = manifest.get_chunk("src/app.tsx")

        assert chunk is not None
        assert chunk["file"] == "assets/app-BxYz123.js"
        assert "css" in chunk
        assert chunk["css"] == ["assets/app-styles-Abc456.css"]

    def test_get_chunk_not_exists(self, manifest):
        """Test getting a non-existent chunk."""
        chunk = manifest.get_chunk("src/nonexistent.ts")

        assert chunk is None

    def test_get_chunk_auto_loads(self, manifest_path):
        """Test that get_chunk auto-loads manifest if not loaded."""
        manifest = ViteManifest(manifest_path)
        # Don't call load() first

        chunk = manifest.get_chunk("src/style.css")

        assert chunk is not None
        assert chunk["file"] == "assets/style-tzKEmwoM.css"

    def test_load_logs_missing_file(self, tmp_path, caplog):
        """Test that loading missing file logs debug message."""
        import logging

        caplog.set_level(logging.DEBUG)
        manifest = ViteManifest(tmp_path / "nonexistent.json")
        data = manifest.load()

        assert data == {}
        assert any(
            "Manifest file not found" in record.message for record in caplog.records
        )

    def test_load_logs_invalid_json(self, tmp_path, caplog):
        """Test that loading invalid JSON logs error message."""
        import logging

        caplog.set_level(logging.ERROR)
        invalid_json_path = tmp_path / "invalid.json"
        invalid_json_path.write_text("invalid json{")

        manifest = ViteManifest(invalid_json_path)
        data = manifest.load()

        assert data == {}
        assert any(
            "Failed to parse manifest" in record.message for record in caplog.records
        )

    def test_load_logs_success(self, manifest_path, caplog):
        """Test that loading valid manifest logs debug message."""
        import logging

        caplog.set_level(logging.DEBUG)
        manifest = ViteManifest(manifest_path)
        manifest.load()

        assert any(
            "Loaded manifest with" in record.message and "entries" in record.message
            for record in caplog.records
        )
