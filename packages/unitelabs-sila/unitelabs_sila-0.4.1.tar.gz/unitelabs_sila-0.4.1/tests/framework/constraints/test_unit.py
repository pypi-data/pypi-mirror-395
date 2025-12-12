import re
import textwrap

import pytest

from sila.framework.constraints.unit import Unit, UnitComponent
from sila.framework.data_types.boolean import Boolean
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.real import Real
from sila.framework.data_types.string import String
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError
from sila.framework.fdl.serializer import Serializer


class TestInitialize:
    async def test_should_initialize(self):
        # Create constraint
        constraint = Unit(label="Length", components=[UnitComponent(unit="Meter")])

        # Assert that the method returns the correct value
        assert constraint.label == "Length"
        assert constraint.components == [UnitComponent(unit="Meter", exponent=1)]
        assert constraint.factor == 1.0
        assert constraint.offset == 0.0

    async def test_should_initialize_with_factor(self):
        # Create constraint
        constraint = Unit(label="Length", components=[UnitComponent(unit="Meter")], factor=3.3)

        # Assert that the method returns the correct value
        assert constraint.label == "Length"
        assert constraint.components == [UnitComponent(unit="Meter", exponent=1)]
        assert constraint.factor == 3.3
        assert constraint.offset == 0.0

    async def test_should_initialize_with_offset(self):
        # Create constraint
        constraint = Unit(label="Length", components=[UnitComponent(unit="Meter")], offset=3.3)

        # Assert that the method returns the correct value
        assert constraint.label == "Length"
        assert constraint.components == [UnitComponent(unit="Meter", exponent=1)]
        assert constraint.factor == 1.0
        assert constraint.offset == 3.3

    async def test_should_raise_on_invalid_label(self):
        # Create constraint
        with pytest.raises(ValueError, match=re.escape("The length of the label must not exceed 255 characters.")):
            Unit(label=" " * 256, components=[UnitComponent(unit="Meter")])


class TestValidate:
    async def test_should_raise_on_invalid_type(self):
        # Create constraint
        constraint = Unit(label="Length", components=[UnitComponent(unit="Meter")])

        # Validate constraint
        with pytest.raises(
            TypeError, match=re.escape("Expected value of type 'Integer' or 'Real', received 'String'.")
        ):
            await constraint.validate(String("Hello, World!"))

    async def test_should_validate_integer(self):
        # Create constraint
        constraint = Unit(label="Length", components=[UnitComponent(unit="Meter")])

        # Validate constraint
        assert await constraint.validate(Integer(42)) is True

    async def test_should_validate_real(self):
        # Create constraint
        constraint = Unit(label="Length", components=[UnitComponent(unit="Meter")])

        # Validate constraint
        assert await constraint.validate(Real(3.141592653589793)) is True


class TestSerialize:
    async def test_should_serialize_singleline_xml(self):
        # Create constraint
        constraint = Unit(label="nm", factor=1e-9, components=[Unit.Component(Unit.SI.METER)])

        # Serialize
        xml = Serializer.serialize(constraint.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == (
            "<Unit>"
            "<Label>nm</Label>"
            "<Factor>0.000000001</Factor>"
            "<Offset>0</Offset>"
            "<UnitComponent>"
            "<SIUnit>Meter</SIUnit>"
            "<Exponent>1</Exponent>"
            "</UnitComponent>"
            "</Unit>"
        )

    async def test_should_serialize_multiline_xml(self):
        # Create constraint
        constraint = Unit(label="ccm", factor=1e-6, components=[Unit.Component(Unit.SI.METER, exponent=3)])

        # Serialize
        xml = Serializer.serialize(constraint.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <Unit>
              <Label>ccm</Label>
              <Factor>0.000001</Factor>
              <Offset>0</Offset>
              <UnitComponent>
                <SIUnit>Meter</SIUnit>
                <Exponent>3</Exponent>
              </UnitComponent>
            </Unit>
            """
        )


class TestDeserialize:
    async def test_should_raise_on_missing_data_type(self):
        # Create xml
        xml = (
            "<Unit>"
            "<Label>nm</Label>"
            "<Factor>0.000000001</Factor>"
            "<Offset>0</Offset>"
            "<UnitComponent>"
            "<SIUnit>Meter</SIUnit>"
            "<Exponent>1</Exponent>"
            "</UnitComponent>"
            "</Unit>"
        )

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Missing 'data_type' in context.")):
            Deserializer.deserialize(xml, Unit.deserialize)

    async def test_should_raise_on_invalid_data_type(self):
        # Create xml
        xml = (
            "<Unit>"
            "<Label>nm</Label>"
            "<Factor>0.000000001</Factor>"
            "<Offset>0</Offset>"
            "<UnitComponent>"
            "<SIUnit>Meter</SIUnit>"
            "<Exponent>1</Exponent>"
            "</UnitComponent>"
            "</Unit>"
        )

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape("Expected constraint's data type to be 'Integer' or 'Real', received 'Boolean'."),
        ):
            Deserializer.deserialize(xml, Unit.deserialize, {"data_type": Boolean})

    async def test_should_deserialize_singleline_xml(self):
        # Create xml
        xml = (
            "<Unit>"
            "<Label>nm</Label>"
            "<Factor>0.000000001</Factor>"
            "<Offset>0</Offset>"
            "<UnitComponent>"
            "<SIUnit>Meter</SIUnit>"
            "<Exponent>1</Exponent>"
            "</UnitComponent>"
            "</Unit>"
        )

        # Deserialize
        constraint = Deserializer.deserialize(xml, Unit.deserialize, {"data_type": Integer})

        # Assert that the method returns the correct value
        assert constraint == Unit(label="nm", factor=1e-9, components=[Unit.Component(Unit.SI.METER)])

    async def test_should_deserialize_multiline_xml(self):
        # Create xml
        xml = """
        <Unit>
          <Label>ccm</Label>
          <Factor>0.000001</Factor>
          <Offset>0</Offset>
          <UnitComponent>
            <SIUnit>Meter</SIUnit>
            <Exponent>3</Exponent>
          </UnitComponent>
        </Unit>
        """

        # Deserialize
        constraint = Deserializer.deserialize(xml, Unit.deserialize, {"data_type": Integer})

        # Assert that the method returns the correct value
        assert constraint == Unit(label="ccm", factor=1e-6, components=[Unit.Component(Unit.SI.METER, exponent=3)])

    async def test_should_deserialize_offset(self):
        # Create xml
        xml = """
        <Unit>
          <Label>°C</Label>
          <Factor>1</Factor>
          <Offset>273.15</Offset>
          <UnitComponent>
            <SIUnit>Kelvin</SIUnit>
            <Exponent>1</Exponent>
          </UnitComponent>
        </Unit>
        """

        # Deserialize
        constraint = Deserializer.deserialize(xml, Unit.deserialize, {"data_type": Integer})

        # Assert that the method returns the correct value
        assert constraint == Unit(label="°C", offset=273.15, components=[Unit.Component(Unit.SI.KELVIN)])

    async def test_should_deserialize_multiple_components(self):
        # Create xml
        xml = """
        <Unit>
          <Label>N</Label>
          <Factor>1</Factor>
          <Offset>0</Offset>
          <UnitComponent>
            <SIUnit>Kilogram</SIUnit>
            <Exponent>1</Exponent>
          </UnitComponent>
          <UnitComponent>
            <SIUnit>Meter</SIUnit>
            <Exponent>1</Exponent>
          </UnitComponent>
          <UnitComponent>
            <SIUnit>Second</SIUnit>
            <Exponent>-2</Exponent>
          </UnitComponent>
        </Unit>
        """

        # Deserialize
        constraint = Deserializer.deserialize(xml, Unit.deserialize, {"data_type": Integer})

        # Assert that the method returns the correct value
        assert constraint == Unit(
            label="N",
            components=[
                Unit.Component(Unit.SI.KILOGRAM),
                Unit.Component(Unit.SI.METER),
                Unit.Component(Unit.SI.SECOND, exponent=-2),
            ],
        )

    async def test_should_raise_on_unexpected_characters(self):
        # Create xml
        xml = "<Unit><Label>m</Label><Factor>1</Factor><Offset>0</Offset>Hello, World!</Unit>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape(
                "Expected start element with name 'UnitComponent', received characters '['Hello, World!']'."
            ),
        ):
            Deserializer.deserialize(xml, Unit.deserialize, {"data_type": Integer})

    async def test_should_raise_on_unexpected_start_element(self):
        # Create xml
        xml = "<Unit><Label>m</Label><Factor>1</Factor><Offset>0</Offset><SIUnit>Meter</SIUnit></Unit>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape(
                "Expected start element with name 'UnitComponent', received start element with name 'SIUnit'."
            ),
        ):
            Deserializer.deserialize(xml, Unit.deserialize, {"data_type": Integer})

    async def test_should_raise_on_missing_component(self):
        # Create xml
        xml = "<Unit><Label>m</Label><Factor>1</Factor><Offset>0</Offset></Unit>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape("Expected at least one 'UnitComponent' element inside the 'Unit' element."),
        ):
            Deserializer.deserialize(xml, Unit.deserialize, {"data_type": Integer})

    async def test_should_raise_on_invalid_factor(self):
        # Create xml
        xml = (
            "<Unit>"
            "<Label>m</Label>"
            "<Factor>X</Factor>"
            "<Offset>0</Offset>"
            "<UnitComponent><SIUnit>Meter</SIUnit><Exponent>1</Exponent></UnitComponent>"
            "</Unit>"
        )

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Could not convert 'Factor' with value 'X' to Real.")):
            Deserializer.deserialize(xml, Unit.deserialize, {"data_type": Integer})

    async def test_should_raise_on_invalid_offset(self):
        # Create xml
        xml = (
            "<Unit>"
            "<Label>m</Label>"
            "<Factor>1</Factor>"
            "<Offset>X</Offset>"
            "<UnitComponent><SIUnit>Meter</SIUnit><Exponent>1</Exponent></UnitComponent>"
            "</Unit>"
        )

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Could not convert 'Offset' with value 'X' to Real.")):
            Deserializer.deserialize(xml, Unit.deserialize, {"data_type": Integer})

    async def test_should_raise_on_invalid_siunit(self):
        # Create xml
        xml = (
            "<Unit>"
            "<Label>m</Label>"
            "<Factor>1</Factor>"
            "<Offset>0</Offset>"
            "<UnitComponent><SIUnit>Test</SIUnit><Exponent>1</Exponent></UnitComponent>"
            "</Unit>"
        )

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Expected a valid 'SIUnit' value, received 'Test'.")):
            Deserializer.deserialize(xml, Unit.deserialize, {"data_type": Integer})

    async def test_should_raise_on_invalid_exponent(self):
        # Create xml
        xml = (
            "<Unit>"
            "<Label>m</Label>"
            "<Factor>1</Factor>"
            "<Offset>0</Offset>"
            "<UnitComponent><SIUnit>Meter</SIUnit><Exponent>X</Exponent></UnitComponent>"
            "</Unit>"
        )

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Could not convert 'Exponent' with value 'X' to Integer.")):
            Deserializer.deserialize(xml, Unit.deserialize, {"data_type": Integer})
