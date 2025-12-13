# Copyright 2025 Amazon.com, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import boto3  # type: ignore[import-untyped]

from amzn_sagemaker_checkpointing.checkpointing.filesystem.exceptions import (
    SageMakerS3TierError,
    SageMakerTieredStorageConfigError,
)
from amzn_sagemaker_checkpointing.config.sagemaker_checkpoint_config import SageMakerCheckpointConfig


class CheckpointHelpers:
    """Helper methods for checkpoint operations."""

    @staticmethod
    def bytes_to_mb(bytes_size: int) -> float:
        """Convert bytes to megabytes."""
        return bytes_size / (1024 * 1024)

    @staticmethod
    def get_log_prefix(rank: int, step: int | None) -> str:
        """Return log prefix for consistent logging."""
        return f"[Rank {rank}] Step {step}:"

    @staticmethod
    def get_s3_uri(s3_base_path: str, namespace: str, rank: int, step: int, filename: str) -> str:
        """Construct S3 URI for checkpoint files."""
        return f"{s3_base_path}/{namespace}/rank_{rank}/step_{step}/{filename}"

    @staticmethod
    def parse_s3_path(s3_path: str) -> tuple[str, str]:
        """Parse S3 path into bucket and prefix.

        Returns:
            tuple[str, str]: (bucket_name, prefix) where prefix has no trailing slash
        """
        path_without_s3 = s3_path[5:]  # Remove 's3://'
        if "/" in path_without_s3:
            bucket, prefix = path_without_s3.split("/", 1)
            return bucket, prefix.rstrip("/")
        return path_without_s3, ""

    @staticmethod
    def is_valid_s3_path(s3_path: str) -> bool:
        return s3_path is not None and s3_path.startswith("s3://")

    @staticmethod
    def validated_checkpoint_config(
        checkpoint_config: SageMakerCheckpointConfig,
    ) -> SageMakerCheckpointConfig:
        if not checkpoint_config.namespace:
            raise SageMakerTieredStorageConfigError("Namespace in SageMakerCheckpointConfig cannot be empty")
        if checkpoint_config.world_size <= 0:
            raise SageMakerTieredStorageConfigError(
                f"Invalid world size:{checkpoint_config.world_size}, expecting a positive integer"
            )

        if checkpoint_config.save_to_s3 and not CheckpointHelpers.is_valid_s3_path(checkpoint_config.s3_tier_base_path):
            raise SageMakerTieredStorageConfigError("Invalid S3 tier base path, should start with s3://")
        return checkpoint_config

    @staticmethod
    def get_bucket_location(s3_base_path: str) -> str:
        """
        Get S3 bucket location from an S3 base path.

        Args:
            s3_base_path (str): S3 path like 's3://bucket-name' or 's3://bucket-name/prefix/path'

        Returns:
            str: AWS region where the bucket is located
        """
        # Remove 's3://' prefix and split by '/'
        path_parts = s3_base_path[5:].split("/")
        bucket_name = path_parts[0]

        if not bucket_name:
            raise SageMakerS3TierError("Invalid S3 path: bucket name is empty")

        s3_client = boto3.client("s3")
        try:
            response = s3_client.get_bucket_location(Bucket=bucket_name)
            location = response["LocationConstraint"]
            return "us-east-1" if location is None else location
        except Exception as e:
            raise SageMakerS3TierError(f"Unable to fetch region for bucket {bucket_name}") from e
        finally:
            s3_client.close()
