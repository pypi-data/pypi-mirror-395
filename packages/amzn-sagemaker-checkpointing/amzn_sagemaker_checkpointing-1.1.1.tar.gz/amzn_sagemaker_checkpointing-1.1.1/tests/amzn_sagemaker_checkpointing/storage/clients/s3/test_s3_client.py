"""
Unit tests for SageMaker S3 Client.

These tests focus on the S3 client logic without requiring actual AWS resources.
Uses mocking to test the client behavior in isolation.
"""

import unittest
from unittest.mock import Mock, patch

from amzn_sagemaker_checkpointing.storage.clients.s3.s3_client import (
    SageMakerS3Client,
    SageMakerS3Config,
)


class TestSageMakerS3Config(unittest.TestCase):
    """Test SageMakerS3Config configuration class."""

    def test_config_initialization(self):
        """Test configuration initialization with minimal parameters."""
        config = SageMakerS3Config(region="us-west-2")

        self.assertEqual(config.region, "us-west-2")

    def test_config_with_kwargs(self):
        """Test configuration with additional kwargs."""
        config = SageMakerS3Config(region="eu-west-1", custom_param="test")

        self.assertEqual(config.region, "eu-west-1")
        # kwargs are accepted but not stored in this minimal config


class TestSageMakerS3Client(unittest.TestCase):
    """Test SageMakerS3Client functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = SageMakerS3Config(region="us-west-2")

    def test_client_initialization(self):
        """Test S3 client initialization."""
        client = SageMakerS3Client(self.config)

        self.assertEqual(client.region, "us-west-2")
        self.assertEqual(client._config, self.config)

    @patch("amzn_sagemaker_checkpointing.storage.clients.s3.s3_client.S3Checkpoint")
    def test_create_write_stream(self, mock_s3_checkpoint_class):
        """Test create_write_stream method."""
        # Setup mocks
        mock_s3_checkpoint = Mock()
        mock_writer = Mock()
        mock_stream = Mock()

        mock_s3_checkpoint_class.return_value = mock_s3_checkpoint
        mock_s3_checkpoint.writer.return_value = mock_writer
        mock_writer.__enter__ = Mock(return_value=mock_stream)
        mock_writer.__exit__ = Mock(return_value=None)

        client = SageMakerS3Client(self.config)

        # Test the context manager
        with client.create_write_stream("s3://test-bucket/test-key") as stream:
            self.assertEqual(stream, mock_stream)

        # Verify S3Checkpoint was created with only region parameter
        mock_s3_checkpoint_class.assert_called_once_with(region="us-west-2")

        # Verify writer was called with s3_uri
        mock_s3_checkpoint.writer.assert_called_once_with("s3://test-bucket/test-key")
        mock_writer.__enter__.assert_called_once()
        mock_writer.__exit__.assert_called_once()

    @patch("amzn_sagemaker_checkpointing.storage.clients.s3.s3_client.S3Checkpoint")
    def test_create_read_stream(self, mock_s3_checkpoint_class):
        """Test create_read_stream method."""
        # Setup mocks
        mock_s3_checkpoint = Mock()
        mock_reader = Mock()
        mock_stream = Mock()

        mock_s3_checkpoint_class.return_value = mock_s3_checkpoint
        mock_s3_checkpoint.reader.return_value = mock_reader
        mock_reader.__enter__ = Mock(return_value=mock_stream)
        mock_reader.__exit__ = Mock(return_value=None)

        client = SageMakerS3Client(self.config)

        # Test the context manager
        with client.create_read_stream("s3://test-bucket/test-key") as stream:
            self.assertEqual(stream, mock_stream)

        # Verify S3Checkpoint was created with only region parameter
        mock_s3_checkpoint_class.assert_called_once_with(region="us-west-2")

        # Verify reader was called with s3_uri
        mock_s3_checkpoint.reader.assert_called_once_with("s3://test-bucket/test-key")
        mock_reader.__enter__.assert_called_once()
        mock_reader.__exit__.assert_called_once()

    @patch("amzn_sagemaker_checkpointing.storage.clients.s3.s3_client.S3Checkpoint")
    def test_write_stream_exception_handling(self, mock_s3_checkpoint_class):
        """Test exception handling in create_write_stream."""
        # Setup mock to raise exception
        mock_s3_checkpoint_class.side_effect = Exception("S3Checkpoint creation failed")

        client = SageMakerS3Client(self.config)

        # Test that exception is re-raised
        with self.assertRaises(Exception) as context:
            with client.create_write_stream("s3://test-bucket/test-key"):
                pass

        self.assertIn("S3Checkpoint creation failed", str(context.exception))

    @patch("amzn_sagemaker_checkpointing.storage.clients.s3.s3_client.S3Checkpoint")
    def test_read_stream_exception_handling(self, mock_s3_checkpoint_class):
        """Test exception handling in create_read_stream."""
        # Setup mock to raise exception
        mock_s3_checkpoint_class.side_effect = Exception("S3Checkpoint creation failed")

        client = SageMakerS3Client(self.config)

        # Test that exception is re-raised
        with self.assertRaises(Exception) as context:
            with client.create_read_stream("s3://test-bucket/test-key"):
                pass

        self.assertIn("S3Checkpoint creation failed", str(context.exception))


if __name__ == "__main__":
    # Configure logging for tests
    import logging

    logging.basicConfig(level=logging.WARNING)

    # Run the tests
    unittest.main(verbosity=2)
