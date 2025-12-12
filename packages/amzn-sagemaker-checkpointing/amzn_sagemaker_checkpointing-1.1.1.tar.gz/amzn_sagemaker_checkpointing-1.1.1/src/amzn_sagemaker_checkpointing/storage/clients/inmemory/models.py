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


import json
from dataclasses import dataclass


@dataclass
class CheckpointShardMeta:
    """
    Represents metadata for a checkpoint shard.

    Attributes:
        checksum: The hash of the content.
        algorithm: The hashing algorithm used.
    """

    checksum: str
    algorithm: str = "xxh3_128"

    def to_json(self) -> str:
        """
        Convert the metadata to a JSON string for headers.

        Returns:
            A JSON string representation of the shard metadata.
        """
        return json.dumps({"checksum": self.checksum, "algorithm": self.algorithm})

    @staticmethod
    def from_json(json_str: str) -> "CheckpointShardMeta":
        """
        Create a CheckpointShardMeta instance from a JSON string.

        Args:
            json_str: A JSON string representation of the metadata.

        Returns:
            An instance of CheckpointShardMeta.
        """
        data = json.loads(json_str)
        return CheckpointShardMeta(checksum=data["checksum"], algorithm=data.get("algorithm", "xxh3_128"))
