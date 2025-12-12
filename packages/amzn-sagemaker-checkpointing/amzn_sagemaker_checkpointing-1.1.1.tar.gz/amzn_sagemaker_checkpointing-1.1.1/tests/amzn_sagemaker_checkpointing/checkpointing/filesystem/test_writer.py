import os
import unittest
from unittest import TestCase
from unittest.mock import Mock, patch

from test_helpers import (
    DummyPlanner,
    DummySavePlan,
    cleanup_temp_dir,
    create_temp_config,
    mock_aws_calls,
)

from amzn_sagemaker_checkpointing.checkpointing.filesystem.exceptions import (
    SageMakerInMemoryTierError,
    SageMakerS3TierError,
    SageMakerTieredStorageError,
)
from amzn_sagemaker_checkpointing.checkpointing.filesystem.filesystem import SageMakerTieredStorageWriter
from amzn_sagemaker_checkpointing.config.sagemaker_checkpoint_config import SageMakerCheckpointConfig


class TestStepValueExtraction(TestCase):
    def test_explicit_step_precedence(self):
        """Test explicit step values always take precedence over path extraction."""
        self._assert_step_extraction(
            [
                (0, "/some/path", 0),
                (0, "/any/path/step_999", 0),
                (42, "/path/step_123/file", 42),
                (9999, "/step_0/checkpoint", 9999),
                (42, "/some/path/step_100/checkpoint", 42),
            ]
        )

    def test_step_from_path(self):
        """Test step extraction from various path formats."""
        self._assert_step_extraction_from_path(
            [
                ("/some/path/step_123/checkpoint", 123),
                ("/some/path/step_456", 456),
                ("/some/path/step_0/checkpoint", 0),
                ("/some/path/step_999999/checkpoint", 999999),
                (os.path.join("/some/path", "step_789", "checkpoint"), 789),
                ("/root/training/experiment_1/step_42/model.pt", 42),
                ("/very/long/nested/path/with/many/dirs/step_12345/checkpoint.bin", 12345),
                ("/path/with/step_100/nested/step_200/file.txt", 100),
                ("./relative/path/step_5/data", 5),
                ("/step_0/beginning", 0),
                ("/end/step_9999", 9999),
                ("/path/step_100/nested/step_200", 100),
                ("/path/step_100123/checkpoint", 100123),
                ("/root/parent/child/grandchild/step_42/file.txt", 42),
            ]
        )

    def test_invalid_paths(self):
        """Test step extraction with invalid path formats raises errors."""
        self._assert_raises_error(
            [
                "/no/step/pattern/here",
                "/path/step_/incomplete",
                "/path/step_abc/invalid_number",
                "",
                None,
                "/some/path/without/step",
                "/some/path/step_abc/checkpoint",
                "/some/path/step_/checkpoint",
                "/path/step_12.5/float",
            ]
        )

    def test_negative_step_in_path(self):
        """Test that negative step numbers in paths raise an error."""
        with self.assertRaises(SageMakerTieredStorageError):
            SageMakerTieredStorageWriter._get_step_val(-1, "/path/step_-5/negative")

    def _assert_step_extraction(self, test_cases):
        """Helper to assert step extraction for multiple test cases."""
        for *args, expected in test_cases:
            with self.subTest(args=args):
                result = SageMakerTieredStorageWriter._get_step_val(*args)
                self.assertEqual(result, expected)

    def _assert_step_extraction_from_path(self, test_cases):
        """Helper to assert step extraction from path (prepends -1 for step arg)."""
        self._assert_step_extraction([(-1, path, expected) for path, expected in test_cases])

    def _assert_raises_error(self, paths):
        """Helper to assert SageMakerTieredStorageError for invalid paths."""
        for path in paths:
            with self.subTest(path=path):
                with self.assertRaises(SageMakerTieredStorageError):
                    SageMakerTieredStorageWriter._get_step_val(-1, path)


class TestWriterInitialization(TestCase):
    def setUp(self):
        self.valid_config, self.temp_dir = create_temp_config(
            namespace="test-init",
            world_size=2,
            save_to_s3=True,
            save_to_disk=False,
        )

    def tearDown(self):
        cleanup_temp_dir(self.temp_dir)

    @mock_aws_calls
    def test_writer_initialization_with_various_steps(self, *_):
        """Test writer initialization with various step values."""
        step_test_cases = [
            # (path, explicit_step, expected_step)
            ("step_0", -1, 0),
            ("step_1", -1, 1),
            ("step_100", -1, 100),
            ("step_999999", -1, 999999),
            ("/path/to/step_42/checkpoint", -1, 42),
            ("any_path", 0, 0),
            ("any_path", 123, 123),
            ("step_999", 42, 42),  # Explicit step overrides path
        ]

        for path, explicit_step, expected_step in step_test_cases:
            with self.subTest(path=path, explicit_step=explicit_step):
                writer = SageMakerTieredStorageWriter(self.valid_config, path=path, step=explicit_step)
                self.assertEqual(writer.step, expected_step)
                self.assertEqual(writer.rank, 0)

    @mock_aws_calls
    @patch("torch.distributed.get_rank", return_value=3)
    @patch("torch.distributed.is_initialized", return_value=True)
    @patch("torch.distributed.is_available", return_value=True)
    def test_writer_initialization_different_ranks(self, *_):
        """Test writer initialization with different ranks."""
        writer = SageMakerTieredStorageWriter(self.valid_config, path="step_10", step=-1)
        self.assertEqual(writer.rank, 3)
        self.assertEqual(writer.step, 10)

    @mock_aws_calls
    def test_writer_initialization_distributed_not_initialized(self, *_):
        """Test writer initialization when distributed is not initialized."""
        writer = SageMakerTieredStorageWriter(self.valid_config, path="step_5", step=-1)
        self.assertEqual(writer.rank, 0)  # Should default to 0
        self.assertEqual(writer.step, 5)

    @mock_aws_calls
    def test_writer_initialization_distributed_not_available(self, *_):
        """Test writer initialization when distributed is not available."""
        writer = SageMakerTieredStorageWriter(self.valid_config, path="step_7", step=-1)
        self.assertEqual(writer.rank, 0)  # Should default to 0
        self.assertEqual(writer.step, 7)


