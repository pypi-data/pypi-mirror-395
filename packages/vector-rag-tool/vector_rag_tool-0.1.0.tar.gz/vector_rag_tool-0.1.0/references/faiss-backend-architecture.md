# FAISS Backend Architecture

## Overview

FAISS (Facebook AI Similarity Search) is an open-source library for efficient similarity search of dense vectors. This document explains how `vector-rag-tool` uses FAISS for local vector storage.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        vector-rag-tool                          │
├─────────────────────────────────────────────────────────────────┤
│  FAISSBackend (faiss_backend.py)                                │
│  ├── faiss.IndexFlatIP (Inner Product index)                    │
│  ├── JSON metadata sidecar files                                │
│  └── File-based persistence                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ File I/O
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              ~/.config/vector-rag-tool/stores/                   │
├─────────────────────────────────────────────────────────────────┤
│  vector-rag-tool.faiss      # Binary FAISS index file           │
│  vector-rag-tool.meta.json  # Metadata (keys, content, etc.)    │
│  another-store.faiss                                            │
│  another-store.meta.json                                        │
└─────────────────────────────────────────────────────────────────┘
```

## Key Concepts

### FAISS Index Types

FAISS offers many index types. We use `IndexFlatIP` (Flat Inner Product):

| Index Type | Description | Use Case |
|------------|-------------|----------|
| **IndexFlatIP** | Exact search with inner product | Small-medium datasets, cosine similarity |
| IndexFlatL2 | Exact search with L2 distance | Euclidean distance |
| IndexIVFFlat | Inverted file with flat quantization | Large datasets |
| IndexHNSW | Hierarchical Navigable Small World | Very large datasets |

### Why IndexFlatIP?

1. **Cosine similarity**: With L2-normalized vectors, inner product equals cosine similarity
2. **Exact results**: No approximation, always finds true nearest neighbors
3. **Simple**: No training required, works out of the box
4. **Fast enough**: For <1M vectors, exact search is fast (~100ms)

### Vector Normalization

For cosine similarity with IndexFlatIP, vectors must be L2-normalized:

```python
# Normalize vectors before adding to index
faiss.normalize_L2(embeddings)  # In-place normalization

# After normalization:
# - ||v|| = 1 (unit length)
# - inner_product(a, b) = cosine_similarity(a, b)
```

## Storage Format

### FAISS Index File (*.faiss)

Binary file containing:
- Index type metadata
- Vector data (float32 arrays)
- Internal FAISS structures

```python
# Save index
faiss.write_index(index, "store.faiss")

# Load index
index = faiss.read_index("store.faiss")
```

### Metadata JSON (*.meta.json)

JSON sidecar file containing:

```json
{
  "dimension": 768,
  "next_id": 269,
  "vectors": {
    "chunk_id_abc123": {
      "index_id": 0,
      "metadata": {
        "source_file": "/path/to/file.py",
        "line_start": 1,
        "line_end": 25,
        "chunk_index": 0,
        "total_chunks": 5,
        "tags": ["python"],
        "content_preview": "def main():\n    ..."
      }
    }
  }
}
```

## Implementation Details

### Backend Class

```python
class FAISSBackend(VectorBackend):
    def __init__(self):
        STORES_DIR.mkdir(parents=True, exist_ok=True)

    def _index_path(self, store_name: str) -> Path:
        return STORES_DIR / f"{store_name}.faiss"

    def _meta_path(self, store_name: str) -> Path:
        return STORES_DIR / f"{store_name}.meta.json"
```

### Store Operations

| Operation | Implementation | Notes |
|-----------|---------------|-------|
| create_store | `faiss.IndexFlatIP(dim)` + save | Creates empty index |
| delete_store | Delete .faiss and .meta.json | Removes all data |
| list_stores | Glob *.faiss files | Returns store names |
| store_exists | Check file exists | Fast file check |
| get_store_info | Load index + metadata | Returns vector count, size |

### Vector Operations

| Operation | Implementation | Notes |
|-----------|---------------|-------|
| put_vectors | `index.add()` + update metadata | Batch insert |
| delete_vectors | Remove from metadata only | FAISS doesn't support deletion |
| query | `index.search()` + map to keys | Returns scores directly |

### Query Implementation

```python
def query(self, store_name, query_vector, top_k):
    # Load index and metadata
    index = self._load_index(store_name)
    metadata = self._load_metadata(store_name)

    # Normalize query vector
    query = np.array([query_vector], dtype=np.float32)
    faiss.normalize_L2(query)

    # Search (returns scores and indices)
    scores, indices = index.search(query, top_k)

    # Map indices back to keys using metadata
    id_to_key = {v["index_id"]: k for k, v in metadata["vectors"].items()}

    results = []
    for score, idx in zip(scores[0], indices[0]):
        key = id_to_key.get(idx)
        if key:
            results.append(VectorQueryResult(
                key=key,
                score=float(score),
                metadata=metadata["vectors"][key]["metadata"],
                content=metadata["vectors"][key]["metadata"].get("content_preview"),
            ))

    return results
```

## Data Flow

### Indexing

```
1. Files → Chunking (1500 chars)
2. Chunks → Ollama Embedding (768-dim vectors)
3. Vectors → L2 normalize → faiss.IndexFlatIP.add()
4. Metadata → JSON file
5. Index → .faiss file
```

### Querying

```
1. Query text → Ollama Embedding (768-dim vector)
2. Query vector → L2 normalize
3. index.search(query, top_k) → (scores, indices)
4. Map indices to keys via metadata
5. Return ranked chunks with content
```

## Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| Query latency | ~10ms | After embedding (~100ms total) |
| Index throughput | ~400 batches/sec | Limited by disk I/O |
| Memory usage | ~4 bytes × dim × vectors | 768D × 1000 vectors ≈ 3MB |
| Disk usage | Similar to memory | Binary format |

### Scaling Considerations

| Vector Count | Query Time | Recommendation |
|--------------|------------|----------------|
| < 10,000 | < 10ms | IndexFlatIP (current) |
| 10,000 - 100,000 | 10-100ms | IndexFlatIP still fine |
| 100,000 - 1M | 100ms-1s | Consider IndexIVFFlat |
| > 1M | > 1s | Use IndexHNSW or S3 Vectors |

## Limitations

1. **No native deletion**: FAISS IndexFlatIP doesn't support deletion
   - Workaround: Remove from metadata, rebuild index periodically

2. **Memory-mapped only**: Entire index loaded into memory
   - For large indexes, consider IndexIVF* variants

3. **Single-threaded search**: Default search is single-threaded
   - Can enable multi-threading with `faiss.omp_set_num_threads(n)`

4. **No metadata in index**: Metadata stored separately in JSON
   - Must keep .faiss and .meta.json in sync

## File Locations

```
~/.config/vector-rag-tool/stores/
├── vector-rag-tool.faiss      # 0.79MB (268 vectors)
├── vector-rag-tool.meta.json  # ~500KB (metadata + content)
├── test-store.faiss
└── test-store.meta.json
```

## References

- [FAISS GitHub](https://github.com/facebookresearch/faiss)
- [FAISS Wiki](https://github.com/facebookresearch/faiss/wiki)
- [Choosing an Index](https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index)
