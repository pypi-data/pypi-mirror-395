"""
Tests for the query command.

This module contains comprehensive tests for the query CLI command, including
argument parsing, option handling, input validation, and output formatting.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from vector_rag_tool.commands.query import query
from vector_rag_tool.core.models import Chunk, ChunkMetadata, QueryResult


@pytest.fixture
def runner():
    """Create a Click test runner."""
    return CliRunner()


@pytest.fixture
def mock_querier():
    """Create a mock querier service."""
    querier = MagicMock()

    # Mock store exists check
    querier.backend.store_exists.return_value = True
    querier.backend.list_stores.return_value = ["test-store"]

    # Create mock query result
    chunk1 = Chunk(
        id="chunk1",
        content="This is about machine learning algorithms",
        metadata=ChunkMetadata(
            source_file="docs/ml.md",
            line_start=1,
            line_end=10,
            chunk_index=0,
            total_chunks=2,
            tags=["ml", "algorithms"],
            links=["[[neural-networks]]"],
            frontmatter={"title": "Machine Learning"},
        ),
    )

    chunk2 = Chunk(
        id="chunk2",
        content="Deep learning uses neural networks",
        metadata=ChunkMetadata(
            source_file="docs/dl.md",
            line_start=15,
            line_end=25,
            chunk_index=1,
            total_chunks=3,
            tags=["dl", "neural"],
            links=[],
            frontmatter={},
        ),
    )

    result = QueryResult(
        query="machine learning",
        chunks=[chunk1, chunk2],
        scores=[0.95, 0.87],
        store_name="test-store",
        total_results=2,
        query_time=0.123,
    )

    querier.query.return_value = result
    return querier


class TestQueryCommand:
    """Test cases for the query command."""

    def test_query_basic_success(self, runner, mock_querier):
        """Test basic query with text argument."""
        with patch("vector_rag_tool.commands.query.Querier", return_value=mock_querier):
            result = runner.invoke(query, ["machine learning", "--store", "test-store"])

            assert result.exit_code == 0
            assert "Query: 'machine learning'" in result.output
            assert "Store: test-store" in result.output
            assert "Results: 2/5" in result.output
            assert "Time: 0.123s" in result.output
            assert "Score: 0.950" in result.output
            assert "📄 docs/ml.md:1-10" in result.output
            assert "🏷️  Tags: ml, algorithms" in result.output

    def test_query_with_custom_top_k(self, runner, mock_querier):
        """Test query with custom top-k value."""
        with patch("vector_rag_tool.commands.query.Querier", return_value=mock_querier):
            result = runner.invoke(
                query, ["deep learning", "--store", "test-store", "--top-k", "10"]
            )

            assert result.exit_code == 0
            assert "Results: 2/10" in result.output
            mock_querier.query.assert_called_once_with(
                store_name="test-store",
                query_text="deep learning",
                top_k=10,
                min_score=0.0,
                snippet_length=300,
            )

    def test_query_json_output(self, runner, mock_querier):
        """Test query with JSON output format."""
        with patch("vector_rag_tool.commands.query.Querier", return_value=mock_querier):
            result = runner.invoke(query, ["neural networks", "--store", "test-store", "--json"])

            assert result.exit_code == 0

            # Parse JSON output
            output_data = json.loads(result.output)
            assert output_data["query"] == "neural networks"
            assert output_data["store"] == "test-store"
            assert output_data["total_results"] == 2
            assert output_data["requested_results"] == 5
            assert output_data["query_time"] == 0.123
            assert len(output_data["results"]) == 2

            # Check first result
            first_result = output_data["results"][0]
            assert first_result["score"] == 0.95
            assert first_result["file_path"] == "docs/ml.md"
            assert first_result["line_start"] == 1
            assert first_result["line_end"] == 10
            assert first_result["content"] == "This is about machine learning algorithms"
            assert first_result["tags"] == ["ml", "algorithms"]
            assert first_result["links"] == ["[[neural-networks]]"]

    def test_query_stdin_input(self, runner, mock_querier):
        """Test query reading from stdin."""
        with patch("vector_rag_tool.commands.query.Querier", return_value=mock_querier):
            result = runner.invoke(
                query, ["--store", "test-store", "--stdin"], input="transformer models\n"
            )

            assert result.exit_code == 0
            assert "Query: 'transformer models'" in result.output
            mock_querier.query.assert_called_once_with(
                store_name="test-store",
                query_text="transformer models",
                top_k=5,
                min_score=0.0,
                snippet_length=300,
            )

    def test_query_verbose_output(self, runner, mock_querier):
        """Test query with verbose logging."""
        with patch("vector_rag_tool.commands.query.Querier", return_value=mock_querier):
            result = runner.invoke(query, ["test query", "--store", "test-store", "-vv"])

            assert result.exit_code == 0
            # Command should still work with verbose flag

    def test_query_shows_help_without_text(self, runner):
        """Test query shows helpful use cases without text argument."""
        result = runner.invoke(query, ["--store", "test-store"])

        assert result.exit_code == 0
        assert "Use cases:" in result.output
        assert "--store" in result.output

    def test_query_empty_stdin(self, runner):
        """Test query with empty stdin."""
        result = runner.invoke(query, ["--store", "test-store", "--stdin"], input="")

        assert result.exit_code == 1
        assert "No input received from stdin" in result.output

    def test_query_stdin_not_available(self, runner):
        """Test query with stdin flag when no stdin is available."""
        # Simulate no stdin available by making stdin empty and isatty return True
        with patch("sys.stdin.isatty", return_value=True):
            # Don't provide any input
            result = runner.invoke(
                query,
                ["--store", "test-store", "--stdin"],
                input="",  # Empty input
            )

            assert result.exit_code == 1
            # The exact error message may vary, but it should be about empty stdin
            assert (
                "No input received from stdin" in result.output or "stdin" in result.output.lower()
            )

    def test_query_store_not_exists(self, runner):
        """Test query with non-existent store."""
        with patch("vector_rag_tool.commands.query.Querier") as mock_querier_class:
            mock_querier = MagicMock()
            mock_querier.backend.store_exists.return_value = False
            mock_querier.list_stores.return_value = ["other-store"]
            mock_querier_class.return_value = mock_querier

            result = runner.invoke(query, ["test query", "--store", "missing-store"])

            assert result.exit_code == 1
            assert "Store 'missing-store' does not exist" in result.output
            assert "Available stores: other-store" in result.output

    def test_query_invalid_top_k(self, runner):
        """Test query with invalid top-k value."""
        result = runner.invoke(query, ["test", "--store", "test-store", "--top-k", "0"])

        assert result.exit_code == 1
        assert "top-k must be at least 1" in result.output

    def test_query_no_results(self, runner):
        """Test query with no matching results."""
        with patch("vector_rag_tool.commands.query.Querier") as mock_querier_class:
            mock_querier = MagicMock()
            mock_querier.backend.store_exists.return_value = True
            mock_querier.query.return_value = QueryResult(
                query="no match",
                chunks=[],
                scores=[],
                store_name="test-store",
                total_results=0,
            )
            mock_querier_class.return_value = mock_querier

            result = runner.invoke(query, ["no match", "--store", "test-store"])

            assert result.exit_code == 0
            assert "No results found for query: 'no match'" in result.output
            assert "Store: test-store" in result.output

    def test_query_querier_value_error(self, runner):
        """Test query when querier raises ValueError."""
        with patch("vector_rag_tool.commands.query.Querier") as mock_querier_class:
            mock_querier = MagicMock()
            mock_querier.backend.store_exists.return_value = True
            mock_querier.query.side_effect = ValueError("Invalid query")
            mock_querier_class.return_value = mock_querier

            result = runner.invoke(query, ["bad query", "--store", "test-store"])

            assert result.exit_code == 1
            assert "Query failed: Invalid query" in result.output

    def test_query_querier_runtime_error(self, runner):
        """Test query when querier raises RuntimeError."""
        with patch("vector_rag_tool.commands.query.Querier") as mock_querier_class:
            mock_querier = MagicMock()
            mock_querier.backend.store_exists.return_value = True
            mock_querier.query.side_effect = RuntimeError("Service unavailable")
            mock_querier_class.return_value = mock_querier

            result = runner.invoke(query, ["test", "--store", "test-store"])

            assert result.exit_code == 1
            assert "Query error: Service unavailable" in result.output

    def test_query_querier_unexpected_error(self, runner):
        """Test query when querier raises unexpected error."""
        with patch("vector_rag_tool.commands.query.Querier") as mock_querier_class:
            mock_querier = MagicMock()
            mock_querier.backend.store_exists.return_value = True
            mock_querier.query.side_effect = Exception("Unexpected error")
            mock_querier_class.return_value = mock_querier

            result = runner.invoke(query, ["test", "--store", "test-store"])

            assert result.exit_code == 1
            assert "Unexpected error: Unexpected error" in result.output

    def test_query_result_without_line_numbers(self, runner, mock_querier):
        """Test query output for chunks without line numbers."""
        # Create chunk without line numbers
        chunk = Chunk(
            id="chunk1",
            content="Content without lines",
            metadata=ChunkMetadata(
                source_file="doc.txt",
                line_start=None,
                line_end=None,
                chunk_index=0,
                total_chunks=1,
                tags=[],
                links=[],
                frontmatter={},
            ),
        )

        result = QueryResult(
            query="test",
            chunks=[chunk],
            scores=[0.9],
            store_name="test-store",
            total_results=1,
        )
        mock_querier.query.return_value = result

        with patch("vector_rag_tool.commands.query.Querier", return_value=mock_querier):
            result = runner.invoke(query, ["test", "--store", "test-store"])

            assert result.exit_code == 0
            assert "📄 doc.txt" in result.output  # Should not show line numbers

    def test_query_result_with_minimal_metadata(self, runner, mock_querier):
        """Test query output for chunks with minimal metadata."""
        # Create chunk with minimal metadata
        chunk = Chunk(
            id="chunk1",
            content="Minimal content",
            metadata=ChunkMetadata(
                source_file="minimal.md",
                line_start=1,
                line_end=1,
                chunk_index=0,
                total_chunks=1,
                tags=[],
                links=[],
                frontmatter={},
            ),
        )

        result = QueryResult(
            query="test",
            chunks=[chunk],
            scores=[0.9],
            store_name="test-store",
            total_results=1,
        )
        mock_querier.query.return_value = result

        with patch("vector_rag_tool.commands.query.Querier", return_value=mock_querier):
            result = runner.invoke(query, ["test", "--store", "test-store"])

            assert result.exit_code == 0
            # Should not show tags or links sections when empty
            assert "🏷️" not in result.output
            assert "🔗" not in result.output

    def test_query_json_with_empty_metadata(self, runner, mock_querier):
        """Test JSON output with empty metadata values (None converted to empty)."""
        # Create chunk with None metadata fields (will be converted to empty)
        chunk = Chunk(
            id="chunk1",
            content="Content",
            metadata=ChunkMetadata(
                source_file="test.md",
                line_start=1,
                line_end=1,
                chunk_index=0,
                total_chunks=1,
                tags=None,  # Will be converted to []
                links=None,  # Will be converted to []
                frontmatter=None,  # Will be converted to {}
            ),
        )

        result = QueryResult(
            query="test",
            chunks=[chunk],
            scores=[0.9],
            store_name="test-store",
            total_results=1,
        )
        mock_querier.query.return_value = result

        with patch("vector_rag_tool.commands.query.Querier", return_value=mock_querier):
            result = runner.invoke(query, ["test", "--store", "test-store", "--json"])

            assert result.exit_code == 0

            # Parse and verify JSON handles empty values
            output_data = json.loads(result.output)
            result_item = output_data["results"][0]
            assert result_item["tags"] == []
            assert result_item["links"] == []
            assert result_item["frontmatter"] == {}

    def test_query_with_s3_backend(self, runner, mock_querier):
        """Test query with S3 backend using bucket option."""
        with (
            patch("vector_rag_tool.commands.query.get_backend") as mock_get_backend,
            patch("vector_rag_tool.commands.query.Querier", return_value=mock_querier),
        ):
            mock_backend = MagicMock()
            mock_get_backend.return_value = mock_backend

            result = runner.invoke(
                query, ["machine learning", "--store", "test-store", "--bucket", "my-bucket"]
            )

            assert result.exit_code == 0
            mock_get_backend.assert_called_once_with(
                bucket="my-bucket", region="eu-central-1", profile=None
            )
            mock_querier.query.assert_called_once()

    def test_query_with_s3_backend_all_options(self, runner, mock_querier):
        """Test query with S3 backend using all AWS options."""
        with (
            patch("vector_rag_tool.commands.query.get_backend") as mock_get_backend,
            patch("vector_rag_tool.commands.query.Querier", return_value=mock_querier),
        ):
            mock_backend = MagicMock()
            mock_get_backend.return_value = mock_backend

            result = runner.invoke(
                query,
                [
                    "test query",
                    "--store",
                    "test-store",
                    "--bucket",
                    "vector-store",
                    "--region",
                    "us-west-2",
                    "--profile",
                    "dev",
                ],
            )

            assert result.exit_code == 0
            mock_get_backend.assert_called_once_with(
                bucket="vector-store", region="us-west-2", profile="dev"
            )
            mock_querier.query.assert_called_once()

    def test_query_with_local_backend_default(self, runner, mock_querier):
        """Test query defaults to local FAISS backend when no bucket specified."""
        with (
            patch("vector_rag_tool.commands.query.get_backend") as mock_get_backend,
            patch("vector_rag_tool.commands.query.Querier", return_value=mock_querier),
        ):
            mock_backend = MagicMock()
            mock_get_backend.return_value = mock_backend

            result = runner.invoke(query, ["local query", "--store", "test-store"])

            assert result.exit_code == 0
            mock_get_backend.assert_called_once_with(
                bucket=None, region="eu-central-1", profile=None
            )
            mock_querier.query.assert_called_once()

    def test_query_with_custom_region_default(self, runner, mock_querier):
        """Test query with custom region but no bucket uses FAISS."""
        with (
            patch("vector_rag_tool.commands.query.get_backend") as mock_get_backend,
            patch("vector_rag_tool.commands.query.Querier", return_value=mock_querier),
        ):
            mock_backend = MagicMock()
            mock_get_backend.return_value = mock_backend

            result = runner.invoke(
                query, ["test", "--store", "test-store", "--region", "ap-southeast-1"]
            )

            assert result.exit_code == 0
            mock_get_backend.assert_called_once_with(
                bucket=None, region="ap-southeast-1", profile=None
            )
            mock_querier.query.assert_called_once()
