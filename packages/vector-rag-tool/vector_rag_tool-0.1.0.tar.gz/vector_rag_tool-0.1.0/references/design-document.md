# vector-rag-tool Design Document

## Related Documentation

| Document | Location |
|----------|----------|
| RAG Architecture Options | `obsidian-vault://reference/ai-ml/rag/rag-architecture-options.md` |
| EmbeddingGemma Model Card | `obsidian-vault://reference/ai-ml/ollama/embeddinggemma-model-card.md` |
| EmbeddingGemma Fit Assessment | `references/embeddinggemma-fit-assessment.md` |
| Ollama Integration Patterns | `references/ollama-integration-patterns.md` |

**Obsidian Vault Path:** `/Users/dennisvriend/projects/obsidian-knowledge-base`

## Overview

This document specifies the architecture and implementation details for `vector-rag-tool`, a CLI tool for semantic search over document collections using:

- **Embeddings**: Ollama `embeddinggemma` (local, no content filtering)
- **Vector Storage**: AWS S3 Vectors (managed, pay-per-use)
- **Chunking**: LangChain text splitters (language-aware)

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           vector-rag-tool                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  CLI Layer (Click)                                                          │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  store create/delete/list  │  index  │  query  │  status  │  list     │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                         │
│  Service Layer                     ▼                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │ StoreManager │  │   Indexer    │  │   Querier    │  │  FileDetector    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────────┘ │
│          │                │                │                    │            │
│  ┌───────┴────────────────┴────────────────┴────────────────────┘            │
│  │                                                                           │
│  │  Core Components                                                          │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────────────┐│
│  │  │  Embeddings  │  │  S3Vectors   │  │  ChunkingStrategies              ││
│  │  │  (Ollama)    │  │  (boto3)     │  │  (LangChain text-splitters)      ││
│  │  └──────────────┘  └──────────────┘  └──────────────────────────────────┘│
│  │                                                                           │
│  └───────────────────────────────────────────────────────────────────────────┘
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Core Concepts

### Store

A **Store** is an isolated container for vectors and their metadata. Each store maps to:

- An S3 Vector Bucket (or namespace within a bucket)
- A Vector Index with specific configuration

```python
@dataclass
class Store:
    name: str                    # e.g., "obsidian-vault", "python-projects"
    bucket_name: str             # S3 vector bucket name
    index_name: str              # Vector index within bucket
    dimension: int               # Embedding dimension (768 for embeddinggemma)
    distance_metric: str         # "cosine" | "euclidean" | "dot_product"
    created_at: datetime
    file_count: int
    chunk_count: int
```

### Document Chunk

A **Chunk** is a segment of a file with metadata for retrieval:

```python
@dataclass
class Chunk:
    key: str                     # Unique ID: "{file_hash}_{chunk_index}"
    content: str                 # The actual text content
    embedding: list[float]       # 768-dim vector from embeddinggemma
    metadata: ChunkMetadata

@dataclass
class ChunkMetadata:
    file_path: str               # Relative path from index root
    file_type: str               # "markdown" | "python" | "yaml" | etc.
    chunk_index: int             # Position in file
    start_line: int              # Line number where chunk starts
    end_line: int                # Line number where chunk ends
    file_hash: str               # SHA256 of file (for change detection)
    tags: list[str]              # Extracted tags (from frontmatter, etc.)
    title: str | None            # Document title if available
    indexed_at: datetime
```

## CLI Commands

### Store Management

```bash
# Create a new store
vector-rag-tool store create <name> [--dimension 768] [--metric cosine]

# List all stores
vector-rag-tool store list [--json]

# Delete a store (requires confirmation)
vector-rag-tool store delete <name> [--force]

# Show store details
vector-rag-tool store info <name>
```

### Indexing

```bash
# Index files matching glob pattern into a store
vector-rag-tool index <glob-pattern> --store <name> [--dry-run]

# Examples:
vector-rag-tool index "**/*.md" --store obsidian-vault
vector-rag-tool index "src/**/*.py" --store python-code
vector-rag-tool index "**/*.{md,py,yaml}" --store mixed-content

# Incremental indexing (only changed files)
vector-rag-tool index "**/*.md" --store obsidian-vault --incremental

# Force re-index all files
vector-rag-tool index "**/*.md" --store obsidian-vault --force
```

### Querying

```bash
# Query a store
vector-rag-tool query "authentication patterns" --store obsidian-vault

# Query with options
vector-rag-tool query "how to configure S3" --store obsidian-vault \
    --top-k 10 \
    --min-score 0.7 \
    --json

# Query with metadata filter
vector-rag-tool query "lambda functions" --store obsidian-vault \
    --filter "file_type=python"

# Query from stdin (for piping)
echo "error handling patterns" | vector-rag-tool query --stdin --store mystore
```

### Status & Listing

```bash
# Show overall status
vector-rag-tool status

# List indexed files in a store
vector-rag-tool list --store obsidian-vault [--json]
```

## Query Response Format

### Console Output (Default)

```
$ vector-rag-tool query "authentication patterns" --store obsidian-vault

Found 5 relevant chunks:

┌─────┬───────┬────────────────────────────────────────────────────────────────┐
│ #   │ Score │ Location                                                       │
├─────┼───────┼────────────────────────────────────────────────────────────────┤
│ 1   │ 0.92  │ work/projects/vodafone/auth-patterns.md:45-67                  │
├─────┴───────┴────────────────────────────────────────────────────────────────┤
│ OAuth2 with PKCE flow for mobile clients using Layer7 API Gateway.          │
│ The authentication flow consists of:                                         │
│ 1. Client requests authorization code with PKCE challenge                    │
│ 2. User authenticates via identity provider                                  │
│ 3. Authorization code exchanged for tokens...                                │
├─────┬───────┬────────────────────────────────────────────────────────────────┤
│ 2   │ 0.87  │ reference/aws/cognito-setup.md:12-34                           │
├─────┴───────┴────────────────────────────────────────────────────────────────┤
│ User pool configuration with MFA enabled. Configure the following:          │
│ - Password policy: minimum 12 characters                                     │
│ - MFA: Required for all users                                                │
│ - Token validity: Access token 1 hour, refresh token 30 days...             │
└──────────────────────────────────────────────────────────────────────────────┘
```

### JSON Output (--json)

```json
{
  "query": "authentication patterns",
  "store": "obsidian-vault",
  "results": [
    {
      "rank": 1,
      "score": 0.92,
      "file_path": "work/projects/vodafone/auth-patterns.md",
      "file_type": "markdown",
      "start_line": 45,
      "end_line": 67,
      "content": "OAuth2 with PKCE flow for mobile clients...",
      "metadata": {
        "title": "Authentication Patterns",
        "tags": ["#auth", "#oauth", "#vodafone"],
        "indexed_at": "2024-12-04T19:30:00Z"
      }
    },
    {
      "rank": 2,
      "score": 0.87,
      "file_path": "reference/aws/cognito-setup.md",
      "file_type": "markdown",
      "start_line": 12,
      "end_line": 34,
      "content": "User pool configuration with MFA enabled...",
      "metadata": {
        "title": "Cognito Setup Guide",
        "tags": ["#aws", "#cognito", "#auth"],
        "indexed_at": "2024-12-04T19:30:00Z"
      }
    }
  ],
  "total_results": 5,
  "query_time_ms": 245
}
```

## File Type Detection & Chunking Strategies

### File Type Detection

Detect file type by extension and optionally by content analysis:

```python
FILE_TYPE_MAP = {
    # Markdown
    ".md": "markdown",
    ".mdx": "markdown",

    # Python
    ".py": "python",
    ".pyi": "python",

    # TypeScript/JavaScript
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",

    # JVM Languages
    ".java": "java",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".scala": "scala",
    ".groovy": "groovy",

    # Go
    ".go": "go",

    # Rust
    ".rs": "rust",

    # Configuration
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".toml": "toml",

    # Shell
    ".sh": "shell",
    ".bash": "shell",
    ".zsh": "shell",

    # Other
    ".txt": "text",
    ".rst": "rst",
    ".html": "html",
    ".xml": "xml",
    ".sql": "sql",
    ".tf": "terraform",
    ".hcl": "terraform",
}
```

### LangChain Text Splitters

Use `langchain-text-splitters` for intelligent chunking:

```python
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    Language,
    MarkdownHeaderTextSplitter,
)

# Install: pip install langchain-text-splitters
```

### Chunking Strategy per File Type

| File Type | Splitter | Chunk Size | Overlap | Special Handling |
|-----------|----------|------------|---------|------------------|
| **Markdown** | MarkdownHeaderTextSplitter + Recursive | 1000 | 200 | Preserve headers, frontmatter |
| **Python** | RecursiveCharacterTextSplitter(Language.PYTHON) | 1500 | 200 | Preserve functions/classes |
| **TypeScript** | RecursiveCharacterTextSplitter(Language.TS) | 1500 | 200 | Preserve functions/classes |
| **Java** | RecursiveCharacterTextSplitter(Language.JAVA) | 2000 | 300 | Preserve methods/classes |
| **Kotlin** | RecursiveCharacterTextSplitter(Language.KOTLIN) | 1500 | 200 | Preserve functions |
| **Go** | RecursiveCharacterTextSplitter(Language.GO) | 1500 | 200 | Preserve functions |
| **YAML** | RecursiveCharacterTextSplitter | 500 | 100 | Keep structure intact |
| **JSON** | RecursiveJsonSplitter | 500 | 0 | Preserve JSON structure |
| **Text** | RecursiveCharacterTextSplitter | 1000 | 200 | Generic splitting |

### Chunking Implementation

```python
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    Language,
    MarkdownHeaderTextSplitter,
)
from dataclasses import dataclass
from typing import Iterator


@dataclass
class ChunkingConfig:
    chunk_size: int
    chunk_overlap: int
    language: Language | None = None


CHUNKING_CONFIGS: dict[str, ChunkingConfig] = {
    "markdown": ChunkingConfig(chunk_size=1000, chunk_overlap=200),
    "python": ChunkingConfig(chunk_size=1500, chunk_overlap=200, language=Language.PYTHON),
    "typescript": ChunkingConfig(chunk_size=1500, chunk_overlap=200, language=Language.TS),
    "javascript": ChunkingConfig(chunk_size=1500, chunk_overlap=200, language=Language.JS),
    "java": ChunkingConfig(chunk_size=2000, chunk_overlap=300, language=Language.JAVA),
    "kotlin": ChunkingConfig(chunk_size=1500, chunk_overlap=200, language=Language.KOTLIN),
    "go": ChunkingConfig(chunk_size=1500, chunk_overlap=200, language=Language.GO),
    "rust": ChunkingConfig(chunk_size=1500, chunk_overlap=200, language=Language.RUST),
    "yaml": ChunkingConfig(chunk_size=500, chunk_overlap=100),
    "json": ChunkingConfig(chunk_size=500, chunk_overlap=0),
    "text": ChunkingConfig(chunk_size=1000, chunk_overlap=200),
}


class ChunkingStrategy:
    """Factory for creating appropriate text splitters."""

    @staticmethod
    def get_splitter(file_type: str) -> RecursiveCharacterTextSplitter:
        config = CHUNKING_CONFIGS.get(file_type, CHUNKING_CONFIGS["text"])

        if file_type == "markdown":
            return ChunkingStrategy._get_markdown_splitter(config)
        elif config.language:
            return RecursiveCharacterTextSplitter.from_language(
                language=config.language,
                chunk_size=config.chunk_size,
                chunk_overlap=config.chunk_overlap,
            )
        else:
            return RecursiveCharacterTextSplitter(
                chunk_size=config.chunk_size,
                chunk_overlap=config.chunk_overlap,
            )

    @staticmethod
    def _get_markdown_splitter(config: ChunkingConfig) -> RecursiveCharacterTextSplitter:
        """Special handling for Markdown with header awareness."""
        # First split by headers
        headers_to_split_on = [
            ("#", "header1"),
            ("##", "header2"),
            ("###", "header3"),
        ]

        # Then use recursive splitter for content within sections
        return RecursiveCharacterTextSplitter.from_language(
            language=Language.MARKDOWN,
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
        )
```

### Markdown-Specific: Frontmatter Extraction

```python
import yaml
import re


def extract_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter from Markdown content.

    Returns:
        Tuple of (frontmatter_dict, content_without_frontmatter)
    """
    frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(frontmatter_pattern, content, re.DOTALL)

    if match:
        try:
            frontmatter = yaml.safe_load(match.group(1))
            content_without_fm = content[match.end():]
            return frontmatter or {}, content_without_fm
        except yaml.YAMLError:
            return {}, content

    return {}, content


def extract_tags_from_content(content: str) -> list[str]:
    """Extract #tags from Markdown content."""
    tag_pattern = r'#[\w-]+'
    return list(set(re.findall(tag_pattern, content)))
```

## Ollama Embedding Integration

### Using the Official `ollama` Package

Use the official `ollama` Python package (not raw HTTP requests) for cleaner integration.
See `references/ollama-integration-patterns.md` for detailed patterns from `ollama-deepseek-ocr-tool`.

