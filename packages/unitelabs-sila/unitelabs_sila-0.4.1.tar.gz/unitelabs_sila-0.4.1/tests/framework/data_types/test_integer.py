import re
import sys
import textwrap
import unittest.mock

import pytest
import typing_extensions as typing

from sila.framework.data_types.integer import Integer
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError
from sila.framework.fdl.serializer import Serializer

NATIVE_TEST_CASES = [
    pytest.param(Integer(value=1), 1, id="1"),
    pytest.param(Integer(value=-1), -1, id="-1"),
    pytest.param(Integer(value=42), 42, id="42"),
    pytest.param(Integer(value=-(2**63)), -sys.maxsize - 1, id="min"),
    pytest.param(Integer(value=2**63 - 1), sys.maxsize, id="max"),
]
ENCODE_TEST_CASES = [
    pytest.param(Integer(value=1), b"\x08\x01", id="1: 1"),
    pytest.param(Integer(value=-1), b"\x08\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01", id="1: -1"),
    pytest.param(Integer(value=42), b"\x08\x2a", id="1: 42"),
    pytest.param(Integer(value=-sys.maxsize - 1), b"\x08\x80\x80\x80\x80\x80\x80\x80\x80\x80\x01", id="min"),
    pytest.param(Integer(value=sys.maxsize), b"\x08\xff\xff\xff\xff\xff\xff\xff\xff\x7f", id="max"),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(Integer(), b"\x08\x00", id="1: 0"),
    pytest.param(Integer(), b"\x10\x00", id="2: 0"),
    pytest.param(Integer(), b"\x08\x00\x10\x00", id="1: 0, 2: 0"),
    pytest.param(Integer(), b"\x10\x00\x08\x00", id="2: 0, 1: 0"),
    pytest.param(Integer(value=42), b"\x08*", id="1: 42"),
    pytest.param(Integer(value=42), b"\x08*\x10\x00", id="1: 42, 2: 0"),
    pytest.param(Integer(value=42), b"\x10\x00\x08*", id="2: 0, 1: 42"),
]


