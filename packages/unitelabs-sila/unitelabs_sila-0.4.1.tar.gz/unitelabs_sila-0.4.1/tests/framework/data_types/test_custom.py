import functools
import re
import textwrap
import unittest.mock

import pytest
import typing_extensions as typing

from sila.framework.common.feature import Feature
from sila.framework.constraints.minimal_length import MinimalLength
from sila.framework.data_types.any import Any
from sila.framework.data_types.constrained import Constrained
from sila.framework.data_types.convertable import Native
from sila.framework.data_types.custom import Custom
from sila.framework.data_types.element import Element
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.list import List
from sila.framework.data_types.real import Real
from sila.framework.data_types.string import String
from sila.framework.data_types.structure import Structure
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError
from sila.framework.fdl.serializer import Serializer
from sila.framework.protobuf.decode_error import DecodeError

MyStructure = Structure.create(
    elements={
        "parameter_a": Element(identifier="ParameterA", display_name="Parameter A", data_type=String),
        "parameter_b": Element(identifier="ParameterB", display_name="Parameter B", data_type=Integer),
    }
)

NATIVE_TEST_CASES = [
    pytest.param(
        Custom.create(identifier="Custom", display_name="Custom", data_type=String)(value=String("Hello, World!")),
        "Hello, World!",
        id='"Hello, World!"',
    ),
]
ENCODE_TEST_CASES = [
    pytest.param(
        Custom.create(identifier="Custom", display_name="Custom", data_type=String)(value=String("Hello, World!")),
        b"\x0a\x0f\x0a\x0dHello, World!",
        id='1: { 1: {"Hello, World!"} }',
    ),
    pytest.param(
        Custom.create(
            identifier="Custom",
            display_name="Custom",
            data_type=MyStructure,
        )(value=MyStructure({"parameter_a": String("Hello, World!"), "parameter_b": Integer(42)})),
        b"\x0a\x15\x0a\x0f\x0a\x0dHello, World!\x12\x02\x08\x2a",
        id='1: { 1: {"Hello, World!"}, 2: 42 }',
    ),
    pytest.param(
        Custom.create(identifier="Custom", display_name="Custom", data_type=List.create(Real))(
            value=List.create(Real)([Real(1.1), Real(2.2), Real(3.3)])
        ),
        b"\x0a\x09\x09\x9a\x99\x99\x99\x99\x99\xf1\x3f\x0a\x09\x09\x9a\x99\x99\x99\x99\x99\x01\x40\x0a\x09\x09\x66\x66\x66\x66\x66\x66\x0a\x40",
        id="1: { 1: 1.1 }, 1: { 1: 2.2 }, 1: { 1: 2.2 }",
    ),
    pytest.param(
        Custom.create(
            identifier="Custom",
            display_name="Custom",
            data_type=List.create(Constrained.create(String, [MinimalLength(0)])),
        )(
            value=List.create(Constrained.create(String, [MinimalLength(0)]))(
                [
                    Constrained.create(String, [MinimalLength(0)])(String("Hello")),
                    Constrained.create(String, [MinimalLength(0)])(String("World")),
                ]
            )
        ),
        b"\x0a\x07\x0a\x05Hello\x0a\x07\x0a\x05World",
        id='1: { 1: {"Hello"} }, 1: { 1: {"World"} }',
    ),
    pytest.param(
        Custom.create(
            identifier="Custom",
            display_name="Custom",
            data_type=Constrained.create(List.create(String), [MinimalLength(0)]),
        )(
            value=Constrained.create(List.create(String), [MinimalLength(0)])(
                List.create(String)(
                    [
                        String("Hello"),
                        String("World"),
                    ]
                )
            )
        ),
        b"\x0a\x07\x0a\x05Hello\x0a\x07\x0a\x05World",
        id='1: { 1: {"Hello"} }, 1: { 1: {"World"} }',
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        Custom.create(identifier="Custom", display_name="Custom", data_type=String)(value=String("Hello, World!")),
        b"\n\x0f\n\rHello, World!\x10\x00",
        id='1: { 1: {"Hello, World!"} }, 2: 0',
    ),
    pytest.param(
        Custom.create(identifier="Custom", display_name="Custom", data_type=String)(value=String("Hello, World!")),
        b"\x10\x00\n\x0f\n\rHello, World!",
        id='2: 0, 1: { 1: {"Hello, World!"} }',
    ),
    pytest.param(
        Custom.create(
            identifier="Custom",
            display_name="Custom",
            data_type=MyStructure,
        )(value=MyStructure({"parameter_a": String("Hello, World!"), "parameter_b": Integer(42)})),
        b"\x0a\x15\x18\x00\x12\x02\x08\x2a\x0a\x0f\x0a\x0dHello, World!",
        id='1: { 3: 0, 2: 42, 1: {"Hello, World!"} }',
    ),
]


