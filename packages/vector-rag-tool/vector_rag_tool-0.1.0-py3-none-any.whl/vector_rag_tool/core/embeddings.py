"""Ollama embedding integration for vector-rag-tool.

This module provides embeddings generation using Ollama's local API
with the embeddinggemma model, producing 768-dimensional vectors.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from __future__ import annotations

import ollama

from vector_rag_tool.logging_config import get_logger

logger = get_logger(__name__)


class OllamaEmbeddings:
    """Generate embeddings using Ollama local API."""

    def __init__(self, model: str = "embeddinggemma", host: str | None = None) -> None:
        """Initialize Ollama embeddings.

        Args:
            model: Model name to use for embeddings (default: embeddinggemma)
            host: Ollama host URL (default: http://localhost:11434)
        """
        self.model = model
        self.host = host
        self._dimension: int | None = None
        self._client = ollama.Client(host=host) if host else None

    @property
    def dimension(self) -> int:
        """Return embedding dimension (768 for embeddinggemma)."""
        if self._dimension is None:
            # Get dimension from a test embedding
            test_embedding = self.embed_text("test")
            self._dimension = len(test_embedding)
        return self._dimension

    def embed_text(self, text: str) -> list[float]:
        """Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            768-dimensional embedding vector

        Raises:
            RuntimeError: If embedding generation fails
        """
        logger.debug("Embedding text: %s...", text[:50])

        try:
            if self._client:
                response = self._client.embed(model=self.model, input=text)
            else:
                response = ollama.embed(model=self.model, input=text)
            embedding: list[float] = response["embeddings"][0]
            logger.debug("Generated embedding with %d dimensions", len(embedding))
            return embedding

        except Exception as e:
            logger.error("Embedding failed for text: %s...", text[:50])
            logger.debug("Full traceback:", exc_info=True)
            raise RuntimeError(f"Embedding generation failed: {e}") from e

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed

        Returns:
            List of 768-dimensional embedding vectors

        Raises:
            RuntimeError: If embedding generation fails
        """
        logger.debug("Embedding batch of %d texts", len(texts))

        try:
            if self._client:
                response = self._client.embed(model=self.model, input=texts)
            else:
                response = ollama.embed(model=self.model, input=texts)
            embeddings: list[list[float]] = response["embeddings"]
            logger.debug("Generated %d embeddings", len(embeddings))
            return embeddings

        except Exception as e:
            logger.error("Batch embedding failed for %d texts", len(texts))
            logger.debug("Full traceback:", exc_info=True)
            raise RuntimeError(f"Batch embedding generation failed: {e}") from e

    def embed_query(self, query: str) -> list[float]:
        """Generate embedding for a search query with optimal formatting.

        Args:
            query: Search query to embed

        Returns:
            768-dimensional embedding vector optimized for search
        """
        # Format query for optimal retrieval as per EmbeddingG docs
        formatted_query = f"task: search result | query: {query}"
        return self.embed_text(formatted_query)

    def embed_document(self, content: str, title: str | None = None) -> list[float]:
        """Generate embedding for document content with optimal formatting.

        Args:
            content: Document text content
            title: Optional document title

        Returns:
            768-dimensional embedding vector optimized for document storage
        """
        # Format document for embedding as per EmbeddingG docs
        title_part = title if title else "none"
        formatted_content = f"title: {title_part} | text: {content}"
        return self.embed_text(formatted_content)


def format_query(query: str) -> str:
    """Format query for optimal retrieval.

    Args:
        query: Raw search query

    Returns:
        Formatted query string for embedding
    """
    return f"task: search result | query: {query}"


def format_document(content: str, title: str | None = None) -> str:
    """Format document for embedding.

    Args:
        content: Document text content
        title: Optional document title

    Returns:
        Formatted document string for embedding
    """
    title_part = title if title else "none"
    return f"title: {title_part} | text: {content}"
