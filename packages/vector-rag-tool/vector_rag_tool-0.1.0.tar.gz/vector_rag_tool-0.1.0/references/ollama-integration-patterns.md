# Ollama Integration Patterns

Reference implementation from `ollama-deepseek-ocr-tool`.

## Key Finding: Use `ollama` Python Package

Instead of raw HTTP requests, use the official `ollama` Python package for cleaner integration.

```toml
# pyproject.toml
dependencies = [
    "ollama>=0.1.0",
]
```

## API Comparison

### Option A: Raw HTTP Requests (Design Document)

```python
import requests

def get_embedding(text: str) -> list[float]:
    response = requests.post(
        "http://localhost:11434/api/embed",
        json={"model": "embeddinggemma", "input": text}
    )
    return response.json()["embeddings"][0]
```

### Option B: Official Ollama Package (Recommended)

```python
import ollama

def get_embedding(text: str) -> list[float]:
    response = ollama.embed(model="embeddinggemma", input=text)
    return response["embeddings"][0]

def get_embeddings_batch(texts: list[str]) -> list[list[float]]:
    response = ollama.embed(model="embeddinggemma", input=texts)
    return response["embeddings"]
```

## Why Use the `ollama` Package

| Aspect | requests | ollama |
|--------|----------|--------|
| Type hints | None | Built-in |
| Error handling | Manual HTTP codes | Typed exceptions |
| Connection management | Manual | Automatic |
| Streaming support | Manual parsing | Built-in |
| Code clarity | More boilerplate | Cleaner |

## Implementation Reference

From `ollama-deepseek-ocr-tool/ocr_processor.py`:

```python
import ollama

try:
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt, "images": [encoded_image]}],
    )
    extracted_text: str = response["message"]["content"]
except Exception as e:
    raise RuntimeError(f"OCR extraction failed: {e}") from e
```

## Embedding-Specific Pattern

For vector-rag-tool, adapt the pattern for embeddings:

```python
"""Ollama embedding integration for vector-rag-tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import ollama
from tqdm import tqdm

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
            # Get dimension from a test embedding
            test_embedding = self.embed_text("test")
            self._dimension = len(test_embedding)
        return self._dimension

    def embed_text(self, text: str) -> list[float]:
        """Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            768-dimensional embedding vector

        Raises:
            RuntimeError: If embedding generation fails
        """
        logger.debug("Embedding text: %s...", text[:50])

        try:
            response = ollama.embed(model=self.model, input=text)
            embedding: list[float] = response["embeddings"][0]
            logger.debug("Generated embedding with %d dimensions", len(embedding))
            return embedding

        except Exception as e:
            logger.error("Embedding failed for text: %s...", text[:50])
            logger.debug("Full traceback:", exc_info=True)
            raise RuntimeError(f"Embedding generation failed: {e}") from e

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed

        Returns:
            List of 768-dimensional embedding vectors

        Raises:
            RuntimeError: If embedding generation fails
        """
        logger.debug("Embedding batch of %d texts", len(texts))

        try:
            response = ollama.embed(model=self.model, input=texts)
            embeddings: list[list[float]] = response["embeddings"]
            logger.debug("Generated %d embeddings", len(embeddings))
            return embeddings

        except Exception as e:
            logger.error("Batch embedding failed for %d texts", len(texts))
            logger.debug("Full traceback:", exc_info=True)
            raise RuntimeError(f"Batch embedding generation failed: {e}") from e


def embed_chunks_with_progress(
    chunks: list[dict],
    embeddings: OllamaEmbeddings,
    batch_size: int = 10,
) -> list[dict]:
    """Embed chunks in batches with progress bar.

    Args:
        chunks: List of chunk dicts with 'content' key
        embeddings: OllamaEmbeddings instance
        batch_size: Number of texts per batch

    Returns:
        Chunks with 'embedding' key added
    """
    result = []

    for i in tqdm(range(0, len(chunks), batch_size), desc="Embedding"):
        batch = chunks[i : i + batch_size]
        texts = [chunk["content"] for chunk in batch]
        vectors = embeddings.embed_batch(texts)

        for chunk, vector in zip(batch, vectors):
            chunk["embedding"] = vector
            result.append(chunk)

    return result
```

## Prompt Templates for EmbeddingGemma

From the model card research, use these prompt templates:

```python
def format_query(query: str) -> str:
    """Format query for optimal retrieval."""
    return f"task: search result | query: {query}"

def format_document(content: str, title: str | None = None) -> str:
    """Format document for embedding."""
    title_part = title if title else "none"
    return f"title: {title_part} | text: {content}"
```

## Error Handling Pattern

From ollama-deepseek-ocr-tool:

```python
try:
    # Ollama operation
    result = ollama.embed(...)
except Exception as e:
    logger.error("Operation failed: %s", str(e))
    logger.debug("Full traceback:", exc_info=True)
    raise RuntimeError(f"Descriptive error: {e}") from e
```

## CLI Integration Pattern

```python
@click.command()
@click.argument("glob_pattern")
@click.option("-v", "--verbose", count=True)
def main(glob_pattern: str, verbose: int) -> None:
    setup_logging(verbose)

    try:
        # Business logic
        pass
    except RuntimeError as e:
        click.echo(f"✗ Error: {e}", err=True)
        click.echo("\nTroubleshooting:", err=True)
        click.echo("  - Ensure Ollama is running: ollama serve", err=True)
        click.echo("  - Verify model is installed: ollama pull embeddinggemma", err=True)
        raise click.Abort()
```

## Updated Dependencies

Update `pyproject.toml`:

```toml
dependencies = [
    "click>=8.1.7",
    "boto3>=1.35.0",
    "ollama>=0.1.0",       # Official Ollama package (instead of requests)
    "tqdm>=4.66.0",
    "pyyaml>=6.0.0",
    "langchain-text-splitters>=0.2.0",
]
```

## Summary

| Pattern | Source | Apply To |
|---------|--------|----------|
| `ollama` package | ollama-deepseek-ocr-tool | Use instead of requests |
| tqdm progress | ollama-deepseek-ocr-tool | Batch embedding |
| Error handling | ollama-deepseek-ocr-tool | All Ollama calls |
| Glob patterns | ollama-deepseek-ocr-tool | File discovery |
| Logging setup | ollama-deepseek-ocr-tool | CLI verbosity |
