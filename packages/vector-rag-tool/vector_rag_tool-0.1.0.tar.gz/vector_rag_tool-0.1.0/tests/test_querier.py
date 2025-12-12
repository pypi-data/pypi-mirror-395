"""
Tests for the querier service.

This module contains comprehensive tests for the Querier class, including
query functionality, embedding generation, FAISS search, and snippet extraction.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from vector_rag_tool.core.backend import VectorQueryResult
from vector_rag_tool.core.faiss_backend import FAISSBackend
from vector_rag_tool.core.models import QueryResult
from vector_rag_tool.services.querier import Querier


@pytest.fixture
def mock_faiss_backend():
    """Create a mock FAISS backend."""
    backend = MagicMock(spec=FAISSBackend)
    backend.store_exists.return_value = True
    backend.get_store_info.return_value = {
        "name": "test-store",
        "backend": "faiss",
        "vector_count": 10,
        "dimension": 768,
    }
    backend.list_stores.return_value = ["test-store", "another-store"]
    return backend


@pytest.fixture
def mock_embeddings():
    """Create a mock embeddings service."""
    embeddings = MagicMock()
    embeddings.model = "embeddinggemma"
    embeddings.embed_query.return_value = [0.1] * 768
    return embeddings


@pytest.fixture
def querier(mock_faiss_backend, mock_embeddings):
    """Create a querier with mocked dependencies."""
    with (
        patch(
            "vector_rag_tool.services.querier.FAISSBackend",
            return_value=mock_faiss_backend,
        ),
        patch(
            "vector_rag_tool.services.querier.OllamaEmbeddings",
            return_value=mock_embeddings,
        ),
    ):
        return Querier(embedding_model="embeddinggemma")


class TestQuerier:
    """Test cases for the Querier class."""

    def test_init_default(self):
        """Test querier initialization with default parameters."""
        with (
            patch("vector_rag_tool.services.querier.FAISSBackend") as mock_backend,
            patch("vector_rag_tool.services.querier.OllamaEmbeddings") as mock_embeddings,
        ):
            Querier()
            mock_backend.assert_called_once()
            mock_embeddings.assert_called_once_with(model="embeddinggemma", host=None)

    def test_init_with_params(self):
        """Test querier initialization with custom parameters."""
        with (
            patch("vector_rag_tool.services.querier.FAISSBackend") as mock_backend,
            patch("vector_rag_tool.services.querier.OllamaEmbeddings") as mock_embeddings,
        ):
            Querier(embedding_model="custom-model", ollama_host="http://localhost:11435")
            mock_backend.assert_called_once()
            mock_embeddings.assert_called_once_with(
                model="custom-model",
                host="http://localhost:11435",
            )

    def test_query_success(self, querier, mock_faiss_backend, mock_embeddings):
        """Test successful query execution."""
        # Setup mock vector results
        vector_results = [
            VectorQueryResult(
                key="chunk1",
                score=0.95,
                metadata={
                    "source_file": "test.md",
                    "line_start": 1,
                    "line_end": 10,
                    "chunk_index": 0,
                    "total_chunks": 2,
                    "tags": ["test"],
                    "links": [],
                    "frontmatter": {},
                    "word_count": 50,
                    "char_count": 200,
                },
                content="This is a test chunk with relevant content",
            ),
            VectorQueryResult(
                key="chunk2",
                score=0.85,
                metadata={
                    "source_file": "test.md",
                    "line_start": 11,
                    "line_end": 20,
                    "chunk_index": 1,
                    "total_chunks": 2,
                    "tags": ["test"],
                    "links": [],
                    "frontmatter": {},
                    "word_count": 30,
                    "char_count": 150,
                },
                content="Another chunk with some information",
            ),
        ]
        mock_faiss_backend.query.return_value = vector_results

        # Execute query
        result = querier.query("test-store", "test query", top_k=5)

        # Verify results
        assert isinstance(result, QueryResult)
        assert result.query == "test query"
        assert result.store_name == "test-store"
        assert len(result.chunks) == 2
        assert len(result.scores) == 2
        assert result.scores[0] == 0.95
        assert result.scores[1] == 0.85
        assert result.total_results == 2
        assert result.query_time is not None
        assert result.query_time > 0

        # Verify chunks
        assert result.chunks[0].id == "chunk1"
        assert result.chunks[0].content == "This is a test chunk with relevant content"
        assert str(result.chunks[0].metadata.source_file) == "test.md"
        assert result.chunks[0].metadata.line_start == 1
        assert result.chunks[0].metadata.line_end == 10

        # Verify calls
        mock_embeddings.embed_query.assert_called_once_with("test query")
        mock_faiss_backend.query.assert_called_once()

    def test_query_with_min_score(self, querier, mock_faiss_backend, mock_embeddings):
        """Test query with minimum score threshold."""
        # Setup mock vector results with varying scores
        vector_results = [
            VectorQueryResult(
                key="chunk1",
                score=0.95,
                metadata={
                    "source_file": "test.md",
                    "line_start": 1,
                    "line_end": 10,
                    "chunk_index": 0,
                    "total_chunks": 1,
                    "tags": [],
                    "links": [],
                    "frontmatter": {},
                },
                content="High scoring chunk",
            ),
            VectorQueryResult(
                key="chunk2",
                score=0.45,  # Below threshold
                metadata={
                    "source_file": "test.md",
                    "line_start": 11,
                    "line_end": 20,
                    "chunk_index": 1,
                    "total_chunks": 1,
                    "tags": [],
                    "links": [],
                    "frontmatter": {},
                },
                content="Low scoring chunk",
            ),
        ]
        mock_faiss_backend.query.return_value = vector_results

        # Execute query with min_score
        result = querier.query("test-store", "test query", min_score=0.5)

        # Verify only high-scoring result is included
        assert len(result.chunks) == 1
        assert result.scores[0] == 0.95
        assert result.chunks[0].content == "High scoring chunk"

    def test_query_store_not_exists(self, querier, mock_faiss_backend):
        """Test query with non-existent store."""
        mock_faiss_backend.store_exists.return_value = False

        with pytest.raises(ValueError, match="Store 'missing-store' does not exist"):
            querier.query("missing-store", "test query")

    def test_query_embedding_failure(self, querier, mock_embeddings):
        """Test query when embedding generation fails."""
        mock_embeddings.embed_query.side_effect = Exception("Embedding failed")

        with pytest.raises(RuntimeError, match="Query embedding failed"):
            querier.query("test-store", "test query")

    def test_query_faiss_failure(self, querier, mock_faiss_backend, mock_embeddings):
        """Test query when FAISS search fails."""
        mock_faiss_backend.query.side_effect = Exception("FAISS error")

        with pytest.raises(RuntimeError, match="Vector search failed"):
            querier.query("test-store", "test query")

    def test_extract_snippet_short_content(self, querier):
        """Test snippet extraction for short content."""
        content = "This is short content"
        query = "short"

        result = querier._extract_snippet(content, query, 100)
        assert result == content

    def test_extract_snippet_long_content_with_match(self, querier):
        """Test snippet extraction for long content with query match."""
        content = (
            "This is the beginning of a long document. " * 20
            + " The important term appears here. "
            + "More content here. " * 20
        )
        query = "important term"

        result = querier._extract_snippet(content, query, 100)
        assert "important term" in result.lower()
        assert len(result) <= 110  # Account for ellipsis and boundary conditions
        assert result.startswith("...") or result.endswith("...")

    def test_extract_snippet_long_content_no_match(self, querier):
        """Test snippet extraction for long content without query match."""
        content = "This is a long document with no matching terms. " * 20
        query = "nonexistent term"

        result = querier._extract_snippet(content, query, 100)
        assert len(result) <= 110  # Account for ellipsis and boundary conditions
        assert result.endswith("...")

    def test_get_store_info(self, querier, mock_faiss_backend):
        """Test getting store information."""
        info = querier.get_store_info("test-store")

        assert info["name"] == "test-store"
        assert info["backend"] == "faiss"
        assert info["vector_count"] == 10
        assert info["dimension"] == 768
        mock_faiss_backend.get_store_info.assert_called_once_with("test-store")

    def test_list_stores(self, querier, mock_faiss_backend):
        """Test listing all stores."""
        stores = querier.list_stores()

        assert stores == ["test-store", "another-store"]
        mock_faiss_backend.list_stores.assert_called_once()

    def test_query_with_long_content_snippet_extraction(self, querier, mock_faiss_backend):
        """Test that long content gets truncated with snippet extraction."""
        long_content = "This is a very long content " * 50  # ~800 characters

        vector_results = [
            VectorQueryResult(
                key="chunk1",
                score=0.95,
                metadata={
                    "source_file": "test.md",
                    "line_start": 1,
                    "line_end": 10,
                    "chunk_index": 0,
                    "total_chunks": 1,
                    "tags": [],
                    "links": [],
                    "frontmatter": {},
                },
                content=long_content,
            ),
        ]
        mock_faiss_backend.query.return_value = vector_results

        result = querier.query("test-store", "long content", snippet_length=200)

        # Verify content is truncated
        assert len(result.chunks[0].content) <= 210  # Account for ellipsis and boundary conditions
        assert "long content" in result.chunks[0].content.lower()

    def test_query_with_custom_snippet_length(self, querier, mock_faiss_backend):
        """Test query with custom snippet length."""
        vector_results = [
            VectorQueryResult(
                key="chunk1",
                score=0.95,
                metadata={
                    "source_file": "test.md",
                    "line_start": 1,
                    "line_end": 10,
                    "chunk_index": 0,
                    "total_chunks": 1,
                    "tags": [],
                    "links": [],
                    "frontmatter": {},
                },
                content="A" * 1000,  # Long content
            ),
        ]
        mock_faiss_backend.query.return_value = vector_results

        # Test with custom snippet length
        result = querier.query("test-store", "test", snippet_length=50)
        assert len(result.chunks[0].content) <= 60  # Account for ellipsis and boundary conditions

    def test_query_metadata_in_result(self, querier, mock_faiss_backend):
        """Test that query metadata is included in the result."""
        vector_results = []
        mock_faiss_backend.query.return_value = vector_results

        result = querier.query(
            "test-store",
            "test query",
            top_k=10,
            min_score=0.5,
            snippet_length=150,
        )

        assert result.metadata["top_k"] == 10
        assert result.metadata["min_score"] == 0.5
        assert result.metadata["snippet_length"] == 150
        assert result.metadata["embedding_model"] == "embeddinggemma"

    @patch("time.time")
    def test_query_timing(self, mock_time, querier, mock_faiss_backend, mock_embeddings):
        """Test that query time is accurately measured."""
        # Setup time mock
        mock_time.side_effect = [100.0, 100.5]  # Start and end times

        vector_results = []
        mock_faiss_backend.query.return_value = vector_results

        result = querier.query("test-store", "test query")

        assert result.query_time == 0.5

    def test_query_with_invalid_metadata(self, querier, mock_faiss_backend):
        """Test query handling of invalid metadata."""
        vector_results = [
            VectorQueryResult(
                key="chunk1",
                score=0.95,
                metadata=None,  # Invalid metadata
                content="Content with invalid metadata",
            ),
            VectorQueryResult(
                key="chunk2",
                score=0.85,
                metadata="string",  # Invalid metadata type
                content="Content with string metadata",
            ),
        ]
        mock_faiss_backend.query.return_value = vector_results

        result = querier.query("test-store", "test query")

        # Should skip results with invalid metadata
        assert len(result.chunks) == 0
        assert result.total_results == 0
