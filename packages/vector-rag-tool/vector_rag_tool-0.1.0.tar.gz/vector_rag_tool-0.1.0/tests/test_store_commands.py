"""Tests for store commands.

Tests the CLI store management commands including create, delete, list,
and info operations using both local FAISS and remote S3 Vectors backends.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from vector_rag_tool.commands.store import store


class TestStoreCommands:
    """Test suite for store management commands."""

    def setup_method(self) -> None:
        """Set up test fixtures before each test method."""
        self.runner = CliRunner()
        self.test_store_name = "test-store"
        self.test_dimension = 768
        self.test_bucket = "test-bucket"
        self.test_region = "eu-central-1"
        self.test_profile = "test-profile"

    @patch("vector_rag_tool.commands.store.get_backend")
    def test_create_store_success(self, mock_get_backend: MagicMock) -> None:
        """Test successful store creation."""
        # Setup mock
        mock_backend = MagicMock()
        mock_backend.store_exists.return_value = False
        mock_backend.create_store.return_value = None
        mock_get_backend.return_value = mock_backend

        # Run command
        result = self.runner.invoke(
            store,
            ["create", self.test_store_name, "--dimension", str(self.test_dimension)],
        )

        # Assertions
        assert result.exit_code == 0
        assert f"Created local FAISS store '{self.test_store_name}'" in result.output
        mock_backend.create_store.assert_called_once_with(self.test_store_name, self.test_dimension)
        mock_get_backend.assert_called_once_with(bucket=None, region="eu-central-1", profile=None)

    @patch("vector_rag_tool.commands.store.get_backend")
    def test_create_store_s3_backend(self, mock_get_backend: MagicMock) -> None:
        """Test successful store creation with S3 backend."""
        # Setup mock
        mock_backend = MagicMock()
        mock_backend.store_exists.return_value = False
        mock_backend.create_store.return_value = None
        mock_get_backend.return_value = mock_backend

        # Run command with S3 options
        result = self.runner.invoke(
            store,
            [
                "create",
                self.test_store_name,
                "--dimension",
                str(self.test_dimension),
                "--bucket",
                self.test_bucket,
                "--region",
                self.test_region,
                "--profile",
                self.test_profile,
            ],
        )

        # Assertions
        assert result.exit_code == 0
        assert (
            f"Created S3 Vectors store '{self.test_store_name}' in bucket '{self.test_bucket}'"
            in result.output
        )
        mock_backend.create_store.assert_called_once_with(self.test_store_name, self.test_dimension)
        mock_get_backend.assert_called_once_with(
            bucket=self.test_bucket, region=self.test_region, profile=self.test_profile
        )

    @patch("vector_rag_tool.commands.store.get_backend")
    def test_create_store_already_exists(self, mock_get_backend: MagicMock) -> None:
        """Test store creation when store already exists."""
        # Setup mock to raise ValueError for existing store
        mock_backend = MagicMock()
        mock_backend.create_store.side_effect = ValueError(
            f"Store '{self.test_store_name}' already exists"
        )
        mock_get_backend.return_value = mock_backend

        # Run command
        result = self.runner.invoke(
            store,
            ["create", self.test_store_name],
        )

        # Assertions
        assert result.exit_code != 0
        assert "already exists" in result.output

    @patch("vector_rag_tool.commands.store.get_backend")
    def test_create_store_custom_dimension(self, mock_get_backend: MagicMock) -> None:
        """Test store creation with custom dimension."""
        custom_dimension = 1536
        mock_backend = MagicMock()
        mock_backend.store_exists.return_value = False
        mock_backend.create_store.return_value = None
        mock_get_backend.return_value = mock_backend

        # Run command
        result = self.runner.invoke(
            store,
            ["create", self.test_store_name, "--dimension", str(custom_dimension)],
        )

        # Assertions
        assert result.exit_code == 0
        mock_backend.create_store.assert_called_once_with(self.test_store_name, custom_dimension)

    @patch("vector_rag_tool.commands.store.get_backend")
    def test_delete_store_success(self, mock_get_backend: MagicMock) -> None:
        """Test successful store deletion."""
        # Setup mock
        mock_backend = MagicMock()
        mock_backend.store_exists.return_value = True
        mock_backend.delete_store.return_value = None
        mock_get_backend.return_value = mock_backend

        # Run command with force flag to avoid interactive prompt
        result = self.runner.invoke(
            store,
            ["delete", self.test_store_name, "--force"],
        )

        # Assertions
        assert result.exit_code == 0
        assert f"Deleted local FAISS store '{self.test_store_name}'" in result.output
        mock_backend.delete_store.assert_called_once_with(self.test_store_name)

    @patch("vector_rag_tool.commands.store.get_backend")
    def test_delete_store_s3_backend(self, mock_get_backend: MagicMock) -> None:
        """Test successful store deletion with S3 backend."""
        # Setup mock
        mock_backend = MagicMock()
        mock_backend.store_exists.return_value = True
        mock_backend.delete_store.return_value = None
        mock_get_backend.return_value = mock_backend

        # Run command with S3 options
        result = self.runner.invoke(
            store,
            [
                "delete",
                self.test_store_name,
                "--bucket",
                self.test_bucket,
                "--force",
            ],
        )

        # Assertions
        assert result.exit_code == 0
        assert f"Deleted S3 Vectors store '{self.test_store_name}'" in result.output
        mock_backend.delete_store.assert_called_once_with(self.test_store_name)
        mock_get_backend.assert_called_once_with(
            bucket=self.test_bucket, region="eu-central-1", profile=None
        )

    @patch("vector_rag_tool.commands.store.get_backend")
    def test_delete_store_not_exists(self, mock_get_backend: MagicMock) -> None:
        """Test store deletion when store doesn't exist."""
        # Setup mock
        mock_backend = MagicMock()
        mock_backend.store_exists.return_value = False
        mock_get_backend.return_value = mock_backend

        # Run command
        result = self.runner.invoke(
            store,
            ["delete", self.test_store_name, "--force"],
        )

        # Assertions
        assert result.exit_code != 0
        assert "does not exist" in result.output
        mock_backend.delete_store.assert_not_called()

    @patch("vector_rag_tool.commands.store.get_backend")
    def test_delete_store_with_confirmation(self, mock_get_backend: MagicMock) -> None:
        """Test store deletion with user confirmation."""
        # Setup mock
        mock_backend = MagicMock()
        mock_backend.store_exists.return_value = True
        mock_backend.delete_store.return_value = None
        mock_get_backend.return_value = mock_backend

        # Run command with confirmation input
        result = self.runner.invoke(
            store,
            ["delete", self.test_store_name],
            input="y\n",
        )

        # Assertions
        assert result.exit_code == 0
        mock_backend.delete_store.assert_called_once_with(self.test_store_name)

    @patch("vector_rag_tool.commands.store.get_backend")
    def test_delete_store_cancelled(self, mock_get_backend: MagicMock) -> None:
        """Test store deletion when user cancels."""
        # Setup mock
        mock_backend = MagicMock()
        mock_backend.store_exists.return_value = True
        mock_get_backend.return_value = mock_backend

        # Run command with cancellation input
        result = self.runner.invoke(
            store,
            ["delete", self.test_store_name],
            input="n\n",
        )

        # Assertions
        assert result.exit_code == 0
        assert "cancelled" in result.output
        mock_backend.delete_store.assert_not_called()

    @patch("vector_rag_tool.commands.store.get_backend")
    def test_list_stores_empty(self, mock_get_backend: MagicMock) -> None:
        """Test listing stores when no stores exist."""
        # Setup mock
        mock_backend = MagicMock()
        mock_backend.list_stores.return_value = []
        mock_get_backend.return_value = mock_backend

        # Run command
        result = self.runner.invoke(
            store,
            ["list"],
        )

        # Assertions
        assert result.exit_code == 0
        assert "No stores found" in result.output

    @patch("vector_rag_tool.commands.store.get_backend")
    def test_list_stores_table_format(self, mock_get_backend: MagicMock) -> None:
        """Test listing stores in table format."""
        # Setup mock
        mock_backend = MagicMock()
        stores = ["store1", "store2", "store3"]
        mock_backend.list_stores.return_value = stores
        mock_backend.get_store_info.return_value = {
            "name": "test",
            "vector_count": 100,
            "dimension": 768,
            "index_size_mb": 1.5,
        }
        mock_get_backend.return_value = mock_backend

        # Run command
        result = self.runner.invoke(
            store,
            ["list", "--format", "table"],
        )

        # Assertions
        assert result.exit_code == 0
        assert "Available stores:" in result.output
        for store_name in stores:
            assert store_name in result.output
        mock_backend.list_stores.assert_called_once()

    @patch("vector_rag_tool.commands.store.get_backend")
    def test_list_stores_json_format(self, mock_get_backend: MagicMock) -> None:
        """Test listing stores in JSON format."""
        # Setup mock
        mock_backend = MagicMock()
        stores = ["store1", "store2"]
        mock_backend.list_stores.return_value = stores
        mock_backend.get_store_info.return_value = {
            "name": "test",
            "vector_count": 100,
            "dimension": 768,
            "index_size_mb": 1.5,
        }
        mock_get_backend.return_value = mock_backend

        # Run command
        result = self.runner.invoke(
            store,
            ["list", "--format", "json"],
        )

        # Assertions
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) == 2
        assert all("name" in item for item in data)

    @patch("vector_rag_tool.commands.store.get_backend")
    def test_store_info_table_format(self, mock_get_backend: MagicMock) -> None:
        """Test getting store info in table format."""
        # Setup mock
        mock_backend = MagicMock()
        info = {
            "name": self.test_store_name,
            "backend": "faiss",
            "location": "/path/to/store.faiss",
            "dimension": 768,
            "vector_count": 100,
            "metadata_keys": 50,
            "index_size_mb": 2.5,
        }
        mock_backend.get_store_info.return_value = info
        mock_get_backend.return_value = mock_backend

        # Run command
        result = self.runner.invoke(
            store,
            ["info", self.test_store_name],
        )

        # Assertions
        assert result.exit_code == 0
        assert f"Store: {self.test_store_name}" in result.output
        assert "Backend: faiss" in result.output
        assert "Vector Count: 100" in result.output
        mock_backend.get_store_info.assert_called_once_with(self.test_store_name)

    @patch("vector_rag_tool.commands.store.get_backend")
    def test_store_info_s3_backend(self, mock_get_backend: MagicMock) -> None:
        """Test getting store info with S3 backend."""
        # Setup mock
        mock_backend = MagicMock()
        info = {
            "name": self.test_store_name,
            "backend": "s3vectors",
            "location": f"s3://{self.test_bucket}/{self.test_store_name}",
            "dimension": 768,
            "vector_count": 100,
            "metadata_keys": 50,
            "index_size_mb": 2.5,
        }
        mock_backend.get_store_info.return_value = info
        mock_get_backend.return_value = mock_backend

        # Run command with S3 options
        result = self.runner.invoke(
            store,
            [
                "info",
                self.test_store_name,
                "--bucket",
                self.test_bucket,
                "--region",
                self.test_region,
            ],
        )

        # Assertions
        assert result.exit_code == 0
        assert f"Store: {self.test_store_name}" in result.output
        assert "Backend: s3vectors" in result.output
        mock_backend.get_store_info.assert_called_once_with(self.test_store_name)
        mock_get_backend.assert_called_once_with(
            bucket=self.test_bucket, region=self.test_region, profile=None
        )

    @patch("vector_rag_tool.commands.store.get_backend")
    def test_store_info_json_format(self, mock_get_backend: MagicMock) -> None:
        """Test getting store info in JSON format."""
        # Setup mock
        mock_backend = MagicMock()
        info = {
            "name": self.test_store_name,
            "backend": "faiss",
            "location": "/path/to/store.faiss",
            "dimension": 768,
            "vector_count": 100,
            "metadata_keys": 50,
            "index_size_mb": 2.5,
        }
        mock_backend.get_store_info.return_value = info
        mock_get_backend.return_value = mock_backend

        # Run command
        result = self.runner.invoke(
            store,
            ["info", self.test_store_name, "--format", "json"],
        )

        # Assertions
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["name"] == self.test_store_name
        assert data["backend"] == "faiss"
        assert data["vector_count"] == 100

    @patch("vector_rag_tool.commands.store.get_backend")
    def test_store_info_not_exists(self, mock_get_backend: MagicMock) -> None:
        """Test getting store info when store doesn't exist."""
        # Setup mock to raise ValueError
        mock_backend = MagicMock()
        mock_backend.get_store_info.side_effect = ValueError(
            f"Store '{self.test_store_name}' does not exist"
        )
        mock_get_backend.return_value = mock_backend

        # Run command
        result = self.runner.invoke(
            store,
            ["info", self.test_store_name],
        )

        # Assertions
        assert result.exit_code != 0
        assert "does not exist" in result.output

    @patch("vector_rag_tool.commands.store.get_backend")
    def test_verbose_logging(self, mock_get_backend: MagicMock) -> None:
        """Test that verbose flag enables detailed logging."""
        # Setup mock
        mock_backend = MagicMock()
        mock_backend.store_exists.return_value = False
        mock_backend.create_store.return_value = None
        mock_get_backend.return_value = mock_backend

        # Run command with verbose flag (passed to create subcommand)
        result = self.runner.invoke(
            store,
            ["create", self.test_store_name, "-v"],
        )

        # Assertions - should still work with verbose logging
        assert result.exit_code == 0
        mock_backend.create_store.assert_called_once()