class TestFullyQualifiedIdentifier:
    async def test_should_raise_on_missing_feature(self):
        # Create custom
        data_type = Custom.create(identifier="Custom", display_name="Custom")

        # Get fully qualified identifier
        with pytest.raises(
            RuntimeError,
            match=re.escape(
                "Unable to get fully qualified identifier for Custom Data Type 'Custom' without feature association."
            ),
        ):
            assert data_type.fully_qualified_identifier() is None

    async def test_should_get_fully_qualified_identifier(self):
        # Create metadata
        feature = Feature(identifier="SiLAService", display_name="SiLAService")
        data_type = Custom.create(identifier="Custom", display_name="Custom", feature=feature)

        # Get fully qualified identifier
        assert data_type.fully_qualified_identifier() == "org.silastandard/none/SiLAService/v1/DataType/Custom"


class TestInitFromNative:
    async def test_should_accept_no_value(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Custom.from_native(context)

        # Assert that the method returns the correct value
        assert data_type == Custom()

    @pytest.mark.parametrize(("expected", "native"), NATIVE_TEST_CASES)
    async def test_should_accept_native(self, expected: Custom, native: Native):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await type(expected).from_native(context, native)

        # Assert that the method returns the correct value
        assert data_type == expected

    async def test_should_raise_on_invalid_type(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = Custom.create(identifier="Custom", display_name="Custom", data_type=String)

        with pytest.raises(TypeError, match=re.escape("Expected value of type 'str', received 'int'.")):
            await data_type.from_native(context, 0)


class TestConvertToNative:
    @pytest.mark.parametrize(("data_type", "native"), NATIVE_TEST_CASES)
    async def test_should_convert_to_native(self, data_type: Custom, native: typing.Any):
        # Convert data type
        context = unittest.mock.Mock()
        assert await data_type.to_native(context) == native

    async def test_should_raise_on_invalid_type(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = Custom.create(identifier="Custom", display_name="Custom", data_type=String)

        # Convert data type
        with pytest.raises(TypeError, match=re.escape("Expected value of type 'String', received 'Integer'.")):
            await data_type(value=Integer(42)).to_native(context)


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode data type
        message = Custom.decode(b"")

        # Assert that the method returns the correct value
        assert message == Custom()

    @pytest.mark.parametrize(("data_type", "reader"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, data_type: Custom, reader: bytes):
        # Decode data type
        message = data_type.decode(reader)

        # Assert that the method returns the correct value
        assert message == data_type

    async def test_should_decode_multiple_fields(self):
        # Create data type
        data_type = Custom.create(identifier="Custom", display_name="Custom", data_type=String)

        # Decode message
        message = data_type.decode(b"\x0a\x07\x0a\x05Hello\x0a\x07\x0a\x05World")

        # Assert that the method returns the correct value
        assert message == data_type(value=String("World"))

    async def test_should_decode_limited_buffer(self):
        # Create data type
        data_type = Custom.create(identifier="Custom", display_name="Custom", data_type=String)

        # Decode data type
        message = data_type.decode(b"\x0a\x07\x0a\x05Hello\x0a\x07\x0a\x05World", 9)

        # Assert that the method returns the correct value
        assert message == data_type(value=String("Hello"))

    async def test_should_raise_on_decode_error(self):
        # Create data type
        data_type = Custom.create(identifier="Custom", display_name="Custom", data_type=String)

        # Decode data type
        with pytest.raises(DecodeError, match=re.escape("Expected wire type 'LEN', received 'VARINT'.")) as error:
            data_type.decode(b"\x0a\x07\x0a\x05Hello\x0a\x07\x08\x01")

        assert error.value.offset == 12
        assert error.value.path == ["Custom"]


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode data type
        message = Custom().encode()

        # Assert that the method returns the correct value
        assert message == (
            b'\x0a\xaf\x01\x0a\xac\x01<DataType xmlns="http://www.sila-standard.org"><Constrained><DataType><Basic>String</Basic></DataType><Constraints><Length>0</Length></Constraints></Constrained></DataType>'
        )

    @pytest.mark.parametrize(("data_type", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, data_type: Custom, buffer: bytes):
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
        data_type = Custom.create(identifier="Custom", display_name="Custom", data_type=String)(String())
        message = data_type.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer


class TestCreate:
    def test_should_create_custom(self):
        # Create data type
        data_type = Custom.create(identifier="Custom", display_name="Custom")

        # Assert that the method returns the correct value
        assert issubclass(data_type, Custom)
        assert data_type.__name__ == "Custom"
        assert data_type.identifier == "Custom"
        assert data_type.display_name == "Custom"
        assert data_type.description == ""
        assert data_type.data_type == Any

    def test_should_accept_identifier(self):
        # Create data type
        data_type = Custom.create(
            identifier="CustomIdentifier",
            display_name="Custom Identifier",
        )

        # Assert that the method returns the correct value
        assert data_type.identifier == "CustomIdentifier"

    def test_should_accept_display_name(self):
        # Create data type
        data_type = Custom.create(
            identifier="CustomIdentifier",
            display_name="Custom Identifier",
        )

        # Assert that the method returns the correct value
        assert data_type.display_name == "Custom Identifier"

    def test_should_accept_description(self):
        # Create data type
        data_type = Custom.create(
            identifier="CustomIdentifier",
            display_name="Custom Identifier",
            description="Custom Identifier.",
        )

        # Assert that the method returns the correct value
        assert data_type.description == "Custom Identifier."

    def test_should_accept_data_type(self):
        # Create data type
        data_type = Custom.create(
            identifier="CustomIdentifier",
            display_name="Custom Identifier",
            data_type=String,
        )

        # Assert that the method returns the correct value
        assert data_type.data_type == String

    def test_should_accept_feature(self):
        # Create data type
        feature = Feature(identifier="Feature", display_name="Feature")
        data_type = Custom.create(
            identifier="CustomIdentifier",
            display_name="Custom Identifier",
            feature=feature,
        )

        # Assert that the method returns the correct value
        assert data_type.feature == feature

    def test_should_accept_name(self):
        # Create data type
        data_type = Custom.create(
            identifier="CustomIdentifier",
            display_name="Custom Identifier",
            name="CustomName",
        )

        # Assert that the method returns the correct value
        assert data_type.__name__ == "CustomName"


class TestSerialize:
    async def test_should_serialize_singleline_xml(self):
        # Create data type
        data_type = Custom.create(
            identifier="CustomDataType",
            display_name="Custom Data Type",
            description="Custom Data Type.",
            data_type=String,
        )

        # Serialize
        xml = Serializer.serialize(data_type.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == "<DataType><DataTypeIdentifier>CustomDataType</DataTypeIdentifier></DataType>"

    async def test_should_serialize_multiline_xml(self):
        # Create data type
        data_type = Custom.create(
            identifier="CustomDataType",
            display_name="Custom Data Type",
            description="Custom Data Type.",
            data_type=String,
        )

        # Serialize
        xml = Serializer.serialize(data_type.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <DataType>
              <DataTypeIdentifier>CustomDataType</DataTypeIdentifier>
            </DataType>
            """
        )

    async def test_should_serialize_singleline_definition_xml(self):
        # Create data type
        data_type = Custom.create(
            identifier="CustomDataType",
            display_name="Custom Data Type",
            description="Custom Data Type.",
            data_type=String,
        )

        # Serialize
        serialize = functools.partial(data_type.serialize, definition=True)
        xml = Serializer.serialize(serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == (
            "<DataTypeDefinition>"
            "<Identifier>CustomDataType</Identifier>"
            "<DisplayName>Custom Data Type</DisplayName>"
            "<Description>Custom Data Type.</Description>"
            "<DataType><Basic>String</Basic></DataType>"
            "</DataTypeDefinition>"
        )

    async def test_should_serialize_multiline_definition_xml(self):
        # Create data type
        data_type = Custom.create(
            identifier="CustomDataType",
            display_name="Custom Data Type",
            description="Custom Data Type.",
            data_type=String,
        )

        # Serialize
        serialize = functools.partial(data_type.serialize, definition=True)
        xml = Serializer.serialize(serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <DataTypeDefinition>
              <Identifier>CustomDataType</Identifier>
              <DisplayName>Custom Data Type</DisplayName>
              <Description>Custom Data Type.</Description>
              <DataType>
                <Basic>String</Basic>
              </DataType>
            </DataTypeDefinition>
            """
        )


class TestDeserialize:
    async def test_should_deserialize_singleline_xml(self):
        # Create xml
        xml = "<DataTypeIdentifier>CustomDataType</DataTypeIdentifier>"

        # Deserialize
        data_type = Deserializer.deserialize(xml, Custom.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Custom)
        assert data_type.identifier == "CustomDataType"
        assert data_type.display_name == "CustomDataType"

    async def test_should_deserialize_multiline_xml(self):
        # Create xml
        xml = """
        <DataTypeIdentifier>
          CustomDataType
        </DataTypeIdentifier>
        """

        # Deserialize
        data_type = Deserializer.deserialize(xml, Custom.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Custom)
        assert data_type.identifier == "CustomDataType"
        assert data_type.display_name == "CustomDataType"

    async def test_should_deserialize_singleline_definition_xml(self):
        # Create xml
        xml = (
            "<DataTypeDefinition>"
            "<Identifier>CustomDataType</Identifier>"
            "<DisplayName>Custom Data Type</DisplayName>"
            "<Description>Custom Data Type.</Description>"
            "<DataType><Basic>String</Basic></DataType>"
            "</DataTypeDefinition>"
        )

        # Deserialize
        data_type = Deserializer.deserialize(xml, Custom.deserialize, {"definition": True})

        # Assert that the method returns the correct value
        assert issubclass(data_type, Custom)
        assert data_type.identifier == "CustomDataType"
        assert data_type.display_name == "Custom Data Type"
        assert data_type.description == "Custom Data Type."
        assert data_type.data_type == String

    async def test_should_deserialize_multiline_definition_xml(self):
        # Create xml
        xml = """
        <DataTypeDefinition>
          <Identifier>CustomDataType</Identifier>
          <DisplayName>Custom Data Type</DisplayName>
          <Description>Custom Data Type.</Description>
          <DataType>
            <Basic>String</Basic>
          </DataType>
        </DataTypeDefinition>
        """

        # Deserialize
        data_type = Deserializer.deserialize(xml, Custom.deserialize, {"definition": True})

        # Assert that the method returns the correct value
        assert issubclass(data_type, Custom)
        assert data_type.identifier == "CustomDataType"
        assert data_type.display_name == "Custom Data Type"
        assert data_type.description == "Custom Data Type."
        assert data_type.data_type == String

    async def test_should_extend_existing_custom(self):
        # Create xml
        custom = Custom.create(identifier="CustomDataType", display_name="CustomDataType")
        xml = """
        <DataTypeDefinition>
          <Identifier>CustomDataType</Identifier>
          <DisplayName>Custom Data Type</DisplayName>
          <Description>Custom Data Type.</Description>
          <DataType>
            <Basic>String</Basic>
          </DataType>
        </DataTypeDefinition>
        """

        # Deserialize
        data_type = Deserializer.deserialize(
            xml, Custom.deserialize, {"definition": True, "data_type_definitions": {"CustomDataType": custom}}
        )

        # Assert that the method returns the correct value
        assert custom == data_type
        assert custom.identifier == "CustomDataType"
        assert custom.display_name == "Custom Data Type"
        assert custom.description == "Custom Data Type."
        assert custom.data_type == String

    async def test_should_raise_on_invalid_identifier(self):
        # Create xml
        xml = "<DataTypeIdentifier>Hello, World!</DataTypeIdentifier>"

        # Deserialize
        with pytest.raises(
            ParseError, match=re.escape("Identifier may only contain letters and digits, received 'Hello, World!'.")
        ):
            Deserializer.deserialize(xml, Custom.deserialize)


class TestAddToFeature:
    async def test_should_add_to_feature(self):
        # Create property
        feature = Feature(identifier="SiLAService", display_name="SiLAService")
        data_type = Custom.create(identifier="CustomIdentifier", display_name="Custom Identifier")

        # Add to feature
        data_type.add_to_feature(feature)

        # Assert that the method returns the correct value
        assert feature.data_type_definitions["CustomIdentifier"] == data_type


class TestEquality:
    def test_should_be_true_on_equal_constraineds(self):
        # Create data type
        data_type_0 = Custom.create(identifier="Custom", display_name="Custom", data_type=String)(String("Hello"))
        data_type_1 = Custom.create(identifier="Custom", display_name="Custom", data_type=String)(String("Hello"))

        # Compare equality
        assert data_type_0 == data_type_1

    def test_should_be_false_on_unequal_type(self):
        # Create data type
        data_type_0 = Custom.create(identifier="Custom", display_name="Custom", data_type=String)()
        data_type_1 = Custom.create(identifier="Custom", display_name="Custom", data_type=Integer)()

        # Compare equality
        assert data_type_0 != data_type_1

    def test_should_be_false_on_unequal_value(self):
        # Create data type
        data_type_0 = Custom.create(identifier="Custom", display_name="Custom", data_type=String)(String("Hello"))
        data_type_1 = Custom.create(identifier="Custom", display_name="Custom", data_type=String)(String("World"))

        # Compare equality
        assert data_type_0 != data_type_1

    def test_should_be_false_on_non_custom(self):
        # Create data type
        data_type = Custom.create(identifier="Custom", display_name="Custom", data_type=String)(String("Hello"))

        # Compare equality
        assert data_type != unittest.mock.Mock()
