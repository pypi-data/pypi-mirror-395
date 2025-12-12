import re
import textwrap

import pytest

from sila.framework.constraints.content_type import ContentType
from sila.framework.data_types.binary import Binary
from sila.framework.data_types.boolean import Boolean
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.string import String
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError
from sila.framework.fdl.serializer import Serializer


class TestInitialize:
    async def test_should_initialize(self):
        # Create constraint
        constraint = ContentType(ctype="text", subtype="html")

        # Assert that the method returns the correct value
        assert constraint.type == "text"
        assert constraint.subtype == "html"
        assert constraint.media_type == "text/html"

    async def test_should_initialize_with_parameters(self):
        # Create constraint
        constraint = ContentType(
            ctype="application",
            subtype="json",
            parameters=[("charset", "utf-8"), ContentType.Parameter("boundary", "Example")],
        )

        # Assert that the method returns the correct value
        assert constraint.type == "application"
        assert constraint.subtype == "json"
        assert constraint.media_type == "application/json; charset=utf-8; boundary=Example"


class TestValidate:
    async def test_should_raise_on_invalid_type(self):
        # Create constraint
        constraint = ContentType(ctype="application", subtype="json")

        # Validate constraint
        with pytest.raises(
            TypeError, match=re.escape("Expected value of type 'String' or 'Binary', received 'Integer'.")
        ):
            await constraint.validate(Integer(42))

    async def test_should_validate_string(self):
        # Create constraint
        constraint = ContentType(ctype="application", subtype="json")

        # Validate constraint
        assert await constraint.validate(String("")) is True

    async def test_should_validate_binary(self):
        # Create constraint
        constraint = ContentType(ctype="application", subtype="json")

        # Validate constraint
        assert await constraint.validate(Binary(b"")) is True


class TestSerialize:
    async def test_should_serialize_singleline_xml(self):
        # Create constraint
        constraint = ContentType(ctype="application", subtype="json")

        # Serialize
        xml = Serializer.serialize(constraint.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == "<ContentType><Type>application</Type><Subtype>json</Subtype></ContentType>"

    async def test_should_serialize_multiline_xml(self):
        # Create constraint
        constraint = ContentType(
            ctype="application",
            subtype="json",
            parameters=[("charset", "utf-8"), ContentType.Parameter("boundary", "Example")],
        )

        # Serialize
        xml = Serializer.serialize(constraint.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <ContentType>
              <Type>application</Type>
              <Subtype>json</Subtype>
              <Parameters>
                <Parameter>
                  <Attribute>charset</Attribute>
                  <Value>utf-8</Value>
                </Parameter>
                <Parameter>
                  <Attribute>boundary</Attribute>
                  <Value>Example</Value>
                </Parameter>
              </Parameters>
            </ContentType>
            """
        )


class TestDeserialize:
    async def test_should_raise_on_missing_data_type(self):
        # Create xml
        xml = "<ContentType><Type>application</Type><Subtype>json</Subtype></ContentType>"

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Missing 'data_type' in context.")):
            Deserializer.deserialize(xml, ContentType.deserialize)

    async def test_should_raise_on_invalid_data_type(self):
        # Create xml
        xml = "<ContentType><Type>application</Type><Subtype>json</Subtype></ContentType>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape("Expected constraint's data type to be 'String' or 'Binary', received 'Boolean'."),
        ):
            Deserializer.deserialize(xml, ContentType.deserialize, {"data_type": Boolean})

    async def test_should_deserialize_singleline_xml(self):
        # Create xml
        xml = "<ContentType><Type>application</Type><Subtype>json</Subtype></ContentType>"

        # Deserialize
        constraint = Deserializer.deserialize(xml, ContentType.deserialize, {"data_type": String})

        # Assert that the method returns the correct value
        assert constraint == ContentType(ctype="application", subtype="json")

    async def test_should_deserialize_multiline_xml(self):
        # Create xml
        xml = """
        <ContentType>
          <Type>application</Type>
          <Subtype>json</Subtype>
          <Parameters>
            <Parameter>
              <Attribute>charset</Attribute>
              <Value>utf-8</Value>
            </Parameter>
            <Parameter>
              <Attribute>boundary</Attribute>
              <Value>Example</Value>
            </Parameter>
          </Parameters>
        </ContentType>
        """

        # Deserialize
        constraint = Deserializer.deserialize(xml, ContentType.deserialize, {"data_type": String})

        # Assert that the method returns the correct value
        assert constraint == ContentType(
            ctype="application",
            subtype="json",
            parameters=[("charset", "utf-8"), ContentType.Parameter("boundary", "Example")],
        )

    async def test_should_raise_on_unexpected_characters(self):
        # Create xml
        xml = "<ContentType><Type>application</Type><Subtype>json</Subtype>Hello, World!</ContentType>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape(
                "Expected start element with name 'Parameters' or end element with name 'ContentType', "
                "received characters '['Hello, World!']'.",
            ),
        ):
            Deserializer.deserialize(xml, ContentType.deserialize, {"data_type": String})

    async def test_should_raise_on_unexpected_start_element(self):
        # Create xml
        xml = "<ContentType><Type>application</Type><Subtype>json</Subtype><Parameter>Value</Parameter></ContentType>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape(
                "Expected start element with name 'Parameters', received start element with name 'Parameter'.",
            ),
        ):
            Deserializer.deserialize(xml, ContentType.deserialize, {"data_type": String})

    async def test_should_raise_on_missing_parameters(self):
        # Create xml
        xml = "<ContentType><Type>application</Type><Subtype>json</Subtype><Parameters></Parameters></ContentType>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape("Expected at least one 'Parameter' element inside the 'ContentType' element."),
        ):
            Deserializer.deserialize(xml, ContentType.deserialize, {"data_type": String})

    async def test_should_raise_on_unexpected_characters_in_parameters(self):
        # Create xml
        xml = (
            "<ContentType>"
            "<Type>application</Type>"
            "<Subtype>json</Subtype>"
            "<Parameters>Hello, World!</Parameters>"
            "</ContentType>"
        )

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape("Expected start element with name 'Parameter', received characters '['Hello, World!']'."),
        ):
            Deserializer.deserialize(xml, ContentType.deserialize, {"data_type": String})

    async def test_should_raise_on_unexpected_start_element_in_parameters(self):
        # Create xml
        xml = (
            "<ContentType>"
            "<Type>application</Type>"
            "<Subtype>json</Subtype>"
            "<Parameters><Attribute></Attribute></Parameters>"
            "</ContentType>"
        )

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape(
                "Expected start element with name 'Parameter', received start element with name 'Attribute'."
            ),
        ):
            Deserializer.deserialize(xml, ContentType.deserialize, {"data_type": String})
