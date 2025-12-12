import pytest

from sila.framework.cloud.command_confirmation_response import CommandConfirmationResponse
from sila.framework.command.command_confirmation import CommandConfirmation
from sila.framework.command.command_execution_uuid import CommandExecutionUUID

ENCODE_TEST_CASES = [
    pytest.param(
        CommandConfirmationResponse(
            command_confirmation=CommandConfirmation(
                command_execution_uuid=CommandExecutionUUID(value="00000000-0000-0000-0000-000000000000"),
            )
        ),
        b"\x0a\x28\x0a\x26\x0a\x2400000000-0000-0000-0000-000000000000",
        id='1: { 1: { 1: {"00000000-0000-0000-0000-000000000000"} } }',
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        CommandConfirmationResponse(
            command_confirmation=CommandConfirmation(
                command_execution_uuid=CommandExecutionUUID(value="00000000-0000-0000-0000-000000000000"),
            )
        ),
        b"\x10\x00\x0a\x28\x0a\x26\x0a\x2400000000-0000-0000-0000-000000000000",
        id='2: 0, 1: { 1: { 1: {"00000000-0000-0000-0000-000000000000"} } }',
    ),
]


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode message
        message = CommandConfirmationResponse.decode(b"")

        # Assert that the method returns the correct value
        assert message == CommandConfirmationResponse()

    @pytest.mark.parametrize(("instance", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, instance: CommandConfirmationResponse, buffer: bytes):
        # Decode message
        message = CommandConfirmationResponse.decode(buffer)

        # Assert that the method returns the correct value
        assert message == instance

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = CommandConfirmationResponse.decode(b"\x0a\x09\x0a\x07\x0a\x05Hello\x0a\x09\x0a\x07\x0a\x05World")

        # Assert that the method returns the correct value
        assert message == CommandConfirmationResponse(CommandConfirmation(CommandExecutionUUID("World")))

    async def test_should_decode_limited_buffer(self):
        # Decode message
        message = CommandConfirmationResponse.decode(b"\x0a\x09\x0a\x07\x0a\x05Hello\x0a\x09\x0a\x07\x0a\x05World", 11)

        # Assert that the method returns the correct value
        assert message == CommandConfirmationResponse(CommandConfirmation(CommandExecutionUUID("Hello")))


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode message
        message = CommandConfirmationResponse().encode()

        # Assert that the method returns the correct value
        assert message == b"\x0a\x02\x0a\x00"

    @pytest.mark.parametrize(("instance", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, instance: CommandConfirmationResponse, buffer: bytes):
        # Encode message
        message = instance.encode()

        # Assert that the method returns the correct value
        assert message == buffer

    @pytest.mark.parametrize(
        ("number", "buffer"),
        [
            pytest.param(1, b"\x0a\x04\x0a\x02\x0a\x00", id="default"),
            pytest.param(2, b"\x12\x04\x0a\x02\x0a\x00", id="custom"),
        ],
    )
    async def test_should_encode_field_number(self, number: int, buffer: bytes):
        # Encode message
        instance = CommandConfirmationResponse()
        message = instance.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer
