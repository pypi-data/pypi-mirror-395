import re
import textwrap

import pytest

from sila.framework.constraints.allowed_types import AllowedTypes
from sila.framework.data_types.any import Any
from sila.framework.data_types.boolean import Boolean
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.list import List
from sila.framework.data_types.string import String
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError
from sila.framework.fdl.serializer import Serializer


class TestInitialize:
    async def test_should_initialize(self):
        # Create constraint
        constraint = AllowedTypes(values=[String])

        # Assert that the method returns the correct value
        assert constraint.values == [String]


@pytest.mark.skip(reason="Not implemented.")
class TestValidate:
    async def test_should_validate_string(self):
        # Create constraint
        constraint = AllowedTypes(values=[String])

        # Validate constraint
        assert await constraint.validate("") is True


class TestSerialize:
    async def test_should_serialize_singleline_xml(self):
        # Create constraint
        constraint = AllowedTypes(values=[Integer, List.create(Integer)])

        # Serialize
        xml = Serializer.serialize(constraint.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == (
            "<AllowedTypes>"
            "<DataType>"
            "<Basic>Integer</Basic>"
            "</DataType>"
            "<DataType>"
            "<List>"
            "<DataType>"
            "<Basic>Integer</Basic>"
            "</DataType>"
            "</List>"
            "</DataType>"
            "</AllowedTypes>"
        )

    async def test_should_serialize_multiline_xml(self):
        # Create constraint
        constraint = AllowedTypes(values=[Integer, List.create(Integer)])

        # Serialize
        xml = Serializer.serialize(constraint.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <AllowedTypes>
              <DataType>
                <Basic>Integer</Basic>
              </DataType>
              <DataType>
                <List>
                  <DataType>
                    <Basic>Integer</Basic>
                  </DataType>
                </List>
              </DataType>
            </AllowedTypes>
            """
        )


class TestDeserialize:
    async def test_should_raise_on_missing_data_type(self):
        # Create xml
        xml = "<AllowedTypes><DataType><Basic>Integer</Basic></DataType></AllowedTypes>"

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Missing 'data_type' in context.")):
            Deserializer.deserialize(xml, AllowedTypes.deserialize)

    async def test_should_raise_on_invalid_data_type(self):
        # Create xml
        xml = "<AllowedTypes><DataType><Basic>Integer</Basic></DataType></AllowedTypes>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape("Expected constraint's data type to be 'Any', received 'Boolean'."),
        ):
            Deserializer.deserialize(xml, AllowedTypes.deserialize, {"data_type": Boolean})

    async def test_should_deserialize_singleline_xml(self):
        # Create xml
        xml = (
            "<AllowedTypes>"
            "<DataType>"
            "<Basic>Integer</Basic>"
            "</DataType>"
            "<DataType>"
            "<List>"
            "<DataType>"
            "<Basic>Integer</Basic>"
            "</DataType>"
            "</List>"
            "</DataType>"
            "</AllowedTypes>"
        )

        # Deserialize
        constraint = Deserializer.deserialize(xml, AllowedTypes.deserialize, {"data_type": Any})

        # Assert that the method returns the correct value
        assert isinstance(constraint, AllowedTypes)
        assert len(constraint.values) == 2
        assert issubclass(constraint.values[0], Integer)
        assert issubclass(constraint.values[1], List)
        assert issubclass(constraint.values[1].data_type, Integer)

    async def test_should_deserialize_multiline_xml(self):
        # Create xml
        xml = """
        <AllowedTypes>
          <DataType>
            <Basic>Integer</Basic>
          </DataType>
          <DataType>
            <List>
              <DataType>
                <Basic>Integer</Basic>
              </DataType>
            </List>
          </DataType>
        </AllowedTypes>
        """

        # Deserialize
        constraint = Deserializer.deserialize(xml, AllowedTypes.deserialize, {"data_type": Any})

        # Assert that the method returns the correct value
        assert isinstance(constraint, AllowedTypes)
        assert len(constraint.values) == 2
        assert issubclass(constraint.values[0], Integer)
        assert issubclass(constraint.values[1], List)
        assert issubclass(constraint.values[1].data_type, Integer)
