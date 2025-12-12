# Ollama Embedding Architecture

## Overview

Ollama is a local LLM runtime that also provides embedding models. This document explains how `vector-rag-tool` uses Ollama for generating vector embeddings.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        vector-rag-tool                          │
├─────────────────────────────────────────────────────────────────┤
│  OllamaEmbeddings (embeddings.py)                               │
│  ├── ollama.embed() API                                         │
│  ├── Query formatting (task: search result)                     │
│  └── Document formatting (title: ... | text: ...)               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP POST http://localhost:11434/api/embed
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Ollama Server                               │
├─────────────────────────────────────────────────────────────────┤
│  Model: embeddinggemma                                          │
│  ├── Input: text string(s)                                      │
│  ├── Output: 768-dimensional float32 vectors                    │
│  └── Batch support: Multiple texts per request                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ GPU/CPU inference
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Hardware (Apple Silicon)                      │
├─────────────────────────────────────────────────────────────────┤
│  M4 GPU: Metal Performance Shaders                              │
│  Memory: Unified memory architecture                            │
│  ~5-7 seconds per batch of 32 texts                             │
└─────────────────────────────────────────────────────────────────┘
```

## Key Concepts

### What are Embeddings?

Embeddings are dense vector representations of text that capture semantic meaning:

```
"machine learning" → [0.12, -0.34, 0.56, ..., 0.78]  # 768 floats
"deep learning"    → [0.11, -0.33, 0.55, ..., 0.77]  # Similar vector
"banana smoothie"  → [-0.45, 0.22, -0.11, ..., 0.03] # Different vector
```

Similar texts produce similar vectors (high cosine similarity).

### Embedding Model: embeddinggemma

| Property | Value |
|----------|-------|
| Model | embeddinggemma |
| Dimension | 768 |
| Max tokens | ~8192 |
| Size | ~500MB |
| Speed | ~5-7s per 32 texts |

```bash
# Install the model
ollama pull embeddinggemma

# Verify installation
ollama list
```

### Why embeddinggemma?

1. **Small footprint**: 500MB vs 4GB+ for larger models
2. **Fast inference**: Optimized for Apple Silicon
3. **Good quality**: Comparable to OpenAI ada-002 for code/docs
4. **768 dimensions**: Standard size, good balance of quality/efficiency

## Text Formatting

### Query Formatting

For search queries, we use a specific format to optimize retrieval:

```python
def embed_query(self, query: str) -> list[float]:
    formatted_query = f"task: search result | query: {query}"
    return self.embed_text(formatted_query)
```

Example:
```
Input:  "how does authentication work"
Format: "task: search result | query: how does authentication work"
```

### Document Formatting

For documents/code, we include title context:

```python
def embed_document(self, content: str, title: str | None = None) -> list[float]:
    title_part = title if title else "none"
    formatted_content = f"title: {title_part} | text: {content}"
    return self.embed_text(formatted_content)
```

Example:
```
Input:  content="def main(): ...", title="cli.py"
Format: "title: cli.py | text: def main(): ..."
```

## Implementation Details

### OllamaEmbeddings Class

```python
class OllamaEmbeddings:
    def __init__(self, model: str = "embeddinggemma", host: str | None = None):
        self.model = model
        self.host = host  # Default: http://localhost:11434
        self._client = ollama.Client(host=host) if host else None

    @property
    def dimension(self) -> int:
        # Lazy evaluation - get dimension from test embedding
        if self._dimension is None:
            test_embedding = self.embed_text("test")
            self._dimension = len(test_embedding)
        return self._dimension
```

### Single Text Embedding

```python
def embed_text(self, text: str) -> list[float]:
    response = ollama.embed(model=self.model, input=text)
    return response["embeddings"][0]
```

### Batch Embedding

```python
def embed_batch(self, texts: list[str]) -> list[list[float]]:
    response = ollama.embed(model=self.model, input=texts)
    return response["embeddings"]
```

## API Details

### Ollama Embed API

**Endpoint**: `POST http://localhost:11434/api/embed`