```python
import ollama

from vector_rag_tool.logging_config import get_logger

logger = get_logger(__name__)


class OllamaEmbeddings:
    """Generate embeddings using Ollama local API."""

    def __init__(self, model: str = "embeddinggemma"):
        self.model = model
        self._dimension: int | None = None

    @property
    def dimension(self) -> int:
        """Return embedding dimension (768 for embeddinggemma)."""
        if self._dimension is None:
            test_embedding = self.embed_text("test")
            self._dimension = len(test_embedding)
        return self._dimension

    def embed_text(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        logger.debug("Embedding text: %s...", text[:50])

        try:
            response = ollama.embed(model=self.model, input=text)
            embedding: list[float] = response["embeddings"][0]
            return embedding
        except Exception as e:
            logger.error("Embedding failed: %s", str(e))
            raise RuntimeError(f"Embedding generation failed: {e}") from e

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        logger.debug("Embedding batch of %d texts", len(texts))

        try:
            response = ollama.embed(model=self.model, input=texts)
            return response["embeddings"]
        except Exception as e:
            logger.error("Batch embedding failed: %s", str(e))
            raise RuntimeError(f"Batch embedding failed: {e}") from e


# Usage
embeddings = OllamaEmbeddings(model="embeddinggemma")
vector = embeddings.embed_text("Hello, world!")
print(f"Dimension: {len(vector)}")  # 768
```

### Batch Processing with Progress

```python
from tqdm import tqdm
from typing import Iterator


def embed_chunks_with_progress(
    chunks: list[Chunk],
    embeddings: OllamaEmbeddings,
    batch_size: int = 10,
) -> Iterator[Chunk]:
    """Embed chunks in batches with progress bar."""

    for i in tqdm(range(0, len(chunks), batch_size), desc="Embedding"):
        batch = chunks[i:i + batch_size]
        texts = [chunk.content for chunk in batch]
        vectors = embeddings.embed_batch(texts)

        for chunk, vector in zip(batch, vectors):
            chunk.embedding = vector
            yield chunk
```

## S3 Vectors Integration

### boto3 S3 Vectors Client

```python
import boto3
from typing import Any


class S3VectorsClient:
    """Wrapper for AWS S3 Vectors operations."""

    def __init__(self, region: str = "eu-central-1", profile: str | None = None):
        session = boto3.Session(profile_name=profile, region_name=region)
        self.client = session.client("s3vectors")

    # --- Store/Bucket Operations ---

    def create_bucket(self, bucket_name: str) -> dict[str, Any]:
        """Create a vector bucket."""
        return self.client.create_vector_bucket(
            vectorBucketName=bucket_name,
        )

    def delete_bucket(self, bucket_name: str) -> dict[str, Any]:
        """Delete a vector bucket."""
        return self.client.delete_vector_bucket(
            vectorBucketName=bucket_name,
        )

    def list_buckets(self) -> list[dict[str, Any]]:
        """List all vector buckets."""
        response = self.client.list_vector_buckets()
        return response.get("vectorBuckets", [])

    # --- Index Operations ---

    def create_index(
        self,
        bucket_name: str,
        index_name: str,
        dimension: int = 768,
        distance_metric: str = "cosine",
    ) -> dict[str, Any]:
        """Create a vector index within a bucket."""
        return self.client.create_index(
            vectorBucketName=bucket_name,
            indexName=index_name,
            dimension=dimension,
            distanceMetric=distance_metric,
        )

    def delete_index(self, bucket_name: str, index_name: str) -> dict[str, Any]:
        """Delete a vector index."""
        return self.client.delete_index(
            vectorBucketName=bucket_name,
            indexName=index_name,
        )

    def list_indexes(self, bucket_name: str) -> list[dict[str, Any]]:
        """List all indexes in a bucket."""
        response = self.client.list_indexes(vectorBucketName=bucket_name)
        return response.get("indexes", [])

    # --- Vector Operations ---

    def put_vectors(
        self,
        bucket_name: str,
        index_name: str,
        vectors: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Insert vectors into an index.

        Args:
            vectors: List of dicts with 'key', 'data', and optional 'metadata'
                Example: [
                    {
                        'key': 'doc1-chunk0',
                        'data': {'float32': [0.1, 0.2, ...]},
                        'metadata': {'file': 'test.md', 'chunk': 0}
                    }
                ]
        """
        return self.client.put_vectors(
            vectorBucketName=bucket_name,
            indexName=index_name,
            vectors=vectors,
        )

    def delete_vectors(
        self,
        bucket_name: str,
        index_name: str,
        keys: list[str],
    ) -> dict[str, Any]:
        """Delete vectors by keys."""
        return self.client.delete_vectors(
            vectorBucketName=bucket_name,
            indexName=index_name,
            keys=keys,
        )

    def query_vectors(
        self,
        bucket_name: str,
        index_name: str,
        query_vector: list[float],
        top_k: int = 5,
        filter_expression: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Query for similar vectors.

        Returns:
            List of matches with 'key', 'score', and 'metadata'
        """
        params = {
            "vectorBucketName": bucket_name,
            "indexName": index_name,
            "queryVector": {"float32": query_vector},
            "topK": top_k,
        }

        if filter_expression:
            params["filter"] = filter_expression

        response = self.client.query_vectors(**params)
        return response.get("vectors", [])
```

