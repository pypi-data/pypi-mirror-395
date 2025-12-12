"""Test helpers and utilities for SageMaker Checkpointing filesystem tests.

This module contains shared test utilities, mock objects, and helper functions
used across multiple test files in the filesystem test suite.
"""

import os
import tempfile
from unittest.mock import Mock, patch

import torch
from torch.distributed.checkpoint.metadata import Metadata
from torch.distributed.checkpoint.planner import WriteItemType

from amzn_sagemaker_checkpointing.config.sagemaker_checkpoint_config import SageMakerCheckpointConfig


# Global AWS mocking decorator
def mock_aws_calls(test_func):
    """Decorator to mock AWS calls for all test methods."""

    @patch("boto3.client")
    def wrapper(*args, **kwargs):
        # Get the mock_boto3_client from the arguments
        mock_boto3_client = args[-1]  # Last argument is the mock

        # Set up AWS client mocks
        mock_sts_client = Mock()
        mock_sts_client.get_caller_identity.return_value = {"Account": "123456789012"}

        mock_s3_client = Mock()
        mock_s3_client.get_bucket_location.return_value = {"LocationConstraint": "us-west-2"}

        def mock_client_factory(service_name, **kwargs):
            if service_name == "sts":
                return mock_sts_client
            elif service_name == "s3":
                return mock_s3_client
            return Mock()

        mock_boto3_client.side_effect = mock_client_factory

        # Call the original test function
        return test_func(*args[:-1], **kwargs)  # Remove the mock from args

    return wrapper


class DummyItem:
    def __init__(self, index):
        self.type = WriteItemType.TENSOR
        self.index = index


class DummyPlanner:
    def resolve_data(self, item):
        return torch.tensor([1, 2, 3])


class DummySavePlan:
    def __init__(self):
        self.items = [DummyItem(0)]


def create_temp_config(namespace="test-namespace", world_size=4, **kwargs):
    """Helper function to create a test configuration with temporary directory."""
    temp_dir = tempfile.mkdtemp()
    config_params = {
        "namespace": namespace,
        "world_size": world_size,
        "disk_tier_base_path": temp_dir,
        "s3_tier_base_path": "s3://test-bucket/checkpoints",
        "save_to_disk": True,
        "save_to_s3": True,
    }
    config_params.update(kwargs)
    return SageMakerCheckpointConfig(**config_params), temp_dir


def cleanup_temp_dir(temp_dir):
    """Helper function to clean up temporary directory."""
    if os.path.exists(temp_dir):
        import shutil

        shutil.rmtree(temp_dir)


def get_mock_metadata(state_dict_data=None):
    """Helper function to create a complete mock Metadata object."""
    if state_dict_data is None:
        state_dict_data = {"test": "data"}

    return Metadata(
        state_dict_metadata=state_dict_data,
        planner_data={"planner": "test_data"},
        storage_data={"storage": "test_data"},
        storage_meta={"meta": "test_data"},
    )
