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

from dataclasses import dataclass


@dataclass
class InMemoryClientConfig:
    """
    Configuration for InMemoryCheckpointClient.

    Attributes:
        base_url: Base URL of the in-memory service.
        request_timeout: Timeout per request in seconds.
        request_retries: Number of retry attempts on failure.
        retry_backoff: Backoff multiplier for retries.
        log_requests: Whether to log all HTTP requests.
    """

    base_url: str = "http://ai-toolkit-gossip-headless.aws-hyperpod.svc.cluster.local:9200"
    request_timeout: float = 60.0
    request_retries: int = 0
    retry_backoff: float = 1.5
    log_requests: bool = True
