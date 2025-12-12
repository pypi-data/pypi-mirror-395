import re

import pytest
import typing_extensions as typing

from sila.framework.constraints.maximal_element_count import MaximalElementCount
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.list import List
from sila.framework.data_types.structure import Structure
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError
from sila.framework.fdl.serializer import Serializer


class TestInitialize:
    async def test_should_initialize(self):
        # Create constraint
        constraint = MaximalElementCount(0)

        # Assert that the method returns the correct value
        assert constraint.value == 0

    async def test_should_raise_on_negative_value(self):
        # Create constraint
        with pytest.raises(
            ValueError, match=re.escape("Maximal element count must be a non-negative integer, received '-1'.")
        ):
            MaximalElementCount(-1)

    async def test_should_raise_on_invalid_value(self):
        # Create constraint
        with pytest.raises(
            ValueError, match=re.escape("Maximal element count must be less than 2⁶³, received '9223372036854775808'.")
        ):
            MaximalElementCount(2**63)


class TestValidate:
    async def test_should_raise_on_invalid_type(self):
        # Create constraint
        constraint = MaximalElementCount(0)

        # Validate constraint
        with pytest.raises(TypeError, match=re.escape("Expected value of type 'List', received 'Structure'.")):
            await constraint.validate(typing.cast(List, Structure()))

    @pytest.mark.parametrize(("value"), [List(), List([Integer(1)]), List([Integer(1), Integer(2)])])
    async def test_should_validate_list(self, value: List):
        # Create constraint
        constraint = MaximalElementCount(2)

        # Validate constraint
        assert await constraint.validate(value) is True

    @pytest.mark.parametrize(("value"), [List([Integer(1), Integer(2), Integer(3)])])
    async def test_should_raise_on_invalid_list(self, value: List):
        # Create constraint
        constraint = MaximalElementCount(2)

        # Validate constraint
        with pytest.raises(
            ValueError, match=re.escape(f"Expected list with maximal element count '2', received '{len(value.value)}'.")
        ):
            await constraint.validate(value)


class TestSerialize:
    async def test_should_serialize_xml(self):
        # Create constraint
        constraint = MaximalElementCount(2)

        # Serialize
        xml = Serializer.serialize(constraint.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == "<MaximalElementCount>2</MaximalElementCount>"


class TestDeserialize:
    async def test_should_raise_on_missing_data_type(self):
        # Create xml
        xml = "<MaximalElementCount>2</MaximalElementCount>"

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Missing 'data_type' in context.")):
            Deserializer.deserialize(xml, MaximalElementCount.deserialize)

    async def test_should_raise_on_invalid_data_type(self):
        # Create xml
        xml = "<MaximalElementCount>2</MaximalElementCount>"

        # Deserialize
        with pytest.raises(
            ParseError, match=re.escape("Expected constraint's data type to be 'List', received 'Integer'.")
        ):
            Deserializer.deserialize(xml, MaximalElementCount.deserialize, {"data_type": Integer})

    async def test_should_deserialize_xml(self):
        # Create xml
        xml = "<MaximalElementCount>2</MaximalElementCount>"

        # Deserialize
        constraint = Deserializer.deserialize(xml, MaximalElementCount.deserialize, {"data_type": List})

        # Assert that the method returns the correct value
        assert constraint == MaximalElementCount(2)

    async def test_should_raise_on_invalid_value(self):
        # Create xml
        xml = "<MaximalElementCount>X</MaximalElementCount>"

        # Deserialize
        with pytest.raises(
            ParseError, match=re.escape("Could not convert 'MaximalElementCount' with value 'X' to Integer.")
        ):
            Deserializer.deserialize(xml, MaximalElementCount.deserialize, {"data_type": List})
