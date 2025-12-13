# Copyright 2025 Amazon.com, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import logging
from typing import Any, BinaryIO, Union

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError, RequestException, Timeout
from urllib3.util.retry import Retry

from amzn_sagemaker_checkpointing.config.in_memory_client import InMemoryClientConfig
from amzn_sagemaker_checkpointing.utils.logging_utils import (
    SageMakerCheckpointingLoggerAdapter,
)

from .checksum import decode_base_64, encode_base_64, hash_xxh3_128
from .exceptions import (
    InMemoryClientError,
    InMemoryConfigError,
    InMemoryConnectionError,
    InMemoryNameSpaceCreateError,
    InMemoryRequestError,
    InMemoryResourceNotFoundError,
    InMemoryServerError,
    InMemoryStorageError,
    InMemoryTimeoutError,
)
from .models import CheckpointShardMeta

logger = logging.getLogger(__name__)


class InMemoryCheckpointClient:
    """
    Client for managing checkpoint files via HTTP with a distributed in-memory backend.

    This client supports uploading, downloading, deleting, and listing checkpoints.
    """

    NAMESPACE_PATH = "/v1/cp/namespaces/{namespace}"
    CHECKPOINT_PATH = "/v1/cp/checkpoints/{namespace}/{rank}/{step}"
    LATEST_CHECKPOINTS_PATH = "/v1/cp/checkpoints/{namespace}/latest"
    CLUSTER_RESET_PATH = "/v1/cp/cluster/reset"

    def __init__(
        self,
        namespace: str,
        rank: str,
        world_size: str,
        config: InMemoryClientConfig | None = None,
        metadata_file_count: int = 1,
        steps_retained: int = 3,
        logger: (Union[logging.Logger, "SageMakerCheckpointingLoggerAdapter"] | None) = None,
    ):
        """
        Initialize the InMemoryCheckpointClient.

        Parameters
        ----------
        namespace : str
            Namespace for the checkpoint group.
        rank : str
            Rank of the current node.
        world_size : str
            Total number of data-parallel ranks.
        config : InMemoryClientConfig, optional
            Optional configuration object.
        metadata_file_count : int, optional
            Number of metadata shards.
        steps_retained : int, optional
            Number of previous steps to retain.
        """
        self.namespace = namespace
        self.config = config or InMemoryClientConfig()
        self.world_size = int(world_size)
        self.rank = int(rank)
        self.metadata_file_count = metadata_file_count
        self.steps_retained = steps_retained
        self._total_ranks = self.world_size + self.metadata_file_count
        self._session = self._initialize_session()
        self._logger = logger or logging.getLogger(__name__)
        self._logger.info(
            f"Initialized InMemoryCheckpointClient with namespace={self.namespace}, world_size={self.world_size}, "
            f"rank={self.rank}, metadata_file_count={self.metadata_file_count}, total_ranks={self._total_ranks}"
        )

    def _initialize_session(self) -> requests.Session:
        session = requests.Session()
        retry_strategy = Retry(
            total=self.config.request_retries,
            backoff_factor=self.config.retry_backoff,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def close(self):
        """
        Close the underlying HTTP session.

        This is important to release any persistent HTTP connections that might be
        open due to requests.Session.
        """
        if self._session:
            self._session.close()
            self._session = None

    def _get_metadata_rank(self, metadata_index: int) -> int:
        """
        Compute the metadata rank from its index.

        Parameters
        ----------
        metadata_index : int
            Index of the metadata shard.

        Returns
        -------
        int
            Corresponding metadata rank.

        Raises
        ------
        InMemoryConfigError
            If metadata index is out of range.
        """
        if metadata_index < 0 or metadata_index >= self.metadata_file_count:
            error_msg = (
                f"Invalid metadata_index: {metadata_index}. Must be between 0 and {self.metadata_file_count - 1}"
            )
            self._logger.error(error_msg)
            raise InMemoryConfigError(error_msg)
        return self.world_size + metadata_index

    def _make_request(
        self,
        method: str,
        endpoint: str,
        *,
        params: dict | None = None,
        data: Any = None,
        headers: dict | None = None,
        timeout: float | None = None,
        allow_404: bool = False,
        retries: int | None = None,
        retry_backoff: float | None = None,
    ) -> requests.Response:
        """
        Make an HTTP request with retry and backoff handling.

        Parameters
        ----------
        method : str
            HTTP method (e.g., 'GET', 'POST').
        endpoint : str
            Endpoint path relative to base URL.
        params : dict, optional
            Query parameters.
        data : any, optional
            Payload to send with the request.
        headers : dict, optional
            Request headers.
        timeout : float, optional
            Timeout for the request in seconds.
        allow_404 : bool, optional
            If True, do not raise exception for 404 errors.
        retries : int, optional
            Deprecated, no longer used with urllib3 retry strategy.
        retry_backoff : float, optional
            Deprecated, no longer used with urllib3 retry strategy.

        Returns
        -------
        requests.Response
            Response object from the request.
        """
        url = f"{self.config.base_url}{endpoint}"
        actual_timeout = timeout if timeout is not None else self.config.request_timeout

        try:
            response = self._session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                headers=headers,
                timeout=actual_timeout,
            )
            if response.status_code == 404:
                if allow_404:
                    return response
                error_msg = f"Resource not found at {url}: {response.text}"
                self._logger.error(f"{error_msg}")
                raise InMemoryResourceNotFoundError(error_msg)
            elif 400 <= response.status_code < 500:
                error_msg = f"Client error for {url}: {response.text}"
                self._logger.error(error_msg)
                raise InMemoryClientError(error_msg)
            elif response.status_code >= 500:
                error_msg = f"Server error for {url}: {response.text}"
                self._logger.error(error_msg)
                raise InMemoryServerError(error_msg)
            return response
        except ConnectionError as e:
            error_msg = "Connection error"
            self._logger.error(f"{error_msg}:{e}")
            raise InMemoryConnectionError(error_msg) from e
        except Timeout as e:
            error_msg = f"Timeout after {actual_timeout}s"
            self._logger.error(f"{error_msg}:{e}")
            raise InMemoryTimeoutError(error_msg) from e
        except RequestException as e:
            error_msg = "Unhandled request error"
            self._logger.error(f"{error_msg}:{e}")
            raise InMemoryRequestError(error_msg) from e

    def get_or_create_namespace(
        self,
        timeout: float | None = None,
        retries: int | None = None,
        retry_backoff: float | None = None,
    ) -> None:
        """
        Get an existing namespace or create it if it does not exist.

        Parameters
        ----------
        timeout : float, optional
            Timeout for the request.
        retries : int, optional
            Number of retry attempts.
        retry_backoff : float, optional
            Backoff multiplier for retries.
        """
        endpoint = self.NAMESPACE_PATH.format(namespace=self.namespace)
        try:
            response = self._make_request(
                "GET",
                endpoint,
                timeout=timeout,
                allow_404=True,
                retries=retries,
                retry_backoff=retry_backoff,
            )
            if response.status_code == 404:
                params = {
                    "num_ranks": self._total_ranks,
                    "steps_retained": self.steps_retained,
                }
                self._make_request(
                    "POST",
                    endpoint,
                    params=params,
                    timeout=timeout,
                    retries=retries,
                    retry_backoff=retry_backoff,
                )
                response = self._make_request(
                    "GET",
                    endpoint,
                    timeout=timeout,
                    retries=retries,
                    retry_backoff=retry_backoff,
                )
            return response.json()
        except Exception as e:
            error_msg = f"Error getting existing namespace (or) creating a new one, with name:{self.namespace}"
            self._logger.error(f"{error_msg}: {e}")
            raise InMemoryNameSpaceCreateError(error_msg) from e

    def get_namespace_config(
        self,
        timeout: float | None = None,
        retries: int | None = None,
        retry_backoff: float | None = None,
    ) -> dict:
        """
        Retrieve the configuration for the current namespace.

        Parameters
        ----------
        timeout : float, optional
            Timeout for the request.
        retries : int, optional
            Number of retry attempts.
        retry_backoff : float, optional
            Backoff multiplier for retries.

        Returns
        -------
        dict
            Configuration of the namespace.
        """
        endpoint = self.NAMESPACE_PATH.format(namespace=self.namespace)
        response = self._make_request(
            "GET",
            endpoint,
            timeout=timeout,
            allow_404=True,
            retries=retries,
            retry_backoff=retry_backoff,
        )
        try:
            if response.status_code == 404:
                self._logger.warning(f"Namespace '{self.namespace}' not found.")
                return {}
            return response.json()
        except ValueError as e:
            error_msg = "Failed to decode JSON for namespace config"
            self._logger.error(f"{error_msg}: {e}")
            raise InMemoryStorageError(error_msg) from e

    def delete_namespace(
        self,
        timeout: float | None = None,
        retries: int | None = None,
        retry_backoff: float | None = None,
    ) -> None:
        """
        Delete the current namespace from the in-memory store.

        Parameters
        ----------
        timeout : float, optional
            Timeout for the request.
        retries : int, optional
            Number of retry attempts.
        retry_backoff : float, optional
            Backoff multiplier for retries.
        """
        endpoint = self.NAMESPACE_PATH.format(namespace=self.namespace)
        self._make_request(
            "DELETE",
            endpoint,
            timeout=timeout,
            retries=retries,
            retry_backoff=retry_backoff,
        )

    def reset_cluster(
        self,
        timeout: float | None = None,
        retries: int | None = None,
        retry_backoff: float | None = None,
    ) -> None:
        """
        Reset the in-memory checkpoint cluster.

        Parameters
        ----------
        timeout : float, optional
            Timeout for the request.
        retries : int, optional
            Number of retry attempts.
        retry_backoff : float, optional
            Backoff multiplier for retries.
        """
        self._logger.warning(f"Resetting in-memory cluster at {self.config.base_url}{self.CLUSTER_RESET_PATH}")
        self._make_request(
            "POST",
            self.CLUSTER_RESET_PATH,
            timeout=timeout,
            retries=retries,
            retry_backoff=retry_backoff,
        )

    def get_latest_checkpoints(
        self,
        limit: int = 5,
        timeout: float | None = None,
        retries: int | None = None,
        retry_backoff: float | None = None,
    ) -> list[int]:
        """
        Fetch the latest checkpoint step values.

        Parameters
        ----------
        limit : int, optional
            Number of steps to return, by default 5.
        timeout : float, optional
            Timeout for the request.
        retries : int, optional
            Number of retry attempts.
        retry_backoff : float, optional
            Backoff multiplier for retries.

        Returns
        -------
        List[int]
            Sorted list of latest checkpoint steps.
        """
        endpoint = self.LATEST_CHECKPOINTS_PATH.format(namespace=self.namespace)
        params = {"limit": limit}
        try:
            response = self._make_request(
                "GET",
                endpoint,
                params=params,
                timeout=timeout,
                allow_404=True,
                retries=retries,
                retry_backoff=retry_backoff,
            )
            if response.status_code == 404:
                return []
            return sorted([int(step) for step in response.json()], reverse=True)
        except Exception as e:
            self._logger.error(f"Failed to fetch latest checkpoints: {e}")
            return []

    def put_checkpoint(
        self,
        step: int | str,
        data: bytes | str | BinaryIO,
        metadata_index: int | None = None,
        rank: int | None = None,
        timeout: float | None = None,
        retries: int | None = None,
        retry_backoff: float | None = None,
    ) -> None:
        """
        Upload a checkpoint shard to the in-memory store.

        Parameters
        ----------
        step : int or str
            Training step associated with the checkpoint.
        data : bytes or str or BinaryIO
            Checkpoint data or path to a local file or file-like object.
        metadata_index : int, optional
            Index of the metadata shard. Used to compute the metadata rank.
        rank : int, optional
            Rank identifier if not using metadata_index.
        timeout : float, optional
            Timeout for the request.
        retries : int, optional
            Number of retry attempts.
        retry_backoff : float, optional
            Backoff multiplier for retries.
        """
        actual_rank = (
            self._get_metadata_rank(metadata_index)
            if metadata_index is not None
            else (rank if rank is not None else self.rank)
        )
        endpoint = self.CHECKPOINT_PATH.format(namespace=self.namespace, rank=actual_rank, step=step)
        headers = {
            "Shard-Meta": CheckpointShardMeta(
                checksum=encode_base_64(hash_xxh3_128(data)), algorithm="xxh3_128"
            ).to_json()
        }
        if isinstance(data, str):
            try:
                with open(data, "rb") as f:
                    self._make_request(
                        "POST",
                        endpoint,
                        data=f,
                        headers=headers,
                        timeout=timeout,
                        retries=retries,
                        retry_backoff=retry_backoff,
                    )
            except Exception as e:
                error_msg = f"Error opening file: {data}"
                self._logger.error(error_msg)
                raise InMemoryStorageError(error_msg) from e
        else:
            self._make_request(
                "POST",
                endpoint,
                data=data,
                headers=headers,
                timeout=timeout,
                retries=retries,
                retry_backoff=retry_backoff,
            )

    def get_checkpoint(
        self,
        step: int | str,
        metadata_index: int | None = None,
        rank: int | None = None,
        timeout: float | None = None,
        retries: int | None = None,
        retry_backoff: float | None = None,
    ) -> bytes | None:
        """
        Download a checkpoint shard from the in-memory store.

        Parameters
        ----------
        step : int or str
            Step of the checkpoint to fetch.
        metadata_index : int, optional
            Index of the metadata shard.
        rank : int, optional
            Rank identifier if not using metadata_index.
        timeout : float, optional
            Timeout for the request.
        retries : int, optional
            Number of retry attempts.
        retry_backoff : float, optional
            Backoff multiplier for retries.

        Returns
        -------
        bytes or None
            Checkpoint content if found, else None.

        Raises
        ------
        InMemoryRequestError
            If checksum or content validation fails.
        """
        actual_rank = (
            self._get_metadata_rank(metadata_index)
            if metadata_index is not None
            else (rank if rank is not None else self.rank)
        )
        endpoint = self.CHECKPOINT_PATH.format(namespace=self.namespace, rank=actual_rank, step=step)
        try:
            response = self._make_request(
                "GET",
                endpoint,
                timeout=timeout,
                allow_404=True,
                retries=retries,
                retry_backoff=retry_backoff,
            )
            if response.status_code == 404:
                return None
            headers = response.headers
            content = response.content
            expected_size = int(headers.get("Content-Length", len(content)))
            meta = CheckpointShardMeta.from_json(headers.get("Shard-Meta", "{}"))
            actual_checksum = hash_xxh3_128(content)
            if decode_base_64(meta.checksum) != actual_checksum:
                error_msg = "Checksum mismatch in response"
                self._logger.error(error_msg)
                raise InMemoryStorageError(error_msg)
            if expected_size and len(content) != expected_size:
                error_msg = "Content length mismatch"
                self._logger.error(error_msg)
                raise InMemoryStorageError(error_msg)
            return content
        except InMemoryResourceNotFoundError:
            self._logger.error(f"Resource not found:{endpoint}")
            return None

    def delete_checkpoint(
        self,
        step: int | str,
        metadata_index: int | None = None,
        rank: int | None = None,
        timeout: float | None = None,
        retries: int | None = None,
        retry_backoff: float | None = None,
    ) -> None:
        """
        Delete a checkpoint shard from the in-memory store.

        Parameters
        ----------
        step : int or str
            Step of the checkpoint to delete.
        metadata_index : int, optional
            Index of the metadata shard.
        rank : int, optional
            Rank identifier if not using metadata_index.
        timeout : float, optional
            Timeout for the request.
        retries : int, optional
            Number of retry attempts.
        retry_backoff : float, optional
            Backoff multiplier for retries.
        """
        actual_rank = (
            self._get_metadata_rank(metadata_index)
            if metadata_index is not None
            else (rank if rank is not None else self.rank)
        )
        endpoint = self.CHECKPOINT_PATH.format(namespace=self.namespace, rank=actual_rank, step=step)
        self._make_request(
            "DELETE",
            endpoint,
            timeout=timeout,
            retries=retries,
            retry_backoff=retry_backoff,
        )
