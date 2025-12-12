import re

import pytest

from sila.framework.constraints.maximal_length import MaximalLength
from sila.framework.data_types.binary import Binary
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.string import String
from sila.framework.data_types.structure import Structure
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError
from sila.framework.fdl.serializer import Serializer


class TestInitialize:
    async def test_should_initialize(self):
        # Create constraint
        constraint = MaximalLength(0)

        # Assert that the method returns the correct value
        assert constraint.value == 0

    async def test_should_raise_on_negative_value(self):
        # Create constraint
        with pytest.raises(
            ValueError, match=re.escape("Maximal length must be a non-negative integer, received '-1'.")
        ):
            MaximalLength(-1)

    async def test_should_raise_on_invalid_value(self):
        # Create constraint
        with pytest.raises(
            ValueError, match=re.escape("Maximal length must be less than 2⁶³, received '9223372036854775808'.")
        ):
            MaximalLength(2**63)


class TestValidate:
    async def test_should_raise_on_invalid_type(self):
        # Create constraint
        constraint = MaximalLength(0)

        # Validate constraint
        with pytest.raises(
            TypeError, match=re.escape("Expected value of type 'String' or 'Binary', received 'Structure'.")
        ):
            await constraint.validate(Structure())

    @pytest.mark.parametrize(("value"), ["", "1", "12"])
    async def test_should_validate_string(self, value: str):
        # Create constraint
        constraint = MaximalLength(2)

        # Validate constraint
        assert await constraint.validate(String(value)) is True

    @pytest.mark.parametrize(("value"), ["123"])
    async def test_should_raise_on_invalid_string(self, value: str):
        # Create constraint
        constraint = MaximalLength(2)

        # Validate constraint
        with pytest.raises(
            ValueError, match=re.escape(f"Expected value with maximal length '2', received '{len(value)}'.")
        ):
            await constraint.validate(String(value))

    @pytest.mark.parametrize(("value"), [b"", b"1", b"12"])
    async def test_should_validate_binary(self, value: bytes):
        # Create constraint
        constraint = MaximalLength(2)

        # Validate constraint
        assert await constraint.validate(Binary(value)) is True

    @pytest.mark.parametrize(("value"), [b"123", b"1234"])
    async def test_should_raise_on_invalid_binary(self, value: bytes):
        # Create constraint
        constraint = MaximalLength(2)

        # Validate constraint
        with pytest.raises(
            ValueError, match=re.escape(f"Expected value with maximal length '2', received '{len(value)}'.")
        ):
            await constraint.validate(Binary(value))


class TestSerialize:
    async def test_should_serialize_xml(self):
        # Create constraint
        constraint = MaximalLength(2)

        # Serialize
        xml = Serializer.serialize(constraint.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == "<MaximalLength>2</MaximalLength>"


class TestDeserialize:
    async def test_should_raise_on_missing_data_type(self):
        # Create xml
        xml = "<MaximalLength>2</MaximalLength>"

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Missing 'data_type' in context.")):
            Deserializer.deserialize(xml, MaximalLength.deserialize)

    async def test_should_raise_on_invalid_data_type(self):
        # Create xml
        xml = "<MaximalLength>2</MaximalLength>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape("Expected constraint's data type to be 'String' or 'Binary', received 'Integer'."),
        ):
            Deserializer.deserialize(xml, MaximalLength.deserialize, {"data_type": Integer})

    async def test_should_deserialize_xml(self):
        # Create xml
        xml = "<MaximalLength>2</MaximalLength>"

        # Deserialize
        constraint = Deserializer.deserialize(xml, MaximalLength.deserialize, {"data_type": String})

        # Assert that the method returns the correct value
        assert constraint == MaximalLength(2)

    async def test_should_raise_on_invalid_value(self):
        # Create xml
        xml = "<MaximalLength>X</MaximalLength>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape("Could not convert 'MaximalLength' with value 'X' to Integer."),
        ):
            Deserializer.deserialize(xml, MaximalLength.deserialize, {"data_type": String})
