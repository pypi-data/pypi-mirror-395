import pytest

from sila.framework.binary_transfer.upload_chunk_response import UploadChunkResponse
from sila.framework.data_types.duration import Duration

ENCODE_TEST_CASES = [
    pytest.param(
        UploadChunkResponse(binary_transfer_uuid="00000000-0000-0000-0000-000000000000"),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x1a\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 3: {}',
    ),
    pytest.param(UploadChunkResponse(chunk_index=42), b"\x10\x2a\x1a\x00", id="2: 42, 3: {}"),
    pytest.param(
        UploadChunkResponse(lifetime_of_binary=Duration(seconds=12, nanos=34000)),
        b"\x1a\x06\x08\x0c\x10\xd0\x89\x02",
        id="3: { 1: 12, 2: 34000 }",
    ),
    pytest.param(
        UploadChunkResponse(
            binary_transfer_uuid="00000000-0000-0000-0000-000000000000",
            chunk_index=42,
            lifetime_of_binary=Duration(seconds=12, nanos=34000),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x10\x2a\x1a\x06\x08\x0c\x10\xd0\x89\x02",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 2: 42, 3: { 1: 12, 2: 34000 }',
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        UploadChunkResponse(
            binary_transfer_uuid="00000000-0000-0000-0000-000000000000",
            chunk_index=42,
            lifetime_of_binary=Duration(seconds=12, nanos=34000),
        ),
        b"\x20\x00\x1a\x06\x08\x0c\x10\xd0\x89\x02\x10\x2a\x0a\x2400000000-0000-0000-0000-000000000000",
        id='4: 0, 3: { 1: 12, 2: 34000 }, 2: 42, 1: {"00000000-0000-0000-0000-000000000000"}',
    ),
]


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode message
        message = UploadChunkResponse.decode(b"")

        # Assert that the method returns the correct value
        assert message == UploadChunkResponse()

    @pytest.mark.parametrize(("instance", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, instance: UploadChunkResponse, buffer: bytes):
        # Decode message
        message = UploadChunkResponse.decode(buffer)

        # Assert that the method returns the correct value
        assert message == instance

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = UploadChunkResponse.decode(b"\x0a\x05Hello\x0a\x05World")

        # Assert that the method returns the correct value
        assert message == UploadChunkResponse(binary_transfer_uuid="World")

    async def test_should_decode_limited_buffer(self):
        # Decode message
        message = UploadChunkResponse.decode(b"\x0a\x05Hello\x0a\x05World", 7)

        # Assert that the method returns the correct value
        assert message == UploadChunkResponse(binary_transfer_uuid="Hello")


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode message
        message = UploadChunkResponse().encode()

        # Assert that the method returns the correct value
        assert message == b"\x1a\x00"

    @pytest.mark.parametrize(("instance", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, instance: UploadChunkResponse, buffer: bytes):
        # Encode message
        message = instance.encode()

        # Assert that the method returns the correct value
        assert message == buffer

    @pytest.mark.parametrize(
        ("number", "buffer"),
        [
            pytest.param(1, b"\x0a\x02\x1a\x00", id="default"),
            pytest.param(2, b"\x12\x02\x1a\x00", id="custom"),
        ],
    )
    async def test_should_encode_field_number(self, number: int, buffer: bytes):
        # Encode message
        instance = UploadChunkResponse()
        message = instance.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer
