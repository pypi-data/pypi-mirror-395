import re

import pytest

from sila.framework.binary_transfer.binary_transfer import BinaryTransfer


class TestInitializeNew:
    async def test_should_initialize_binary_transfer(self):
        # Create binary transfer
        binary_transfer = BinaryTransfer.new(size=5, chunks=3)

        # Assert that the method returns the correct value
        assert binary_transfer.size == 5
        assert binary_transfer.chunks == [None, None, None]
        assert binary_transfer.is_completed is False
        assert binary_transfer.buffer == b""
        assert binary_transfer.lifetime.total_seconds > 0


class TestInitializeFromBuffer:
    async def test_should_initialize_binary_transfer(self):
        # Create binary transfer
        binary_transfer = BinaryTransfer.from_buffer(b"abcde")

        # Assert that the method returns the correct value
        assert binary_transfer.size == 5
        assert binary_transfer.chunks == [b"abcde"]
        assert binary_transfer.is_completed is True
        assert binary_transfer.buffer == b"abcde"
        assert binary_transfer.lifetime.total_seconds > 0


class TestGetChunk:
    async def test_should_get_chunk(self):
        # Create binary transfer
        binary_transfer = BinaryTransfer.from_buffer(b"abcde")

        # Get chunk
        chunk_0 = binary_transfer.get_chunk(0, 2)
        chunk_1 = binary_transfer.get_chunk(2, 2)
        chunk_2 = binary_transfer.get_chunk(4, 1)

        # Assert that the method returns the correct value
        assert chunk_0 == b"ab"
        assert chunk_1 == b"cd"
        assert chunk_2 == b"e"

    async def test_should_raise_on_oversized_length(self):
        # Create binary transfer
        binary_transfer = BinaryTransfer.from_buffer(b"abcde")

        # Get chunk
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Expected length of chunk with offset '0' to not exceed "
                "the maximum size of 2 MiB, received 2097153 bytes."
            ),
        ):
            binary_transfer.get_chunk(0, 2**21 + 1)

    async def test_should_raise_on_overflowing_offset(self):
        # Create binary transfer
        binary_transfer = BinaryTransfer.from_buffer(b"abcde")

        # Get chunk
        with pytest.raises(
            ValueError,
            match=re.escape("Expected offset to not exceed the binary's size of 5 bytes, received 10 bytes."),
        ):
            binary_transfer.get_chunk(10, 1)

    async def test_should_raise_on_overflowing_length(self):
        # Create binary transfer
        binary_transfer = BinaryTransfer.from_buffer(b"abcde")

        # Get chunk
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Expected length of chunk with offset '0' to not exceed "
                "the binary's size of 5 bytes, received 10 bytes."
            ),
        ):
            binary_transfer.get_chunk(0, 10)


class TestSetChunk:
    async def test_should_set_chunk(self):
        # Create binary transfer
        binary_transfer = BinaryTransfer.new(5, 3)

        # Set chunk
        binary_transfer.set_chunk(0, b"ab")
        binary_transfer.set_chunk(1, b"cd")
        binary_transfer.set_chunk(2, b"e")

        # Assert that the method returns the correct value
        assert binary_transfer.buffer == b"abcde"

    async def test_should_raise_on_already_completed_binary(self):
        # Create binary transfer
        binary_transfer = BinaryTransfer.new(0, 0)

        # Set chunk
        with pytest.raises(
            ValueError,
            match=re.escape("Received chunk with index '0' for already completed binary transfer."),
        ):
            binary_transfer.set_chunk(0, b"")

    async def test_should_raise_on_oversized_chunk(self):
        # Create binary transfer
        binary_transfer = BinaryTransfer.new(0, 1)

        # Set chunk
        with pytest.raises(
            ValueError,
            match=re.escape("Expected chunk '0' to not exceed the maximum size of 2 MiB, received 2097153 bytes."),
        ):
            binary_transfer.set_chunk(0, b" " * (2**21 + 1))

    async def test_should_raise_on_invalid_index(self):
        # Create binary transfer
        binary_transfer = BinaryTransfer.new(0, 1)

        # Set chunk
        with pytest.raises(
            ValueError,
            match=re.escape("Expected chunks up to index '0', received '1'."),
        ):
            binary_transfer.set_chunk(1, b"")

    async def test_should_raise_on_duplicate_chunk(self):
        # Create binary transfer
        binary_transfer = BinaryTransfer.new(1, 2)

        # Set chunk
        binary_transfer.set_chunk(0, b"")
        with pytest.raises(
            ValueError,
            match=re.escape("Received chunk with index '0' for already received chunk."),
        ):
            binary_transfer.set_chunk(0, b"")

    async def test_should_raise_on_overflowing_bytes(self):
        # Create binary transfer
        binary_transfer = BinaryTransfer.new(0, 1)

        # Set chunk
        with pytest.raises(
            ValueError,
            match=re.escape("Expected a total size of 0 bytes, received already 3 bytes with chunk '0'."),
        ):
            binary_transfer.set_chunk(0, b"...")
