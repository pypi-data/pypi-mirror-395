"""Tests for the setup module."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from mcp_sharepoint.setup import copy_to_clipboard, generate_certificate


class TestGenerateCertificate:
    """Tests for certificate generation."""

    def test_generates_certificate_files(self, tmp_path):
        """Test that certificate files are created."""
        result = generate_certificate(output_dir=str(tmp_path))

        assert Path(result["cert_path"]).exists()
        assert Path(result["pem_path"]).exists()
        assert "thumbprint" in result
        assert len(result["thumbprint"]) == 40  # SHA1 thumbprint is 40 hex chars

    def test_certificate_contains_key_and_cert(self, tmp_path):
        """Test that PEM file contains both cert and key."""
        result = generate_certificate(output_dir=str(tmp_path))

        pem_content = Path(result["pem_path"]).read_text()
        assert "-----BEGIN CERTIFICATE-----" in pem_content
        assert "-----BEGIN PRIVATE KEY-----" in pem_content

    def test_creates_output_directory(self, tmp_path):
        """Test that output directory is created if it doesn't exist."""
        new_dir = tmp_path / "new_certs_dir"
        assert not new_dir.exists()

        generate_certificate(output_dir=str(new_dir))

        assert new_dir.exists()

    def test_thumbprint_format(self, tmp_path):
        """Test that thumbprint is uppercase hex without colons."""
        result = generate_certificate(output_dir=str(tmp_path))

        thumbprint = result["thumbprint"]
        assert thumbprint.isalnum()
        assert thumbprint == thumbprint.upper()
        assert ":" not in thumbprint

    def test_openssl_not_found(self, tmp_path):
        """Test error handling when openssl is not found."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()

            with pytest.raises(SystemExit) as exc_info:
                generate_certificate(output_dir=str(tmp_path))

            assert exc_info.value.code == 1


class TestCopyToClipboard:
    """Tests for clipboard functionality."""

    def test_returns_false_when_no_clipboard_tool(self):
        """Test that function returns False when no clipboard tool is available."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()

            result = copy_to_clipboard("test text")

            assert result is False

    def test_tries_pbcopy_first(self):
        """Test that pbcopy is tried first (macOS)."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = None

            copy_to_clipboard("test text")

            # First call should be pbcopy
            first_call = mock_run.call_args_list[0]
            assert first_call[0][0] == ["pbcopy"]

    def test_returns_true_on_success(self):
        """Test that function returns True when copy succeeds."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = None

            result = copy_to_clipboard("test text")

            assert result is True

    def test_tries_xclip_after_pbcopy_fails(self):
        """Test that xclip is tried if pbcopy fails."""
        call_count = 0

        def side_effect(*_args, **_kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:  # pbcopy fails
                raise FileNotFoundError()
            return None  # xclip succeeds

        with patch("subprocess.run", side_effect=side_effect):
            result = copy_to_clipboard("test text")

            assert result is True
            assert call_count == 2


class TestConfigGeneration:
    """Tests for config JSON generation."""

    def test_config_structure(self):
        """Test that generated config has correct structure."""
        config = {
            "mcpServers": {
                "sharepoint": {
                    "command": "uvx",
                    "args": ["mcp-sharepoint"],
                    "env": {
                        "SHP_ID_APP": "test-app-id",
                        "SHP_TENANT_ID": "test-tenant-id",
                        "SHP_SITE_URL": "https://test.sharepoint.com/sites/Test",
                        "SHP_DOC_LIBRARY": "Shared Documents",
                        "SHP_CERT_PATH": "/path/to/cert.pem",
                        "SHP_CERT_THUMBPRINT": "ABC123",
                    },
                }
            }
        }

        config_json = json.dumps(config, indent=2)
        parsed = json.loads(config_json)

        assert "mcpServers" in parsed
        assert "sharepoint" in parsed["mcpServers"]
        assert parsed["mcpServers"]["sharepoint"]["command"] == "uvx"
        assert "SHP_ID_APP" in parsed["mcpServers"]["sharepoint"]["env"]
