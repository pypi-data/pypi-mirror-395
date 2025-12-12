import pytest

from sila.framework.cloud.cloud_metadata import CloudMetadata
from sila.framework.cloud.property_request import PropertyRequest

ENCODE_TEST_CASES = [
    pytest.param(
        PropertyRequest(
            fully_qualified_property_id="org.silastandard/core/SiLAService/v1/Property/ServerUUID",
        ),
        b"\x0a\x38org.silastandard/core/SiLAService/v1/Property/ServerUUID",
        id='1: {"org.silastandard/core/SiLAService/v1/Property/ServerUUID"}',
    ),
    pytest.param(
        PropertyRequest(
            metadata=[
                CloudMetadata(
                    fully_qualified_metadata_id="org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken",
                    value=b"Token",
                ),
            ],
        ),
        b"\x12\x4b\x0a\x42org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken\x12\x05Token",
        id='2: { 1: {"org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken"}, 2: {"Token"} }',
    ),
    pytest.param(
        PropertyRequest(
            fully_qualified_property_id="org.silastandard/core/SiLAService/v1/Property/ServerUUID",
            metadata=[
                CloudMetadata(
                    fully_qualified_metadata_id="org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken",
                    value=b"Token",
                ),
                CloudMetadata(
                    fully_qualified_metadata_id="org.silastandard/test/MetadataProvider/v1/Metadata/StringMetadata",
                    value=b"Metadata",
                ),
            ],
        ),
        (
            b"\x0a\x38org.silastandard/core/SiLAService/v1/Property/ServerUUID"
            b"\x12\x4b\x0a\x42org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken\x12\x05Token"
            b"\x12\x4d\x0a\x41org.silastandard/test/MetadataProvider/v1/Metadata/StringMetadata\x12\x08Metadata"
        ),
        id=(
            '1: {"org.silastandard/core/SiLAService/v1/Property/ServerUUID"}, '
            '2: { 1: {"org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken"}, 2: {"Token"} }, '
            '2: { 1: {"org.silastandard/test/MetadataProvider/v1/Metadata/StringMetadata"}, 2: {"Metadata"} }'
        ),
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        PropertyRequest(
            fully_qualified_property_id="org.silastandard/core/SiLAService/v1/Property/ServerUUID",
            metadata=[
                CloudMetadata(
                    fully_qualified_metadata_id="org.silastandard/test/MetadataProvider/v1/Metadata/StringMetadata",
                    value=b"Metadata",
                ),
                CloudMetadata(
                    fully_qualified_metadata_id="org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken",
                    value=b"Token",
                ),
            ],
        ),
        (
            b"\x18\x00"
            b"\x12\x4d\x0a\x41org.silastandard/test/MetadataProvider/v1/Metadata/StringMetadata\x12\x08Metadata"
            b"\x0a\x38org.silastandard/core/SiLAService/v1/Property/ServerUUID"
            b"\x12\x4b\x0a\x42org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken\x12\x05Token"
        ),
        id=(
            "3: 0, "
            '2: { 1: {"org.silastandard/test/MetadataProvider/v1/Metadata/StringMetadata"}, 2: {"Metadata"} }, '
            '1: {"org.silastandard/core/SiLAService/v1/Property/ServerUUID"}, '
            '2: { 1: {"org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken"}, 2: {"Token"} }'
        ),
    ),
]


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode message
        message = PropertyRequest.decode(b"")

        # Assert that the method returns the correct value
        assert message == PropertyRequest()

    @pytest.mark.parametrize(("instance", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, instance: PropertyRequest, buffer: bytes):
        # Decode message
        message = PropertyRequest.decode(buffer)

        # Assert that the method returns the correct value
        assert message == instance

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = PropertyRequest.decode(b"\x0a\x05Hello\x0a\x05World")

        # Assert that the method returns the correct value
        assert message == PropertyRequest(fully_qualified_property_id="World")

    async def test_should_decode_limited_buffer(self):
        # Decode message
        message = PropertyRequest.decode(b"\x0a\x05Hello\x0a\x05World", 7)

        # Assert that the method returns the correct value
        assert message == PropertyRequest(fully_qualified_property_id="Hello")


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode message
        message = PropertyRequest().encode()

        # Assert that the method returns the correct value
        assert message == b""

    @pytest.mark.parametrize(("instance", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, instance: PropertyRequest, buffer: bytes):
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
        instance = PropertyRequest()
        message = instance.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer
