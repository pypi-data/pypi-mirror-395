"""
Tests for core data models.

This module contains comprehensive tests for all data models defined in
vector_rag_tool.core.models, ensuring proper initialization, validation,
and functionality.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from datetime import datetime
from pathlib import Path

import pytest

from vector_rag_tool.core.models import (
    Chunk,
    ChunkMetadata,
    QueryResult,
    SimilarityLevel,
    Store,
    StoreType,
)


class TestStoreType:
    """Test the StoreType enum."""

    def test_store_type_values(self) -> None:
        """Test that StoreType has expected values."""
        assert StoreType.OBISIDIAN == "obsidian"
        assert StoreType.FILESYSTEM == "filesystem"
        assert StoreType.CUSTOM == "custom"

    def test_store_type_is_str_enum(self) -> None:
        """Test that StoreType behaves like a string."""
        assert StoreType.OBISIDIAN.value == "obsidian"
        assert isinstance(StoreType.OBISIDIAN, str)
        # Test that it can be compared to strings directly
        assert StoreType.OBISIDIAN == "obsidian"


class TestSimilarityLevel:
    """Test the SimilarityLevel enum."""

    def test_similarity_level_values(self) -> None:
        """Test that SimilarityLevel has expected values."""
        assert SimilarityLevel.DUPLICATE == "duplicate"
        assert SimilarityLevel.VERY_SIMILAR == "very_similar"
        assert SimilarityLevel.RELATED == "related"
        assert SimilarityLevel.UNRELATED == "unrelated"
        assert SimilarityLevel.CONTRADICTION == "contradiction"

    def test_from_score_duplicate(self) -> None:
        """Test score classification for duplicate range (>=0.85)."""
        assert SimilarityLevel.from_score(1.0) == SimilarityLevel.DUPLICATE
        assert SimilarityLevel.from_score(0.95) == SimilarityLevel.DUPLICATE
        assert SimilarityLevel.from_score(0.85) == SimilarityLevel.DUPLICATE

    def test_from_score_very_similar(self) -> None:
        """Test score classification for very_similar range (0.60-0.84)."""
        assert SimilarityLevel.from_score(0.84) == SimilarityLevel.VERY_SIMILAR
        assert SimilarityLevel.from_score(0.75) == SimilarityLevel.VERY_SIMILAR
        assert SimilarityLevel.from_score(0.60) == SimilarityLevel.VERY_SIMILAR

    def test_from_score_related(self) -> None:
        """Test score classification for related range (0.30-0.59)."""
        assert SimilarityLevel.from_score(0.59) == SimilarityLevel.RELATED
        assert SimilarityLevel.from_score(0.50) == SimilarityLevel.RELATED
        assert SimilarityLevel.from_score(0.30) == SimilarityLevel.RELATED

    def test_from_score_unrelated(self) -> None:
        """Test score classification for unrelated range (0.00-0.29)."""
        assert SimilarityLevel.from_score(0.29) == SimilarityLevel.UNRELATED
        assert SimilarityLevel.from_score(0.15) == SimilarityLevel.UNRELATED
        assert SimilarityLevel.from_score(0.00) == SimilarityLevel.UNRELATED

    def test_from_score_contradiction(self) -> None:
        """Test score classification for contradiction range (<0.0)."""
        assert SimilarityLevel.from_score(-0.01) == SimilarityLevel.CONTRADICTION
        assert SimilarityLevel.from_score(-0.50) == SimilarityLevel.CONTRADICTION
        assert SimilarityLevel.from_score(-1.0) == SimilarityLevel.CONTRADICTION

    def test_description(self) -> None:
        """Test human-readable descriptions."""
        assert SimilarityLevel.DUPLICATE.description() == "Near-duplicate or exact match"
        assert (
            SimilarityLevel.VERY_SIMILAR.description()
            == "Very similar (paraphrases, close variants)"
        )
        assert SimilarityLevel.RELATED.description() == "Semantically related topics"
        assert SimilarityLevel.UNRELATED.description() == "Unrelated content"
        assert SimilarityLevel.CONTRADICTION.description() == "Contradictory or opposing concepts"


class TestStore:
    """Test the Store dataclass."""

    def test_store_minimal_creation(self) -> None:
        """Test creating a store with minimal required fields."""
        store = Store(name="test-store", type=StoreType.FILESYSTEM, path=Path("/test/path"))

        assert store.name == "test-store"
        assert store.type == StoreType.FILESYSTEM
        assert store.path == Path("/test/path")
        assert store.description is None
        assert store.metadata == {}
        assert isinstance(store.created_at, datetime)
        assert isinstance(store.updated_at, datetime)

    def test_store_full_creation(self) -> None:
        """Test creating a store with all fields."""
        created_time = datetime.now()
        store = Store(
            name="full-store",
            type=StoreType.OBISIDIAN,
            path=Path("/vault/path"),
            description="A test store",
            metadata={"key": "value"},
            created_at=created_time,
            updated_at=created_time,
        )

        assert store.name == "full-store"
        assert store.type == StoreType.OBISIDIAN
        assert store.path == Path("/vault/path")
        assert store.description == "A test store"
        assert store.metadata == {"key": "value"}
        assert store.created_at == created_time
        assert store.updated_at == created_time


class TestChunkMetadata:
    """Test the ChunkMetadata dataclass."""

    def test_chunk_metadata_minimal_creation(self) -> None:
        """Test creating chunk metadata with minimal required fields."""
        metadata = ChunkMetadata(
            source_file=Path("test.md"), line_start=1, line_end=10, chunk_index=0, total_chunks=5
        )

        assert metadata.source_file == Path("test.md")
        assert metadata.line_start == 1
        assert metadata.line_end == 10
        assert metadata.chunk_index == 0
        assert metadata.total_chunks == 5
        assert metadata.tags == []
        assert metadata.links == []
        assert metadata.frontmatter == {}
        assert metadata.word_count is None
        assert metadata.char_count is None
        assert isinstance(metadata.created_at, datetime)
        assert isinstance(metadata.updated_at, datetime)

    def test_chunk_metadata_full_creation(self) -> None:
        """Test creating chunk metadata with all fields."""
        created_time = datetime.now()
        metadata = ChunkMetadata(
            source_file=Path("full.md"),
            line_start=5,
            line_end=15,
            chunk_index=2,
            total_chunks=10,
            tags=["tag1", "tag2"],
            links=["[[note1]]", "[[note2]]"],
            frontmatter={"title": "Test Note"},
            word_count=100,
            char_count=500,
            created_at=created_time,
            updated_at=created_time,
        )

        assert metadata.source_file == Path("full.md")
        assert metadata.line_start == 5
        assert metadata.line_end == 15
        assert metadata.chunk_index == 2
        assert metadata.total_chunks == 10
        assert metadata.tags == ["tag1", "tag2"]
        assert metadata.links == ["[[note1]]", "[[note2]]"]
        assert metadata.frontmatter == {"title": "Test Note"}
        assert metadata.word_count == 100
        assert metadata.char_count == 500
        assert metadata.created_at == created_time
        assert metadata.updated_at == created_time


class TestChunk:
    """Test the Chunk dataclass."""

    def test_chunk_creation_without_counts(self) -> None:
        """Test creating a chunk where word/char counts are calculated."""
        content = "This is a test chunk with some content."
        metadata = ChunkMetadata(
            source_file=Path("test.md"), line_start=1, line_end=2, chunk_index=0, total_chunks=1
        )

        chunk = Chunk(id="test-chunk-1", content=content, metadata=metadata)

        assert chunk.id == "test-chunk-1"
        assert chunk.content == content
        assert chunk.metadata == metadata
        assert chunk.embedding is None
        assert chunk.store_name is None
        assert chunk.metadata.word_count == len(content.split())
        assert chunk.metadata.char_count == len(content)

    def test_chunk_creation_with_counts(self) -> None:
        """Test creating a chunk with pre-calculated counts."""
        content = "Test content"
        metadata = ChunkMetadata(
            source_file=Path("test.md"),
            line_start=1,
            line_end=2,
            chunk_index=0,
            total_chunks=1,
            word_count=2,
            char_count=12,
        )

        chunk = Chunk(
            id="test-chunk-2",
            content=content,
            metadata=metadata,
            embedding=[0.1, 0.2, 0.3],
            store_name="test-store",
        )

        assert chunk.id == "test-chunk-2"
        assert chunk.content == content
        assert chunk.metadata.word_count == 2
        assert chunk.metadata.char_count == 12
        assert chunk.embedding == [0.1, 0.2, 0.3]
        assert chunk.store_name == "test-store"


class TestQueryResult:
    """Test the QueryResult dataclass."""

    def test_query_result_creation(self) -> None:
        """Test creating a query result."""
        chunk1 = self._create_test_chunk("chunk-1", "Content 1", 0.9)
        chunk2 = self._create_test_chunk("chunk-2", "Content 2", 0.7)

        result = QueryResult(
            query="test query",
            chunks=[chunk1, chunk2],
            scores=[0.9, 0.7],
            store_name="test-store",
            total_results=2,
            query_time=0.1,
        )

        assert result.query == "test query"
        assert len(result.chunks) == 2
        assert result.scores == [0.9, 0.7]
        assert result.store_name == "test-store"
        assert result.total_results == 2
        assert result.query_time == 0.1
        assert result.metadata == {}

    def test_query_result_mismatched_lengths(self) -> None:
        """Test that mismatched chunks and scores raises an error."""
        chunk1 = self._create_test_chunk("chunk-1", "Content 1")
        chunk2 = self._create_test_chunk("chunk-2", "Content 2")

        with pytest.raises(ValueError, match="Number of chunks must match number of scores"):
            QueryResult(
                query="test",
                chunks=[chunk1, chunk2],
                scores=[0.9],  # Only one score for two chunks
                store_name="test",
                total_results=2,
            )

    def test_top_result(self) -> None:
        """Test getting the top result."""
        chunk1 = self._create_test_chunk("chunk-1", "Content 1")
        chunk2 = self._create_test_chunk("chunk-2", "Content 2")
        chunk3 = self._create_test_chunk("chunk-3", "Content 3")

        result = QueryResult(
            query="test",
            chunks=[chunk1, chunk2, chunk3],
            scores=[0.7, 0.9, 0.5],
            store_name="test",
            total_results=3,
        )

        top_chunk = result.top_result
        assert top_chunk is not None
        assert top_chunk.id == "chunk-2"  # Highest score (0.9)

    def test_top_result_empty(self) -> None:
        """Test getting top result from empty query."""
        result = QueryResult(query="test", chunks=[], scores=[], store_name="test", total_results=0)

        assert result.top_result is None

    def test_get_sorted_chunks(self) -> None:
        """Test getting chunks sorted by score."""
        chunk1 = self._create_test_chunk("chunk-1", "Content 1")
        chunk2 = self._create_test_chunk("chunk-2", "Content 2")
        chunk3 = self._create_test_chunk("chunk-3", "Content 3")

        result = QueryResult(
            query="test",
            chunks=[chunk1, chunk2, chunk3],
            scores=[0.7, 0.9, 0.5],
            store_name="test",
            total_results=3,
        )

        sorted_pairs = result.get_sorted_chunks()
        assert len(sorted_pairs) == 3
        assert sorted_pairs[0][0].id == "chunk-2"  # Highest score
        assert sorted_pairs[0][1] == 0.9
        assert sorted_pairs[1][0].id == "chunk-1"  # Middle score
        assert sorted_pairs[1][1] == 0.7
        assert sorted_pairs[2][0].id == "chunk-3"  # Lowest score
        assert sorted_pairs[2][1] == 0.5

    def test_filter_by_score(self) -> None:
        """Test filtering chunks by minimum score."""
        chunk1 = self._create_test_chunk("chunk-1", "Content 1")
        chunk2 = self._create_test_chunk("chunk-2", "Content 2")
        chunk3 = self._create_test_chunk("chunk-3", "Content 3")

        result = QueryResult(
            query="test",
            chunks=[chunk1, chunk2, chunk3],
            scores=[0.9, 0.7, 0.5],
            store_name="test",
            total_results=3,
            query_time=0.1,
        )

        # Filter with min_score=0.6
        filtered = result.filter_by_score(0.6)
        assert len(filtered.chunks) == 2
        assert filtered.scores == [0.9, 0.7]
        assert filtered.total_results == 2
        assert filtered.query_time == 0.1
        assert filtered.store_name == "test"

        # Filter with min_score=0.8
        filtered_high = result.filter_by_score(0.8)
        assert len(filtered_high.chunks) == 1
        assert filtered_high.scores == [0.9]
        assert filtered_high.total_results == 1

        # Filter with min_score=0.95 (no results)
        filtered_none = result.filter_by_score(0.95)
        assert len(filtered_none.chunks) == 0
        assert filtered_none.scores == []
        assert filtered_none.total_results == 0

    def _create_test_chunk(self, chunk_id: str, content: str, score: float = 0.0) -> Chunk:
        """Helper method to create a test chunk."""
        metadata = ChunkMetadata(
            source_file=Path("test.md"), line_start=1, line_end=2, chunk_index=0, total_chunks=1
        )

        return Chunk(id=chunk_id, content=content, metadata=metadata)
