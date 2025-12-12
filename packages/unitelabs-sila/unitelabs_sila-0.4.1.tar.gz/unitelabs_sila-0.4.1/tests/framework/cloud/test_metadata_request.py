import pytest

from sila.framework.cloud.metadata_request import MetadataRequest

ENCODE_TEST_CASES = [
    pytest.param(
        MetadataRequest(
            fully_qualified_metadata_id="org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken"
        ),
        b"\x0a\x42org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken",
        id='1: {"org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken"}',
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        MetadataRequest(
            fully_qualified_metadata_id="org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken"
        ),
        b"\x10\x00\x0a\x42org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken",
        id='2: 0, 1: {"org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken"}',
    ),
]


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode message
        message = MetadataRequest.decode(b"")

        # Assert that the method returns the correct value
        assert message == MetadataRequest()

    @pytest.mark.parametrize(("instance", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, instance: MetadataRequest, buffer: bytes):
        # Decode message
        message = MetadataRequest.decode(buffer)

        # Assert that the method returns the correct value
        assert message == instance

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = MetadataRequest.decode(b"\x0a\x05Hello\x0a\x05World")

        # Assert that the method returns the correct value
        assert message == MetadataRequest(fully_qualified_metadata_id="World")

    async def test_should_decode_limited_buffer(self):
        # Decode message
        message = MetadataRequest.decode(b"\x0a\x05Hello\x0a\x05World", 7)

        # Assert that the method returns the correct value
        assert message == MetadataRequest(fully_qualified_metadata_id="Hello")


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode message
        message = MetadataRequest().encode()

        # Assert that the method returns the correct value
        assert message == b""

    @pytest.mark.parametrize(("instance", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, instance: MetadataRequest, buffer: bytes):
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
        instance = MetadataRequest()
        message = instance.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer
