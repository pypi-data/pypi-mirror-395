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


class InMemoryStorageError(Exception):
    """Base exception for InMemoryCheckpointClient errors."""


class InMemoryConfigError(InMemoryStorageError):
    """Raised when the client configuration is invalid."""


class InMemoryConnectionError(InMemoryStorageError):
    """Raised when the client fails to connect to the service."""


class InMemoryTimeoutError(InMemoryStorageError):
    """Raised when a request to the service times out."""


class InMemoryRequestError(InMemoryStorageError):
    """Raised for other request errors (non-http, non-timeout, non-connection)"""


class InMemoryClientError(InMemoryStorageError):
    """Raised if storage server returns error codes HTTP 400-499."""


class InMemoryServerError(InMemoryStorageError):
    """Raised if storage server returns error codes HTTP >=500."""


class InMemoryResourceNotFoundError(InMemoryStorageError):
    """Raised when a resource is not found on the server."""


class InMemoryNamespaceIncompatibleError(InMemoryStorageError):
    """Raised when namespace configuration is incompatible with the expected setup."""


class InMemoryNameSpaceCreateError(InMemoryStorageError):
    """Raised when namespace creation fails."""
