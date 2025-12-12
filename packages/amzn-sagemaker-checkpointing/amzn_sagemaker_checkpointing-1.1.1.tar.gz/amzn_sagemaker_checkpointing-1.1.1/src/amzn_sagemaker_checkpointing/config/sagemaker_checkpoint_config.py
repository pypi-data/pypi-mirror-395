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
from dataclasses import dataclass


@dataclass
class SageMakerCheckpointConfig:
    """
    Configuration for SageMakerCheckpointConfig.
    Defines the storage paths and save frequencies for different tiers.

    Attributes:
        namespace: Namespace of the in-memory checkpoint. Should be unique for each ML job.
        world_size: Total number of data-parallel ranks in the workload.
        disk_tier_base_path: Path for disk checkpoint storage .
        s3_tier_base_path: S3 bucket name + path prefix for checkpoint storage.
        save_to_s3: Flag indicating if the checkpoint should be saved in S3 tier.
        save_to_disk: Flag indicating if the checkpoint should be saved in disk tier.
    """

    namespace: str
    world_size: int
    disk_tier_base_path: str = ""
    s3_tier_base_path: str = ""
    save_to_s3: bool = False
    save_to_disk: bool = False
    logger: logging.Logger | None = None
