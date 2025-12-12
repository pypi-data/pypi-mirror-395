import io
import pickle
from unittest import TestCase
from unittest.mock import Mock, patch

import torch
from test_helpers import cleanup_temp_dir, create_temp_config, mock_aws_calls
from torch.distributed.checkpoint.metadata import Metadata
from torch.distributed.checkpoint.planner import LoadItemType

from amzn_sagemaker_checkpointing.checkpointing.filesystem.exceptions import (
    SageMakerInMemoryTierError,
    SageMakerTieredStorageConfigError,
    SageMakerTieredStorageError,
)
from amzn_sagemaker_checkpointing.checkpointing.filesystem.filesystem import SageMakerTieredStorageReader
from amzn_sagemaker_checkpointing.checkpointing.filesystem.storage_info import _SageMakerStorageInfo
from amzn_sagemaker_checkpointing.config.sagemaker_checkpoint_config import SageMakerCheckpointConfig


class TestReaderInitialization(TestCase):
    def setUp(self):
        self.valid_config, self.temp_dir = create_temp_config(
            namespace="test-reader-init",
            world_size=4,
            save_to_disk=False,
            save_to_s3=False,
        )

    def tearDown(self):
        cleanup_temp_dir(self.temp_dir)

    @mock_aws_calls
    def test_reader_initialization_with_various_steps(self, *_):
        """Test reader initialization with various step values."""
        step_values = [0, 1, 10, 100, 999999, None]

        for step in step_values:
            with self.subTest(step=step):
                reader = SageMakerTieredStorageReader(self.valid_config, step=step)
                self.assertEqual(reader.step, step)
                self.assertEqual(reader.rank, 0)

    @mock_aws_calls
    @patch("torch.distributed.get_rank", return_value=2)
    @patch("torch.distributed.is_initialized", return_value=True)
    @patch("torch.distributed.is_available", return_value=True)
    def test_reader_initialization_different_ranks(self, *_):
        """Test reader initialization with different ranks."""
        reader = SageMakerTieredStorageReader(self.valid_config, step=50)
        self.assertEqual(reader.rank, 2)
        self.assertEqual(reader.step, 50)


class TestTieredRead(TestCase):
    def setUp(self):
        self.config, self.temp_dir = create_temp_config()

    def tearDown(self):
        cleanup_temp_dir(self.temp_dir)

    def test_init_with_invalid_config(self):
        invalid_config = SageMakerCheckpointConfig(namespace="", world_size=4)
        with self.assertRaises(SageMakerTieredStorageConfigError):
            SageMakerTieredStorageReader(checkpoint_config=invalid_config)

        invalid_config = SageMakerCheckpointConfig(namespace="test-namespace", world_size=0)
        with self.assertRaises(SageMakerTieredStorageError):
            SageMakerTieredStorageReader(checkpoint_config=invalid_config)

    @mock_aws_calls
    def test_read_data_from_memory(self, *_):
        """Test read_data method with mocked client"""
        reader = SageMakerTieredStorageReader(self.config)
        reader.step = 100

        # Mock storage data and metadata
        reader.storage_data = {0: Mock(rank=0, offset=0, length=100)}

        # Mock client.get_checkpoint to return test data
        test_data = b"test checkpoint data"
        reader.client.get_checkpoint = Mock(return_value=test_data)

        # Create mock plan and planner
        mock_plan = Mock()
        mock_plan.items = [Mock(storage_index=0, type=LoadItemType.BYTE_IO)]
        mock_planner = Mock()

        # Capture data passed to load_bytes
        captured_data = None

        def capture_load_bytes(read_item, stream):
            nonlocal captured_data
            captured_data = stream.getvalue()

        mock_planner.load_bytes.side_effect = capture_load_bytes

        # Execute read_data
        future = reader.read_data(mock_plan, mock_planner)
        future.wait()

        # Verify client was called
        reader.client.get_checkpoint.assert_called_once_with(step=100, rank=0)
        # Verify planner.load_bytes was called with correct data
        mock_planner.load_bytes.assert_called_once()
        self.assertEqual(captured_data, test_data)

    @mock_aws_calls
    def test_read_data_from_s3_fallback(self, *_):
        """Test read_data method falls back to S3 when memory read fails"""
        config = SageMakerCheckpointConfig(
            namespace="test-namespace", world_size=1, s3_tier_base_path="s3://test-bucket/checkpoints"
        )
        reader = SageMakerTieredStorageReader(config)
        reader.step = 100
        reader.storage_data = {0: Mock(rank=0, offset=0, length=100)}
        reader.client.get_checkpoint = Mock(return_value=None)

        mock_plan = Mock()
        mock_plan.items = [Mock(storage_index=0, type=LoadItemType.BYTE_IO)]
        mock_planner = Mock()
        mock_s3_stream(b"test checkpoint data from s3", reader)

        future = reader.read_data(mock_plan, mock_planner)
        future.wait()

        reader.client.get_checkpoint.assert_called_once_with(step=100, rank=0)
        mock_planner.load_bytes.assert_called_once()


