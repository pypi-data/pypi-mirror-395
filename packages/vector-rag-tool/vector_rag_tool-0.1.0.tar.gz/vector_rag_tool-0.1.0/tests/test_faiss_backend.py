"""
Tests for FAISS backend implementation.

This module contains comprehensive tests for the FAISS vector storage backend,
ensuring proper functionality for all vector operations including store
management, vector insertion/deletion, and similarity search.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import json
from pathlib import Path

import numpy as np
import pytest

from vector_rag_tool.core.backend import VectorQueryResult
from vector_rag_tool.core.faiss_backend import FAISSBackend


@pytest.fixture
def temp_stores_dir(tmp_path: Path) -> Path:
    """Create a temporary stores directory for testing."""
    stores_dir = tmp_path / ".config" / "vector-rag-tool" / "stores"
    stores_dir.mkdir(parents=True)
    return stores_dir


@pytest.fixture
def backend(temp_stores_dir: Path) -> FAISSBackend:
    """Create a FAISS backend instance with temporary directory."""
    # Patch the STORES_DIR in the backend module
    import vector_rag_tool.core.faiss_backend as faiss_module

    original_stores_dir = faiss_module.STORES_DIR
    faiss_module.STORES_DIR = temp_stores_dir

    backend = FAISSBackend()

    # Restore original after test
    yield backend

    faiss_module.STORES_DIR = original_stores_dir


@pytest.fixture
def sample_vectors() -> list[dict]:
    """Create sample vectors for testing."""
    # Generate normalized vectors (already unit vectors)
    vectors = []
    for i in range(10):
        # Create a random vector and normalize it
        vec = np.random.randn(384).astype(np.float32)
        vec = vec / np.linalg.norm(vec)

        vectors.append(
            {
                "key": f"doc_{i}",
                "embedding": vec.tolist(),
                "metadata": {
                    "title": f"Document {i}",
                    "content": f"This is the content of document {i}",
                    "category": "test",
                },
            }
        )
    return vectors


@pytest.fixture
def query_vector() -> list[float]:
    """Create a sample query vector."""
    # Create a normalized query vector
    vec = np.random.randn(384).astype(np.float32)
    vec = vec / np.linalg.norm(vec)
    return vec.tolist()


class TestFAISSBackendInit:
    """Test FAISS backend initialization."""

    def test_init_creates_stores_dir(self, temp_stores_dir: Path) -> None:
        """Test that backend initialization creates the stores directory."""
        import vector_rag_tool.core.faiss_backend as faiss_module

        original_stores_dir = faiss_module.STORES_DIR
        faiss_module.STORES_DIR = temp_stores_dir / "new"

        FAISSBackend()  # Just initialize to create the directory
        assert faiss_module.STORES_DIR.exists()

        faiss_module.STORES_DIR = original_stores_dir


class TestStoreManagement:
    """Test store management operations."""

    def test_create_store(self, backend: FAISSBackend) -> None:
        """Test creating a new store."""
        backend.create_store("test-store", dimension=384)

        assert backend.store_exists("test-store")
        assert "test-store" in backend.list_stores()

        # Check files are created
        index_path = backend._index_path("test-store")
        meta_path = backend._meta_path("test-store")
        assert index_path.exists()
        assert meta_path.exists()

        # Check metadata content
        metadata = json.loads(meta_path.read_text())
        assert metadata["dimension"] == 384
        assert metadata["vectors"] == {}
        assert metadata["next_id"] == 0

    def test_create_store_already_exists(self, backend: FAISSBackend) -> None:
        """Test creating a store that already exists raises an error."""
        backend.create_store("test-store")

        with pytest.raises(ValueError, match="Store 'test-store' already exists"):
            backend.create_store("test-store")

    def test_delete_store(self, backend: FAISSBackend) -> None:
        """Test deleting a store."""
        backend.create_store("test-store")
        assert backend.store_exists("test-store")

        backend.delete_store("test-store")
        assert not backend.store_exists("test-store")
        assert "test-store" not in backend.list_stores()

    def test_delete_nonexistent_store(self, backend: FAISSBackend) -> None:
        """Test deleting a non-existent store doesn't raise an error."""
        # Should not raise an error
        backend.delete_store("nonexistent-store")

    def test_list_stores_empty(self, backend: FAISSBackend) -> None:
        """Test listing stores when none exist."""
        stores = backend.list_stores()
        assert stores == []

    def test_list_stores_multiple(self, backend: FAISSBackend) -> None:
        """Test listing multiple stores."""
        backend.create_store("store1")
        backend.create_store("store2")
        backend.create_store("store3")

        stores = sorted(backend.list_stores())
        assert stores == ["store1", "store2", "store3"]

    def test_store_exists(self, backend: FAISSBackend) -> None:
        """Test checking if a store exists."""
        assert not backend.store_exists("test-store")

        backend.create_store("test-store")
        assert backend.store_exists("test-store")


class TestVectorOperations:
    """Test vector storage and retrieval operations."""

    def test_put_vectors_empty(self, backend: FAISSBackend) -> None:
        """Test putting an empty list of vectors."""
        backend.create_store("test-store")
        count = backend.put_vectors("test-store", [])
        assert count == 0

    def test_put_vectors(self, backend: FAISSBackend, sample_vectors: list[dict]) -> None:
        """Test putting vectors into a store."""
        backend.create_store("test-store", dimension=384)

        count = backend.put_vectors("test-store", sample_vectors[:5])
        assert count == 5

        # Check metadata is updated
        metadata = backend._load_metadata("test-store")
        assert len(metadata["vectors"]) == 5
        assert metadata["next_id"] == 5

        # Check specific vectors
        for i, vector in enumerate(sample_vectors[:5]):
            key = vector["key"]
            assert key in metadata["vectors"]
            assert metadata["vectors"][key]["index_id"] == i
            assert metadata["vectors"][key]["metadata"]["title"] == vector["metadata"]["title"]

    def test_put_vectors_wrong_dimension(
        self, backend: FAISSBackend, sample_vectors: list[dict]
    ) -> None:
        """Test putting vectors with wrong dimension raises an error."""
        backend.create_store("test-store", dimension=256)  # Different dimension

        with pytest.raises(
            ValueError,
            match="Vector dimension 384 does not match store dimension 256",
        ):
            backend.put_vectors("test-store", sample_vectors)

    def test_put_vectors_to_nonexistent_store(
        self, backend: FAISSBackend, sample_vectors: list[dict]
    ) -> None:
        """Test putting vectors to a non-existent store raises an error."""
        with pytest.raises(ValueError, match="Store 'test-store' does not exist"):
            backend.put_vectors("test-store", sample_vectors)

    def test_put_vectors_multiple_batches(
        self, backend: FAISSBackend, sample_vectors: list[dict]
    ) -> None:
        """Test putting vectors in multiple batches."""
        backend.create_store("test-store", dimension=384)

        # First batch
        count1 = backend.put_vectors("test-store", sample_vectors[:3])
        assert count1 == 3

        # Second batch
        count2 = backend.put_vectors("test-store", sample_vectors[3:7])
        assert count2 == 4

        # Check all vectors are stored
        metadata = backend._load_metadata("test-store")
        assert len(metadata["vectors"]) == 7
        assert metadata["next_id"] == 7

    def test_delete_vectors(self, backend: FAISSBackend, sample_vectors: list[dict]) -> None:
        """Test deleting vectors from metadata."""
        backend.create_store("test-store", dimension=384)
        backend.put_vectors("test-store", sample_vectors)

        # Delete some vectors
        deleted = backend.delete_vectors("test-store", ["doc_0", "doc_2", "doc_4"])
        assert deleted == 3

        # Check metadata is updated
        metadata = backend._load_metadata("test-store")
        assert len(metadata["vectors"]) == 7
        assert "doc_0" not in metadata["vectors"]
        assert "doc_1" in metadata["vectors"]
        assert "doc_2" not in metadata["vectors"]
        assert "doc_3" in metadata["vectors"]

    def test_delete_nonexistent_vectors(
        self, backend: FAISSBackend, sample_vectors: list[dict]
    ) -> None:
        """Test deleting vectors that don't exist."""
        backend.create_store("test-store", dimension=384)
        backend.put_vectors("test-store", sample_vectors)

        deleted = backend.delete_vectors("test-store", ["nonexistent_1", "nonexistent_2"])
        assert deleted == 0

    def test_query(
        self, backend: FAISSBackend, sample_vectors: list[dict], query_vector: list[float]
    ) -> None:
        """Test querying for similar vectors."""
        backend.create_store("test-store", dimension=384)
        backend.put_vectors("test-store", sample_vectors)

        results = backend.query("test-store", query_vector, top_k=3)

        assert len(results) <= 3
        assert all(isinstance(r, VectorQueryResult) for r in results)

        # Check results are sorted by score (descending)
        if len(results) > 1:
            scores = [r.score for r in results]
            assert scores == sorted(scores, reverse=True)

        # Check result structure
        for result in results:
            assert isinstance(result.key, str)
            assert isinstance(result.score, float)
            assert isinstance(result.metadata, dict)
            assert result.key in [v["key"] for v in sample_vectors]

    def test_query_empty_store(self, backend: FAISSBackend, query_vector: list[float]) -> None:
        """Test querying an empty store."""
        backend.create_store("test-store", dimension=384)

        results = backend.query("test-store", query_vector, top_k=5)
        assert results == []

    def test_query_wrong_dimension(self, backend: FAISSBackend, query_vector: list[float]) -> None:
        """Test querying with wrong dimension raises an error."""
        backend.create_store("test-store", dimension=256)

        with pytest.raises(
            ValueError,
            match="Query vector dimension 384 does not match store dimension 256",
        ):
            backend.query("test-store", query_vector)

    def test_query_nonexistent_store(
        self, backend: FAISSBackend, query_vector: list[float]
    ) -> None:
        """Test querying a non-existent store raises an error."""
        with pytest.raises(ValueError, match="Store 'test-store' does not exist"):
            backend.query("test-store", query_vector)

    def test_query_top_k_larger_than_store(
        self, backend: FAISSBackend, sample_vectors: list[dict], query_vector: list[float]
    ) -> None:
        """Test querying with top_k larger than number of vectors in store."""
        backend.create_store("test-store", dimension=384)
        backend.put_vectors("test-store", sample_vectors[:3])  # Only 3 vectors

        results = backend.query("test-store", query_vector, top_k=10)
        assert len(results) <= 3


class TestStoreInfo:
    """Test getting store information."""

    def test_get_store_info(self, backend: FAISSBackend, sample_vectors: list[dict]) -> None:
        """Test getting information about a store."""
        backend.create_store("test-store", dimension=384)
        backend.put_vectors("test-store", sample_vectors)

        info = backend.get_store_info("test-store")

        assert info["name"] == "test-store"
        assert info["backend"] == "faiss"
        assert "test-store.faiss" in info["location"]
        assert info["dimension"] == 384
        assert info["vector_count"] == len(sample_vectors)
        assert info["metadata_keys"] == len(sample_vectors)
        assert isinstance(info["index_size_mb"], float)
        assert info["index_size_mb"] > 0

    def test_get_store_info_nonexistent(self, backend: FAISSBackend) -> None:
        """Test getting info for a non-existent store raises an error."""
        with pytest.raises(ValueError, match="Store 'test-store' does not exist"):
            backend.get_store_info("test-store")

    def test_get_store_info_empty(self, backend: FAISSBackend) -> None:
        """Test getting info for an empty store."""
        backend.create_store("test-store", dimension=384)

        info = backend.get_store_info("test-store")

        assert info["vector_count"] == 0
        assert info["metadata_keys"] == 0
        assert info["dimension"] == 384


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_high_dimensional_vectors(self, backend: FAISSBackend) -> None:
        """Test with high-dimensional vectors."""
        dimension = 1536  # OpenAI embedding dimension
        backend.create_store("high-dim-store", dimension=dimension)

        # Create high-dimensional vectors
        vectors = []
        for i in range(5):
            vec = np.random.randn(dimension).astype(np.float32)
            vec = vec / np.linalg.norm(vec)
            vectors.append(
                {
                    "key": f"high_dim_doc_{i}",
                    "embedding": vec.tolist(),
                    "metadata": {"dim": dimension},
                }
            )

        count = backend.put_vectors("high-dim-store", vectors)
        assert count == 5

        # Query with similar high-dimensional vector
        query_vec = np.random.randn(dimension).astype(np.float32)
        query_vec = query_vec / np.linalg.norm(query_vec)

        results = backend.query("high-dim-store", query_vec.tolist(), top_k=3)
        assert len(results) <= 3

    def test_single_vector(self, backend: FAISSBackend) -> None:
        """Test operations with a single vector."""
        backend.create_store("single-store", dimension=384)

        # Create a single vector
        vec = np.random.randn(384).astype(np.float32)
        vec = vec / np.linalg.norm(vec)

        vectors = [
            {
                "key": "single_doc",
                "embedding": vec.tolist(),
                "metadata": {"title": "Single Document"},
            }
        ]

        count = backend.put_vectors("single-store", vectors)
        assert count == 1

        # Query for the single vector
        results = backend.query("single-store", vec.tolist(), top_k=5)
        assert len(results) == 1
        assert results[0].key == "single_doc"
        assert results[0].score == pytest.approx(1.0, rel=1e-5)  # Perfect match

    def test_identical_vectors(self, backend: FAISSBackend) -> None:
        """Test storing and querying identical vectors."""
        backend.create_store("identical-store", dimension=384)

        # Create identical vectors
        vec = np.random.randn(384).astype(np.float32)
        vec = vec / np.linalg.norm(vec)

        vectors = [
            {
                "key": f"doc_{i}",
                "embedding": vec.tolist(),
                "metadata": {"copy": i},
            }
            for i in range(5)
        ]

        backend.put_vectors("identical-store", vectors)

        # Query should return all identical vectors
        results = backend.query("identical-store", vec.tolist(), top_k=10)
        assert len(results) == 5

        # All scores should be ~1.0 (identical)
        for result in results:
            assert result.score == pytest.approx(1.0, rel=1e-5)

    def test_orthogonal_vectors(self, backend: FAISSBackend) -> None:
        """Test with orthogonal vectors (should have low similarity)."""
        backend.create_store("orthogonal-store", dimension=384)

        # Create orthogonal vectors (using different random seeds)
        vectors = []
        for i in range(10):
            np.random.seed(i)  # Different seed for each vector
            vec = np.random.randn(384).astype(np.float32)
            vec = vec / np.linalg.norm(vec)
            vectors.append(
                {
                    "key": f"orthogonal_{i}",
                    "embedding": vec.tolist(),
                    "metadata": {"seed": i},
                }
            )

        backend.put_vectors("orthogonal-store", vectors)

        # Query with first vector
        query_vec = vectors[0]["embedding"]
        results = backend.query("orthogonal-store", query_vec, top_k=5)

        # First result should be the query vector itself (score ~1.0)
        if results:
            assert results[0].key == "orthogonal_0"
            assert results[0].score == pytest.approx(1.0, rel=1e-5)

            # Other results should have lower scores
            if len(results) > 1:
                for result in results[1:]:
                    assert result.score < 0.9  # Much lower similarity