class TestInitFromNative:
    async def test_should_accept_no_value(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Integer.from_native(context)

        # Assert that the method returns the correct value
        assert data_type == Integer()

    @pytest.mark.parametrize(("expected", "native"), NATIVE_TEST_CASES)
    async def test_should_accept_native(self, expected: Integer, native: int):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Integer.from_native(context, native)

        # Assert that the method returns the correct value
        assert data_type == expected

    async def test_should_raise_on_invalid_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected value of type 'int', received 'str'.")):
            await Integer.from_native(context, typing.cast(int, ""))

    async def test_should_raise_on_invalid_value(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(
            ValueError, match=re.escape("Integer must be between -2⁶³ and 2⁶³-1, received '9223372036854775808'.")
        ):
            await Integer.from_native(context, 2**63)


class TestConvertToNative:
    @pytest.mark.parametrize(("data_type", "native"), NATIVE_TEST_CASES)
    async def test_should_convert_to_native(self, data_type: Integer, native: int):
        # Convert data type
        context = unittest.mock.Mock()
        assert await data_type.to_native(context) == native

    async def test_should_raise_on_invalid_type(self):
        # Create data type
        context = unittest.mock.Mock()

        # Convert data type
        with pytest.raises(TypeError, match=re.escape("Expected value of type 'int', received 'str'.")):
            await Integer(typing.cast(int, "")).to_native(context)


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode data type
        message = Integer.decode(b"")

        # Assert that the method returns the correct value
        assert message == Integer()

    @pytest.mark.parametrize(("data_type", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, data_type: Integer, buffer: bytes):
        # Decode data type
        message = Integer.decode(buffer)

        # Assert that the method returns the correct value
        assert message == data_type

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = Integer.decode(b"\x08\x01\x08\x00")

        # Assert that the method returns the correct value
        assert message == Integer(value=0)

    async def test_should_decode_limited_buffer(self):
        # Decode data type
        message = Integer.decode(b"\x08\x01\x08\x00", 2)

        # Assert that the method returns the correct value
        assert message == Integer(value=1)


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode data type
        message = Integer().encode()

        # Assert that the method returns the correct value
        assert message == b""

    @pytest.mark.parametrize(("data_type", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, data_type: Integer, buffer: bytes):
        # Encode data type
        message = data_type.encode()

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
        # Encode data type
        data_type = Integer()
        message = data_type.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer


class TestSerialize:
    async def test_should_serialize_singleline_xml(self):
        # Serialize
        xml = Serializer.serialize(Integer.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == "<DataType><Basic>Integer</Basic></DataType>"

    async def test_should_deserialize_multiline_xml(self):
        # Serialize
        xml = Serializer.serialize(Integer.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <DataType>
              <Basic>Integer</Basic>
            </DataType>
            """
        )


class TestDeserialize:
    async def test_should_deserialize_singleline_xml(self):
        # Create xml
        xml = "<Basic>Integer</Basic>"

        # Deserialize
        data_type = Deserializer.deserialize(xml, Integer.deserialize)

        # Assert that the method returns the correct value
        assert data_type == Integer

    async def test_should_deserialize_multiline_xml(self):
        # Create xml
        xml = """
        <Basic>
            Integer
        </Basic>
        """

        # Deserialize
        data_type = Deserializer.deserialize(xml, Integer.deserialize)

        # Assert that the method returns the correct value
        assert data_type == Integer

    async def test_should_raise_on_unknown_basic_type(self):
        # Create xml
        xml = "<Basic>Complex</Basic>"

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Expected basic type value, received 'Complex'.")):
            Deserializer.deserialize(xml, Integer.deserialize)


class TestStringify:
    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            (Integer(), "0"),
            (Integer(value=3), "3"),
            (Integer(value=-sys.maxsize - 1), "-9223372036854775808"),
            (Integer(value=sys.maxsize), "9223372036854775807"),
        ],
    )
    def test_should_return_string(self, data_type: Integer, value: str):
        # Convert data type
        assert f"{data_type}" == value


class TestEquality:
    @pytest.mark.parametrize(
        ("value"),
        [
            pytest.param(0, id="0"),
            pytest.param(3, id="3"),
            pytest.param(-sys.maxsize - 1, id="min"),
            pytest.param(sys.maxsize, id="max"),
        ],
    )
    def test_should_compare_equality(self, value: int):
        assert Integer(value) == Integer(value)

    def test_should_compare_inequality(self):
        assert Integer(value=3) != object()


class TestOrder:
    @pytest.mark.parametrize(
        ("data_type_0", "data_type_1", "lt", "le", "gt", "ge"),
        [
            pytest.param(Integer(3), Integer(3), False, True, False, True, id="3|3"),
            pytest.param(Integer(3), Integer(4), True, True, False, False, id="3|4"),
            pytest.param(Integer(4), Integer(3), False, False, True, True, id="4|3"),
        ],
    )
    def test_should_order_integers(
        self, data_type_0: Integer, data_type_1: Integer, lt: bool, le: bool, gt: bool, ge: bool
    ):
        assert (data_type_0 < data_type_1) is lt
        assert (data_type_0 <= data_type_1) is le
        assert (data_type_0 > data_type_1) is gt
        assert (data_type_0 >= data_type_1) is ge

    def test_should_ignore_comparison_to_object(self):
        with pytest.raises(TypeError):
            assert (Integer(3) < object()) is False

        with pytest.raises(TypeError):
            assert (Integer(3) <= object()) is False

        with pytest.raises(TypeError):
            assert (Integer(3) > object()) is False

        with pytest.raises(TypeError):
            assert (Integer(3) >= object()) is False


class TestHash:
    def test_should_hash_constrained(self):
        # Create data type
        data_type_0 = Integer(value=42)
        data_type_1 = Integer(value=42)

        # Hash data type
        assert hash(data_type_0) == hash(data_type_1)
