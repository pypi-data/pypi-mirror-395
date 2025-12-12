import re
import textwrap
import unittest.mock

import pytest

from sila import datetime
from sila.framework.constraints.maximal_length import MaximalLength
from sila.framework.constraints.unit import Unit
from sila.framework.data_types.any import Any
from sila.framework.data_types.binary import Binary
from sila.framework.data_types.boolean import Boolean
from sila.framework.data_types.constrained import Constrained
from sila.framework.data_types.date import Date
from sila.framework.data_types.element import Element
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.list import List
from sila.framework.data_types.real import Real
from sila.framework.data_types.string import String
from sila.framework.data_types.structure import Structure
from sila.framework.data_types.time import Time
from sila.framework.data_types.timestamp import Timestamp
from sila.framework.data_types.timezone import Timezone
from sila.framework.data_types.void import Void
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError
from sila.framework.fdl.serializer import Serializer
from sila.framework.protobuf.decode_error import DecodeError


class TestInitFromNative:
    async def test_should_accept_no_value(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Any.from_native(context)

        # Assert that the method returns the correct value
        assert data_type == Any()

    async def test_should_accept_none(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Any.from_native(context, None)

        # Assert that the method returns the correct value
        assert data_type == Any()

    async def test_should_accept_string(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Any.from_native(context, "Hello, World!")

        # Assert that the method returns the correct value
        assert data_type == Any(value=String("Hello, World!"))

    async def test_should_accept_bytes(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Any.from_native(context, b"Hello, World!")

        # Assert that the method returns the correct value
        assert data_type == Any(value=Binary(b"Hello, World!"))

    async def test_should_accept_boolean(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Any.from_native(context, True)

        # Assert that the method returns the correct value
        assert data_type == Any(value=Boolean(True))

    async def test_should_accept_integer(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Any.from_native(context, 42)

        # Assert that the method returns the correct value
        assert data_type == Any(value=Integer(42))

    async def test_should_accept_float(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Any.from_native(context, 3.141592653589793)

        # Assert that the method returns the correct value
        assert data_type == Any(value=Real(3.141592653589793))

    async def test_should_accept_datetime(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Any.from_native(
            context,
            datetime.datetime(
                year=2022,
                month=8,
                day=5,
                hour=12,
                minute=34,
                second=56,
                microsecond=789000,
                tzinfo=datetime.timezone(datetime.timedelta(hours=12, minutes=34)),
            ),
        )

        # Assert that the method returns the correct value
        assert data_type == Any(
            value=Timestamp(
                year=2022,
                month=8,
                day=5,
                hour=12,
                minute=34,
                second=56,
                millisecond=789,
                timezone=Timezone(hours=12, minutes=34),
            )
        )

    async def test_should_accept_date(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Any.from_native(
            context,
            datetime.date(
                year=2022,
                month=8,
                day=5,
                tzinfo=datetime.timezone(datetime.timedelta(hours=12, minutes=34)),
            ),
        )

        # Assert that the method returns the correct value
        assert data_type == Any(
            value=Date(
                year=2022,
                month=8,
                day=5,
                timezone=Timezone(hours=12, minutes=34),
            )
        )

    async def test_should_accept_time(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Any.from_native(
            context,
            datetime.time(
                hour=12,
                minute=34,
                second=56,
                microsecond=789000,
                tzinfo=datetime.timezone(datetime.timedelta(hours=12, minutes=34)),
            ),
        )

        # Assert that the method returns the correct value
        assert data_type == Any(
            value=Time(
                hour=12,
                minute=34,
                second=56,
                millisecond=789,
                timezone=Timezone(hours=12, minutes=34),
            )
        )

    async def test_should_accept_empty_dict(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Any.from_native(context, {})

        # Assert that the method returns the correct value
        assert data_type == Any(value=Structure.create({})({}))

    async def test_should_accept_dict(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Any.from_native(context, {"StringValue": "Hello, World!", "IntegerValue": 42})

        # Assert that the method returns the correct value
        assert data_type == Any(
            value=Structure.create(
                {
                    "StringValue": Element(identifier="StringValue", display_name="StringValue", data_type=String),
                    "IntegerValue": Element(identifier="IntegerValue", display_name="IntegerValue", data_type=Integer),
                }
            )({"StringValue": String("Hello, World!"), "IntegerValue": Integer(42)})
        )

    async def test_should_accept_empty_list(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Any.from_native(context, [])

        # Assert that the method returns the correct value
        assert data_type == Any(value=List.create(Void)([]))

    async def test_should_accept_list(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Any.from_native(context, [{"X": 1.23, "Y": 3.21}, {"X": 4.56, "Y": 6.54}])

        # Assert that the method returns the correct value
        Struct = Structure.create(
            {
                "X": Element(identifier="X", display_name="X", data_type=Real),
                "Y": Element(identifier="Y", display_name="Y", data_type=Real),
            }
        )
        assert data_type == Any(
            value=List.create(Struct)(
                [Struct({"X": Real(1.23), "Y": Real(3.21)}), Struct({"X": Real(4.56), "Y": Real(6.54)})]
            )
        )

    async def test_should_accept_any(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Any.from_native(context, Any(value=Integer(42)))

        # Assert that the method returns the correct value
        assert data_type == Any(value=Integer(42))

    async def test_should_accept_data_type(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Any.from_native(context, Integer(42))

        # Assert that the method returns the correct value
        assert data_type == Any(value=Integer(42))

    async def test_should_raise_on_nested_list(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        with pytest.raises(ValueError, match=re.escape("List may not contain other lists.")):
            await Any.from_native(context, [[]])

    async def test_should_raise_on_list_with_multiple_types(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        with pytest.raises(ValueError, match=re.escape("Only same type lists are allowed.")):
            await Any.from_native(context, ["Hello, World!", 42])


class TestConvertToNative:
    async def test_should_convert_string(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = Any(value=String("Hello, World!"))

        # Convert to native
        native = await data_type.to_native(context)

        # Assert that the method returns the correct value
        assert native == data_type

    async def test_should_convert_binary(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = Any(value=Binary(b"Hello, World!"))

        # Convert to native
        native = await data_type.to_native(context)

        # Assert that the method returns the correct value
        assert native == data_type

    async def test_should_convert_boolean(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = Any(value=Boolean(True))

        # Convert to native
        native = await data_type.to_native(context)

        # Assert that the method returns the correct value
        assert native == data_type

    async def test_should_convert_integer(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = Any(value=Integer(42))

        # Convert to native
        native = await data_type.to_native(context)

        # Assert that the method returns the correct value
        assert native == data_type

    async def test_should_convert_real(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = Any(value=Real(3.141592653589793))

        # Convert to native
        native = await data_type.to_native(context)

        # Assert that the method returns the correct value
        assert native == data_type

    async def test_should_convert_timestamp(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = Any(
            value=Timestamp(
                year=2022,
                month=8,
                day=5,
                hour=12,
                minute=34,
                second=56,
                millisecond=789,
                timezone=Timezone(hours=12, minutes=34),
            )
        )

        # Convert to native
        native = await data_type.to_native(context)

        # Assert that the method returns the correct value
        assert native == data_type

    async def test_should_convert_date(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = Any(value=Date(year=2022, month=8, day=5, timezone=Timezone(hours=12, minutes=34)))

        # Convert to native
        native = await data_type.to_native(context)

        # Assert that the method returns the correct value
        assert native == data_type

    async def test_should_convert_time(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = Any(
            value=Time(hour=12, minute=34, second=56, millisecond=789, timezone=Timezone(hours=12, minutes=34))
        )

        # Convert to native
        native = await data_type.to_native(context)

        # Assert that the method returns the correct value
        assert native == data_type

    async def test_should_convert_empty_structure(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = Any(value=Structure.create({})({}))

        # Convert to native
        native = await data_type.to_native(context)

        # Assert that the method returns the correct value
        assert native == data_type

    async def test_should_convert_structure(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = Any(
            value=Structure.create(
                {
                    "string_value": Element(identifier="StringValue", display_name="String Value", data_type=String),
                    "integer_value": Element(
                        identifier="IntegerValue", display_name="Integer Value", data_type=Integer
                    ),
                }
            )({"string_value": String("Hello, World!"), "integer_value": Integer(42)})
        )

        # Convert to native
        native = await data_type.to_native(context)

        # Assert that the method returns the correct value
        assert native == data_type

    async def test_should_convert_empty_list(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = Any(value=List.create(Void)([]))

        # Convert to native
        native = await data_type.to_native(context)

        # Assert that the method returns the correct value
        assert native == data_type

    async def test_should_convert_list(self):
        # Create data type
        context = unittest.mock.Mock()
        Struct = Structure.create(
            {
                "x": Element(identifier="X", display_name="X", data_type=Real),
                "y": Element(identifier="Y", display_name="Y", data_type=Real),
            }
        )
        data_type = Any(
            value=List.create(Struct)(
                [Struct({"x": Real(1.23), "y": Real(3.21)}), Struct({"x": Real(4.56), "y": Real(6.54)})]
            )
        )

        # Convert to native
        native = await data_type.to_native(context)

        # Assert that the method returns the correct value
        assert native == data_type

    async def test_should_convert_constrained(self):
        # Create data type
        context = unittest.mock.Mock()
        data_type = Any(value=Constrained.create(String, [MaximalLength(1)])(String("a")))

        # Convert to native
        native = await data_type.to_native(context)

        # Assert that the method returns the correct value
        assert native == data_type


class TestDecode:
    async def test_should_decode_string(self):
        # Create buffer
        buffer = (
            b'\x0a\x4f<DataType xmlns="http://www.sila-standard.org"><Basic>String</Basic></DataType>'
            b"\x12\x11\x0a\x0f\x0a\x0dHello, World!"
        )

        # Decode data type
        message = Any.decode(buffer)

        # Assert that the method returns the correct value
        assert message == Any(value=String("Hello, World!"))

    async def test_should_decode_binary(self):
        # Create buffer
        buffer = (
            b'\x0a\x4f<DataType xmlns="http://www.sila-standard.org"><Basic>Binary</Basic></DataType>'
            b"\x12\x11\x0a\x0f\x0a\x0dHello, World!"
        )

        # Decode data type
        message = Any.decode(buffer)

        # Assert that the method returns the correct value
        assert message == Any(value=Binary(b"Hello, World!"))

    async def test_should_decode_boolean(self):
        # Create buffer
        buffer = b'\x0a\x50<DataType xmlns="http://www.sila-standard.org"><Basic>Boolean</Basic></DataType>\x12\x04\x0a\x02\x08\x01'

        # Decode data type
        message = Any.decode(buffer)

        # Assert that the method returns the correct value
        assert message == Any(value=Boolean(True))

    async def test_should_decode_integer(self):
        # Create buffer
        buffer = b'\x0a\x50<DataType xmlns="http://www.sila-standard.org"><Basic>Integer</Basic></DataType>\x12\x04\x0a\x02\x08\x2a'

        # Decode data type
        message = Any.decode(buffer)

        # Assert that the method returns the correct value
        assert message == Any(value=Integer(42))

    async def test_should_decode_real(self):
        # Create buffer
        buffer = b'\x0a\x4d<DataType xmlns="http://www.sila-standard.org"><Basic>Real</Basic></DataType>\x12\x0b\x0a\x09\x09\x18\x2d\x44\x54\xfb\x21\x09\x40'

        # Decode data type
        message = Any.decode(buffer)

        # Assert that the method returns the correct value
        assert message == Any(value=Real(3.141592653589793))

    async def test_should_decode_timestamp(self):
        # Create buffer
        buffer = (
            b"\x0a\x52"
            b'<DataType xmlns="http://www.sila-standard.org">'
            b"<Basic>Timestamp</Basic>"
            b"</DataType>"
            b"\x12\x18\x0a\x16\x08\x38\x10\x22\x18\x0c\x20\x05\x28\x08\x30\xe6\x0f\x3a\x04\x08\x0c\x10\x22\x40\x95\x06"
        )

        # Decode data type
        message = Any.decode(buffer)

        # Assert that the method returns the correct value
        assert message == Any(
            value=Timestamp(
                year=2022,
                month=8,
                day=5,
                hour=12,
                minute=34,
                second=56,
                millisecond=789,
                timezone=Timezone(hours=12, minutes=34),
            )
        )

    async def test_should_decode_date(self):
        # Create buffer
        buffer = (
            b"\x0a\x4d"
            b'<DataType xmlns="http://www.sila-standard.org">'
            b"<Basic>Date</Basic>"
            b"</DataType>"
            b"\x12\x0f\x0a\x0d\x08\x05\x10\x08\x18\xe6\x0f\x22\x04\x08\x0c\x10\x22"
        )

        # Decode data type
        message = Any.decode(buffer)

        # Assert that the method returns the correct value
        assert message == Any(value=Date(year=2022, month=8, day=5, timezone=Timezone(hours=12, minutes=34)))

    async def test_should_decode_time(self):
        # Create buffer
        buffer = (
            b"\x0a\x4d"
            b'<DataType xmlns="http://www.sila-standard.org">'
            b"<Basic>Time</Basic>"
            b"</DataType>"
            b"\x12\x11\x0a\x0f\x08\x38\x10\x22\x18\x0c\x22\x04\x08\x0c\x10\x22\x28\x95\x06"
        )

        # Decode data type
        message = Any.decode(buffer)

        # Assert that the method returns the correct value
        assert message == Any(
            value=Time(hour=12, minute=34, second=56, millisecond=789, timezone=Timezone(hours=12, minutes=34))
        )

    async def test_should_decode_void(self):
        # Create buffer
        buffer = (
            b"\x0a\xac\x01"
            b'<DataType xmlns="http://www.sila-standard.org">'
            b"<Constrained>"
            b"<DataType>"
            b"<Basic>String</Basic>"
            b"</DataType>"
            b"<Constraints>"
            b"<Length>0</Length>"
            b"</Constraints>"
            b"</Constrained>"
            b"</DataType>"
        )

        # Decode data type
        message = Any.decode(buffer)

        # Assert that the method returns the correct value
        assert message == Any(value=Void())

    async def test_should_decode_constrained(self):
        # Create buffer
        buffer = (
            b"\x0a\xa8\x02"
            b'<DataType xmlns="http://www.sila-standard.org">'
            b"<Constrained>"
            b"<DataType>"
            b"<Basic>Integer</Basic>"
            b"</DataType>"
            b"<Constraints>"
            b"<Unit>"
            b"<Label>s</Label>"
            b"<Factor>1</Factor>"
            b"<Offset>0</Offset>"
            b"<UnitComponent>"
            b"<SIUnit>Second</SIUnit>"
            b"<Exponent>1</Exponent>"
            b"</UnitComponent>"
            b"</Unit>"
            b"</Constraints>"
            b"</Constrained>"
            b"</DataType>"
            b"\x12\x04\x0a\x02\x08\x2a"
        )

        # Decode data type
        message = Any.decode(buffer)

        # Assert that the method returns the correct value
        assert message == Any(
            value=Constrained.create(data_type=Integer, constraints=[Unit("s", [Unit.Component("Second")])])(
                Integer(42)
            )
        )

    async def test_should_decode_structure(self):
        # Create buffer
        buffer = (
            b"\x0a\xb5\x03"
            b'<DataType xmlns="http://www.sila-standard.org">'
            b"<Structure>"
            b"<Element>"
            b"<Identifier>StringValue</Identifier>"
            b"<DisplayName>String Value</DisplayName>"
            b"<Description>String Value.</Description>"
            b"<DataType>"
            b"<Basic>String</Basic>"
            b"</DataType>"
            b"</Element>"
            b"<Element>"
            b"<Identifier>IntegerValue</Identifier>"
            b"<DisplayName>Integer Value</DisplayName>"
            b"<Description>Integer Value.</Description>"
            b"<DataType>"
            b"<Basic>Integer</Basic>"
            b"</DataType>"
            b"</Element>"
            b"</Structure>"
            b"</DataType>"
            b"\x12\x17\x0a\x15\x0a\x0f\x0a\x0dHello, World!\x12\x02\x08\x2a"
        )

        # Decode data type
        message = Any.decode(buffer)

        # Assert that the method returns the correct value
        assert message == Any(
            value=Structure.create(
                {
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
            )({"StringValue": String("Hello, World!"), "IntegerValue": Integer(42)})
        )

    async def test_should_decode_list(self):
        # Create buffer
        buffer = (
            b"\x0a\xc3\x03"
            b'<DataType xmlns="http://www.sila-standard.org">'
            b"<List>"
            b"<DataType>"
            b"<Structure>"
            b"<Element>"
            b"<Identifier>X</Identifier>"
            b"<DisplayName>X Coordinate</DisplayName>"
            b"<Description>The X coordinate.</Description>"
            b"<DataType>"
            b"<Basic>Real</Basic>"
            b"</DataType>"
            b"</Element>"
            b"<Element>"
            b"<Identifier>Y</Identifier>"
            b"<DisplayName>Y Coordinate</DisplayName>"
            b"<Description>The Y coordinate.</Description>"
            b"<DataType>"
            b"<Basic>Real</Basic>"
            b"</DataType>"
            b"</Element>"
            b"</Structure>"
            b"</DataType>"
            b"</List>"
            b"</DataType>"
            b"\x12\x30\x0a\x16\x0a\x09\x09\xae\x47\xe1\x7a\x14\xae\xf3\x3f\x12\x09\x09\xae\x47\xe1\x7a\x14\xae\x09\x40\x0a\x16\x0a\x09\x09\x3d\x0a\xd7\xa3\x70\x3d\x12\x40\x12\x09\x09\x29\x5c\x8f\xc2\xf5\x28\x1a\x40"
        )

        # Decode data type
        message = Any.decode(buffer)

        # Assert that the method returns the correct value
        Struct = Structure.create(
            {
                "X": Element(
                    identifier="X", display_name="X Coordinate", description="The X coordinate.", data_type=Real
                ),
                "Y": Element(
                    identifier="Y", display_name="Y Coordinate", description="The Y coordinate.", data_type=Real
                ),
            },
        )
        assert message == Any(
            value=List.create(Struct)(
                [Struct({"X": Real(1.23), "Y": Real(3.21)}), Struct({"X": Real(4.56), "Y": Real(6.54)})]
            )
        )

    async def test_should_raise_on_invalid_schema(self):
        # Create buffer
        buffer = b'\x0a\x50<DataType xmlns="http://www.sila-standard.org"><Basic>Complex</Basic></DataType>\x12\x04\x0a\x02\x08\x2a'

        # Decode data type
        with pytest.raises(DecodeError, match=re.escape("Expected basic type value, received 'Complex'.")):
            Any.decode(buffer)

    async def test_should_skip_unknown_fields(self):
        # Create buffer
        buffer = (
            b'\x0a\x4f<DataType xmlns="http://www.sila-standard.org"><Basic>String</Basic></DataType>'
            b"\x12\x11\x0a\x0f\x0a\x0dHello, World!\x18\x2a"
        )

        # Decode data type
        message = Any.decode(buffer)

        # Assert that the method returns the correct value
        assert message == Any(value=String("Hello, World!"))

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = Any.decode(
            b'\x0a\x4f<DataType xmlns="http://www.sila-standard.org"><Basic>String</Basic></DataType>\x12\x09\x0a\x07\x0a\x05Hello\x12\x09\x0a\x07\x0a\x05World'
        )

        # Assert that the method returns the correct value
        assert message == Any(value=String("World"))

    async def test_should_decode_limited_buffer(self):
        # Decode data type
        message = Any.decode(
            b'\x0a\x4f<DataType xmlns="http://www.sila-standard.org"><Basic>String</Basic></DataType>\x12\x09\x0a\x07\x0a\x05Hello\x12\x09\x0a\x07\x0a\x05World',
            92,
        )

        # Assert that the method returns the correct value
        assert message == Any(value=String("Hello"))

    async def test_should_skip_xml_declaration(self):
        # Create buffer
        buffer = (
            b'\x0a\x75<?xml version="1.0" encoding="UTF-8"?><DataType xmlns="http://www.sila-standard.org"><Basic>String</Basic></DataType>'
            b"\x12\x11\x0a\x0f\x0a\x0dHello, World!\x18\x2a"
        )

        # Decode data type
        message = Any.decode(buffer)

        # Assert that the method returns the correct value
        assert message == Any(value=String("Hello, World!"))


class TestEncode:
    async def test_should_encode_string(self):
        # Create data type
        data_type = Any(value=String("Hello, World!"))

        # Encode data type
        message = data_type.encode()

        # Assert that the method returns the correct value
        assert message == (
            b'\x0a\x4f<DataType xmlns="http://www.sila-standard.org"><Basic>String</Basic></DataType>'
            b"\x12\x11\x0a\x0f\x0a\x0dHello, World!"
        )

    async def test_should_encode_binary(self):
        # Create data type
        data_type = Any(value=Binary(b"Hello, World!"))

        # Encode data type
        message = data_type.encode()

        # Assert that the method returns the correct value
        assert message == (
            b'\x0a\x4f<DataType xmlns="http://www.sila-standard.org"><Basic>Binary</Basic></DataType>'
            b"\x12\x11\x0a\x0f\x0a\x0dHello, World!"
        )

    async def test_should_encode_boolean(self):
        # Create data type
        data_type = Any(value=Boolean(True))

        # Encode data type
        message = data_type.encode()

        # Assert that the method returns the correct value
        assert (
            message
            == b'\x0a\x50<DataType xmlns="http://www.sila-standard.org"><Basic>Boolean</Basic></DataType>\x12\x04\x0a\x02\x08\x01'
        )

    async def test_should_encode_integer(self):
        # Create data type
        data_type = Any(value=Integer(42))

        # Encode data type
        message = data_type.encode()

        # Assert that the method returns the correct value
        assert (
            message
            == b'\x0a\x50<DataType xmlns="http://www.sila-standard.org"><Basic>Integer</Basic></DataType>\x12\x04\x0a\x02\x08\x2a'
        )

    async def test_should_encode_real(self):
        # Create data type
        data_type = Any(value=Real(3.141592653589793))

        # Encode data type
        message = data_type.encode()

        # Assert that the method returns the correct value
        assert message == (
            b'\x0a\x4d<DataType xmlns="http://www.sila-standard.org"><Basic>Real</Basic></DataType>\x12\x0b\x0a\x09\x09\x18\x2d\x44\x54\xfb\x21\x09\x40'
        )

    async def test_should_encode_timestamp(self):
        # Create data type
        data_type = Any(
            value=Timestamp(
                year=2022,
                month=8,
                day=5,
                hour=12,
                minute=34,
                second=56,
                millisecond=789,
                timezone=Timezone(hours=12, minutes=34),
            )
        )

        # Encode data type
        message = data_type.encode()

        # Assert that the method returns the correct value
        assert message == (
            b"\x0a\x52"
            b'<DataType xmlns="http://www.sila-standard.org">'
            b"<Basic>Timestamp</Basic>"
            b"</DataType>"
            b"\x12\x18\x0a\x16\x08\x38\x10\x22\x18\x0c\x20\x05\x28\x08\x30\xe6\x0f\x3a\x04\x08\x0c\x10\x22\x40\x95\x06"
        )

    async def test_should_encode_date(self):
        # Create data type
        data_type = Any(value=Date(year=2022, month=8, day=5, timezone=Timezone(hours=12, minutes=34)))

        # Encode data type
        message = data_type.encode()

        # Assert that the method returns the correct value
        assert message == (
            b"\x0a\x4d"
            b'<DataType xmlns="http://www.sila-standard.org">'
            b"<Basic>Date</Basic>"
            b"</DataType>"
            b"\x12\x0f\x0a\x0d\x08\x05\x10\x08\x18\xe6\x0f\x22\x04\x08\x0c\x10\x22"
        )

    async def test_should_encode_time(self):
        # Create data type
        data_type = Any(
            value=Time(hour=12, minute=34, second=56, millisecond=789, timezone=Timezone(hours=12, minutes=34))
        )

        # Encode data type
        message = data_type.encode()

        # Assert that the method returns the correct value
        assert message == (
            b"\x0a\x4d"
            b'<DataType xmlns="http://www.sila-standard.org">'
            b"<Basic>Time</Basic>"
            b"</DataType>"
            b"\x12\x11\x0a\x0f\x08\x38\x10\x22\x18\x0c\x22\x04\x08\x0c\x10\x22\x28\x95\x06"
        )

    async def test_should_encode_void(self):
        # Create data type
        data_type = Any(value=Void())

        # Encode data type
        message = data_type.encode()

        # Assert that the method returns the correct value
        assert message == (
            b"\x0a\xac\x01"
            b'<DataType xmlns="http://www.sila-standard.org">'
            b"<Constrained>"
            b"<DataType>"
            b"<Basic>String</Basic>"
            b"</DataType>"
            b"<Constraints>"
            b"<Length>0</Length>"
            b"</Constraints>"
            b"</Constrained>"
            b"</DataType>"
        )

    async def test_should_encode_constrained(self):
        # Create data type
        data_type = Any(
            value=Constrained.create(data_type=Integer, constraints=[Unit("s", [Unit.Component("Second")])])(
                Integer(42)
            )
        )

        # Encode data type
        message = data_type.encode()

        # Assert that the method returns the correct value
        assert message == (
            b"\x0a\xa8\x02"
            b'<DataType xmlns="http://www.sila-standard.org">'
            b"<Constrained>"
            b"<DataType>"
            b"<Basic>Integer</Basic>"
            b"</DataType>"
            b"<Constraints>"
            b"<Unit>"
            b"<Label>s</Label>"
            b"<Factor>1</Factor>"
            b"<Offset>0</Offset>"
            b"<UnitComponent>"
            b"<SIUnit>Second</SIUnit>"
            b"<Exponent>1</Exponent>"
            b"</UnitComponent>"
            b"</Unit>"
            b"</Constraints>"
            b"</Constrained>"
            b"</DataType>"
            b"\x12\x04\x0a\x02\x08\x2a"
        )

    async def test_should_encode_structure(self):
        # Create data type
        data_type = Any(
            value=Structure.create(
                {
                    "string_value": Element(
                        identifier="StringValue",
                        display_name="String Value",
                        description="String Value.",
                        data_type=String,
                    ),
                    "integer_value": Element(
                        identifier="IntegerValue",
                        display_name="Integer Value",
                        description="Integer Value.",
                        data_type=Integer,
                    ),
                }
            )({"string_value": String("Hello, World!"), "integer_value": Integer(42)})
        )

        # Encode data type
        message = data_type.encode()

        # Assert that the method returns the correct value
        assert message == (
            b"\x0a\xb5\x03"
            b'<DataType xmlns="http://www.sila-standard.org">'
            b"<Structure>"
            b"<Element>"
            b"<Identifier>StringValue</Identifier>"
            b"<DisplayName>String Value</DisplayName>"
            b"<Description>String Value.</Description>"
            b"<DataType>"
            b"<Basic>String</Basic>"
            b"</DataType>"
            b"</Element>"
            b"<Element>"
            b"<Identifier>IntegerValue</Identifier>"
            b"<DisplayName>Integer Value</DisplayName>"
            b"<Description>Integer Value.</Description>"
            b"<DataType>"
            b"<Basic>Integer</Basic>"
            b"</DataType>"
            b"</Element>"
            b"</Structure>"
            b"</DataType>"
            b"\x12\x17\x0a\x15\x0a\x0f\x0a\x0dHello, World!\x12\x02\x08\x2a"
        )

    async def test_should_encode_list(self):
        # Create data type
        Struct = Structure.create(
            {
                "x": Element(
                    identifier="X", display_name="X Coordinate", description="The X coordinate.", data_type=Real
                ),
                "y": Element(
                    identifier="Y", display_name="Y Coordinate", description="The Y coordinate.", data_type=Real
                ),
            }
        )
        data_type = Any(
            value=List.create(Struct)(
                [Struct({"x": Real(1.23), "y": Real(3.21)}), Struct({"x": Real(4.56), "y": Real(6.54)})]
            )
        )

        # Encode data type
        message = data_type.encode()

        # Assert that the method returns the correct value
        assert message == (
            b"\x0a\xc3\x03"
            b'<DataType xmlns="http://www.sila-standard.org">'
            b"<List>"
            b"<DataType>"
            b"<Structure>"
            b"<Element>"
            b"<Identifier>X</Identifier>"
            b"<DisplayName>X Coordinate</DisplayName>"
            b"<Description>The X coordinate.</Description>"
            b"<DataType>"
            b"<Basic>Real</Basic>"
            b"</DataType>"
            b"</Element>"
            b"<Element>"
            b"<Identifier>Y</Identifier>"
            b"<DisplayName>Y Coordinate</DisplayName>"
            b"<Description>The Y coordinate.</Description>"
            b"<DataType>"
            b"<Basic>Real</Basic>"
            b"</DataType>"
            b"</Element>"
            b"</Structure>"
            b"</DataType>"
            b"</List>"
            b"</DataType>"
            b"\x12\x30\x0a\x16\x0a\x09\x09\xae\x47\xe1\x7a\x14\xae\xf3\x3f\x12\x09\x09\xae\x47\xe1\x7a\x14\xae\x09\x40\x0a\x16\x0a\x09\x09\x3d\x0a\xd7\xa3\x70\x3d\x12\x40\x12\x09\x09\x29\x5c\x8f\xc2\xf5\x28\x1a\x40"
        )

    @pytest.mark.parametrize(
        ("number", "buffer"),
        [
            pytest.param(
                1,
                b'\x0a\x5c\x0a\x4f<DataType xmlns="http://www.sila-standard.org"><Basic>String</Basic></DataType>\x12\x09\x0a\x07\x0a\x05Hello',
                id="default",
            ),
            pytest.param(
                2,
                b'\x12\x5c\x0a\x4f<DataType xmlns="http://www.sila-standard.org"><Basic>String</Basic></DataType>\x12\x09\x0a\x07\x0a\x05Hello',
                id="custom",
            ),
        ],
    )
    async def test_should_encode_field_number(self, number: int, buffer: bytes):
        # Encode data type
        data_type = Any(value=String("Hello"))
        message = data_type.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer


class TestSerialize:
    async def test_should_serialize_singleline_xml(self):
        # Serialize
        xml = Serializer.serialize(Any.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == "<DataType><Basic>Any</Basic></DataType>"

    async def test_should_deserialize_multiline_xml(self):
        # Serialize
        xml = Serializer.serialize(Any.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <DataType>
              <Basic>Any</Basic>
            </DataType>
            """
        )


class TestDeserialize:
    async def test_should_deserialize_singleline_xml(self):
        # Create xml
        xml = "<Basic>Any</Basic>"

        # Deserialize
        data_type = Deserializer.deserialize(xml, Any.deserialize)

        # Assert that the method returns the correct value
        assert data_type == Any

    async def test_should_deserialize_multiline_xml(self):
        # Create xml
        xml = """
        <Basic>
          Any
        </Basic>
        """

        # Deserialize
        data_type = Deserializer.deserialize(xml, Any.deserialize)

        # Assert that the method returns the correct value
        assert data_type == Any

    async def test_should_raise_on_unknown_basic_type(self):
        # Create xml
        xml = "<Basic>Complex</Basic>"

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Expected basic type value, received 'Complex'.")):
            Deserializer.deserialize(xml, Any.deserialize)
