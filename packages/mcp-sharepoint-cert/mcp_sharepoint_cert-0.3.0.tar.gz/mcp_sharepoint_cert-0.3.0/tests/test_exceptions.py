"""Tests for custom exceptions."""

from mcp_sharepoint.exceptions import (
    FileNotFoundError,
    FolderAlreadyExistsError,
    FolderNotEmptyError,
    FolderNotFoundError,
    InvalidPathError,
    SharePointError,
)


class TestSharePointError:
    """Tests for base SharePointError."""

    def test_basic_error(self):
        """Basic error with message."""
        err = SharePointError("Something went wrong")
        assert str(err) == "Something went wrong"
        assert err.message == "Something went wrong"
        assert err.details is None

    def test_error_with_details(self):
        """Error with details."""
        err = SharePointError("Failed", details="extra info")
        assert err.message == "Failed"
        assert err.details == "extra info"


class TestFileNotFoundError:
    """Tests for FileNotFoundError."""

    def test_creates_message(self):
        """Should create descriptive message."""
        err = FileNotFoundError("Documents", "report.pdf")
        assert "report.pdf" in str(err)
        assert "Documents" in str(err)
        assert err.folder == "Documents"
        assert err.file_name == "report.pdf"


class TestFolderNotFoundError:
    """Tests for FolderNotFoundError."""

    def test_creates_message(self):
        """Should create descriptive message."""
        err = FolderNotFoundError("Projects/2024")
        assert "Projects/2024" in str(err)
        assert err.folder_path == "Projects/2024"


class TestFolderAlreadyExistsError:
    """Tests for FolderAlreadyExistsError."""

    def test_with_parent(self):
        """Should include parent folder."""
        err = FolderAlreadyExistsError("NewFolder", "Documents")
        assert "NewFolder" in str(err)
        assert "Documents" in str(err)

    def test_without_parent(self):
        """Should work without parent folder."""
        err = FolderAlreadyExistsError("NewFolder")
        assert "NewFolder" in str(err)
        assert "root" in str(err)


class TestFolderNotEmptyError:
    """Tests for FolderNotEmptyError."""

    def test_with_counts(self):
        """Should include file and folder counts."""
        err = FolderNotEmptyError("MyFolder", files=5, subfolders=2)
        assert "MyFolder" in str(err)
        assert err.files == 5
        assert err.subfolders == 2


class TestInvalidPathError:
    """Tests for InvalidPathError."""

    def test_with_reason(self):
        """Should include reason."""
        err = InvalidPathError("bad<path", "invalid character")
        assert "bad<path" in str(err)
        assert "invalid character" in str(err)
        assert err.path == "bad<path"
        assert err.reason == "invalid character"
