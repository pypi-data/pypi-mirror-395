"""Tests for OllamaEmbeddings class.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from __future__ import annotations

from unittest.mock import Mock, patch

import pytest

from vector_rag_tool.core.embeddings import OllamaEmbeddings, format_document, format_query


class TestOllamaEmbeddings:
    """Test cases for OllamaEmbeddings class."""

    @patch("vector_rag_tool.core.embeddings.ollama")
    def test_init_default(self, mock_ollama: Mock) -> None:
        """Test default initialization."""
        embeddings = OllamaEmbeddings()

        assert embeddings.model == "embeddinggemma"
        assert embeddings.host is None
        assert embeddings._dimension is None
        mock_ollama.host.assert_not_called()

    @patch("vector_rag_tool.core.embeddings.ollama")
    def test_init_with_host(self, mock_ollama: Mock) -> None:
        """Test initialization with custom host."""
        host = "http://example.com:11434"
        embeddings = OllamaEmbeddings(host=host)

        assert embeddings.host == host
        mock_ollama.host = host

    @patch("vector_rag_tool.core.embeddings.ollama")
    def test_embed_text_success(self, mock_ollama: Mock) -> None:
        """Test successful single text embedding."""
        test_embedding = [0.1] * 768
        mock_ollama.embed.return_value = {"embeddings": [test_embedding]}

        embeddings = OllamaEmbeddings()
        result = embeddings.embed_text("test text")

        assert result == test_embedding
        mock_ollama.embed.assert_called_once_with(model="embeddinggemma", input="test text")

    @patch("vector_rag_tool.core.embeddings.ollama")
    def test_embed_text_failure(self, mock_ollama: Mock) -> None:
        """Test embedding failure handling."""
        mock_ollama.embed.side_effect = Exception("Connection failed")

        embeddings = OllamaEmbeddings()

        with pytest.raises(RuntimeError, match="Embedding generation failed"):
            embeddings.embed_text("test text")

    @patch("vector_rag_tool.core.embeddings.ollama")
    def test_embed_batch_success(self, mock_ollama: Mock) -> None:
        """Test successful batch embedding."""
        test_embeddings = [[0.1] * 768, [0.2] * 768]
        mock_ollama.embed.return_value = {"embeddings": test_embeddings}

        embeddings = OllamaEmbeddings()
        texts = ["text 1", "text 2"]
        result = embeddings.embed_batch(texts)

        assert result == test_embeddings
        mock_ollama.embed.assert_called_once_with(model="embeddinggemma", input=texts)

    @patch("vector_rag_tool.core.embeddings.ollama")
    def test_embed_batch_failure(self, mock_ollama: Mock) -> None:
        """Test batch embedding failure handling."""
        mock_ollama.embed.side_effect = Exception("Batch failed")

        embeddings = OllamaEmbeddings()

        with pytest.raises(RuntimeError, match="Batch embedding generation failed"):
            embeddings.embed_batch(["text 1", "text 2"])

    @patch("vector_rag_tool.core.embeddings.ollama")
    def test_embed_query(self, mock_ollama: Mock) -> None:
        """Test query embedding with formatting."""
        test_embedding = [0.1] * 768
        mock_ollama.embed.return_value = {"embeddings": [test_embedding]}

        embeddings = OllamaEmbeddings()
        result = embeddings.embed_query("search query")

        assert result == test_embedding
        mock_ollama.embed.assert_called_once_with(
            model="embeddinggemma", input="task: search result | query: search query"
        )

    @patch("vector_rag_tool.core.embeddings.ollama")
    def test_embed_document_with_title(self, mock_ollama: Mock) -> None:
        """Test document embedding with title."""
        test_embedding = [0.1] * 768
        mock_ollama.embed.return_value = {"embeddings": [test_embedding]}

        embeddings = OllamaEmbeddings()
        result = embeddings.embed_document("content", "title")

        assert result == test_embedding
        mock_ollama.embed.assert_called_once_with(
            model="embeddinggemma", input="title: title | text: content"
        )

    @patch("vector_rag_tool.core.embeddings.ollama")
    def test_embed_document_without_title(self, mock_ollama: Mock) -> None:
        """Test document embedding without title."""
        test_embedding = [0.1] * 768
        mock_ollama.embed.return_value = {"embeddings": [test_embedding]}

        embeddings = OllamaEmbeddings()
        result = embeddings.embed_document("content")

        assert result == test_embedding
        mock_ollama.embed.assert_called_once_with(
            model="embeddinggemma", input="title: none | text: content"
        )

    @patch("vector_rag_tool.core.embeddings.ollama")
    def test_dimension_property(self, mock_ollama: Mock) -> None:
        """Test dimension property calculation."""
        test_embedding = [0.1] * 768
        mock_ollama.embed.return_value = {"embeddings": [test_embedding]}

        embeddings = OllamaEmbeddings()

        # First call should calculate dimension
        assert embeddings.dimension == 768
        mock_ollama.embed.assert_called_once_with(model="embeddinggemma", input="test")

        # Second call should use cached value
        assert embeddings.dimension == 768
        mock_ollama.embed.assert_called_once()  # No additional call

    @patch("vector_rag_tool.core.embeddings.ollama")
    def test_custom_model(self, mock_ollama: Mock) -> None:
        """Test using custom model."""
        test_embedding = [0.1] * 768
        mock_ollama.embed.return_value = {"embeddings": [test_embedding]}

        embeddings = OllamaEmbeddings(model="custom-model")
        result = embeddings.embed_text("test")

        assert result == test_embedding
        mock_ollama.embed.assert_called_once_with(model="custom-model", input="test")


class TestUtilityFunctions:
    """Test cases for utility functions."""

    def test_format_query(self) -> None:
        """Test query formatting."""
        query = "search query"
        expected = "task: search result | query: search query"
        assert format_query(query) == expected

    def test_format_document_with_title(self) -> None:
        """Test document formatting with title."""
        content = "document content"
        title = "document title"
        expected = "title: document title | text: document content"
        assert format_document(content, title) == expected

    def test_format_document_without_title(self) -> None:
        """Test document formatting without title."""
        content = "document content"
        expected = "title: none | text: document content"
        assert format_document(content) == expected


class TestIntegration:
    """Integration tests (require actual Ollama instance)."""

    @pytest.mark.slow
    @pytest.mark.integration
    def test_real_embedding(self) -> None:
        """Test real embedding generation (requires Ollama running).

        This test is marked as integration and slow, and will only run
        when explicitly requested with: pytest -m integration -m slow
        """
        try:
            embeddings = OllamaEmbeddings()
            result = embeddings.embed_text("test text")

            assert isinstance(result, list)
            assert len(result) == 768
            assert all(isinstance(x, float) for x in result)
        except RuntimeError as e:
            if "Connection refused" in str(e):
                pytest.skip("Ollama not running - skipping integration test")
            raise

    @pytest.mark.slow
    @pytest.mark.integration
    def test_real_batch_embedding(self) -> None:
        """Test real batch embedding generation (requires Ollama running)."""
        try:
            embeddings = OllamaEmbeddings()
            texts = ["text 1", "text 2", "text 3"]
            results = embeddings.embed_batch(texts)

            assert isinstance(results, list)
            assert len(results) == len(texts)
            for result in results:
                assert isinstance(result, list)
                assert len(result) == 768
                assert all(isinstance(x, float) for x in result)
        except RuntimeError as e:
            if "Connection refused" in str(e):
                pytest.skip("Ollama not running - skipping integration test")
            raise
