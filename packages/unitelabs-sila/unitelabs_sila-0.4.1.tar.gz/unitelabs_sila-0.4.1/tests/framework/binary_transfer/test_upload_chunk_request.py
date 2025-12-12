import pytest

from sila.framework.binary_transfer.upload_chunk_request import UploadChunkRequest

ENCODE_TEST_CASES = [
    pytest.param(
        UploadChunkRequest(binary_transfer_uuid="00000000-0000-0000-0000-000000000000"),
        b"\x0a\x2400000000-0000-0000-0000-000000000000",
        id='1: {"00000000-0000-0000-0000-000000000000"}',
    ),
    pytest.param(UploadChunkRequest(chunk_index=42), b"\x10\x2a", id="2: 42"),
    pytest.param(
        UploadChunkRequest(payload=b"Hello, World!"),
        b"\x1a\x0dHello, World!",
        id='3: {"Hello, World!"}',
    ),
    pytest.param(
        UploadChunkRequest(
            binary_transfer_uuid="00000000-0000-0000-0000-000000000000", chunk_index=42, payload=b"Hello, World!"
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x10\x2a\x1a\x0dHello, World!",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 2: 42, 3: {"Hello, World!"}',
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        UploadChunkRequest(
            binary_transfer_uuid="00000000-0000-0000-0000-000000000000", chunk_index=42, payload=b"Hello, World!"
        ),
        b"\x20\x00\x1a\x0dHello, World!\x10\x2a\x0a\x2400000000-0000-0000-0000-000000000000",
        id='4: 0, 3: {"Hello, World!"}, 2: 42, 1: {"00000000-0000-0000-0000-000000000000"}',
    ),
]


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode message
        message = UploadChunkRequest.decode(b"")

        # Assert that the method returns the correct value
        assert message == UploadChunkRequest()

    @pytest.mark.parametrize(("instance", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, instance: UploadChunkRequest, buffer: bytes):
        # Decode message
        message = UploadChunkRequest.decode(buffer)

        # Assert that the method returns the correct value
        assert message == instance

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = UploadChunkRequest.decode(b"\x0a\x05Hello\x0a\x05World")

        # Assert that the method returns the correct value
        assert message == UploadChunkRequest(binary_transfer_uuid="World")

    async def test_should_decode_limited_buffer(self):
        # Decode message
        message = UploadChunkRequest.decode(b"\x0a\x05Hello\x0a\x05World", 7)

        # Assert that the method returns the correct value
        assert message == UploadChunkRequest(binary_transfer_uuid="Hello")


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode message
        message = UploadChunkRequest().encode()

        # Assert that the method returns the correct value
        assert message == b""

    @pytest.mark.parametrize(("instance", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, instance: UploadChunkRequest, buffer: bytes):
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
        # Encode
        instance = UploadChunkRequest()
        message = instance.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer
