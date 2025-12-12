import re

import pytest

from sila.framework.protobuf.decode_error import DecodeError
from sila.framework.protobuf.reader import Reader

from .conftest import (
    DOUBLE_TEST_CASES,
    INT32_TEST_CASES,
    INT64_TEST_CASES,
    UINT32_TEST_CASES,
    UINT64_TEST_CASES,
    VARINT_TEST_CASES,
)


class TestInitialize:
    def test_should_initialize(self):
        # Create reader
        reader = Reader(b"abc")

        # Assert that the method returns the correct value
        assert reader.buffer == b"abc"
        assert reader.length == 3
        assert reader.cursor == 0


class TestReadVarint:
    @pytest.mark.parametrize(("value", "buffer"), VARINT_TEST_CASES)
    def test_should_read_varint_from_custom_buffer(self, value: int, buffer: bytes):
        # Create reader
        reader = Reader(buffer)

        # Read varint
        varint = reader.read_varint()

        # Assert that the method returns the correct value
        assert varint == value

    def test_should_raise_on_empty_buffer(self):
        # Create reader
        reader = Reader(b"")

        # Read varint
        with pytest.raises(
            DecodeError, match=re.escape("Buffer does not contain enough bytes to decode a variable-length integer.")
        ):
            reader.read_varint()

    def test_should_raise_on_short_buffer(self):
        # Create reader
        reader = Reader(b"\x80")

        # Read varint
        with pytest.raises(
            DecodeError, match=re.escape("Buffer does not contain enough bytes to decode a variable-length integer.")
        ):
            reader.read_varint()

    def test_should_raise_on_exceeding_64_bits(self):
        # Create reader
        reader = Reader(b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80")

        # Read varint
        with pytest.raises(DecodeError, match=re.escape("Variable-length integer is too large.")):
            reader.read_varint()


class TestReadUInt32:
    @pytest.mark.parametrize(("value", "buffer"), UINT32_TEST_CASES)
    def test_should_read_uint32_from_custom_buffer(self, value: int, buffer: bytes):
        # Create reader
        reader = Reader(buffer)

        # Read uint32
        uint32 = reader.read_uint32()

        # Assert that the method returns the correct value
        assert uint32 == value

    def test_should_read_uint32_consecutively(self):
        # Create reader
        reader = Reader(b"\x84\x72\x12")

        # Read uint32
        uint32 = reader.read_uint32()

        # Assert that the method returns the correct value
        assert reader.cursor == 2
        assert uint32 == 14596

        # Read uint32
        uint32 = reader.read_uint32()

        # Assert that the method returns the correct value
        assert reader.cursor == 3
        assert uint32 == 18

    def test_should_raise_on_out_of_bounds_uint32(self):
        # Create reader
        reader = Reader(b"\x80\x80\x80\x80\x10")

        # Read double
        with pytest.raises(
            DecodeError,
            match=re.escape("Variable-length integer overflows its maximum size of 32 bit."),
        ):
            reader.read_uint32()


class TestReadInt32:
    @pytest.mark.parametrize(("value", "buffer"), INT32_TEST_CASES)
    def test_should_read_int32_from_custom_buffer(self, value: int, buffer: bytes):
        # Create reader
        reader = Reader(buffer)

        # Read int32
        int32 = reader.read_int32()

        # Assert that the method returns the correct value
        assert int32 == value

    def test_should_read_int32_consecutively(self):
        # Create reader
        reader = Reader(b"\xf2\xfd\xff\xff\xff\xff\xff\xff\xff\x01\x84\x72")

        # Read int32
        int32 = reader.read_int32()

        # Assert that the method returns the correct value
        assert reader.cursor == 10
        assert int32 == -270

        # Read int32
        int32 = reader.read_int32()

        # Assert that the method returns the correct value
        assert reader.cursor == 12
        assert int32 == 14596


class TestReadUInt64:
    @pytest.mark.parametrize(("value", "buffer"), UINT64_TEST_CASES)
    def test_should_read_uint64_from_custom_buffer(self, value: int, buffer: bytes):
        # Create reader
        reader = Reader(buffer)

        # Read uint64
        uint64 = reader.read_uint64()

        # Assert that the method returns the correct value
        assert uint64 == value

    def test_should_read_uint64_consecutively(self):
        # Create reader
        reader = Reader(b"\x84\x72\x12")

        # Read uint64
        uint64 = reader.read_uint64()

        # Assert that the method returns the correct value
        assert reader.cursor == 2
        assert uint64 == 14596

        # Read uint64
        uint64 = reader.read_uint64()

        # Assert that the method returns the correct value
        assert reader.cursor == 3
        assert uint64 == 18


class TestReadInt64:
    @pytest.mark.parametrize(("value", "buffer"), INT64_TEST_CASES)
    def test_should_read_int64_from_custom_buffer(self, value: int, buffer: bytes):
        # Create reader
        reader = Reader(buffer)

        # Read int64
        int64 = reader.read_int64()

        # Assert that the method returns the correct value
        assert int64 == value

    def test_should_read_int64_consecutively(self):
        # Create reader
        reader = Reader(b"\xf2\xfd\xff\xff\xff\xff\xff\xff\xff\x01\x84\x72")

        # Read int64
        int64 = reader.read_int64()

        # Assert that the method returns the correct value
        assert reader.cursor == 10
        assert int64 == -270

        # Read int64
        int64 = reader.read_int64()

        # Assert that the method returns the correct value
        assert reader.cursor == 12
        assert int64 == 14596


class TestReadDouble:
    @pytest.mark.parametrize(("value", "buffer"), DOUBLE_TEST_CASES)
    def test_should_read_double_from_custom_buffer(self, value: float, buffer: bytes):
        # Create reader
        reader = Reader(buffer)

        # Read double
        double = reader.read_double()

        # Assert that the method returns the correct value
        assert double == value

    def test_should_raise_on_out_of_bounds_double(self):
        # Create reader
        reader = Reader(b"\x80")

        # Read double
        with pytest.raises(
            DecodeError,
            match=re.escape("Buffer does not contain enough bytes to read a double-precision floating-point number."),
        ):
            reader.read_double()


class TestReadBool:
    @pytest.mark.parametrize(
        ("value", "buffer"),
        [
            pytest.param(False, b"\x00", id="false"),
            pytest.param(True, b"\x01", id="true"),
        ],
    )
    def test_should_read_bool_from_custom_buffer(self, value: bool, buffer: bytes):
        # Create reader
        reader = Reader(buffer)

        # Read bool
        bool_ = reader.read_bool()

        # Assert that the method returns the correct value
        assert bool_ == value


class TestReadBytes:
    @pytest.mark.parametrize(
        ("value", "buffer"),
        [
            pytest.param(b"", b"\x00", id=""),
            pytest.param(b"ABC", b"\x03\x41\x42\x43", id="ABC"),
        ],
    )
    def test_should_read_bytes_from_custom_buffer(self, value: bytes, buffer: bytes):
        # Create reader
        reader = Reader(buffer)

        # Read bytes
        bytes_ = reader.read_bytes()

        # Assert that the method returns the correct value
        assert bytes_ == value

    def test_should_raise_on_out_of_bounds_bytes(self):
        # Create reader
        reader = Reader(b"\x05\x41\x42")

        # Read bytes
        with pytest.raises(
            DecodeError,
            match=re.escape(
                "Attempted to read 5 bytes at position 1, but the buffer only has "
                "2 remaining bytes. Cannot read past the end of the buffer."
            ),
        ):
            reader.read_bytes()


class TestReadString:
    @pytest.mark.parametrize(
        ("value", "buffer"),
        [
            pytest.param("", b"\x00", id=""),
            pytest.param("Hello", b"\x05\x48\x65\x6c\x6c\x6f", id="Hello"),
        ],
    )
    def test_should_read_string_from_custom_buffer(self, value: str, buffer: bytes):
        # Create reader
        reader = Reader(buffer)

        # Read string
        string = reader.read_string()

        # Assert that the method returns the correct value
        assert string == value


class TestSkip:
    def test_should_skip_bytes(self):
        # Create reader
        reader = Reader(b"\xac\x02")

        # Skip bytes
        reader.skip()

        # Assert that the object is in the correct state
        assert reader.cursor == 2

    def test_should_skip_bytes_with_custom_length(self):
        # Create reader
        reader = Reader(b"\x41\x42\x43\x44")

        # Skip bytes
        reader.skip(2)

        # Assert that the object is in the correct state
        assert reader.cursor == 2

        # Skip bytes
        reader.skip(2)

        # Assert that the object is in the correct state
        assert reader.cursor == 4

    def test_should_raise_on_skipping_bytes_out_of_bounds(self):
        # Create reader
        reader = Reader(b"\x41\x42")

        # Read bytes
        with pytest.raises(
            DecodeError,
            match=re.escape(
                "Attempted to skip 5 bytes from position 0, but the buffer only has "
                "2 remaining bytes. Cannot read past the end of the buffer."
            ),
        ):
            reader.skip(5)


class TestSkipType:
    def test_should_skip_type_varint(self):
        # Create reader
        reader = Reader(b"\xac\x02\x41")

        # Skip type
        reader.skip_type(0)

        # Assert that the object is in the correct state
        assert reader.cursor == 2
        assert reader.buffer[reader.cursor] == 0x41

    def test_should_skip_type_64bit(self):
        # Create reader
        reader = Reader(b"\x00\x00\x00\x00\x00\x00\x00\x00\x41")

        # Skip type
        reader.skip_type(1)

        # Assert that the object is in the correct state
        assert reader.cursor == 8
        assert reader.buffer[reader.cursor] == 0x41

    def test_should_skip_type_length_delimited(self):
        # Create reader
        reader = Reader(b"\x03\x41\x42\x43\x50")

        # Skip type
        reader.skip_type(2)

        # Assert that the object is in the correct state
        assert reader.cursor == 4
        assert reader.buffer[reader.cursor] == 0x50

    def test_should_skip_type_32bit(self):
        # Create reader
        reader = Reader(b"\x00\x00\x00\x00\x41")

        # Skip type
        reader.skip_type(5)

        # Assert that the object is in the correct state
        assert reader.cursor == 4
        assert reader.buffer[reader.cursor] == 0x41

    def test_should_raise_on_skipping_invalid_wire_type(self):
        # Create reader
        reader = Reader(b"\x00\x01")

        # Read bytes
        with pytest.raises(DecodeError, match=re.escape("Invalid wire type '6' at offset '0'.")):
            reader.skip_type(6)
