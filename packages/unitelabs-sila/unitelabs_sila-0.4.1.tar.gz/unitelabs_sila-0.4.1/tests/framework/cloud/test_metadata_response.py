import pytest

from sila.framework.cloud.metadata_response import MetadataResponse

ENCODE_TEST_CASES = [
    pytest.param(
        MetadataResponse(affected_calls=["Hello", "World"]),
        b"\x0a\x05Hello\x0a\x05World",
        id='1: {"Hello"}, 1: {"World"}',
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        MetadataResponse(affected_calls=["Hello", "World"]),
        b"\x10\x00\x0a\x05Hello\x0a\x05World",
        id='2: 0, 1: {"Hello"}, 1: {"World"}',
    ),
]


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode message
        message = MetadataResponse.decode(b"")

        # Assert that the method returns the correct value
        assert message == MetadataResponse()

    @pytest.mark.parametrize(("instance", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, instance: MetadataResponse, buffer: bytes):
        # Decode message
        message = MetadataResponse.decode(buffer)

        # Assert that the method returns the correct value
        assert message == instance

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = MetadataResponse.decode(b"\x0a\x05Hello\x0a\x05World")

        # Assert that the method returns the correct value
        assert message == MetadataResponse(affected_calls=["Hello", "World"])

    async def test_should_decode_limited_buffer(self):
        # Decode message
        message = MetadataResponse.decode(b"\x0a\x05Hello\x0a\x05World", 0)

        # Assert that the method returns the correct value
        assert message == MetadataResponse(affected_calls=[])


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode message
        message = MetadataResponse().encode()

        # Assert that the method returns the correct value
        assert message == b""

    @pytest.mark.parametrize(("instance", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, instance: MetadataResponse, buffer: bytes):
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
        instance = MetadataResponse()
        message = instance.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer
