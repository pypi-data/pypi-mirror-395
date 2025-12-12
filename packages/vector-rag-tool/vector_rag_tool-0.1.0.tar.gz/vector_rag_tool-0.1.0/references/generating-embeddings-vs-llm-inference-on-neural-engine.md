# Generating Embeddings vs LLM Inference on Neural Engine

A comparison of computational characteristics between embedding generation and LLM inference on Apple Silicon (M4 Pro).

## The Paradox

A small embedding model (~400MB) can saturate the GPU at 80% utilization, while a large LLM (19GB) appears to run smoothly. Why?

## Embedding Generation

```
32 chunks x 250 tokens = 8000 tokens processed in parallel
                    |
                    v
    Full attention: every token attends to every token
    All computed in single forward pass
```

**Characteristics:**
- **Compute-bound** - bottleneck is matrix multiplication
- Batch size = 32 (32x parallel work)
- No KV-cache, full N^2 attention per chunk
- No streaming output, must wait for entire batch

### Computation per Batch

For a typical embedding model (EmbeddingGemma, 6 layers, 768 hidden dim):

| Operation | Calculation | FLOPs |
|-----------|-------------|-------|
| QKV projections | 3 x 250 x 768 x 768 | ~442M |
| Attention scores | 250 x 250 x 768 | ~48M |
| FFN layer | 250 x 768 x 3072 x 2 | ~1.2B |
| **Per layer** | | **~1.7B** |
| **x 6 layers** | | **~10B** |
| **x 32 batch** | | **~320B** |

**Result: ~320 billion FLOPs per batch**

## LLM Inference

```
Prompt: "Hello" -> Generate token 1 -> token 2 -> token 3...
                        |
                        v
         Load 19GB weights, compute for 1 token
         Load 19GB weights, compute for 1 token
         (repeat)
```

**Characteristics:**
- **Memory-bandwidth bound** - bottleneck is loading weights from RAM
- Batch size = 1 (one prompt at a time)
- KV-cache reuses previous computation
- Streaming output feels fast (tokens appear incrementally)

## Comparison

| Aspect | 19GB LLM | 400MB Embedding |
|--------|----------|-----------------|
| Bottleneck | Memory bandwidth | Compute |
| Tokens/pass | 1 | 8000 |
| GPU utilization | ~20-40% | ~80% |
| Feels fast because | Streaming | - |

## The Claude Code Effect

When running Claude Code alongside embedding generation, both compete for compute resources.

### Simple LLM Prompt

```
"What is 2+2?" (5 tokens)
        |
        v
Prefill: trivial
Generate: memory-bound, fast
```

### Claude Code Prompt

```
System prompt + CLAUDE.md + conversation + tool results
        |
        v
~20K-100K tokens context
        |
        v
Prefill: COMPUTE-BOUND (must process entire context)
Generate: memory-bound, but longer KV-cache
```

### Prefill Phase Scaling

| Context size | Attention ops | Prefill impact |
|--------------|---------------|----------------|
| 100 tokens | 100^2 = 10K | instant |
| 10K tokens | 10K^2 = 100M | noticeable |
| 50K tokens | 50K^2 = 2.5B | heavy |

## Why Concurrent Workloads Slow Down

With Claude Code's large context:
- **Prefill phase** becomes compute-bound (like embeddings)
- **Both** embedding batches and LLM prefill compete for compute
- Neural engine saturated from two directions

## Key Takeaways

1. **Big model + batch=1 = memory-bound** - GPU cores often idle waiting for data
2. **Small model + batch=32 = compute-bound** - GPU cores saturated with parallel matmuls
3. **Large context LLM = compute-bound during prefill** - attention scales quadratically
4. **Running embeddings + Claude Code = compute contention** - both workloads fight for the same compute resources

## Practical Implications

- Embedding batch size of 32 is aggressive for concurrent workloads
- Consider lowering batch size (8-16) when running alongside other GPU tasks
- Memory (48GB) is not the constraint - compute throughput is
- For dedicated embedding jobs, batch=32 maximizes throughput
