import re
import textwrap

import pytest
import typing_extensions as typing

from sila.framework.constraints.set import Set
from sila.framework.data_types.boolean import Boolean
from sila.framework.data_types.date import Date
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.real import Real
from sila.framework.data_types.string import String
from sila.framework.data_types.time import Time
from sila.framework.data_types.timestamp import Timestamp
from sila.framework.data_types.timezone import Timezone
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError
from sila.framework.fdl.serializer import Serializer


class TestInitialize:
    async def test_should_initialize(self):
        # Create constraint
        constraint = Set(values=[Integer(1), Integer(2), Integer(3)])

        # Assert that the method returns the correct value
        assert constraint.values == [Integer(1), Integer(2), Integer(3)]

    async def test_should_raise_on_empty_values(self):
        # Create constraint
        with pytest.raises(ValueError, match=re.escape("The list of allowed values must not be empty.")):
            Set(values=[])

    async def test_should_raise_on_invalid_types(self):
        # Create constraint
        with pytest.raises(TypeError, match=re.escape("The list of allowed values must all have the same type.")):
            Set(values=[typing.cast(Integer, String("a")), Integer(2), Integer(3)])


class TestValidate:
    async def test_should_raise_on_invalid_type(self):
        # Create constraint
        constraint = Set(values=[String("a"), String("b"), String("c")])

        # Validate constraint
        with pytest.raises(TypeError, match=re.escape("Expected value of type 'String', received 'Integer'.")):
            await constraint.validate(typing.cast(String, Integer(42)))

    async def test_should_validate_string(self):
        # Create constraint
        constraint = Set(values=[String("a"), String("b"), String("c")])

        # Validate constraint
        assert await constraint.validate(String("b")) is True

    async def test_should_raise_on_invalid_string(self):
        # Create constraint
        constraint = Set(values=[String("a"), String("b"), String("c")])

        # Validate constraint
        with pytest.raises(ValueError, match=re.escape("Value 'x' is not in the set of allowed values.")):
            await constraint.validate(String("x"))

    async def test_should_validate_integer(self):
        # Create constraint
        constraint = Set(values=[Integer(1), Integer(2), Integer(3)])

        # Validate constraint
        assert await constraint.validate(Integer(1)) is True

    async def test_should_raise_on_invalid_integer(self):
        # Create constraint
        constraint = Set(values=[Integer(1), Integer(2), Integer(3)])

        # Validate constraint
        with pytest.raises(ValueError, match=re.escape("Value '10' is not in the set of allowed values.")):
            await constraint.validate(Integer(10))

    async def test_should_validate_real(self):
        # Create constraint
        constraint = Set(values=[Real(1.1), Real(2.2), Real(3.3)])

        # Validate constraint
        assert await constraint.validate(Real(1.1)) is True

    async def test_should_raise_on_invalid_real(self):
        # Create constraint
        constraint = Set(values=[Real(1.1), Real(2.2), Real(3.3)])

        # Validate constraint
        with pytest.raises(ValueError, match=re.escape("Value '4.4' is not in the set of allowed values.")):
            await constraint.validate(Real(4.4))

    async def test_should_validate_date(self):
        # Create constraint
        constraint = Set(values=[Date(1970, 1, 1), Date(1987, 6, 5), Date(1999, 12, 13)])

        # Validate constraint
        assert await constraint.validate(Date(1970, 1, 1)) is True

    async def test_should_raise_on_invalid_date(self):
        # Create constraint
        constraint = Set(values=[Date(1970, 1, 1), Date(1987, 6, 5), Date(1999, 12, 13)])

        # Validate constraint
        with pytest.raises(ValueError, match=re.escape("Value '1912-03-04Z' is not in the set of allowed values.")):
            await constraint.validate(Date(1912, 3, 4))

    async def test_should_validate_time(self):
        # Create constraint
        constraint = Set(values=[Time(13, 37, 42, 900), Time(6, 7, 8, 9), Time(23, 32, 23, 32)])

        # Validate constraint
        assert await constraint.validate(Time(13, 37, 42, 900)) is True

    async def test_should_raise_on_invalid_time(self):
        # Create constraint
        constraint = Set(values=[Time(13, 37, 42, 900), Time(6, 7, 8, 9), Time(23, 32, 23, 32)])

        # Validate constraint
        with pytest.raises(ValueError, match=re.escape("Value '23:32:23.031Z' is not in the set of allowed values.")):
            await constraint.validate(Time(23, 32, 23, 31))

    async def test_should_validate_timestamp(self):
        # Create constraint
        constraint = Set(
            values=[
                Timestamp(1970, 1, 1, 13, 37, 42, 900),
                Timestamp(3, 4, 5, 6, 7, 8, 9),
                Timestamp(1999, 12, 13, 23, 32, 23, 32),
            ]
        )

        # Validate constraint
        assert await constraint.validate(Timestamp(1970, 1, 1, 13, 37, 42, 900)) is True

    async def test_should_raise_on_invalid_timestamp(self):
        # Create constraint
        constraint = Set(
            values=[
                Timestamp(1970, 1, 1, 13, 37, 42, 900),
                Timestamp(3, 4, 5, 6, 7, 8, 9),
                Timestamp(1999, 12, 13, 23, 32, 23, 32),
            ]
        )

        # Validate constraint
        with pytest.raises(
            ValueError, match=re.escape("Value '0032-12-31T23:32:23.031Z' is not in the set of allowed values.")
        ):
            await constraint.validate(Timestamp(32, 12, 31, 23, 32, 23, 31))


class TestSerialize:
    async def test_should_serialize_singleline_xml(self):
        # Create constraint
        constraint = Set([String("Hello"), String("World")])

        # Serialize
        xml = Serializer.serialize(constraint.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == "<Set><Value>Hello</Value><Value>World</Value></Set>"

    async def test_should_serialize_multiline_xml(self):
        # Create constraint
        constraint = Set([String("Hello"), String("World")])

        # Serialize
        xml = Serializer.serialize(constraint.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <Set>
              <Value>Hello</Value>
              <Value>World</Value>
            </Set>
            """
        )

    async def test_should_serialize_string(self):
        # Create constraint
        constraint = Set([String("First option"), String("Second option"), String("Third option")])

        # Serialize
        xml = Serializer.serialize(constraint.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == "<Set><Value>First option</Value><Value>Second option</Value><Value>Third option</Value></Set>"

    async def test_should_serialize_integer(self):
        # Create constraint
        constraint = Set([Integer(1), Integer(2), Integer(3)])

        # Serialize
        xml = Serializer.serialize(constraint.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == "<Set><Value>1</Value><Value>2</Value><Value>3</Value></Set>"

    async def test_should_serialize_real(self):
        # Create constraint
        constraint = Set([Real(1.11), Real(2.22), Real(3.33)])

        # Serialize
        xml = Serializer.serialize(constraint.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == "<Set><Value>1.11</Value><Value>2.22</Value><Value>3.33</Value></Set>"

    async def test_should_serialize_date(self):
        # Create constraint
        constraint = Set(
            [
                Date(2022, 9, 10),
                Date(2022, 9, 11, Timezone(hours=-1, minutes=45)),
                Date(2022, 9, 12, Timezone(hours=11, minutes=30)),
            ]
        )

        # Serialize
        xml = Serializer.serialize(constraint.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert (
            xml == "<Set><Value>2022-09-10Z</Value><Value>2022-09-11-00:15</Value><Value>2022-09-12+11:30</Value></Set>"
        )

    async def test_should_serialize_time(self):
        # Create constraint
        constraint = Set(
            [
                Time(18, 59, 59, 999, Timezone(hours=2)),
                Time(19, 0, 0, 0, Timezone(hours=-1, minutes=45)),
                Time(19, 59, 0, 123),
            ]
        )

        # Serialize
        xml = Serializer.serialize(constraint.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == (
            "<Set><Value>18:59:59.999+02:00</Value><Value>19:00:00.000-00:15</Value><Value>19:59:00.123Z</Value></Set>"
        )

    async def test_should_serialize_timestamp(self):
        # Create constraint
        constraint = Set(
            [
                Timestamp(1969, 7, 16, 13, 32, 0, 1, Timezone(hours=-2)),
                Timestamp(1969, 7, 20, 20, 17, 40),
                Timestamp(1969, 7, 24, 16, 50, 35, 123),
            ]
        )

        # Serialize
        xml = Serializer.serialize(constraint.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == (
            "<Set>"
            "<Value>1969-07-16T13:32:00.001-02:00</Value>"
            "<Value>1969-07-20T20:17:40.000Z</Value>"
            "<Value>1969-07-24T16:50:35.123Z</Value>"
            "</Set>"
        )


class TestDeserialize:
    async def test_should_raise_on_missing_data_type(self):
        # Create xml
        xml = "<Set><Value>Hello</Value><Value>World</Value></Set>"

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Missing 'data_type' in context.")):
            Deserializer.deserialize(xml, Set.deserialize)

    async def test_should_raise_on_invalid_data_type(self):
        # Create xml
        xml = "<Set><Value>Hello</Value><Value>World</Value></Set>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape(
                "Expected constraint's data type to be 'String', 'Integer', 'Real', 'Date', 'Time' or 'Timestamp', "
                "received 'Boolean'."
            ),
        ):
            Deserializer.deserialize(xml, Set.deserialize, {"data_type": Boolean})

    async def test_should_deserialize_singleline_xml(self):
        # Create xml
        xml = "<Set><Value>Hello</Value><Value>World</Value></Set>"

        # Deserialize
        constraint = Deserializer.deserialize(xml, Set.deserialize, {"data_type": String})

        # Assert that the method returns the correct value
        assert constraint == Set([String("Hello"), String("World")])

    async def test_should_deserialize_multiline_xml(self):
        # Create xml
        xml = """
        <Set>
          <Value>Hello</Value>
          <Value>World</Value>
        </Set>
        """

        # Deserialize
        constraint = Deserializer.deserialize(xml, Set.deserialize, {"data_type": String})

        # Assert that the method returns the correct value
        assert constraint == Set([String("Hello"), String("World")])

    async def test_should_deserialize_string(self):
        # Create xml
        xml = "<Set><Value>First option</Value><Value>Second option</Value><Value>Third option</Value></Set>"

        # Deserialize
        constraint = Deserializer.deserialize(xml, Set.deserialize, {"data_type": String})

        # Assert that the method returns the correct value
        assert constraint == Set([String("First option"), String("Second option"), String("Third option")])

    async def test_should_deserialize_integer(self):
        # Create xml
        xml = "<Set><Value>1</Value><Value>2</Value><Value>3</Value></Set>"

        # Deserialize
        constraint = Deserializer.deserialize(xml, Set.deserialize, {"data_type": Integer})

        # Assert that the method returns the correct value
        assert constraint == Set([Integer(1), Integer(2), Integer(3)])

    async def test_should_deserialize_real(self):
        # Create xml
        xml = "<Set><Value>1.11</Value><Value>2.22</Value><Value>3.33</Value></Set>"

        # Deserialize
        constraint = Deserializer.deserialize(xml, Set.deserialize, {"data_type": Real})

        # Assert that the method returns the correct value
        assert constraint == Set([Real(1.11), Real(2.22), Real(3.33)])

    async def test_should_deserialize_date(self):
        # Create xml
        xml = "<Set><Value>2022-09-10Z</Value><Value>2022-09-11-00:15</Value><Value>2022-09-12+11:30</Value></Set>"

        # Deserialize
        constraint = Deserializer.deserialize(xml, Set.deserialize, {"data_type": Date})

        # Assert that the method returns the correct value
        assert constraint == Set(
            [
                Date(2022, 9, 10),
                Date(2022, 9, 11, Timezone(hours=-1, minutes=45)),
                Date(2022, 9, 12, Timezone(hours=11, minutes=30)),
            ]
        )

    async def test_should_deserialize_time(self):
        # Create xml
        xml = (
            "<Set><Value>18:59:59.999+02:00</Value><Value>19:00:00.000-00:15</Value><Value>19:59:00.123Z</Value></Set>"
        )

        # Deserialize
        constraint = Deserializer.deserialize(xml, Set.deserialize, {"data_type": Time})

        # Assert that the method returns the correct value
        assert constraint == Set(
            [
                Time(18, 59, 59, 999, Timezone(hours=2)),
                Time(19, 0, 0, 0, Timezone(hours=-1, minutes=45)),
                Time(19, 59, 0, 123),
            ]
        )

    async def test_should_deserialize_timestamp(self):
        # Create xml
        xml = (
            "<Set>"
            "<Value>1969-07-16T13:32:00.001-02:00</Value>"
            "<Value>1969-07-20T20:17:40.000Z</Value>"
            "<Value>1969-07-24T16:50:35.123Z</Value>"
            "</Set>"
        )

        # Deserialize
        constraint = Deserializer.deserialize(xml, Set.deserialize, {"data_type": Timestamp})

        # Assert that the method returns the correct value
        assert constraint == Set(
            [
                Timestamp(1969, 7, 16, 13, 32, 0, 1, Timezone(hours=-2)),
                Timestamp(1969, 7, 20, 20, 17, 40),
                Timestamp(1969, 7, 24, 16, 50, 35, 123),
            ]
        )

    async def test_should_raise_on_unexpected_characters(self):
        # Create xml
        xml = "<Set>Hello, World!</Set>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape(
                "Expected start element with name 'Value', received characters '['Hello, World!']'.",
            ),
        ):
            Deserializer.deserialize(xml, Set.deserialize, {"data_type": String})

    async def test_should_raise_on_unexpected_start_element(self):
        # Create xml
        xml = "<Set><Basic>String</Basic></Set>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape("Expected start element with name 'Value', received start element with name 'Basic'."),
        ):
            Deserializer.deserialize(xml, Set.deserialize, {"data_type": String})

    async def test_should_raise_on_missing_values(self):
        # Create xml
        xml = "<Set></Set>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape("Expected at least one 'Value' element inside the 'Set' element."),
        ):
            Deserializer.deserialize(xml, Set.deserialize, {"data_type": String})
