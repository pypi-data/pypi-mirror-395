from unittest.mock import Mock

import pytest
from utils.test_base import (
    BASE_URL,
    REQUEST_ERROR_CASES,
    REQUEST_TIMEOUT,
    InMemoryCheckpointClientTest,
)

from amzn_sagemaker_checkpointing.config.in_memory_client import InMemoryClientConfig


class TestResetCluster(InMemoryCheckpointClientTest):
    def setup_method(self):
        super().setup_method()
        self.reset_path = "v1/cp/cluster/reset"

    @pytest.mark.parametrize(
        "params",
        [
            {"timeout": None},
            {"timeout": REQUEST_TIMEOUT},
        ],
    )
    def test_reset_cluster_success(self, params):
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        self.mock_session.request.return_value = mock_response

        # Act
        self.client.reset_cluster(**params)

        # Assert
        self.assert_http_adapter_and_retry_config()
        self.mock_session.request.assert_called_once_with(
            method="POST",
            url=f"{BASE_URL}/{self.reset_path}",
            params=None,
            data=None,
            headers=None,
            timeout=params["timeout"] or InMemoryClientConfig.request_timeout,
        )

    @pytest.mark.parametrize("test_case", REQUEST_ERROR_CASES)
    def test_reset_cluster_request_errors(self, test_case):
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
        self.assert_request_error(test_case, self.client.reset_cluster)
        self.mock_session.request.assert_called_once_with(
            method="POST",
            url=f"{BASE_URL}/{self.reset_path}",
            params=None,
            data=None,
            headers=None,
            timeout=InMemoryClientConfig.request_timeout,
        )
