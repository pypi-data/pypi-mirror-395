import os
import tempfile
from io import BytesIO

import pytest

from amzn_sagemaker_checkpointing.storage.clients.inmemory.checksum import (
    decode_base_64,
    encode_base_64,
    hash_xxh3_128,
)


@pytest.fixture
def hello_world_hash():
    return b"\xdf\x8d\t\xe9?\x87I\x00\xa9\x9b\x87u\xcc\x15\xb6\xc7"


@pytest.fixture
def hello_world_base64():
    return "aGVsbG8gd29ybGQ="


@pytest.fixture
def test_file():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"hello world")
    yield f.name
    os.remove(f.name)


def test_hash_xxh3_128_with_bytes():
    test_data = b"hello world"
    result = hash_xxh3_128(test_data)
    expected = b"\xdf\x8d\t\xe9?\x87I\x00\xa9\x9b\x87u\xcc\x15\xb6\xc7"
    assert result == expected


def test_hash_xxh3_128_with_file_path(test_file, hello_world_hash):
    result = hash_xxh3_128(test_file)
    assert result == hello_world_hash


def test_hash_xxh3_128_with_binary_io(hello_world_hash):
    binary_io = BytesIO(b"hello world")
    result = hash_xxh3_128(binary_io)
    assert result == hello_world_hash


def test_encode_base_64(hello_world_base64):
    test_bytes = b"hello world"
    result = encode_base_64(test_bytes)
    assert isinstance(result, str)
    assert result == hello_world_base64


def test_decode_base_64(hello_world_base64):
    result = decode_base_64(hello_world_base64)
    assert isinstance(result, bytes)
    assert result == b"hello world"
