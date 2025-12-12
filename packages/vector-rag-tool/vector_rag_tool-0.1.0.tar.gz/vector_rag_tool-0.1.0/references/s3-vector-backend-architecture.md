# S3 Vectors Backend Architecture

## Overview

AWS S3 Vectors is a serverless vector storage service that provides scalable similarity search without infrastructure management. This document explains how `vector-rag-tool` integrates with S3 Vectors.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        vector-rag-tool                          │
├─────────────────────────────────────────────────────────────────┤
│  S3VectorsBackend (s3vectors_backend.py)                        │
│  ├── boto3 S3Vectors client                                     │
│  ├── Vector bucket management                                   │
│  └── Index operations (CRUD + query)                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS (AWS SDK)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AWS S3 Vectors Service                        │
├─────────────────────────────────────────────────────────────────┤
│  Vector Bucket: dnvriend-vectors                                │
│  ├── Index: vector-rag-tool                                     │
│  │   ├── dimension: 768                                         │
│  │   ├── dataType: float32                                      │
│  │   ├── distanceMetric: cosine                                 │
│  │   └── vectors: [{key, embedding, metadata}, ...]             │
│  └── Index: another-store                                       │
└─────────────────────────────────────────────────────────────────┘
```

## Key Concepts

### Vector Bucket

A container for vector indexes. Similar to an S3 bucket but specifically for vector data.

```bash
# Create a vector bucket
aws s3vectors create-vector-bucket --vector-bucket-name my-vectors

# List vector buckets
aws s3vectors list-vector-buckets
```

### Index

A collection of vectors within a vector bucket. Each index has:
- **dimension**: Vector size (768 for embeddinggemma)
- **dataType**: `float32` (required)
- **distanceMetric**: `cosine`, `euclidean`, or `dotproduct`

```bash
# Create an index
aws s3vectors create-index \
    --vector-bucket-name my-vectors \
    --index-name my-store \
    --data-type float32 \
    --dimension 768 \
    --distance-metric cosine
```

### Vector

A single entry in an index containing:
- **key**: Unique identifier (chunk ID)
- **vector**: Float32 array of embeddings
- **metadata**: JSON object with source file, line numbers, content, etc.

## Implementation Details

### Backend Class

```python
class S3VectorsBackend(VectorBackend):
    def __init__(self, bucket_name, region, profile):
        self.client = boto3.client('s3vectors', region_name=region)
        self.bucket_name = bucket_name
```

### Store Operations

| Operation | API Call | Notes |
|-----------|----------|-------|
| create_store | `create_index` | Requires dataType="float32" |
| delete_store | `delete_index` | Removes all vectors |
| list_stores | `list_indexes` | Returns index names |
| store_exists | `list_indexes` + check | No direct exists API |
| get_store_info | `get_index` | Response nested under "index" |

### Vector Operations

| Operation | API Call | Notes |
|-----------|----------|-------|
| put_vectors | `put_vectors` | Batch insert with metadata |
| delete_vectors | `delete_vectors` | By key list |
| query | `query_vectors` | Returns distance, not score |

### Query Response Handling

S3 Vectors returns **distance** (lower is better), but RAG expects **score** (higher is better):

```python
# Convert distance to score
distance = v.get("distance", 0.0)
score = 1.0 / (1.0 + distance)  # Higher score = more similar
```

## Data Flow

### Indexing

```
1. Files → Chunking (1500 chars)
2. Chunks → Ollama Embedding (768-dim vectors)
3. Vectors + Metadata → S3 Vectors put_vectors API
```

### Querying

```
1. Query text → Ollama Embedding (768-dim vector)
2. Query vector → S3 Vectors query_vectors API
3. Results (with distance) → Convert to score
4. Return ranked chunks with metadata
```

## Configuration

```bash
# Index to S3 Vectors
vector-rag-tool index "**/*.py" --store my-store \
    --bucket my-vectors --region eu-central-1 --profile aws-profile

# Query from S3 Vectors
vector-rag-tool query "search term" --store my-store \
    --bucket my-vectors --region eu-central-1
```

## Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| Query latency | 200-500ms | Network overhead |
| Index throughput | ~2.5 batches/sec | API rate limits |
| Max vectors/index | Millions | Serverless scaling |
| Cost | Pay per request | No idle costs |

## Limitations

1. **No vector count**: `get_index` doesn't return vector count
2. **No index size**: Storage size not exposed
3. **Distance only**: Must convert to similarity score
4. **Eventual consistency**: Recently added vectors may not appear immediately

## Error Handling

| Exception | Meaning | Handling |
|-----------|---------|----------|
| ConflictException | Resource already exists | Ignore for idempotent creates |
| NotFoundException | Bucket/index not found | Create or raise error |
| ValidationException | Invalid parameters | Check dimension, dataType |

## References

- [AWS S3 Vectors Documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html)
- [boto3 S3Vectors Client](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors.html)
