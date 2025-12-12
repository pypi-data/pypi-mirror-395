# vector-rag-tool - Project Specification

## Goal

A CLI that provides local RAG (Retrieval-Augmented Generation) with Ollama embeddings and FAISS vector search.

## What is vector-rag-tool?

`vector-rag-tool` is a CLI that provides semantic code search and document retrieval using vector embeddings. It indexes codebases and documents into vector stores for fast similarity search, using Ollama for local embeddings and FAISS for vector storage.

## Technical Requirements

### Runtime

- Python 3.13+
- Installable globally with mise
- Cross-platform (macOS, Linux, Windows)

### Dependencies

- `click` - CLI framework
- `faiss-cpu` - Vector similarity search
- `ollama` - Local LLM embeddings
- `pydantic` - Data validation
- `boto3` - AWS SDK (for S3 Vectors backend)
- `tqdm` - Progress bars

### Development Dependencies

- `ruff` - Linting and formatting
- `mypy` - Type checking
- `pytest` - Testing framework
- `bandit` - Security linting
- `pip-audit` - Dependency vulnerability scanning
- `gitleaks` - Secret detection (requires separate installation)

## CLI Commands

```bash
vector-rag-tool [OPTIONS] COMMAND [ARGS]
```

### Global Options

- `-v, --verbose` - Enable verbose output (count flag: -v, -vv, -vvv)
  - `-v` (count=1): INFO level logging
  - `-vv` (count=2): DEBUG level logging
  - `-vvv` (count=3+): TRACE level (includes library internals)
- `--help` / `-h` - Show help message
- `--version` - Show version

### Commands

- `index` - Index files matching glob patterns into a vector store
- `query` - Query a vector store for relevant document chunks
- `store` - Manage vector stores (create, delete, list, info)
- `completion` - Generate shell completion script

## Project Structure

```
vector-rag-tool/
├── vector_rag_tool/
│   ├── __init__.py
│   ├── cli.py              # Click CLI entry point (group with subcommands)
│   ├── completion.py       # Shell completion command
│   ├── logging_config.py   # Multi-level verbosity logging
│   ├── utils.py            # Utility functions
│   ├── commands/           # CLI subcommands
│   │   ├── index.py        # Index command
│   │   ├── query.py        # Query command
│   │   └── store.py        # Store management commands
│   ├── core/               # Core functionality
│   │   ├── backend.py      # Backend interface
│   │   ├── backend_factory.py
│   │   ├── chunking.py     # Text chunking
│   │   ├── embeddings.py   # Ollama embeddings
│   │   ├── faiss_backend.py
│   │   ├── file_detector.py
│   │   ├── models.py       # Data models
│   │   └── s3vectors_backend.py
│   └── services/           # Business logic
│       ├── indexer.py
│       └── querier.py
├── tests/                  # Test suite
├── plugins/                # Claude Code plugin
├── references/             # Design documentation
├── pyproject.toml          # Project configuration
├── README.md               # User documentation
├── CLAUDE.md               # This file
├── Makefile                # Development commands
├── LICENSE                 # MIT License
├── .mise.toml              # mise configuration
├── .gitleaks.toml          # Gitleaks configuration
└── .gitignore
```

## Code Style

- Type hints for all functions
- Docstrings for all public functions
- Follow PEP 8 via ruff
- 100 character line length
- Strict mypy checking

## Development Workflow

```bash
# Install dependencies
make install

# Run linting
make lint

# Format code
make format

# Type check
make typecheck

# Run tests
make test

# Security scanning
make security-bandit       # Python security linting
make security-pip-audit    # Dependency CVE scanning
make security-gitleaks     # Secret detection
make security              # Run all security checks

# Run all checks (includes security)
make check

# Full pipeline (includes security)
make pipeline
```

## Security

The template includes three lightweight security tools:

1. **bandit** - Python code security linting
   - Detects: SQL injection, hardcoded secrets, unsafe functions
   - Speed: ~2-3 seconds

2. **pip-audit** - Dependency vulnerability scanning
   - Detects: Known CVEs in dependencies
   - Speed: ~2-3 seconds