### Batch Insertion

```python
def insert_chunks_batch(
    client: S3VectorsClient,
    bucket_name: str,
    index_name: str,
    chunks: list[Chunk],
    batch_size: int = 100,
) -> int:
    """Insert chunks in batches.

    S3 Vectors has limits on batch size, so we chunk the inserts.
    """
    inserted = 0

    for i in tqdm(range(0, len(chunks), batch_size), desc="Uploading"):
        batch = chunks[i:i + batch_size]

        vectors = [
            {
                "key": chunk.key,
                "data": {"float32": chunk.embedding},
                "metadata": {
                    "file_path": chunk.metadata.file_path,
                    "file_type": chunk.metadata.file_type,
                    "chunk_index": chunk.metadata.chunk_index,
                    "start_line": chunk.metadata.start_line,
                    "end_line": chunk.metadata.end_line,
                    "file_hash": chunk.metadata.file_hash,
                    "tags": chunk.metadata.tags,
                    "title": chunk.metadata.title,
                },
            }
            for chunk in batch
        ]

        client.put_vectors(bucket_name, index_name, vectors)
        inserted += len(batch)

    return inserted
```

## Incremental Indexing

### Change Detection

Use file hashes to detect changes and avoid re-indexing unchanged files:

```python
import hashlib
from pathlib import Path
import json


class IndexState:
    """Track indexed files and their hashes."""

    def __init__(self, state_file: Path):
        self.state_file = state_file
        self.state: dict[str, str] = {}  # file_path -> file_hash
        self._load()

    def _load(self) -> None:
        if self.state_file.exists():
            self.state = json.loads(self.state_file.read_text())

    def save(self) -> None:
        self.state_file.write_text(json.dumps(self.state, indent=2))

    def get_hash(self, file_path: str) -> str | None:
        return self.state.get(file_path)

    def set_hash(self, file_path: str, file_hash: str) -> None:
        self.state[file_path] = file_hash

    def remove(self, file_path: str) -> None:
        self.state.pop(file_path, None)


def compute_file_hash(file_path: Path) -> str:
    """Compute SHA256 hash of file content."""
    return hashlib.sha256(file_path.read_bytes()).hexdigest()


def get_files_to_index(
    glob_pattern: str,
    base_path: Path,
    state: IndexState,
) -> tuple[list[Path], list[Path], list[str]]:
    """Determine which files need indexing.

    Returns:
        Tuple of (new_files, changed_files, deleted_file_paths)
    """
    current_files = set(base_path.glob(glob_pattern))
    indexed_files = set(state.state.keys())

    new_files = []
    changed_files = []

    for file_path in current_files:
        rel_path = str(file_path.relative_to(base_path))
        current_hash = compute_file_hash(file_path)
        stored_hash = state.get_hash(rel_path)

        if stored_hash is None:
            new_files.append(file_path)
        elif stored_hash != current_hash:
            changed_files.append(file_path)

    # Find deleted files
    current_rel_paths = {str(f.relative_to(base_path)) for f in current_files}
    deleted = [f for f in indexed_files if f not in current_rel_paths]

    return new_files, changed_files, deleted
```

## Configuration

### Config File Structure

Store configuration in `~/.config/vector-rag-tool/config.yaml`:

```yaml
# Default settings
defaults:
  embedding_model: embeddinggemma
  ollama_url: http://localhost:11434
  aws_region: eu-central-1
  aws_profile: sandbox-ilionx-amf

# Store definitions (cached locally)
stores:
  obsidian-vault:
    bucket_name: obsidian-rag-obsidian-vault
    index_name: main
    created_at: "2024-12-04T19:30:00Z"

  python-projects:
    bucket_name: obsidian-rag-python-projects
    index_name: main
    created_at: "2024-12-04T20:00:00Z"

# Chunking overrides (optional)
chunking:
  markdown:
    chunk_size: 1200
    chunk_overlap: 250
```

