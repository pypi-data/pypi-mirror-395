import re

import pytest

from sila.framework.protobuf.encode_error import EncodeError
from sila.framework.protobuf.writer import Writer

from .conftest import (
    DOUBLE_TEST_CASES,
    INT32_TEST_CASES,
    INT64_TEST_CASES,
    UINT32_TEST_CASES,
    UINT64_TEST_CASES,
    VARINT_TEST_CASES,
)


class TestInitialize:
    async def test_should_initialize(self):
        # Create writer
        writer = Writer()

        # Assert that the method returns the correct value
        assert writer.buffer.getbuffer() == b""
        assert writer.length == 0


class TestWriteVarint:
    @pytest.mark.parametrize(("value", "buffer"), VARINT_TEST_CASES)
    def test_should_write_varint_with_custom_value(self, value: int, buffer: bytes):
        # Create writer
        writer = Writer()

        # Write varint
        writer.write_varint(value)

        # Assert that the object is in the correct state
        assert writer.length == len(buffer)
        assert writer.finish() == buffer

    def test_should_raise_on_negative_varint(self):
        # Create writer
        writer = Writer()

        # Write varint
        with pytest.raises(EncodeError, match=re.escape("Varint encoding does not support negative values.")):
            writer.write_varint(-1)


class TestWriteUInt32:
    @pytest.mark.parametrize(("value", "buffer"), UINT32_TEST_CASES)
    def test_should_write_uint32_with_custom_value(self, value: int, buffer: bytes):
        # Create writer
        writer = Writer()

        # Write uint32
        writer = writer.write_uint32(value)

        # Assert that the method returns the correct value
        assert writer.finish() == buffer

    def test_should_write_uint32_consecutively(self):
        # Create writer
        writer = Writer()

        # Write uint32
        writer.write_uint32(14596)

        # Assert that the object is in the correct state
        assert writer.length == 2

        # Write uint32
        writer.write_uint32(18)

        # Assert that the object is in the correct state
        assert writer.length == 3

        # Assert that the method returns the correct value
        assert writer.finish() == b"\x84\x72\x12"

    @pytest.mark.parametrize(("value"), [-1, 2**32])
    def test_should_raise_on_uint32_out_of_bounds(self, value: int):
        # Create writer
        writer = Writer()

        # Write uint32
        with pytest.raises(
            EncodeError, match=re.escape("Value must be a 32-bit unsigned integer (0 <= value < 2^32).")
        ):
            writer.write_uint32(value)


class TestWriteInt32:
    @pytest.mark.parametrize(("value", "buffer"), INT32_TEST_CASES)
    def test_should_write_int32_with_custom_value(self, value: int, buffer: bytes):
        # Create writer
        writer = Writer()

        # Write int32
        writer = writer.write_int32(value)

        # Assert that the method returns the correct value
        assert writer.finish() == buffer

    def test_should_write_int32_consecutively(self):
        # Create writer
        writer = Writer()

        # Write int32
        writer.write_int32(-270)

        # Assert that the object is in the correct state
        assert writer.length == 10

        # Write int32
        writer.write_int32(14596)

        # Assert that the object is in the correct state
        assert writer.length == 12

        # Assert that the method returns the correct value
        assert writer.finish() == b"\xf2\xfd\xff\xff\xff\xff\xff\xff\xff\x01\x84\x72"

    @pytest.mark.parametrize(("value"), [-(2**31) - 1, 2**31])
    def test_should_raise_on_int32_out_of_bounds(self, value: int):
        # Create writer
        writer = Writer()

        # Write int32
        with pytest.raises(
            EncodeError, match=re.escape("Value must be a 32-bit signed integer (-2^31 <= value < 2^31).")
        ):
            writer.write_int32(value)


class TestWriteUInt64:
    @pytest.mark.parametrize(("value", "buffer"), UINT64_TEST_CASES)
    def test_should_write_uint64_with_custom_value(self, value: int, buffer: bytes):
        # Create writer
        writer = Writer()

        # Write uint64
        writer = writer.write_uint64(value)

        # Assert that the method returns the correct value
        assert writer.finish() == buffer

    def test_should_write_uint64_consecutively(self):
        # Create writer
        writer = Writer()

        # Write uint64
        writer.write_uint64(14596)

        # Assert that the object is in the correct state
        assert writer.length == 2

        # Write uint64
        writer.write_uint64(18)

        # Assert that the object is in the correct state
        assert writer.length == 3

        # Assert that the method returns the correct value
        assert writer.finish() == b"\x84\x72\x12"

    @pytest.mark.parametrize(("value"), [-1, 2**64])
    def test_should_raise_on_uint64_out_of_bounds(self, value: int):
        # Create writer
        writer = Writer()

        # Write uint64
        with pytest.raises(
            EncodeError, match=re.escape("Value must be a 64-bit unsigned integer (0 <= value < 2^64).")
        ):
            writer.write_uint64(value)


class TestWriteInt64:
    @pytest.mark.parametrize(("value", "buffer"), INT64_TEST_CASES)
    def test_should_write_int64_with_custom_value(self, value: int, buffer: bytes):
        # Create writer
        writer = Writer()

        # Write int64
        writer = writer.write_int64(value)

        # Assert that the method returns the correct value
        assert writer.finish() == buffer

    def test_should_write_int64_consecutively(self):
        # Create writer
        writer = Writer()

        # Write int64
        writer.write_int64(-270)

        # Assert that the object is in the correct state
        assert writer.length == 10

        # Write int64
        writer.write_int64(14596)

        # Assert that the object is in the correct state
        assert writer.length == 12

        # Assert that the method returns the correct value
        assert writer.finish() == b"\xf2\xfd\xff\xff\xff\xff\xff\xff\xff\x01\x84\x72"

    @pytest.mark.parametrize(("value"), [-(2**63) - 1, 2**63])
    def test_should_raise_on_int64_out_of_bounds(self, value: int):
        # Create writer
        writer = Writer()

        # Write int64
        with pytest.raises(
            EncodeError, match=re.escape("Value must be a 64-bit signed integer (-2^63 <= value < 2^63).")
        ):
            writer.write_int64(value)


class TestWriteDouble:
    @pytest.mark.parametrize(("value", "buffer"), DOUBLE_TEST_CASES)
    def test_should_write_double_with_custom_value(self, value: float, buffer: bytes):
        # Create writer
        writer = Writer()

        # Write double
        writer = writer.write_double(value)

        # Assert that the method returns the correct value
        assert writer.finish() == buffer

    @pytest.mark.parametrize(("value"), ["nan"])
    def test_should_raise_on_double_out_of_bounds(self, value: float):
        # Create writer
        writer = Writer()

        # Write double
        with pytest.raises(
            EncodeError, match=re.escape("Value must be a 64-bit double-precision floating-point number.")
        ):
            writer.write_double(value)


class TestWriteBool:
    @pytest.mark.parametrize(
        ("value", "buffer"),
        [
            pytest.param(False, b"\x00", id="false"),
            pytest.param(True, b"\x01", id="true"),
        ],
    )
    def test_should_write_bool_with_custom_value(self, value: bool, buffer: bytes):
        # Create writer
        writer = Writer()

        # Write bool
        writer = writer.write_bool(value)

        # Assert that the method returns the correct value
        assert writer.finish() == buffer


class TestWriteBytes:
    @pytest.mark.parametrize(
        ("value", "buffer"),
        [
            pytest.param(b"", b"\x00", id=""),
            pytest.param(b"ABC", b"\x03\x41\x42\x43", id="ABC"),
        ],
    )
    def test_should_write_bytes_with_custom_value(self, value: bytes, buffer: bytes):
        # Create writer
        writer = Writer()

        # Write bytes
        writer = writer.write_bytes(value)

        # Assert that the method returns the correct value
        assert writer.finish() == buffer


class TestWriteString:
    @pytest.mark.parametrize(
        ("value", "buffer"),
        [
            pytest.param("", b"\x00", id=""),
            pytest.param("Hello", b"\x05\x48\x65\x6c\x6c\x6f", id="Hello"),
        ],
    )
    def test_should_write_string_with_custom_value(self, value: str, buffer: bytes):
        # Create writer
        writer = Writer()

        # Write string
        writer = writer.write_string(value)

        # Assert that the method returns the correct value
        assert writer.finish() == buffer


class TestLdelim:
    @pytest.mark.parametrize(
        ("value", "buffer"),
        [
            pytest.param(b"", b"\x00", id=""),
            pytest.param(b"Hello", b"\x05\x48\x65\x6c\x6c\x6f", id="Hello"),
        ],
    )
    def test_should_write_length_delimiter(self, value: bytes, buffer: bytes):
        # Create writer
        writer = Writer()
        writer.fork()
        writer.write(value)

        # Write length delimiter
        writer.ldelim()

        # Assert that the object is in the correct state
        assert writer.length == len(buffer)
        assert writer.finish() == buffer

    @pytest.mark.parametrize(
        ("value", "buffer"),
        [
            pytest.param(b"", b"\x00", id=""),
            pytest.param(b"Hello", b"\x05Hello", id="Hello"),
        ],
    )
    def test_should_write_ldelim_with_custom_offset(self, value: bytes, buffer: bytes):
        # Create writer
        writer = Writer()
        writer.write(b"\x41\x42\x43")
        writer.fork()

        # Write length delimiter
        writer.write(value)
        writer.ldelim()

        # Assert that the object is in the correct state
        assert writer.length == len(buffer) + 3
        assert writer.finish() == b"\x41\x42\x43" + buffer

    def test_should_write_ldelim_consecutively(self):
        # Create writer
        writer = Writer()
        writer.write(b"\x41\x42\x43")

        # Write length delimiter
        writer.fork()
        writer.write(b"Hello")
        writer.ldelim()

        writer.write(b", ")

        # Write length delimiter
        writer.fork()
        writer.write(b"World")
        writer.ldelim()

        writer.write(b"!")

        # Assert that the object is in the correct state
        assert writer.length == 18
        assert writer.finish() == b"\x41\x42\x43\x05Hello, \x05World!"

    def test_should_write_ldelim_nested(self):
        # Create writer
        writer = Writer()
        writer.write(b"\x41\x42\x43")

        # Write length delimiter
        writer.fork()
        writer.write(b"Hello")

        writer.write(b", ")

        # Write length delimiter
        writer.fork()
        writer.write(b"World")
        writer.ldelim()

        writer.ldelim()
        writer.write(b"!")

        # Assert that the object is in the correct state
        assert writer.length == 18
        assert writer.finish() == b"\x41\x42\x43\x0dHello, \x05World!"