3. **gitleaks** - Secret and API key detection
   - Detects: AWS keys, GitHub tokens, API keys, private keys
   - Speed: ~1 second
   - Requires: `brew install gitleaks` (macOS)

All security checks run automatically in `make check` and `make pipeline`.

## Multi-Level Verbosity Logging

The template includes a centralized logging system with progressive verbosity levels.

### Implementation Pattern

1. **logging_config.py** - Centralized logging configuration
   - `setup_logging(verbose_count)` - Configure logging based on -v count
   - `get_logger(name)` - Get logger instance for module
   - Maps verbosity to Python logging levels (WARNING/INFO/DEBUG)

2. **CLI Integration** - Add to every CLI command
   ```python
   from vector_rag_tool.logging_config import get_logger, setup_logging

   logger = get_logger(__name__)

   @click.command()
   @click.option("-v", "--verbose", count=True, help="...")
   def command(verbose: int):
       setup_logging(verbose)  # First thing in command
       logger.info("Operation started")
       logger.debug("Detailed info")
   ```

3. **Logging Levels**
   - **0 (no -v)**: WARNING only - production/quiet mode
   - **1 (-v)**: INFO - high-level operations
   - **2 (-vv)**: DEBUG - detailed debugging
   - **3+ (-vvv)**: TRACE - enable library internals

4. **Best Practices**
   - Always log to stderr (keeps stdout clean for piping)
   - Use structured messages with placeholders: `logger.info("Found %d items", count)`
   - Call `setup_logging()` first in every command
   - Use `get_logger(__name__)` at module level
   - For TRACE level, enable third-party library loggers in `logging_config.py`

5. **Customizing Library Logging**
   Edit `logging_config.py` to add project-specific libraries:
   ```python
   if verbose_count >= 3:
       logging.getLogger("requests").setLevel(logging.DEBUG)
       logging.getLogger("urllib3").setLevel(logging.DEBUG)
   ```

## Shell Completion

The template includes shell completion for bash, zsh, and fish following the Click Shell Completion Pattern.

### Implementation

1. **completion.py** - Separate module for completion command
   - Uses Click's `BashComplete`, `ZshComplete`, `FishComplete` classes
   - Generates shell-specific completion scripts
   - Includes installation instructions in help text

2. **CLI Integration** - Added as subcommand
   ```python
   from vector_rag_tool.completion import completion_command

   @click.group(invoke_without_command=True)
   def main(ctx: click.Context):
       # Default behavior when no subcommand
       if ctx.invoked_subcommand is None:
           # Main command logic here
           pass

   # Add completion subcommand
   main.add_command(completion_command)
   ```

3. **Usage Pattern** - User-friendly command
   ```bash
   # Generate completion script
   vector-rag-tool completion bash
   vector-rag-tool completion zsh
   vector-rag-tool completion fish

   # Install (eval or save to file)
   eval "$(vector-rag-tool completion bash)"
   ```

4. **Supported Shells**
   - **Bash** (≥ 4.4) - Uses bash-completion
   - **Zsh** (any recent) - Uses zsh completion system
   - **Fish** (≥ 3.0) - Uses fish completion system
   - **PowerShell** - Not supported by Click

5. **Installation Methods**
   - **Temporary**: `eval "$(vector-rag-tool completion bash)"`
   - **Permanent**: Add eval to ~/.bashrc or ~/.zshrc
   - **File-based** (recommended): Save to dedicated completion file

### Adding More Commands

The CLI uses `@click.group()` for extensibility. To add new commands:

1. Create new command module in `vector_rag_tool/`
2. Import and add to CLI group:
   ```python
   from vector_rag_tool.new_command import new_command
   main.add_command(new_command)
   ```

3. Completion will automatically work for new commands and their options

## Installation Methods

### Global installation with mise

```bash
cd /path/to/vector-rag-tool
mise use -g python@3.14
uv sync
uv tool install .
```

After installation, `vector-rag-tool` command is available globally.

### Local development

```bash
uv sync
uv run vector-rag-tool [args]
```
