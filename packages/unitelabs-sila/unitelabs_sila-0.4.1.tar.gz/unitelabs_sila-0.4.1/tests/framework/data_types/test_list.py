import re
import textwrap
import unittest.mock

import pytest
import typing_extensions as typing

from sila.framework.constraints.maximal_length import MaximalLength
from sila.framework.data_types.any import Any
from sila.framework.data_types.constrained import Constrained
from sila.framework.data_types.custom import Custom
from sila.framework.data_types.element import Element
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.list import List
from sila.framework.data_types.string import String
from sila.framework.data_types.structure import Structure
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError
from sila.framework.fdl.serializer import Serializer
from sila.framework.protobuf.conversion_error import ConversionError
from sila.framework.protobuf.decode_error import DecodeError

STRING_ITEM_1 = b"\x0a\x08\x0a\x06SiLA 2"  # 1: { 1: {"SiLA 2"} }
STRING_ITEM_2 = b"\x0a\x04\x0a\x02is"  # 1: { 1: {"is"} }
STRING_ITEM_3 = b"\x0a\x0a\x0a\x08awesome!"  # 1: { 1: {"awesome!"} }
INTEGER_VALUE = b"\x12\x02\x08\x2a"  # 2: { 1: 42 }

NATIVE_TEST_CASES = [
    pytest.param(List.create(String)(value=[String(), String(), String()]), ["", "", ""], id='["", "", ""]'),
    pytest.param(
        List.create(String)(value=[String("SiLA 2"), String("is"), String("awesome!")]),
        ["SiLA 2", "is", "awesome!"],
        id='["SiLA 2", "is", "awesome!"]',
    ),
    pytest.param(
        List.create(Integer)(value=[Integer(5124), Integer(5125), Integer(5126)]),
        [5124, 5125, 5126],
        id="[5124, 5125, 5126]",
    ),
]
ENCODE_TEST_CASES = [
    pytest.param(
        List.create(String)(value=[String("SiLA 2"), String("is"), String("awesome!")]),
        STRING_ITEM_1 + STRING_ITEM_2 + STRING_ITEM_3,
        id='1: { 1: {"SiLA 2"} }, 1: { 1: {"is"} }, 1: { 1: {"awesome!"} }',
    ),
    pytest.param(
        List.create(Integer)(value=[Integer(5124), Integer(5125), Integer(5126)]),
        b"\x0a\x03\x08\x84\x28\x0a\x03\x08\x85\x28\x0a\x03\x08\x86\x28",
        id="1: { 1: 5124 }, 1: { 1: 5125 }, 1: { 1: 5126 }",
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        List.create(String)(value=[String("SiLA 2"), String("is"), String("awesome!")]),
        STRING_ITEM_1 + b"\x10\x00" + STRING_ITEM_2 + STRING_ITEM_3,
        id='1: { 1: {"SiLA 2"} }, 2: 0, 1: { 1: {"is"} }, 1: { 1: {"awesome!"} }',
    ),
    pytest.param(
        List.create(String)(value=[String("SiLA 2"), String("is"), String("awesome!")]),
        STRING_ITEM_1 + STRING_ITEM_2 + b"\x10\x00" + STRING_ITEM_3,
        id='1: { 1: {"SiLA 2"} }, 1: { 1: {"is"} }, 2: 0, 1: { 1: {"awesome!"} }',
    ),
    pytest.param(
        List.create(String)(value=[String("SiLA 2"), String("is"), String("awesome!")]),
        STRING_ITEM_1 + STRING_ITEM_2 + STRING_ITEM_3 + b"\x10\x00",
        id='1: { 1: {"SiLA 2"} }, 1: { 1: {"is"} }, 1: { 1: {"awesome!"} }, 2: 0',
    ),
]


class TestInitFromNative:
    async def test_should_accept_no_value(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await List.from_native(context)

        # Assert that the method returns the correct value
        assert data_type == List()

    @pytest.mark.parametrize(("expected", "native"), NATIVE_TEST_CASES)
    async def test_should_accept_native(self, expected: List, native: list):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await type(expected).from_native(context, native)

        # Assert that the method returns the correct value
        assert data_type == expected

    async def test_should_raise_on_invalid_type(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = List.create(String)

        with pytest.raises(ConversionError, match=re.escape("Expected value of type 'str', received 'int'.")) as error:
            await data_type.from_native(context, [0])

        assert error.value.path == [0]

    async def test_should_raise_on_invalid_value(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = List.create(String)

        with pytest.raises(
            ConversionError, match=re.escape("String must not exceed 2²¹ characters, received '2097153'.")
        ) as error:
            await data_type.from_native(context, [" " * (2**21 + 1)])

        assert error.value.path == [0]

    async def test_should_raise_nested_error(self):
        # Create data type
        context = unittest.mock.Mock()
        inner_data_type = Structure.create(
            {
                "string_value": Element(identifier="StringID", display_name="String ID", data_type=String),
                "integer_value": Element(identifier="IntegerID", display_name="Integer ID", data_type=Integer),
            }
        )
        data_type = List.create(inner_data_type)

        with pytest.raises(ConversionError, match=re.escape("Expected value of type 'int', received 'str'.")) as error:
            await data_type.from_native(
                context, [{"string_value": "a", "integer_value": 1}, {"string_value": "b", "integer_value": "invalid"}]
            )

        assert error.value.path == [1, "IntegerID"]


class TestConvertToNative:
    @pytest.mark.parametrize(("data_type", "native"), NATIVE_TEST_CASES)
    async def test_should_convert_to_native(self, data_type: List, native: list):
        # Convert data type
        context = unittest.mock.Mock()
        assert await data_type.to_native(context) == native

    async def test_should_raise_on_invalid_type(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = List.create(String)

        # Convert data type
        with pytest.raises(
            ConversionError, match=re.escape("Expected value of type 'String', received 'Integer'.")
        ) as error:
            await data_type([Integer(0)]).to_native(context)

        assert error.value.path == [0]

    async def test_should_raise_on_invalid_value(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = List.create(String)

        # Convert data type
        with pytest.raises(
            ConversionError, match=re.escape("String must not exceed 2²¹ characters, received '2097153'.")
        ) as error:
            await data_type([String(" " * (2**21 + 1))]).to_native(context)

        assert error.value.path == [0]

    async def test_should_raise_nested_error(self):
        # Create data type
        context = unittest.mock.Mock()
        inner_data_type = Structure.create(
            {
                "string_value": Element(identifier="StringID", display_name="String ID", data_type=String),
                "integer_value": Element(identifier="IntegerID", display_name="Integer ID", data_type=Integer),
            }
        )
        data_type = List.create(inner_data_type)
        data_value = data_type(
            [
                inner_data_type({"string_value": String("a"), "integer_value": Integer(1)}),
                inner_data_type({"string_value": String("b"), "integer_value": String("Invalid")}),
            ]
        )

        # Convert data type
        with pytest.raises(
            ConversionError, match=re.escape("Expected value of type 'Integer', received 'String'.")
        ) as error:
            await data_value.to_native(context)

        assert error.value.path == [1, "IntegerID"]


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode data type
        message = List.decode(b"")

        # Assert that the method returns the correct value
        assert message == List()

    @pytest.mark.parametrize(("data_type", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, data_type: List, buffer: bytes):
        # Decode data type
        message = data_type.decode(buffer)

        # Assert that the method returns the correct value
        assert message == data_type

    async def test_should_decode_limited_buffer(self):
        # Create data type
        data_type = List.create(data_type=String)

        # Decode data type
        message = data_type.decode(STRING_ITEM_1 + STRING_ITEM_2 + STRING_ITEM_3, 16)

        # Assert that the method returns the correct value
        assert message == data_type([String("SiLA 2"), String("is")])

    @pytest.mark.parametrize(
        "buffer",
        [
            STRING_ITEM_1 + STRING_ITEM_2 + STRING_ITEM_3 + INTEGER_VALUE,
            STRING_ITEM_1 + STRING_ITEM_2 + INTEGER_VALUE + STRING_ITEM_3,
            STRING_ITEM_1 + INTEGER_VALUE + STRING_ITEM_2 + STRING_ITEM_3,
            INTEGER_VALUE + STRING_ITEM_1 + STRING_ITEM_2 + STRING_ITEM_3,
        ],
    )
    async def test_should_decode_interleaved_fields(self, buffer: bytes):
        # Create data type
        data_type = List.create(data_type=String)
        structure_type = Structure.create(
            elements={
                "string_list": Element(
                    identifier="StringList",
                    display_name="String List",
                    description="A list of SiLA data type String.",
                    data_type=data_type,
                ),
                "integer_value": Element(
                    identifier="IntegerValue",
                    display_name="Integer Value",
                    description="A value of SiLA data type Integer.",
                    data_type=Integer,
                ),
            }
        )

        # Decode data type
        message = structure_type.decode(buffer)

        # Assert that the method returns the correct value
        assert message == structure_type(
            {
                "string_list": data_type([String("SiLA 2"), String("is"), String("awesome!")]),
                "integer_value": Integer(42),
            }
        )

    async def test_should_decode_structure(self):
        # Create data type
        structure_type = Structure.create(
            elements={
                "string_value": Element(
                    identifier="StringValue",
                    display_name="String Value",
                    description="A value of SiLA data type String.",
                    data_type=String,
                ),
                "integer_value": Element(
                    identifier="IntegerValue",
                    display_name="Integer Value",
                    description="A value of SiLA data type Integer.",
                    data_type=Integer,
                ),
            }
        )
        data_type = List.create(data_type=structure_type)

        # Decode data type
        message = data_type.decode(
            b"\x0a\x0d\x0a\x07\x0a\x05Hello\x12\x02\x08\x2a\x0a\x0d\x0a\x07\x0a\x05World\x12\x02\x08\x18"
        )

        # Assert that the method returns the correct value
        assert message == data_type(
            [
                structure_type({"string_value": String("Hello"), "integer_value": Integer(42)}),
                structure_type({"string_value": String("World"), "integer_value": Integer(24)}),
            ]
        )

    async def test_should_decode_constrained(self):
        # Create data type
        constrained_type = Constrained.create(String, [MaximalLength(5)])
        data_type = List.create(data_type=constrained_type)

        # Decode data type
        message = data_type.decode(b"\x0a\x07\x0a\x05\x48\x65\x6c\x6c\x6f\x0a\x07\x0a\x05\x57\x6f\x72\x6c\x64")

        # Assert that the method returns the correct value
        assert message == data_type([constrained_type(String("Hello")), constrained_type(String("World"))])

    async def test_should_decode_custom(self):
        # Create data type
        custom_type = Custom.create(identifier="Custom", display_name="Custom", data_type=String)
        data_type = List.create(data_type=custom_type)

        # Decode data type
        message = data_type.decode(
            b"\x0a\x09\x0a\x07\x0a\x05\x48\x65\x6c\x6c\x6f\x0a\x09\x0a\x07\x0a\x05\x57\x6f\x72\x6c\x64"
        )

        # Assert that the method returns the correct value
        assert message == data_type([custom_type(String("Hello")), custom_type(String("World"))])

    async def test_should_raise_on_decode_error(self):
        # Create data type
        data_type = List.create(data_type=String)

        # Decode data type
        with pytest.raises(DecodeError, match=re.escape("Expected wire type 'LEN', received 'VARINT'.")) as error:
            data_type.decode(b"\x0a\x07\x0a\x05Hello\x0a\x07\x08\x01")

        assert error.value.offset == 12
        assert error.value.path == [1]


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode data type
        message = List().encode()

        # Assert that the method returns the correct value
        assert message == b""

    @pytest.mark.parametrize(("data_type", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, data_type: List, buffer: bytes):
        # Encode data type
        message = data_type.encode()

        # Assert that the method returns the correct value
        assert message == buffer

    @pytest.mark.parametrize(
        ("number", "buffer"),
        [
            pytest.param(1, b"\x0a\x00\x0a\x00\x0a\x00", id="default"),
            pytest.param(2, b"\x12\x00\x12\x00\x12\x00", id="custom"),
        ],
    )
    async def test_should_encode_field_number(self, number: int, buffer: bytes):
        # Encode data type
        data_type = List.create(String)(value=[String(), String(), String()])
        # Encode data type
        message = data_type.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer

    async def test_should_encode_structure(self):
        # Create data type
        structure_type = Structure.create(
            elements={
                "string_value": Element(
                    identifier="StringValue",
                    display_name="String Value",
                    description="A value of SiLA data type String.",
                    data_type=String,
                ),
                "integer_value": Element(
                    identifier="IntegerValue",
                    display_name="Integer Value",
                    description="A value of SiLA data type Integer.",
                    data_type=Integer,
                ),
            }
        )
        list_type = List.create(data_type=structure_type)
        data_type = list_type(
            [
                structure_type({"string_value": String("Hello"), "integer_value": Integer(42)}),
                structure_type({"string_value": String("World"), "integer_value": Integer(24)}),
            ]
        )

        # Encode data type
        message = data_type.encode()

        # Assert that the method returns the correct value
        assert message == (
            b"\x0a\x0d\x0a\x07\x0a\x05\x48\x65\x6c\x6c\x6f\x12\x02\x08\x2a"
            b"\x0a\x0d\x0a\x07\x0a\x05\x57\x6f\x72\x6c\x64\x12\x02\x08\x18"
        )

    async def test_should_encode_constrained(self):
        # Create data type
        constrained_type = Constrained.create(String, [MaximalLength(5)])
        list_type = List.create(data_type=constrained_type)
        data_type = list_type([constrained_type(String("Hello")), constrained_type(String("World"))])

        # Encode data type
        message = data_type.encode()

        # Assert that the method returns the correct value
        assert message == b"\x0a\x07\x0a\x05\x48\x65\x6c\x6c\x6f\x0a\x07\x0a\x05\x57\x6f\x72\x6c\x64"

    async def test_should_encode_custom(self):
        # Create data type
        custom_type = Custom.create(identifier="Custom", display_name="Custom", data_type=String)
        list_type = List.create(data_type=custom_type)
        data_type = list_type([custom_type(String("Hello")), custom_type(String("World"))])

        # Encode data type
        message = data_type.encode()

        # Assert that the method returns the correct value
        assert message == b"\x0a\x09\x0a\x07\x0a\x05\x48\x65\x6c\x6c\x6f\x0a\x09\x0a\x07\x0a\x05\x57\x6f\x72\x6c\x64"


class TestCreate:
    def test_should_create_list(self):
        # Create data type
        data_type = List.create()

        # Assert that the method returns the correct value
        assert issubclass(data_type, List)
        assert data_type.__name__ == "List"
        assert data_type.data_type == Any

    def test_should_accept_data_type(self):
        # Create data type
        data_type = List.create(data_type=String)

        # Assert that the method returns the correct value
        assert data_type.data_type == String

    def test_should_accept_name(self):
        # Create data type
        data_type = List.create(name="ListName")

        # Assert that the method returns the correct value
        assert data_type.__name__ == "ListName"

    def test_should_raise_on_invalid_data_type(self):
        # Create data type
        with pytest.raises(TypeError, match=re.escape("The data type of list entries must not be a list itself.")):
            List.create(data_type=typing.cast(type[String], List))


class TestSerialize:
    async def test_should_serialize_singleline_xml(self):
        # Create data type
        data_type = List.create(data_type=String)

        # Serialize
        xml = Serializer.serialize(data_type.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == "<DataType><List><DataType><Basic>String</Basic></DataType></List></DataType>"

    async def test_should_deserialize_multiline_xml(self):
        # Create data type
        data_type = List.create(data_type=String)

        # Serialize
        xml = Serializer.serialize(data_type.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <DataType>
              <List>
                <DataType>
                  <Basic>String</Basic>
                </DataType>
              </List>
            </DataType>
            """
        )


class TestDeserialize:
    async def test_should_deserialize_singleline_xml(self):
        # Create xml
        xml = "<List><DataType><Basic>String</Basic></DataType></List>"

        # Deserialize
        data_type = Deserializer.deserialize(xml, List.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, List)
        assert data_type.data_type == String

    async def test_should_deserialize_multiline_xml(self):
        # Create xml
        xml = """
        <List>
          <DataType>
            <Basic>String</Basic>
          </DataType>
        </List>
        """

        # Deserialize
        data_type = Deserializer.deserialize(xml, List.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, List)
        assert data_type.data_type == String

    async def test_should_raise_on_unexpected_characters(self):
        # Create xml
        xml = "<List>Hello, World!</List>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape("Expected start element with name 'DataType', received characters '['Hello, World!']'."),
        ):
            Deserializer.deserialize(xml, List.deserialize)

    async def test_should_raise_on_unexpected_start_element(self):
        # Create xml
        xml = "<List><Basic>String</Basic></List>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape("Expected start element with name 'DataType', received start element with name 'Basic'."),
        ):
            Deserializer.deserialize(xml, List.deserialize)

    async def test_should_raise_on_invalid_data_type(self):
        # Create xml
        xml = "<List><DataType><Basic>Complex</Basic></DataType></List>"

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Expected basic type value, received 'Complex'.")):
            Deserializer.deserialize(xml, List.deserialize)

    async def test_should_raise_on_list_data_type(self):
        # Create xml
        xml = "<List><DataType><List><DataType><Basic>String</Basic></DataType></List></DataType></List>"

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("The data type of list entries must not be a list itself.")):
            Deserializer.deserialize(xml, List.deserialize)


class TestEquality:
    def test_should_be_true_on_equal_lists(self):
        # Create data type
        data_type_0 = List.create(data_type=String)([String("Hello"), String("World")])
        data_type_1 = List.create(data_type=String)([String("Hello"), String("World")])

        # Compare equality
        assert data_type_0 == data_type_1

    def test_should_be_false_on_unequal_type(self):
        # Create data type
        data_type_0 = List.create(data_type=String)([])
        data_type_1 = List.create(data_type=Integer)([])

        # Compare equality
        assert data_type_0 != data_type_1

    def test_should_be_false_on_unequal_value(self):
        # Create data type
        data_type_0 = List.create(data_type=String)([String("Hello")])
        data_type_1 = List.create(data_type=String)([String("World")])

        # Compare equality
        assert data_type_0 != data_type_1

    def test_should_be_false_on_non_list(self):
        # Create data type
        data_type = List.create(data_type=String)([String("Hello")])

        # Compare equality
        assert data_type != unittest.mock.Mock()
