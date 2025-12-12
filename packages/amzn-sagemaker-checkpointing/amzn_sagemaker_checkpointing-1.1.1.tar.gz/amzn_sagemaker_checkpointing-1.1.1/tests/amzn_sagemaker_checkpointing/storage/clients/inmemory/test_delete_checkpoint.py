from unittest.mock import Mock

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
from amzn_sagemaker_checkpointing.storage.clients.inmemory.exceptions import InMemoryConfigError


class TestDeleteCheckpoint(InMemoryCheckpointClientTest):
    STEP = 42

    def setup_method(self):
        super().setup_method()
        self.checkpoint_path = f"v1/cp/checkpoints/{NAMESPACE}/{RANK}/{self.STEP}"

    def test_delete_checkpoint_success(self):
        # Arrange
        mock_response = Mock(status_code=200)
        self.mock_session.request.return_value = mock_response

        # Act
        self.client.delete_checkpoint(step=self.STEP)

        # Assert
        self.assert_http_adapter_and_retry_config()
        self.mock_session.request.assert_called_once_with(
            method="DELETE",
            url=f"{BASE_URL}/{self.checkpoint_path}",
            params=None,
            data=None,
            headers=None,
            timeout=InMemoryClientConfig.request_timeout,
        )

    def test_delete_checkpoint_with_custom_rank(self):
        # Arrange
        mock_response = Mock(status_code=200)
        self.mock_session.request.return_value = mock_response
        custom_rank = 5
        custom_path = f"v1/cp/checkpoints/{NAMESPACE}/{custom_rank}/{self.STEP}"

        # Act
        self.client.delete_checkpoint(step=self.STEP, rank=custom_rank)

        # Assert
        self.assert_http_adapter_and_retry_config()
        self.mock_session.request.assert_called_once_with(
            method="DELETE",
            url=f"{BASE_URL}/{custom_path}",
            params=None,
            data=None,
            headers=None,
            timeout=InMemoryClientConfig.request_timeout,
        )

    def test_delete_checkpoint_with_metadata_index(self):
        # Arrange
        mock_response = Mock(status_code=200)
        self.mock_session.request.return_value = mock_response
        metadata_index = 0
        metadata_rank = int(WORLD_SIZE) + metadata_index
        metadata_path = f"v1/cp/checkpoints/{NAMESPACE}/{metadata_rank}/{self.STEP}"

        # Act
        self.client.delete_checkpoint(step=self.STEP, metadata_index=metadata_index)

        # Assert
        self.assert_http_adapter_and_retry_config()
        self.mock_session.request.assert_called_once_with(
            method="DELETE",
            url=f"{BASE_URL}/{metadata_path}",
            params=None,
            data=None,
            headers=None,
            timeout=InMemoryClientConfig.request_timeout,
        )

    def test_delete_checkpoint_with_custom_timeout(self):
        # Arrange
        mock_response = Mock(status_code=200)
        self.mock_session.request.return_value = mock_response

        # Act
        self.client.delete_checkpoint(step=self.STEP, timeout=REQUEST_TIMEOUT)

        # Assert
        self.assert_http_adapter_and_retry_config()
        self.mock_session.request.assert_called_once_with(
            method="DELETE",
            url=f"{BASE_URL}/{self.checkpoint_path}",
            params=None,
            data=None,
            headers=None,
            timeout=REQUEST_TIMEOUT,
        )

    def test_delete_checkpoint_with_string_step(self):
        # Arrange
        mock_response = Mock(status_code=200)
        self.mock_session.request.return_value = mock_response
        step = "latest"
        path = f"v1/cp/checkpoints/{NAMESPACE}/{RANK}/{step}"

        # Act
        self.client.delete_checkpoint(step=step)

        # Assert
        self.assert_http_adapter_and_retry_config()
        self.mock_session.request.assert_called_once_with(
            method="DELETE",
            url=f"{BASE_URL}/{path}",
            params=None,
            data=None,
            headers=None,
            timeout=InMemoryClientConfig.request_timeout,
        )

    def test_delete_checkpoint_invalid_metadata_index(self):
        # Act & Assert
        with pytest.raises(InMemoryConfigError) as exc_info:
            self.client.delete_checkpoint(step=self.STEP, metadata_index=999)
        assert "Invalid metadata_index" in str(exc_info.value)

    @pytest.mark.parametrize("test_case", REQUEST_ERROR_CASES)
    def test_delete_checkpoint_request_errors(self, test_case):
        # Arrange
        if "exception" in test_case["response"]:
            self.mock_session.request.side_effect = test_case["response"]["exception"]
        else:
            mock_response = Mock()
            mock_response.status_code = test_case["response"]["status_code"]
            mock_response.text = test_case["response"]["text"]
            self.mock_session.request.return_value = mock_response

        # Act & Assert
        self.assert_request_error(test_case, self.client.delete_checkpoint, step=self.STEP)
