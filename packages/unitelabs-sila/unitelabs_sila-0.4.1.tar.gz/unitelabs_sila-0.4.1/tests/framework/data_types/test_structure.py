import re
import textwrap
import unittest.mock

import pytest

from sila.framework.constraints.maximal_length import MaximalLength
from sila.framework.data_types.constrained import Constrained
from sila.framework.data_types.custom import Custom
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.list import List
from sila.framework.data_types.real import Real
from sila.framework.data_types.string import String
from sila.framework.data_types.structure import Element, Structure
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError
from sila.framework.fdl.serializer import Serializer
from sila.framework.protobuf.conversion_error import ConversionError
from sila.framework.protobuf.decode_error import DecodeError

NATIVE_TEST_CASES = [
    pytest.param(
        Structure.create(
            {"string_value": Element(identifier="StringValue", display_name="String Value", data_type=String)}
        )({"string_value": String("Hello, World!")}),
        {"string_value": "Hello, World!"},
        id='{"string_value": "Hello, World!"}',
    ),
    pytest.param(
        Structure.create(
            {"integer_value": Element(identifier="IntegerValue", display_name="Integer Value", data_type=Integer)}
        )({"integer_value": Integer(42)}),
        {"integer_value": 42},
        id='{"integer_value": 42}',
    ),
]
ENCODE_TEST_CASES = [
    pytest.param(
        Structure.create(
            {"string_value": Element(identifier="StringValue", display_name="String Value", data_type=String)}
        )({"string_value": String("Hello, World!")}),
        b"\x0a\x0f\x0a\x0dHello, World!",
        id='1: { 1: {"Hello, World!"} }',
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        Structure.create(
            {"string_value": Element(identifier="StringValue", display_name="String Value", data_type=String)}
        )({"string_value": String("Hello, World!")}),
        b"\n\x0f\n\rHello, World!\x10\x00",
        id='1: { 1: {"Hello, World!"} }, 2: 0',
    ),
    pytest.param(
        Structure.create(
            {"string_value": Element(identifier="StringValue", display_name="String Value", data_type=String)}
        )({"string_value": String("Hello, World!")}),
        b"\x10\x00\n\x0f\n\rHello, World!",
        id='2: 0, 1: { 1: {"Hello, World!"} }',
    ),
    pytest.param(
        Structure.create(
            {"string_list": Element(identifier="ListValue", display_name="List Value", data_type=List.create(String))}
        )({"string_list": List.create(String)([])}),
        b"",
        id="",
    ),
]


