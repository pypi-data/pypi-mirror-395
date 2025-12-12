import pytest

from sila.framework.errors.defined_execution_error import DefinedExecutionError
from sila.framework.errors.sila_error import SiLAError
from sila.framework.errors.undefined_execution_error import UndefinedExecutionError

ENCODE_TEST_CASES = [
    pytest.param(
        UndefinedExecutionError("Undefined Execution Error."),
        b"\x1a\x1c\x0a\x1aUndefined Execution Error.",
        id='3: { 1: {"Undefined Execution Error."} }',
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        UndefinedExecutionError("Undefined Execution Error."),
        b"\x1a\x1e\x0a\x1aUndefined Execution Error.\x10\x00",
        id='3: { 1: {"Undefined Execution Error."}, 2: 0 }',
    ),
]


class TestInitialize:
    async def test_should_initialize(self):
        # Create error
        error = UndefinedExecutionError("Undefined Execution Error.")

        # Assert that the method returns the correct value
        assert error.message == "Undefined Execution Error."


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode error
        message = UndefinedExecutionError.decode(b"")

        # Assert that the method returns the correct value
        assert message == UndefinedExecutionError()

    @pytest.mark.parametrize(("error", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, error: UndefinedExecutionError, buffer: bytes):
        # Decode error
        message = SiLAError.decode(buffer)

        # Assert that the method returns the correct value
        assert isinstance(message, UndefinedExecutionError)
        assert message == error

    async def test_should_decode_multiple_fields(self):
        # Decode error
        message = UndefinedExecutionError.decode(b"\x0a\x05Hello\x0a\x05World")

        # Assert that the method returns the correct value
        assert message == UndefinedExecutionError("World")

    async def test_should_decode_limited_buffer(self):
        # Decode error
        message = UndefinedExecutionError.decode(
            b"\x0a\x05Hello\x0a\x05World",
            len(b"\x0a\x05Hello"),
        )

        # Assert that the method returns the correct value
        assert message == UndefinedExecutionError("Hello")


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode error
        message = UndefinedExecutionError().encode()

        # Assert that the method returns the correct value
        assert message == b"\x1a\x00"

    @pytest.mark.parametrize(("error", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, error: UndefinedExecutionError, buffer: bytes):
        # Encode error
        message = error.encode()

        # Assert that the method returns the correct value
        assert message == buffer

    @pytest.mark.parametrize(
        ("error", "number", "buffer"),
        [
            pytest.param(UndefinedExecutionError(), 1, b"\x0a\x02\x1a\x00", id="default"),
            pytest.param(UndefinedExecutionError(), 2, b"\x12\x02\x1a\x00", id="custom"),
        ],
    )
    async def test_should_encode_field_number(self, error: UndefinedExecutionError, number: int, buffer: bytes):
        # Encode error
        message = error.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer


class TestStringify:
    async def test_should_convert_to_string(self):
        # Create error
        error = UndefinedExecutionError("Undefined Execution Error.")

        # Assert that the method returns the correct value
        assert str(error) == "Undefined Execution Error."


class TestEquality:
    def test_should_be_true_on_equal_type(self):
        # Create error
        error_0 = UndefinedExecutionError("Undefined Execution Error.")
        error_1 = UndefinedExecutionError("Undefined Execution Error.")

        # Compare equality
        assert error_0 == error_1

    def test_should_be_false_on_unequal_type(self):
        # Create error
        error_0 = UndefinedExecutionError("Undefined Execution Error.")
        error_1 = DefinedExecutionError("Undefined Execution Error.")

        # Compare equality
        assert error_0 != error_1

    def test_should_be_false_on_unequal_message(self):
        # Create error
        error_0 = UndefinedExecutionError("Undefined Execution Error.")
        error_1 = UndefinedExecutionError("Another Execution Error.")

        # Compare equality
        assert error_0 != error_1

    def test_should_be_false_on_non_sila_error(self):
        # Create error
        error = UndefinedExecutionError("Undefined Execution Error.")

        # Compare equality
        assert error != Exception()