class TestTieredWriter(TestCase):
    def setUp(self):
        self.config, self.temp_dir = create_temp_config()

    def tearDown(self):
        cleanup_temp_dir(self.temp_dir)

    @mock_aws_calls
    def test_init_with_valid_config(self, *_):
        """Test writer initialization with valid configuration."""
        writer = SageMakerTieredStorageWriter(checkpoint_config=self.config, path="/some/path", step=42)
        self.assertEqual(writer.step, 42)
        self.assertEqual(writer.rank, 0)

        writer = SageMakerTieredStorageWriter(checkpoint_config=self.config, path="/some/path/step_123/checkpoint")
        self.assertEqual(writer.step, 123)
        self.assertEqual(writer.rank, 0)

    def test_init_with_invalid_config(self):
        """Test writer initialization with invalid configuration raises errors."""
        invalid_config = SageMakerCheckpointConfig(namespace="", world_size=4)
        with self.assertRaises(SageMakerTieredStorageError):
            SageMakerTieredStorageWriter(checkpoint_config=invalid_config)

        invalid_config = SageMakerCheckpointConfig(namespace="test-namespace", world_size=0)
        with self.assertRaises(SageMakerTieredStorageError):
            SageMakerTieredStorageWriter(checkpoint_config=invalid_config)

    def test_init_with_invalid_step(self):
        """Test writer initialization with invalid step path raises error."""
        config, temp_dir = create_temp_config()
        with self.assertRaises(SageMakerTieredStorageError):
            SageMakerTieredStorageWriter(checkpoint_config=config, path="/no/step/path")

    @mock_aws_calls
    def test_write_data_success_mem(self, *_):
        """Test successful write to in-memory storage only."""
        writer = SageMakerTieredStorageWriter(checkpoint_config=self.config, path="step_10")

        mock_client = Mock()
        mock_client.put_checkpoint.return_value = None
        writer.client = mock_client
        writer.checkpoint_config.save_to_s3 = False

        results = writer.write_data(DummySavePlan(), DummyPlanner()).wait()

        mock_client.put_checkpoint.assert_called_once()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].index, 0)

    @mock_aws_calls
    def test_write_data_mem_and_s3(self, *_):
        """Test successful write to both in-memory and S3 storage."""
        writer = SageMakerTieredStorageWriter(checkpoint_config=self.config, path="step_20")

        mock_mem_client = Mock()
        mock_mem_client.put_checkpoint.return_value = None
        writer.client = mock_mem_client

        mock_s3_client = Mock()
        mock_s3_client.create_write_stream.return_value = _create_mock_s3_write_stream()
        writer.s3_client = mock_s3_client
        writer.checkpoint_config.save_to_s3 = True

        future = writer.write_data(DummySavePlan(), DummyPlanner())
        results = future.wait()

        mock_mem_client.put_checkpoint.assert_called_once()
        mock_s3_client.create_write_stream.assert_called_once()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].index, 0)

    @mock_aws_calls
    def test_write_data_mem_fails_s3_succeeds(self, *_):
        """Test in-memory write failure with successful S3 fallback."""
        writer = SageMakerTieredStorageWriter(checkpoint_config=self.config, path="step_30")

        mock_mem_client = Mock()
        mock_mem_client.put_checkpoint.side_effect = RuntimeError("Memory write failed")
        writer.client = mock_mem_client

        mock_s3_client = Mock()
        mock_s3_client.create_write_stream.return_value = _create_mock_s3_write_stream()
        writer.s3_client = mock_s3_client
        writer.checkpoint_config.save_to_s3 = True

        future = writer.write_data(DummySavePlan(), DummyPlanner())
        results = future.wait()

        mock_mem_client.put_checkpoint.assert_called_once()
        mock_s3_client.create_write_stream.assert_called_once()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].index, 0)

    @mock_aws_calls
    def test_write_data_mem_fails_s3_disabled(self, *_):
        """Test in-memory write failure when S3 is disabled raises SageMakerInMemoryTierError."""
        writer = SageMakerTieredStorageWriter(checkpoint_config=self.config, path="step_40")

        mock_mem_client = Mock()
        mock_mem_client.put_checkpoint.side_effect = RuntimeError("Memory write failed")
        writer.client = mock_mem_client
        writer.checkpoint_config.save_to_s3 = False
        writer.s3_client = Mock()

        future = writer.write_data(DummySavePlan(), DummyPlanner())
        with self.assertRaises(SageMakerInMemoryTierError):
            future.wait()

        mock_mem_client.put_checkpoint.assert_called_once()
        writer.s3_client.create_write_stream.assert_not_called()

    @mock_aws_calls
    def test_write_data_mem_succeeds_s3_fails(self, *_):
        """Test in-memory write succeeds but S3 write fails with retries."""
        writer = SageMakerTieredStorageWriter(checkpoint_config=self.config, path="step_50")

        mock_mem_client = Mock()
        mock_mem_client.put_checkpoint.return_value = None
        writer.client = mock_mem_client

        mock_s3_client = Mock()
        mock_s3_client.create_write_stream.side_effect = RuntimeError("S3 write failed")
        writer.s3_client = mock_s3_client
        writer.checkpoint_config.save_to_s3 = True

        future = writer.write_data(DummySavePlan(), DummyPlanner())
        with self.assertRaises(SageMakerS3TierError):
            future.wait()

        mock_mem_client.put_checkpoint.assert_called_once()
        # Assert called thrice due to retries. TODO - Retries are happening fast; check while refactoring
        self.assertEqual(mock_s3_client.create_write_stream.call_count, 3)

    @mock_aws_calls
    def test_write_data_both_fail(self, *_):
        """Test both in-memory and S3 writes fail with retries."""
        writer = SageMakerTieredStorageWriter(checkpoint_config=self.config, path="step_60")

        mock_mem_client = Mock()
        mock_mem_client.put_checkpoint.side_effect = RuntimeError("Memory write failed")
        writer.client = mock_mem_client

        mock_s3_client = Mock()
        mock_s3_client.create_write_stream.side_effect = RuntimeError("S3 write failed")
        writer.s3_client = mock_s3_client
        writer.checkpoint_config.save_to_s3 = True

        future = writer.write_data(DummySavePlan(), DummyPlanner())
        with self.assertRaises(SageMakerS3TierError):
            future.wait()

        mock_mem_client.put_checkpoint.assert_called_once()
        self.assertEqual(mock_s3_client.create_write_stream.call_count, 3)

    @mock_aws_calls
    def test_finish_mem_only_success(self, *_):
        """Test finish successfully writes metadata to in-memory only."""
        writer = SageMakerTieredStorageWriter(checkpoint_config=self.config, path="step_70")
        writer.client = Mock()
        writer.checkpoint_config.save_to_s3 = False

        writer.finish(_create_mock_metadata(), [[_create_mock_write_result(0)]])

        writer.client.put_checkpoint.assert_called_once()

    @mock_aws_calls
    def test_finish_mem_and_s3_success(self, *_):
        """Test finish successfully writes metadata to both in-memory and S3."""
        writer = SageMakerTieredStorageWriter(checkpoint_config=self.config, path="step_80")
        writer.client = Mock()
        writer.s3_client = Mock()
        writer.s3_client.create_write_stream.return_value = _create_mock_s3_write_stream()
        writer.checkpoint_config.save_to_s3 = True

        writer.finish(_create_mock_metadata(), [[_create_mock_write_result(0)]])

        writer.client.put_checkpoint.assert_called_once()
        writer.s3_client.create_write_stream.assert_called_once()

    @mock_aws_calls
    def test_finish_mem_fails_s3_disabled(self, *_):
        """Test finish raises error when in-memory fails and S3 is disabled."""
        writer = SageMakerTieredStorageWriter(checkpoint_config=self.config, path="step_90")
        writer.client = Mock()
        writer.client.put_checkpoint.side_effect = RuntimeError("Memory write failed")
        writer.checkpoint_config.save_to_s3 = False

        with self.assertRaises(SageMakerInMemoryTierError):
            writer.finish(_create_mock_metadata(), [[_create_mock_write_result(0)]])

    @mock_aws_calls
    def test_finish_mem_fails_s3_succeeds(self, *_):
        """Test finish succeeds when in-memory fails but S3 succeeds."""
        writer = SageMakerTieredStorageWriter(checkpoint_config=self.config, path="step_100")
        writer.client = Mock()
        writer.client.put_checkpoint.side_effect = RuntimeError("Memory write failed")
        writer.s3_client = Mock()
        writer.s3_client.create_write_stream.return_value = _create_mock_s3_write_stream()
        writer.checkpoint_config.save_to_s3 = True

        writer.finish(_create_mock_metadata(), [[_create_mock_write_result(0)]])

        writer.s3_client.create_write_stream.assert_called_once()

    @mock_aws_calls
    def test_finish_mem_succeeds_s3_fails(self, *_):
        """Test finish raises error when in-memory succeeds but S3 fails."""
        writer = SageMakerTieredStorageWriter(checkpoint_config=self.config, path="step_110")
        writer.client = Mock()
        writer.s3_client = Mock()
        writer.s3_client.create_write_stream.side_effect = RuntimeError("S3 write failed")
        writer.checkpoint_config.save_to_s3 = True

        with self.assertRaises(SageMakerS3TierError):
            writer.finish(_create_mock_metadata(), [[_create_mock_write_result(0)]])

    @mock_aws_calls
    def test_finish_with_multiple_results(self, *_):
        """Test finish correctly processes multiple write results."""
        writer = SageMakerTieredStorageWriter(checkpoint_config=self.config, path="step_120")
        writer.client = Mock()
        writer.checkpoint_config.save_to_s3 = False

        metadata = _create_mock_metadata()
        results = [
            [_create_mock_write_result(0), _create_mock_write_result(1)],
            [_create_mock_write_result(2), _create_mock_write_result(3)],
        ]

        writer.finish(metadata, results)

        self.assertEqual(len(metadata.storage_data), 4)


def _create_mock_s3_write_stream():
    """Create a mock S3 write stream for testing."""
    mock_write_stream = Mock()
    mock_write_stream.write.return_value = 1024
    mock_write_stream.__enter__ = Mock(return_value=mock_write_stream)
    mock_write_stream.__exit__ = Mock(return_value=False)
    return mock_write_stream


def _create_mock_metadata():
    """Create a mock Metadata object for testing."""
    from torch.distributed.checkpoint.metadata import Metadata

    return Metadata(state_dict_metadata={"model": "test"}, planner_data={}, storage_data={}, storage_meta=None)


def _create_mock_write_result(index):
    """Create a mock WriteResult for testing."""
    from torch.distributed.checkpoint.storage import WriteResult

    from amzn_sagemaker_checkpointing.checkpointing.filesystem.storage_info import _SageMakerStorageInfo

    return WriteResult(
        index=index, size_in_bytes=1024, storage_data=_SageMakerStorageInfo(rank=0, offset=0, length=1024)
    )


if __name__ == "__main__":
    unittest.main()