**Request**:
```json
{
  "model": "embeddinggemma",
  "input": ["text 1", "text 2", "text 3"]
}
```

**Response**:
```json
{
  "embeddings": [
    [0.12, -0.34, 0.56, ...],  // 768 floats
    [0.11, -0.33, 0.55, ...],
    [0.13, -0.35, 0.57, ...]
  ]
}
```

## Performance Characteristics

### Throughput

| Batch Size | Time | Throughput |
|------------|------|------------|
| 1 text | ~200ms | 5 texts/sec |
| 32 texts | ~5-7s | 5-6 texts/sec |
| 64 texts | ~10-14s | 5-6 texts/sec |

Throughput is roughly constant regardless of batch size due to model loading overhead.

### Bottleneck Analysis

```
Total indexing time for 35 files, 269 chunks: ~63 seconds

Breakdown:
- File processing: <1s (negligible)
- Embedding generation: ~62s (98% of time) ← BOTTLENECK
- Vector storage: <1s (negligible)
```

### Parallelism Limitations

Ollama does **not** efficiently parallelize embedding requests:

```
OLLAMA_NUM_PARALLEL only affects text generation, not embeddings.
Multiple concurrent embedding requests are queued, not parallelized.
```

**Workarounds**:
1. Increase batch size (marginal improvement)
2. Run multiple Ollama instances on different ports
3. Use a different embedding backend (sentence-transformers)

## Data Flow

### Indexing Flow

```
1. Chunk text (1500 chars max)
2. Format: "title: {filename} | text: {content}"
3. Batch chunks (32 per request)
4. POST to Ollama /api/embed
5. Receive 768-dim vectors
6. Store vectors in FAISS/S3
```

### Query Flow

```
1. User query: "how does X work"
2. Format: "task: search result | query: how does X work"
3. POST to Ollama /api/embed (single text)
4. Receive 768-dim vector
5. Search in FAISS/S3 for similar vectors
6. Return top-k results
```

## Configuration

### Environment Variables

```bash
# Custom Ollama host
OLLAMA_HOST=http://192.168.1.100:11434

# Number of parallel requests (text generation only)
OLLAMA_NUM_PARALLEL=4
```

### CLI Options

```bash
# Use default (localhost:11434)
vector-rag-tool index "**/*.py" --store my-store

# Custom host (not yet implemented in CLI)
# Would require --ollama-host option
```

## Embedding Quality

### Semantic Similarity Examples

| Query | Top Result | Score | Correct? |
|-------|------------|-------|----------|
| "chunking strategy" | chunking.py | 0.517 | ✅ |
| "FAISS backend" | faiss_backend.py | 0.601 | ✅ |
| "S3 vectors AWS" | s3vectors_backend.py | 0.730 | ✅ |
| "CLI commands" | cli.py | 0.443 | ✅ |

### Score Interpretation

| Score Range | Meaning |
|-------------|---------|
| > 0.7 | Strong match (exact topic) |
| 0.5 - 0.7 | Good match (related topic) |
| 0.3 - 0.5 | Weak match (tangentially related) |
| < 0.3 | Poor match (likely irrelevant) |

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Connection refused | Ollama not running | `ollama serve` |
| Model not found | Model not pulled | `ollama pull embeddinggemma` |
| Slow embedding | Cold start | First request loads model |
| Out of memory | Model too large | Use smaller model |

### Verifying Ollama

```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Test embedding
curl -X POST http://localhost:11434/api/embed \
  -d '{"model": "embeddinggemma", "input": "test"}'
```

## Alternative Models

| Model | Dimension | Size | Quality |
|-------|-----------|------|---------|
| embeddinggemma | 768 | 500MB | Good |
| nomic-embed-text | 768 | 274MB | Good |
| mxbai-embed-large | 1024 | 670MB | Better |
| all-minilm | 384 | 45MB | Fast but lower quality |

To use a different model:

```python
embeddings = OllamaEmbeddings(model="nomic-embed-text")
```

## References

- [Ollama Documentation](https://ollama.ai/docs)
- [Ollama API Reference](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Embedding Models on Ollama](https://ollama.ai/library?q=embed)
