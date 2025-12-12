import re
import textwrap
import unittest.mock

import pytest
import typing_extensions as typing

from sila.framework.data_types.boolean import Boolean
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError
from sila.framework.fdl.serializer import Serializer

NATIVE_TEST_CASES = [
    pytest.param(Boolean(), False, id="false"),
    pytest.param(Boolean(value=True), True, id="true"),
]
ENCODE_TEST_CASES = [
    pytest.param(Boolean(value=True), b"\x08\x01", id="1: 1"),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(Boolean(), b"\x08\x00", id="1: 0"),
    pytest.param(Boolean(), b"\x10\x00", id="2: 0"),
    pytest.param(Boolean(), b"\x08\x00\x10\x00", id="1: 0, 2: 0"),
    pytest.param(Boolean(), b"\x10\x00\x08\x00", id="2: 0, 1: 0"),
    pytest.param(Boolean(value=True), b"\x08\x01", id="1: 1"),
    pytest.param(Boolean(value=True), b"\x08\x01\x10\x00", id="1: 1, 2: 0"),
    pytest.param(Boolean(value=True), b"\x10\x00\x08\x01", id="2: 0, 1: 1"),
]


class TestInitFromNative:
    async def test_should_accept_no_value(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Boolean.from_native(context)

        # Assert that the method returns the correct value
        assert data_type == Boolean()

    @pytest.mark.parametrize(("data_type", "native"), NATIVE_TEST_CASES)
    async def test_should_accept_native(self, data_type: Boolean, native: bool):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        assert await Boolean.from_native(context, native) == data_type

    async def test_should_raise_on_invalid_type(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        with pytest.raises(TypeError, match=re.escape("Expected value of type 'bool', received 'int'.")):
            await Boolean.from_native(context, typing.cast(bool, 0))


class TestConvertToNative:
    @pytest.mark.parametrize(("data_type", "native"), NATIVE_TEST_CASES)
    async def test_should_convert_to_native(self, data_type: Boolean, native: bool):
        # Create context
        context = unittest.mock.Mock()

        # Convert data type
        assert await data_type.to_native(context) == native

    async def test_should_raise_on_invalid_type(self):
        # Create context
        context = unittest.mock.Mock()

        # Convert data type
        with pytest.raises(TypeError, match=re.escape("Expected value of type 'bool', received 'int'.")):
            await Boolean(typing.cast(bool, 0)).to_native(context)


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode data type
        message = Boolean.decode(b"")

        # Assert that the method returns the correct value
        assert message == Boolean()

    @pytest.mark.parametrize(("data_type", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, data_type: Boolean, buffer: bytes):
        # Decode data type
        message = Boolean.decode(buffer)

        # Assert that the method returns the correct value
        assert message == data_type

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = Boolean.decode(b"\x08\x01\x08\x00")

        # Assert that the method returns the correct value
        assert message == Boolean(value=False)

    async def test_should_decode_limited_buffer(self):
        # Decode data type
        message = Boolean.decode(b"\x08\x01\x08\x00", 2)

        # Assert that the method returns the correct value
        assert message == Boolean(value=True)


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode data type
        message = Boolean().encode()

        # Assert that the method returns the correct value
        assert message == b""

    @pytest.mark.parametrize(("data_type", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, data_type: Boolean, buffer: bytes):
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
        data_type = Boolean()
        message = data_type.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer


class TestSerialize:
    async def test_should_serialize_singleline_xml(self):
        # Serialize
        xml = Serializer.serialize(Boolean.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == "<DataType><Basic>Boolean</Basic></DataType>"

    async def test_should_deserialize_multiline_xml(self):
        # Serialize
        xml = Serializer.serialize(Boolean.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <DataType>
              <Basic>Boolean</Basic>
            </DataType>
            """
        )


class TestDeserialize:
    async def test_should_deserialize_singleline_xml(self):
        # Create xml
        xml = "<Basic>Boolean</Basic>"

        # Deserialize
        data_type = Deserializer.deserialize(xml, Boolean.deserialize)

        # Assert that the method returns the correct value
        assert data_type == Boolean

    async def test_should_deserialize_multiline_xml(self):
        # Create xml
        xml = """
        <Basic>
            Boolean
        </Basic>
        """

        # Deserialize
        data_type = Deserializer.deserialize(xml, Boolean.deserialize)

        # Assert that the method returns the correct value
        assert data_type == Boolean

    async def test_should_raise_on_unknown_basic_type(self):
        # Create xml
        xml = "<Basic>Complex</Basic>"

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Expected basic type value, received 'Complex'.")):
            Deserializer.deserialize(xml, Boolean.deserialize)


class TestStringify:
    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            pytest.param(Boolean(), "No", id="No"),
            pytest.param(Boolean(value=True), "Yes", id="Yes"),
        ],
    )
    async def test_should_return_string(self, data_type: Boolean, value: str):
        # Convert data type
        assert f"{data_type}" == value


class TestEquality:
    @pytest.mark.parametrize(
        ("value"),
        [
            pytest.param(True, id="True"),
            pytest.param(False, id="False"),
        ],
    )
    def test_should_compare_equality(self, value: float):
        assert Boolean(value) == Boolean(value)

    def test_should_compare_inequality(self):
        assert Boolean(b"Hello, World!") != object()


class TestHash:
    def test_should_hash_constrained(self):
        # Create data type
        data_type_0 = Boolean(value=True)
        data_type_1 = Boolean(value=True)

        # Hash data type
        assert hash(data_type_0) == hash(data_type_1)