class TestStoreCommandIntegration:
    """Integration tests for store commands with real FAISS backend."""

    def setup_method(self) -> None:
        """Set up test fixtures with temporary directory."""
        self.runner = CliRunner()
        self.test_store_name = "integration-test-store"

        # Create temporary directory for test stores
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self) -> None:
        """Clean up after each test method."""
        # Clean up any test stores that might have been created

        stores_dir = Path.home() / ".config" / "vector-rag-tool" / "stores"
        test_store_file = stores_dir / f"{self.test_store_name}.faiss"
        test_meta_file = stores_dir / f"{self.test_store_name}.meta.json"

        if test_store_file.exists():
            test_store_file.unlink()
        if test_meta_file.exists():
            test_meta_file.unlink()

    def test_end_to_end_store_operations(self) -> None:
        """Test complete store lifecycle: create, list, info, delete."""
        # Create store
        result = self.runner.invoke(
            store,
            ["create", self.test_store_name, "--dimension", 384],
        )
        assert result.exit_code == 0

        # List stores - should include our test store
        result = self.runner.invoke(
            store,
            ["list"],
        )
        assert result.exit_code == 0
        assert self.test_store_name in result.output

        # Get store info
        result = self.runner.invoke(
            store,
            ["info", self.test_store_name],
        )
        assert result.exit_code == 0
        assert f"Store: {self.test_store_name}" in result.output
        assert "Dimension: 384" in result.output

        # Delete store
        result = self.runner.invoke(
            store,
            ["delete", self.test_store_name, "--force"],
        )
        assert result.exit_code == 0

        # Verify store is gone
        result = self.runner.invoke(
            store,
            ["list"],
        )
        assert result.exit_code == 0
        assert self.test_store_name not in result.output
