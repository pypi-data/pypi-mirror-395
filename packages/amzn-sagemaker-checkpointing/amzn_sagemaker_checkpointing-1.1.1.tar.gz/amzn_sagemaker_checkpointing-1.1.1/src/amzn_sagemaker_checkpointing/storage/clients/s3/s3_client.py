"""
SageMaker S3 Client for checkpoint operations using S3Checkpoint backend.

This module provides a minimal SageMaker S3 client that uses S3Checkpoint
with the simplest possible configuration.
"""

import logging
from contextlib import contextmanager

from botocore.exceptions import ClientError  # type: ignore[import-untyped]
from s3torchconnector import S3Checkpoint  # type: ignore[import-untyped]
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

logger = logging.getLogger(__name__)


def is_throttling_error(exception):
    """Check if exception is a throttling error"""
    if isinstance(exception, ClientError):
        error_code = exception.response.get("Error", {}).get("Code", "")
        return error_code in [
            "Throttling",
            "ThrottlingException",
            "RequestLimitExceeded",
            "SlowDown",
        ]

    error_str = str(exception).lower()
    return any(keyword in error_str for keyword in ["throttl", "rate limit", "too many requests", "slow down"])


def s3_retry_with_jitter(max_attempts: int = 3, base_delay: float = 1.0, max_delay: float = 30.0):
    """Retry decorator with exponential backoff and jitter"""
    return retry(
        retry=retry_if_exception_type((ClientError, Exception)),
        stop=stop_after_attempt(max_attempts),
        wait=wait_random_exponential(multiplier=base_delay, max=max_delay),
        before_sleep=before_sleep_log(logging.getLogger(__name__), logging.WARNING),
        reraise=True,
    )


class SageMakerS3Config:
    """Simple configuration for SageMaker S3 client."""

    def __init__(self, region: str, **kwargs):
        self.region = region


class SageMakerS3Client:
    """
    Minimal SageMaker S3 Client using S3Checkpoint backend.

    This client provides basic read/write functionality using S3Checkpoint
    with the simplest possible configuration.
    """

    def __init__(self, config: SageMakerS3Config):
        self._config = config

        logger.info(f"Initialized SageMaker S3 client for region {self._config.region}")

    @property
    def region(self) -> str:
        """Get the AWS region."""
        return self._config.region

    @contextmanager
    def create_write_stream(self, s3_uri: str):
        """
        Create a write stream using S3Checkpoint backend with minimal config.

        Args:
            bucket: S3 bucket name
            key: S3 object key

        Yields:
            Stream object with direct write() method
        """
        logger.debug(f"Creating S3Checkpoint write stream for {s3_uri}")

        try:
            # Create S3Checkpoint with only required parameters
            s3_checkpoint = S3Checkpoint(region=self._config.region)

            # Use S3Checkpoint's write stream
            with s3_checkpoint.writer(s3_uri) as stream:
                yield stream

        except Exception as e:
            logger.error(f"Failed to create write stream for {s3_uri}: {e}")
            raise

    @contextmanager
    def create_read_stream(self, s3_uri: str):
        """
        Create a read stream using S3Checkpoint backend with minimal config.

        Args:
            bucket: S3 bucket name
            key: S3 object key

        Yields:
            Stream object with direct read() method
        """
        logger.debug(f"Creating S3Checkpoint read stream for {s3_uri}")

        try:
            # Create S3Checkpoint with only required parameters
            s3_checkpoint = S3Checkpoint(region=self._config.region)

            # Use S3Checkpoint's read stream
            with s3_checkpoint.reader(s3_uri) as stream:
                yield stream

        except Exception as e:
            logger.error(f"Failed to create read stream for {s3_uri}: {e}")
            raise
