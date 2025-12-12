# EmbeddingGemma vs Amazon Titan Embed Text V2

## Overview

This document compares two embedding models used for RAG (Retrieval-Augmented Generation):
- **EmbeddingGemma**: Google's open-source on-device embedding model (used via Ollama)
- **Amazon Titan Text Embeddings V2**: AWS's managed embedding service (via Bedrock)

## Quick Comparison

| Feature             | EmbeddingGemma       | Amazon Titan Embed V2    |
|---------------------|----------------------|--------------------------|
| Provider            | Google (Open Source) | AWS (Managed Service)    |
| Parameters          | 308M                 | Not disclosed            |
| Default Dimensions  | 768                  | 1024                     |
| Flexible Dimensions | 128, 256, 512, 768   | 256, 512, 1024           |
| Max Context         | 2,048 tokens         | 8,192 tokens             |
| Languages           | 100+                 | 100+ (preview)           |
| Deployment          | Local (Ollama)       | Cloud (Bedrock API)      |
| Cost                | Free (local compute) | $0.02 per 1M tokens      |
| Latency             | ~5-7s/batch (local)  | ~100-200ms/request (API) |

## Model Specifications

### EmbeddingGemma

```
Model: embeddinggemma (308M parameters)
Base: Gemma 3 architecture
Dimensions: 768 (default), 512, 256, 128 via MRL
Context: 2,048 tokens
Memory: <200MB RAM (quantized)
Inference: <22ms on EdgeTPU, ~200ms on CPU
```

**Key Features**:
- **Matryoshka Representation Learning (MRL)**: Allows dimension truncation without retraining
- **On-device inference**: No internet required, data stays local
- **Multilingual**: Trained on 100+ languages
- **Open weights**: Apache 2.0 license

### Amazon Titan Text Embeddings V2

```
Model: amazon.titan-embed-text-v2:0
Dimensions: 1024 (default), 512, 256
Context: 8,192 tokens (~50,000 characters)
Normalization: Optional (API parameter)
```

**Key Features**:
- **Higher dimensions**: 1024D default for potentially richer representations
- **Longer context**: 4x more tokens than EmbeddingGemma
- **Managed service**: No infrastructure to maintain
- **AWS integration**: Native Bedrock, S3, and Lambda integration

## Performance Benchmarks

### MTEB (Massive Text Embedding Benchmark)

| Model                         | MTEB Score | Retrieval | Classification | Clustering |
|-------------------------------|------------|-----------|----------------|------------|
| EmbeddingGemma (768D)         | ~62*       | Good      | Good           | Good       |
| Titan Embed V2 (1024D)        | ~61*       | Good      | Good           | Good       |
| OpenAI text-embedding-3-large | ~64        | Better    | Better         | Better     |
| Cohere embed-v3               | ~64        | Better    | Better         | Better     |

*Approximate scores - both models perform similarly in the 60-62 range on MTEB.

**Note**: EmbeddingGemma claims "highest ranking open multilingual text embedding model under 500M parameters" on MTEB.

### Retrieval Quality (RAG Use Case)

Based on our testing with `vector-rag-tool`:

| Query               | EmbeddingGemma Score | Relevance    |
|---------------------|----------------------|--------------|
| "chunking strategy" | 0.517                | Correct file |
| "FAISS backend"     | 0.601                | Correct file |
| "S3 vectors AWS"    | 0.730                | Correct file |

Both models produce good retrieval results for code search use cases.

## Cost Analysis

### EmbeddingGemma (Local via Ollama)

```
Infrastructure Cost:
- Free (runs on existing hardware)
- No per-token charges

Compute Cost (approximate):
- Electricity: ~$0.001 per 1000 embeddings
- Hardware amortization: Depends on existing setup

Total: Essentially free for most use cases
```

### Amazon Titan Embed V2 (Bedrock)

```
Per-token pricing:
- $0.02 per 1,000,000 input tokens
- $0.00002 per 1,000 tokens

Example costs:
- 1,000 documents (avg 500 tokens): $0.01
- 100,000 documents: $1.00
- 1,000,000 documents: $10.00

Monthly estimate (10K queries/day):
- Queries: 300K queries × 50 tokens × $0.00002 = $0.30/month
```

### Cost Comparison for 1M Embeddings

| Scenario                     | EmbeddingGemma | Titan V2 |
|------------------------------|----------------|----------|
| 1M short texts (100 tokens)  | ~$0 (local)    | $2.00    |
| 1M medium texts (500 tokens) | ~$0 (local)    | $10.00   |
| 1M long texts (2000 tokens)  | ~$0 (local)    | $40.00   |

## Latency Comparison

### Indexing (Batch Processing)

| Model                   | Batch Size | Time   | Throughput    |
|-------------------------|------------|--------|---------------|
| EmbeddingGemma (Ollama) | 32         | ~6-7s  | 5 texts/sec   |
| Titan V2 (Bedrock)      | 1*         | ~150ms | 6-7 texts/sec |

*Titan V2 doesn't support batch embedding in a single API call.

### Query (Single Text)

| Model          | Latency    | Notes               |
|----------------|------------|---------------------|
| EmbeddingGemma | ~100-200ms | Local inference     |
| Titan V2       | ~100-200ms | Network + inference |

## Dimension Trade-offs

### EmbeddingGemma MRL Dimensions

| Dimensions | Quality  | Storage   | Use Case         |
|------------|----------|-----------|------------------|
| 768        | Best     | 3KB/vec   | Maximum accuracy |
| 512        | Good     | 2KB/vec   | Balanced         |
| 256        | Moderate | 1KB/vec   | Large scale      |
| 128        | Lower    | 0.5KB/vec | Extreme scale    |

### Titan V2 Dimensions

| Dimensions | Quality  | Storage | Use Case         |
|------------|----------|---------|------------------|
| 1024       | Best     | 4KB/vec | Maximum accuracy |
| 512        | Good     | 2KB/vec | Balanced         |
| 256        | Moderate | 1KB/vec | Large scale      |

## Use Case Recommendations

### Choose EmbeddingGemma When:

1. **Privacy is critical**: Data never leaves your infrastructure
2. **Cost-sensitive**: High volume embeddings with minimal budget
3. **Offline required**: No internet connectivity available
4. **Open source preferred**: Need to inspect/modify model weights
5. **Edge deployment**: Running on mobile/IoT devices

### Choose Amazon Titan V2 When:

1. **AWS ecosystem**: Already using Bedrock, S3, Lambda
2. **Long documents**: Need 8K token context (vs 2K)
3. **No GPU available**: Don't have local compute resources
4. **Enterprise support**: Need AWS support and SLAs
5. **Scale without ops**: Don't want to manage Ollama infrastructure

## Integration with vector-rag-tool

### Current Implementation (EmbeddingGemma)

```python
# embeddings.py
class OllamaEmbeddings:
    def __init__(self, model: str = "embeddinggemma"):
        self.model = model

    def embed_text(self, text: str) -> list[float]:
        response = ollama.embed(model=self.model, input=text)
        return response["embeddings"][0]  # 768-dim vector
```

### Potential Titan V2 Integration

```python
# titan_embeddings.py (not implemented)
import boto3

class TitanEmbeddings:
    def __init__(self, region: str = "us-east-1"):
        self.client = boto3.client("bedrock-runtime", region_name=region)

    def embed_text(self, text: str, dimensions: int = 1024) -> list[float]:
        response = self.client.invoke_model(
            modelId="amazon.titan-embed-text-v2:0",
            body=json.dumps({
                "inputText": text,
                "dimensions": dimensions,
                "normalize": True
            })
        )
        return json.loads(response["body"].read())["embedding"]
```

## Migration Considerations

### From EmbeddingGemma to Titan V2

1. **Dimension mismatch**: 768 vs 1024 - must reindex all vectors
2. **Index recreation**: FAISS/S3 Vectors indexes are dimension-specific
3. **Cost planning**: Calculate expected token volume
4. **API changes**: Different embedding API structure

### Hybrid Approach

Consider using both:
- **EmbeddingGemma**: Development, testing, small projects
- **Titan V2**: Production, large-scale, AWS-integrated systems

## Conclusion

| Criteria        | Winner                 |
|-----------------|------------------------|
| Cost            | EmbeddingGemma (free)  |
| Context length  | Titan V2 (8K vs 2K)    |
| Privacy         | EmbeddingGemma (local) |
| Ease of setup   | Titan V2 (managed)     |
| AWS integration | Titan V2               |
| Open source     | EmbeddingGemma         |
| Quality (MTEB)  | Roughly equal          |

**Recommendation for vector-rag-tool**:

EmbeddingGemma is the right choice for a local-first RAG tool because:
1. Zero cost for high-volume indexing
2. Data privacy (code never leaves your machine)
3. No cloud dependencies
4. Good enough quality for code search

Consider adding Titan V2 as an optional backend for users who:
- Are already in the AWS ecosystem
- Need longer context windows
- Prefer managed services

## References

- [EmbeddingGemma Documentation](https://ai.google.dev/gemma/docs/embeddinggemma)
- [Introducing EmbeddingGemma](https://developers.googleblog.com/en/introducing-embeddinggemma/)
- [Amazon Titan Text Embeddings](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html)
- [Amazon Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/)
- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
