import pytest

from sila.framework.binary_transfer.download_chunk_response import DownloadChunkResponse
from sila.framework.data_types.duration import Duration

ENCODE_TEST_CASES = [
    pytest.param(
        DownloadChunkResponse(binary_transfer_uuid="00000000-0000-0000-0000-000000000000"),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x22\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 4: {}',
    ),
    pytest.param(DownloadChunkResponse(offset=42), b"\x10\x2a\x22\x00", id="2: 42"),
    pytest.param(
        DownloadChunkResponse(payload=b"Hello, World!"),
        b"\x1a\x0dHello, World!\x22\x00",
        id='3: {"Hello, World!"}, 4: {}',
    ),
    pytest.param(
        DownloadChunkResponse(lifetime_of_binary=Duration(seconds=12, nanos=34000)),
        b"\x22\x06\x08\x0c\x10\xd0\x89\x02",
        id="4: { 1: 12, 2: 34000 }",
    ),
    pytest.param(
        DownloadChunkResponse(
            binary_transfer_uuid="00000000-0000-0000-0000-000000000000",
            offset=42,
            payload=b"Hello, World!",
            lifetime_of_binary=Duration(seconds=12, nanos=34000),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x10\x2a\x1a\x0dHello, World!\x22\x06\x08\x0c\x10\xd0\x89\x02",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 2: 42, 3: {"Hello, World!"}, 4: { 1: 12, 2: 34000 }',
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        DownloadChunkResponse(
            binary_transfer_uuid="00000000-0000-0000-0000-000000000000",
            offset=42,
            payload=b"Hello, World!",
            lifetime_of_binary=Duration(seconds=12, nanos=34000),
        ),
        (
            b"\x28\x00\x22\x06\x08\x0c\x10\xd0\x89\x02\x1a\x0dHello, World!"
            b"\x10\x2a\x0a\x2400000000-0000-0000-0000-000000000000"
        ),
        id='5: 0, 4: { 1: 12, 2: 34000 }, 3: {"Hello, World!"}, 2: 42, 1: {"00000000-0000-0000-0000-000000000000"}',
    ),
]


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode message
        message = DownloadChunkResponse.decode(b"")

        # Assert that the method returns the correct value
        assert message == DownloadChunkResponse()

    @pytest.mark.parametrize(("instance", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, instance: DownloadChunkResponse, buffer: bytes):
        # Decode message
        message = DownloadChunkResponse.decode(buffer)

        # Assert that the method returns the correct value
        assert message == instance

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = DownloadChunkResponse.decode(
            b"\x0a\x05Hello\x0a\x05World",
        )

        # Assert that the method returns the correct value
        assert message == DownloadChunkResponse(binary_transfer_uuid="World")

    async def test_should_decode_limited_buffer(self):
        # Decode message
        message = DownloadChunkResponse.decode(b"\x0a\x05Hello\x0a\x05World", 7)

        # Assert that the method returns the correct value
        assert message == DownloadChunkResponse(binary_transfer_uuid="Hello")


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode message
        message = DownloadChunkResponse().encode()

        # Assert that the method returns the correct value
        assert message == b"\x22\x00"

    @pytest.mark.parametrize(("instance", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, instance: DownloadChunkResponse, buffer: bytes):
        # Encode message
        message = instance.encode()

        # Assert that the method returns the correct value
        assert message == buffer

    @pytest.mark.parametrize(
        ("number", "buffer"),
        [
            pytest.param(1, b"\x0a\x02\x22\x00", id="default"),
            pytest.param(2, b"\x12\x02\x22\x00", id="custom"),
        ],
    )
    async def test_should_encode_field_number(self, number: int, buffer: bytes):
        # Encode message
        instance = DownloadChunkResponse()
        message = instance.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer
