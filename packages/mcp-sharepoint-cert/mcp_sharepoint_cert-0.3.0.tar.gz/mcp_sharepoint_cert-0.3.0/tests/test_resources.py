"""Tests for resource utilities."""

from mcp_sharepoint.resources import (
    FILE_TYPES,
    TREE_CONFIG,
    _get_sp_path,
)


class TestFileTypes:
    """Tests for FILE_TYPES configuration."""

    def test_text_extensions(self):
        """Text file extensions should be defined."""
        assert ".txt" in FILE_TYPES["text"]
        assert ".json" in FILE_TYPES["text"]
        assert ".py" in FILE_TYPES["text"]

    def test_pdf_extensions(self):
        """PDF extensions should be defined."""
        assert ".pdf" in FILE_TYPES["pdf"]

    def test_excel_extensions(self):
        """Excel extensions should be defined."""
        assert ".xlsx" in FILE_TYPES["excel"]
        assert ".xls" in FILE_TYPES["excel"]

    def test_word_extensions(self):
        """Word extensions should be defined."""
        assert ".docx" in FILE_TYPES["word"]
        assert ".doc" in FILE_TYPES["word"]


class TestTreeConfig:
    """Tests for TREE_CONFIG defaults."""

    def test_default_values(self):
        """Default config values should be set."""
        assert "max_depth" in TREE_CONFIG
        assert "max_folders_per_level" in TREE_CONFIG
        assert "level_delay" in TREE_CONFIG
        assert "batch_delay" in TREE_CONFIG

    def test_max_depth_is_positive(self):
        """Max depth should be positive."""
        assert int(TREE_CONFIG["max_depth"]) > 0


class TestGetSpPath:
    """Tests for _get_sp_path function."""

    def test_root_path(self):
        """Root path should work without sub_path."""
        # This will use the SHP_DOC_LIBRARY env var
        result = _get_sp_path()
        assert isinstance(result, str)
        assert not result.endswith("/")

    def test_with_sub_path(self):
        """Sub path should be appended correctly."""
        result = _get_sp_path("subfolder")
        assert "subfolder" in result
        assert not result.endswith("/")

    def test_with_nested_path(self):
        """Nested paths should work."""
        result = _get_sp_path("folder/subfolder/deep")
        assert "folder/subfolder/deep" in result
