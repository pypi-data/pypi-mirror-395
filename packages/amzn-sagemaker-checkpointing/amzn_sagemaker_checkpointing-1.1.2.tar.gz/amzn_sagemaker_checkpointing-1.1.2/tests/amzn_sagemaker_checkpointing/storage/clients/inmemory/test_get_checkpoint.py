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


class TestGetCheckpoint(InMemoryCheckpointClientTest):
    # Constants
    STEP = 42
    TEST_CONTENT = b"test checkpoint data"
    MOCK_CHECKSUM = "mock-checksum"
    MOCK_ENCODED_CHECKSUM = "bW9jay1jaGVja3N1bQ=="  # base64 of mock-checksum
    CONTENT_LENGTH = len(TEST_CONTENT)
    RESPONSE_HEADERS: ClassVar[dict[str, str]] = {
        "Content-Length": str(CONTENT_LENGTH),
        "Shard-Meta": '{"checksum": "bW9jay1jaGVja3N1bQ==", "algorithm": "xxh3_128"}',
    }

    def setup_method(self):
        super().setup_method()
        self.checkpoint_path = f"v1/cp/checkpoints/{NAMESPACE}/{RANK}/{self.STEP}"

        # Mock checksum functions
        self.mock_decode_base_64 = patch(
            "amzn_sagemaker_checkpointing.storage.clients.inmemory.inmemory_client.decode_base_64"
        ).start()
        self.mock_hash_xxh3_128 = patch(
            "amzn_sagemaker_checkpointing.storage.clients.inmemory.inmemory_client.hash_xxh3_128"
        ).start()
        self.mock_decode_base_64.return_value = self.MOCK_CHECKSUM
        self.mock_hash_xxh3_128.return_value = self.MOCK_CHECKSUM

    def test_get_checkpoint_success(self):
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = self.TEST_CONTENT
        mock_response.headers = self.RESPONSE_HEADERS
        self.mock_session.request.return_value = mock_response

        # Act
        result = self.client.get_checkpoint(step=self.STEP)

        # Assert
        self.assert_http_adapter_and_retry_config()
        self.mock_hash_xxh3_128.assert_called_once_with(self.TEST_CONTENT)
        self.mock_decode_base_64.assert_called_once_with(self.MOCK_ENCODED_CHECKSUM)
        self.mock_session.request.assert_called_once_with(
            method="GET",
            url=f"{BASE_URL}/{self.checkpoint_path}",
            params=None,
            data=None,
            headers=None,
            timeout=InMemoryClientConfig.request_timeout,
        )
        assert result == self.TEST_CONTENT

    def test_get_checkpoint_with_custom_rank(self):
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = self.TEST_CONTENT
        mock_response.headers = self.RESPONSE_HEADERS
        self.mock_session.request.return_value = mock_response
        custom_rank = 5
        custom_path = f"v1/cp/checkpoints/{NAMESPACE}/{custom_rank}/{self.STEP}"

        # Act
        result = self.client.get_checkpoint(step=self.STEP, rank=custom_rank)

        # Assert
        self.assert_http_adapter_and_retry_config()
        self.mock_session.request.assert_called_once_with(
            method="GET",
            url=f"{BASE_URL}/{custom_path}",
            params=None,
            data=None,
            headers=None,
            timeout=InMemoryClientConfig.request_timeout,
        )
        assert result == self.TEST_CONTENT

    def test_get_checkpoint_with_metadata_index(self):
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = self.TEST_CONTENT
        mock_response.headers = self.RESPONSE_HEADERS
        self.mock_session.request.return_value = mock_response
        metadata_index = 0
        metadata_rank = int(WORLD_SIZE) + metadata_index
        metadata_path = f"v1/cp/checkpoints/{NAMESPACE}/{metadata_rank}/{self.STEP}"

        # Act
        result = self.client.get_checkpoint(step=self.STEP, metadata_index=metadata_index)

        # Assert
        self.assert_http_adapter_and_retry_config()
        self.mock_session.request.assert_called_once_with(
            method="GET",
            url=f"{BASE_URL}/{metadata_path}",
            params=None,
            data=None,
            headers=None,
            timeout=InMemoryClientConfig.request_timeout,
        )
        assert result == self.TEST_CONTENT

    def test_get_checkpoint_with_custom_timeout(self):
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = self.TEST_CONTENT
        mock_response.headers = self.RESPONSE_HEADERS
        self.mock_session.request.return_value = mock_response

        # Act
        result = self.client.get_checkpoint(step=self.STEP, timeout=REQUEST_TIMEOUT)

        # Assert
        self.assert_http_adapter_and_retry_config()
        self.mock_session.request.assert_called_once_with(
            method="GET",
            url=f"{BASE_URL}/{self.checkpoint_path}",
            params=None,
            data=None,
            headers=None,
            timeout=REQUEST_TIMEOUT,
        )
        assert result == self.TEST_CONTENT

    def test_get_checkpoint_not_found(self):
        # Arrange
        mock_response = Mock(status_code=404)
        self.mock_session.request.return_value = mock_response

        # Act
        result = self.client.get_checkpoint(step=self.STEP)

        # Assert
        self.assert_http_adapter_and_retry_config()
        self.mock_session.request.assert_called_once_with(
            method="GET",
            url=f"{BASE_URL}/{self.checkpoint_path}",
            params=None,
            data=None,
            headers=None,
            timeout=InMemoryClientConfig.request_timeout,
        )
        assert result is None

    def test_get_checkpoint_checksum_mismatch(self):
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = self.TEST_CONTENT
        mock_response.headers = self.RESPONSE_HEADERS
        self.mock_session.request.return_value = mock_response
        self.mock_hash_xxh3_128.return_value = "different-checksum"

        # Act & Assert
        with pytest.raises(InMemoryStorageError) as exc_info:
            self.client.get_checkpoint(step=self.STEP)
        assert "Checksum mismatch in response" in str(exc_info.value)

    def test_get_checkpoint_content_length_mismatch(self):
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = self.TEST_CONTENT
        mock_response.headers = {
            "Content-Length": str(self.CONTENT_LENGTH + 1),  # Wrong content length
            "Shard-Meta": '{"checksum": "bW9jay1jaGVja3N1bQ==", "algorithm": "xxh3_128"}',
        }
        self.mock_session.request.return_value = mock_response

        # Act & Assert
        with pytest.raises(InMemoryStorageError) as exc_info:
            self.client.get_checkpoint(step=self.STEP)
        assert "Content length mismatch" in str(exc_info.value)

    def test_get_checkpoint_invalid_metadata_index(self):
        # Act & Assert
        with pytest.raises(InMemoryConfigError) as exc_info:
            self.client.get_checkpoint(step=self.STEP, metadata_index=999)
        assert "Invalid metadata_index" in str(exc_info.value)

    @pytest.mark.parametrize("test_case", REQUEST_ERROR_CASES)
    def test_get_checkpoint_request_errors(self, test_case):
        # Arrange
        if "exception" in test_case["response"]:
            self.mock_session.request.side_effect = test_case["response"]["exception"]
        else:
            mock_response = Mock()
            mock_response.status_code = test_case["response"]["status_code"]
            mock_response.text = test_case["response"]["text"]
            self.mock_session.request.return_value = mock_response

        # Act & Assert
        self.assert_request_error(test_case, self.client.get_checkpoint, step=self.STEP)
