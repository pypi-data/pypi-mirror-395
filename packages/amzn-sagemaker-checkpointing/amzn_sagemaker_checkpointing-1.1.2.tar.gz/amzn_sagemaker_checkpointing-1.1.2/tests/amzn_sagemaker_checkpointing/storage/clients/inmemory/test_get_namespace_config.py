from unittest.mock import Mock

import pytest
from utils.test_base import (
    BASE_URL,
    NAMESPACE,
    REQUEST_ERROR_CASES,
    REQUEST_TIMEOUT,
    InMemoryCheckpointClientTest,
)

from amzn_sagemaker_checkpointing.config.in_memory_client import InMemoryClientConfig
from amzn_sagemaker_checkpointing.storage.clients.inmemory.exceptions import InMemoryStorageError


class TestGetNamespaceConfig(InMemoryCheckpointClientTest):
    def setup_method(self):
        super().setup_method()
        self.namespace_path = f"v1/cp/namespaces/{NAMESPACE}"

    @pytest.mark.parametrize(
        "params",
        [
            {"timeout": None},
            {"timeout": REQUEST_TIMEOUT},
        ],
    )
    def test_get_namespace_config_success(self, params):
        # Arrange
        expected_response = {"steps_retained": 5}
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response
        self.mock_session.request.return_value = mock_response

        # Act
        result = self.client.get_namespace_config(**params)

        # Assert
        self.assert_http_adapter_and_retry_config()
        self.mock_session.request.assert_called_once_with(
            method="GET",
            url=f"{BASE_URL}/{self.namespace_path}",
            params=None,
            data=None,
            headers=None,
            timeout=params["timeout"] or InMemoryClientConfig.request_timeout,
        )
        assert result == expected_response

    def test_get_namespace_config_not_found(self):
        # Arrange
        mock_response = Mock(status_code=404)
        self.mock_session.request.return_value = mock_response

        # Act
        result = self.client.get_namespace_config()

        # Assert
        self.assert_http_adapter_and_retry_config()
        self.mock_session.request.assert_called_once_with(
            method="GET",
            url=f"{BASE_URL}/{self.namespace_path}",
            params=None,
            data=None,
            headers=None,
            timeout=InMemoryClientConfig.request_timeout,
        )
        assert result == {}

    def test_get_namespace_config_json_decode_error(self):
        # Arrange
        mock_response = Mock(status_code=200)
        mock_response.json.side_effect = ValueError("Invalid JSON")
        self.mock_session.request.return_value = mock_response

        # Act & Assert
        with pytest.raises(InMemoryStorageError) as exc_info:
            self.client.get_namespace_config()

        assert "Failed to decode JSON for namespace config" in str(exc_info.value)
        self.assert_http_adapter_and_retry_config()
        self.mock_session.request.assert_called_once_with(
            method="GET",
            url=f"{BASE_URL}/{self.namespace_path}",
            params=None,
            data=None,
            headers=None,
            timeout=InMemoryClientConfig.request_timeout,
        )

    @pytest.mark.parametrize("test_case", REQUEST_ERROR_CASES)
    def test_get_namespace_config_request_errors(self, test_case):
        # Arrange
        if "exception" in test_case["response"]:
            self.mock_session.request.side_effect = test_case["response"]["exception"]
        else:
            mock_response = Mock()
            mock_response.status_code = test_case["response"]["status_code"]
            mock_response.text = test_case["response"]["text"]
            self.mock_session.request.return_value = mock_response

        # Act & Assert
        self.assert_http_adapter_and_retry_config()
        self.assert_request_error(test_case, self.client.get_namespace_config)
        self.mock_session.request.assert_called_once_with(
            method="GET",
            url=f"{BASE_URL}/{self.namespace_path}",
            params=None,
            data=None,
            headers=None,
            timeout=InMemoryClientConfig.request_timeout,
        )
