import pytest

from sila.framework.binary_transfer.get_binary_info_response import GetBinaryInfoResponse
from sila.framework.data_types.duration import Duration

ENCODE_TEST_CASES = [
    pytest.param(
        GetBinaryInfoResponse(binary_size=42),
        b"\x08\x2a\x12\x00",
        id="1: 42, 2: {}",
    ),
    pytest.param(
        GetBinaryInfoResponse(lifetime_of_binary=Duration(seconds=12, nanos=34000)),
        b"\x12\x06\x08\x0c\x10\xd0\x89\x02",
        id="2: { 1: 12, 2: 34000 }",
    ),
    pytest.param(
        GetBinaryInfoResponse(binary_size=42, lifetime_of_binary=Duration(seconds=12, nanos=34000)),
        b"\x08\x2a\x12\x06\x08\x0c\x10\xd0\x89\x02",
        id="1: 42, 2: { 1: 12, 2: 34000 }",
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        GetBinaryInfoResponse(binary_size=42, lifetime_of_binary=Duration(seconds=12, nanos=34000)),
        b"\x18\x00\x12\x06\x08\x0c\x10\xd0\x89\x02\x08\x2a",
        id="3: 0, 2: { 1: 12, 2: 34000 }, 1: 42",
    ),
]


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode message
        message = GetBinaryInfoResponse.decode(b"")

        # Assert that the method returns the correct value
        assert message == GetBinaryInfoResponse()

    @pytest.mark.parametrize(("instance", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, instance: GetBinaryInfoResponse, buffer: bytes):
        # Decode message
        message = GetBinaryInfoResponse.decode(buffer)

        # Assert that the method returns the correct value
        assert message == instance

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = GetBinaryInfoResponse.decode(b"\x08\x01\x08\x00")

        # Assert that the method returns the correct value
        assert message == GetBinaryInfoResponse(binary_size=0)

    async def test_should_decode_limited_buffer(self):
        # Decode message
        message = GetBinaryInfoResponse.decode(b"\x08\x01\x08\x00", 2)

        # Assert that the method returns the correct value
        assert message == GetBinaryInfoResponse(binary_size=1)


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode message
        message = GetBinaryInfoResponse().encode()

        # Assert that the method returns the correct value
        assert message == b"\x12\x00"

    @pytest.mark.parametrize(("instance", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, instance: GetBinaryInfoResponse, buffer: bytes):
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
        instance = GetBinaryInfoResponse()
        message = instance.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer
