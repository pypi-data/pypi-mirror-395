"""
FAISS backend for local vector storage.

This module implements the VectorBackend interface using FAISS (Facebook AI
Similarity Search) for high-performance vector similarity search on local
storage. Vectors are stored in FAISS index files with JSON sidecar metadata.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import json
from pathlib import Path
from typing import Any, cast

import faiss
import numpy as np

from vector_rag_tool.core.backend import VectorBackend, VectorQueryResult
from vector_rag_tool.logging_config import get_logger

logger = get_logger(__name__)

# Store directory in user's config folder
STORES_DIR = Path.home() / ".config" / "vector-rag-tool" / "stores"


class FAISSBackend(VectorBackend):
    """Local FAISS vector storage backend."""

    def __init__(self) -> None:
        """Initialize FAISS backend and ensure stores directory exists."""
        STORES_DIR.mkdir(parents=True, exist_ok=True)
        logger.debug("FAISS backend initialized with stores dir: %s", STORES_DIR)

    def _index_path(self, store_name: str) -> Path:
        """Get the path to the FAISS index file for a store."""
        return STORES_DIR / f"{store_name}.faiss"

    def _meta_path(self, store_name: str) -> Path:
        """Get the path to the metadata JSON file for a store."""
        return STORES_DIR / f"{store_name}.meta.json"

    def _load_index(self, store_name: str) -> faiss.Index:
        """Load a FAISS index from disk."""
        path = self._index_path(store_name)
        if not path.exists():
            raise ValueError(f"Store '{store_name}' does not exist at {path}")

        logger.debug("Loading FAISS index from %s", path)
        return faiss.read_index(str(path))

    def _load_metadata(self, store_name: str) -> dict[str, Any]:
        """Load metadata for a store from disk."""
        path = self._meta_path(store_name)
        if path.exists():
            logger.debug("Loading metadata from %s", path)
            return cast(dict[str, Any], json.loads(path.read_text()))

        # Return default metadata if file doesn't exist
        return {"vectors": {}, "dimension": 768, "next_id": 0}

    def _save_metadata(self, store_name: str, metadata: dict[str, Any]) -> None:
        """Save metadata for a store to disk."""
        path = self._meta_path(store_name)
        logger.debug("Saving metadata to %s", path)
        path.write_text(json.dumps(metadata, indent=2))

    def create_store(self, store_name: str, dimension: int = 768) -> None:
        """Create a new vector store."""
        if self.store_exists(store_name):
            raise ValueError(f"Store '{store_name}' already exists")

        # Create empty FAISS index (IndexFlatIP for cosine similarity)
        logger.info("Creating FAISS store '%s' with dimension %d", store_name, dimension)
        index = faiss.IndexFlatIP(dimension)

        # Write the empty index to disk
        index_path = self._index_path(store_name)
        faiss.write_index(index, str(index_path))
        logger.debug("Created empty FAISS index at %s", index_path)

        # Create metadata file
        metadata = {
            "dimension": dimension,
            "vectors": {},  # key -> {index_id, metadata}
            "next_id": 0,
            "created_at": None,  # Will be added by frontend if needed
        }
        self._save_metadata(store_name, metadata)

        logger.info("Created FAISS store: %s", store_name)

    def delete_store(self, store_name: str) -> None:
        """Delete a vector store."""
        index_path = self._index_path(store_name)
        meta_path = self._meta_path(store_name)

        # Remove both index and metadata files if they exist
        index_path.unlink(missing_ok=True)
        meta_path.unlink(missing_ok=True)

        logger.info("Deleted FAISS store: %s", store_name)

    def list_stores(self) -> list[str]:
        """List all available stores."""
        stores = [p.stem for p in STORES_DIR.glob("*.faiss")]
        logger.debug("Found %d stores: %s", len(stores), stores)
        return stores

    def store_exists(self, store_name: str) -> bool:
        """Check if store exists."""
        exists = self._index_path(store_name).exists()
        logger.debug("Store '%s' exists: %s", store_name, exists)
        return exists

    def put_vectors(self, store_name: str, vectors: list[dict[str, Any]]) -> int:
        """Insert vectors into store. Returns count inserted."""
        if not vectors:
            return 0

        # Load existing index and metadata
        index = self._load_index(store_name)
        metadata = self._load_metadata(store_name)

        logger.debug("Inserting %d vectors into store '%s'", len(vectors), store_name)

        # Extract embeddings and convert to numpy array
        embeddings = np.array([v["embedding"] for v in vectors], dtype=np.float32)

        # Validate dimension matches the index
        expected_dim = index.d
        if embeddings.shape[1] != expected_dim:
            raise ValueError(
                f"Vector dimension {embeddings.shape[1]} does not match "
                f"store dimension {expected_dim}"
            )

        # Normalize vectors for cosine similarity
        faiss.normalize_L2(embeddings)

        # Add vectors to index
        start_id = metadata["next_id"]
        index.add(embeddings)
        logger.debug("Added %d vectors to FAISS index", len(vectors))

        # Update metadata to track vector keys and their index IDs
        for i, vector_data in enumerate(vectors):
            key = vector_data["key"]
            metadata["vectors"][key] = {
                "index_id": start_id + i,
                "metadata": vector_data.get("metadata", {}),
            }
        metadata["next_id"] = start_id + len(vectors)

        # Save both index and metadata
        faiss.write_index(index, str(self._index_path(store_name)))
        self._save_metadata(store_name, metadata)

        logger.info("Inserted %d vectors into store '%s'", len(vectors), store_name)
        return len(vectors)

    def delete_vectors(self, store_name: str, keys: list[str]) -> int:
        """Delete vectors by keys. Returns count deleted."""
        # Note: FAISS doesn't support efficient deletion of individual vectors
        # This implementation would require rebuilding the index
        # For now, we'll remove from metadata but the vectors remain in the index

        if not keys:
            return 0

        metadata = self._load_metadata(store_name)
        deleted_count = 0

        for key in keys:
            if key in metadata["vectors"]:
                del metadata["vectors"][key]
                deleted_count += 1

        if deleted_count > 0:
            self._save_metadata(store_name, metadata)
            logger.warning(
                "Deleted %d vectors from metadata (but not from FAISS index). "
                "Consider rebuilding the index to fully remove vectors.",
                deleted_count,
            )

        return deleted_count

    def query(
        self,
        store_name: str,
        query_vector: list[float],
        top_k: int = 5,
    ) -> list[VectorQueryResult]:
        """Query for similar vectors."""
        # Load index and metadata
        index = self._load_index(store_name)
        metadata = self._load_metadata(store_name)

        logger.debug("Querying store '%s' with top_k=%d", store_name, top_k)

        # Validate query vector dimension
        expected_dim = index.d
        if len(query_vector) != expected_dim:
            raise ValueError(
                f"Query vector dimension {len(query_vector)} does not match "
                f"store dimension {expected_dim}"
            )

        # Normalize query vector for cosine similarity
        query = np.array([query_vector], dtype=np.float32)
        faiss.normalize_L2(query)

        # Perform search
        k = min(top_k, index.ntotal)  # Can't return more vectors than exist
        if k == 0:
            return []

        scores, indices = index.search(query, k)
        logger.debug("Search returned %d results", k)

        # Map index IDs back to vector keys
        id_to_key = {
            vector_data["index_id"]: key for key, vector_data in metadata["vectors"].items()
        }

        # Build results
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:  # FAISS returns -1 for missing results
                continue

            key = id_to_key.get(idx)
            if key:
                vector_data = metadata["vectors"][key]
                results.append(
                    VectorQueryResult(
                        key=key,
                        score=float(score),
                        metadata=vector_data["metadata"],
                        content=vector_data["metadata"].get("content_preview"),
                    )
                )

        logger.info("Query returned %d results from store '%s'", len(results), store_name)
        return results

    def get_store_info(self, store_name: str) -> dict[str, Any]:
        """Get store metadata (vector count, dimension, etc.)."""
        if not self.store_exists(store_name):
            raise ValueError(f"Store '{store_name}' does not exist")

        index = self._load_index(store_name)
        metadata = self._load_metadata(store_name)

        return {
            "name": store_name,
            "backend": "faiss",
            "location": str(self._index_path(store_name)),
            "dimension": metadata["dimension"],
            "vector_count": index.ntotal,
            "metadata_keys": len(metadata["vectors"]),
            "index_size_mb": self._index_path(store_name).stat().st_size / (1024 * 1024),
        }

    def get_file_hashes(self, store_name: str) -> dict[str, str]:
        """Get stored file hashes for incremental indexing."""
        if not self.store_exists(store_name):
            return {}

        metadata = self._load_metadata(store_name)
        hashes: dict[str, str] = metadata.get("file_hashes", {})
        logger.debug("Loaded %d file hashes from store '%s'", len(hashes), store_name)
        return hashes

    def set_file_hashes(self, store_name: str, hashes: dict[str, str]) -> None:
        """Save file hashes for incremental indexing."""
        if not self.store_exists(store_name):
            logger.warning("Cannot save hashes: store '%s' does not exist", store_name)
            return

        metadata = self._load_metadata(store_name)
        metadata["file_hashes"] = hashes
        self._save_metadata(store_name, metadata)
        logger.debug("Saved %d file hashes to store '%s'", len(hashes), store_name)
