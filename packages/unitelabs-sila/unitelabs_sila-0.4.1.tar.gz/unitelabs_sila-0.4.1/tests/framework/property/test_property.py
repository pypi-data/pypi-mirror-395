import re
import textwrap
import unittest.mock

import pytest

from sila.framework.common.feature import Feature
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.string import String
from sila.framework.errors.defined_execution_error import DefinedExecutionError
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.serializer import Serializer
from sila.framework.property.observable_property import ObservableProperty
from sila.framework.property.property import Property
from sila.framework.property.unobservable_property import UnobservableProperty


class TestInitialize:
    async def test_should_raise_on_invalid_identifier(self):
        # Create property
        with pytest.raises(
            ValueError, match=re.escape("Identifier must start with an upper-case letter, received ''.")
        ):
            Property(identifier="")

    async def test_should_raise_on_invalid_display_name(self):
        # Create property
        with pytest.raises(ValueError, match=re.escape("Display name must not be empty, received ''.")):
            Property(identifier="Property", display_name="")

    async def test_should_add_to_feature(self):
        # Create property
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")
        property_ = Property(identifier="TestProperty", display_name="Test Property", feature=feature)

        # Get fully qualified identifier
        assert property_.feature == feature
        assert feature.properties["TestProperty"] == property_


class TestFullyQualifiedIdentifier:
    async def test_should_raise_on_missing_feature(self):
        # Create property
        property_ = Property(identifier="TestProperty", display_name="Test Property")

        # Get fully qualified identifier
        with pytest.raises(
            RuntimeError,
            match=re.escape(
                "Unable to get fully qualified identifier for Property 'TestProperty' without feature association."
            ),
        ):
            assert property_.fully_qualified_identifier is None

    async def test_should_get_fully_qualified_identifier(self):
        # Create property
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")
        property_ = Property(identifier="TestProperty", display_name="Test Property", feature=feature)

        # Get fully qualified identifier
        assert property_.fully_qualified_identifier == "org.silastandard/none/SiLAService/v1/Property/TestProperty"


class TestAddToFeature:
    async def test_should_add_to_feature(self):
        # Create property
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")
        property_ = Property(identifier="TestProperty", display_name="Test Property")

        # Add to feature
        property_.add_to_feature(feature)

        # Assert that the method returns the correct value
        assert property_.feature == feature
        assert feature.properties["TestProperty"] == property_


class TestSerialize:
    async def test_should_serialize_unobservable_property(self):
        # Create property
        unobservable_property = UnobservableProperty(
            identifier="UnobservableProperty",
            display_name="Unobservable Property",
            description="Unobservable Property.",
            data_type=String,
        )

        # Serialize
        xml = Serializer.serialize(unobservable_property.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <Property>
              <Identifier>UnobservableProperty</Identifier>
              <DisplayName>Unobservable Property</DisplayName>
              <Description>Unobservable Property.</Description>
              <Observable>No</Observable>
              <DataType>
                <Basic>String</Basic>
              </DataType>
            </Property>
            """
        )

    async def test_should_serialize_observable_property(self):
        # Create property
        observable_property = ObservableProperty(
            identifier="ObservableProperty",
            display_name="Observable Property",
            description="Observable Property.",
            data_type=Integer,
        )

        # Serialize
        xml = Serializer.serialize(observable_property.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <Property>
              <Identifier>ObservableProperty</Identifier>
              <DisplayName>Observable Property</DisplayName>
              <Description>Observable Property.</Description>
              <Observable>Yes</Observable>
              <DataType>
                <Basic>Integer</Basic>
              </DataType>
            </Property>
            """
        )

    async def test_should_serialize_errors(self):
        # Create property
        error1 = DefinedExecutionError.create(
            identifier="Error1",
            display_name="Error 1",
            description="Error 1.",
        )
        error2 = DefinedExecutionError.create(
            identifier="Error2",
            display_name="Error 2",
            description="Error 2.",
        )
        unobservable_property = UnobservableProperty(
            identifier="UnobservableProperty",
            display_name="Unobservable Property",
            description="Unobservable Property.",
            data_type=String,
            errors={error1.identifier: error1, error2.identifier: error2},
        )

        # Serialize
        xml = Serializer.serialize(unobservable_property.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <Property>
              <Identifier>UnobservableProperty</Identifier>
              <DisplayName>Unobservable Property</DisplayName>
              <Description>Unobservable Property.</Description>
              <Observable>No</Observable>
              <DataType>
                <Basic>String</Basic>
              </DataType>
              <DefinedExecutionErrors>
                <Identifier>Error1</Identifier>
                <Identifier>Error2</Identifier>
              </DefinedExecutionErrors>
            </Property>
            """
        )


class TestDeserialize:
    async def test_should_deserialize_unobservable_property(self):
        # Create xml
        xml = """
        <Property>
          <Identifier>UnobservableProperty</Identifier>
          <DisplayName>Unobservable Property</DisplayName>
          <Description>Unobservable Property.</Description>
          <Observable>No</Observable>
          <DataType>
            <Basic>String</Basic>
          </DataType>
        </Property>
        """

        # Deserialize
        unobservable_property = Deserializer.deserialize(
            xml,
            Property.deserialize,
            {
                "unobservable_property_factory": UnobservableProperty,
            },
        )

        # Assert that the method returns the correct value
        assert unobservable_property == UnobservableProperty(
            identifier="UnobservableProperty",
            display_name="Unobservable Property",
            description="Unobservable Property.",
            data_type=String,
        )

    async def test_should_deserialize_observable_property(self):
        # Create xml
        xml = """
        <Property>
          <Identifier>ObservableProperty</Identifier>
          <DisplayName>Observable Property</DisplayName>
          <Description>Observable Property.</Description>
          <Observable>Yes</Observable>
          <DataType>
            <Basic>String</Basic>
          </DataType>
        </Property>
        """

        # Deserialize
        observable_property = Deserializer.deserialize(
            xml,
            Property.deserialize,
            {
                "observable_property_factory": ObservableProperty,
            },
        )

        # Assert that the method returns the correct value
        assert observable_property == ObservableProperty(
            identifier="ObservableProperty",
            display_name="Observable Property",
            description="Observable Property.",
            data_type=String,
        )

    async def test_should_deserialize_errors(self):
        # Create xml
        xml = """
        <Property>
          <Identifier>UnobservableProperty</Identifier>
          <DisplayName>Unobservable Property</DisplayName>
          <Description>Unobservable Property.</Description>
          <Observable>No</Observable>
          <DataType>
            <Basic>String</Basic>
          </DataType>
          <DefinedExecutionErrors>
            <Identifier>Error1</Identifier>
            <Identifier>Error2</Identifier>
          </DefinedExecutionErrors>
        </Property>
        """

        # Deserialize
        unobservable_property = Deserializer.deserialize(
            xml,
            Property.deserialize,
            {
                "unobservable_property_factory": UnobservableProperty,
            },
        )

        assert unobservable_property.errors.keys() == {"Error1", "Error2"}
        assert unobservable_property.errors["Error1"].identifier == "Error1"
        assert unobservable_property.errors["Error1"].display_name == "Error1"
        assert unobservable_property.errors["Error1"].description == ""
        assert unobservable_property.errors["Error2"].identifier == "Error2"
        assert unobservable_property.errors["Error2"].display_name == "Error2"
        assert unobservable_property.errors["Error2"].description == ""


class TestEquality:
    def test_should_be_true_on_equal_properties(self):
        # Create data type
        property_0 = Property(
            identifier="Property",
            display_name="Property",
            description="Property.",
            data_type=String,
        )
        property_1 = Property(
            identifier="Property",
            display_name="Property",
            description="Property.",
            data_type=String,
        )

        # Compare equality
        assert property_0 == property_1

    def test_should_be_false_on_unequal_properties(self):
        # Create data type
        property_0 = Property(
            identifier="Property1",
            display_name="Property1",
            description="Property1.",
            data_type=String,
        )
        property_1 = Property(
            identifier="Property2",
            display_name="Property2",
            description="Property2.",
            data_type=String,
        )

        # Compare equality
        assert property_0 != property_1

    def test_should_be_false_on_non_property(self):
        # Create data type
        property_ = Property(
            identifier="Property1",
            display_name="Property1",
            description="Property1.",
            data_type=String,
        )

        # Compare equality
        assert property_ != unittest.mock.Mock()
