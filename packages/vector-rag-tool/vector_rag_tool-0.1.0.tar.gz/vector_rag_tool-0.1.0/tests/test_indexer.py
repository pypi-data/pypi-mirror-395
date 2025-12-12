"""
Tests for the indexing service.

This module contains comprehensive tests for the Indexer class and its
associated helper classes, mocking all external dependencies.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from vector_rag_tool.core.backend import VectorBackend
from vector_rag_tool.core.embeddings import OllamaEmbeddings
from vector_rag_tool.core.models import Chunk, ChunkMetadata
from vector_rag_tool.services.indexer import FileHashTracker, Indexer, IndexingProgress


class TestIndexingProgress:
    """Test the IndexingProgress class."""

    def test_initialization(self) -> None:
        """Test that progress tracker initializes correctly."""
        progress = IndexingProgress()
        assert progress.files_scanned == 0
        assert progress.files_updated == 0
        assert progress.files_skipped == 0
        assert progress.chunks_created == 0
        assert progress.embeddings_generated == 0
        assert progress.errors == []

    def test_add_error(self) -> None:
        """Test error tracking."""
        progress = IndexingProgress()
        error = ValueError("Test error")
        progress.add_error("test.py", error)

        assert len(progress.errors) == 1
        assert progress.errors[0] == ("test.py", error)

    def test_get_summary(self) -> None:
        """Test summary generation."""
        progress = IndexingProgress()
        progress.files_scanned = 10
        progress.files_updated = 5
        progress.files_skipped = 5
        progress.chunks_created = 20
        progress.embeddings_generated = 20
        progress.add_error("test.py", ValueError("Test error"))

        summary = progress.get_summary()
        assert summary["files_scanned"] == 10
        assert summary["files_updated"] == 5
        assert summary["files_skipped"] == 5
        assert summary["chunks_created"] == 20
        assert summary["embeddings_generated"] == 20
        assert summary["errors_count"] == 1
        assert len(summary["errors"]) == 1
        assert summary["errors"][0]["file"] == "test.py"


class TestFileHashTracker:
    """Test the FileHashTracker class."""

    def test_initialization(self) -> None:
        """Test tracker initialization."""
        backend = Mock(spec=VectorBackend)
        tracker = FileHashTracker("test_store", backend)
        assert tracker.store_name == "test_store"
        assert tracker.backend == backend
        assert not tracker._loaded

    def test_calculate_file_hash(self, tmp_path: Path) -> None:
        """Test file hash calculation."""
        # Create a test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, World!")

        # Calculate hash
        hash_value = FileHashTracker.calculate_file_hash(test_file)

        # Verify it's a valid SHA-256 hash (64 hex characters)
        assert isinstance(hash_value, str)
        assert len(hash_value) == 64
        assert all(c in "0123456789abcdef" for c in hash_value.lower())

    def test_hash_tracking(self) -> None:
        """Test hash storage and retrieval."""
        backend = Mock(spec=VectorBackend)
        backend.get_store_info.return_value = {}

        tracker = FileHashTracker("test_store", backend)

        # Initially, no hash should be returned
        assert tracker.get_file_hash("test.py") is None

        # Update hash
        tracker.update_file_hash("test.py", "hash123")
        assert tracker.get_file_hash("test.py") == "hash123"

        # Update with new hash
        tracker.update_file_hash("test.py", "hash456")
        assert tracker.get_file_hash("test.py") == "hash456"

    @patch.object(FileHashTracker, "calculate_file_hash")
    def test_ensure_loaded(self, mock_calc_hash: Mock) -> None:
        """Test that hash cache is loaded from backend."""
        backend = Mock(spec=VectorBackend)
        backend.get_file_hashes.return_value = {"test.py": "hash123", "other.py": "hash456"}

        tracker = FileHashTracker("test_store", backend)

        # Hashes should not be loaded yet
        assert not tracker._loaded

        # Access should trigger loading
        assert tracker.get_file_hash("test.py") == "hash123"
        assert tracker._loaded

        # All hashes should be loaded
        assert tracker._hash_cache == {
            "test.py": "hash123",
            "other.py": "hash456",
        }


class TestIndexer:
    """Test the Indexer class."""

    @pytest.fixture
    def mock_backend(self) -> Mock:
        """Create a mock vector backend."""
        backend = Mock(spec=VectorBackend)
        backend.store_exists.return_value = True
        backend.get_store_info.return_value = {"vector_count": 0}
        backend.put_vectors.return_value = 5
        return backend

    @pytest.fixture
    def mock_embeddings(self) -> Mock:
        """Create a mock embeddings generator."""
        embeddings = Mock(spec=OllamaEmbeddings)
        embeddings.dimension = 768
        embeddings.embed_batch.return_value = [
            [0.1] * 768,
            [0.2] * 768,
        ]
        return embeddings

    @pytest.fixture
    def indexer(self, mock_backend: Mock, mock_embeddings: Mock) -> Indexer:
        """Create an indexer instance with mocked dependencies."""
        return Indexer(
            backend=mock_backend,
            embeddings=mock_embeddings,
            batch_size=2,
        )

    @patch("vector_rag_tool.services.indexer.detect_files_from_patterns")
    @patch("vector_rag_tool.services.indexer.ChunkerFactory.chunk_file")
    def test_index_files_success(
        self,
        mock_chunk_file: Mock,
        mock_detect_files: Mock,
        indexer: Indexer,
        tmp_path: Path,
    ) -> None:
        """Test successful file indexing."""
        # Mock file detection
        mock_detect_files.return_value = [
            (str(tmp_path / "test1.py"), "python"),
            (str(tmp_path / "test2.py"), "python"),
        ]

        # Mock chunking
        chunk1 = Chunk(
            id="chunk1",
            content="print('hello')",
            metadata=ChunkMetadata(
                source_file=tmp_path / "test1.py",
                line_start=1,
                line_end=1,
                chunk_index=0,
                total_chunks=1,
            ),
        )
        chunk2 = Chunk(
            id="chunk2",
            content="print('world')",
            metadata=ChunkMetadata(
                source_file=tmp_path / "test2.py",
                line_start=1,
                line_end=1,
                chunk_index=0,
                total_chunks=1,
            ),
        )
        mock_chunk_file.side_effect = [[chunk1], [chunk2]]

        # Run indexing
        results = indexer.index_files(
            store_name="test_store",
            patterns=["*.py"],
            incremental=False,
            show_progress=False,
        )

        # Verify results
        assert results["files_scanned"] == 2
        assert results["files_updated"] == 2
        assert results["files_skipped"] == 0
        assert results["chunks_created"] == 2
        assert results["embeddings_generated"] == 2
        assert results["errors_count"] == 0

        # Verify backend interactions
        indexer.backend.store_exists.assert_called_once_with("test_store")
        indexer.backend.put_vectors.assert_called_once()

        # Verify embeddings were generated
        assert indexer.embeddings.embed_batch.call_count == 1

    @patch("vector_rag_tool.services.indexer.detect_files_from_patterns")
    def test_index_files_no_files_found(
        self,
        mock_detect_files: Mock,
        indexer: Indexer,
    ) -> None:
        """Test indexing when no files are found."""
        # Mock no files found
        mock_detect_files.return_value = []

        # Run indexing
        results = indexer.index_files(
            store_name="test_store",
            patterns=["*.nonexistent"],
            incremental=False,
            show_progress=False,
        )

        # Verify results
        assert results["files_scanned"] == 0
        assert results["files_updated"] == 0
        assert results["files_skipped"] == 0
        assert results["chunks_created"] == 0
        assert results["embeddings_generated"] == 0
        assert results["errors_count"] == 0

    @patch("vector_rag_tool.services.indexer.detect_files_from_patterns")
    def test_index_files_create_store_if_not_exists(
        self,
        mock_detect_files: Mock,
        indexer: Indexer,
    ) -> None:
        """Test that store is created if it doesn't exist."""
        # Mock store doesn't exist
        indexer.backend.store_exists.return_value = False

        # Mock no files found (just testing store creation)
        mock_detect_files.return_value = []

        # Run indexing
        indexer.index_files(
            store_name="new_store",
            patterns=["*.py"],
            incremental=False,
            show_progress=False,
        )

        # Verify store was created
        indexer.backend.create_store.assert_called_once_with(
            "new_store", dimension=indexer.embeddings.dimension
        )

    @patch("vector_rag_tool.services.indexer.detect_files_from_patterns")
    @patch("vector_rag_tool.services.indexer.ChunkerFactory.chunk_file")
    @patch("vector_rag_tool.services.indexer.FileHashTracker")
    def test_incremental_indexing(
        self,
        mock_tracker_class: Mock,
        mock_chunk_file: Mock,
        mock_detect_files: Mock,
        indexer: Indexer,
        tmp_path: Path,
    ) -> None:
        """Test incremental indexing with file hash tracking."""
        # Mock file detection
        mock_detect_files.return_value = [
            (str(tmp_path / "test.py"), "python"),
        ]

        # Mock hash tracker
        mock_tracker = Mock(spec=FileHashTracker)
        mock_tracker.get_file_hash.return_value = None
        mock_tracker_class.return_value = mock_tracker

        # Mock chunking
        chunk = Chunk(
            id="chunk1",
            content="print('hello')",
            metadata=ChunkMetadata(
                source_file=tmp_path / "test.py",
                line_start=1,
                line_end=1,
                chunk_index=0,
                total_chunks=1,
            ),
        )
        mock_chunk_file.return_value = [chunk]

        # Run incremental indexing
        indexer.index_files(
            store_name="test_store",
            patterns=["*.py"],
            incremental=True,
            show_progress=False,
        )

        # Verify hash tracker was used
        mock_tracker_class.assert_called_once_with("test_store", indexer.backend)
        mock_tracker.update_file_hash.assert_called_once()

    @patch("vector_rag_tool.services.indexer.detect_files_from_patterns")
    @patch("vector_rag_tool.services.indexer.ChunkerFactory.chunk_file")
    def test_index_files_with_error(
        self,
        mock_chunk_file: Mock,
        mock_detect_files: Mock,
        indexer: Indexer,
        tmp_path: Path,
    ) -> None:
        """Test error handling during indexing."""
        # Mock file detection
        mock_detect_files.return_value = [
            (str(tmp_path / "test.py"), "python"),
        ]

        # Mock chunking error
        mock_chunk_file.side_effect = Exception("Chunking failed")

        # Run indexing
        results = indexer.index_files(
            store_name="test_store",
            patterns=["*.py"],
            incremental=False,
            show_progress=False,
        )

        # Verify error was recorded
        assert results["files_scanned"] == 1
        assert results["files_updated"] == 0
        assert results["errors_count"] == 1
        assert "Chunking failed" in results["errors"][0]["error"]

    def test_generate_embeddings_batch(self, indexer: Indexer) -> None:
        """Test batch embedding generation."""
        # Create test chunks
        chunks = [
            Chunk(
                id="chunk1",
                content="content1",
                metadata=ChunkMetadata(
                    source_file=Path("test1.py"),
                    line_start=1,
                    line_end=1,
                    chunk_index=0,
                    total_chunks=1,
                ),
            ),
            Chunk(
                id="chunk2",
                content="content2",
                metadata=ChunkMetadata(
                    source_file=Path("test2.py"),
                    line_start=1,
                    line_end=1,
                    chunk_index=0,
                    total_chunks=1,
                ),
            ),
        ]

        # Generate embeddings
        embeddings = indexer._generate_embeddings_batch(
            chunks,
            show_progress=False,
        )

        # Verify results
        assert len(embeddings) == 2
        assert all(len(e) == 768 for e in embeddings)

        # Verify batch embedding was called
        indexer.embeddings.embed_batch.assert_called_once()
        call_args = indexer.embeddings.embed_batch.call_args[0][0]
        assert len(call_args) == 2
        assert all("title:" in text and "text:" in text for text in call_args)

    def test_store_chunks(self, indexer: Indexer) -> None:
        """Test storing chunks in backend."""
        # Create test chunks with embeddings
        chunks = [
            Chunk(
                id="chunk1",
                content="content1",
                embedding=[0.1] * 768,
                metadata=ChunkMetadata(
                    source_file=Path("test1.py"),
                    line_start=1,
                    line_end=1,
                    chunk_index=0,
                    total_chunks=1,
                    word_count=1,
                    char_count=7,
                ),
            ),
        ]

        # Store chunks
        indexer._store_chunks(
            "test_store",
            chunks,
            show_progress=False,
        )

        # Verify backend was called
        indexer.backend.put_vectors.assert_called_once()
        call_args = indexer.backend.put_vectors.call_args[0]
        assert call_args[0] == "test_store"
        assert len(call_args[1]) == 1

        # Verify vector format
        vector = call_args[1][0]
        assert vector["key"] == "chunk1"
        assert vector["embedding"] == [0.1] * 768
        assert "metadata" in vector
        assert vector["metadata"]["source_file"] == "test1.py"

    def test_get_indexing_stats(self, indexer: Indexer) -> None:
        """Test getting indexing statistics."""
        # Mock store info
        indexer.backend.get_store_info.return_value = {
            "vector_count": 100,
            "dimension": 768,
            "last_updated": "2024-01-01",
        }

        # Get stats
        stats = indexer.get_indexing_stats("test_store")

        # Verify stats
        assert stats["store_name"] == "test_store"
        assert stats["vector_count"] == 100
        assert stats["dimension"] == 768
        assert stats["backend_type"] == "Mock"
        assert stats["last_indexed"] == "2024-01-01"

    def test_get_indexing_stats_store_not_exists(self, indexer: Indexer) -> None:
        """Test getting stats for non-existent store."""
        # Mock store doesn't exist
        indexer.backend.store_exists.return_value = False

        # Get stats
        stats = indexer.get_indexing_stats("nonexistent")

        # Verify error
        assert "error" in stats
        assert "does not exist" in stats["error"]
