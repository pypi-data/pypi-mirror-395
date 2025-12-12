import re
import textwrap
import unittest.mock

import pytest
import typing_extensions as typing

from sila.framework.constraints.allowed_types import AllowedTypes
from sila.framework.constraints.content_type import ContentType
from sila.framework.constraints.element_count import ElementCount
from sila.framework.constraints.fully_qualified_identifier import FullyQualifiedIdentifier
from sila.framework.constraints.length import Length
from sila.framework.constraints.maximal_element_count import MaximalElementCount
from sila.framework.constraints.maximal_exclusive import MaximalExclusive
from sila.framework.constraints.maximal_inclusive import MaximalInclusive
from sila.framework.constraints.maximal_length import MaximalLength
from sila.framework.constraints.minimal_element_count import MinimalElementCount
from sila.framework.constraints.minimal_exclusive import MinimalExclusive
from sila.framework.constraints.minimal_inclusive import MinimalInclusive
from sila.framework.constraints.minimal_length import MinimalLength
from sila.framework.constraints.pattern import Pattern
from sila.framework.constraints.schema import Schema
from sila.framework.constraints.set import Set
from sila.framework.constraints.unit import Unit
from sila.framework.data_types.any import Any
from sila.framework.data_types.binary import Binary
from sila.framework.data_types.constrained import Constrained
from sila.framework.data_types.convertable import Native
from sila.framework.data_types.date import Date
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.list import List
from sila.framework.data_types.real import Real
from sila.framework.data_types.string import String
from sila.framework.data_types.timezone import Timezone
from sila.framework.data_types.void import Void
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError
from sila.framework.fdl.serializer import Serializer

StringList = List.create(String)

NATIVE_TEST_CASES = [
    pytest.param(
        Constrained.create(String, [MaximalLength(5)])(value=String("Hello")),
        "Hello",
        id='"Hello"',
    ),
]
ENCODE_TEST_CASES = [
    pytest.param(
        Constrained.create(String)(value=String("Hello, World!")), b"\x0a\x0dHello, World!", id='1: {"Hello, World!"}'
    ),
    pytest.param(Constrained.create(Integer)(value=Integer(42)), b"\x08\x2a", id="1: 42"),
    pytest.param(
        Constrained.create(Real)(value=Real(3.141592653589793)),
        b"\x09\x18\x2d\x44\x54\xfb\x21\x09\x40",
        id="1: 3.141592653589793",
    ),
    pytest.param(
        Constrained.create(Binary)(value=Binary(b"Hello, World!")), b"\x0a\x0dHello, World!", id='1: {"Hello, World!"}'
    ),
    pytest.param(
        Constrained.create(Date)(value=Date(year=2022, month=8, day=5, timezone=Timezone(hours=12, minutes=34))),
        b"\x08\x05\x10\x08\x18\xe6\x0f\x22\x04\x08\x0c\x10\x22",
        id="1: 5, 2: 8, 3: 2022, 4: { 1: 12, 2: 34 }",
    ),
    pytest.param(
        Constrained.create(StringList)(value=StringList(value=[String("SiLA 2"), String("is"), String("awesome!")])),
        b"\x0a\x08\x0a\x06SiLA 2\x0a\x04\x0a\x02is\x0a\x0a\x0a\x08awesome!",
        id='1: { 1: {"SiLA 2"} }, 1: { 1: {"is"} }, 1: { 1: {"awesome!"} }',
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        Constrained.create(String)(value=String("Hello, World!")),
        b"\x0a\x0dHello, World!\x10\x00",
        id='1: {"Hello, World!"}, 2: 0',
    ),
    pytest.param(Constrained.create(Integer)(value=Integer(42)), b"\x10\x00\x08*", id="2: 0, 1: 42"),
    pytest.param(
        Constrained.create(StringList)(value=StringList(value=[String("SiLA 2"), String("is"), String("awesome!")])),
        b"\x0a\x08\x0a\x06SiLA 2\x10\x00\x0a\x04\x0a\x02is\x0a\x0a\x0a\x08awesome!",
        id='1: { 1: {"SiLA 2"} }, 2: 0, 1: { 1: {"is"} }, 1: { 1: {"awesome!"} }',
    ),
    pytest.param(
        Constrained.create(StringList)(value=StringList(value=[String("SiLA 2"), String("is"), String("awesome!")])),
        b"\x0a\x08\x0a\x06SiLA 2\x0a\x04\x0a\x02is\x10\x00\x0a\x0a\x0a\x08awesome!",
        id='1: { 1: {"SiLA 2"} }, 1: { 1: {"is"} }, 2: 0, 1: { 1: {"awesome!"} }',
    ),
    pytest.param(
        Constrained.create(StringList)(value=StringList(value=[String("SiLA 2"), String("is"), String("awesome!")])),
        b"\x0a\x08\x0a\x06SiLA 2\x0a\x04\x0a\x02is\x0a\x0a\x0a\x08awesome!\x10\x00",
        id='1: { 1: {"SiLA 2"} }, 1: { 1: {"is"} }, 1: { 1: {"awesome!"} }, 2: 0',
    ),
]


class TestInitFromNative:
    async def test_should_accept_no_value(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Constrained.from_native(context)

        # Assert that the method returns the correct value
        assert data_type == Constrained()

    @pytest.mark.parametrize(("expected", "native"), NATIVE_TEST_CASES)
    async def test_should_accept_native(self, expected: Constrained, native: Native):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await type(expected).from_native(context, native)

        # Assert that the method returns the correct value
        assert data_type == expected

    async def test_should_raise_on_invalid_type(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = Constrained.create(String, [MaximalLength(5)])

        with pytest.raises(TypeError, match=re.escape("Expected value of type 'str', received 'int'.")):
            await data_type.from_native(context, 0)

    async def test_should_raise_on_invalid_value(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = Constrained.create(String, [MaximalLength(5)])

        with pytest.raises(ValueError, match=re.escape("Expected value with maximal length '5', received '6'.")):
            await data_type.from_native(context, "123456")


class TestConvertToNative:
    @pytest.mark.parametrize(("data_type", "native"), NATIVE_TEST_CASES)
    async def test_should_convert_to_native(self, data_type: Constrained, native: typing.Any):
        # Convert data type
        context = unittest.mock.Mock()
        assert await data_type.to_native(context) == native

    async def test_should_raise_on_invalid_type(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = Constrained.create(String, [MaximalLength(5)])

        # Convert data type
        with pytest.raises(TypeError, match=re.escape("Expected value of type 'String', received 'Integer'.")):
            await data_type(value=Integer(42)).to_native(context)

    async def test_should_raise_on_invalid_value(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = Constrained.create(String, [MaximalLength(5)])

        # Convert data type
        with pytest.raises(ValueError, match=re.escape("Expected value with maximal length '5', received '6'.")):
            await data_type(value=String("123456")).to_native(context)


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode data type
        message = Constrained.decode(b"")

        # Assert that the method returns the correct value
        assert message == Constrained()

    @pytest.mark.parametrize(("data_type", "reader"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, data_type: Constrained, reader: bytes):
        # Decode data type
        message = data_type.decode(reader)

        # Assert that the method returns the correct value
        assert message == data_type

    async def test_should_decode_multiple_fields(self):
        # Create data type
        data_type = Constrained.create(data_type=String)

        # Decode message
        message = data_type.decode(b"\x0a\x05Hello\x0a\x05World")

        # Assert that the method returns the correct value
        assert message == data_type(String(value="World"))

    async def test_should_decode_limited_buffer(self):
        # Create data type
        data_type = Constrained.create(data_type=String)

        # Decode data type
        message = data_type.decode(b"\x0a\x05Hello\x0a\x05World", 7)

        # Assert that the method returns the correct value
        assert message == data_type(String(value="Hello"))


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode data type
        message = Constrained().encode()

        # Assert that the method returns the correct value
        assert message == (
            b'\x0a\xac\x01<DataType xmlns="http://www.sila-standard.org"><Constrained><DataType><Basic>String</Basic></DataType><Constraints><Length>0</Length></Constraints></Constrained></DataType>'
        )

    @pytest.mark.parametrize(("data_type", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, data_type: Constrained, buffer: bytes):
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
        data_type = Constrained.create(String)()
        message = data_type.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer


class TestCreate:
    def test_should_create_constrained(self):
        # Create data type
        data_type = Constrained.create()

        # Assert that the method returns the correct value
        assert issubclass(data_type, Constrained)
        assert data_type.__name__ == "Constrained"
        assert data_type.data_type == Any
        assert not data_type.constraints

    def test_should_accept_data_type(self):
        # Create constrained
        data_type = Constrained.create(data_type=String)

        # Assert that the method returns the correct value
        assert data_type.data_type == String

    def test_should_accept_constraints(self):
        # Create constrained
        data_type = Constrained.create(constraints=[MaximalLength(5)])

        # Assert that the method returns the correct value
        assert data_type.constraints == [MaximalLength(5)]

    def test_should_accept_name(self):
        # Create constrained
        data_type = Constrained.create(name="ConstrainedName")

        # Assert that the method returns the correct value
        assert data_type.__name__ == "ConstrainedName"


class TestSerialize:
    async def test_should_serialize_singleline_xml(self):
        # Create data type
        data_type = Constrained.create(data_type=String, constraints=[MaximalLength(5)])

        # Serialize
        xml = Serializer.serialize(data_type.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == (
            "<DataType><Constrained>"
            "<DataType><Basic>String</Basic></DataType>"
            "<Constraints><MaximalLength>5</MaximalLength></Constraints>"
            "</Constrained></DataType>"
        )

    async def test_should_serialize_multiline_xml(self):
        # Create data type
        data_type = Constrained.create(data_type=Integer, constraints=[MaximalLength(5)])

        # Serialize
        xml = Serializer.serialize(data_type.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <DataType>
              <Constrained>
                <DataType>
                  <Basic>Integer</Basic>
                </DataType>
                <Constraints>
                  <MaximalLength>5</MaximalLength>
                </Constraints>
              </Constrained>
            </DataType>
            """
        )


class TestDeserialize:
    async def test_should_deserialize_singleline_xml(self):
        # Create xml
        xml = (
            "<Constrained><DataType><Basic>String</Basic></DataType>"
            "<Constraints><MaximalLength>5</MaximalLength></Constraints></Constrained>"
        )

        # Deserialize
        data_type = Deserializer.deserialize(xml, Constrained.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Constrained)
        assert data_type.data_type == String
        assert data_type.constraints == [MaximalLength(5)]

    async def test_should_deserialize_multiline_xml(self):
        # Create xml
        xml = """
        <Constrained>
          <DataType>
            <Basic>String</Basic>
          </DataType>
          <Constraints>
            <MaximalLength>5</MaximalLength>
          </Constraints>
        </Constrained>
        """

        # Deserialize
        data_type = Deserializer.deserialize(xml, Constrained.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Constrained)
        assert data_type.data_type == String
        assert data_type.constraints == [MaximalLength(5)]

    async def test_should_deserialize_void(self):
        # Create xml
        xml = (
            "<Constrained><DataType><Basic>String</Basic></DataType><Constraints>"
            "<Length>0</Length>"
            "</Constraints></Constrained>"
        )

        # Deserialize
        data_type = Deserializer.deserialize(xml, Constrained.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Void)

    async def test_should_deserialize_length(self):
        # Create xml
        xml = (
            "<Constrained><DataType><Basic>String</Basic></DataType><Constraints>"
            "<Length>10</Length>"
            "</Constraints></Constrained>"
        )

        # Deserialize
        data_type = Deserializer.deserialize(xml, Constrained.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Constrained)
        assert data_type.data_type == String
        assert data_type.constraints == [Length(10)]

    async def test_should_deserialize_minimal_length(self):
        # Create xml
        xml = (
            "<Constrained><DataType><Basic>String</Basic></DataType><Constraints>"
            "<MinimalLength>5</MinimalLength>"
            "</Constraints></Constrained>"
        )

        # Deserialize
        data_type = Deserializer.deserialize(xml, Constrained.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Constrained)
        assert data_type.data_type == String
        assert data_type.constraints == [MinimalLength(5)]

    async def test_should_deserialize_maximal_length(self):
        # Create xml
        xml = (
            "<Constrained><DataType><Basic>String</Basic></DataType><Constraints>"
            "<MaximalLength>5</MaximalLength>"
            "</Constraints></Constrained>"
        )

        # Deserialize
        data_type = Deserializer.deserialize(xml, Constrained.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Constrained)
        assert data_type.data_type == String
        assert data_type.constraints == [MaximalLength(5)]

    async def test_should_deserialize_set(self):
        # Create xml
        xml = (
            "<Constrained><DataType><Basic>String</Basic></DataType><Constraints>"
            "<Set><Value>First option</Value><Value>Second option</Value><Value>Third option</Value></Set>"
            "</Constraints></Constrained>"
        )

        # Deserialize
        data_type = Deserializer.deserialize(xml, Constrained.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Constrained)
        assert data_type.data_type == String
        assert data_type.constraints == [Set([String("First option"), String("Second option"), String("Third option")])]

    async def test_should_deserialize_pattern(self):
        # Create xml
        xml = (
            "<Constrained><DataType><Basic>String</Basic></DataType><Constraints>"
            r"<Pattern>[0-9]{2}/[0-9]{2}/[0-9]{4}</Pattern>"
            "</Constraints></Constrained>"
        )

        # Deserialize
        data_type = Deserializer.deserialize(xml, Constrained.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Constrained)
        assert data_type.data_type == String
        assert data_type.constraints == [Pattern(r"[0-9]{2}/[0-9]{2}/[0-9]{4}")]

    async def test_should_deserialize_maximal_exclusive(self):
        # Create xml
        xml = (
            "<Constrained><DataType><Basic>Integer</Basic></DataType><Constraints>"
            "<MaximalExclusive>11</MaximalExclusive>"
            "</Constraints></Constrained>"
        )

        # Deserialize
        data_type = Deserializer.deserialize(xml, Constrained.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Constrained)
        assert data_type.data_type == Integer
        assert data_type.constraints == [MaximalExclusive(Integer(11))]

    async def test_should_deserialize_maximal_inclusive(self):
        # Create xml
        xml = (
            "<Constrained><DataType><Basic>Integer</Basic></DataType><Constraints>"
            "<MaximalInclusive>10</MaximalInclusive>"
            "</Constraints></Constrained>"
        )

        # Deserialize
        data_type = Deserializer.deserialize(xml, Constrained.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Constrained)
        assert data_type.data_type == Integer
        assert data_type.constraints == [MaximalInclusive(Integer(10))]

    async def test_should_deserialize_minimal_exclusive(self):
        # Create xml
        xml = (
            "<Constrained><DataType><Basic>Integer</Basic></DataType><Constraints>"
            "<MinimalExclusive>-1</MinimalExclusive>"
            "</Constraints></Constrained>"
        )

        # Deserialize
        data_type = Deserializer.deserialize(xml, Constrained.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Constrained)
        assert data_type.data_type == Integer
        assert data_type.constraints == [MinimalExclusive(Integer(-1))]

    async def test_should_deserialize_minimal_inclusive(self):
        # Create xml
        xml = (
            "<Constrained><DataType><Basic>Integer</Basic></DataType><Constraints>"
            "<MinimalInclusive>0</MinimalInclusive>"
            "</Constraints></Constrained>"
        )

        # Deserialize
        data_type = Deserializer.deserialize(xml, Constrained.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Constrained)
        assert data_type.data_type == Integer
        assert data_type.constraints == [MinimalInclusive(Integer(0))]

    async def test_should_deserialize_unit(self):
        # Create xml
        xml = (
            "<Constrained><DataType><Basic>Integer</Basic></DataType><Constraints>"
            "<Unit><Label>mL</Label><Factor>0.000001</Factor><Offset>0</Offset><UnitComponent><SIUnit>Meter</SIUnit><Exponent>3</Exponent></UnitComponent></Unit>"
            "</Constraints></Constrained>"
        )

        # Deserialize
        data_type = Deserializer.deserialize(xml, Constrained.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Constrained)
        assert data_type.data_type == Integer
        assert data_type.constraints == [Unit("mL", [Unit.Component("Meter", 3)], factor=0.000001)]

    async def test_should_deserialize_content_type(self):
        # Create xml
        xml = (
            "<Constrained><DataType><Basic>String</Basic></DataType><Constraints>"
            "<ContentType><Type>application</Type><Subtype>xml</Subtype></ContentType>"
            "</Constraints></Constrained>"
        )

        # Deserialize
        data_type = Deserializer.deserialize(xml, Constrained.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Constrained)
        assert data_type.data_type == String
        assert data_type.constraints == [ContentType("application", "xml")]

    async def test_should_deserialize_element_count(self):
        # Create xml
        xml = (
            "<Constrained><DataType><List><DataType><Basic>String</Basic></DataType></List></DataType><Constraints>"
            "<ElementCount>5</ElementCount>"
            "</Constraints></Constrained>"
        )

        # Deserialize
        data_type = Deserializer.deserialize(xml, Constrained.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Constrained)
        assert issubclass(data_type.data_type, List)
        assert data_type.data_type.data_type == String
        assert data_type.constraints == [ElementCount(5)]

    async def test_should_deserialize_minimal_element_count(self):
        # Create xml
        xml = (
            "<Constrained><DataType><List><DataType><Basic>String</Basic></DataType></List></DataType><Constraints>"
            "<MinimalElementCount>5</MinimalElementCount>"
            "</Constraints></Constrained>"
        )

        # Deserialize
        data_type = Deserializer.deserialize(xml, Constrained.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Constrained)
        assert issubclass(data_type.data_type, List)
        assert data_type.data_type.data_type == String
        assert data_type.constraints == [MinimalElementCount(5)]

    async def test_should_deserialize_maximal_element_count(self):
        # Create xml
        xml = (
            "<Constrained><DataType><List><DataType><Basic>String</Basic></DataType></List></DataType><Constraints>"
            "<MaximalElementCount>5</MaximalElementCount>"
            "</Constraints></Constrained>"
        )

        # Deserialize
        data_type = Deserializer.deserialize(xml, Constrained.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Constrained)
        assert issubclass(data_type.data_type, List)
        assert data_type.data_type.data_type == String
        assert data_type.constraints == [MaximalElementCount(5)]

    async def test_should_deserialize_fully_qualified_identifier(self):
        # Create xml
        xml = (
            "<Constrained><DataType><Basic>String</Basic></DataType><Constraints>"
            "<FullyQualifiedIdentifier>FeatureIdentifier</FullyQualifiedIdentifier>"
            "</Constraints></Constrained>"
        )

        # Deserialize
        data_type = Deserializer.deserialize(xml, Constrained.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Constrained)
        assert data_type.data_type == String
        assert data_type.constraints == [FullyQualifiedIdentifier("FeatureIdentifier")]

    async def test_should_deserialize_schema(self):
        # Create xml
        xml = (
            "<Constrained><DataType><Basic>String</Basic></DataType><Constraints>"
            "<Schema><Type>Xml</Type><Url>https://gitlab.com/SiLA2/sila_base/-/raw/master/schema/FeatureDefinition.xsd</Url></Schema>"
            "</Constraints></Constrained>"
        )

        # Deserialize
        data_type = Deserializer.deserialize(xml, Constrained.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Constrained)
        assert data_type.data_type == String
        assert data_type.constraints == [
            Schema("Xml", url="https://gitlab.com/SiLA2/sila_base/-/raw/master/schema/FeatureDefinition.xsd")
        ]

    async def test_should_deserialize_allowed_types(self):
        # Create xml
        xml = (
            "<Constrained><DataType><Basic>Any</Basic></DataType><Constraints>"
            "<AllowedTypes><DataType><Basic>Integer</Basic></DataType><DataType><List><DataType><Basic>Integer</Basic></DataType></List></DataType></AllowedTypes>"
            "</Constraints></Constrained>"
        )

        # Deserialize
        data_type = Deserializer.deserialize(xml, Constrained.deserialize)

        # Assert that the method returns the correct value
        assert issubclass(data_type, Constrained)
        assert data_type.data_type == Any
        assert len(data_type.constraints) == 1
        assert isinstance(data_type.constraints[0], AllowedTypes)
        assert len(data_type.constraints[0].values) == 2
        assert issubclass(data_type.constraints[0].values[0], Integer)
        assert issubclass(data_type.constraints[0].values[1], List)
        assert issubclass(data_type.constraints[0].values[1].data_type, Integer)

    async def test_should_raise_on_invalid_data_type(self):
        # Create xml
        xml = (
            "<Constrained><DataType><Basic>Complex</Basic></DataType>"
            "<Constraints><MaximalLength>5</MaximalLength></Constraints></Constrained>"
        )

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Expected basic type value, received 'Complex'.")):
            Deserializer.deserialize(xml, Constrained.deserialize)

    async def test_should_raise_on_structure_data_type(self):
        # Create xml
        xml = (
            "<Constrained><DataType>"
            "<Structure><Element>"
            "<Identifier>StringValue</Identifier>"
            "<DisplayName>String Value</DisplayName>"
            "<Description>String Value.</Description>"
            "<DataType><Basic>String</Basic></DataType>"
            "</Element></Structure>"
            "</DataType>"
            "<Constraints><MaximalLength>5</MaximalLength></Constraints></Constrained>"
        )

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape("Expected constraint's data type to be 'BasicType' or 'List', received 'Structure'."),
        ):
            Deserializer.deserialize(xml, Constrained.deserialize)

    async def test_should_raise_on_constrained_data_type(self):
        # Create xml
        xml = (
            "<Constrained><DataType>"
            "<Constrained><DataType><Basic>String</Basic></DataType>"
            "<Constraints><MaximalLength>5</MaximalLength></Constraints></Constrained>"
            "</DataType>"
            "<Constraints><MaximalLength>5</MaximalLength></Constraints></Constrained>"
        )

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape("Expected constraint's data type to be 'BasicType' or 'List', received 'Constrained'."),
        ):
            Deserializer.deserialize(xml, Constrained.deserialize)

    async def test_should_raise_on_custom_data_type(self):
        # Create xml
        xml = (
            "<Constrained><DataType>"
            "<DataTypeIdentifier>CustomDataType</DataTypeIdentifier>"
            "</DataType>"
            "<Constraints><MaximalLength>5</MaximalLength></Constraints></Constrained>"
        )

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape("Expected constraint's data type to be 'BasicType' or 'List', received 'CustomDataType'."),
        ):
            Deserializer.deserialize(xml, Constrained.deserialize)

    async def test_should_raise_on_unexpected_characters(self):
        # Create xml
        xml = (
            "<Constrained><DataType><Basic>String</Basic></DataType>"
            "<Constraints>Hello, World!</Constraints></Constrained>"
        )

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape("Expected start element with a constraint name, received characters '['Hello, World!']'."),
        ):
            Deserializer.deserialize(xml, Constrained.deserialize)

    async def test_should_raise_on_unexpected_start_element(self):
        # Create xml
        xml = (
            "<Constrained><DataType><Basic>String</Basic></DataType>"
            "<Constraints><Value></Value></Constraints></Constrained>"
        )

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape("Expected start element with a constraint name, received start element with name 'Value'."),
        ):
            Deserializer.deserialize(xml, Constrained.deserialize)


class TestEquality:
    def test_should_be_true_on_equal_constraineds(self):
        # Create data type
        data_type_0 = Constrained.create(data_type=String, constraints=[MaximalLength(5)])(String("Hello"))
        data_type_1 = Constrained.create(data_type=String, constraints=[MaximalLength(5)])(String("Hello"))

        # Compare equality
        assert data_type_0 == data_type_1

    def test_should_be_false_on_unequal_type(self):
        # Create data type
        data_type_0 = Constrained.create(data_type=String, constraints=[MaximalLength(5)])()
        data_type_1 = Constrained.create(data_type=Binary, constraints=[MaximalLength(5)])()

        # Compare equality
        assert data_type_0 != data_type_1

    def test_should_be_false_on_unequal_constraints(self):
        # Create data type
        data_type_0 = Constrained.create(data_type=String, constraints=[MaximalLength(5)])(String("Hello"))
        data_type_1 = Constrained.create(data_type=String, constraints=[Length(5)])(String("Hello"))

        # Compare equality
        assert data_type_0 != data_type_1

    def test_should_be_false_on_unequal_value(self):
        # Create data type
        data_type_0 = Constrained.create(data_type=String, constraints=[MaximalLength(5)])(String("Hello"))
        data_type_1 = Constrained.create(data_type=String, constraints=[MaximalLength(5)])(String("World"))

        # Compare equality
        assert data_type_0 != data_type_1

    def test_should_be_false_on_non_constrained(self):
        # Create data type
        data_type = Constrained.create(data_type=String, constraints=[MaximalLength(5)])(String("Hello"))

        # Compare equality
        assert data_type != unittest.mock.Mock()
