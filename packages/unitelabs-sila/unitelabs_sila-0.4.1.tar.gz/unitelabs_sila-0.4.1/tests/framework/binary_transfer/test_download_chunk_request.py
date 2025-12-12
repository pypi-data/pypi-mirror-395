import pytest

from sila.framework.binary_transfer.download_chunk_request import DownloadChunkRequest

ENCODE_TEST_CASES = [
    pytest.param(
        DownloadChunkRequest(binary_transfer_uuid="00000000-0000-0000-0000-000000000000"),
        b"\x0a\x2400000000-0000-0000-0000-000000000000",
        id='1: {"00000000-0000-0000-0000-000000000000"}',
    ),
    pytest.param(DownloadChunkRequest(offset=42), b"\x10\x2a", id="2: 42"),
    pytest.param(DownloadChunkRequest(length=5124), b"\x18\x84\x28", id="3: 5124"),
    pytest.param(
        DownloadChunkRequest(binary_transfer_uuid="00000000-0000-0000-0000-000000000000", offset=42, length=5124),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x10\x2a\x18\x84\x28",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 2: 42, 3: 5124',
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        DownloadChunkRequest(binary_transfer_uuid="00000000-0000-0000-0000-000000000000", offset=42, length=5124),
        b"\x20\x00\x18\x84\x28\x10\x2a\x0a\x2400000000-0000-0000-0000-000000000000",
        id='4: 0, 3: 5124, 2: 42, 1: {"00000000-0000-0000-0000-000000000000"}',
    ),
]


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode message
        message = DownloadChunkRequest.decode(b"")

        # Assert that the method returns the correct value
        assert message == DownloadChunkRequest()

    @pytest.mark.parametrize(("instance", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, instance: DownloadChunkRequest, buffer: bytes):
        # Decode message
        message = DownloadChunkRequest.decode(buffer)

        # Assert that the method returns the correct value
        assert message == instance

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = DownloadChunkRequest.decode(b"\x0a\x05Hello\x0a\x05World")

        # Assert that the method returns the correct value
        assert message == DownloadChunkRequest(binary_transfer_uuid="World")

    async def test_should_decode_limited_buffer(self):
        # Decode message
        message = DownloadChunkRequest.decode(b"\x0a\x05Hello\x0a\x05World", 7)

        # Assert that the method returns the correct value
        assert message == DownloadChunkRequest(binary_transfer_uuid="Hello")


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode message
        message = DownloadChunkRequest().encode()

        # Assert that the method returns the correct value
        assert message == b""

    @pytest.mark.parametrize(("instance", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, instance: DownloadChunkRequest, buffer: bytes):
        # Encode message
        message = instance.encode()

        # Assert that the method returns the correct value
        assert message == buffer

    @pytest.mark.parametrize(
        ("number", "buffer"),
        [
            pytest.param(1, b"\x0a\x00", id="default"),
            pytest.param(2, b"\x12\x00", id="custom"),
        ],
    )
    async def test_should_encode_field_number(self, number: int, buffer: bytes):
        # Encode message
        instance = DownloadChunkRequest()
        message = instance.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer
