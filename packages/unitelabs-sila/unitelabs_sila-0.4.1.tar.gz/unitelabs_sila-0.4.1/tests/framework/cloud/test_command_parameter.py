import pytest

from sila.framework.cloud.cloud_metadata import CloudMetadata
from sila.framework.cloud.command_parameter import CommandParameter

ENCODE_TEST_CASES = [
    pytest.param(
        CommandParameter(parameters=b"\x0a\x05Hello"),
        b"\x12\x07\x0a\x05Hello",
        id='2: {"\x0a\x05Hello"}',
    ),
    pytest.param(
        CommandParameter(
            metadata=[
                CloudMetadata(
                    fully_qualified_metadata_id="org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken",
                    value=b"Token",
                ),
            ],
        ),
        b"\x0a\x4b\x0a\x42org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken\x12\x05Token",
        id='1: { 1: {"org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken"}, 2: {"Token"} }',
    ),
    pytest.param(
        CommandParameter(
            parameters=b"\x0a\x05Hello",
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
            b"\x0a\x4b\x0a\x42org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken\x12\x05Token"
            b"\x0a\x4d\x0a\x41org.silastandard/test/MetadataProvider/v1/Metadata/StringMetadata\x12\x08Metadata"
            b"\x12\x07\x0a\x05Hello"
        ),
        id=(
            '1: { 1: {"org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken"}, 2: {"Token"} }, '
            '1: { 1: {"org.silastandard/test/MetadataProvider/v1/Metadata/StringMetadata"}, 2: {"Metadata"} }, '
            '2: {"\x0a\x05Hello"}'
        ),
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        CommandParameter(
            parameters=b"\x0a\x05Hello",
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
            b"\x18\x00"
            b"\x0a\x4b\x0a\x42org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken\x12\x05Token"
            b"\x12\x07\x0a\x05Hello"
            b"\x0a\x4d\x0a\x41org.silastandard/test/MetadataProvider/v1/Metadata/StringMetadata\x12\x08Metadata"
        ),
        id=(
            "3: 0, "
            '1: { 1: {"org.silastandard/test/MetadataProvider/v1/Metadata/StringMetadata"}, 2: {"Metadata"} }, '
            '2: {"\x0a\x05Hello"}, '
            '1: { 1: {"org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken"}, 2: {"Token"} }'
        ),
    ),
]


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode message
        message = CommandParameter.decode(b"")

        # Assert that the method returns the correct value
        assert message == CommandParameter()

    @pytest.mark.parametrize(("instance", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, instance: CommandParameter, buffer: bytes):
        # Decode message
        message = CommandParameter.decode(buffer)

        # Assert that the method returns the correct value
        assert message == instance

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = CommandParameter.decode(b"\x12\x07\x0a\x05Hello\x12\x07\x0a\x05World")

        # Assert that the method returns the correct value
        assert message == CommandParameter(parameters=b"\x0a\x05World")

    async def test_should_decode_limited_buffer(self):
        # Decode message
        message = CommandParameter.decode(b"\x12\x07\x0a\x05Hello\x12\x07\x0a\x05World", 9)

        # Assert that the method returns the correct value
        assert message == CommandParameter(parameters=b"\x0a\x05Hello")


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode message
        message = CommandParameter().encode()

        # Assert that the method returns the correct value
        assert message == b""

    @pytest.mark.parametrize(("instance", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, instance: CommandParameter, buffer: bytes):
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
        instance = CommandParameter()
        message = instance.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer
