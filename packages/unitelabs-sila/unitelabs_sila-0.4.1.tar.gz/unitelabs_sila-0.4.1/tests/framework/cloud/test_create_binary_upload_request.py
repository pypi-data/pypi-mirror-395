import pytest

from sila.framework.binary_transfer.create_binary_request import CreateBinaryRequest
from sila.framework.cloud.cloud_metadata import CloudMetadata
from sila.framework.cloud.create_binary_upload_request import CreateBinaryUploadRequest

ENCODE_TEST_CASES = [
    pytest.param(
        CreateBinaryUploadRequest(
            create_binary_request=CreateBinaryRequest(
                binary_size=5124,
                chunk_count=42,
                parameter_identifier="org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier",
            )
        ),
        b"\x12\x64\x08\x84\x28\x10\x2a\x1a\x5dorg.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier",
        id=(
            "2: { 1: 5124, 2: 42, "
            '3: {"org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier"} }'
        ),
    ),
    pytest.param(
        CreateBinaryUploadRequest(
            metadata=[
                CloudMetadata(
                    fully_qualified_metadata_id="org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken",
                    value=b"Token",
                )
            ]
        ),
        b"\x0a\x4b\x0a\x42org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken\x12\x05Token\x12\x00",
        id='1: { 1: {"org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken"}, 2: {"Token"} }',
    ),
    pytest.param(
        CreateBinaryUploadRequest(
            create_binary_request=CreateBinaryRequest(
                binary_size=5124,
                chunk_count=42,
                parameter_identifier="org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier",
            ),
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
            b"\x12\x64\x08\x84\x28\x10\x2a\x1a\x5dorg.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier"
        ),
        id=(
            "2: { "
            "1: 5124, 2: 42, "
            '3: {"org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier"} '
            "}, "
            '1: { 1: {"org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken"}, 2: {"Token"} }, '
            '1: { 1: {"org.silastandard/test/MetadataProvider/v1/Metadata/StringMetadata"}, 2: {"Metadata"} }'
        ),
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        CreateBinaryUploadRequest(
            create_binary_request=CreateBinaryRequest(
                binary_size=5124,
                chunk_count=42,
                parameter_identifier="org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier",
            ),
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
            b"\x0a\x4d\x0a\x41org.silastandard/test/MetadataProvider/v1/Metadata/StringMetadata\x12\x08Metadata"
            b"\x12\x64\x08\x84\x28\x10\x2a\x1a\x5dorg.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier"
        ),
        id=(
            "3: 0, "
            '1: { 1: {"org.silastandard/test/MetadataProvider/v1/Metadata/StringMetadata"}, 2: {"Metadata"} }, '
            "2: { "
            "1: 5124, 2: 42, "
            '3: {"org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier"} '
            "}, "
            '1: { 1: {"org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken"}, 2: {"Token"} }'
        ),
    ),
]


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode message
        message = CreateBinaryUploadRequest.decode(b"")

        # Assert that the method returns the correct value
        assert message == CreateBinaryUploadRequest()

    @pytest.mark.parametrize(("instance", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, instance: CreateBinaryUploadRequest, buffer: bytes):
        # Decode message
        message = CreateBinaryUploadRequest.decode(buffer)

        # Assert that the method returns the correct value
        assert message == instance

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = CreateBinaryUploadRequest.decode(b"\x12\x07\x1a\x05Hello\x12\x07\x1a\x05World")

        # Assert that the method returns the correct value
        assert message == CreateBinaryUploadRequest(
            create_binary_request=CreateBinaryRequest(parameter_identifier="World")
        )

    async def test_should_decode_limited_buffer(self):
        # Decode message
        message = CreateBinaryUploadRequest.decode(b"\x12\x07\x1a\x05Hello\x12\x07\x1a\x05World", 9)

        # Assert that the method returns the correct value
        assert message == CreateBinaryUploadRequest(
            create_binary_request=CreateBinaryRequest(parameter_identifier="Hello")
        )


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode message
        message = CreateBinaryUploadRequest().encode()

        # Assert that the method returns the correct value
        assert message == b"\x12\x00"

    @pytest.mark.parametrize(("instance", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, instance: CreateBinaryUploadRequest, buffer: bytes):
        # Encode message
        message = instance.encode()

        # Assert that the method returns the correct value
        assert message == buffer

    @pytest.mark.parametrize(
        ("number", "buffer"),
        [
            pytest.param(1, b"\x0a\x02\x12\x00", id="default"),
            pytest.param(2, b"\x12\x02\x12\x00", id="custom"),
        ],
    )
    async def test_should_encode_field_number(self, number: int, buffer: bytes):
        # Encode message
        instance = CreateBinaryUploadRequest()
        message = instance.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer
