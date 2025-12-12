import re
import textwrap

import pytest

from sila.framework.constraints.schema import Schema
from sila.framework.data_types.binary import Binary
from sila.framework.data_types.boolean import Boolean
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.string import String
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError
from sila.framework.fdl.serializer import Serializer


class TestInitialize:
    async def test_should_raise_on_missing_url_and_inline(self):
        # Create constraint
        with pytest.raises(ValueError, match=re.escape("Either 'url' or 'inline' must be provided.")):
            Schema(type="Xml")

    async def test_should_initialize_with_url(self):
        # Create constraint
        constraint = Schema(type="Json", url="https://json-schema.org/draft/2020-12/schema")

        # Assert that the method returns the correct value
        assert constraint.type == Schema.Type.JSON
        assert constraint.url == "https://json-schema.org/draft/2020-12/schema"
        assert constraint.inline is None

    async def test_should_initialize_with_inline(self):
        # Create constraint
        constraint = Schema(type=Schema.Type.JSON, inline="{}")

        # Assert that the method returns the correct value
        assert constraint.type == "Json"
        assert constraint.url is None
        assert constraint.inline == "{}"

    async def test_should_raise_on_both_url_and_inline(self):
        # Create constraint
        with pytest.raises(ValueError, match=re.escape("'url' and 'inline' cannot both be provided.")):
            Schema(type=Schema.Type.JSON, url="https://json-schema.org/draft/2020-12/schema", inline="{}")


class TestValidate:
    async def test_should_raise_on_invalid_type(self):
        # Create constraint
        constraint = Schema(type=Schema.Type.JSON, url="https://json-schema.org/draft/2020-12/schema")

        # Validate constraint
        with pytest.raises(
            TypeError, match=re.escape("Expected value of type 'String' or 'Binary', received 'Integer'.")
        ):
            await constraint.validate(Integer(42))

    @pytest.mark.skip(reason="Not implemented.")
    async def test_should_validate_json_string(self):
        # Create constraint
        constraint = Schema(type=Schema.Type.JSON, url="https://json-schema.org/draft/2020-12/schema")

        # Validate constraint
        assert await constraint.validate(String("")) is True

    @pytest.mark.skip(reason="Not implemented.")
    async def test_should_validate_json_bytes(self):
        # Create constraint
        constraint = Schema(type=Schema.Type.JSON, url="https://json-schema.org/draft/2020-12/schema")

        # Validate constraint
        assert await constraint.validate(Binary(b"")) is True

    @pytest.mark.skip(reason="Not implemented.")
    async def test_should_validate_xml_string(self):
        # Create constraint
        constraint = Schema(type=Schema.Type.XML, url="https://json-schema.org/draft/2020-12/schema")

        # Validate constraint
        assert await constraint.validate(String("")) is True

    @pytest.mark.skip(reason="Not implemented.")
    async def test_should_validate_xml_bytes(self):
        # Create constraint
        constraint = Schema(type=Schema.Type.XML, url="https://json-schema.org/draft/2020-12/schema")

        # Validate constraint
        assert await constraint.validate(Binary(b"")) is True


class TestSerialize:
    async def test_should_serialize_singleline_xml(self):
        # Create constraint
        constraint = Schema(type=Schema.Type.JSON, url="https://json-schema.org/draft/2020-12/schema")

        # Serialize
        xml = Serializer.serialize(constraint.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == "<Schema><Type>Json</Type><Url>https://json-schema.org/draft/2020-12/schema</Url></Schema>"

    async def test_should_serialize_multiline_xml(self):
        # Create constraint
        constraint = Schema(type=Schema.Type.JSON, url="https://json-schema.org/draft/2020-12/schema")

        # Serialize
        xml = Serializer.serialize(constraint.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <Schema>
              <Type>Json</Type>
              <Url>https://json-schema.org/draft/2020-12/schema</Url>
            </Schema>
            """
        )

    async def test_should_serialize_inline(self):
        # Create constraint
        constraint = Schema(type=Schema.Type.JSON, inline='{ "type": "string" }')

        # Serialize
        xml = Serializer.serialize(constraint.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == "<Schema><Type>Json</Type><Inline>{ &quot;type&quot;: &quot;string&quot; }</Inline></Schema>"


class TestDeserialize:
    async def test_should_raise_on_missing_data_type(self):
        # Create xml
        xml = "<Schema><Type>Json</Type><Url>https://json-schema.org/draft/2020-12/schema</Url></Schema>"

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Missing 'data_type' in context.")):
            Deserializer.deserialize(xml, Schema.deserialize)

    async def test_should_raise_on_invalid_data_type(self):
        # Create xml
        xml = "<Schema><Type>Json</Type><Url>https://json-schema.org/draft/2020-12/schema</Url></Schema>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape("Expected constraint's data type to be 'String' or 'Binary', received 'Boolean'."),
        ):
            Deserializer.deserialize(xml, Schema.deserialize, {"data_type": Boolean})

    async def test_should_deserialize_singleline_xml(self):
        # Create xml
        xml = "<Schema><Type>Json</Type><Url>https://json-schema.org/draft/2020-12/schema</Url></Schema>"

        # Deserialize
        constraint = Deserializer.deserialize(xml, Schema.deserialize, {"data_type": String})

        # Assert that the method returns the correct value
        assert constraint == Schema(type=Schema.Type.JSON, url="https://json-schema.org/draft/2020-12/schema")

    async def test_should_deserialize_multiline_xml(self):
        # Create xml
        xml = """
        <Schema>
          <Type>Json</Type>
          <Url>https://json-schema.org/draft/2020-12/schema</Url>
        </Schema>
        """

        # Deserialize
        constraint = Deserializer.deserialize(xml, Schema.deserialize, {"data_type": String})

        # Assert that the method returns the correct value
        assert constraint == Schema(type=Schema.Type.JSON, url="https://json-schema.org/draft/2020-12/schema")

    async def test_should_deserialize_inline(self):
        # Create xml
        xml = "<Schema><Type>Json</Type><Inline>{ &quot;type&quot;: &quot;string&quot; }</Inline></Schema>"

        # Deserialize
        constraint = Deserializer.deserialize(xml, Schema.deserialize, {"data_type": String})

        # Assert that the method returns the correct value
        assert constraint == Schema(type=Schema.Type.JSON, inline='{ "type": "string" }')

    async def test_should_raise_on_unexpected_characters(self):
        # Create xml
        xml = "<Schema><Type>Json</Type>Hello, World!</Schema>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape(
                "Expected start element with name 'Url' or 'Inline', received characters '['Hello, World!']'."
            ),
        ):
            Deserializer.deserialize(xml, Schema.deserialize, {"data_type": String})

    async def test_should_raise_on_unexpected_start_element(self):
        # Create xml
        xml = "<Schema><Type>Json</Type><Basic>String</Basic></Schema>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape(
                "Expected start element with name 'Url' or 'Inline', received start element with name 'Basic'."
            ),
        ):
            Deserializer.deserialize(xml, Schema.deserialize, {"data_type": String})

    async def test_should_raise_on_missing_url_or_inline(self):
        # Create xml
        xml = "<Schema><Type>Json</Type></Schema>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape(
                "Expected start element with name 'Url' or 'Inline', received end element with name 'Schema'."
            ),
        ):
            Deserializer.deserialize(xml, Schema.deserialize, {"data_type": String})

    async def test_should_raise_on_invalid_type(self):
        # Create xml
        xml = "<Schema><Type>Invalid</Type><Url>https://json-schema.org/draft/2020-12/schema</Url></Schema>"

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Expected a valid 'Type' value, received 'Invalid'.")):
            Deserializer.deserialize(xml, Schema.deserialize, {"data_type": String})