class TestFindLatestCompleteStep(TestCase):
    def setUp(self):
        self.config = SageMakerCheckpointConfig(
            namespace="test-namespace",
            world_size=2,
            s3_tier_base_path="s3://test-bucket/checkpoints",
            save_to_s3=True,
        )

    @mock_aws_calls
    def test_find_latest_complete_step_with_prefix(self, *_):
        """Test finding latest complete step with S3 prefix"""
        reader = SageMakerTieredStorageReader(self.config)
        reader.region = "us-west-2"

        mock_pages = [
            {
                "CommonPrefixes": [
                    {"Prefix": "checkpoints/test-namespace/rank_0/step_100/"},
                    {"Prefix": "checkpoints/test-namespace/rank_0/step_200/"},
                    {"Prefix": "checkpoints/test-namespace/rank_0/step_300/"},
                ]
            }
        ]

        with patch("boto3.client", return_value=mock_s3_paginator(mock_pages)):
            result = reader._find_latest_complete_step()

        self.assertEqual(result, 300)

    @mock_aws_calls
    def test_find_latest_complete_step_bucket_only(self, *_):
        """Test finding latest complete step with bucket-only S3 path"""
        config = SageMakerCheckpointConfig(
            namespace="test-namespace", world_size=2, s3_tier_base_path="s3://test-bucket", save_to_s3=True
        )
        reader = SageMakerTieredStorageReader(config)
        reader.region = "us-west-2"

        mock_pages = [
            {
                "CommonPrefixes": [
                    {"Prefix": "test-namespace/rank_0/step_50/"},
                    {"Prefix": "test-namespace/rank_0/step_100/"},
                ]
            }
        ]

        with patch("boto3.client", return_value=mock_s3_paginator(mock_pages)):
            result = reader._find_latest_complete_step()

        self.assertEqual(result, 100)

    @mock_aws_calls
    def test_find_latest_complete_step_no_region(self, *_):
        """Test that method returns None when region is empty"""
        reader = SageMakerTieredStorageReader(self.config)
        reader.region = ""

        result = reader._find_latest_complete_step()
        self.assertIsNone(result)

    @mock_aws_calls
    def test_find_latest_complete_step_invalid_s3_path(self, *_):
        """Test that method returns None for invalid S3 path"""
        reader = SageMakerTieredStorageReader(self.config)
        reader.region = "us-west-2"

        # Directly modify the s3_tier_base_path to test invalid path handling
        reader.checkpoint_config.s3_tier_base_path = "invalid://not-s3"

        result = reader._find_latest_complete_step()
        self.assertIsNone(result)

    @mock_aws_calls
    def test_find_latest_complete_step_incomplete_ranks(self, *_):
        """Test finding steps when not all ranks have same steps"""
        reader = SageMakerTieredStorageReader(self.config)
        reader.region = "us-west-2"

        # Mock S3 client and paginator
        mock_s3_client = Mock()
        mock_paginator = Mock()
        mock_s3_client.get_paginator.return_value = mock_paginator

        # Mock different responses for different ranks
        def mock_paginate(Bucket, Prefix, Delimiter):  # noqa: N803 - Named params in actual invocation.
            if "rank_0" in Prefix:
                return [
                    {
                        "CommonPrefixes": [
                            {"Prefix": "checkpoints/test-namespace/rank_0/step_100/"},
                            {"Prefix": "checkpoints/test-namespace/rank_0/step_200/"},
                        ]
                    }
                ]
            elif "rank_1" in Prefix:
                return [{"CommonPrefixes": [{"Prefix": "checkpoints/test-namespace/rank_1/step_100/"}]}]
            return [{}]

        mock_paginator.paginate.side_effect = mock_paginate

        with patch("boto3.client", return_value=mock_s3_client):
            result = reader._find_latest_complete_step()

        # Should return 100 as it's complete across all ranks
        self.assertEqual(result, 100)

    @mock_aws_calls
    def test_find_latest_complete_step_no_steps(self, *_):
        """Test when no steps are found"""
        reader = SageMakerTieredStorageReader(self.config)
        reader.region = "us-west-2"

        with patch("boto3.client", return_value=mock_s3_paginator([{}])):
            result = reader._find_latest_complete_step()

        self.assertIsNone(result)


class TestReadMetadata(TestCase):
    def setUp(self):
        self.config = SageMakerCheckpointConfig(
            namespace="test-metadata",
            world_size=2,
            s3_tier_base_path="s3://test-bucket/checkpoints",
        )

    @mock_aws_calls
    def test_read_metadata_from_memory(self, *_):
        """Test reading metadata from in-memory storage"""
        reader = SageMakerTieredStorageReader(self.config, step=100)
        mock_metadata = create_mock_metadata()
        reader.client.get_checkpoint = Mock(return_value=pickle.dumps(mock_metadata))

        result = reader.read_metadata()

        reader.client.get_checkpoint.assert_called_once_with(step=100, metadata_index=0)
        self.assertIsInstance(result, Metadata)
        self.assertEqual(result.state_dict_metadata, mock_metadata.state_dict_metadata)

    @mock_aws_calls
    def test_read_metadata_from_memory_latest_step(self, *_):
        """Test reading metadata from latest step in memory"""
        reader = SageMakerTieredStorageReader(self.config, step=None)
        mock_metadata = create_mock_metadata()
        reader.client.get_checkpoint = Mock(return_value=pickle.dumps(mock_metadata))
        reader.client.get_latest_checkpoints = Mock(return_value=[100, 100])

        result = reader.read_metadata()

        reader.client.get_checkpoint.assert_called_once_with(step=100, metadata_index=0)
        self.assertIsInstance(result, Metadata)
        self.assertEqual(result.state_dict_metadata, mock_metadata.state_dict_metadata)

    @mock_aws_calls
    def test_read_metadata_from_s3_when_mem_fails(self, *_):
        """Test reading metadata from S3 when memory read fails"""
        reader = SageMakerTieredStorageReader(self.config, step=100)
        reader.client.get_checkpoint = Mock(return_value=None)
        mock_metadata = create_mock_metadata()
        mock_s3_stream(mock_metadata, reader)

        result = reader.read_metadata()

        reader.client.get_checkpoint.assert_called_once_with(step=100, metadata_index=0)
        reader.s3_client.create_read_stream.assert_called_once()
        self.assertIsInstance(result, Metadata)
        self.assertEqual(result.state_dict_metadata, mock_metadata.state_dict_metadata)

    @mock_aws_calls
    def test_read_metadata_from_s3_latest_step(self, *_):
        """Test reading metadata from latest step in S3"""
        reader = SageMakerTieredStorageReader(self.config, step=None)
        mock_metadata = create_mock_metadata()
        reader.client.get_checkpoint = Mock(return_value=None)
        reader.client.get_latest_checkpoints = Mock(return_value=[])

        with patch.object(reader, "_find_latest_complete_step", return_value=200):
            mock_s3_stream(mock_metadata, reader)
            result = reader.read_metadata()

        reader.s3_client.create_read_stream.assert_called_once()
        self.assertIsInstance(result, Metadata)
        self.assertEqual(result.state_dict_metadata, mock_metadata.state_dict_metadata)
        self.assertEqual(reader.step, 200)


class TestReadDataDeep(TestCase):
    """Deep tests for all branches of _read_data method."""

    def setUp(self):
        self.config, self.temp_dir = create_temp_config()

    def tearDown(self):
        cleanup_temp_dir(self.temp_dir)

    @mock_aws_calls
    def test_read_data_step_none_raises_error(self, *_):
        """Test _read_data raises error when step is None."""
        reader = SageMakerTieredStorageReader(self.config, step=None)
        reader.storage_data = {}

        future = reader.read_data(Mock(items=[]), Mock())
        with self.assertRaises(SageMakerTieredStorageError):
            future.wait()

    @mock_aws_calls
    def test_read_data_memory_success_byte_io(self, *_):
        """Test successful read from memory with BYTE_IO type."""
        reader = self._create_reader_with_storage(self.config, step=10)
        reader.client = Mock()
        reader.client.get_checkpoint.return_value = b"test data"

        future = reader.read_data(Mock(items=[self._create_mock_plan_item()]), Mock())
        future.wait()

        reader.client.get_checkpoint.assert_called_once_with(step=10, rank=0)

    @mock_aws_calls
    def test_read_data_memory_returns_none_fallback_to_s3(self, *_):
        """Test fallback to S3 when memory returns None."""
        config = SageMakerCheckpointConfig(namespace="test", world_size=1, s3_tier_base_path="s3://bucket/path")
        reader = self._create_reader_with_storage(config, step=10)
        reader.client = Mock()
        reader.client.get_checkpoint.return_value = None
        mock_s3_stream(b"s3 data", reader)

        future = reader.read_data(Mock(items=[self._create_mock_plan_item()]), Mock())
        future.wait()

        reader.s3_client.create_read_stream.assert_called_once()

    @mock_aws_calls
    def test_read_data_memory_fails_no_s3_raises_error(self, *_):
        """Test error raised when memory fails and no S3 configured."""
        reader = self._create_reader_with_storage(self.config, step=10)
        reader.client = Mock()
        reader.client.get_checkpoint.side_effect = RuntimeError("Memory error")
        reader.s3_base_path = None

        future = reader.read_data(Mock(items=[self._create_mock_plan_item()]), Mock())
        with self.assertRaises(SageMakerInMemoryTierError):
            future.wait()

    @mock_aws_calls
    def test_read_data_memory_fails_s3_succeeds(self, *_):
        """Test successful S3 fallback when memory fails."""
        config = SageMakerCheckpointConfig(namespace="test", world_size=1, s3_tier_base_path="s3://bucket/path")
        reader = self._create_reader_with_storage(config, step=10)
        reader.client = Mock()
        reader.client.get_checkpoint.side_effect = RuntimeError("Memory error")
        mock_s3_stream(b"s3 data", reader)

        future = reader.read_data(Mock(items=[self._create_mock_plan_item()]), Mock())
        future.wait()

        reader.s3_client.create_read_stream.assert_called_once()

    @mock_aws_calls
    def test_read_data_memory_success_tensor_type(self, *_):
        """Test successful read from memory with tensor type."""
        tensor_bytes = self._create_tensor_bytes()
        reader = self._create_reader_with_storage(self.config, step=10, data_length=len(tensor_bytes))
        reader.client = Mock()
        reader.client.get_checkpoint.return_value = tensor_bytes
        reader.s3_base_path = None

        mock_planner = Mock()
        mock_planner.resolve_tensor.return_value = torch.zeros(10)

        future = reader.read_data(
            Mock(items=[self._create_mock_plan_item(item_type=LoadItemType.TENSOR)]), mock_planner
        )
        future.wait()

        reader.client.get_checkpoint.assert_called_once_with(step=10, rank=0)
        mock_planner.resolve_tensor.assert_called_once()
        mock_planner.commit_tensor.assert_called_once()

    @mock_aws_calls
    def test_read_data_s3_fallback_tensor_type(self, *_):
        """Test S3 fallback with tensor type when memory fails."""
        config = SageMakerCheckpointConfig(namespace="test", world_size=1, s3_tier_base_path="s3://bucket/path")
        tensor_bytes = self._create_tensor_bytes()
        reader = self._create_reader_with_storage(config, step=10, data_length=len(tensor_bytes))
        reader.client = Mock()
        reader.client.get_checkpoint.return_value = None
        mock_s3_stream(tensor_bytes, reader)

        mock_planner = Mock()
        mock_planner.resolve_tensor.return_value = torch.zeros(10)

        future = reader.read_data(
            Mock(items=[self._create_mock_plan_item(item_type=LoadItemType.TENSOR)]), mock_planner
        )
        future.wait()

        reader.s3_client.create_read_stream.assert_called_once()
        mock_planner.resolve_tensor.assert_called_once()
        mock_planner.commit_tensor.assert_called_once()

    def _create_reader_with_storage(self, config, step, storage_index=0, data_length=10):
        """Helper to create reader with storage data."""
        reader = SageMakerTieredStorageReader(config, step=step)
        reader.storage_data = {storage_index: _SageMakerStorageInfo(rank=0, offset=0, length=data_length)}
        return reader

    def _create_mock_plan_item(self, storage_index=0, item_type=LoadItemType.BYTE_IO):
        """Helper to create mock plan item."""
        mock_item = Mock(storage_index=storage_index, type=item_type)
        if item_type != LoadItemType.BYTE_IO:
            mock_item.storage_offsets = [0]
            mock_item.lengths = [10]
        return mock_item

    def _create_tensor_bytes(self, size=10):
        """Helper to create serialized tensor bytes."""
        tensor_data = torch.randn(size)
        stream = io.BytesIO()
        torch.save(tensor_data, stream)
        return stream.getvalue()


# Helper functions
def mock_s3_stream(data, reader):
    """Mock S3 client stream for testing."""
    byte_stream = pickle.dumps(data) if not isinstance(data, bytes) else data
    mock_stream = Mock()
    mock_stream.read.side_effect = [byte_stream, None]
    mock_context = Mock()
    mock_context.__enter__ = Mock(return_value=mock_stream)
    mock_context.__exit__ = Mock(return_value=None)
    reader.s3_client = Mock()
    reader.s3_client.create_read_stream.return_value = mock_context


def create_mock_metadata():
    """Create mock metadata for testing."""
    return Metadata({"test_key": "test_value"})


def mock_s3_paginator(mock_pages):
    """Create mock S3 client with paginator."""
    mock_s3_client = Mock()
    mock_paginator = Mock()
    mock_s3_client.get_paginator.return_value = mock_paginator
    mock_paginator.paginate.return_value = mock_pages
    return mock_s3_client
