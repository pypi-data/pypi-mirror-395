"""
Abstract base class for vector storage backends.

This module defines the VectorBackend interface that all storage backends
must implement, providing a consistent API for both local (FAISS) and
remote (S3 Vectors) storage solutions.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class VectorQueryResult:
    """Result from vector similarity search."""

    key: str
    score: float
    metadata: dict[str, Any]
    content: str | None = None


class VectorBackend(ABC):
    """Abstract base class for vector storage backends."""

    @abstractmethod
    def create_store(self, store_name: str, dimension: int = 768) -> None:
        """Create a new vector store."""
        pass

    @abstractmethod
    def delete_store(self, store_name: str) -> None:
        """Delete a vector store."""
        pass

    @abstractmethod
    def list_stores(self) -> list[str]:
        """List all available stores."""
        pass

    @abstractmethod
    def store_exists(self, store_name: str) -> bool:
        """Check if store exists."""
        pass

    @abstractmethod
    def put_vectors(
        self,
        store_name: str,
        vectors: list[dict[str, Any]],  # [{'key': str, 'embedding': list, 'metadata': dict}]
    ) -> int:
        """Insert vectors into store. Returns count inserted."""
        pass

    @abstractmethod
    def delete_vectors(self, store_name: str, keys: list[str]) -> int:
        """Delete vectors by keys. Returns count deleted."""
        pass

    @abstractmethod
    def query(
        self,
        store_name: str,
        query_vector: list[float],
        top_k: int = 5,
    ) -> list[VectorQueryResult]:
        """Query for similar vectors."""
        pass

    @abstractmethod
    def get_store_info(self, store_name: str) -> dict[str, Any]:
        """Get store metadata (vector count, dimension, etc.)."""
        pass

    def get_file_hashes(self, store_name: str) -> dict[str, str]:
        """Get stored file hashes for incremental indexing.

        Args:
            store_name: Name of the vector store

        Returns:
            Dictionary mapping file paths to their hashes
        """
        return {}

    def set_file_hashes(self, store_name: str, hashes: dict[str, str]) -> None:
        """Save file hashes for incremental indexing.

        Args:
            store_name: Name of the vector store
            hashes: Dictionary mapping file paths to their hashes
        """
        pass
