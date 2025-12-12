import math

import pytest

from sila.framework.command.command_execution_info import CommandExecutionInfo, CommandExecutionStatus
from sila.framework.data_types.duration import Duration
from sila.framework.data_types.real import Real

ENCODE_TEST_CASES = [
    pytest.param(
        CommandExecutionInfo(status=CommandExecutionStatus.RUNNING),
        b"\x08\x01",
        id="1: 1",
    ),
    pytest.param(
        CommandExecutionInfo(progress=Real(math.pi)),
        b"\x12\x09\x09\x18\x2d\x44\x54\xfb\x21\x09\x40",
        id="2: { 1: 3.141592653589793 }",
    ),
    pytest.param(
        CommandExecutionInfo(remaining_time=Duration(seconds=12, nanos=34000)),
        b"\x1a\x06\x08\x0c\x10\xd0\x89\x02",
        id="3: { 1: 12, 2: 34000 }",
    ),
    pytest.param(
        CommandExecutionInfo(updated_lifetime=Duration(seconds=12, nanos=34000)),
        b"\x22\x06\x08\x0c\x10\xd0\x89\x02",
        id="4: { 1: 12, 2: 34000 }",
    ),
    pytest.param(
        CommandExecutionInfo(
            status=CommandExecutionStatus.RUNNING,
            progress=Real(math.pi),
            remaining_time=Duration(seconds=12, nanos=34000),
            updated_lifetime=Duration(seconds=12, nanos=34000),
        ),
        b"\x08\x01\x12\x09\x09\x18\x2d\x44\x54\xfb\x21\x09\x40\x1a\x06\x08\x0c\x10\xd0\x89\x02\x22\x06\x08\x0c\x10\xd0\x89\x02",
        id="1: 1, 2: { 1: 3.141592653589793 }, 3: { 1: 12, 2: 34000 }, 4: { 1: 12, 2: 34000 }",
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        CommandExecutionInfo(
            status=CommandExecutionStatus.RUNNING,
            progress=Real(math.pi),
            remaining_time=Duration(seconds=12, nanos=34000),
            updated_lifetime=Duration(seconds=12, nanos=34000),
        ),
        b"\x28\x00\x08\x01\x12\x09\x09\x18\x2d\x44\x54\xfb\x21\x09\x40\x1a\x06\x08\x0c\x10\xd0\x89\x02\x22\x06\x08\x0c\x10\xd0\x89\x02",
        id="5: 0, 4: { 1: 12, 2: 34000 }, 3: { 1: 12, 2: 34000 }, 2: { 1: 3.141592653589793 }, 1: 1",
    ),
]


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode message
        message = CommandExecutionInfo.decode(b"")

        # Assert that the method returns the correct value
        assert message == CommandExecutionInfo()

    @pytest.mark.parametrize(("instance", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, instance: CommandExecutionInfo, buffer: bytes):
        # Decode message
        message = CommandExecutionInfo.decode(buffer)

        # Assert that the method returns the correct value
        assert message == instance

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = CommandExecutionInfo.decode(b"\x08\x01\x08\x00")

        # Assert that the method returns the correct value
        assert message == CommandExecutionInfo(status=CommandExecutionStatus.WAITING)

    async def test_should_decode_limited_buffer(self):
        # Decode message
        message = CommandExecutionInfo.decode(b"\x08\x01\x08\x00", 2)

        # Assert that the method returns the correct value
        assert message == CommandExecutionInfo(status=CommandExecutionStatus.RUNNING)


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode message
        message = CommandExecutionInfo().encode()

        # Assert that the method returns the correct value
        assert message == b""

    @pytest.mark.parametrize(("instance", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, instance: CommandExecutionInfo, buffer: bytes):
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
        instance = CommandExecutionInfo()
        message = instance.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer
