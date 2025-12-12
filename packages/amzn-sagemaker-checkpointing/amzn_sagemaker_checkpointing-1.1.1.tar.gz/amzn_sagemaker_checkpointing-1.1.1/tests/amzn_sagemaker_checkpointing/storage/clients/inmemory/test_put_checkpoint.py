from io import BytesIO
from typing import ClassVar
from unittest.mock import Mock, patch

import pytest
from utils.test_base import (
    BASE_URL,
    NAMESPACE,
    RANK,
    REQUEST_ERROR_CASES,
    REQUEST_TIMEOUT,
    WORLD_SIZE,
    InMemoryCheckpointClientTest,
)

from amzn_sagemaker_checkpointing.config.in_memory_client import InMemoryClientConfig
from amzn_sagemaker_checkpointing.storage.clients.inmemory.exceptions import InMemoryConfigError, InMemoryStorageError


class TestPutCheckpoint(InMemoryCheckpointClientTest):
    # Constants
    STEP = 42
    TEST_DATA = b"test checkpoint data"
    MOCK_CHECKSUM = "mock-checksum"
    MOCK_ENCODED_CHECKSUM = "bW9jay1jaGVja3N1bQ=="  # base64 of mock-checksum
    CHECKSUM_ALGORITHM = "xxh3_128"
    SHARD_META_HEADER: ClassVar[dict[str, str]] = {
        "Shard-Meta": '{"checksum": "bW9jay1jaGVja3N1bQ==", "algorithm": "xxh3_128"}'
    }

    def setup_method(self):
        super().setup_method()
        self.checkpoint_path = f"v1/cp/checkpoints/{NAMESPACE}/{RANK}/{self.STEP}"

        # Mock checksum module
        self.mock_encode_base_64 = patch(
            "amzn_sagemaker_checkpointing.storage.clients.inmemory.inmemory_client.encode_base_64"
        ).start()
        self.mock_hash_xxh3_128 = patch(
            "amzn_sagemaker_checkpointing.storage.clients.inmemory.inmemory_client.hash_xxh3_128"
        ).start()
        self.mock_encode_base_64.return_value = self.MOCK_ENCODED_CHECKSUM
        self.mock_hash_xxh3_128.return_value = self.MOCK_CHECKSUM

    def test_put_checkpoint_with_bytes_data(self):
        # Arrange
        mock_response = Mock(status_code=200)
        self.mock_session.request.return_value = mock_response

        # Act
        self.client.put_checkpoint(step=self.STEP, data=self.TEST_DATA)

        # Assert
        self.assert_http_adapter_and_retry_config()
        self.mock_hash_xxh3_128.assert_called_once_with(self.TEST_DATA)
        self.mock_encode_base_64.assert_called_once_with(self.MOCK_CHECKSUM)
        self.mock_session.request.assert_called_once_with(
            method="POST",
            url=f"{BASE_URL}/{self.checkpoint_path}",
            data=self.TEST_DATA,
            headers=self.SHARD_META_HEADER,
            params=None,
            timeout=InMemoryClientConfig.request_timeout,
        )

    def test_put_checkpoint_with_file_path(self):
        # Arrange
        mock_response = Mock(status_code=200)
        self.mock_session.request.return_value = mock_response
        test_file_path = "/path/to/checkpoint"
        mock_file = BytesIO(self.TEST_DATA)

        with patch("builtins.open", return_value=mock_file) as mock_open:
            # Act
            self.client.put_checkpoint(step=self.STEP, data=test_file_path)

            # Assert
            mock_open.assert_called_once_with(test_file_path, "rb")
            self.assert_http_adapter_and_retry_config()
            self.mock_hash_xxh3_128.assert_called_once_with(test_file_path)
            self.mock_encode_base_64.assert_called_once_with(self.MOCK_CHECKSUM)
            self.mock_session.request.assert_called_once_with(
                method="POST",
                url=f"{BASE_URL}/{self.checkpoint_path}",
                data=mock_file,
                headers=self.SHARD_META_HEADER,
                params=None,
                timeout=InMemoryClientConfig.request_timeout,
            )

    def test_put_checkpoint_with_file_object(self):
        # Arrange
        mock_response = Mock(status_code=200)
        self.mock_session.request.return_value = mock_response
        file_obj = BytesIO(self.TEST_DATA)

        # Act
        self.client.put_checkpoint(step=self.STEP, data=file_obj)

        # Assert
        self.assert_http_adapter_and_retry_config()
        self.mock_hash_xxh3_128.assert_called_once_with(file_obj)
        self.mock_encode_base_64.assert_called_once_with(self.MOCK_CHECKSUM)
        self.mock_session.request.assert_called_once_with(
            method="POST",
            url=f"{BASE_URL}/{self.checkpoint_path}",
            data=file_obj,
            headers=self.SHARD_META_HEADER,
            params=None,
            timeout=InMemoryClientConfig.request_timeout,
        )

    def test_put_checkpoint_with_custom_rank(self):
        # Arrange
        mock_response = Mock(status_code=200)
        self.mock_session.request.return_value = mock_response
        custom_rank = 5
        custom_path = f"v1/cp/checkpoints/{NAMESPACE}/{custom_rank}/{self.STEP}"

        # Act
        self.client.put_checkpoint(step=self.STEP, data=self.TEST_DATA, rank=custom_rank)

        # Assert
        self.assert_http_adapter_and_retry_config()
        self.mock_session.request.assert_called_once_with(
            method="POST",
            url=f"{BASE_URL}/{custom_path}",
            data=self.TEST_DATA,
            headers=self.SHARD_META_HEADER,
            params=None,
            timeout=InMemoryClientConfig.request_timeout,
        )

    def test_put_checkpoint_with_metadata_index(self):
        # Arrange
        mock_response = Mock(status_code=200)
        self.mock_session.request.return_value = mock_response
        metadata_index = 0
        metadata_rank = int(WORLD_SIZE) + metadata_index
        metadata_path = f"v1/cp/checkpoints/{NAMESPACE}/{metadata_rank}/{self.STEP}"  # hardcoded rank as 1

        # Act
        self.client.put_checkpoint(step=self.STEP, data=self.TEST_DATA, metadata_index=metadata_index)

        # Assert
        self.assert_http_adapter_and_retry_config()
        self.mock_session.request.assert_called_once_with(
            method="POST",
            url=f"{BASE_URL}/{metadata_path}",
            data=self.TEST_DATA,
            headers=self.SHARD_META_HEADER,
            params=None,
            timeout=InMemoryClientConfig.request_timeout,
        )

    def test_put_checkpoint_with_custom_timeout(self):
        # Arrange
        mock_response = Mock(status_code=200)
        self.mock_session.request.return_value = mock_response

        # Act
        self.client.put_checkpoint(step=self.STEP, data=self.TEST_DATA, timeout=REQUEST_TIMEOUT)

        # Assert
        self.assert_http_adapter_and_retry_config()
        self.mock_session.request.assert_called_once_with(
            method="POST",
            url=f"{BASE_URL}/{self.checkpoint_path}",
            data=self.TEST_DATA,
            headers=self.SHARD_META_HEADER,
            params=None,
            timeout=REQUEST_TIMEOUT,
        )

    def test_put_checkpoint_invalid_metadata_index(self):
        # Act & Assert
        with pytest.raises(InMemoryConfigError) as exc_info:
            self.client.put_checkpoint(step=self.STEP, data=self.TEST_DATA, metadata_index=999)
        assert "Invalid metadata_index" in str(exc_info.value)

    def test_put_checkpoint_file_not_found(self):
        # Act & Assert
        test_file_path = "/non_existent_path"
        with patch("builtins.open", side_effect=FileNotFoundError("Mocked File Not Found")) as mock_open:
            with pytest.raises(InMemoryStorageError) as exc_info:
                self.client.put_checkpoint(step=self.STEP, data=test_file_path)
            mock_open.assert_called_once_with(test_file_path, "rb")
        assert str(exc_info.value) == f"Error opening file: {test_file_path}"

    @pytest.mark.parametrize("test_case", REQUEST_ERROR_CASES)
    def test_put_checkpoint_request_errors(self, test_case):
        # Arrange
        if "exception" in test_case["response"]:
            self.mock_session.request.side_effect = test_case["response"]["exception"]
        else:
            mock_response = Mock()
            mock_response.status_code = test_case["response"]["status_code"]
            mock_response.text = test_case["response"]["text"]
            self.mock_session.request.return_value = mock_response

        # Act & Assert
        self.assert_request_error(test_case, self.client.put_checkpoint, step=self.STEP, data=self.TEST_DATA)
