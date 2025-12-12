import re

import pytest
import typing_extensions as typing

from sila.framework.constraints.pattern import Pattern
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.string import String
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError
from sila.framework.fdl.serializer import Serializer


class TestInitialize:
    async def test_should_initialize(self):
        # Create constraint
        constraint = Pattern(value=r".")

        # Assert that the method returns the correct value
        assert constraint.value == "."


class TestValidate:
    async def test_should_raise_on_invalid_type(self):
        # Create constraint
        constraint = Pattern(value=r".")

        # Validate constraint
        with pytest.raises(TypeError, match=re.escape("Expected value of type 'String', received 'Integer'.")):
            await constraint.validate(typing.cast(String, Integer(42)))

    async def test_should_validate_string(self):
        # Create constraint
        constraint = Pattern(value=r".")

        # Validate constraint
        assert await constraint.validate(String("a")) is True

    async def test_should_raise_on_invalid_string(self):
        # Create constraint
        constraint = Pattern(value=r".")

        # Validate constraint
        with pytest.raises(ValueError, match=re.escape("Value 'abc' does not match the pattern: '.'.")):
            await constraint.validate(String("abc"))


class TestSerialize:
    async def test_should_serialize_xml(self):
        # Create constraint
        constraint = Pattern(r"[0-9]{2}/[0-9]{2}/[0-9]{4}")

        # Serialize
        xml = Serializer.serialize(constraint.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == "<Pattern>[0-9]{2}/[0-9]{2}/[0-9]{4}</Pattern>"


class TestDeserialize:
    async def test_should_raise_on_missing_data_type(self):
        # Create xml
        xml = "<Pattern>[0-9]{2}/[0-9]{2}/[0-9]{4}</Pattern>"

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Missing 'data_type' in context.")):
            Deserializer.deserialize(xml, Pattern.deserialize)

    async def test_should_raise_on_invalid_data_type(self):
        # Create xml
        xml = "<Pattern>[0-9]{2}/[0-9]{2}/[0-9]{4}</Pattern>"

        # Deserialize
        with pytest.raises(
            ParseError, match=re.escape("Expected constraint's data type to be 'String', received 'Integer'.")
        ):
            Deserializer.deserialize(xml, Pattern.deserialize, {"data_type": Integer})

    async def test_should_deserialize_singleline_xml(self):
        # Create xml
        xml = "<Pattern>[0-9]{2}/[0-9]{2}/[0-9]{4}</Pattern>"

        # Deserialize
        constraint = Deserializer.deserialize(xml, Pattern.deserialize, {"data_type": String})

        # Assert that the method returns the correct value
        assert constraint == Pattern(r"[0-9]{2}/[0-9]{2}/[0-9]{4}")

    async def test_should_deserialize_multiline_xml(self):
        # Create xml
        xml = """
        <Pattern>
          [0-9]{2}/[0-9]{2}/[0-9]{4}
        </Pattern>
        """

        # Deserialize
        constraint = Deserializer.deserialize(xml, Pattern.deserialize, {"data_type": String})

        # Assert that the method returns the correct value
        assert constraint == Pattern(r"[0-9]{2}/[0-9]{2}/[0-9]{4}")
