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
import os
from logging import FileHandler

import torch.distributed as dist

from amzn_sagemaker_checkpointing.checkpointing.filesystem.checkpoint_helpers import CheckpointHelpers
from amzn_sagemaker_checkpointing.checkpointing.filesystem.exceptions import SageMakerS3TierError
from amzn_sagemaker_checkpointing.config.sagemaker_checkpoint_config import SageMakerCheckpointConfig
from amzn_sagemaker_checkpointing.storage.clients.inmemory.inmemory_client import InMemoryCheckpointClient
from amzn_sagemaker_checkpointing.storage.clients.s3.s3_client_manager import S3ClientManager
from amzn_sagemaker_checkpointing.utils.logging_utils import (
    CheckpointFilter,
    SageMakerCheckpointingLoggerAdapter,
)


class _TieredStorageBase:
    """Base class for tiered storage reader and writer with shared initialization logic."""

    def _initialize_common(
        self, checkpoint_config: SageMakerCheckpointConfig, step: int | None, class_type: str
    ) -> None:
        """Initialize common components for reader and writer.

        Parameters
        ----------
        checkpoint_config : SageMakerCheckpointConfig
            Configuration object containing checkpoint storage parameters.
        step : int | None
            Training step associated with the checkpoint.
        class_type : str
            Type of class ('reader' or 'writer') for logger naming.
        """
        self.checkpoint_config = CheckpointHelpers.validated_checkpoint_config(checkpoint_config)
        self.rank = dist.get_rank() if dist.is_available() and dist.is_initialized() else 0
        self.step = step

        logger_name = f"sagemaker.checkpointing.{class_type}.rank_{self.rank}"
        self.logger = self._setup_logger(logger_name, self.checkpoint_config.namespace, checkpoint_config.logger)

        self.s3_base_path = self.checkpoint_config.s3_tier_base_path
        self._initialize_s3_client()
        self._initialize_memory_client()

    def _initialize_s3_client(self) -> None:
        """Initialize S3 client if S3 path is configured."""
        if self.s3_base_path:
            region = CheckpointHelpers.get_bucket_location(s3_base_path=self.s3_base_path)
            try:
                s3_client_manager = S3ClientManager(logger=self.logger)
                s3_client = s3_client_manager.get_client(region=region, rank=self.rank)
                stats = s3_client_manager.get_client_stats()
                self.logger.info(f"{CheckpointHelpers.get_log_prefix(self.rank, self.step)} S3 client stats: {stats}")
                self.s3_client = s3_client
                self.region = region
            except Exception as e:
                error_msg = f"{CheckpointHelpers.get_log_prefix(self.rank, self.step)} S3 client creation failed"
                self.logger.error(f"{error_msg}:{e}")
                raise SageMakerS3TierError(error_msg) from e
        else:
            self.region = ""

    def _initialize_memory_client(self) -> None:
        """Initialize in-memory checkpoint client."""
        try:
            self.client = InMemoryCheckpointClient(  # TODO Exception handling is broken; client may not be initialized.
                namespace=self.checkpoint_config.namespace,
                rank=str(self.rank),
                world_size=str(self.checkpoint_config.world_size),
                metadata_file_count=1,
                logger=self.logger,
            )
        except Exception as e:
            self.logger.error(
                f"{CheckpointHelpers.get_log_prefix(self.rank, self.step)} In-memory client creation failed: {e}"
            )

    @staticmethod
    def _setup_logger(
        logger_name: str, namespace: str, provided_logger: logging.Logger | None = None
    ) -> logging.Logger | SageMakerCheckpointingLoggerAdapter:
        """Set up logger with namespace-specific host path and checkpointing filtering."""
        base_log_dir = "/var/log/sagemaker_checkpointing"
        host_log_path = f"{base_log_dir}/{namespace}_checkpointing.log"

        if provided_logger is not None:
            base_logger = provided_logger
        else:
            base_logger = logging.getLogger(logger_name)
            if not base_logger.handlers:
                console_handler = logging.StreamHandler()
                console_formatter = logging.Formatter(
                    f"[%(asctime)s] [{namespace}] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
                )
                console_handler.setFormatter(console_formatter)
                base_logger.addHandler(console_handler)

        has_checkpointing_handler = False
        for handler in base_logger.handlers:
            if (
                isinstance(handler, FileHandler)
                and hasattr(handler, "baseFilename")
                and handler.baseFilename == os.path.abspath(host_log_path)
            ):
                has_checkpointing_handler = True
                break

        if not has_checkpointing_handler:
            try:
                log_dir = os.path.dirname(host_log_path)
                os.makedirs(log_dir, exist_ok=True)
                file_handler = FileHandler(host_log_path, mode="a", encoding="utf-8")
                file_handler.addFilter(CheckpointFilter())
                formatter = logging.Formatter(
                    f"[%(asctime)s] [{namespace}] [%(name)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
                )
                file_handler.setFormatter(formatter)
                base_logger.addHandler(file_handler)
                adapter = SageMakerCheckpointingLoggerAdapter(base_logger, {})
                adapter.info(f"SageMaker checkpointing file logging enabled: {host_log_path}")
            except Exception as e:
                base_logger.warning(f"Failed to setup checkpointing file logging: {e}")

        return SageMakerCheckpointingLoggerAdapter(base_logger, {})
