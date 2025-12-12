"""
Tests for backend factory module.

Tests the get_backend() function to ensure it returns the correct
backend instance based on configuration parameters.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from unittest.mock import Mock, patch

from vector_rag_tool.core.backend import VectorBackend
from vector_rag_tool.core.backend_factory import get_backend
from vector_rag_tool.core.faiss_backend import FAISSBackend
from vector_rag_tool.core.s3vectors_backend import S3VectorsBackend


class TestGetBackend:
    """Test cases for the get_backend factory function."""

    def test_get_backend_returns_faiss_by_default(self) -> None:
        """Test that get_backend returns FAISSBackend when no bucket is provided."""
        backend = get_backend()

        assert isinstance(backend, FAISSBackend)
        assert isinstance(backend, VectorBackend)

    def test_get_backend_returns_faiss_with_none_bucket(self) -> None:
        """Test that get_backend returns FAISSBackend when bucket is explicitly None."""
        backend = get_backend(bucket=None)

        assert isinstance(backend, FAISSBackend)
        assert isinstance(backend, VectorBackend)

    def test_get_backend_returns_faiss_with_empty_bucket(self) -> None:
        """Test that get_backend returns FAISSBackend when bucket is empty string."""
        backend = get_backend(bucket="")

        assert isinstance(backend, FAISSBackend)
        assert isinstance(backend, VectorBackend)

    @patch("vector_rag_tool.core.backend_factory.S3VectorsBackend")
    def test_get_backend_returns_s3vectors_with_bucket(self, mock_s3_backend: Mock) -> None:
        """Test that get_backend returns S3VectorsBackend when bucket is provided."""
        mock_instance = Mock(spec=S3VectorsBackend)
        mock_s3_backend.return_value = mock_instance

        backend = get_backend(bucket="test-bucket")

        mock_s3_backend.assert_called_once_with(
            bucket_name="test-bucket",
            region="eu-central-1",
            profile=None,
        )
        assert backend is mock_instance

    @patch("vector_rag_tool.core.backend_factory.S3VectorsBackend")
    def test_get_backend_passes_region_parameter(self, mock_s3_backend: Mock) -> None:
        """Test that get_backend passes region parameter to S3VectorsBackend."""
        mock_instance = Mock(spec=S3VectorsBackend)
        mock_s3_backend.return_value = mock_instance

        backend = get_backend(bucket="test-bucket", region="us-west-2")

        mock_s3_backend.assert_called_once_with(
            bucket_name="test-bucket",
            region="us-west-2",
            profile=None,
        )
        assert backend is mock_instance

    @patch("vector_rag_tool.core.backend_factory.S3VectorsBackend")
    def test_get_backend_passes_profile_parameter(self, mock_s3_backend: Mock) -> None:
        """Test that get_backend passes profile parameter to S3VectorsBackend."""
        mock_instance = Mock(spec=S3VectorsBackend)
        mock_s3_backend.return_value = mock_instance

        backend = get_backend(
            bucket="test-bucket",
            region="eu-central-1",
            profile="my-aws-profile",
        )

        mock_s3_backend.assert_called_once_with(
            bucket_name="test-bucket",
            region="eu-central-1",
            profile="my-aws-profile",
        )
        assert backend is mock_instance

    @patch("vector_rag_tool.core.backend_factory.S3VectorsBackend")
    def test_get_backend_passes_all_parameters_to_s3vectors(self, mock_s3_backend: Mock) -> None:
        """Test that get_backend passes all parameters correctly to S3VectorsBackend."""
        mock_instance = Mock(spec=S3VectorsBackend)
        mock_s3_backend.return_value = mock_instance

        backend = get_backend(
            bucket="my-vector-bucket",
            region="ap-southeast-1",
            profile="production",
        )

        mock_s3_backend.assert_called_once_with(
            bucket_name="my-vector-bucket",
            region="ap-southeast-1",
            profile="production",
        )
        assert backend is mock_instance

    def test_get_backend_type_annotations(self) -> None:
        """Test that return type annotation matches VectorBackend."""

        # This test ensures type hints are correct
        def typed_get_backend(
            bucket: str | None = None,
            region: str = "eu-central-1",
            profile: str | None = None,
        ) -> VectorBackend:
            return get_backend(bucket, region, profile)

        # Should not raise any type errors
        backend = typed_get_backend()
        assert isinstance(backend, VectorBackend)
