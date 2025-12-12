import pytest

from sila.framework.cloud.command_execution_response import CommandExecutionResponse
from sila.framework.command.command_execution_info import CommandExecutionInfo, CommandExecutionStatus
from sila.framework.command.command_execution_uuid import CommandExecutionUUID

ENCODE_TEST_CASES = [
    pytest.param(
        CommandExecutionResponse(
            command_execution_uuid=CommandExecutionUUID(value="00000000-0000-0000-0000-000000000000"),
        ),
        b"\x0a\x26\x0a\x2400000000-0000-0000-0000-000000000000\x12\x00",
        id='1: { 1: "00000000-0000-0000-0000-000000000000" }, 2: {}',
    ),
    pytest.param(
        CommandExecutionResponse(execution_info=CommandExecutionInfo(status=CommandExecutionStatus.RUNNING)),
        b"\x0a\x00\x12\x02\x08\x01",
        id="1: {}, 2: { 1: 1 }",
    ),
    pytest.param(
        CommandExecutionResponse(
            command_execution_uuid=CommandExecutionUUID(value="00000000-0000-0000-0000-000000000000"),
            execution_info=CommandExecutionInfo(status=CommandExecutionStatus.RUNNING),
        ),
        b"\x0a\x26\x0a\x2400000000-0000-0000-0000-000000000000\x12\x02\x08\x01",
        id='1: { 1: "00000000-0000-0000-0000-000000000000" }, 2: { 1: 1 }',
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        CommandExecutionResponse(
            command_execution_uuid=CommandExecutionUUID(value="00000000-0000-0000-0000-000000000000"),
            execution_info=CommandExecutionInfo(status=CommandExecutionStatus.RUNNING),
        ),
        b"\x18\x00\x12\x02\x08\x01\x0a\x26\x0a\x2400000000-0000-0000-0000-000000000000",
        id='3: 0, 2: { 1: 1 }, 1: { 1: "00000000-0000-0000-0000-000000000000" }',
    ),
]


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode message
        message = CommandExecutionResponse.decode(b"")

        # Assert that the method returns the correct value
        assert message == CommandExecutionResponse()

    @pytest.mark.parametrize(("instance", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, instance: CommandExecutionResponse, buffer: bytes):
        # Decode message
        message = CommandExecutionResponse.decode(buffer)

        # Assert that the method returns the correct value
        assert message == instance

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = CommandExecutionResponse.decode(b"\x12\x02\x08\x01\x12\x02\x08\x02")

        # Assert that the method returns the correct value
        assert message == CommandExecutionResponse(
            execution_info=CommandExecutionInfo(status=CommandExecutionStatus.FINISHED_SUCCESSFULLY)
        )

    async def test_should_decode_limited_buffer(self):
        # Decode message
        message = CommandExecutionResponse.decode(b"\x12\x02\x08\x01\x12\x02\x08\x02", 4)

        # Assert that the method returns the correct value
        assert message == CommandExecutionResponse(
            execution_info=CommandExecutionInfo(status=CommandExecutionStatus.RUNNING)
        )


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode message
        message = CommandExecutionResponse().encode()

        # Assert that the method returns the correct value
        assert message == b"\x0a\x00\x12\x00"

    @pytest.mark.parametrize(("instance", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, instance: CommandExecutionResponse, buffer: bytes):
        # Encode message
        message = instance.encode()

        # Assert that the method returns the correct value
        assert message == buffer

    @pytest.mark.parametrize(
        ("number", "buffer"),
        [
            pytest.param(1, b"\x0a\x04\x0a\x00\x12\x00", id="default"),
            pytest.param(2, b"\x12\x04\x0a\x00\x12\x00", id="custom"),
        ],
    )
    async def test_should_encode_field_number(self, number: int, buffer: bytes):
        # Encode message
        instance = CommandExecutionResponse()
        message = instance.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer
