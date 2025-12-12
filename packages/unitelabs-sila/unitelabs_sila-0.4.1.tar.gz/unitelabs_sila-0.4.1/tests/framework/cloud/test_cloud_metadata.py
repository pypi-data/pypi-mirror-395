import pytest

from sila.framework.cloud.cloud_metadata import CloudMetadata

ENCODE_TEST_CASES = [
    pytest.param(
        CloudMetadata(fully_qualified_metadata_id="org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken"),
        b"\x0a\x42org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken",
        id='1: {"org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken"}',
    ),
    pytest.param(
        CloudMetadata(value=b"Token"),
        b"\x12\x05Token",
        id='2: {"Token"}',
    ),
    pytest.param(
        CloudMetadata(
            fully_qualified_metadata_id="org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken",
            value=b"Token",
        ),
        b"\x0a\x42org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken\x12\x05Token",
        id='1: {"org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken"}, 2: {"Token"}',
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        CloudMetadata(
            fully_qualified_metadata_id="org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken",
            value=b"Token",
        ),
        b"\x18\x00\x12\x05Token\x0a\x42org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken",
        id='3: 0, 2: {"Token"}, 1: {"org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken"}',
    ),
]


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode message
        message = CloudMetadata.decode(b"")

        # Assert that the method returns the correct value
        assert message == CloudMetadata()

    @pytest.mark.parametrize(("instance", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, instance: CloudMetadata, buffer: bytes):
        # Decode message
        message = CloudMetadata.decode(buffer)

        # Assert that the method returns the correct value
        assert message == instance

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = CloudMetadata.decode(b"\x0a\x05Hello\x0a\x05World")

        # Assert that the method returns the correct value
        assert message == CloudMetadata(fully_qualified_metadata_id="World")

    async def test_should_decode_limited_buffer(self):
        # Decode message
        message = CloudMetadata.decode(b"\x0a\x05Hello\x0a\x05World", 7)

        # Assert that the method returns the correct value
        assert message == CloudMetadata(fully_qualified_metadata_id="Hello")


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode message
        message = CloudMetadata().encode()

        # Assert that the method returns the correct value
        assert message == b""

    @pytest.mark.parametrize(("instance", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, instance: CloudMetadata, buffer: bytes):
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
        instance = CloudMetadata()
        message = instance.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer
