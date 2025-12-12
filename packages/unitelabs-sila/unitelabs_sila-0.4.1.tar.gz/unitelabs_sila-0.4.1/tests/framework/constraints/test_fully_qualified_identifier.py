import re

import pytest
import typing_extensions as typing

from sila.framework.constraints.fully_qualified_identifier import FullyQualifiedIdentifier
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.string import String
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError
from sila.framework.fdl.serializer import Serializer


class TestInitialize:
    async def test_should_initialize(self):
        # Create constraint
        constraint = FullyQualifiedIdentifier("FeatureIdentifier")

        # Assert that the method returns the correct value
        assert constraint.value == FullyQualifiedIdentifier.Type.FEATURE_IDENTIFIER

    async def test_should_initialize_with_type(self):
        # Create constraint
        constraint = FullyQualifiedIdentifier(FullyQualifiedIdentifier.Type.PROPERTY_IDENTIFIER)

        # Assert that the method returns the correct value
        assert constraint.value == "PropertyIdentifier"

    async def test_should_raise_on_invalid_type(self):
        # Create constraint
        with pytest.raises(ValueError, match=re.escape("Identifier type must be valid type, received 'Unknown'.")):
            FullyQualifiedIdentifier("Unknown")  # type: ignore


class TestValidate:
    async def test_should_raise_on_invalid_type(self):
        # Create constraint
        constraint = FullyQualifiedIdentifier("FeatureIdentifier")

        # Validate constraint
        with pytest.raises(TypeError, match=re.escape("Expected value of type 'String', received 'Integer'.")):
            await constraint.validate(typing.cast(String, Integer(42)))

    async def test_should_validate_string(self):
        # Create constraint
        constraint = FullyQualifiedIdentifier("FeatureIdentifier")

        # Validate constraint
        assert await constraint.validate(String("org.silastandard/core/SiLAService/v1")) is True

    async def test_should_raise_on_invalid_string(self):
        # Create constraint
        constraint = FullyQualifiedIdentifier("FeatureIdentifier")

        # Validate constraint
        with pytest.raises(
            ValueError, match=re.escape("Expected value with format for a 'FeatureIdentifier', received 'Invalid'.")
        ):
            await constraint.validate(String("Invalid"))


class TestSerialize:
    async def test_should_serialize_xml(self):
        # Create constraint
        constraint = FullyQualifiedIdentifier("FeatureIdentifier")

        # Serialize
        xml = Serializer.serialize(constraint.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == "<FullyQualifiedIdentifier>FeatureIdentifier</FullyQualifiedIdentifier>"


class TestDeserialize:
    async def test_should_raise_on_missing_data_type(self):
        # Create xml
        xml = "<FullyQualifiedIdentifier>FeatureIdentifier</FullyQualifiedIdentifier>"

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Missing 'data_type' in context.")):
            Deserializer.deserialize(xml, FullyQualifiedIdentifier.deserialize)

    async def test_should_raise_on_invalid_data_type(self):
        # Create xml
        xml = "<FullyQualifiedIdentifier>FeatureIdentifier</FullyQualifiedIdentifier>"

        # Deserialize
        with pytest.raises(
            ParseError, match=re.escape("Expected constraint's data type to be 'String', received 'Integer'.")
        ):
            Deserializer.deserialize(xml, FullyQualifiedIdentifier.deserialize, {"data_type": Integer})

    async def test_should_deserialize_xml(self):
        # Create xml
        xml = "<FullyQualifiedIdentifier>FeatureIdentifier</FullyQualifiedIdentifier>"

        # Deserialize
        constraint = Deserializer.deserialize(xml, FullyQualifiedIdentifier.deserialize, {"data_type": String})

        # Assert that the method returns the correct value
        assert constraint == FullyQualifiedIdentifier("FeatureIdentifier")

    async def test_should_raise_on_invalid_value(self):
        # Create xml
        xml = "<FullyQualifiedIdentifier>X</FullyQualifiedIdentifier>"

        # Deserialize
        with pytest.raises(
            ParseError, match=re.escape("Expected a valid 'FullyQualifiedIdentifier' value, received 'X'.")
        ):
            Deserializer.deserialize(xml, FullyQualifiedIdentifier.deserialize, {"data_type": String})
