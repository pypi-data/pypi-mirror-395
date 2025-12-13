"""
S3 client module for SageMaker Checkpointing.

This module provides optimized S3 clients built on top of the high-performance
MountpointS3Client from s3-connector-for-pytorch.
"""

from .s3_client import SageMakerS3Client, SageMakerS3Config

__all__ = [
    "SageMakerS3Client",
    "SageMakerS3Config",
]
