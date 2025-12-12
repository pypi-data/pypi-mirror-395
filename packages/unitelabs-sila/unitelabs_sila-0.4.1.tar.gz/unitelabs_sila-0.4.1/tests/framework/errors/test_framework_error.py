import pytest

from sila.framework.errors.defined_execution_error import DefinedExecutionError
from sila.framework.errors.framework_error import (
    CommandExecutionNotAccepted,
    CommandExecutionNotFinished,
    FrameworkError,
    InvalidCommandExecutionUUID,
    InvalidMetadata,
    NoMetadataAllowed,
)
from sila.framework.errors.sila_error import SiLAError

ENCODE_TEST_CASES = [
    pytest.param(
        CommandExecutionNotAccepted("Command Execution Not Accepted."),
        b"\x22\x21\x12\x1fCommand Execution Not Accepted.",
        id='4: { 1: 0, 2: {"Command Execution Not Accepted."} }',
    ),
    pytest.param(
        InvalidCommandExecutionUUID("Invalid Command Execution UUID."),
        b"\x22\x23\x08\x01\x12\x1fInvalid Command Execution UUID.",
        id='4: { 1: 1, 2: {"Invalid Command Execution UUID."} }',
    ),
    pytest.param(
        CommandExecutionNotFinished("Command Execution Not Finished."),
        b"\x22\x23\x08\x02\x12\x1fCommand Execution Not Finished.",
        id='4: { 1: 2, 2: {"Command Execution Not Finished."} }',
    ),
    pytest.param(
        InvalidMetadata("Invalid Metadata."),
        b"\x22\x15\x08\x03\x12\x11Invalid Metadata.",
        id='4: { 1: 3, 2: {"Invalid Metadata."} }',
    ),
    pytest.param(
        NoMetadataAllowed("No Metadata Allowed."),
        b"\x22\x18\x08\x04\x12\x14No Metadata Allowed.",
        id='4: { 1: 4, 2: {"No Metadata Allowed."} }',
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        FrameworkError("Framework Error.", FrameworkError.Type.COMMAND_EXECUTION_NOT_ACCEPTED),
        b"\x22\x16\x18\x00\x12\x10Framework Error.\x08\x00",
        id='4: { 3: 0, 2: {"Framework Error."}, 1: 0 }',
    ),
]


class TestInitialize:
    async def test_should_initialize(self):
        # Create error
        error = FrameworkError("Framework Error.", FrameworkError.Type.COMMAND_EXECUTION_NOT_ACCEPTED)

        # Assert that the method returns the correct value
        assert error.message == "Framework Error."
        assert error.error_type == FrameworkError.Type.COMMAND_EXECUTION_NOT_ACCEPTED


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode error
        message = FrameworkError.decode(b"")

        # Assert that the method returns the correct value
        assert message == CommandExecutionNotAccepted("")

    @pytest.mark.parametrize(("error", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, error: FrameworkError, buffer: bytes):
        # Decode error
        message = SiLAError.decode(buffer)

        # Assert that the method returns the correct value
        assert isinstance(message, FrameworkError)
        assert message == error

    async def test_should_decode_multiple_fields(self):
        # Decode error
        message = FrameworkError.decode(b"\x12\x05Hello\x12\x05World")

        # Assert that the method returns the correct value
        assert message == CommandExecutionNotAccepted("World")

    async def test_should_decode_limited_buffer(self):
        # Decode error
        message = FrameworkError.decode(
            b"\x12\x05Hello\x12\x05World",
            len(b"\x12\x05Hello"),
        )

        # Assert that the method returns the correct value
        assert message == CommandExecutionNotAccepted("Hello")


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode error
        message = CommandExecutionNotAccepted("").encode()

        # Assert that the method returns the correct value
        assert message == b"\x22\x00"

    @pytest.mark.parametrize(("error", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, error: FrameworkError, buffer: bytes):
        # Encode error
        message = error.encode()

        # Assert that the method returns the correct value
        assert message == buffer

    @pytest.mark.parametrize(
        ("number", "buffer"),
        [
            pytest.param(1, b"\x0a\x02\x22\x00", id="default"),
            pytest.param(2, b"\x12\x02\x22\x00", id="custom"),
        ],
    )
    async def test_should_encode_field_number(self, number: int, buffer: bytes):
        # Encode error
        error = CommandExecutionNotAccepted("")
        message = error.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer


class TestStringify:
    async def test_should_convert_to_string(self):
        # Create error
        error = FrameworkError("Framework Error.", FrameworkError.Type.COMMAND_EXECUTION_NOT_ACCEPTED)

        # Assert that the method returns the correct value
        assert str(error) == "Framework Error."


class TestEquality:
    def test_should_be_true_on_equal_type(self):
        # Create error
        error_0 = FrameworkError("Framework Error.", FrameworkError.Type.COMMAND_EXECUTION_NOT_ACCEPTED)
        error_1 = FrameworkError("Framework Error.", FrameworkError.Type.COMMAND_EXECUTION_NOT_ACCEPTED)

        # Compare equality
        assert error_0 == error_1

    def test_should_be_true_on_equal_subclass(self):
        # Create error
        error_0 = FrameworkError("Framework Error.", FrameworkError.Type.COMMAND_EXECUTION_NOT_ACCEPTED)
        error_1 = CommandExecutionNotAccepted("Framework Error.")

        # Compare equality
        assert error_0 == error_1

    def test_should_be_false_on_unequal_type(self):
        # Create error
        error_0 = FrameworkError("Framework Error.", FrameworkError.Type.COMMAND_EXECUTION_NOT_ACCEPTED)
        error_1 = DefinedExecutionError("Undefined Execution Error.")

        # Compare equality
        assert error_0 != error_1

    def test_should_be_false_on_unequal_message(self):
        # Create error
        error_0 = FrameworkError("Framework Error.", FrameworkError.Type.COMMAND_EXECUTION_NOT_ACCEPTED)
        error_1 = FrameworkError("Other Error.", FrameworkError.Type.COMMAND_EXECUTION_NOT_ACCEPTED)

        # Compare equality
        assert error_0 != error_1

    def test_should_be_false_on_unequal_error_type(self):
        # Create error
        error_0 = FrameworkError("Framework Error.", FrameworkError.Type.COMMAND_EXECUTION_NOT_ACCEPTED)
        error_1 = FrameworkError("Framework Error.", FrameworkError.Type.INVALID_COMMAND_EXECUTION_UUID)

        # Compare equality
        assert error_0 != error_1

    def test_should_be_false_on_non_sila_error(self):
        # Create error
        error = FrameworkError("Framework Error.", FrameworkError.Type.COMMAND_EXECUTION_NOT_ACCEPTED)

        # Compare equality
        assert error != Exception()
