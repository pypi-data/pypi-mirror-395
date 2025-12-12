"""Pydantic settings and validation models for MCP SharePoint."""

import re
from typing import Annotated

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .exceptions import InvalidPathError

# Validation patterns
INVALID_CHARS_PATTERN = re.compile(r'[<>:"|?*\x00-\x1f]')
PATH_TRAVERSAL_PATTERN = re.compile(r"(^|/)\.\.(/|$)")
RESERVED_NAMES = frozenset(
    [
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
    ]
)


class SharePointSettings(BaseSettings):
    """SharePoint connection settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="SHP_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Required settings
    site_url: str = Field(..., alias="SHP_SITE_URL", description="SharePoint site URL")
    id_app: str = Field(..., alias="SHP_ID_APP", description="Azure AD application ID")
    id_app_secret: str = Field(
        ..., alias="SHP_ID_APP_SECRET", description="Azure AD application secret"
    )

    # Optional settings with defaults
    doc_library: str = Field(
        default="Shared Documents/mcp_server",
        alias="SHP_DOC_LIBRARY",
        description="Document library path",
    )
    tenant_id: str | None = Field(
        default=None, alias="SHP_TENANT_ID", description="Azure AD tenant ID"
    )

    # Tree configuration
    max_depth: int = Field(default=15, alias="SHP_MAX_DEPTH", ge=1, le=50)
    max_folders_per_level: int = Field(
        default=100, alias="SHP_MAX_FOLDERS_PER_LEVEL", ge=1, le=1000
    )
    level_delay: float = Field(default=0.5, alias="SHP_LEVEL_DELAY", ge=0, le=10)
    batch_delay: float = Field(default=0.1, alias="SHP_BATCH_DELAY", ge=0, le=5)


class TreeConfig(BaseModel):
    """Configuration for folder tree operations."""

    max_depth: int = Field(default=15, ge=1, le=50)
    max_folders_per_level: int = Field(default=100, ge=1, le=1000)
    level_delay: float = Field(default=0.5, ge=0)
    batch_delay: float = Field(default=0.1, ge=0)


class DownloadConfig(BaseModel):
    """Configuration for download operations."""

    fallback_dir: str = Field(default="./downloads")


class PathValidator:
    """Validates file and folder paths for SharePoint operations."""

    @staticmethod
    def validate_name(name: str, is_folder: bool = False) -> str:  # noqa: ARG004
        """
        Validate a file or folder name.

        Raises:
            InvalidPathError: If the name contains invalid characters or patterns.
        """
        if not name or not name.strip():
            raise InvalidPathError(name, "Name cannot be empty")

        name = name.strip()

        # Check for invalid characters
        if INVALID_CHARS_PATTERN.search(name):
            raise InvalidPathError(name, 'Contains invalid characters: < > : " | ? *')

        # Check for path traversal
        if ".." in name or name.startswith("/") or name.startswith("\\"):
            raise InvalidPathError(name, "Path traversal not allowed")

        # Check for reserved names (Windows)
        base_name = name.split(".")[0].upper()
        if base_name in RESERVED_NAMES:
            raise InvalidPathError(name, f"'{base_name}' is a reserved name")

        # Check for names ending with space or period
        if name.endswith(" ") or name.endswith("."):
            raise InvalidPathError(name, "Name cannot end with space or period")

        # Length check
        if len(name) > 255:
            raise InvalidPathError(name, "Name exceeds 255 characters")

        return name

    @staticmethod
    def validate_path(path: str) -> str:
        """
        Validate a full path.

        Raises:
            InvalidPathError: If the path contains invalid patterns.
        """
        if not path:
            return path

        path = path.strip()

        # Check for path traversal attempts
        if PATH_TRAVERSAL_PATTERN.search(path):
            raise InvalidPathError(path, "Path traversal not allowed")

        # Validate each component
        components = path.replace("\\", "/").split("/")
        for component in components:
            if component:  # Skip empty components from leading/trailing slashes
                PathValidator.validate_name(component)

        return path


# Input models for tool operations
class FolderInput(BaseModel):
    """Input validation for folder operations."""

    folder_name: Annotated[str, Field(min_length=1, max_length=255)]
    parent_folder: str | None = None

    @field_validator("folder_name")
    @classmethod
    def validate_folder_name(cls, v: str) -> str:
        return PathValidator.validate_name(v, is_folder=True)

    @field_validator("parent_folder")
    @classmethod
    def validate_parent_folder(cls, v: str | None) -> str | None:
        if v is not None:
            return PathValidator.validate_path(v)
        return v


class FileInput(BaseModel):
    """Input validation for file operations."""

    folder_name: str
    file_name: Annotated[str, Field(min_length=1, max_length=255)]

    @field_validator("file_name")
    @classmethod
    def validate_file_name(cls, v: str) -> str:
        return PathValidator.validate_name(v, is_folder=False)

    @field_validator("folder_name")
    @classmethod
    def validate_folder(cls, v: str) -> str:
        return PathValidator.validate_path(v)


class UploadInput(FileInput):
    """Input validation for upload operations."""

    content: str
    is_base64: bool = False


class MetadataInput(FileInput):
    """Input validation for metadata operations."""

    metadata: dict[str, str | int | float | bool | list[str]]
