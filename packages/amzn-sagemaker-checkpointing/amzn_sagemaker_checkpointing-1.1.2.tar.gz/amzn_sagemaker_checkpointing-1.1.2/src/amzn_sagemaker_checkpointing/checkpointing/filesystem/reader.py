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

import boto3  # type: ignore[import-untyped]
import torch
from torch.distributed._shard._utils import narrow_tensor_by_index
from torch.distributed.checkpoint.metadata import Metadata
from torch.distributed.checkpoint.planner import LoadItemType, LoadPlan, LoadPlanner, ReadItem
from torch.distributed.checkpoint.storage import StorageReader
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
    StorageTier,
    _SageMakerStorageInfo,
)
from amzn_sagemaker_checkpointing.config.sagemaker_checkpoint_config import SageMakerCheckpointConfig

log_prefix = CheckpointHelpers.get_log_prefix
bytes_to_mb = CheckpointHelpers.bytes_to_mb
get_s3_uri = CheckpointHelpers.get_s3_uri


class SageMakerTieredStorageReader(_TieredStorageBase, StorageReader):
    """
    Storage reader implementation for SageMaker's tiered in-memory checkpoint storage.

    Manages reading checkpoint data and metadata using an in-memory distributed storage backend.
    """

    def __init__(self, checkpoint_config: SageMakerCheckpointConfig, step: int | None = None):
        """
        Initialize the storage reader.

        Parameters
        ----------
        checkpoint_config : SageMakerCheckpointConfig
            Configuration object containing checkpoint storage parameters.
        step : int
            Training step associated with the checkpoint.

        Raises
        ------
        SageMakerTieredStorageConfigError
            Errors related to checkpoint configuration
        SageMakerS3TierError
            Error in initializing S3 client
        """
        super().__init__()
        self._initialize_common(checkpoint_config, step, "reader")
        self.logger.info(f"{log_prefix(self.rank, self.step)} Initialized StorageReader for rank")

    def reset(self, checkpoint_id: str | os.PathLike | None = None) -> None:
        """
        Reset the reader's internal state for a new checkpoint operation.

        Parameters
        ----------
        checkpoint_id : str or os.PathLike, optional
            Identifier for the new checkpoint operation.
        """
        self.logger.debug(f"{log_prefix(self.rank, self.step)} Reset called with checkpoint_id={checkpoint_id}")

    def set_up_storage_reader(self, metadata: Metadata, is_coordinator: bool) -> None:
        """
        Store the provided metadata and coordinator status for later use.

        Parameters
        ----------
        metadata : Metadata
            Metadata object containing checkpoint schema and details.
        is_coordinator : bool
            Indicates if the current instance coordinates the checkpoint.
        """
        self.logger.debug(f"{log_prefix(self.rank, self.step)} Setting up reader (is_coordinator={is_coordinator})")
        self.metadata = metadata
        self.is_coordinator = is_coordinator
        self.storage_data = metadata.storage_data

    def prepare_local_plan(self, plan: LoadPlan) -> LoadPlan:
        """
        Process and return the local load plan without modifications.

        Parameters
        ----------
        plan : LoadPlan
            Local load plan to execute.

        Returns
        -------
        LoadPlan
            Unmodified local load plan.
        """
        self.logger.debug(f"{log_prefix(self.rank, self.step)} Preparing local load plan with {len(plan.items)} items")
        return plan

    def prepare_global_plan(self, plans: list[LoadPlan]) -> list[LoadPlan]:
        """
        Process and return global load plans without modifications.

        Parameters
        ----------
        plans : List[LoadPlan]
            Global load plans from all ranks.

        Returns
        -------
        List[LoadPlan]
            Unmodified global load plans.
        """
        self.logger.debug(f"{log_prefix(self.rank, self.step)} Preparing global load plan with {len(plans)} plans")
        return plans

    def read_metadata(self) -> Metadata:
        """
        Retrieve and deserialize checkpoint metadata.

        Returns
        -------
        Metadata
            Metadata object containing checkpoint information.
            (or) empty Metadata if not available
        """
        try:
            if self.step is not None:
                self.logger.info(f"{log_prefix(self.rank, self.step)} reading metadata for configured step")
                return self._read_metadata_for_step(self.step)

            latest_step_all_tiers = self._get_latest_step_all_tiers()
            for latest_step, tier in latest_step_all_tiers:
                metadata = self._read_metadata_for_step(latest_step)
                if metadata.state_dict_metadata:
                    self.step = latest_step
                    self.logger.info(
                        f"{log_prefix(self.rank, self.step)} Metadata read from step {latest_step} of {tier} tier"
                    )
                    return metadata

            self.logger.error(f"{log_prefix(self.rank, self.step)} No checkpoints to read metadata")
        except Exception as e:
            self.logger.error(f"{log_prefix(self.rank, self.step)} read_metadata failed: {e}")
        return Metadata({})

    def read_data(self, plan: LoadPlan, planner: LoadPlanner) -> Future[None]:
        """
        Enhanced checkpoint data reading with tiered storage fallback and multi-item support.

        Features:
        - Always attempts In-memory read first for all items
        - Falls back to S3 if In-memory read fails or data not found
        - Handles multiple items individually with proper error handling
        - Automatic fallback handling with comprehensive retry logic
        - Latest step discovery for missing checkpoints

        Parameters
        ----------
        plan : LoadPlan
            Local load plan specifying items to load.
        planner : LoadPlanner
            Planner to load checkpoint data items into memory.

        Returns
        -------
        Future[None]
            A completed future object indicating data loading completion.
        """

        def _read_data(future: Future, plan: LoadPlan, planner: LoadPlanner):
            try:
                self.logger.info(f"{log_prefix(self.rank, self.step)} Reading data")
                if self.step is None:
                    raise SageMakerTieredStorageError(
                        f"{log_prefix(self.rank, self.step)} Step must be set before calling read_data"
                    )

                total_start = time.time()
                self.logger.info(
                    f"{log_prefix(self.rank, self.step)} Starting checkpoint read ({len(plan.items)} items)"
                )

                in_memory_read_success = True
                per_rank: dict[int, list[ReadItem]] = {}
                in_memory_ckpt_read_size = 0

                for read_item in plan.items:
                    storage_info: _SageMakerStorageInfo = self.storage_data[read_item.storage_index]
                    per_rank.setdefault(storage_info.rank, []).append(read_item)

                for rank, items in per_rank.items():
                    try:
                        blob = self.client.get_checkpoint(step=self.step, rank=rank)  # type: ignore
                        if blob is None:
                            self.logger.info(f"{log_prefix(self.rank, self.step)} get_check_point returned empty blob")
                            in_memory_read_success = False
                        if blob:
                            in_memory_ckpt_read_size += len(blob)
                            for read_item in items:
                                try:
                                    self._process_read_item(read_item, blob, planner)
                                except EOFError:
                                    break
                                except Exception as e:
                                    error_msg = (
                                        f"{log_prefix(self.rank, self.step)} Checkpoint load in to state_dict failed"
                                    )
                                    self.logger.error(f"{error_msg}:{e}")
                                    raise SageMakerTieredStorageError(error_msg) from e
                    except Exception as e:
                        in_memory_read_success = False
                        error_msg = f"{log_prefix(self.rank, self.step)} In-memory read failed"
                        self.logger.error(f"{error_msg}:{e}")
                        if self.s3_base_path:
                            break
                        else:
                            raise SageMakerInMemoryTierError(error_msg) from e

                if not in_memory_read_success:
                    s3_ckpt_read_size = 0
                    for rank, items in per_rank.items():
                        try:
                            s3_read_start_time = time.time()
                            s3_uri = get_s3_uri(
                                self.checkpoint_config.s3_tier_base_path,
                                self.checkpoint_config.namespace,
                                rank,
                                self.step,
                                "checkpoint.pt",
                            )
                            s3_ops = _S3Operations(self.s3_client, self.logger, rank, self.step)
                            blob = s3_ops.read_checkpoint(s3_uri)
                            s3_ckpt_read_size += len(blob)
                            s3_read_time_taken = time.time() - s3_read_start_time
                            blob_mb = bytes_to_mb(len(blob))
                            s3_speed = blob_mb / s3_read_time_taken if s3_read_time_taken > 0 else 0
                            self.logger.info(
                                f"{log_prefix(self.rank, self.step)} read from S3 in {s3_read_time_taken:.3f}s "
                                f"({blob_mb:.1f}MB, {s3_speed:.1f} MB/s, {len(blob)} blob)"
                            )

                            for read_item in items:
                                try:
                                    self._process_read_item(read_item, blob, planner)
                                except EOFError:
                                    break
                                except Exception as e:
                                    error_msg = (
                                        f"{log_prefix(self.rank, self.step)} Checkpoint load in to state_dict failed"
                                    )
                                    self.logger.error(f"{error_msg}:{e}")
                                    raise SageMakerTieredStorageError(error_msg) from e

                        except Exception as e:
                            self.logger.error(f"{log_prefix(self.rank, self.step)} S3 read failed:{e}")
                            future.set_exception(e)
                            return
                # Final logging and statistics
                total_time = time.time() - total_start
                self.logger.info(f"{log_prefix(self.rank, self.step)} Checkpoint read completed in {total_time:.3f}s")
                future.set_result(None)
            except Exception as e:
                error_msg = f"{log_prefix(self.rank, self.step)} Checkpoint load failed"
                self.logger.error(f"{error_msg}:{e}")
                future.set_exception(e)

        future: Future = Future()
        t = threading.Thread(target=_read_data, args=(future, plan, planner))
        t.start()
        return future

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

    def _try_read_md_from_memory(self, step: int) -> bytes | None:
        """Try reading metadata from in-memory storage."""
        try:
            return self.client.get_checkpoint(step=step, metadata_index=METADATA_INDEX)
        except Exception as e:
            self.logger.error(f"{log_prefix(self.rank, self.step)} Memory read failed: {e}")
            return None

    def _try_read_md_from_s3(self, step: int) -> bytes | None:
        """Try reading metadata from S3 storage."""
        try:
            s3_uri = get_s3_uri(
                self.checkpoint_config.s3_tier_base_path, self.checkpoint_config.namespace, 0, step, "metadata.metadata"
            )
            s3_ops = _S3Operations(self.s3_client, self.logger, 0, step)
            return s3_ops.read_item(s3_uri)
        except Exception as e:
            self.logger.error(f"S3 metadata read failed for step {step}: {e}")
            return None

    def _find_latest_complete_step(self) -> int | None:
        """
        Find the latest step that is complete across ALL ranks in S3.

        Returns
        -------
        Optional[int]
            The latest step number available for all ranks, or None if no complete steps found.
        """
        try:
            s3_base_path = self.checkpoint_config.s3_tier_base_path
            bucket, base_prefix = CheckpointHelpers.parse_s3_path(s3_base_path)

            if base_prefix:
                full_base_prefix = f"{base_prefix}/{self.checkpoint_config.namespace}"
            else:
                full_base_prefix = self.checkpoint_config.namespace

            s3_client = boto3.client("s3", region_name=self.region)

            # Collect steps for each rank
            rank_steps: dict[int, set[int]] = {}
            self.logger.info(
                f"{log_prefix(self.rank, self.step)} Searching bucket: {bucket}, full_base_prefix: {full_base_prefix}"
            )

            for rank in range(self.checkpoint_config.world_size):
                rank_prefix = f"{full_base_prefix}/rank_{rank}/"
                self.logger.debug(f"{log_prefix(self.rank, self.step)} Searching with rank_prefix: '{rank_prefix}'")

                paginator = s3_client.get_paginator("list_objects_v2")
                rank_steps[rank] = set()

                for page in paginator.paginate(Bucket=bucket, Prefix=rank_prefix, Delimiter="/"):
                    prefixes = page.get("CommonPrefixes", [])
                    for prefix_info in prefixes:
                        prefix = prefix_info["Prefix"]
                        if "/step_" in prefix:
                            try:
                                step_part = prefix.split("/step_")[1].rstrip("/")
                                step_num = int(step_part)
                                rank_steps[rank].add(step_num)
                            except (ValueError, IndexError):
                                continue
                self.logger.debug(f"{log_prefix(self.rank, self.step)} Final steps for rank {rank}: {rank_steps[rank]}")

            s3_client.close()
            # Find intersection of all rank steps (steps present in ALL ranks)
            if not rank_steps:
                return None

            all_complete_steps = set.intersection(*rank_steps.values()) if rank_steps else set()

            if all_complete_steps:
                latest_complete_step = max(all_complete_steps)
                self.logger.info(
                    f"{log_prefix(self.rank, self.step)} Latest complete step across all "
                    f"{self.checkpoint_config.world_size} ranks: {latest_complete_step}"
                )
                return latest_complete_step
            else:
                self.logger.warning(
                    f"{log_prefix(self.rank, self.step)} No steps found that are complete across all ranks"
                )
                return None

        except Exception as e:
            self.logger.error(f"{log_prefix(self.rank, self.step)} Failed to find latest complete step: {e}")
            return None

    def _read_metadata_for_step(self, step) -> Metadata:
        """Read metadata for a specific step, trying memory first then S3."""
        try:
            metadata_buffer = self._try_read_md_from_memory(step)
            if metadata_buffer:
                self.logger.info(
                    f"{log_prefix(self.rank, step)} Successfully read metadata from memory, "
                    f"size={len(metadata_buffer)} bytes"
                )
                return pickle.loads(metadata_buffer)  # TODO See comment in CR-232402799

            if self.s3_base_path:
                metadata_buffer = self._try_read_md_from_s3(step)
                if metadata_buffer:
                    self.logger.info(
                        f"{log_prefix(self.rank, step)} Successfully read metadata from S3, "
                        f"size={len(metadata_buffer)} bytes"
                    )
                    return pickle.loads(metadata_buffer)
        except Exception as e:
            self.logger.error(f"{log_prefix(self.rank, step)} _read_metadata_for_step failed: {e}")
        return Metadata({})

    def _get_latest_step_all_tiers(self) -> list[tuple[int, StorageTier]]:
        latest_step_all_tiers = []
        try:
            memory_steps = self.client.get_latest_checkpoints(limit=3)
            if memory_steps:
                latest_step_all_tiers = [(step, StorageTier.IN_MEMORY) for step in memory_steps]
        except Exception as e:
            self.logger.error(f"{log_prefix(self.rank, self.step)} Failed to get memory steps: {e}")
        try:
            s3_step = self._find_latest_complete_step()
            if s3_step:
                latest_step_all_tiers.append((s3_step, StorageTier.S3))
        except Exception as e:
            self.logger.error(f"{log_prefix(self.rank, self.step)} Failed to get S3 step: {e}")

        latest_step_all_tiers.sort(key=lambda tier_step: (-tier_step[0], tier_step[1].value))
        self.logger.info(f"{log_prefix(self.rank, self.step)} Latest steps across tiers: {latest_step_all_tiers}")
        return latest_step_all_tiers

    def _process_read_item(self, read_item, blob: bytes, planner: LoadPlanner) -> None:
        """Process a single read item from blob data."""
        storage_info = self.storage_data[read_item.storage_index]
        item_data = blob[storage_info.offset : storage_info.offset + storage_info.length]

        with io.BytesIO(item_data) as stream:
            if read_item.type == LoadItemType.BYTE_IO:
                planner.load_bytes(read_item, stream)
            else:
                tensor = torch.load(stream, map_location="cpu")
                if hasattr(read_item, "storage_offsets") and hasattr(read_item, "lengths"):
                    tensor = narrow_tensor_by_index(
                        tensor,
                        read_item.storage_offsets,
                        read_item.lengths,
                    )

                target_tensor = planner.resolve_tensor(read_item).detach()
                if target_tensor.size() != tensor.size():
                    raise SageMakerTieredStorageError(
                        f"{log_prefix(self.rank, self.step)} Size mismatch for {read_item.storage_index}: "
                        f"expected {target_tensor.size()}, got {tensor.size()}"
                    )

                target_tensor.copy_(tensor)
                planner.commit_tensor(read_item, target_tensor)
