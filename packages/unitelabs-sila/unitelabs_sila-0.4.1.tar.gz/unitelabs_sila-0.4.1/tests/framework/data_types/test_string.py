import re
import textwrap
import unittest.mock

import pytest
import typing_extensions as typing

from sila.framework.data_types.string import String
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError
from sila.framework.fdl.serializer import Serializer

NATIVE_TEST_CASES = [
    pytest.param(String(value="Hello, World!"), "Hello, World!", id="Hello, World!"),
    pytest.param(String(value=" " * 2**21), " " * 2**21, id="max"),
]
ENCODE_TEST_CASES = [
    pytest.param(String(value="Hello, World!"), b"\x0a\x0dHello, World!", id='1: {"Hello, World!"}'),
    pytest.param(String(value=" " * 2**21), b"\x0a\x80\x80\x80\x01" + b"\x20" * 2**21, id="max"),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(String(), b"\x0a\x00", id="1: {}"),
    pytest.param(String(), b"\x10\x00", id="2: 0"),
    pytest.param(String(), b"\x0a\x00\x10\x00", id="1: {}, 2: 0"),
    pytest.param(String(), b"\x10\x00\x0a\x00", id="2: 0, 1: {}"),
    pytest.param(String(value="Hello, World!"), b"\x0a\rHello, World!", id='1: {"Hello, World!"}'),
    pytest.param(String(value="Hello, World!"), b"\x0a\rHello, World!\x10\x00", id='1: {"Hello, World!"}, 2: 0'),
    pytest.param(String(value="Hello, World!"), b"\x10\x00\x0a\rHello, World!", id='2: 0, 1: {"Hello, World!"}'),
]


class TestInitFromNative:
    async def test_should_accept_no_value(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await String.from_native(context)

        # Assert that the method returns the correct value
        assert data_type == String()

    @pytest.mark.parametrize(("expected", "native"), NATIVE_TEST_CASES)
    async def test_should_accept_native(self, expected: String, native: str):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await String.from_native(context, native)

        # Assert that the method returns the correct value
        assert data_type == expected

    async def test_should_raise_on_invalid_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected value of type 'str', received 'int'.")):
            await String.from_native(context, typing.cast(str, 0))

    async def test_should_raise_on_invalid_value(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("String must not exceed 2²¹ characters, received '2097153'.")):
            await String.from_native(context, " " * (2**21 + 1))


class TestConvertToNative:
    @pytest.mark.parametrize(("data_type", "native"), NATIVE_TEST_CASES)
    async def test_should_convert_string(self, data_type: String, native: str):
        # Convert data type
        context = unittest.mock.Mock()
        assert await data_type.to_native(context) == native

    async def test_should_raise_on_invalid_type(self):
        # Create data type
        context = unittest.mock.Mock()

        # Convert data type
        with pytest.raises(TypeError, match=re.escape("Expected value of type 'str', received 'int'.")):
            await String(typing.cast(str, 0)).to_native(context)

    async def test_should_raise_on_invalid_value(self):
        # Create data type
        context = unittest.mock.Mock()

        # Convert data type
        with pytest.raises(ValueError, match=re.escape("String must not exceed 2²¹ characters, received '2097153'.")):
            await String(" " * (2**21 + 1)).to_native(context)


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode data type
        message = String.decode(b"")

        # Assert that the method returns the correct value
        assert message == String()

    @pytest.mark.parametrize(("data_type", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, data_type: String, buffer: bytes):
        # Decode data type
        message = String.decode(buffer)

        # Assert that the method returns the correct value
        assert message == data_type

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = String.decode(b"\x0a\x05Hello\x0a\x05World")

        # Assert that the method returns the correct value
        assert message == String(value="World")

    async def test_should_decode_limited_buffer(self):
        # Decode data type
        message = String.decode(b"\x0a\x05Hello\x0a\x05World", 7)

        # Assert that the method returns the correct value
        assert message == String(value="Hello")


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode data type
        message = String().encode()

        # Assert that the method returns the correct value
        assert message == b""

    @pytest.mark.parametrize(("data_type", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, data_type: String, buffer: bytes):
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
        data_type = String()
        message = data_type.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer


class TestSerialize:
    async def test_should_serialize_singleline_xml(self):
        # Serialize
        xml = Serializer.serialize(String.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == "<DataType><Basic>String</Basic></DataType>"

    async def test_should_deserialize_multiline_xml(self):
        # Serialize
        xml = Serializer.serialize(String.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <DataType>
              <Basic>String</Basic>
            </DataType>
            """
        )


class TestDeserialize:
    async def test_should_deserialize_singleline_xml(self):
        # Create xml
        xml = "<Basic>String</Basic>"

        # Deserialize
        data_type = Deserializer.deserialize(xml, String.deserialize)

        # Assert that the method returns the correct value
        assert data_type == String

    async def test_should_deserialize_multiline_xml(self):
        # Create xml
        xml = """
        <Basic>
            String
        </Basic>
        """

        # Deserialize
        data_type = Deserializer.deserialize(xml, String.deserialize)

        # Assert that the method returns the correct value
        assert data_type == String

    async def test_should_raise_on_unknown_basic_type(self):
        # Create xml
        xml = "<Basic>Complex</Basic>"

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Expected basic type value, received 'Complex'.")):
            Deserializer.deserialize(xml, String.deserialize)


class TestStringify:
    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            (String(), ""),
            (String(value="Hello, World!"), "Hello, World!"),
        ],
    )
    def test_should_return_string(self, data_type: String, value: str):
        # Convert data type
        assert f"{data_type}" == value


class TestEquality:
    @pytest.mark.parametrize(
        ("value"),
        [
            pytest.param("Hello, World!", id="Hello, World!"),
        ],
    )
    def test_should_compare_equality(self, value: float):
        assert String(value) == String(value)

    def test_should_compare_inequality(self):
        assert String(b"Hello, World!") != object()


class TestHash:
    def test_should_hash_constrained(self):
        # Create data type
        data_type_0 = String(value="Hello, World!")
        data_type_1 = String(value="Hello, World!")

        # Hash data type
        assert hash(data_type_0) == hash(data_type_1)
