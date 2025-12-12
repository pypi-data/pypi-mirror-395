---
description: Show help information for vector-rag-tool
argument-hint: command
---

Display help information for vector-rag-tool CLI commands.

## Usage

```bash
# Show general help
vector-rag-tool --help

# Show command-specific help
vector-rag-tool COMMAND --help

# Show version
vector-rag-tool --version
```

## Available Commands

- `index` - Index files matching glob patterns into a vector store
- `query` - Query a vector store for relevant document chunks
- `store` - Manage vector stores (create, delete, list, info)
- `completion` - Generate shell completion script

## Arguments

- `COMMAND` (optional): Specific command to get help for
- `--help` / `-h`: Show help information
- `--version`: Show version information

## Examples

```bash
# General help
vector-rag-tool --help

# Index command help
vector-rag-tool index --help

# Query command help
vector-rag-tool query --help

# Store management help
vector-rag-tool store --help
vector-rag-tool store create --help
vector-rag-tool store delete --help
vector-rag-tool store list --help
vector-rag-tool store info --help

# Completion command help
vector-rag-tool completion --help

# Version information
vector-rag-tool --version
```

## Output

Displays usage information, available commands, options, and examples.
