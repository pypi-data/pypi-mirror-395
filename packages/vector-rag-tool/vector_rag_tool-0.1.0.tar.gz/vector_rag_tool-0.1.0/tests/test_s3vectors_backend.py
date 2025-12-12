"""
Tests for S3 Vectors backend implementation.

This module contains unit tests for the S3VectorsBackend class, using
mocked boto3 responses to test the functionality without AWS dependencies.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from unittest.mock import Mock, patch

import pytest
from botocore.exceptions import ClientError

from vector_rag_tool.core.s3vectors_backend import S3VectorsBackend


class TestS3VectorsBackend:
    """Test suite for S3VectorsBackend."""

    @pytest.fixture
    def backend(self):
        """Create S3VectorsBackend instance with mocked client."""
        with patch("boto3.Session") as mock_session:
            mock_client = Mock()
            mock_session.return_value.client.return_value = mock_client
            backend = S3VectorsBackend(
                bucket_name="test-bucket",
                region="eu-central-1",
                profile="test-profile",
            )
            backend.client = mock_client
            return backend

    @pytest.fixture
    def mock_error(self):
        """Create a mock ClientError."""

        def create_error(error_code, message="Test error"):
            error_response = {
                "Error": {
                    "Code": error_code,
                    "Message": message,
                }
            }
            return ClientError(error_response, "TestOperation")

        return create_error

    def test_init_with_profile(self):
        """Test backend initialization with profile."""
        with patch("boto3.Session") as mock_session:
            mock_client = Mock()
            mock_session.return_value.client.return_value = mock_client

            backend = S3VectorsBackend(
                bucket_name="test-bucket",
                region="us-west-2",
                profile="my-profile",
            )

            mock_session.assert_called_once_with(
                region_name="us-west-2",
                profile_name="my-profile",
            )
            assert backend.bucket_name == "test-bucket"
            assert backend.region == "us-west-2"

    def test_init_without_profile(self):
        """Test backend initialization without profile."""
        with patch("boto3.Session") as mock_session:
            mock_client = Mock()
            mock_session.return_value.client.return_value = mock_client

            backend = S3VectorsBackend(
                bucket_name="test-bucket",
                region="us-west-2",
                profile=None,
            )

            mock_session.assert_called_once_with(region_name="us-west-2")
            assert backend.bucket_name == "test-bucket"
            assert backend.region == "us-west-2"

    def test_create_store_success(self, backend):
        """Test successful store creation."""
        backend.client.create_vector_bucket.side_effect = [
            backend.client.exceptions.ConflictException(
                {"Error": {"Code": "ConflictException", "Message": "Bucket exists"}},
                "CreateVectorBucket",
            ),
        ]

        backend.create_store("my-store", dimension=512)

        backend.client.create_vector_bucket.assert_called_once_with(vectorBucketName="test-bucket")
        backend.client.create_index.assert_called_once_with(
            vectorBucketName="test-bucket",
            indexName="my-store",
            dataType="float32",
            dimension=512,
            distanceMetric="cosine",
        )

    def test_create_store_bucket_new(self, backend):
        """Test store creation when bucket is newly created."""
        # No exception - bucket creation succeeds
        backend.client.create_vector_bucket.return_value = None

        backend.create_store("my-store", dimension=512)

        backend.client.create_vector_bucket.assert_called_once_with(vectorBucketName="test-bucket")
        backend.client.create_index.assert_called_once_with(
            vectorBucketName="test-bucket",
            indexName="my-store",
            dataType="float32",
            dimension=512,
            distanceMetric="cosine",
        )

    def test_create_store_already_exists(self, backend, mock_error):
        """Test error when store already exists."""
        backend.client.create_index.side_effect = mock_error("IndexAlreadyExistsException")

        backend.client.create_vector_bucket.side_effect = None

        with pytest.raises(ValueError, match="Store 'my-store' already exists"):
            backend.create_store("my-store")

    def test_delete_store_success(self, backend):
        """Test successful store deletion."""
        backend.delete_store("my-store")

        backend.client.delete_index.assert_called_once_with(
            vectorBucketName="test-bucket",
            indexName="my-store",
        )

    def test_delete_store_not_found(self, backend, mock_error):
        """Test error when deleting non-existent store."""
        backend.client.delete_index.side_effect = mock_error("IndexNotFoundException")

        with pytest.raises(ValueError, match="Store 'my-store' does not exist"):
            backend.delete_store("my-store")

    def test_list_stores_success(self, backend):
        """Test successful store listing."""
        backend.client.list_indexes.return_value = {
            "indexes": [
                {"indexName": "store1"},
                {"indexName": "store2"},
                {"indexName": "store3"},
            ]
        }

        stores = backend.list_stores()

        assert stores == ["store1", "store2", "store3"]
        backend.client.list_indexes.assert_called_once_with(vectorBucketName="test-bucket")

    def test_list_stores_empty(self, backend):
        """Test listing stores when empty."""
        backend.client.list_indexes.return_value = {"indexes": []}

        stores = backend.list_stores()

        assert stores == []

    def test_list_stores_bucket_not_found(self, backend, mock_error):
        """Test listing stores when bucket doesn't exist."""
        backend.client.list_indexes.side_effect = mock_error("BucketNotFoundException")

        stores = backend.list_stores()

        assert stores == []

    def test_store_exists_true(self, backend):
        """Test store_exists when store exists."""
        backend.list_stores = Mock(return_value=["store1", "store2"])

        assert backend.store_exists("store1") is True
        assert backend.store_exists("store2") is True
        assert backend.store_exists("store3") is False

    def test_put_vectors_success(self, backend):
        """Test successful vector insertion."""
        vectors = [
            {
                "key": "doc1",
                "embedding": [0.1, 0.2, 0.3],
                "metadata": {"title": "Doc 1"},
            },
            {
                "key": "doc2",
                "embedding": [0.4, 0.5, 0.6],
                "metadata": {"title": "Doc 2"},
            },
        ]

        result = backend.put_vectors("my-store", vectors)

        assert result == 2
        backend.client.put_vectors.assert_called_once_with(
            vectorBucketName="test-bucket",
            indexName="my-store",
            vectors=[
                {
                    "key": "doc1",
                    "data": {"float32": [0.1, 0.2, 0.3]},
                    "metadata": {"title": "Doc 1"},
                },
                {
                    "key": "doc2",
                    "data": {"float32": [0.4, 0.5, 0.6]},
                    "metadata": {"title": "Doc 2"},
                },
            ],
        )

    def test_put_vectors_empty(self, backend):
        """Test putting empty vectors list."""
        result = backend.put_vectors("my-store", [])

        assert result == 0
        backend.client.put_vectors.assert_not_called()

    def test_put_vectors_store_not_found(self, backend, mock_error):
        """Test error when putting vectors to non-existent store."""
        backend.client.put_vectors.side_effect = mock_error("IndexNotFoundException")

        with pytest.raises(ValueError, match="Store 'my-store' does not exist"):
            backend.put_vectors("my-store", [{"key": "doc1", "embedding": [1, 2, 3]}])

    def test_delete_vectors_success(self, backend):
        """Test successful vector deletion."""
        keys = ["doc1", "doc2", "doc3"]

        result = backend.delete_vectors("my-store", keys)

        assert result == 3
        backend.client.delete_vectors.assert_called_once_with(
            vectorBucketName="test-bucket",
            indexName="my-store",
            keys=keys,
        )

    def test_delete_vectors_empty(self, backend):
        """Test deleting empty key list."""
        result = backend.delete_vectors("my-store", [])

        assert result == 0
        backend.client.delete_vectors.assert_not_called()

    def test_delete_vectors_store_not_found(self, backend, mock_error):
        """Test error when deleting vectors from non-existent store."""
        backend.client.delete_vectors.side_effect = mock_error("IndexNotFoundException")

        with pytest.raises(ValueError, match="Store 'my-store' does not exist"):
            backend.delete_vectors("my-store", ["doc1"])

    def test_query_success(self, backend):
        """Test successful vector query."""
        query_vector = [0.1, 0.2, 0.3]
        # Implementation expects distance and converts to score: score = 1.0 / (1.0 + distance)
        # distance=0.0526 -> score=0.95, distance=0.1765 -> score=0.85
        backend.client.query_vectors.return_value = {
            "vectors": [
                {
                    "key": "doc1",
                    "distance": 0.0526,  # ~0.95 score
                    "metadata": {"title": "Doc 1", "content_preview": "Content 1"},
                },
                {
                    "key": "doc2",
                    "distance": 0.1765,  # ~0.85 score
                    "metadata": {"title": "Doc 2"},
                },
            ]
        }

        results = backend.query("my-store", query_vector, top_k=5)

        assert len(results) == 2
        assert results[0].key == "doc1"
        assert abs(results[0].score - 0.95) < 0.01  # Allow small floating point variance
        assert results[0].metadata["title"] == "Doc 1"
        assert results[0].content == "Content 1"

        assert results[1].key == "doc2"
        assert abs(results[1].score - 0.85) < 0.01
        assert results[1].content is None

        backend.client.query_vectors.assert_called_once_with(
            vectorBucketName="test-bucket",
            indexName="my-store",
            queryVector={"float32": query_vector},
            topK=5,
            returnDistance=True,
            returnMetadata=True,
        )

    def test_query_empty_results(self, backend):
        """Test query with no results."""
        backend.client.query_vectors.return_value = {"vectors": []}

        results = backend.query("my-store", [1, 2, 3])

        assert results == []

    def test_query_store_not_found(self, backend, mock_error):
        """Test error when querying non-existent store."""
        backend.client.query_vectors.side_effect = mock_error("IndexNotFoundException")

        with pytest.raises(ValueError, match="Store 'my-store' does not exist"):
            backend.query("my-store", [1, 2, 3])

    def test_get_store_info_success(self, backend):
        """Test successful store info retrieval."""
        backend.client.get_index.return_value = {
            "index": {
                "dimension": 512,
                "distanceMetric": "cosine",
                "dataType": "float32",
                "creationTime": "2024-01-15T10:30:00Z",
            }
        }

        info = backend.get_store_info("my-store")

        assert info["name"] == "my-store"
        assert info["backend"] == "s3vectors"
        assert info["bucket"] == "test-bucket"
        assert info["region"] == "eu-central-1"
        assert info["location"] == "s3://test-bucket/my-store/"
        assert info["dimension"] == 512
        assert info["metric"] == "cosine"
        assert info["data_type"] == "float32"
        assert info["created_at"] == "2024-01-15T10:30:00Z"

    def test_get_store_info_not_found(self, backend, mock_error):
        """Test error when getting info for non-existent store."""
        backend.client.get_index.side_effect = mock_error("IndexNotFoundException")

        with pytest.raises(ValueError, match="Store 'my-store' does not exist"):
            backend.get_store_info("my-store")

    def test_get_store_info_fallback(self, backend, mock_error):
        """Test fallback info when get_index fails with non-NotFound error."""
        backend.client.get_index.side_effect = mock_error("SomeOtherError")

        info = backend.get_store_info("my-store")

        assert info["name"] == "my-store"
        assert info["backend"] == "s3vectors"
        assert info["bucket"] == "test-bucket"
        assert info["region"] == "eu-central-1"
        assert info["location"] == "s3://test-bucket/my-store/"
        assert info["status"] == "UNKNOWN"
        assert "dimension" not in info
        assert "metric" not in info

    def test_vector_without_metadata(self, backend):
        """Test handling vectors with no metadata."""
        vectors = [
            {
                "key": "doc1",
                "embedding": [0.1, 0.2, 0.3],
                # No metadata key
            },
            {
                "key": "doc2",
                "embedding": [0.4, 0.5, 0.6],
                "metadata": {},  # Empty metadata
            },
        ]

        backend.put_vectors("my-store", vectors)

        # Should convert missing metadata to empty dict
        backend.client.put_vectors.assert_called_once_with(
            vectorBucketName="test-bucket",
            indexName="my-store",
            vectors=[
                {
                    "key": "doc1",
                    "data": {"float32": [0.1, 0.2, 0.3]},
                    "metadata": {},
                },
                {
                    "key": "doc2",
                    "data": {"float32": [0.4, 0.5, 0.6]},
                    "metadata": {},
                },
            ],
        )
