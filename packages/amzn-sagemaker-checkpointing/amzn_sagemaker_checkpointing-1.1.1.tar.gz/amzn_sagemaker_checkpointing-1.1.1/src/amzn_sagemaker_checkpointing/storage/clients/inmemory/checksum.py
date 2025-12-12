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

import base64
from typing import BinaryIO

import xxhash


def hash_xxh3_128(data: bytes | str | BinaryIO) -> bytes:
    """
    Compute xxh3_128 hash of the given data.

    Args:
        data: Input data as bytes, string (file path), or BinaryIO.

    Returns:
        Hash digest as bytes.
    """
    h = xxhash.xxh3_128()
    if isinstance(data, bytes):
        h.update(data)
    elif isinstance(data, str):
        with open(data, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
    else:
        while chunk := data.read(8192):
            h.update(chunk)
        data.seek(0)  # rewind stream
    return h.digest()


def encode_base_64(data: bytes) -> str:
    """
    Encode bytes into base64 string.

    Args:
        data: Input bytes.

    Returns:
        Base64 encoded string.
    """
    return base64.b64encode(data).decode("utf-8")


def decode_base_64(encoded: str) -> bytes:
    """
    Decode base64 string into bytes.

    Args:
        encoded: Base64 encoded string.

    Returns:
        Decoded bytes.
    """
    return base64.b64decode(encoded)
