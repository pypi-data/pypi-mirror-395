import pytest

from sila.framework.binary_transfer.delete_binary_request import DeleteBinaryRequest

ENCODE_TEST_CASES = [
    pytest.param(
        DeleteBinaryRequest(binary_transfer_uuid="00000000-0000-0000-0000-000000000000"),
        b"\x0a\x2400000000-0000-0000-0000-000000000000",
        id='1: {"00000000-0000-0000-0000-000000000000"}',
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        DeleteBinaryRequest(binary_transfer_uuid="00000000-0000-0000-0000-000000000000"),
        b"\x10\x00\x0a\x2400000000-0000-0000-0000-000000000000",
        id='2: 0, 1: {"00000000-0000-0000-0000-000000000000"}',
    ),
]


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode message
        message = DeleteBinaryRequest.decode(b"")

        # Assert that the method returns the correct value
        assert message == DeleteBinaryRequest()

    @pytest.mark.parametrize(("instance", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, instance: DeleteBinaryRequest, buffer: bytes):
        # Decode message
        message = DeleteBinaryRequest.decode(buffer)

        # Assert that the method returns the correct value
        assert message == instance

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = DeleteBinaryRequest.decode(b"\x0a\x05Hello\x0a\x05World")

        # Assert that the method returns the correct value
        assert message == DeleteBinaryRequest(binary_transfer_uuid="World")

    async def test_should_decode_limited_buffer(self):
        # Decode message
        message = DeleteBinaryRequest.decode(
            b"\x0a\x05Hello\x0a\x05World",
            len(b"\x0a\x05Hello"),
        )

        # Assert that the method returns the correct value
        assert message == DeleteBinaryRequest(binary_transfer_uuid="Hello")


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode message
        message = DeleteBinaryRequest().encode()

        # Assert that the method returns the correct value
        assert message == b""

    @pytest.mark.parametrize(("instance", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, instance: DeleteBinaryRequest, buffer: bytes):
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
        instance = DeleteBinaryRequest()
        message = instance.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer
