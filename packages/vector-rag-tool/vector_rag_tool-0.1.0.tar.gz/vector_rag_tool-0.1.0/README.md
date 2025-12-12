<p align="center">
  <img src=".github/assets/logo.png" alt="vector-rag-tool logo" width="200">
</p>

# vector-rag-tool

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://github.com/python/mypy)
[![Built with Claude Code](https://img.shields.io/badge/Built_with-Claude_Code-5A67D8.svg)](https://www.anthropic.com/claude/code)

A CLI that provides local RAG with Ollama embeddings and FAISS vector search.

## Features

- Semantic search using vector embeddings
- Multiple file types: Python, Markdown, YAML, JSON
- Document support: PDF, Word, Excel, PowerPoint via markitdown
- Fast local search with FAISS (~100ms queries)
- Optional S3 Vectors backend for cloud scale
- Incremental indexing with file hash tracking
- Configurable chunk size and overlap

## Installation

**Prerequisites:**
- Python 3.13+
- [Ollama](https://ollama.ai/) with an embedding model

```bash
# Install Ollama and pull embedding model
brew install ollama
ollama pull embeddinggemma

# Install vector-rag-tool
git clone https://github.com/dnvriend/vector-rag-tool.git
cd vector-rag-tool
uv tool install .
```

## Usage

```bash
# Preview what would be indexed (dry-run is default)
vector-rag-tool index "**/*.py" --store my-project

# Index files
vector-rag-tool index "**/*.py" --store my-project --no-dry-run

# Index multiple file types
vector-rag-tool index "**/*.py" "**/*.md" --store my-project --no-dry-run

# Query for relevant code
vector-rag-tool query "how does authentication work" --store my-project

# Get full chunk content for RAG grounding
vector-rag-tool query "database connection" --store my-project --full

# JSON output for piping
vector-rag-tool query "logging" --store my-project --json

# Force reindex all files
vector-rag-tool index "**/*.py" --store my-project --force --no-dry-run

# Index documents (PDF, Word, Excel)
vector-rag-tool index "docs/**/*.pdf" --store my-docs --no-dry-run

# Use S3 Vectors backend
vector-rag-tool index "**/*.py" --store my-store \
    --bucket my-vectors-bucket --profile aws-profile --no-dry-run
```

### Store Management

```bash
vector-rag-tool store list              # List all stores
vector-rag-tool store create my-store   # Create empty store
vector-rag-tool store delete my-store --force  # Delete store
```

## Options

### Index Command

| Option | Description |
|--------|-------------|
| `--store` | Store name (required) |
| `--chunk-size` | Characters per chunk (default: 1500) |
| `--chunk-overlap` | Overlap between chunks (default: 200) |
| `--force` | Reindex all files, ignore cache |
| `--no-dry-run` | Actually index files |
| `--bucket` | S3 bucket for S3 Vectors backend |
| `--profile` | AWS profile for S3 backend |

### Query Command

| Option | Description |
|--------|-------------|
| `--store` | Store name (required) |
| `--top-k` | Number of results (default: 5) |
| `--full` | Return full chunk content |
| `--snippet-length` | Characters per snippet (default: 300) |
| `--json` | JSON output |
| `--stdin` | Read query from stdin |

### Global Options

| Option | Description |
|--------|-------------|
| `-v` | INFO level logging |
| `-vv` | DEBUG level logging |
| `-vvv` | TRACE level (library internals) |

## Development

```bash
make install        # Install dependencies
make test           # Run tests
make lint           # Run linting
make typecheck      # Type checking
make check          # All checks
make pipeline       # Full pipeline
```

## License

[MIT](LICENSE)

## Author

[Dennis Vriend](https://github.com/dnvriend)
