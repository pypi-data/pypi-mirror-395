"""
Indexing service that orchestrates file detection, chunking, embedding, and storage.

This module provides the Indexer class which coordinates the entire indexing pipeline:
1. File detection using glob patterns
2. Content chunking with appropriate strategies
3. Batch embedding generation for efficiency
4. Vector storage with incremental indexing support

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from typing import Any

from tqdm import tqdm

from vector_rag_tool.core.backend import VectorBackend
from vector_rag_tool.core.chunking import ChunkerFactory
from vector_rag_tool.core.embeddings import OllamaEmbeddings, format_document
from vector_rag_tool.core.file_detector import (
    detect_files_from_patterns,
)
from vector_rag_tool.core.file_detector import (
    requires_markitdown as file_requires_markitdown,
)
from vector_rag_tool.core.models import Chunk
from vector_rag_tool.logging_config import get_logger

logger = get_logger(__name__)


class IndexingProgress:
    """Tracks indexing progress and statistics."""

    def __init__(self) -> None:
        """Initialize progress tracking."""
        self.files_scanned = 0
        self.files_updated = 0
        self.files_skipped = 0
        self.chunks_created = 0
        self.embeddings_generated = 0
        self.errors: list[tuple[str, Exception]] = []

    def add_error(self, file_path: str, error: Exception) -> None:
        """Record an error that occurred during indexing."""
        self.errors.append((file_path, error))
        logger.error("Error processing %s: %s", file_path, error)

    def get_summary(self) -> dict[str, Any]:
        """Get a summary of indexing results."""
        return {
            "files_scanned": self.files_scanned,
            "files_updated": self.files_updated,
            "files_skipped": self.files_skipped,
            "chunks_created": self.chunks_created,
            "embeddings_generated": self.embeddings_generated,
            "errors_count": len(self.errors),
            "errors": [{"file": f, "error": str(e)} for f, e in self.errors],
        }


class FileHashTracker:
    """Tracks file hashes to support incremental indexing across sessions."""

    def __init__(self, store_name: str, backend: VectorBackend) -> None:
        """
        Initialize file hash tracker.

        Args:
            store_name: Name of the vector store
            backend: Vector backend instance
        """
        self.store_name = store_name
        self.backend = backend
        self._hash_cache: dict[str, str] = {}
        self._loaded = False
        self._dirty = False  # Track if changes need saving

    def _ensure_loaded(self) -> None:
        """Load hash cache from backend if not already loaded."""
        if self._loaded:
            return

        try:
            self._hash_cache = self.backend.get_file_hashes(self.store_name)
            logger.debug(
                "Loaded %d file hashes from store '%s'", len(self._hash_cache), self.store_name
            )
        except Exception as e:
            logger.debug("Could not load file hash cache: %s", e)
            self._hash_cache = {}

        self._loaded = True

    def get_file_hash(self, file_path: str) -> str | None:
        """
        Get stored hash for a file.

        Args:
            file_path: Path to the file

        Returns:
            Stored hash or None if not found
        """
        self._ensure_loaded()
        return self._hash_cache.get(file_path)

    def update_file_hash(self, file_path: str, file_hash: str) -> None:
        """
        Update hash for a file.

        Args:
            file_path: Path to the file
            file_hash: New hash for the file
        """
        self._ensure_loaded()
        if self._hash_cache.get(file_path) != file_hash:
            self._hash_cache[file_path] = file_hash
            self._dirty = True

    def save_hashes(self) -> None:
        """Save hash cache to backend storage."""
        if not self._dirty or not self._hash_cache:
            logger.debug("No hash changes to save")
            return

        try:
            self.backend.set_file_hashes(self.store_name, self._hash_cache)
            self._dirty = False
            logger.info(
                "Saved %d file hashes to store '%s'", len(self._hash_cache), self.store_name
            )
        except Exception as e:
            logger.warning("Could not save file hash cache: %s", e)

    @staticmethod
    def calculate_file_hash(file_path: Path) -> str:
        """
        Calculate SHA-256 hash of file content.

        Args:
            file_path: Path to the file

        Returns:
            Hexadecimal hash string
        """
        content = file_path.read_text(encoding="utf-8")
        return sha256(content.encode("utf-8")).hexdigest()


class Indexer:
    """
    Main indexing service that orchestrates the entire indexing pipeline.

    Handles file detection, chunking, embedding generation, and vector storage
    with support for incremental indexing and batch processing. Supports both
    native text files and documents that require conversion via markitdown.
    """

    def __init__(
        self,
        backend: VectorBackend,
        embeddings: OllamaEmbeddings | None = None,
        batch_size: int = 32,
        chunking_kwargs: dict[str, Any] | None = None,
        enable_openai: bool = False,
        openai_model: str = "gpt-4o",
    ) -> None:
        """
        Initialize the indexer.

        Args:
            backend: Vector storage backend
            embeddings: Embeddings generator (creates default if None)
            batch_size: Number of embeddings to generate in each batch
            chunking_kwargs: Additional arguments for chunking strategies
            enable_openai: Enable OpenAI for image descriptions in documents
            openai_model: OpenAI model to use for image descriptions
        """
        self.backend = backend
        self.embeddings = embeddings or OllamaEmbeddings()
        self.batch_size = batch_size
        self.chunking_kwargs = chunking_kwargs or {}
        self.enable_openai = enable_openai
        self.openai_model = openai_model

        # Document converter (initialized lazily when needed)
        self._converter: Any = None

        # Progress tracking
        self.progress = IndexingProgress()

        # File hash tracking for incremental indexing
        self.hash_trackers: dict[str, FileHashTracker] = {}

    def _get_converter(self) -> Any:
        """Get or create the document converter."""
        if self._converter is None:
            from vector_rag_tool.core.converter import (
                DocumentConverter,
                is_markitdown_available,
            )

            if not is_markitdown_available():
                raise ImportError(
                    "markitdown is not installed. Install with: "
                    "uv add 'vector-rag-tool[documents]' or uv add markitdown[all]"
                )

            self._converter = DocumentConverter(
                enable_openai=self.enable_openai,
                openai_model=self.openai_model,
            )

        return self._converter

    def index_files(
        self,
        store_name: str,
        patterns: list[str],
        incremental: bool = True,
        show_progress: bool = True,
    ) -> dict[str, Any]:
        """
        Index files matching the given patterns.

        Args:
            store_name: Name of the vector store
            patterns: Glob patterns to match files
            incremental: If True, skip unchanged files
            show_progress: Whether to show progress bars

        Returns:
            Indexing results summary
        """
        logger.info("Starting indexing for store: %s", store_name)

        # Reset progress
        self.progress = IndexingProgress()

        # Ensure store exists
        if not self.backend.store_exists(store_name):
            logger.info("Creating new store: %s", store_name)
            self.backend.create_store(store_name, dimension=self.embeddings.dimension)

        # Get hash tracker for incremental indexing
        hash_tracker = None
        if incremental:
            if store_name not in self.hash_trackers:
                self.hash_trackers[store_name] = FileHashTracker(store_name, self.backend)
            hash_tracker = self.hash_trackers[store_name]

        # Detect files
        logger.info("Detecting files from patterns: %s", patterns)
        file_matches = detect_files_from_patterns(patterns)
        self.progress.files_scanned = len(file_matches)

        if not file_matches:
            logger.warning("No files found matching patterns: %s", patterns)
            return self.progress.get_summary()

        logger.info("Found %d files to process", len(file_matches))

        # Process files with progress bar
        if show_progress:
            files_to_process = tqdm(
                file_matches,
                desc="Processing files",
                unit="file",
                disable=not show_progress,
            )
        else:
            files_to_process = file_matches  # type: ignore[assignment]

        all_chunks: list[Chunk] = []

        for file_path, file_type in files_to_process:
            try:
                path = Path(file_path)

                # Check if file should be skipped (incremental indexing)
                if hash_tracker:
                    # For binary files, use file size and mtime as hash
                    if file_requires_markitdown(file_path):
                        stat = path.stat()
                        current_hash = f"{stat.st_size}:{stat.st_mtime}"
                    else:
                        current_hash = FileHashTracker.calculate_file_hash(path)

                    stored_hash = hash_tracker.get_file_hash(file_path)

                    if current_hash == stored_hash:
                        self.progress.files_skipped += 1
                        logger.debug("Skipping unchanged file: %s", file_path)
                        continue

                    # Update hash tracker
                    hash_tracker.update_file_hash(file_path, current_hash)

                # Handle file based on type
                if file_requires_markitdown(file_path):
                    # Document file - needs conversion via markitdown
                    from vector_rag_tool.core.converter import (
                        requires_openai as file_needs_openai,
                    )

                    # Skip if OpenAI required but not enabled
                    if file_needs_openai(file_path) and not self.enable_openai:
                        self.progress.files_skipped += 1
                        logger.warning(
                            "Skipping %s: requires --enable-openai for content extraction",
                            file_path,
                        )
                        continue

                    # Convert document to markdown
                    try:
                        converter = self._get_converter()
                        markdown_content = converter.convert(file_path)

                        # Create chunks from converted markdown content
                        chunks = ChunkerFactory.chunk_text(
                            content=markdown_content,
                            source_file=path,
                            file_type="markdown",  # Converted content is markdown
                            **self.chunking_kwargs,
                        )
                    except ImportError as e:
                        logger.warning("Skipping %s: %s", file_path, e)
                        self.progress.files_skipped += 1
                        continue
                else:
                    # Native text file - read directly
                    chunks = ChunkerFactory.chunk_file(path, **self.chunking_kwargs)

                self.progress.chunks_created += len(chunks)

                # Set store name for chunks
                for chunk in chunks:
                    chunk.store_name = store_name

                all_chunks.extend(chunks)
                self.progress.files_updated += 1

                logger.debug("Chunked %s into %d chunks", file_path, len(chunks))

            except Exception as e:
                self.progress.add_error(file_path, e)

        if not all_chunks:
            logger.info("No new content to index")
            return self.progress.get_summary()

        # Generate embeddings in batches
        logger.info("Generating embeddings for %d chunks", len(all_chunks))
        embeddings_list = self._generate_embeddings_batch(
            all_chunks,
            show_progress=show_progress,
        )

        # Update chunks with embeddings
        for chunk, embedding in zip(all_chunks, embeddings_list):
            chunk.embedding = embedding

        # Store vectors in backend
        logger.info("Storing vectors in backend")
        self._store_chunks(store_name, all_chunks, show_progress=show_progress)

        # Save file hashes for incremental indexing
        if hash_tracker:
            hash_tracker.save_hashes()

        logger.info(
            "Indexing complete: %d files updated, %d chunks indexed",
            self.progress.files_updated,
            len(all_chunks),
        )

        return self.progress.get_summary()

    def _generate_embeddings_batch(
        self,
        chunks: list[Chunk],
        show_progress: bool = True,
    ) -> list[list[float]]:
        """
        Generate embeddings for chunks in batches.

        Args:
            chunks: List of chunks to embed
            show_progress: Whether to show progress bar

        Returns:
            List of embedding vectors
        """
        embeddings_list: list[list[float]] = []

        # Process in batches for efficiency
        if show_progress:
            batch_iterator = tqdm(
                range(0, len(chunks), self.batch_size),
                desc="Generating embeddings",
                unit="batch",
                total=(len(chunks) + self.batch_size - 1) // self.batch_size,
            )
        else:
            batch_iterator = range(0, len(chunks), self.batch_size)  # type: ignore[assignment]

        for i in batch_iterator:
            batch = chunks[i : i + self.batch_size]

            # Prepare texts for embedding
            texts = []
            for chunk in batch:
                title = chunk.metadata.source_file.stem
                formatted_text = format_document(chunk.content, title)
                texts.append(formatted_text)

            # Generate batch embeddings
            batch_embeddings = self.embeddings.embed_batch(texts)
            embeddings_list.extend(batch_embeddings)

            self.progress.embeddings_generated += len(batch_embeddings)

        return embeddings_list

    def _store_chunks(
        self,
        store_name: str,
        chunks: list[Chunk],
        show_progress: bool = True,
    ) -> None:
        """
        Store chunks in the vector backend.

        Args:
            store_name: Name of the vector store
            chunks: List of chunks to store
            show_progress: Whether to show progress bar
        """
        # Prepare vectors for backend
        vectors = []
        for chunk in chunks:
            vector_data = {
                "key": chunk.id,
                "embedding": chunk.embedding,
                "metadata": {
                    "source_file": str(chunk.metadata.source_file),
                    "line_start": chunk.metadata.line_start,
                    "line_end": chunk.metadata.line_end,
                    "chunk_index": chunk.metadata.chunk_index,
                    "total_chunks": chunk.metadata.total_chunks,
                    "tags": chunk.metadata.tags,
                    "word_count": chunk.metadata.word_count,
                    "char_count": chunk.metadata.char_count,
                    "content_preview": chunk.content,
                },
            }
            vectors.append(vector_data)

        # Store in batches
        if show_progress:
            batch_iterator = tqdm(
                range(0, len(vectors), self.batch_size),
                desc="Storing vectors",
                unit="batch",
                total=(len(vectors) + self.batch_size - 1) // self.batch_size,
            )
        else:
            batch_iterator = range(0, len(vectors), self.batch_size)  # type: ignore[assignment]

        total_stored = 0
        for i in batch_iterator:
            batch = vectors[i : i + self.batch_size]
            stored = self.backend.put_vectors(store_name, batch)
            total_stored += stored

        logger.info("Stored %d vectors in backend", total_stored)

    def get_indexing_stats(self, store_name: str) -> dict[str, Any]:
        """
        Get statistics about the indexed content.

        Args:
            store_name: Name of the vector store

        Returns:
            Dictionary with indexing statistics
        """
        if not self.backend.store_exists(store_name):
            return {"error": f"Store '{store_name}' does not exist"}

        info = self.backend.get_store_info(store_name)
        return {
            "store_name": store_name,
            "vector_count": info.get("vector_count", 0),
            "dimension": info.get("dimension", 0),
            "backend_type": type(self.backend).__name__,
            "last_indexed": info.get("last_updated"),
        }
