"""Security regression tests for fastapi-vite-assets integration.

These tests verify that the integration between fastapi-vite-assets and FastAPI's
StaticFiles does not introduce security vulnerabilities, particularly around
directory traversal attacks.
"""

import pytest
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.testclient import TestClient

from fastapi_vite_assets import ViteConfig, setup_vite


class TestSecurityIntegration:
    """Security regression tests for library + FastAPI integration."""

    @pytest.fixture
    def app_with_vite_and_secrets(self, tmp_path):
        """Create FastAPI app with Vite configured and sensitive files nearby."""
        app = FastAPI()

        # Create templates directory
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()
        templates = Jinja2Templates(directory=str(templates_dir))

        # Create dist directory with assets
        dist_dir = tmp_path / "dist"
        dist_dir.mkdir()
        (dist_dir / "main.js").write_text("console.log('app');")

        # Create .vite directory with manifest
        vite_dir = dist_dir / ".vite"
        vite_dir.mkdir()
        manifest_content = '{"src/main.ts": {"file": "main.js"}}'
        (vite_dir / "manifest.json").write_text(manifest_content)

        # Create sensitive files OUTSIDE dist directory (siblings to dist)
        (tmp_path / ".env").write_text("SECRET_KEY=12345")
        (tmp_path / "config.json").write_text('{"database": "secret"}')

        # Create parent-level sensitive file
        parent_secret = tmp_path.parent / "parent_secret.txt"
        parent_secret.write_text("PARENT_SECRET=67890")

        # Configure Vite with base_path at tmp_path
        config = ViteConfig(
            assets_path="dist",
            manifest_path="dist/.vite/manifest.json",
            base_path=tmp_path,
            force_dev_mode=False,
        )

        setup_vite(app, templates, config)
        return app, tmp_path

    def test_static_files_mounted_correctly(self, app_with_vite_and_secrets):
        """Test that static files are accessible at the correct path."""
        app, _ = app_with_vite_and_secrets
        client = TestClient(app)

        # Should be able to access legitimate assets
        response = client.get("/static/main.js")
        assert response.status_code == 200
        assert "console.log" in response.text

    def test_directory_traversal_to_parent_blocked(self, app_with_vite_and_secrets):
        """Regression test: directory traversal cannot access files outside dist."""
        app, _ = app_with_vite_and_secrets
        client = TestClient(app)

        # Try to access .env file (sibling to dist directory)
        traversal_attempts = [
            "/static/../.env",
            "/static/../../.env",
            "/static/../config.json",
            "/static/./../.env",
            "/static/main.js/../../.env",
        ]

        for attempt in traversal_attempts:
            response = client.get(attempt)
            # FastAPI StaticFiles should block these (404 or 422)
            assert response.status_code in [404, 422], (
                f"Directory traversal {attempt} was not blocked! "
                f"Got status {response.status_code}"
            )

            # Ensure sensitive content is not leaked
            if response.status_code == 200:
                assert "SECRET_KEY" not in response.text
                assert "database" not in response.text

    def test_directory_traversal_url_encoded(self, app_with_vite_and_secrets):
        """Regression test: URL-encoded directory traversal is blocked."""
        app, _ = app_with_vite_and_secrets
        client = TestClient(app)

        # URL-encoded attempts
        encoded_attempts = [
            "/static/..%2F.env",  # ../.env
            "/static/..%5c.env",  # ..\.env (backslash)
            "/static/%2e%2e%2f.env",  # ../.env (fully encoded)
        ]

        for attempt in encoded_attempts:
            response = client.get(attempt)
            assert response.status_code in [
                404,
                422,
            ], f"URL-encoded traversal {attempt} was not blocked!"

            if response.status_code == 200:
                assert "SECRET_KEY" not in response.text

    def test_absolute_path_attempts_blocked(self, app_with_vite_and_secrets):
        """Regression test: absolute paths cannot bypass static directory."""
        app, tmp_path = app_with_vite_and_secrets
        client = TestClient(app)

        absolute_attempts = [
            "/static//etc/passwd",
            f"/static/{tmp_path}/.env",
            "/static//tmp/secrets",
        ]

        for attempt in absolute_attempts:
            response = client.get(attempt)
            assert response.status_code in [
                404,
                422,
            ], f"Absolute path {attempt} was not blocked!"

    def test_manifest_whitelisting_in_production(self, tmp_path):
        """Test that only files in manifest can generate asset tags in production."""
        from fastapi_vite_assets.template_helpers import ViteTemplateHelpers

        # Create manifest with only one entry
        manifest_dir = tmp_path / ".vite"
        manifest_dir.mkdir()
        manifest_file = manifest_dir / "manifest.json"
        manifest_file.write_text('{"src/main.ts": {"file": "main.js"}}')

        config = ViteConfig(
            assets_path=str(tmp_path),
            manifest_path=str(manifest_file),
            base_path=tmp_path.parent,
            force_dev_mode=False,
        )

        helpers = ViteTemplateHelpers(config)

        # File in manifest should generate tag
        valid_result = helpers.vite_asset("src/main.ts")
        assert str(valid_result) != ""
        assert "main.js" in str(valid_result)

        # Files NOT in manifest should return empty (whitelisting)
        invalid_paths = [
            "../.env",
            "../../config.json",
            "../../../etc/passwd",
            "arbitrary-file.js",
        ]

        for invalid_path in invalid_paths:
            result = helpers.vite_asset(invalid_path)
            assert str(result) == "", (
                f"Non-manifest path {invalid_path} should return empty!"
            )

    def test_config_paths_resolve_relative_to_base(self, tmp_path):
        """Test that config paths are resolved relative to base_path.

        Note: ViteConfig doesn't prevent traversal in paths - it simply concatenates.
        However, the manifest whitelisting and FastAPI's StaticFiles prevent actual
        security issues. This test documents the current behavior.
        """
        # Paths with .. are allowed in config (they concatenate)
        config = ViteConfig(
            assets_path="../../../etc",
            manifest_path="../../../etc/passwd",
            base_path=tmp_path,
        )

        # The paths will contain .. segments
        # This is OK because:
        # 1. Manifest whitelisting prevents arbitrary file inclusion
        # 2. StaticFiles prevents directory traversal at HTTP layer
        assert "../.." in str(config.assets_path)
        assert "../.." in str(config.manifest_path)

    def test_dev_mode_urls_point_to_vite_server(self, tmp_path):
        """Test that dev mode doesn't expose local filesystem.

        In dev mode, asset paths are converted to Vite dev server URLs.
        The Vite dev server itself is responsible for validating paths.
        """
        from fastapi_vite_assets.template_helpers import ViteTemplateHelpers

        config = ViteConfig(
            base_path=tmp_path,
            force_dev_mode=True,
        )

        helpers = ViteTemplateHelpers(config)

        # Even malicious paths just become URLs to Vite dev server
        result = helpers.vite_asset("../../../etc/passwd")
        assert str(result) != ""
        assert "http://localhost:5173/" in str(result)
        assert "../../../etc/passwd" in str(result)

        # Vite dev server should reject invalid paths
        # This test just verifies we're not reading local files directly

    def test_manifest_json_safely_parsed(self, tmp_path):
        """Test that malformed manifest.json doesn't cause issues."""
        from fastapi_vite_assets.manifest import ViteManifest

        # Create various malformed manifests
        test_cases = [
            ('{"__proto__": {"polluted": true}}', "prototype pollution"),
            ('{"src/main.ts": null}', "null value"),
            (
                '{"src/main.ts": {"file": "../../../etc/passwd"}}',
                "traversal in manifest",
            ),
        ]

        for content, description in test_cases:
            manifest_file = tmp_path / f"test_{description.replace(' ', '_')}.json"
            manifest_file.write_text(content)

            manifest = ViteManifest(manifest_file)
            data = manifest.load()

            # Should load without error
            assert isinstance(data, dict), f"Failed for: {description}"

    def test_no_information_disclosure_on_404(self, app_with_vite_and_secrets):
        """Test that 404 responses don't leak path information."""
        app, tmp_path = app_with_vite_and_secrets
        client = TestClient(app)

        # Request non-existent file
        response = client.get("/static/nonexistent.js")
        assert response.status_code == 404

        # Response should not leak full filesystem paths
        response_text = response.text.lower()
        assert str(tmp_path).lower() not in response_text
        assert "/tmp/" not in response_text or "pytest" not in response_text
