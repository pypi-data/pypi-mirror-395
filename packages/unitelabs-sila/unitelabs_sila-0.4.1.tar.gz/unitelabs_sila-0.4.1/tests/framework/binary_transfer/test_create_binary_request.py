import pytest

from sila.framework.binary_transfer.create_binary_request import CreateBinaryRequest

ENCODE_TEST_CASES = [
    pytest.param(CreateBinaryRequest(binary_size=5124), b"\x08\x84\x28", id="1: 5124"),
    pytest.param(CreateBinaryRequest(chunk_count=42), b"\x10\x2a", id="2: 42"),
    pytest.param(
        CreateBinaryRequest(
            parameter_identifier="org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier"
        ),
        b"\x1a\x5dorg.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier",
        id='3: {"org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier"}',
    ),
    pytest.param(
        CreateBinaryRequest(
            binary_size=5124,
            chunk_count=42,
            parameter_identifier="org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier",
        ),
        b"\x08\x84\x28\x10\x2a\x1a\x5dorg.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier",
        id=(
            "1: 5124, 2: 42, "
            '3: {"org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier"}'
        ),
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        CreateBinaryRequest(
            binary_size=5124,
            chunk_count=42,
            parameter_identifier="org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier",
        ),
        b"\x20\x00\x1a\x5dorg.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier\x10\x2a\x08\x84\x28",
        id=(
            "4: 0, "
            '3: {"org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier"}, '
            "2: 42, 1: 5124"
        ),
    ),
]


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode message
        message = CreateBinaryRequest.decode(b"")

        # Assert that the method returns the correct value
        assert message == CreateBinaryRequest()

    @pytest.mark.parametrize(("instance", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, instance: CreateBinaryRequest, buffer: bytes):
        # Decode message
        message = CreateBinaryRequest.decode(buffer)

        # Assert that the method returns the correct value
        assert message == instance

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = CreateBinaryRequest.decode(b"\x1a\x05Hello\x1a\x05World")

        # Assert that the method returns the correct value
        assert message == CreateBinaryRequest(parameter_identifier="World")

    async def test_should_decode_limited_buffer(self):
        # Decode message
        message = CreateBinaryRequest.decode(
            b"\x1a\x05Hello\x1a\x05World",
            len(b"\x1a\x05Hello"),
        )

        # Assert that the method returns the correct value
        assert message == CreateBinaryRequest(parameter_identifier="Hello")


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode message
        message = CreateBinaryRequest().encode()

        # Assert that the method returns the correct value
        assert message == b""

    @pytest.mark.parametrize(("instance", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, instance: CreateBinaryRequest, buffer: bytes):
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
        instance = CreateBinaryRequest()
        message = instance.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer
