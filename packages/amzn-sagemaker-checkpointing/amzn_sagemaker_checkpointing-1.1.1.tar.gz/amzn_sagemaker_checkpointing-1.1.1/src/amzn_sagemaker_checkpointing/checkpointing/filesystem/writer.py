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

import io
import os
import pickle
import threading
import time
from typing import Any

import torch
from torch.distributed.checkpoint.metadata import Metadata, StorageMeta
from torch.distributed.checkpoint.planner import SavePlan, SavePlanner, WriteItemType
from torch.distributed.checkpoint.storage import StorageWriter, WriteResult
from torch.futures import Future

from amzn_sagemaker_checkpointing.checkpointing.filesystem.checkpoint_helpers import (
    CheckpointHelpers,
)
from amzn_sagemaker_checkpointing.checkpointing.filesystem.exceptions import (
    SageMakerInMemoryTierError,
    SageMakerTieredStorageError,
)
from amzn_sagemaker_checkpointing.checkpointing.filesystem.s3_operations import _S3Operations
from amzn_sagemaker_checkpointing.checkpointing.filesystem.storage_base import _TieredStorageBase
from amzn_sagemaker_checkpointing.checkpointing.filesystem.storage_info import (
    METADATA_INDEX,
    _SageMakerStorageInfo,
)
from amzn_sagemaker_checkpointing.config.sagemaker_checkpoint_config import SageMakerCheckpointConfig

log_prefix = CheckpointHelpers.get_log_prefix
bytes_to_mb = CheckpointHelpers.bytes_to_mb
get_s3_uri = CheckpointHelpers.get_s3_uri


class SageMakerTieredStorageWriter(_TieredStorageBase, StorageWriter):
    """
    Storage writer implementation for SageMaker's tiered in-memory checkpoint storage.

    Manages writing checkpoint data and metadata using an in-memory distributed storage backend.
    """

    def __init__(
        self,
        checkpoint_config: SageMakerCheckpointConfig,
        path: str | os.PathLike = "",
        step: int = -1,
        *args: Any,
        **kwargs: Any,
    ):
        """
        Initialize the storage writer.

        Parameters
        ----------
        checkpoint_config : SageMakerCheckpointConfig
            Configuration object containing checkpoint storage parameters.
        path : str or os.PathLike, optional
            Path indicating the checkpoint location, by default "".
        step : int, optional
            Training step associated with the checkpoint, by default -1.

        Raises
        ------
        SageMakerTieredStorageConfigError
            Errors related to checkpoint configuration
        SageMakerS3TierError
            Error in initializing S3 client
        """
        super().__init__()
        step_val = self._get_step_val(step, path)
        self._initialize_common(checkpoint_config, step_val, "writer")
        self.step: int = step_val  # Type assertion: step is always int in Writer

        self.logger.debug(f"{log_prefix(self.rank, self.step)} Initialized StorageWriter for rank")
        self.in_memory_success = True
        self.s3_success = False

    def reset(self, checkpoint_id: str | os.PathLike | None = None) -> None:
        """
        Reset the writer's internal state for a new checkpoint operation.

        Parameters
        ----------
        checkpoint_id : str or os.PathLike, optional
            Identifier for the new checkpoint operation.
        """

    def set_up_storage_writer(self, is_coordinator: bool) -> None:
        """
        Set up the storage writer and initialize namespace if the instance is coordinator.

        Parameters
        ----------
        is_coordinator : bool
            Indicates if the current instance coordinates the checkpoint.
        """
        self.logger.debug(
            f"{log_prefix(self.rank, self.step)} Setting up storage writer (is_coordinator={is_coordinator})"
        )
        self.is_coordinator = is_coordinator
        try:
            if is_coordinator:
                self.client.get_or_create_namespace()
        except Exception as e:
            self.logger.error(f"{log_prefix(self.rank, self.step)} In-memory client failed: {e}")

    def prepare_local_plan(self, plan: SavePlan) -> SavePlan:
        """
        Process and return the local save plan without modifications.

        Parameters
        ----------
        plan : SavePlan
            Local save plan to execute.

        Returns
        -------
        SavePlan
            Unmodified local save plan.
        """
        return plan

    def prepare_global_plan(self, plans: list[SavePlan]) -> list[SavePlan]:
        """
        Process and return global save plans without modifications.

        Parameters
        ----------
        plans : List[SavePlan]
            Global save plans from all ranks.

        Returns
        -------
        List[SavePlan]
            Unmodified global save plans.
        """
        return plans

    def write_data(self, plan: SavePlan, planner: SavePlanner) -> Future[list[WriteResult]]:
        def _write_data(future: Future, plan: SavePlan, planner: SavePlanner):
            """
            Enhanced checkpoint data writing with tiered storage and complete consistency.

            Features:
            - Always attempts In-memory write first for all items
            - Writes to S3 at specified frequency regardless of In-memory status
            - Chunked S3 uploads for large data
            - Complete checkpoint consistency across storage tiers

            Parameters
            ----------
            plan : SavePlan
                Local save plan containing items to save.
            planner : SavePlanner
                Planner to resolve checkpoint data items.

            Returns
            -------
            List[WriteResult]]
                A list of WriteResult instances representing checkpoint storage metadata.
            """
            try:
                buffer = io.BytesIO()
                write_results: list[WriteResult] = []
                total_start = time.time()
                self.logger.info(
                    f"{log_prefix(self.rank, self.step)} Starting checkpoint write ({len(plan.items)} items)"
                )

                for item in plan.items:
                    try:
                        write_results.append(self._process_write_item(item, planner, buffer))
                    except Exception as e:
                        error_msg = f"{log_prefix(self.rank, self.step)} Could not write item {item.index}"
                        self.logger.error(f"{error_msg}:{e}")
                        raise SageMakerTieredStorageError(error_msg) from e

                in_memory_start = time.time()
                buffer_data = buffer.getvalue()
                try:
                    self.client.put_checkpoint(step=self.step, data=buffer_data, rank=self.rank)
                    in_memory_write_time = time.time() - in_memory_start
                    data_mb = bytes_to_mb(len(buffer_data))
                    self.logger.info(
                        f"{log_prefix(self.rank, self.step)} In-memory write completed "
                        f"in {in_memory_write_time:.3f}s ({data_mb / in_memory_write_time:.1f} MB/s)"
                    )
                except Exception as e:
                    self.in_memory_success = False
                    error_msg = f"{log_prefix(self.rank, self.step)} In-memory write failed"
                    self.logger.error(f"{error_msg}:{e}")
                    if self.checkpoint_config.save_to_s3:
                        self.logger.warning(
                            f"{log_prefix(self.rank, self.step)} Checkpoint might be saved to "
                            f"{self.s3_base_path} based on configuration"
                        )
                    else:
                        raise SageMakerInMemoryTierError(error_msg) from e

                # Execute S3 writes if needed
                if self.checkpoint_config.save_to_s3:
                    try:
                        self.logger.info(
                            f"{log_prefix(self.rank, self.step)} Scheduled S3 write - "
                            f"writing all {len(plan.items)} items to S3"
                        )
                        s3_batch_start = time.time()
                        s3_uri = get_s3_uri(
                            self.s3_base_path, self.checkpoint_config.namespace, self.rank, self.step, "checkpoint.pt"
                        )
                        s3_ops = _S3Operations(self.s3_client, self.logger, self.rank, self.step)
                        s3_ops.write_checkpoint(buffer, s3_uri)
                        self.s3_success = True
                        s3_batch_time = time.time() - s3_batch_start
                        buffer_mb = bytes_to_mb(buffer.tell())
                        s3_batch_speed = buffer_mb / s3_batch_time if buffer.tell() > 0 else 0
                        self.logger.info(
                            f"{log_prefix(self.rank, self.step)} S3 batch write completed "
                            f"in {s3_batch_time:.3f}s ({buffer_mb:.1f}MB total, {s3_batch_speed:.1f} MB/s average)"
                        )
                    except Exception as e:
                        self.logger.error(
                            f"{log_prefix(self.rank, self.step)} S3 checkpoint save failed after in-memory failure: {e}"
                        )
                        future.set_exception(e)
                        return

                total_time = time.time() - total_start
                total_size_mb = bytes_to_mb(sum(result.size_in_bytes for result in write_results))
                self.logger.info(
                    f"{log_prefix(self.rank, self.step)} Checkpoint write completed "
                    f"in {total_time:.3f}s ({total_size_mb:.1f}MB total, {total_size_mb / total_time:.1f} MB/s average)"
                )
                future.set_result(write_results)

            except Exception as e:
                self.logger.error(f"{log_prefix(self.rank, self.step)} Checkpoint write failed across tiers: {e}")
                future.set_exception(e)

        future: Future[list[WriteResult]] = Future()
        t = threading.Thread(target=_write_data, args=(future, plan, planner))
        t.start()
        return future

    def finish(self, metadata: Metadata, results: list[list[WriteResult]]) -> None:
        """
        Consolidate and serialize checkpoint metadata, then store it in the in-memory storage.

        Parameters
        ----------
        metadata : Metadata
            Metadata object containing detailed checkpoint information.
        results : List[List[WriteResult]]
            Nested list of WriteResults from checkpoint write operations across all ranks.
        """

        self.logger.info(f"{log_prefix(self.rank, self.step)} Finishing checkpoint write")
        storage_md = {}
        for wr_list in results:
            for wr in wr_list:
                storage_md[wr.index] = wr.storage_data

        metadata.storage_data = storage_md
        metadata.storage_meta = self.storage_meta()
        metadata_buffer = pickle.dumps(metadata, protocol=pickle.HIGHEST_PROTOCOL)
        self.logger.info(
            f"{log_prefix(self.rank, self.step)} Created checkpoint metadata, size:{len(metadata_buffer)} bytes"
        )
        try:
            self.client.put_checkpoint(step=self.step, data=metadata_buffer, metadata_index=METADATA_INDEX)
            self.logger.info(f"{log_prefix(self.rank, self.step)} Checkpoint metadata written successfully in-memory")
        except Exception as e:
            error_msg = f"{log_prefix(self.rank, self.step)} Checkpoint metadata failed saving in-memory"
            self.logger.error(f"{error_msg}:{e}")
            if self.checkpoint_config.save_to_s3:
                self.logger.warning(
                    f"{log_prefix(self.rank, self.step)} Checkpoint metadata might be saved to S3 "
                    f"based on configuration"
                )
            else:
                raise SageMakerInMemoryTierError(error_msg) from e

        if self.checkpoint_config.save_to_s3:
            s3_uri = get_s3_uri(
                self.s3_base_path, self.checkpoint_config.namespace, self.rank, self.step, "metadata.metadata"
            )
            s3_ops = _S3Operations(self.s3_client, self.logger, self.rank, self.step)
            s3_ops.write_item(metadata_buffer, s3_uri)
            self.logger.info(f"{log_prefix(self.rank, self.step)} Checkpoint metadata written successfully to S3")

    @classmethod
    def validate_checkpoint_id(cls, checkpoint_id: str | os.PathLike) -> bool:
        """
        Validate checkpoint ID for storage compatibility. Currently always returns True.

        Parameters
        ----------
        checkpoint_id : str or os.PathLike
            Checkpoint identifier to validate.

        Returns
        -------
        bool
            Always True, indicating compatibility.
        """
        return True

    def storage_meta(self) -> StorageMeta | None:
        """
        Provide basic storage metadata associated with this checkpoint operation.

        Returns
        -------
        StorageMeta
            Basic storage metadata object.
        """
        return StorageMeta()

    def _process_write_item(self, item, planner: SavePlanner, buffer: io.BytesIO) -> WriteResult:
        """Process a single write item and return WriteResult."""
        offset = buffer.tell()
        data = planner.resolve_data(item)

        if item.type == WriteItemType.BYTE_IO:
            if not isinstance(data, io.BytesIO):
                raise TypeError(
                    f"{log_prefix(self.rank, self.step)} Expected BytesIO for BYTE_IO item, got {type(data)}"
                )
            buffer.write(data.getbuffer())
        else:
            if not isinstance(data, torch.Tensor):
                raise TypeError(f"Expected Tensor, got {type(data)}")
            data = data.detach().contiguous().cpu()
            torch.save(data, buffer)

        length = buffer.tell() - offset
        return WriteResult(
            index=item.index,
            size_in_bytes=length,
            storage_data=_SageMakerStorageInfo(
                rank=self.rank,
                offset=offset,
                length=length,
            ),
        )

    @staticmethod
    def _get_step_val(step: int, path: str | os.PathLike) -> int:
        """Extract or validate the checkpoint step number."""
        selected_step = -1
        if step != -1:
            selected_step = step
        elif path and "step_" in str(path):
            try:
                selected_step = int(str(path).split("step_")[1].split("/")[0])
            except (IndexError, ValueError):
                pass

        if selected_step < 0:
            raise SageMakerTieredStorageError(f"Invalid step value, step:{step}. path:{path}")
        return selected_step
