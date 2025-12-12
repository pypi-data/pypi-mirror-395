# Dual Backend Design: FAISS (Local) + S3 Vectors (Remote)

## Overview

The tool supports two vector storage backends:

| Backend | Trigger | Store Location |
|---------|---------|----------------|
| **FAISS** (default) | No `--bucket` flag | `~/.config/vector-rag-tool/stores/<store>.faiss` |
| **S3 Vectors** | `--bucket <name>` | `s3://<bucket>/<store>/` (index within bucket) |

## CLI Design

### Mode Selection

```bash
# LOCAL mode (FAISS) - default
vector-rag-tool index "**/*.md" --store mystore
vector-rag-tool query "search term" --store mystore

# REMOTE mode (S3 Vectors) - with --bucket
vector-rag-tool index "**/*.md" --store mystore --bucket obsidian-rag-bucket
vector-rag-tool query "search term" --store mystore --bucket obsidian-rag-bucket
```

### Store Management

```bash
# List stores (shows both local and remote if bucket specified)
vector-rag-tool store list                           # Local stores only
vector-rag-tool store list --bucket my-bucket        # Remote stores in bucket

# Create store
vector-rag-tool store create mystore                 # Creates local FAISS
vector-rag-tool store create mystore --bucket x      # Creates S3 index

# Delete store
vector-rag-tool store delete mystore                 # Deletes local FAISS file
vector-rag-tool store delete mystore --bucket x      # Deletes S3 index

# Info
vector-rag-tool store info mystore                   # Local store info
vector-rag-tool store info mystore --bucket x        # Remote store info
```

### Indexing

```bash
# Index to local FAISS
vector-rag-tool index "**/*.md" --store obsidian-vault

# Index to S3 Vectors
vector-rag-tool index "**/*.md" --store obsidian-vault --bucket obsidian-rag-bucket

# With AWS profile (for S3)
vector-rag-tool index "**/*.md" --store vault --bucket my-bucket \
    --profile sandbox-ilionx-amf --region eu-central-1
```

### Querying

```bash
# Query local FAISS
vector-rag-tool query "authentication patterns" --store obsidian-vault

# Query S3 Vectors
vector-rag-tool query "authentication patterns" --store obsidian-vault \
    --bucket obsidian-rag-bucket

# With options
vector-rag-tool query "auth" --store vault --top-k 10 --json
vector-rag-tool query "auth" --store vault --bucket x --top-k 10 --json
```

## Storage Layout

### Local FAISS

```
~/.config/vector-rag-tool/
├── config.yaml                    # Global configuration
└── stores/
    ├── obsidian-vault.faiss       # FAISS index file
    ├── obsidian-vault.meta.json   # Metadata (file paths, hashes, etc.)
    ├── python-code.faiss
    ├── python-code.meta.json
    └── ...
```

### S3 Vectors

```
s3://obsidian-rag-bucket/          # Vector bucket (S3 Vectors type)
├── obsidian-vault/                # Index name = store name
│   └── (managed by S3 Vectors)
├── python-code/
│   └── (managed by S3 Vectors)
└── ...
```

## Architecture

### Backend Abstraction

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass
class QueryResult:
    """Result from vector similarity search."""
    key: str
    score: float
    metadata: dict
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
        vectors: list[dict],  # [{'key': str, 'embedding': list, 'metadata': dict}]
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
    ) -> list[QueryResult]:
        """Query for similar vectors."""
        pass

    @abstractmethod
    def get_store_info(self, store_name: str) -> dict:
        """Get store metadata (vector count, dimension, etc.)."""
        pass
```

### FAISS Backend

```python
import json
from pathlib import Path

import faiss
import numpy as np

from vector_rag_tool.core.backend import VectorBackend, QueryResult
from vector_rag_tool.logging_config import get_logger

logger = get_logger(__name__)

STORES_DIR = Path.home() / ".config" / "vector-rag-tool" / "stores"


class FAISSBackend(VectorBackend):
    """Local FAISS vector storage backend."""

    def __init__(self):
        STORES_DIR.mkdir(parents=True, exist_ok=True)

    def _index_path(self, store_name: str) -> Path:
        return STORES_DIR / f"{store_name}.faiss"

    def _meta_path(self, store_name: str) -> Path:
        return STORES_DIR / f"{store_name}.meta.json"

    def _load_index(self, store_name: str) -> faiss.Index:
        path = self._index_path(store_name)
        if not path.exists():
            raise ValueError(f"Store '{store_name}' does not exist")
        return faiss.read_index(str(path))

    def _load_metadata(self, store_name: str) -> dict:
        path = self._meta_path(store_name)
        if path.exists():
            return json.loads(path.read_text())
        return {"vectors": {}, "dimension": 768}

    def _save_metadata(self, store_name: str, metadata: dict) -> None:
        self._meta_path(store_name).write_text(json.dumps(metadata, indent=2))

    def create_store(self, store_name: str, dimension: int = 768) -> None:
        if self.store_exists(store_name):
            raise ValueError(f"Store '{store_name}' already exists")

        # Create empty FAISS index (IndexFlatIP for cosine similarity)
        index = faiss.IndexFlatIP(dimension)
        faiss.write_index(index, str(self._index_path(store_name)))

        # Create metadata file
        self._save_metadata(store_name, {
            "dimension": dimension,
            "vectors": {},  # key -> {index_id, metadata}
            "next_id": 0,
        })

        logger.info("Created FAISS store: %s", store_name)

    def delete_store(self, store_name: str) -> None:
        self._index_path(store_name).unlink(missing_ok=True)
        self._meta_path(store_name).unlink(missing_ok=True)
        logger.info("Deleted FAISS store: %s", store_name)

    def list_stores(self) -> list[str]:
        return [p.stem for p in STORES_DIR.glob("*.faiss")]

    def store_exists(self, store_name: str) -> bool:
        return self._index_path(store_name).exists()

    def put_vectors(self, store_name: str, vectors: list[dict]) -> int:
        index = self._load_index(store_name)
        meta = self._load_metadata(store_name)

        # Normalize vectors for cosine similarity
        embeddings = np.array([v["embedding"] for v in vectors], dtype=np.float32)
        faiss.normalize_L2(embeddings)

        # Add to index
        start_id = meta["next_id"]
        index.add(embeddings)

        # Update metadata
        for i, v in enumerate(vectors):
            meta["vectors"][v["key"]] = {
                "index_id": start_id + i,
                "metadata": v.get("metadata", {}),
            }
        meta["next_id"] = start_id + len(vectors)

        # Save
        faiss.write_index(index, str(self._index_path(store_name)))
        self._save_metadata(store_name, meta)

        return len(vectors)

    def query(
        self,
        store_name: str,
        query_vector: list[float],
        top_k: int = 5,
    ) -> list[QueryResult]:
        index = self._load_index(store_name)
        meta = self._load_metadata(store_name)

        # Normalize query vector
        query = np.array([query_vector], dtype=np.float32)
        faiss.normalize_L2(query)

        # Search
        scores, indices = index.search(query, top_k)

        # Map back to keys
        id_to_key = {v["index_id"]: k for k, v in meta["vectors"].items()}

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:  # FAISS returns -1 for missing results
                continue
            key = id_to_key.get(idx)
            if key:
                results.append(QueryResult(
                    key=key,
                    score=float(score),
                    metadata=meta["vectors"][key]["metadata"],
                ))

        return results

    def get_store_info(self, store_name: str) -> dict:
        index = self._load_index(store_name)
        meta = self._load_metadata(store_name)
        return {
            "name": store_name,
            "backend": "faiss",
            "location": str(self._index_path(store_name)),
            "dimension": meta["dimension"],
            "vector_count": index.ntotal,
        }
```

### S3 Vectors Backend

```python
import boto3

from vector_rag_tool.core.backend import VectorBackend, QueryResult
from vector_rag_tool.logging_config import get_logger

logger = get_logger(__name__)


class S3VectorsBackend(VectorBackend):
    """AWS S3 Vectors storage backend."""

    def __init__(
        self,
        bucket_name: str,
        region: str = "eu-central-1",
        profile: str | None = None,
    ):
        self.bucket_name = bucket_name
        session = boto3.Session(profile_name=profile, region_name=region)
        self.client = session.client("s3vectors")

    def create_store(self, store_name: str, dimension: int = 768) -> None:
        # Ensure bucket exists (create if needed)
        try:
            self.client.create_vector_bucket(vectorBucketName=self.bucket_name)
        except self.client.exceptions.BucketAlreadyExists:
            pass

        # Create index
        self.client.create_index(
            vectorBucketName=self.bucket_name,
            indexName=store_name,
            dimension=dimension,
            distanceMetric="cosine",
        )
        logger.info("Created S3 Vectors store: %s/%s", self.bucket_name, store_name)

    def delete_store(self, store_name: str) -> None:
        self.client.delete_index(
            vectorBucketName=self.bucket_name,
            indexName=store_name,
        )
        logger.info("Deleted S3 Vectors store: %s/%s", self.bucket_name, store_name)

    def list_stores(self) -> list[str]:
        response = self.client.list_indexes(vectorBucketName=self.bucket_name)
        return [idx["indexName"] for idx in response.get("indexes", [])]

    def store_exists(self, store_name: str) -> bool:
        return store_name in self.list_stores()

    def put_vectors(self, store_name: str, vectors: list[dict]) -> int:
        s3_vectors = [
            {
                "key": v["key"],
                "data": {"float32": v["embedding"]},
                "metadata": v.get("metadata", {}),
            }
            for v in vectors
        ]

        self.client.put_vectors(
            vectorBucketName=self.bucket_name,
            indexName=store_name,
            vectors=s3_vectors,
        )
        return len(vectors)

    def query(
        self,
        store_name: str,
        query_vector: list[float],
        top_k: int = 5,
    ) -> list[QueryResult]:
        response = self.client.query_vectors(
            vectorBucketName=self.bucket_name,
            indexName=store_name,
            queryVector={"float32": query_vector},
            topK=top_k,
        )

        return [
            QueryResult(
                key=v["key"],
                score=v["score"],
                metadata=v.get("metadata", {}),
            )
            for v in response.get("vectors", [])
        ]

    def get_store_info(self, store_name: str) -> dict:
        # S3 Vectors API for index info
        return {
            "name": store_name,
            "backend": "s3vectors",
            "bucket": self.bucket_name,
            "location": f"s3://{self.bucket_name}/{store_name}/",
        }
```

### Backend Factory

```python
from vector_rag_tool.core.backend import VectorBackend
from vector_rag_tool.core.faiss_backend import FAISSBackend
from vector_rag_tool.core.s3vectors_backend import S3VectorsBackend


def get_backend(
    bucket: str | None = None,
    region: str = "eu-central-1",
    profile: str | None = None,
) -> VectorBackend:
    """Get appropriate backend based on configuration.

    Args:
        bucket: S3 bucket name. If None, uses local FAISS.
        region: AWS region for S3 Vectors.
        profile: AWS profile name.

    Returns:
        VectorBackend instance (FAISS or S3Vectors)
    """
    if bucket:
        return S3VectorsBackend(
            bucket_name=bucket,
            region=region,
            profile=profile,
        )
    else:
        return FAISSBackend()
```

### CLI Integration

```python
import click

from vector_rag_tool.core.backend_factory import get_backend


@click.group()
@click.option("--bucket", "-b", help="S3 bucket for remote storage (omit for local FAISS)")
@click.option("--region", default="eu-central-1", help="AWS region")
@click.option("--profile", help="AWS profile name")
@click.pass_context
def main(ctx, bucket, region, profile):
    """Obsidian RAG tool with local (FAISS) and remote (S3 Vectors) support."""
    ctx.ensure_object(dict)
    ctx.obj["backend"] = get_backend(bucket=bucket, region=region, profile=profile)
    ctx.obj["bucket"] = bucket


@main.command()
@click.argument("glob_pattern")
@click.option("--store", "-s", required=True, help="Store name")
@click.pass_context
def index(ctx, glob_pattern, store):
    """Index files matching glob pattern."""
    backend = ctx.obj["backend"]
    # ... indexing logic


@main.command()
@click.argument("query_text")
@click.option("--store", "-s", required=True, help="Store name")
@click.option("--top-k", "-k", default=5, help="Number of results")
@click.pass_context
def query(ctx, query_text, store, top_k):
    """Query for similar documents."""
    backend = ctx.obj["backend"]
    # ... query logic
```

## Dependencies Update

```toml
[project]
dependencies = [
    "click>=8.1.7",
    "boto3>=1.35.0",
    "ollama>=0.1.0",
    "tqdm>=4.66.0",
    "pyyaml>=6.0.0",
    "langchain-text-splitters>=0.2.0",
    "faiss-cpu>=1.7.0",               # FAISS for local vector storage
    "numpy>=1.24.0",                   # Required by FAISS
]
```

## Usage Examples

### Local Development (FAISS)

```bash
# Create local store
vector-rag-tool store create obsidian-vault

# Index vault
vector-rag-tool index "**/*.md" --store obsidian-vault

# Query
vector-rag-tool query "authentication" --store obsidian-vault
```

### Production (S3 Vectors)

```bash
# Create remote store
vector-rag-tool store create obsidian-vault \
    --bucket obsidian-rag-prod \
    --profile sandbox-ilionx-amf

# Index vault
vector-rag-tool index "**/*.md" --store obsidian-vault \
    --bucket obsidian-rag-prod \
    --profile sandbox-ilionx-amf

# Query
vector-rag-tool query "authentication" --store obsidian-vault \
    --bucket obsidian-rag-prod \
    --profile sandbox-ilionx-amf
```

### Multiple Stores

```bash
# Local stores for different projects
vector-rag-tool index "vault/**/*.md" --store obsidian-notes
vector-rag-tool index "code/**/*.py" --store python-code
vector-rag-tool index "docs/**/*.md" --store documentation

# Query specific store
vector-rag-tool query "decorator pattern" --store python-code

# List all local stores
vector-rag-tool store list
# Output:
# Local stores (~/.config/vector-rag-tool/stores/):
#   - obsidian-notes (1234 vectors)
#   - python-code (567 vectors)
#   - documentation (890 vectors)
```

## Comparison

| Feature | FAISS (Local) | S3 Vectors (Remote) |
|---------|---------------|---------------------|
| **Latency** | <10ms | 100ms-1s |
| **Cost** | Free | Pay-per-use |
| **Scalability** | Limited by disk | Elastic |
| **Offline** | Yes | No |
| **Sharing** | Manual sync | Native |
| **Persistence** | Local files | Managed |

## When to Use Which

| Use Case | Recommended Backend |
|----------|---------------------|
| Local development | FAISS |
| Quick testing | FAISS |
| Offline usage | FAISS |
| Production | S3 Vectors |
| Team sharing | S3 Vectors |
| Large datasets | S3 Vectors |
| Cost-sensitive | FAISS |
