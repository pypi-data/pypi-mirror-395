"""Custom exceptions for MCP SharePoint operations."""


class SharePointError(Exception):
    """Base exception for SharePoint operations."""

    def __init__(self, message: str, details: str | None = None):
        self.message = message
        self.details = details
        super().__init__(self.message)


class SharePointConnectionError(SharePointError):
    """Raised when connection to SharePoint fails."""

    pass


class SharePointAuthError(SharePointError):
    """Raised when authentication fails."""

    pass


class FileNotFoundError(SharePointError):
    """Raised when a file is not found in SharePoint."""

    def __init__(self, folder: str, file_name: str):
        self.folder = folder
        self.file_name = file_name
        super().__init__(
            f"File '{file_name}' not found in folder '{folder}'",
            details=f"folder={folder}, file={file_name}",
        )


class FolderNotFoundError(SharePointError):
    """Raised when a folder is not found in SharePoint."""

    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        super().__init__(
            f"Folder '{folder_path}' not found",
            details=f"path={folder_path}",
        )


class FolderAlreadyExistsError(SharePointError):
    """Raised when trying to create a folder that already exists."""

    def __init__(self, folder_name: str, parent_folder: str | None = None):
        self.folder_name = folder_name
        self.parent_folder = parent_folder
        location = parent_folder or "root"
        super().__init__(
            f"Folder '{folder_name}' already exists in '{location}'",
            details=f"folder={folder_name}, parent={location}",
        )


class FolderNotEmptyError(SharePointError):
    """Raised when trying to delete a non-empty folder."""

    def __init__(self, folder_path: str, files: int = 0, subfolders: int = 0):
        self.folder_path = folder_path
        self.files = files
        self.subfolders = subfolders
        super().__init__(
            f"Folder '{folder_path}' is not empty",
            details=f"files={files}, subfolders={subfolders}",
        )


class InvalidPathError(SharePointError):
    """Raised when a path contains invalid characters or patterns."""

    def __init__(self, path: str, reason: str):
        self.path = path
        self.reason = reason
        super().__init__(
            f"Invalid path '{path}': {reason}",
            details=f"path={path}",
        )


class FileTooLargeError(SharePointError):
    """Raised when a file exceeds size limits."""

    def __init__(self, file_name: str, size: int, max_size: int):
        self.file_name = file_name
        self.size = size
        self.max_size = max_size
        super().__init__(
            f"File '{file_name}' ({size} bytes) exceeds maximum size ({max_size} bytes)",
            details=f"size={size}, max={max_size}",
        )