class TestInitFromNative:
    async def test_should_accept_no_value(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Structure.from_native(context)

        # Assert that the method returns the correct value
        assert data_type == Structure()

    @pytest.mark.parametrize(("expected", "native"), NATIVE_TEST_CASES)
    async def test_should_accept_native(self, expected: Structure, native: dict):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await type(expected).from_native(context, native)

        # Assert that the method returns the correct value
        assert data_type == expected

    async def test_should_raise_on_missing_key(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = Structure.create(
            {
                "string_value": Element(identifier="StringID", display_name="String ID", data_type=String),
                "integer_value": Element(identifier="IntegerID", display_name="Integer ID", data_type=Integer),
            }
        )

        with pytest.raises(
            ConversionError, match=re.escape("Missing field 'IntegerID' in message 'Structure'.")
        ) as error:
            await data_type.from_native(context, {"string_value": "Hello, World!"})

        assert error.value.path == ["IntegerID"]

    async def test_should_raise_nested_error(self):
        # Create data type
        context = unittest.mock.Mock()
        inner_data_type = Structure.create(
            {
                "string_value": Element(identifier="StringID", display_name="String ID", data_type=String),
                "integer_value": Element(identifier="IntegerID", display_name="Integer ID", data_type=Integer),
            }
        )
        data_type = Structure.create(
            {
                "inner_structure": Element(
                    identifier="InnerStructure", display_name="Inner Structure", data_type=inner_data_type
                )
            }
        )

        with pytest.raises(ConversionError, match=re.escape("Expected value of type 'int', received 'str'.")) as error:
            await data_type.from_native(
                context, {"inner_structure": {"string_value": "Hello, World!", "integer_value": "Invalid"}}
            )

        assert error.value.path == ["InnerStructure", "IntegerID"]


class TestConvertToNative:
    @pytest.mark.parametrize(("data_type", "native"), NATIVE_TEST_CASES)
    async def test_should_convert_to_native(self, data_type: Structure, native: dict):
        # Convert data type
        context = unittest.mock.Mock()
        assert await data_type.to_native(context) == native

    async def test_should_raise_on_invalid_type(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = Structure.create(
            elements={
                "string_value": Element(identifier="StringID", display_name="String ID", data_type=String),
                "integer_value": Element(identifier="IntegerID", display_name="Integer ID", data_type=Integer),
            }
        )
        data_value = data_type({"string_value": String("Hello, World!"), "integer_value": String("Invalid")})

        # Convert data type
        with pytest.raises(
            ConversionError, match=re.escape("Expected value of type 'Integer', received 'String'.")
        ) as error:
            await data_value.to_native(context)

        assert error.value.path == ["IntegerID"]

    async def test_should_raise_on_invalid_value(self):
        # Create data type
        context = unittest.mock.Mock()
        constrained_data_type = Constrained.create(String, [MaximalLength(5)])
        data_type = Structure.create(
            elements={
                "string_value": Element(
                    identifier="StringID", display_name="String ID", data_type=constrained_data_type
                ),
                "integer_value": Element(identifier="IntegerID", display_name="Integer ID", data_type=Integer),
            }
        )
        data_value = data_type(
            {"string_value": constrained_data_type(String("Hello, World!")), "integer_value": Integer()}
        )

        # Convert data type
        with pytest.raises(
            ConversionError, match=re.escape("Expected value with maximal length '5', received '13'.")
        ) as error:
            await data_value.to_native(context)

        assert error.value.path == ["StringID"]

    async def test_should_raise_on_missing_key(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = Structure.create(
            elements={
                "string_value": Element(identifier="StringID", display_name="String ID", data_type=String),
                "integer_value": Element(identifier="IntegerID", display_name="Integer ID", data_type=Integer),
            }
        )
        data_value = data_type({"string_value": String("Hello, World!")})

        # Convert data type
        with pytest.raises(
            ConversionError, match=re.escape("Missing field 'IntegerID' in message 'Structure'.")
        ) as error:
            await data_value.to_native(context)

        assert error.value.path == ["IntegerID"]

    async def test_should_raise_nested_error(self):
        # Create data type
        context = unittest.mock.Mock()
        inner_data_type = Structure.create(
            {
                "string_value": Element(identifier="StringID", display_name="String ID", data_type=String),
                "integer_value": Element(identifier="IntegerID", display_name="Integer ID", data_type=Integer),
            }
        )
        data_type = Structure.create(
            {
                "inner_structure": Element(
                    identifier="InnerStructure", display_name="Inner Structure", data_type=inner_data_type
                )
            }
        )
        data_value = data_type(
            {
                "inner_structure": inner_data_type(
                    {"string_value": String("Hello, World!"), "integer_value": String("Invalid")}
                )
            }
        )

        # Convert data type
        with pytest.raises(
            ConversionError, match=re.escape("Expected value of type 'Integer', received 'String'.")
        ) as error:
            await data_value.to_native(context)

        assert error.value.path == ["InnerStructure", "IntegerID"]


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode data type
        message = Structure.decode(b"")

        # Assert that the method returns the correct value
        assert message == Structure()

    @pytest.mark.parametrize(("data_type", "reader"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, data_type: Structure, reader: bytes):
        # Decode data type
        message = data_type.decode(reader)

        # Assert that the method returns the correct value
        assert message == data_type

    async def test_should_decode_multiple_fields(self):
        # Create data type
        data_type = Structure.create(
            {"string_value": Element(identifier="StringValue", display_name="String Value", data_type=String)}
        )

        # Decode message
        message = data_type.decode(b"\x0a\x07\x0a\x05Hello\x0a\x07\x0a\x05World")

        # Assert that the method returns the correct value
        assert message == data_type({"string_value": String("World")})

    async def test_should_decode_limited_buffer(self):
        # Create data type
        data_type = Structure.create(
            {"string_value": Element(identifier="StringValue", display_name="String Value", data_type=String)}
        )

        # Decode data type
        message = data_type.decode(b"\x0a\x07\x0a\x05Hello\x0a\x07\x0a\x05World", 9)

        # Assert that the method returns the correct value
        assert message == data_type({"string_value": String("Hello")})

    async def test_should_decode_list(self):
        # Create data type
        list_type = List.create(data_type=String)
        data_type = Structure.create(
            {"string_list": Element(identifier="StringList", display_name="String List", data_type=list_type)}
        )

        # Decode data type
        message = data_type.decode(b"\x0a\x07\x0a\x05Hello\x0a\x07\x0a\x05World")

        # Assert that the method returns the correct value
        assert message == data_type({"string_list": list_type([String("Hello"), String("World")])})

    async def test_should_decode_structure(self):
        # Create data type
        inner_structure = Structure.create(
            {
                "inner_string_type_value": Element(
                    identifier="InnerStringTypeValue", display_name="Inner String Type Value", data_type=String
                ),
                "inner_integer_type_value": Element(
                    identifier="InnerIntegerTypeValue", display_name="Inner Integer Type Value", data_type=Integer
                ),
            }
        )
        middle_structure = Structure.create(
            {
                "middle_string_type_value": Element(
                    identifier="MiddleStringTypeValue", display_name="Middle String Type Value", data_type=String
                ),
                "middle_integer_type_value": Element(
                    identifier="MiddleIntegerTypeValue", display_name="Middle Integer Type Value", data_type=Integer
                ),
                "inner_structure": Element(
                    identifier="InnerStructure", display_name="Inner Structure", data_type=inner_structure
                ),
            }
        )
        data_type = Structure.create(
            {
                "outer_string_type_value": Element(
                    identifier="OuterStringTypeValue", display_name="Outer String Type Value", data_type=String
                ),
                "outer_integer_type_value": Element(
                    identifier="OuterIntegerTypeValue", display_name="Outer Integer Type Value", data_type=Integer
                ),
                "middle_structure": Element(
                    identifier="MiddleStructure", display_name="Middle Structure", data_type=middle_structure
                ),
            }
        )

        # Decode data type
        message = data_type.decode(
            b"\x0a\x13\x0a\x11Outer_Test_String\x12\x03\x08\xd7\x08\x1a\x37"
            b"\x0a\x14\x0a\x12Middle_Test_String\x12\x03\x08\xae\x11\x1a\x1a"
            b"\x0a\x13\x0a\x11Inner_Test_String\x12\x03\x08\x85\x1a"
        )

        # Assert that the method returns the correct value
        assert message == data_type(
            {
                "outer_string_type_value": String("Outer_Test_String"),
                "outer_integer_type_value": Integer(1111),
                "middle_structure": middle_structure(
                    {
                        "middle_string_type_value": String("Middle_Test_String"),
                        "middle_integer_type_value": Integer(2222),
                        "inner_structure": inner_structure(
                            {
                                "inner_string_type_value": String("Inner_Test_String"),
                                "inner_integer_type_value": Integer(3333),
                            }
                        ),
                    }
                ),
            }
        )

    async def test_should_decode_constrained(self):
        # Create data type
        constrained_type = Constrained.create(String, [MaximalLength(5)])
        data_type = Structure.create(
            {
                "constrained_string": Element(
                    identifier="ConstrainedString", display_name="Constrained String", data_type=constrained_type
                )
            }
        )

        # Decode data type
        message = data_type.decode(b"\x0a\x07\x0a\x05Hello")

        # Assert that the method returns the correct value
        assert message == data_type({"constrained_string": constrained_type(String("Hello"))})

    async def test_should_decode_custom(self):
        # Create data type
        custom_type = Custom.create(identifier="Custom", display_name="Custom", data_type=String)
        data_type = Structure.create(
            {"custom_string": Element(identifier="CustomString", display_name="Custom String", data_type=custom_type)}
        )

        # Decode data type
        message = data_type.decode(b"\x0a\x09\x0a\x07\x0a\x05Hello")

        # Assert that the method returns the correct value
        assert message == data_type({"custom_string": custom_type(String("Hello"))})

    async def test_should_raise_on_decode_error(self):
        # Create data type
        data_type = Structure.create(
            {"string_value": Element(identifier="StringValue", display_name="String Value", data_type=String)}
        )

        # Decode data type
        with pytest.raises(DecodeError, match=re.escape("Expected wire type 'LEN', received 'VARINT'.")) as error:
            data_type.decode(b"\x0a\x07\x0a\x05Hello\x0a\x07\x08\x01")

        assert error.value.offset == 12
        assert error.value.path == ["StringValue"]


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode data type
        message = Structure().encode()

        # Assert that the method returns the correct value
        assert message == b""

    @pytest.mark.parametrize(("data_type", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, data_type: Structure, buffer: bytes):
        # Encode data type
        message = data_type.encode()

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
        # Encode data type
        data_type = Structure.create(
            {"string_value": Element(identifier="StringValue", display_name="String Value", data_type=String)}
        )({"string_value": String()})
        message = data_type.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer

    async def test_should_encode_list(self):
        # Create data type
        list_type = List.create(data_type=String)
        data_type = Structure.create(
            {"string_list": Element(identifier="StringList", display_name="Strin gList", data_type=list_type)}
        )
        data_value = data_type({"string_list": list_type([String("Hello"), String("World")])})

        # Encode data type
        message = data_value.encode()

        # Assert that the method returns the correct value
        assert message == b"\x0a\x07\x0a\x05\x48\x65\x6c\x6c\x6f\x0a\x07\x0a\x05\x57\x6f\x72\x6c\x64"

    async def test_should_encode_structure(self):
        # Create data type
        inner_structure = Structure.create(
            {
                "inner_string_type_value": Element(
                    identifier="InnerStringTypeValue", display_name="Inner String Type Value", data_type=String
                ),
                "inner_integer_type_value": Element(
                    identifier="InnerIntegerTypeValue", display_name="Inner Integer Type Value", data_type=Integer
                ),
            }
        )
        middle_structure = Structure.create(
            {
                "middle_string_type_value": Element(
                    identifier="MiddleStringTypeValue", display_name="Middle String Type Value", data_type=String
                ),
                "middle_integer_type_value": Element(
                    identifier="MiddleIntegerTypeValue", display_name="Middle Integer Type Value", data_type=Integer
                ),
                "inner_structure": Element(
                    identifier="InnerStructure", display_name="Inner Structure", data_type=inner_structure
                ),
            }
        )
        data_type = Structure.create(
            {
                "outer_string_type_value": Element(
                    identifier="OuterStringTypeValue", display_name="Outer String Type Value", data_type=String
                ),
                "outer_integer_type_value": Element(
                    identifier="OuterIntegerTypeValue", display_name="Outer Integer Type Value", data_type=Integer
                ),
                "middle_structure": Element(
                    identifier="MiddleStructure", display_name="Middle Structure", data_type=middle_structure
                ),
            }
        )

        data_value = data_type(
            {
                "outer_string_type_value": String("Outer_Test_String"),
                "outer_integer_type_value": Integer(1111),
                "middle_structure": middle_structure(
                    {
                        "middle_string_type_value": String("Middle_Test_String"),
                        "middle_integer_type_value": Integer(2222),
                        "inner_structure": inner_structure(
                            {
                                "inner_string_type_value": String("Inner_Test_String"),
                                "inner_integer_type_value": Integer(3333),
                            }
                        ),
                    }
                ),
            }
        )

        # Encode data type
        message = data_value.encode()

        # Assert that the method returns the correct value
        assert message == (
            b"\x0a\x13\x0a\x11Outer_Test_String\x12\x03\x08\xd7\x08\x1a\x37"
            b"\x0a\x14\x0a\x12Middle_Test_String\x12\x03\x08\xae\x11\x1a\x1a"
            b"\x0a\x13\x0a\x11Inner_Test_String\x12\x03\x08\x85\x1a"
        )

    async def test_should_encode_constrained(self):
        # Create data type
        constrained_type = Constrained.create(String, [MaximalLength(5)])
        data_type = Structure.create(
            {
                "constrained_string": Element(
                    identifier="ConstrainedString", display_name="Constrained String", data_type=constrained_type
                )
            }
        )
        data_value = data_type({"constrained_string": constrained_type(String("Hello"))})

        # Encode data type
        message = data_value.encode()

        # Assert that the method returns the correct value
        assert message == b"\x0a\x07\x0a\x05\x48\x65\x6c\x6c\x6f"

    async def test_should_encode_custom(self):
        # Create data type
        custom_type = Custom.create(identifier="Custom", display_name="Custom", data_type=String)
        data_type = Structure.create(
            {"custom_string": Element(identifier="CustomString", display_name="Custom String", data_type=custom_type)}
        )
        data_value = data_type({"custom_string": custom_type(String("Hello"))})

        # Encode data type
        message = data_value.encode()

        # Assert that the method returns the correct value
        assert message == b"\x0a\x09\x0a\x07\x0a\x05Hello"


class TestCreate:
    def test_should_create_structure(self):
        # Create data type
        data_type = Structure.create()

        # Assert that the method returns the correct value
        assert issubclass(data_type, Structure)
        assert data_type.__name__ == "Structure"
        assert data_type.elements == {}

    def test_should_accept_elements(self):
        # Create data type
        data_type = Structure.create(
            elements={
                "string_value": Element(identifier="StringValue", display_name="String Value", data_type=String),
                "integer_value": Element(identifier="IntegerValue", display_name="Integer Value", data_type=Integer),
            }
        )

        # Assert that the method returns the correct value
        assert data_type.elements == {
            "string_value": Element(identifier="StringValue", display_name="String Value", data_type=String),
            "integer_value": Element(identifier="IntegerValue", display_name="Integer Value", data_type=Integer),
        }

    def test_should_accept_name(self):
        # Create data type
        data_type = Structure.create(name="StructureName")

        # Assert that the method returns the correct value
        assert data_type.__name__ == "StructureName"

    def test_should_accept_description(self):
        # Create data type
        data_type = Structure.create(description="Structure description.")

        # Assert that the method returns the correct value
        assert data_type.__doc__ == "Structure description."


class TestSerialize:
    async def test_should_serialize_singleline_xml(self):
        # Create data type
        data_type = Structure.create(
            {
                "a": Element(
                    identifier="StringValue",
                    display_name="String Value",
                    description="String Value.",
                    data_type=String,
                ),
                "b": Element(
                    identifier="IntegerValue",
                    display_name="Integer Value",
                    description="Integer Value.",
                    data_type=Integer,
                ),
            }
        )

        # Serialize
        xml = Serializer.serialize(data_type.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == (
            "<DataType><Structure><Element>"
            "<Identifier>StringValue</Identifier>"
            "<DisplayName>String Value</DisplayName>"
            "<Description>String Value.</Description>"
            "<DataType><Basic>String</Basic></DataType>"
            "</Element><Element>"
            "<Identifier>IntegerValue</Identifier>"
            "<DisplayName>Integer Value</DisplayName>"
            "<Description>Integer Value.</Description>"
            "<DataType><Basic>Integer</Basic></DataType>"
            "</Element></Structure></DataType>"
        )

    async def test_should_serialize_multiline_xml(self):
        # Create data type
        data_type = Structure.create(
            {
                "a": Element(
                    identifier="StringValue",
                    display_name="String Value",
                    description="String Value.",
                    data_type=String,
                ),
                "b": Element(
                    identifier="IntegerValue",
                    display_name="Integer Value",
                    description="Integer Value.",
                    data_type=Integer,
                ),
            }
        )

        # Serialize
        xml = Serializer.serialize(data_type.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <DataType>
              <Structure>
                <Element>
                  <Identifier>StringValue</Identifier>
                  <DisplayName>String Value</DisplayName>
                  <Description>String Value.</Description>
                  <DataType>
                    <Basic>String</Basic>
                  </DataType>
                </Element>
                <Element>
                  <Identifier>IntegerValue</Identifier>
                  <DisplayName>Integer Value</DisplayName>
                  <Description>Integer Value.</Description>
                  <DataType>
                    <Basic>Integer</Basic>
                  </DataType>
                </Element>
              </Structure>
            </DataType>
            """
        )

    async def test_should_serialize_long_description(self):
        # Create data type
        data_type = Structure.create(
            {
                "a": Element(
                    identifier="StringValue",
                    display_name="String Value",
                    description=(
                        "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam "
                        "nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam "
                        "erat, sed diam voluptua. At vero eos et accusam et justo duo "
                        "dolores et ea rebum."
                    ),
                    data_type=String,
                ),
            }
        )

        # Serialize
        xml = Serializer.serialize(data_type.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <DataType>
              <Structure>
                <Element>
                  <Identifier>StringValue</Identifier>
                  <DisplayName>String Value</DisplayName>
                  <Description>
                    Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor
                    invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et
                    accusam et justo duo dolores et ea rebum.
                  </Description>
                  <DataType>
                    <Basic>String</Basic>
                  </DataType>
                </Element>
              </Structure>
            </DataType>
            """
        )


class TestDeserialize:
    async def test_should_deserialize_singleline_xml(self):
        # Create xml
        xml = (
            "<Structure><Element>"
            "<Identifier>StringValue</Identifier>"
            "<DisplayName>String Value</DisplayName>"
            "<Description>String Value.</Description>"
            "<DataType><Basic>String</Basic></DataType>"
            "</Element><Element>"
            "<Identifier>IntegerValue</Identifier>"
            "<DisplayName>Integer Value</DisplayName>"
            "<Description>Integer Value.</Description>"
            "<DataType><Basic>Integer</Basic></DataType>"
            "</Element></Structure>"
        )

        # Deserialize
        data_type = Deserializer.deserialize(xml, Structure.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Structure)
        assert data_type.elements == {
            "StringValue": Element(
                identifier="StringValue",
                display_name="String Value",
                description="String Value.",
                data_type=String,
            ),
            "IntegerValue": Element(
                identifier="IntegerValue",
                display_name="Integer Value",
                description="Integer Value.",
                data_type=Integer,
            ),
        }

    async def test_should_deserialize_multiline_xml(self):
        # Create xml
        xml = """
        <Structure>
          <Element>
            <Identifier>StringValue</Identifier>
            <DisplayName>String Value</DisplayName>
            <Description>String Value.</Description>
            <DataType>
              <Basic>String</Basic>
            </DataType>
          </Element>
          <Element>
            <Identifier>IntegerValue</Identifier>
            <DisplayName>Integer Value</DisplayName>
            <Description>Integer Value.</Description>
            <DataType>
              <Basic>Integer</Basic>
            </DataType>
          </Element>
        </Structure>
        """

        # Deserialize
        data_type = Deserializer.deserialize(xml, Structure.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Structure)
        assert data_type.elements == {
            "StringValue": Element(
                identifier="StringValue",
                display_name="String Value",
                description="String Value.",
                data_type=String,
            ),
            "IntegerValue": Element(
                identifier="IntegerValue",
                display_name="Integer Value",
                description="Integer Value.",
                data_type=Integer,
            ),
        }

    async def test_should_deserialize_long_description(self):
        # Create xml
        xml = """
        <Structure>
          <Element>
            <Identifier>StringValue</Identifier>
            <DisplayName>String Value</DisplayName>
            <Description>
              Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor
              invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et
              accusam et justo duo dolores et ea rebum.
            </Description>
            <DataType>
              <Basic>String</Basic>
            </DataType>
          </Element>
        </Structure>
        """

        # Deserialize
        data_type = Deserializer.deserialize(xml, Structure.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Structure)
        assert data_type.elements == {
            "StringValue": Element(
                identifier="StringValue",
                display_name="String Value",
                description=(
                    "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam "
                    "nonumy eirmod tempor\ninvidunt ut labore et dolore magna aliquyam "
                    "erat, sed diam voluptua. At vero eos et\naccusam et justo duo "
                    "dolores et ea rebum."
                ),
                data_type=String,
            ),
        }

    async def test_should_raise_on_unexpected_characters(self):
        # Create xml
        xml = "<Structure>Hello, World!</Structure>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape("Expected start element with name 'Element', received characters '['Hello, World!']'."),
        ):
            Deserializer.deserialize(xml, Structure.deserialize)

    async def test_should_raise_on_unexpected_start_element(self):
        # Create xml
        xml = "<Structure><Basic>String</Basic></Structure>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape("Expected start element with name 'Element', received start element with name 'Basic'."),
        ):
            Deserializer.deserialize(xml, Structure.deserialize)

    async def test_should_raise_on_missing_elements(self):
        # Create xml
        xml = "<Structure></Structure>"

        # Deserialize
        with pytest.raises(
            ParseError, match=re.escape("Expected at least one 'Element' element inside the 'Structure' element.")
        ):
            Deserializer.deserialize(xml, Structure.deserialize)

    async def test_should_raise_on_invalid_identifier(self):
        # Create xml
        xml = (
            "<Structure><Element>"
            "<Identifier>Hello, World!</Identifier>"
            "<DisplayName>String Value</DisplayName>"
            "<Description>String Value.</Description>"
            "<DataType><Basic>String</Basic></DataType>"
            "</Element></Structure>"
        )

        # Deserialize
        with pytest.raises(
            ParseError, match=re.escape("Identifier may only contain letters and digits, received 'Hello, World!'.")
        ):
            Deserializer.deserialize(xml, Structure.deserialize)

    async def test_should_raise_on_invalid_display_type(self):
        # Create xml
        xml = (
            "<Structure><Element>"
            "<Identifier>StringValue</Identifier>"
            f"<DisplayName>{'a' * 256}</DisplayName>"
            "<Description>String Value.</Description>"
            "<DataType><Basic>String</Basic></DataType>"
            "</Element></Structure>"
        )

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape(
                "Display name must not exceed 255 characters in length, received "
                "'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'."
            ),
        ):
            Deserializer.deserialize(xml, Structure.deserialize)

    async def test_should_raise_on_invalid_data_type(self):
        # Create xml
        xml = (
            "<Structure><Element>"
            "<Identifier>StringValue</Identifier>"
            "<DisplayName>String Value</DisplayName>"
            "<Description>String Value.</Description>"
            "<DataType><Basic>Complex</Basic></DataType>"
            "</Element></Structure>"
        )

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Expected basic type value, received 'Complex'.")):
            Deserializer.deserialize(xml, Structure.deserialize)


class TestEquality:
    def test_should_be_true_on_equal_structures(self):
        # Create data type
        data_type_0 = Structure.create(
            {
                "a": Element(identifier="A", display_name="A", data_type=String),
                "b": Element(identifier="B", display_name="B", data_type=Integer),
            }
        )({"a": String("Hello, World!"), "b": Integer(42)})
        data_type_1 = Structure.create(
            {
                "a": Element(identifier="A", display_name="A", data_type=String),
                "b": Element(identifier="B", display_name="B", data_type=Integer),
            }
        )({"a": String("Hello, World!"), "b": Integer(42)})

        # Compare equality
        assert data_type_0 == data_type_1

    def test_should_be_false_on_unequal_type(self):
        # Create data type
        data_type_0 = Structure.create(
            {
                "a": Element(identifier="A", display_name="A", data_type=String),
                "b": Element(identifier="B", display_name="B", data_type=Integer),
            }
        )({})
        data_type_1 = Structure.create(
            {
                "a": Element(identifier="A", display_name="A", data_type=String),
                "b": Element(identifier="B", display_name="B", data_type=Real),
            }
        )({})

        # Compare equality
        assert data_type_0 != data_type_1

    def test_should_be_false_on_unequal_value(self):
        # Create data type
        data_type_0 = Structure.create(
            {
                "a": Element(identifier="A", display_name="A", data_type=String),
                "b": Element(identifier="B", display_name="B", data_type=Integer),
            }
        )({"a": String("Hello"), "b": Integer(42)})
        data_type_1 = Structure.create(
            {
                "a": Element(identifier="A", display_name="A", data_type=String),
                "b": Element(identifier="B", display_name="B", data_type=Integer),
            }
        )({"a": String("World"), "b": Integer(42)})

        # Compare equality
        assert data_type_0 != data_type_1

    def test_should_be_false_on_non_structure(self):
        # Create data type
        data_type = Structure.create(
            {
                "a": Element(identifier="A", display_name="A", data_type=String),
                "b": Element(identifier="B", display_name="B", data_type=Integer),
            }
        )({"a": String("Hello"), "b": Integer(42)})

        # Compare equality
        assert data_type != unittest.mock.Mock()
