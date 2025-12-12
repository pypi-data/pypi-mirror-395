"""Tests for settings and validation."""

import pytest

from mcp_sharepoint.exceptions import InvalidPathError
from mcp_sharepoint.settings import PathValidator


class TestPathValidator:
    """Tests for PathValidator."""

    def test_validate_name_valid(self):
        """Valid names should pass."""
        assert PathValidator.validate_name("document.pdf") == "document.pdf"
        assert PathValidator.validate_name("folder_name") == "folder_name"
        assert PathValidator.validate_name("file-with-dashes.txt") == "file-with-dashes.txt"

    def test_validate_name_empty(self):
        """Empty names should raise error."""
        with pytest.raises(InvalidPathError):
            PathValidator.validate_name("")
        with pytest.raises(InvalidPathError):
            PathValidator.validate_name("   ")

    def test_validate_name_invalid_chars(self):
        """Names with invalid characters should raise error."""
        invalid_names = [
            "file<name",
            "file>name",
            "file:name",
            'file"name',
            "file|name",
            "file?name",
            "file*name",
        ]
        for name in invalid_names:
            with pytest.raises(InvalidPathError):
                PathValidator.validate_name(name)

    def test_validate_name_path_traversal(self):
        """Path traversal attempts should raise error."""
        with pytest.raises(InvalidPathError):
            PathValidator.validate_name("../parent")
        with pytest.raises(InvalidPathError):
            PathValidator.validate_name("/absolute")
        with pytest.raises(InvalidPathError):
            PathValidator.validate_name("..\\parent")

    def test_validate_name_reserved(self):
        """Windows reserved names should raise error."""
        reserved = ["CON", "PRN", "AUX", "NUL", "COM1", "LPT1"]
        for name in reserved:
            with pytest.raises(InvalidPathError):
                PathValidator.validate_name(name)
            with pytest.raises(InvalidPathError):
                PathValidator.validate_name(f"{name}.txt")

    def test_validate_name_trailing_period(self):
        """Names ending with period should raise error."""
        with pytest.raises(InvalidPathError):
            PathValidator.validate_name("file.")

    def test_validate_name_strips_whitespace(self):
        """Trailing whitespace is stripped (not rejected)."""
        # Trailing space gets stripped, resulting in valid "file"
        result = PathValidator.validate_name("file ")
        assert result == "file"

    def test_validate_name_too_long(self):
        """Names over 255 characters should raise error."""
        with pytest.raises(InvalidPathError):
            PathValidator.validate_name("a" * 256)

    def test_validate_path_valid(self):
        """Valid paths should pass."""
        assert PathValidator.validate_path("folder/subfolder") == "folder/subfolder"
        assert PathValidator.validate_path("") == ""
        assert PathValidator.validate_path("single") == "single"

    def test_validate_path_traversal(self):
        """Path traversal in paths should raise error."""
        with pytest.raises(InvalidPathError):
            PathValidator.validate_path("folder/../other")
        with pytest.raises(InvalidPathError):
            PathValidator.validate_path("../parent/folder")
