from unittest.mock import Mock, patch

import pytest
from requests import ConnectionError, RequestException, Timeout

from amzn_sagemaker_checkpointing.config.in_memory_client import InMemoryClientConfig
from amzn_sagemaker_checkpointing.storage.clients.inmemory.exceptions import (
    InMemoryClientError,
    InMemoryConnectionError,
    InMemoryNameSpaceCreateError,
    InMemoryRequestError,
    InMemoryServerError,
    InMemoryTimeoutError,
)
from amzn_sagemaker_checkpointing.storage.clients.inmemory.inmemory_client import (
    InMemoryCheckpointClient,
)

BASE_URL = "http://ai-toolkit-gossip-headless.aws-hyperpod.svc.cluster.local:9200"
NAMESPACE = "test-namespace"
RANK = "0"
WORLD_SIZE = "1"
STEPS_RETAINED = 3
METADATA_FILE_COUNT = 1
TOTAL_RANKS = 2
STATUS_FORCELIST = [429, 500, 502, 503, 504]
ALLOWED_METHODS = ["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"]
REQUEST_RETRIES = 0
RETRY_BACKOFF = 1.5
REQUEST_TIMEOUT = 60.0
REQUEST_ERROR_CASES = [
    {
        "name": "client_error",
        "response": {"status_code": 409, "text": "Namespace conflict"},
        "expected_error_class": InMemoryClientError,
        "error_text": "Client error for",
    },
    {
        "name": "server_error",
        "response": {"status_code": 500, "text": "Internal Server Error"},
        "expected_error_class": InMemoryServerError,
        "error_text": "Server error for",
    },
    {
        "name": "connection_error",
        "response": {"exception": ConnectionError("Connection failed")},
        "expected_error_class": InMemoryConnectionError,
        "error_text": "Connection error",
    },
    {
        "name": "timeout_error",
        "response": {"exception": Timeout("Request timed out")},
        "expected_error_class": InMemoryTimeoutError,
        "error_text": "Timeout after",
    },
    {
        "name": "generic_request_error",
        "response": {"exception": RequestException("Generic request error")},
        "expected_error_class": InMemoryRequestError,
        "error_text": "Unhandled request error",
    },
]


class InMemoryCheckpointClientTest:
    def setup_method(self):
        self.mock_requests = patch(
            "amzn_sagemaker_checkpointing.storage.clients.inmemory.inmemory_client.requests"
        ).start()
        self.mock_adapter = patch(
            "amzn_sagemaker_checkpointing.storage.clients.inmemory.inmemory_client.HTTPAdapter"
        ).start()
        self.mock_retry = patch("amzn_sagemaker_checkpointing.storage.clients.inmemory.inmemory_client.Retry").start()
        self.mock_session = Mock()
        self.mock_requests.Session.return_value = self.mock_session
        self.mock_adapter_instance = Mock()
        self.mock_adapter.return_value = self.mock_adapter_instance
        self.client = InMemoryCheckpointClient(namespace=NAMESPACE, rank=RANK, world_size=WORLD_SIZE)

    def teardown_method(self):
        """Teardown method that runs after each test"""
        self.client.close()

    def assert_request_error(self, test_case, method_to_test, expected_wrapper_error=None, **kwargs):
        """
        Assert request error handling.
        Args:
            test_case: Error test case with expected_error_class and error_text
            method_to_test: Method to test
            expected_wrapper_error: If provided, verifies wrapper exception message
            kwargs: Additional arguments for method_to_test
        """
        if expected_wrapper_error:
            with pytest.raises(InMemoryNameSpaceCreateError) as exc_info:
                method_to_test(**kwargs)
            assert str(exc_info.value) == expected_wrapper_error
            assert isinstance(exc_info.value.__cause__, test_case["expected_error_class"])
            assert test_case["error_text"] in str(exc_info.value.__cause__)
        else:
            with pytest.raises(test_case["expected_error_class"]) as exc_info:
                method_to_test(**kwargs)
            assert test_case["error_text"] in str(exc_info.value)

    def assert_http_adapter_and_retry_config(self):
        self.mock_retry.assert_called_once_with(
            total=InMemoryClientConfig.request_retries,
            backoff_factor=InMemoryClientConfig.retry_backoff,
            status_forcelist=STATUS_FORCELIST,
            allowed_methods=ALLOWED_METHODS,
        )
        self.mock_adapter.assert_called_once_with(max_retries=self.mock_retry.return_value)
        self.mock_session.mount.assert_any_call("http://", self.mock_adapter_instance)
        self.mock_session.mount.assert_any_call("https://", self.mock_adapter_instance)
