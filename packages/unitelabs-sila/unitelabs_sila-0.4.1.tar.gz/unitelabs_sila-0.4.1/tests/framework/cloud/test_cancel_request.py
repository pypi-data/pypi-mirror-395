import pytest

from sila.framework.cloud.cancel_request import CancelRequest


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode message
        message = CancelRequest.decode(b"")

        # Assert that the method returns the correct value
        assert message == CancelRequest()

    async def test_should_decode_custom_buffer(self):
        # Decode message
        message = CancelRequest.decode(b"\x08\x00")

        # Assert that the method returns the correct value
        assert message == CancelRequest()

    async def test_should_decode_limited_buffer(self):
        # Decode message
        message = CancelRequest.decode(b"\x08\x00", 0)

        # Assert that the method returns the correct value
        assert message == CancelRequest()


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode message
        message = CancelRequest().encode()

        # Assert that the method returns the correct value
        assert message == b""

    @pytest.mark.parametrize(
        ("number", "buffer"),
        [
            pytest.param(1, b"\x0a\x00", id="default"),
            pytest.param(2, b"\x12\x00", id="custom"),
        ],
    )
    async def test_should_encode_field_number(self, number: int, buffer: bytes):
        # Encode message
        instance = CancelRequest()
        message = instance.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer
