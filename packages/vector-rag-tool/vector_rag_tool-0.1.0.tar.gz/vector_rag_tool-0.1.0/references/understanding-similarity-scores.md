# Understanding Similarity Scores in Vector RAG

## Executive Summary

Cosine similarity scores in vector search measure geometric relationships between embeddings, not confidence or probability. A score of 0.5 indicates semantically related content and is completely normal for semantic search systems.

## Cosine Similarity vs Confidence Scores

### Key Distinction

| Score Type | Range | Meaning | Interpretation |
|------------|-------|---------|----------------|
| **Cosine Similarity** | -1 to +1 | Geometric angle between vectors in embedding space | Measures semantic relationship |
| **Confidence/Probability** | 0 to 1 | Model's certainty about a prediction | Measures prediction confidence |

### What Cosine Similarity Measures

Cosine similarity calculates the cosine of the angle between two vectors in high-dimensional space (768 dimensions for embeddinggemma):

```
similarity = cos(θ) = (A · B) / (||A|| × ||B||)
```

Where:
- `A` = query embedding vector
- `B` = document embedding vector
- `θ` = angle between the vectors

### Score Interpretation Guide

| Score Range | Angle | Relationship | Similarity Level | Use Case |
|-------------|-------|--------------|------------------|----------|
| **0.85 - 1.0** | 0° - 30° | Near-duplicate or exact match | `duplicate` | Deduplication, exact retrieval |
| **0.60 - 0.85** | 30° - 53° | Very similar with significant overlap | `very_similar` | Paraphrase detection, close variants |
| **0.30 - 0.60** | 53° - 73° | Semantically related (typical RAG results) | `related` | General semantic search, Q&A |
| **0.00 - 0.30** | 73° - 90° | Unrelated | `unrelated` | Noise, tangential content |
| **< 0.00** | 90° - 180° | Negatively correlated | `contradiction` | Antonyms, contradictions |

## Why RAG Scores Are "Low"

### Typical Score Ranges

**In production RAG systems, scores of 0.4-0.6 are common and expected** for several reasons:

1. **Asymmetric Query-Document Matching**
   - Query: Short, question-like text (2-10 words)
   - Document: Long, informational chunks (500-2000 characters)
   - Natural semantic distance between query and answer formats

2. **Embedding Model Characteristics**
   - Models are trained to spread representations across embedding space
   - Prevents clustering and enables better discrimination
   - Results in moderate similarity for related but distinct content

3. **Context Dilution**
   - Large chunks contain multiple concepts
   - Target information mixed with surrounding context
   - Reduces focused similarity to specific query terms

4. **Semantic Relationship, Not Duplication**
   - RAG retrieves *related* content, not *identical* content
   - A query about "foundation models" and a definition of foundation models are related but not identical
   - High scores (>0.8) typically indicate near-duplicates, not relevance

## Vector-RAG-Tool Implementation

### Similarity Level Enum

The tool provides a `SimilarityLevel` enum in `core/models.py` that automatically categorizes scores:

```python
class SimilarityLevel(str, Enum):
    DUPLICATE = "duplicate"          # >= 0.85
    VERY_SIMILAR = "very_similar"    # >= 0.60
    RELATED = "related"              # >= 0.30
    UNRELATED = "unrelated"          # >= 0.00
    CONTRADICTION = "contradiction"  # <  0.00

    @classmethod
    def from_score(cls, score: float) -> "SimilarityLevel":
        """Convert cosine similarity score to human-readable level."""
        # Automatic classification based on thresholds above
```

This enum is used in query results to provide human-readable similarity interpretation alongside numeric scores.

### Query Output Format

Both text and JSON output now include similarity levels:

**Text Output:**
```
1. Score: 0.540 (related: Semantically related topics)
   📄 /path/to/file.md:1-3
```

**JSON Output:**
```json
{
  "score": 0.5404907464981079,
  "similarity_level": "related",
  "similarity_description": "Semantically related topics",
  "file_path": "/path/to/file.md",
  ...
}
```

This format makes it easier for:
- **Humans**: Quick interpretation without memorizing score ranges
- **LLMs/Agents**: Can filter by `similarity_level` enum instead of numeric thresholds
- **Applications**: Can display user-friendly labels instead of raw scores

### Embedding Strategy

The tool uses **asymmetric embedding** formats (see `core/embeddings.py`):

**Query Format:**
```python
formatted_query = f"task: search result | query: {query}"
```

**Document Format:**
```python
formatted_content = f"title: {title} | text: {content}"
```

This asymmetry is intentional - it helps the model distinguish between queries and documents, but creates natural distance in the embedding space.

### Chunking Strategy

Default chunk sizes (see `core/chunking.py`):

| Content Type | Chunk Size | Overlap | Impact on Scores |
|--------------|------------|---------|------------------|
| Markdown | 1500 chars | 200 chars | Larger chunks → lower scores |
| Code | 1500 chars | 200 chars | Larger chunks → lower scores |
| YAML | 500 chars | 50 chars | Smaller chunks → higher scores |
| Generic | 1000 chars | 100 chars | Medium impact |

**Trade-off:** Smaller chunks yield higher scores but may lack context; larger chunks provide more context but yield lower scores.

### Example Query Analysis

Query: `"foundation models"`

Result: Score 0.54, content:
```
- **Foundation Models**: Very large models trained on vast data,
  adaptable for many tasks.
```

**Why 0.54 is correct:**
- Query is 2 words, document chunk is 329 characters
- Query seeks concept, document provides definition + context
- Embedded as search task vs document text (asymmetric)
- Content is semantically related but not duplicate text

## When to Be Concerned

### Red Flags

- **All scores < 0.3**: Poor query formulation or mismatched corpus
- **All scores > 0.9**: Possible data duplication or overfitting
- **High variance (0.2 to 0.9)**: Inconsistent chunking or mixed content types

### Healthy Patterns

- **Scores cluster 0.4-0.7**: Normal semantic search
- **Top result significantly higher than others**: Good discrimination
- **Gradual score degradation**: Proper ranking

## Improving Similarity Scores

If you need higher scores (though not always desirable), try:

### 1. Query Optimization

**Poor:** `"foundation models"`
**Better:** `"what are foundation models trained on"`
**Best:** `"foundation models definition training data applications"`

Longer, more specific queries better match document embedding style.

### 2. Adjust Chunk Size

```bash
# Smaller chunks for tighter semantic matching
vector-rag-tool index "**/*.md" --store my-store --chunk-size 800 --overlap 100
```

Trade-off: Less context per chunk.

### 3. Different Embedding Model

Try alternative Ollama models:

| Model | Dimensions | Characteristics |
|-------|------------|-----------------|
| `embeddinggemma` | 768 | Fast, balanced (default) |
| `mxbai-embed-large` | 1024 | Higher quality, slower |
| `nomic-embed-text` | 768 | Optimized for long documents |

### 4. Symmetric Embedding (Advanced)

Remove asymmetric formatting in `core/embeddings.py`:

```python
def embed_query(self, query: str) -> list[float]:
    # Direct embedding without task prefix
    return self.embed_text(query)

def embed_document(self, content: str, title: str | None = None) -> list[float]:
    # Direct embedding without title prefix
    return self.embed_text(content)
```

**Warning:** May reduce retrieval quality for some queries.

## Practical Guidelines

### For General RAG Use

- **Accept scores 0.4-0.7** as normal and healthy
- **Focus on result relevance**, not absolute score values
- **Use top-k filtering** (default: 5) rather than score thresholds
- **Evaluate qualitatively**: Does it find the right content?

### For Specific Use Cases

**Document Deduplication:** Set threshold 0.85+
**Semantic Q&A:** Accept scores 0.4+
**Citation Retrieval:** Set threshold 0.6+
**Exploratory Search:** Accept scores 0.3+

### Setting Score Thresholds

```bash
# Current: No minimum score (shows all top-k results)
vector-rag-tool query "foundation models" --store my-store --top-k 5

# To filter by minimum score, modify query.py:
# Change: min_score=0.0
# To: min_score=0.4  (or your desired threshold)
```

**Recommendation:** Start without thresholds, examine score distribution, then set threshold if needed.

## Conclusion

**Key Takeaways:**

1. Cosine similarity measures geometric relationships, not prediction confidence
2. Scores of 0.4-0.7 are typical and healthy for semantic search
3. A score of 0.5 means "semantically related" - exactly what RAG should deliver
4. Focus on retrieval quality (does it find relevant content?) over absolute scores
5. Only tune for higher scores if your use case requires near-duplicates

**If your RAG finds the right documents with scores around 0.5, it's working correctly.**

## References

- LangChain Text Splitters: Used in `core/chunking.py`
- Ollama embeddinggemma: Default embedding model
- FAISS: Vector similarity search backend
- EmbeddingG asymmetric format: Query vs document formatting strategy

---

*This document was created for vector-rag-tool to explain similarity score interpretation for users unfamiliar with vector search systems.*
