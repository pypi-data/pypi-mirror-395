"""
Querier service for RAG operations using FAISS and Ollama.

This module provides high-level query functionality that combines Ollama embeddings
with FAISS vector search to retrieve relevant document chunks from indexed stores.
Includes snippet extraction and result ranking capabilities.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from __future__ import annotations

import time
from typing import Any

from vector_rag_tool.core.backend import VectorBackend
from vector_rag_tool.core.embeddings import OllamaEmbeddings
from vector_rag_tool.core.faiss_backend import FAISSBackend
from vector_rag_tool.core.models import Chunk, ChunkMetadata, QueryResult
from vector_rag_tool.logging_config import get_logger

logger = get_logger(__name__)


class Querier:
    """High-level querier for RAG operations using configurable backends."""

    def __init__(
        self,
        backend: VectorBackend | None = None,
        embedding_model: str = "embeddinggemma",
        ollama_host: str | None = None,
    ) -> None:
        """Initialize the querier.

        Args:
            backend: Vector backend to use (FAISSBackend, S3VectorsBackend, etc.)
                     If None, uses FAISSBackend for local storage.
            embedding_model: Ollama model to use for embeddings (default: embeddinggemma)
            ollama_host: Ollama host URL (default: http://localhost:11434)
        """
        self.embeddings = OllamaEmbeddings(model=embedding_model, host=ollama_host)
        self.backend = backend if backend is not None else FAISSBackend()
        logger.debug(
            "Querier initialized with model '%s', host '%s', and backend '%s'",
            embedding_model,
            ollama_host or "default",
            type(self.backend).__name__,
        )

    def query(
        self,
        store_name: str,
        query_text: str,
        top_k: int = 5,
        min_score: float | None = None,
        snippet_length: int = 200,
    ) -> QueryResult:
        """Query a vector store for relevant chunks.

        Args:
            store_name: Name of the store to query
            query_text: The query text to search for
            top_k: Maximum number of results to return (default: 5)
            min_score: Minimum similarity score threshold (optional)
            snippet_length: Length of extracted snippets in characters (default: 200)

        Returns:
            QueryResult with matched chunks and scores

        Raises:
            ValueError: If store doesn't exist or query is invalid
            RuntimeError: If embedding generation or query fails
        """
        start_time = time.time()

        logger.info(
            "Querying store '%s' with top_k=%d, min_score=%s",
            store_name,
            top_k,
            min_score or "none",
        )

        # Validate store exists
        if not self.backend.store_exists(store_name):
            raise ValueError(f"Store '{store_name}' does not exist")

        # Generate embedding for the query
        logger.debug("Generating embedding for query: %s", query_text[:100])
        try:
            query_vector = self.embeddings.embed_query(query_text)
            logger.debug("Generated query embedding with %d dimensions", len(query_vector))
        except Exception as e:
            logger.error("Failed to generate embedding for query: %s", query_text[:100])
            raise RuntimeError(f"Query embedding failed: {e}") from e

        # Search for similar vectors
        try:
            vector_results = self.backend.query(store_name, query_vector, top_k)
            logger.debug("FAISS search returned %d results", len(vector_results))
        except Exception as e:
            logger.error("FAISS query failed for store '%s'", store_name)
            raise RuntimeError(f"Vector search failed: {e}") from e

        # Convert VectorQueryResult to Chunk objects
        chunks: list[Chunk] = []
        scores: list[float] = []

        for result in vector_results:
            # Apply score threshold if specified
            if min_score is not None and result.score < min_score:
                logger.debug(
                    "Skipping result with score %.3f below threshold %.3f",
                    result.score,
                    min_score,
                )
                continue

            # Extract chunk metadata
            metadata = result.metadata
            if not isinstance(metadata, dict):
                logger.warning(
                    "Invalid metadata format for result '%s': %s", result.key, type(metadata)
                )
                continue

            # Reconstruct ChunkMetadata
            chunk_metadata = ChunkMetadata(
                source_file=metadata.get("source_file", ""),
                line_start=metadata.get("line_start", 0),
                line_end=metadata.get("line_end", 0),
                chunk_index=metadata.get("chunk_index", 0),
                total_chunks=metadata.get("total_chunks", 1),
                tags=metadata.get("tags", []),
                links=metadata.get("links", []),
                frontmatter=metadata.get("frontmatter", {}),
                word_count=metadata.get("word_count"),
                char_count=metadata.get("char_count"),
            )

            # Extract content with snippet
            content = result.content or ""
            if content and len(content) > snippet_length:
                # Extract a snippet around the most relevant part
                snippet = self._extract_snippet(content, query_text, snippet_length)
                content = snippet

            # Create Chunk object
            chunk = Chunk(
                id=result.key,
                content=content,
                metadata=chunk_metadata,
                store_name=store_name,
            )

            chunks.append(chunk)
            scores.append(result.score)

        # Calculate query time
        query_time = time.time() - start_time

        logger.info(
            "Query completed in %.2fs, returned %d chunks",
            query_time,
            len(chunks),
        )

        # Create and return QueryResult
        return QueryResult(
            query=query_text,
            chunks=chunks,
            scores=scores,
            store_name=store_name,
            total_results=len(chunks),
            query_time=query_time,
            metadata={
                "top_k": top_k,
                "min_score": min_score,
                "snippet_length": snippet_length,
                "embedding_model": self.embeddings.model,
            },
        )

    def _extract_snippet(self, content: str, query: str, max_length: int) -> str:
        """Extract a relevant snippet from content based on query terms.

        Args:
            content: Full text content
            query: Query text to find relevant terms
            max_length: Maximum length of snippet in characters

        Returns:
            Extracted snippet with query terms highlighted if possible
        """
        if not content or len(content) <= max_length:
            return content

        # Split query into individual terms
        query_terms = [term.lower() for term in query.split() if len(term) > 2]

        # Try to find the best window with most query terms
        best_start = 0
        best_score = 0

        content_lower = content.lower()
        window_size = max_length

        # Slide a window through the content
        for i in range(0, len(content) - window_size + 1, 50):  # Step by 50 for efficiency
            window = content_lower[i : i + window_size]
            score = sum(1 for term in query_terms if term in window)

            if score > best_score:
                best_score = score
                best_start = i

        # If no query terms found, return the beginning
        if best_score == 0:
            return content[:max_length] + "..."

        # Extract the best window
        snippet = content[best_start : best_start + max_length]

        # Add ellipsis if we're not at the start/end
        if best_start > 0:
            snippet = "..." + snippet
        if best_start + max_length < len(content):
            snippet = snippet + "..."

        return snippet

    def get_store_info(self, store_name: str) -> dict[str, Any]:
        """Get information about a store.

        Args:
            store_name: Name of the store

        Returns:
            Dictionary with store information

        Raises:
            ValueError: If store doesn't exist
        """
        logger.debug("Getting info for store '%s'", store_name)
        return self.backend.get_store_info(store_name)

    def list_stores(self) -> list[str]:
        """List all available stores.

        Returns:
            List of store names
        """
        stores = self.backend.list_stores()
        logger.debug("Found %d stores: %s", len(stores), stores)
        return stores
