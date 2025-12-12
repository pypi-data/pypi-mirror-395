"""
Core data models for vector-rag-tool.

This module defines the main data structures used throughout the application
for managing Obsidian vault content and RAG operations.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class StoreType(str, Enum):
    """Type of store for RAG operations."""

    OBISIDIAN = "obsidian"
    FILESYSTEM = "filesystem"
    CUSTOM = "custom"


class SimilarityLevel(str, Enum):
    """Human-readable similarity level interpretation for cosine similarity scores."""

    DUPLICATE = "duplicate"
    VERY_SIMILAR = "very_similar"
    RELATED = "related"
    UNRELATED = "unrelated"
    CONTRADICTION = "contradiction"

    @classmethod
    def from_score(cls, score: float) -> "SimilarityLevel":
        """
        Convert cosine similarity score to human-readable level.

        Args:
            score: Cosine similarity score (-1 to 1)

        Returns:
            SimilarityLevel enum value

        Score Mapping:
            >= 0.85: DUPLICATE (near-duplicate or exact match)
            >= 0.60: VERY_SIMILAR (paraphrases, close variants)
            >= 0.30: RELATED (semantically related topics)
            >= 0.00: UNRELATED (perpendicular, no clear relation)
            <  0.00: CONTRADICTION (antonyms, opposing concepts)
        """
        if score >= 0.85:
            return cls.DUPLICATE
        elif score >= 0.60:
            return cls.VERY_SIMILAR
        elif score >= 0.30:
            return cls.RELATED
        elif score >= 0.00:
            return cls.UNRELATED
        else:
            return cls.CONTRADICTION

    def description(self) -> str:
        """Get human-readable description of similarity level."""
        descriptions = {
            SimilarityLevel.DUPLICATE: "Near-duplicate or exact match",
            SimilarityLevel.VERY_SIMILAR: "Very similar (paraphrases, close variants)",
            SimilarityLevel.RELATED: "Semantically related topics",
            SimilarityLevel.UNRELATED: "Unrelated content",
            SimilarityLevel.CONTRADICTION: "Contradictory or opposing concepts",
        }
        return descriptions[self]


@dataclass
class Store:
    """
    Represents a storage configuration for RAG operations.

    A store defines how content is organized and accessed, supporting
    multiple backends including Obsidian vaults and filesystem directories.
    """

    name: str
    type: StoreType
    path: Path
    description: str | None = None
    metadata: dict[str, Any] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        """Initialize default values after dataclass creation."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.metadata is None:
            self.metadata = {}


@dataclass
class ChunkMetadata:
    """
    Metadata associated with a content chunk.

    Contains information about the source, structure, and context
    of the chunked content for enhanced retrieval and processing.
    """

    source_file: Path
    line_start: int
    line_end: int
    chunk_index: int
    total_chunks: int
    tags: list[str] | None = None
    links: list[str] | None = None
    frontmatter: dict[str, Any] | None = None
    word_count: int | None = None
    char_count: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        """Initialize default values after dataclass creation."""
        if self.tags is None:
            self.tags = []
        if self.links is None:
            self.links = []
        if self.frontmatter is None:
            self.frontmatter = {}
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

        # Calculate counts if not provided
        if self.word_count is None or self.char_count is None:
            # These will be calculated when the chunk content is available
            pass


@dataclass
class Chunk:
    """
    A chunk of content extracted from a source file.

    Represents a piece of text that has been extracted from a larger
    document, complete with metadata for context and retrieval.
    """

    id: str
    content: str
    metadata: ChunkMetadata
    embedding: list[float] | None = None
    store_name: str | None = None

    def __post_init__(self) -> None:
        """Calculate content statistics after dataclass creation."""
        if self.metadata.word_count is None:
            self.metadata.word_count = len(self.content.split())
        if self.metadata.char_count is None:
            self.metadata.char_count = len(self.content)


@dataclass
class QueryResult:
    """
    Result of a RAG query operation.

    Contains the matched chunks along with relevance scores and
    query metadata for result processing and display.
    """

    query: str
    chunks: list[Chunk]
    scores: list[float]
    store_name: str
    total_results: int
    query_time: float | None = None
    metadata: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        """Validate and initialize result data."""
        if len(self.chunks) != len(self.scores):
            raise ValueError("Number of chunks must match number of scores")
        if self.metadata is None:
            self.metadata = {}

    @property
    def top_result(self) -> Chunk | None:
        """Get the highest scoring chunk if available."""
        if not self.chunks or not self.scores:
            return None

        max_index = max(range(len(self.scores)), key=lambda i: self.scores[i])
        return self.chunks[max_index]

    def get_sorted_chunks(self) -> list[tuple[Chunk, float]]:
        """Get chunks sorted by relevance score (highest first)."""
        return sorted(zip(self.chunks, self.scores), key=lambda pair: pair[1], reverse=True)

    def filter_by_score(self, min_score: float) -> "QueryResult":
        """Create a new QueryResult with only chunks above the minimum score."""
        filtered_pairs = [
            (chunk, score) for chunk, score in zip(self.chunks, self.scores) if score >= min_score
        ]

        if not filtered_pairs:
            return QueryResult(
                query=self.query,
                chunks=[],
                scores=[],
                store_name=self.store_name,
                total_results=0,
                query_time=self.query_time,
                metadata=self.metadata,
            )

        filtered_chunks, filtered_scores = zip(*filtered_pairs)
        return QueryResult(
            query=self.query,
            chunks=list(filtered_chunks),
            scores=list(filtered_scores),
            store_name=self.store_name,
            total_results=len(filtered_chunks),
            query_time=self.query_time,
            metadata=self.metadata,
        )
