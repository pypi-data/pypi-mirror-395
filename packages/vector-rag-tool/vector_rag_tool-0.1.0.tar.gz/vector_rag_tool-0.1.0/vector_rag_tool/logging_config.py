"""Centralized logging configuration with multi-level verbosity support.

This module provides setup_logging() for configuring logging based on
verbosity count from CLI arguments (-v, -vv, -vvv).

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import logging
import sys


def setup_logging(verbose_count: int = 0) -> None:
    """Configure logging based on verbosity level.

    Maps CLI verbosity count to Python logging levels and configures
    both application and dependent library loggers.

    Args:
        verbose_count: Number of -v flags (0-3+)
            0: WARNING level (quiet mode)
            1: INFO level (normal verbose)
            2: DEBUG level (detailed debugging)
            3+: DEBUG + enable dependent library logging (trace mode)

    Example:
        >>> setup_logging(0)  # No -v flag: WARNING only
        >>> setup_logging(1)  # -v: INFO level
        >>> setup_logging(2)  # -vv: DEBUG level
        >>> setup_logging(3)  # -vvv: DEBUG + library internals
    """
    # Map verbosity count to logging levels
    if verbose_count == 0:
        level = logging.WARNING
    elif verbose_count == 1:
        level = logging.INFO
    elif verbose_count >= 2:
        level = logging.DEBUG
    else:
        level = logging.WARNING

    # Configure format - all levels include module name for traceability
    if verbose_count >= 2:
        # Detailed format for DEBUG (includes line number)
        fmt = "[%(levelname)s] %(name)s:%(lineno)d - %(message)s"
    else:
        # Standard format for INFO/WARNING (module name, no line number)
        fmt = "[%(levelname)s] %(name)s - %(message)s"

    # Configure root logger
    logging.basicConfig(
        level=level,
        format=fmt,
        stream=sys.stderr,
        force=True,  # Override any existing configuration
    )

    # Libraries used by this project that need logging configuration
    # - boto3/botocore: AWS SDK for S3 Vectors backend
    # - urllib3: HTTP client used by boto3
    # - ollama: Local LLM embeddings
    # - httpx/httpcore: HTTP client used by ollama
    # - langchain/langchain_text_splitters: Text chunking
    # - langchain_core: Core langchain utilities
    # - faiss: Vector similarity search (C library, no Python logging)
    # - numpy: Numerical operations (minimal logging)
    # - tqdm: Progress bars
    # - pyyaml: YAML parsing
    # - openai: Optional OpenAI integration for image descriptions
    trace_libraries = [
        # AWS SDK
        "boto3",
        "botocore",
        "urllib3",
        # Ollama and HTTP
        "ollama",
        "httpx",
        "httpcore",
        # LangChain
        "langchain",
        "langchain_core",
        "langchain_text_splitters",
        # OpenAI (optional)
        "openai",
        # Other
        "tqdm",
    ]

    # Configure dependent library loggers at TRACE level (-vvv)
    if verbose_count >= 3:
        # Enable library internals for trace-level debugging
        for lib in trace_libraries:
            logging.getLogger(lib).setLevel(logging.DEBUG)
    else:
        # Suppress noisy libraries at lower verbosity levels
        for lib in trace_libraries:
            logging.getLogger(lib).setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module.

    This is a convenience wrapper around logging.getLogger() that
    ensures consistent logger naming across your application.

    Args:
        name: Module name (typically __name__)

    Returns:
        Logger instance

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Operation started")
        >>> logger.debug("Detailed operation info")
    """
    return logging.getLogger(name)
