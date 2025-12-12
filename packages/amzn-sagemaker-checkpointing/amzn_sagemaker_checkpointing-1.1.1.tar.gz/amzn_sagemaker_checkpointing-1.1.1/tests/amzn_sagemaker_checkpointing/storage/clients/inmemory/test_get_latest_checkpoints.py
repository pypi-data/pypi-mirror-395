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


class TestGetLatestCheckpoints(InMemoryCheckpointClientTest):
    def setup_method(self):
        super().setup_method()
        self.checkpoints_path = f"v1/cp/checkpoints/{NAMESPACE}/latest"

    @pytest.mark.parametrize(
        "params, api_steps, expected_steps",
        [
            # Default limit, ordered steps
            ({"limit": 5, "timeout": None}, ["10", "8", "6", "4", "2"], [10, 8, 6, 4, 2]),
            # Custom limit
            ({"limit": 2, "timeout": None}, ["10", "8"], [10, 8]),
            # Custom timeout
            ({"limit": 5, "timeout": REQUEST_TIMEOUT}, ["10", "8", "6", "4", "2"], [10, 8, 6, 4, 2]),
            # Unordered steps
            ({"limit": 5, "timeout": None}, ["4", "8", "2", "10", "6"], [10, 8, 6, 4, 2]),
        ],
    )
    def test_get_latest_checkpoints_success(self, params, api_steps, expected_steps):
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = api_steps
        self.mock_session.request.return_value = mock_response

        # Act
        result = self.client.get_latest_checkpoints(**params)

        # Assert
        self.assert_http_adapter_and_retry_config()
        self.mock_session.request.assert_called_once_with(
            method="GET",
            url=f"{BASE_URL}/{self.checkpoints_path}",
            params={"limit": params["limit"]},
            data=None,
            headers=None,
            timeout=params["timeout"] or InMemoryClientConfig.request_timeout,
        )
        assert result == expected_steps

    @pytest.mark.parametrize("test_case", REQUEST_ERROR_CASES)
    def test_get_latest_checkpoints_request_errors(self, test_case):
        # Arrange
        if "exception" in test_case["response"]:
            self.mock_session.request.side_effect = test_case["response"]["exception"]
        else:
            mock_response = Mock()
            mock_response.status_code = test_case["response"]["status_code"]
            mock_response.text = test_case["response"]["text"]
            self.mock_session.request.return_value = mock_response

        # Act
        result = self.client.get_latest_checkpoints()

        # Assert
        self.assert_http_adapter_and_retry_config()
        self.mock_session.request.assert_called_once_with(
            method="GET",
            url=f"{BASE_URL}/{self.checkpoints_path}",
            params={"limit": 5},
            data=None,
            headers=None,
            timeout=InMemoryClientConfig.request_timeout,
        )
        assert result == []

    def test_get_latest_checkpoints_json_decode_error(self):
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        self.mock_session.request.return_value = mock_response

        # Act
        result = self.client.get_latest_checkpoints()

        # Assert
        self.assert_http_adapter_and_retry_config()
        self.mock_session.request.assert_called_once_with(
            method="GET",
            url=f"{BASE_URL}/{self.checkpoints_path}",
            params={"limit": 5},
            data=None,
            headers=None,
            timeout=InMemoryClientConfig.request_timeout,
        )
        assert result == []
