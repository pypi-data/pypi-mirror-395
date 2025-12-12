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

from amzn_sagemaker_checkpointing.checkpointing.filesystem.checkpoint_helpers import CheckpointHelpers
from amzn_sagemaker_checkpointing.checkpointing.filesystem.exceptions import SageMakerS3TierError
from amzn_sagemaker_checkpointing.storage.clients.s3.s3_client import s3_retry_with_jitter

S3_STREAM_CHUNK_SIZE = 32 * 1024 * 1024
log_prefix = CheckpointHelpers.get_log_prefix


class _S3Operations:
    """Helper class for S3 checkpoint operations with retry logic."""

    def __init__(self, s3_client, logger, rank: int, step: int):
        self.s3_client = s3_client
        self.logger = logger
        self.rank = rank
        self.step = step

    @s3_retry_with_jitter(max_attempts=3, base_delay=2.0, max_delay=60.0)
    def write_checkpoint(self, buffer: io.BytesIO, s3_uri: str) -> None:
        """Write checkpoint data to S3 in chunks."""
        try:
            self.logger.debug(f"{log_prefix(self.rank, self.step)} Starting S3 upload")
            with self.s3_client.create_write_stream(s3_uri=s3_uri) as writer:
                total_written = 0
                chunk_count = 0
                for i in range(0, len(buffer.getvalue()), S3_STREAM_CHUNK_SIZE):
                    chunk = buffer.getvalue()[i : i + S3_STREAM_CHUNK_SIZE]
                    bytes_written = writer.write(chunk)
                    total_written += bytes_written
                    chunk_count += 1
        except Exception as e:
            error_msg = f"Failed to write checkpoint to S3 for rank:{self.rank} and step:{self.step}"
            self.logger.error(f"{error_msg}:{e}")
            raise SageMakerS3TierError(error_msg) from e

    @s3_retry_with_jitter(max_attempts=3, base_delay=2.0, max_delay=60.0)
    def read_checkpoint(self, s3_uri: str) -> bytes:
        """Read checkpoint data from S3 in chunks."""
        try:
            self.logger.debug(f"{log_prefix(self.rank, self.step)} Reading from S3: {s3_uri}")
            with self.s3_client.create_read_stream(s3_uri) as reader:
                chunks = []
                total_read = 0
                while True:
                    chunk = reader.read(S3_STREAM_CHUNK_SIZE)
                    if not chunk:
                        break
                    chunks.append(chunk)
                    total_read += len(chunk)
                    if len(chunks) % 10 == 0:
                        self.logger.debug(
                            f"{log_prefix(self.rank, self.step)} S3 read progress "
                            f"{total_read / (1024*1024):.1f}MB ({len(chunks)} chunks)"
                        )
                return b"".join(chunks)
        except Exception as e:
            error_msg = f"Failed to read checkpoint from S3 for rank:{self.rank} and step: {self.step}"
            self.logger.error(f"{error_msg}:{e}")
            raise SageMakerS3TierError(error_msg) from e

    def write_item(self, byte_buffer: bytes, s3_uri: str) -> None:
        """Write item to S3."""
        try:
            with self.s3_client.create_write_stream(s3_uri=s3_uri) as writer:
                writer.write(byte_buffer)
        except Exception as e:
            error_msg = f"{log_prefix(self.rank, self.step)} Failed to write item to S3"
            self.logger.error(f"{error_msg}:{e}")
            raise SageMakerS3TierError(error_msg) from e

    def read_item(self, s3_uri: str) -> bytes | None:
        """Read item from S3."""
        try:
            with self.s3_client.create_read_stream(s3_uri=s3_uri) as reader:
                chunks = []
                total_read = 0
                while True:
                    chunk = reader.read(S3_STREAM_CHUNK_SIZE)
                    if not chunk:
                        break
                    chunks.append(chunk)
                    total_read += len(chunk)
                return b"".join(chunks)
        except Exception as e:
            self.logger.debug(f"{log_prefix(self.rank, self.step)} Failed to read item from S3: {e}")
            return None
