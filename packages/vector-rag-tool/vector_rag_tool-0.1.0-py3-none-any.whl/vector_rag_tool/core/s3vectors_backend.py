"""
S3 Vectors backend implementation for remote vector storage.

This module provides an implementation of the VectorBackend interface using
AWS S3 Vectors service for scalable, cloud-based vector storage and search.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from typing import Any

import boto3
from botocore.exceptions import ClientError

from vector_rag_tool.core.backend import VectorBackend, VectorQueryResult
from vector_rag_tool.logging_config import get_logger

logger = get_logger(__name__)


class S3VectorsBackend(VectorBackend):
    """AWS S3 Vectors storage backend implementation."""

    def __init__(
        self,
        bucket_name: str,
        region: str = "eu-central-1",
        profile: str | None = None,
    ):
        """Initialize S3 Vectors backend.

        Args:
            bucket_name: S3 bucket name for vector storage
            region: AWS region
            profile: AWS profile name for authentication
        """
        self.bucket_name = bucket_name
        self.region = region

        # Create boto3 session with profile if provided
        session_kwargs = {"region_name": region}
        if profile:
            session_kwargs["profile_name"] = profile

        session = boto3.Session(**session_kwargs)
        self.client = session.client("s3vectors")

        logger.debug(
            "Initialized S3VectorsBackend: bucket=%s, region=%s, profile=%s",
            bucket_name,
            region,
            profile,
        )

    def create_store(self, store_name: str, dimension: int = 768) -> None:
        """Create a new vector store (index) in S3.

        Args:
            store_name: Name of the store/index to create
            dimension: Vector dimension size
        """
        try:
            # First ensure the vector bucket exists
            try:
                self.client.create_vector_bucket(vectorBucketName=self.bucket_name)
                logger.info("Created vector bucket: %s", self.bucket_name)
            except self.client.exceptions.ConflictException:
                logger.debug("Vector bucket already exists: %s", self.bucket_name)

            # Create the index within the bucket
            self.client.create_index(
                vectorBucketName=self.bucket_name,
                indexName=store_name,
                dataType="float32",
                dimension=dimension,
                distanceMetric="cosine",
            )

            logger.info(
                "Created S3 Vectors store: %s/%s (dimension=%d)",
                self.bucket_name,
                store_name,
                dimension,
            )

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "IndexAlreadyExistsException":
                raise ValueError(f"Store '{store_name}' already exists") from e
            else:
                logger.error("Failed to create store %s: %s", store_name, e)
                raise

    def delete_store(self, store_name: str) -> None:
        """Delete a vector store from S3.

        Args:
            store_name: Name of the store/index to delete
        """
        try:
            self.client.delete_index(
                vectorBucketName=self.bucket_name,
                indexName=store_name,
            )
            logger.info("Deleted S3 Vectors store: %s/%s", self.bucket_name, store_name)

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "IndexNotFoundException":
                raise ValueError(f"Store '{store_name}' does not exist") from e
            else:
                logger.error("Failed to delete store %s: %s", store_name, e)
                raise

    def list_stores(self) -> list[str]:
        """List all vector stores (indexes) in the bucket.

        Returns:
            List of store names
        """
        try:
            response = self.client.list_indexes(vectorBucketName=self.bucket_name)
            indexes = response.get("indexes", [])
            return [idx["indexName"] for idx in indexes]

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "BucketNotFoundException":
                logger.debug("Bucket does not exist: %s", self.bucket_name)
                return []
            else:
                logger.error("Failed to list stores: %s", e)
                raise

    def store_exists(self, store_name: str) -> bool:
        """Check if a vector store exists.

        Args:
            store_name: Name of the store to check

        Returns:
            True if store exists, False otherwise
        """
        return store_name in self.list_stores()

    def put_vectors(
        self,
        store_name: str,
        vectors: list[dict[str, Any]],  # [{'key': str, 'embedding': list, 'metadata': dict}]
    ) -> int:
        """Insert vectors into the store.

        Args:
            store_name: Name of the store
            vectors: List of vectors with keys, embeddings, and metadata

        Returns:
            Number of vectors inserted
        """
        if not vectors:
            return 0

        # Convert vectors to S3 Vectors format
        s3_vectors = [
            {
                "key": v["key"],
                "data": {"float32": v["embedding"]},
                "metadata": v.get("metadata", {}),
            }
            for v in vectors
        ]

        try:
            self.client.put_vectors(
                vectorBucketName=self.bucket_name,
                indexName=store_name,
                vectors=s3_vectors,
            )
            logger.debug(
                "Inserted %d vectors into store %s/%s",
                len(vectors),
                self.bucket_name,
                store_name,
            )
            return len(vectors)

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "IndexNotFoundException":
                raise ValueError(f"Store '{store_name}' does not exist") from e
            else:
                logger.error("Failed to put vectors: %s", e)
                raise

    def delete_vectors(self, store_name: str, keys: list[str]) -> int:
        """Delete vectors by keys.

        Args:
            store_name: Name of the store
            keys: List of vector keys to delete

        Returns:
            Number of vectors deleted
        """
        if not keys:
            return 0

        try:
            self.client.delete_vectors(
                vectorBucketName=self.bucket_name,
                indexName=store_name,
                keys=keys,
            )
            logger.debug(
                "Deleted %d vectors from store %s/%s",
                len(keys),
                self.bucket_name,
                store_name,
            )
            return len(keys)

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "IndexNotFoundException":
                raise ValueError(f"Store '{store_name}' does not exist") from e
            else:
                logger.error("Failed to delete vectors: %s", e)
                raise

    def query(
        self,
        store_name: str,
        query_vector: list[float],
        top_k: int = 5,
    ) -> list[VectorQueryResult]:
        """Query for similar vectors.

        Args:
            store_name: Name of the store to query
            query_vector: Query vector embedding
            top_k: Number of results to return

        Returns:
            List of query results with scores and metadata
        """
        try:
            response = self.client.query_vectors(
                vectorBucketName=self.bucket_name,
                indexName=store_name,
                queryVector={"float32": query_vector},
                topK=top_k,
                returnDistance=True,
                returnMetadata=True,
            )

            results = []
            for v in response.get("vectors", []):
                # S3 Vectors returns distance, convert to score (higher is better)
                distance = v.get("distance", 0.0)
                score = 1.0 / (1.0 + distance)
                metadata = v.get("metadata", {})
                results.append(
                    VectorQueryResult(
                        key=v["key"],
                        score=score,
                        metadata=metadata,
                        content=metadata.get("content_preview"),
                    )
                )

            logger.debug(
                "Query returned %d results from store %s/%s",
                len(results),
                self.bucket_name,
                store_name,
            )
            return results

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "IndexNotFoundException":
                raise ValueError(f"Store '{store_name}' does not exist") from e
            else:
                logger.error("Failed to query vectors: %s", e)
                raise

    def get_store_info(self, store_name: str) -> dict[str, Any]:
        """Get store metadata and information.

        Args:
            store_name: Name of the store

        Returns:
            Dictionary with store information
        """
        try:
            # S3 Vectors API for index info
            response = self.client.get_index(
                vectorBucketName=self.bucket_name,
                indexName=store_name,
            )

            # Response is nested under 'index' key
            index_info = response.get("index", {})

            return {
                "name": store_name,
                "backend": "s3vectors",
                "bucket": self.bucket_name,
                "region": self.region,
                "location": f"s3://{self.bucket_name}/{store_name}/",
                "dimension": index_info.get("dimension"),
                "metric": index_info.get("distanceMetric", "cosine"),
                "data_type": index_info.get("dataType", "float32"),
                "created_at": index_info.get("creationTime"),
            }

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "IndexNotFoundException":
                raise ValueError(f"Store '{store_name}' does not exist") from e
            else:
                # Fallback to basic info if describe_index is not available
                logger.debug("Could not get detailed store info: %s", e)
                return {
                    "name": store_name,
                    "backend": "s3vectors",
                    "bucket": self.bucket_name,
                    "region": self.region,
                    "location": f"s3://{self.bucket_name}/{store_name}/",
                    "status": "UNKNOWN",
                }
