import pytest

from sila.framework.cloud.property_response import PropertyResponse

ENCODE_TEST_CASES = [
    pytest.param(
        PropertyResponse(value=b"\x0a\x05Hello"),
        b"\x0a\x07\x0a\x05Hello",
        id='1: {"\x0a\x05Hello"}',
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        PropertyResponse(value=b"\x0a\x05Hello"),
        b"\x10\x00\x0a\x07\x0a\x05Hello",
        id='2: 0, 1: {"\x0a\x05Hello"}',
    ),
]


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode message
        message = PropertyResponse.decode(b"")

        # Assert that the method returns the correct value
        assert message == PropertyResponse()

    @pytest.mark.parametrize(("instance", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, instance: PropertyResponse, buffer: bytes):
        # Decode message
        message = PropertyResponse.decode(buffer)

        # Assert that the method returns the correct value
        assert message == instance

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = PropertyResponse.decode(b"\x0a\x07\x0a\x05Hello\x0a\x07\x0a\x05World")

        # Assert that the method returns the correct value
        assert message == PropertyResponse(value=b"\x0a\x05World")

    async def test_should_decode_limited_buffer(self):
        # Decode message
        message = PropertyResponse.decode(b"\x0a\x07\x0a\x05Hello\x0a\x07\x0a\x05World", 9)

        # Assert that the method returns the correct value
        assert message == PropertyResponse(value=b"\x0a\x05Hello")


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode message
        message = PropertyResponse().encode()

        # Assert that the method returns the correct value
        assert message == b""

    @pytest.mark.parametrize(("instance", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, instance: PropertyResponse, buffer: bytes):
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
        instance = PropertyResponse()
        message = instance.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer
