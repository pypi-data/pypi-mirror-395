import re

import pytest

from sila.framework.data_types.boolean import Boolean
from sila.framework.data_types.data_type import DataType
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError


class TestDeserialize:
    async def test_should_deserialize_singleline_xml(self):
        # Create xml
        xml = "<DataType><Basic>Boolean</Basic></DataType>"

        # Deserialize
        data_type = Deserializer.deserialize(xml, DataType.deserialize)

        # Assert that the method returns the correct value
        assert data_type == Boolean

    async def test_should_deserialize_multiline_xml(self):
        # Create xml
        xml = """
        <DataType>
            <Basic>Boolean</Basic>
        </DataType>
        """

        # Deserialize
        data_type = Deserializer.deserialize(xml, DataType.deserialize)

        # Assert that t`he method returns the correct value
        assert data_type == Boolean

    async def test_should_raise_on_unknown_data_type(self):
        # Create xml
        xml = "<DataType><Complex>Complex</Complex></DataType>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape(
                "Expected start element with name 'Basic', 'List', 'Structure', 'Constrained' "
                "or 'DataTypeIdentifier', received start element with name 'Complex'."
            ),
        ):
            Deserializer.deserialize(xml, DataType.deserialize)

    async def test_should_raise_on_missing_data_type(self):
        # Create xml
        xml = "<DataType></DataType>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape(
                "Expected start element with name 'Basic', 'List', 'Structure', 'Constrained' "
                "or 'DataTypeIdentifier', received end element with name 'DataType'."
            ),
        ):
            Deserializer.deserialize(xml, DataType.deserialize)

    async def test_should_raise_on_invalid_syntax(self):
        # Create xml
        xml = "<DataType>Boolean</DataType>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape(
                "Expected start element with name 'Basic', 'List', 'Structure', 'Constrained' "
                "or 'DataTypeIdentifier', received token 'Characters(value=['Boolean'])'."
            ),
        ):
            Deserializer.deserialize(xml, DataType.deserialize)
