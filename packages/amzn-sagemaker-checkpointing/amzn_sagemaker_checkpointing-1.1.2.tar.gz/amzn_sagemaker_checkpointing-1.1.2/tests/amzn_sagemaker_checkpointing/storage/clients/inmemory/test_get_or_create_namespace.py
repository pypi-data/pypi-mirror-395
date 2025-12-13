from unittest.mock import Mock, call

import pytest
from utils.test_base import (
    BASE_URL,
    NAMESPACE,
    REQUEST_ERROR_CASES,
    STEPS_RETAINED,
    TOTAL_RANKS,
    InMemoryCheckpointClientTest,
)

from amzn_sagemaker_checkpointing.config.in_memory_client import InMemoryClientConfig


class TestGetOrCreateNameSpace(InMemoryCheckpointClientTest):
    def setup_method(self):
        super().setup_method()
        self.namespace_path = f"v1/cp/namespaces/{NAMESPACE}"
        self.expected_error = f"Error getting existing namespace (or) creating a new one, " f"with name:{NAMESPACE}"

    @pytest.mark.parametrize(
        "params, expected_calls",
        [
            # Default timeout case
            (
                {"timeout": None},
                [
                    call(
                        method="GET",
                        url=f"{BASE_URL}/v1/cp/namespaces/{NAMESPACE}",
                        params=None,
                        data=None,
                        headers=None,
                        timeout=InMemoryClientConfig.request_timeout,
                    )
                ],
            ),
            # Custom timeout case
            (
                {"timeout": 30.0},
                [
                    call(
                        method="GET",
                        url=f"{BASE_URL}/v1/cp/namespaces/{NAMESPACE}",
                        params=None,
                        data=None,
                        headers=None,
                        timeout=30.0,
                    )
                ],
            ),
        ],
    )
    def test_namespace_exists(self, params, expected_calls):
        expected_response = {"namespace": NAMESPACE}
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response
        self.mock_session.request.return_value = mock_response
        result = self.client.get_or_create_namespace(**params)
        self.assert_http_adapter_and_retry_config()
        self.mock_session.request.assert_has_calls(expected_calls)
        assert self.mock_session.request.call_count == len(expected_calls)
        assert result == expected_response

    def test_namespace_doesnt_exist(self):
        mock_success_response = Mock(status_code=200)
        mock_success_response.json.return_value = {"namespace": NAMESPACE}
        self.mock_session.request.side_effect = [
            Mock(status_code=404),  # First GET -> 404
            Mock(status_code=200),  # POST -> 200
            mock_success_response,  # Final GET -> 200
        ]
        result = self.client.get_or_create_namespace()
        self.assert_http_adapter_and_retry_config()
        expected_calls = [
            # First GET attempt
            call(
                method="GET",
                url=f"{BASE_URL}/{self.namespace_path}",
                params=None,
                data=None,
                headers=None,
                timeout=InMemoryClientConfig.request_timeout,
            ),
            # POST to create namespace
            call(
                method="POST",
                url=f"{BASE_URL}/{self.namespace_path}",
                params={
                    "num_ranks": TOTAL_RANKS,
                    "steps_retained": STEPS_RETAINED,
                },
                data=None,
                headers=None,
                timeout=InMemoryClientConfig.request_timeout,
            ),
            # Final GET
            call(
                method="GET",
                url=f"{BASE_URL}/{self.namespace_path}",
                params=None,
                data=None,
                headers=None,
                timeout=InMemoryClientConfig.request_timeout,
            ),
        ]
        self.mock_session.request.assert_has_calls(expected_calls)
        assert self.mock_session.request.call_count == 3
        assert result == {"namespace": NAMESPACE}

    @pytest.mark.parametrize("test_case", REQUEST_ERROR_CASES)
    def test_get_namespace_errors(self, test_case):
        if "exception" in test_case["response"]:
            self.mock_session.request.side_effect = test_case["response"]["exception"]
        else:
            mock_response = Mock()
            mock_response.status_code = test_case["response"]["status_code"]
            mock_response.text = test_case["response"]["text"]
            self.mock_session.request.return_value = mock_response
        self.assert_http_adapter_and_retry_config()
        self.assert_request_error(test_case, self.client.get_or_create_namespace, self.expected_error)
        self.mock_session.request.assert_called_once_with(
            method="GET",
            url=f"{BASE_URL}/{self.namespace_path}",
            params=None,
            data=None,
            headers=None,
            timeout=InMemoryClientConfig.request_timeout,
        )

    @pytest.mark.parametrize("test_case", REQUEST_ERROR_CASES)
    def test_post_namespace_errors(self, test_case):
        mock_get_response = Mock(status_code=404)
        if "exception" in test_case["response"]:
            self.mock_session.request.side_effect = [
                mock_get_response,
                test_case["response"]["exception"],
            ]
        else:
            mock_post_response = Mock()
            mock_post_response.status_code = test_case["response"]["status_code"]
            mock_post_response.text = test_case["response"]["text"]
            self.mock_session.request.side_effect = [
                mock_get_response,
                mock_post_response,
            ]
        self.assert_http_adapter_and_retry_config()
        self.assert_request_error(test_case, self.client.get_or_create_namespace, self.expected_error)
        expected_calls = [
            # First GET attempt (404)
            call(
                method="GET",
                url=f"{BASE_URL}/{self.namespace_path}",
                params=None,
                data=None,
                headers=None,
                timeout=InMemoryClientConfig.request_timeout,
            ),
            # POST attempt that fails
            call(
                method="POST",
                url=f"{BASE_URL}/{self.namespace_path}",
                params={
                    "num_ranks": TOTAL_RANKS,
                    "steps_retained": STEPS_RETAINED,
                },
                data=None,
                headers=None,
                timeout=InMemoryClientConfig.request_timeout,
            ),
        ]
        self.mock_session.request.assert_has_calls(expected_calls)
        assert self.mock_session.request.call_count == 2

    @pytest.mark.parametrize("test_case", REQUEST_ERROR_CASES)
    def test_get_namespace_errors_after_post(self, test_case):
        mock_get_404_response = Mock(status_code=404)
        mock_post_response = Mock(status_code=200)
        if "exception" in test_case["response"]:
            self.mock_session.request.side_effect = [
                mock_get_404_response,
                mock_post_response,
                test_case["response"]["exception"],
            ]
        else:
            mock_final_get_response = Mock()
            mock_final_get_response.status_code = test_case["response"]["status_code"]
            mock_final_get_response.text = test_case["response"]["text"]
            self.mock_session.request.side_effect = [
                mock_get_404_response,
                mock_post_response,
                mock_final_get_response,
            ]
        self.assert_http_adapter_and_retry_config()
        self.assert_request_error(test_case, self.client.get_or_create_namespace, self.expected_error)
        expected_calls = [
            call(
                method="GET",
                url=f"{BASE_URL}/{self.namespace_path}",
                params=None,
                data=None,
                headers=None,
                timeout=InMemoryClientConfig.request_timeout,
            ),
            call(
                method="POST",
                url=f"{BASE_URL}/{self.namespace_path}",
                params={
                    "num_ranks": TOTAL_RANKS,
                    "steps_retained": STEPS_RETAINED,
                },
                data=None,
                headers=None,
                timeout=InMemoryClientConfig.request_timeout,
            ),
            call(
                method="GET",
                url=f"{BASE_URL}/{self.namespace_path}",
                params=None,
                data=None,
                headers=None,
                timeout=InMemoryClientConfig.request_timeout,
            ),
        ]
        self.mock_session.request.assert_has_calls(expected_calls)
        assert self.mock_session.request.call_count == 3

    def test_get_namespace_json_decode_error(self):
        mock_response = Mock(status_code=200)
        mock_response.json.side_effect = ValueError("Invalid JSON")
        self.mock_session.request.return_value = mock_response

        test_case = {
            "expected_error_class": ValueError,
            "error_text": "Invalid JSON",
        }
        self.assert_http_adapter_and_retry_config()
        self.assert_request_error(test_case, self.client.get_or_create_namespace, self.expected_error)
        self.mock_session.request.assert_called_once_with(
            method="GET",
            url=f"{BASE_URL}/{self.namespace_path}",
            params=None,
            data=None,
            headers=None,
            timeout=InMemoryClientConfig.request_timeout,
        )
