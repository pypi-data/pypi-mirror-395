"""
Backend factory for vector storage.

This module provides a factory function to create the appropriate vector
backend based on configuration (local FAISS or remote S3 Vectors).

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from vector_rag_tool.core.backend import VectorBackend
from vector_rag_tool.core.faiss_backend import FAISSBackend
from vector_rag_tool.core.s3vectors_backend import S3VectorsBackend
from vector_rag_tool.logging_config import get_logger

logger = get_logger(__name__)


def get_backend(
    bucket: str | None = None,
    region: str = "eu-central-1",
    profile: str | None = None,
) -> VectorBackend:
    """Get appropriate backend based on configuration.

    Returns FAISSBackend by default for local storage, or S3VectorsBackend
    when a bucket name is provided for remote storage.

    Args:
        bucket: S3 bucket name for remote storage. If None, uses local FAISS.
        region: AWS region for S3 Vectors. Defaults to eu-central-1.
        profile: AWS profile name for authentication. Optional.

    Returns:
        VectorBackend instance configured appropriately.

    Examples:
        >>> # Local FAISS backend (default)
        >>> backend = get_backend()
        >>> isinstance(backend, FAISSBackend)
        True

        >>> # Remote S3 Vectors backend
        >>> backend = get_backend(bucket="my-bucket", profile="dev")
        >>> isinstance(backend, S3VectorsBackend)
        True
    """
    if bucket:
        logger.debug(
            "Creating S3VectorsBackend: bucket=%s, region=%s, profile=%s",
            bucket,
            region,
            profile,
        )
        return S3VectorsBackend(bucket_name=bucket, region=region, profile=profile)
    else:
        logger.debug("Creating FAISSBackend for local storage")
        return FAISSBackend()
