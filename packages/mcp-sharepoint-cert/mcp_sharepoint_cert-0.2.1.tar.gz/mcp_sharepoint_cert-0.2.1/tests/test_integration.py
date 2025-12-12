"""Integration tests against real SharePoint.

These tests require real SharePoint credentials and are skipped in CI.
Run locally with: uv run pytest tests/test_integration.py -v
"""

import contextlib
import os
import uuid
from pathlib import Path

import pytest
from dotenv import load_dotenv

# Load .env file for local testing
load_dotenv()

# Skip all tests in this file if no real credentials
pytestmark = pytest.mark.skipif(
    os.getenv("SHP_CERT_PATH") is None or not Path(os.getenv("SHP_CERT_PATH", "")).exists(),
    reason="No SharePoint credentials configured (need SHP_CERT_PATH)",
)


class TestFolderOperations:
    """Test folder operations against real SharePoint."""

    def test_list_folders(self):
        """Test listing folders at root."""
        from mcp_sharepoint.resources import list_folders

        folders = list_folders("")
        assert isinstance(folders, list)
        assert len(folders) >= 0
        if folders:
            assert "name" in folders[0]
            assert "url" in folders[0]

    def test_list_documents(self):
        """Test listing documents at root."""
        from mcp_sharepoint.resources import list_documents

        docs = list_documents("")
        assert isinstance(docs, list)
        if docs:
            assert "name" in docs[0]
            assert "size" in docs[0]


class TestDocumentOperations:
    """Test document CRUD operations."""

    @pytest.fixture
    async def test_folder(self):
        """Create a test folder for document operations."""
        from mcp_sharepoint.tools import create_folder, delete_folder

        folder_name = f"_mcp_test_{uuid.uuid4().hex[:8]}"
        await create_folder(folder_name, "")
        yield folder_name
        # Cleanup
        with contextlib.suppress(Exception):
            await delete_folder(folder_name)

    @pytest.mark.asyncio
    async def test_upload_and_delete_document(self, test_folder):
        """Test uploading and deleting a document."""
        from mcp_sharepoint.resources import list_documents
        from mcp_sharepoint.tools import delete_document, upload_document

        # Upload - signature: (folder_name, file_name, content)
        filename = f"test_{uuid.uuid4().hex[:8]}.txt"
        content = "Hello from integration test!"
        result = await upload_document(test_folder, filename, content)
        assert isinstance(result, dict)
        assert result.get("success") is True

        # Verify it exists
        docs = list_documents(test_folder)
        doc_names = [d["name"] for d in docs]
        assert filename in doc_names

        # Delete - signature: (folder_name, file_name)
        result = await delete_document(test_folder, filename)
        assert isinstance(result, dict)
        assert result.get("success") is True

        # Verify it's gone
        docs = list_documents(test_folder)
        doc_names = [d["name"] for d in docs]
        assert filename not in doc_names

    @pytest.mark.asyncio
    async def test_get_document_content(self, test_folder):
        """Test reading document content."""
        from mcp_sharepoint.resources import get_document_content
        from mcp_sharepoint.tools import delete_document, upload_document

        # Upload a file - signature: (folder_name, file_name, content)
        filename = f"test_{uuid.uuid4().hex[:8]}.txt"
        original_content = "Test content for reading!"
        await upload_document(test_folder, filename, original_content)

        # Read it back - signature: (folder_name, file_name)
        result = get_document_content(test_folder, filename)
        assert isinstance(result, dict)
        assert original_content in result.get("content", "")

        # Cleanup
        await delete_document(test_folder, filename)


class TestTreeOperations:
    """Test folder tree operations."""

    @pytest.mark.skip(reason="Tree operation is slow on large SharePoint sites")
    def test_get_folder_tree(self):
        """Test getting folder tree."""
        from mcp_sharepoint.resources import get_folder_tree

        tree = get_folder_tree("")
        assert isinstance(tree, dict)
        assert "name" in tree
        assert "type" in tree
        assert tree["type"] == "folder"