### Environment Variables

```bash
# Override defaults via environment
OBSIDIAN_RAG_OLLAMA_URL=http://localhost:11434
OBSIDIAN_RAG_AWS_REGION=eu-central-1
OBSIDIAN_RAG_AWS_PROFILE=sandbox-ilionx-amf
```

## Dependencies

### pyproject.toml

```toml
[project]
dependencies = [
    "click>=8.1.7",
    "boto3>=1.35.0",
    "ollama>=0.1.0",                    # Official Ollama package
    "tqdm>=4.66.0",
    "pyyaml>=6.0.0",
    "langchain-text-splitters>=0.2.0",
]
```

## Module Structure

```
vector_rag_tool/
├── __init__.py
├── cli.py                    # Click CLI entry point
├── commands/
│   ├── __init__.py
│   ├── store.py              # store create/delete/list/info
│   ├── index.py              # index command
│   ├── query.py              # query command
│   └── status.py             # status command
├── core/
│   ├── __init__.py
│   ├── embeddings.py         # OllamaEmbeddings class
│   ├── s3vectors.py          # S3VectorsClient class
│   ├── chunking.py           # ChunkingStrategy, splitters
│   ├── file_detector.py      # File type detection
│   └── models.py             # Dataclasses (Store, Chunk, etc.)
├── services/
│   ├── __init__.py
│   ├── store_manager.py      # Store CRUD operations
│   ├── indexer.py            # Indexing orchestration
│   └── querier.py            # Query orchestration
├── config.py                 # Configuration management
├── logging_config.py         # Logging setup
├── completion.py             # Shell completion
└── utils.py                  # Utilities
```

## Error Handling

### Validation Errors

Always provide actionable error messages:

```python
class ValidationError(Exception):
    """Raised when input validation fails."""

    def __init__(self, message: str, suggestion: str):
        self.message = message
        self.suggestion = suggestion
        super().__init__(f"{message}\n\nSuggestion: {suggestion}")


# Example usage
def validate_store_name(name: str) -> None:
    if not name:
        raise ValidationError(
            "Store name cannot be empty",
            "Provide a store name: vector-rag-tool store create <name>"
        )
    if not name.replace("-", "").replace("_", "").isalnum():
        raise ValidationError(
            f"Invalid store name: {name}",
            "Store names can only contain letters, numbers, hyphens, and underscores"
        )
```

## Testing Strategy

### Unit Tests

```python
# tests/test_chunking.py
def test_markdown_chunking():
    splitter = ChunkingStrategy.get_splitter("markdown")
    content = "# Title\n\nParagraph one.\n\n## Section\n\nParagraph two."
    chunks = splitter.split_text(content)
    assert len(chunks) >= 1

def test_python_chunking():
    splitter = ChunkingStrategy.get_splitter("python")
    content = "def hello():\n    print('world')\n\ndef goodbye():\n    print('bye')"
    chunks = splitter.split_text(content)
    assert len(chunks) >= 1
```

### Integration Tests

```python
# tests/test_integration.py
@pytest.mark.integration
def test_full_index_query_flow(tmp_path):
    # Create test files
    (tmp_path / "test.md").write_text("# Test\n\nHello world content.")

    # Index
    result = runner.invoke(cli, ["index", "**/*.md", "--store", "test-store"])
    assert result.exit_code == 0

    # Query
    result = runner.invoke(cli, ["query", "hello", "--store", "test-store", "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert len(data["results"]) > 0
```

## Summary

| Component | Technology | Purpose |
|-----------|------------|---------|
| CLI | Click | Command-line interface |
| Embeddings | Ollama embeddinggemma | Local 768-dim vectors |
| Vector Store | AWS S3 Vectors | Managed vector storage |
| Chunking | LangChain text-splitters | Language-aware splitting |
| Config | YAML + env vars | Settings management |

### Key Design Decisions

1. **Store isolation**: Each store = separate S3 Vector bucket + index
2. **Glob-based indexing**: Flexible file selection patterns
3. **Language-aware chunking**: Preserve code structure
4. **Incremental indexing**: Hash-based change detection
5. **JSON output**: Machine-readable for piping/scripting
6. **Actionable errors**: Help users/agents recover from failures
