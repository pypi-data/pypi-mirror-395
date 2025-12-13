import logging
import threading
from dataclasses import dataclass
from typing import Optional, Union

from amzn_sagemaker_checkpointing.storage.clients.s3.s3_client import (
    SageMakerS3Client,
    SageMakerS3Config,
)
from amzn_sagemaker_checkpointing.utils.logging_utils import (
    SageMakerCheckpointingLoggerAdapter,
)


@dataclass
class ClientKey:
    """Immutable key for client identification"""

    region: str
    rank: int

    def __hash__(self):
        return hash((self.region, self.rank))

    def __eq__(self, other):
        return isinstance(other, ClientKey) and (self.region, self.rank) == (
            other.region,
            other.rank,
        )


class S3ClientManager:
    """Thread-safe singleton S3 client manager with lifecycle management"""

    _instance: Optional["S3ClientManager"] = None
    _lock = threading.RLock()  # Use RLock for nested locking

    def __new__(
        cls,
        logger: (Union[logging.Logger, "SageMakerCheckpointingLoggerAdapter"] | None) = None,
    ):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(S3ClientManager, cls).__new__(cls)
                    cls._instance._initialize(logger)
        return cls._instance

    def _initialize(
        self,
        logger: (Union[logging.Logger, "SageMakerCheckpointingLoggerAdapter"] | None) = None,
    ) -> None:
        """Initialize the manager state"""
        self._clients: dict[ClientKey, SageMakerS3Client] = {}
        self._client_refs: dict[ClientKey, int] = {}  # Reference counting
        self._logger = logger or logging.getLogger(__name__)
        self._logger.info("S3ClientManager initialized")

    def get_client(self, region: str, rank: int) -> SageMakerS3Client:
        """Get or create an S3 client for a specific rank and region"""
        client_key = ClientKey(region=region, rank=rank)

        with self._lock:
            if client_key not in self._clients:
                # Create new client
                config = SageMakerS3Config(region=region)
                self._clients[client_key] = SageMakerS3Client(config)
                self._client_refs[client_key] = 0
                self._logger.info(f"Created new S3 client for region={region}, rank={rank}")

            # Increment reference count
            self._client_refs[client_key] += 1
            self._logger.debug(f"S3 client reference count for {client_key}: {self._client_refs[client_key]}")

            return self._clients[client_key]

    def release_client(self, region: str, rank: int) -> None:
        """Release a client reference when no longer needed"""
        client_key = ClientKey(region=region, rank=rank)

        with self._lock:
            if client_key in self._client_refs:
                self._client_refs[client_key] -= 1
                self._logger.debug(
                    f"Released S3 client reference for {client_key}, remaining: {self._client_refs[client_key]}"
                )

                # Clean up if no more references
                if self._client_refs[client_key] <= 0:
                    if client_key in self._clients:
                        del self._clients[client_key]
                    del self._client_refs[client_key]
                    self._logger.info(f"Cleaned up S3 client for {client_key}")

    def get_client_stats(self) -> dict[str, int]:
        """Get statistics about active clients"""
        with self._lock:
            return {
                "active_clients": len(self._clients),
                "total_references": sum(self._client_refs.values()),
            }

    def cleanup_all(self) -> None:
        """Emergency cleanup of all clients"""
        with self._lock:
            client_count = len(self._clients)
            self._clients.clear()
            self._client_refs.clear()
            self._logger.warning(f"Emergency cleanup: removed {client_count} S3 clients")
