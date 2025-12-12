import re

import pytest

from sila.framework.command.command_confirmation import CommandConfirmation
from sila.framework.command.command_execution_uuid import CommandExecutionUUID
from sila.framework.data_types.duration import Duration
from sila.framework.protobuf.decode_error import DecodeError

ENCODE_TEST_CASES = [
    pytest.param(
        CommandConfirmation(command_execution_uuid=CommandExecutionUUID(value="00000000-0000-0000-0000-000000000000")),
        b"\x0a\x26\x0a\x2400000000-0000-0000-0000-000000000000",
        id='1: { 1: {"00000000-0000-0000-0000-000000000000"} }',
    ),
    pytest.param(
        CommandConfirmation(lifetime_of_execution=Duration(seconds=12, nanos=34000)),
        b"\x0a\x00\x12\x06\x08\x0c\x10\xd0\x89\x02",
        id="2: { 1: 12, 2: 34000 }",
    ),
    pytest.param(
        CommandConfirmation(
            command_execution_uuid=CommandExecutionUUID(value="00000000-0000-0000-0000-000000000000"),
            lifetime_of_execution=Duration(seconds=12, nanos=34000),
        ),
        b"\x0a\x26\x0a\x2400000000-0000-0000-0000-000000000000\x12\x06\x08\x0c\x10\xd0\x89\x02",
        id='1: { 1: {"00000000-0000-0000-0000-000000000000"} }, 2: { 1: 12, 2: 34000 }',
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        CommandConfirmation(
            command_execution_uuid=CommandExecutionUUID(value="00000000-0000-0000-0000-000000000000"),
            lifetime_of_execution=Duration(seconds=12, nanos=34000),
        ),
        b"\x18\x00\x12\x06\x08\x0c\x10\xd0\x89\x02\x0a\x26\x0a\x2400000000-0000-0000-0000-000000000000",
        id='3: 0, 2: { 1: 12, 2: 34000 }, 1: { 1: {"00000000-0000-0000-0000-000000000000"} }',
    ),
]


class TestDecode:
    async def test_should_raise_on_empty_buffer(self):
        # Decode message
        with pytest.raises(
            DecodeError, match=re.escape("Missing field 'commandExecutionUUID' in message 'CommandConfirmation'.")
        ):
            CommandConfirmation.decode(b"")

    @pytest.mark.parametrize(("instance", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, instance: CommandConfirmation, buffer: bytes):
        # Decode message
        message = CommandConfirmation.decode(buffer)

        # Assert that the method returns the correct value
        assert message == instance

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = CommandConfirmation.decode(b"\x0a\x07\x0a\x05Hello\x0a\x07\x0a\x05World")

        # Assert that the method returns the correct value
        assert message == CommandConfirmation(command_execution_uuid=CommandExecutionUUID("World"))

    async def test_should_decode_limited_buffer(self):
        # Decode message
        message = CommandConfirmation.decode(b"\x0a\x07\x0a\x05Hello\x0a\x07\x0a\x05World", 9)

        # Assert that the method returns the correct value
        assert message == CommandConfirmation(command_execution_uuid=CommandExecutionUUID("Hello"))


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode message
        message = CommandConfirmation().encode()

        # Assert that the method returns the correct value
        assert message == b"\x0a\x00"

    @pytest.mark.parametrize(("instance", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, instance: CommandConfirmation, buffer: bytes):
        # Encode message
        message = instance.encode()

        # Assert that the method returns the correct value
        assert message == buffer

    @pytest.mark.parametrize(
        ("number", "buffer"),
        [
            pytest.param(1, b"\x0a\x02\x0a\x00", id="default"),
            pytest.param(2, b"\x12\x02\x0a\x00", id="custom"),
        ],
    )
    async def test_should_encode_field_number(self, number: int, buffer: bytes):
        # Encode message
        instance = CommandConfirmation()
        message = instance.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer
