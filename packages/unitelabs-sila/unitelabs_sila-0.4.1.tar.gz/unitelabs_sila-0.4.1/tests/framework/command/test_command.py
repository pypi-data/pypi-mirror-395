import re
import textwrap
import unittest.mock

import pytest

from sila.framework.command.command import Command
from sila.framework.command.observable_command import ObservableCommand
from sila.framework.command.unobservable_command import UnobservableCommand
from sila.framework.common.feature import Feature
from sila.framework.data_types.element import Element
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.string import String
from sila.framework.errors.defined_execution_error import DefinedExecutionError
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError
from sila.framework.fdl.serializer import Serializer


class TestInitialize:
    async def test_should_raise_on_invalid_identifier(self):
        # Create command
        with pytest.raises(
            ValueError, match=re.escape("Identifier must start with an upper-case letter, received ''.")
        ):
            Command(identifier="")

    async def test_should_raise_on_invalid_display_name(self):
        # Create command
        with pytest.raises(ValueError, match=re.escape("Display name must not be empty, received ''.")):
            Command(identifier="Command", display_name="")

    async def test_should_add_to_feature(self):
        # Create command
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")
        command = Command(identifier="TestCommand", display_name="Test Command", feature=feature)

        # Get fully qualified identifier
        assert command.feature == feature
        assert feature.commands["TestCommand"] == command


class TestFullyQualifiedIdentifier:
    async def test_should_raise_on_missing_feature(self):
        # Create command
        command = Command(identifier="TestCommand", display_name="Test Command")

        # Get fully qualified identifier
        with pytest.raises(
            RuntimeError,
            match=re.escape(
                "Unable to get fully qualified identifier for Command 'TestCommand' without feature association."
            ),
        ):
            assert command.fully_qualified_identifier is None

    async def test_should_get_fully_qualified_identifier(self):
        # Create command
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")
        command = Command(identifier="TestCommand", display_name="Test Command", feature=feature)

        # Get fully qualified identifier
        assert command.fully_qualified_identifier == "org.silastandard/none/SiLAService/v1/Command/TestCommand"


class TestAddToFeature:
    async def test_should_add_to_feature(self):
        # Create command
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")
        command = Command(identifier="TestCommand", display_name="Test Command")

        # Add to feature
        command.add_to_feature(feature)

        # Assert that the method returns the correct value
        assert command.feature == feature
        assert feature.commands["TestCommand"] == command


class TestSerialize:
    async def test_should_serialize_unobservable_command(self):
        # Create command
        unobservable_command = UnobservableCommand(
            identifier="UnobservableCommand",
            display_name="Unobservable Command",
            description="Unobservable Command.",
        )

        # Serialize
        xml = Serializer.serialize(unobservable_command.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <Command>
              <Identifier>UnobservableCommand</Identifier>
              <DisplayName>Unobservable Command</DisplayName>
              <Description>Unobservable Command.</Description>
              <Observable>No</Observable>
            </Command>
            """
        )

    async def test_should_serialize_parameters(self):
        # Create command
        observable_command = ObservableCommand(
            identifier="ObservableCommand",
            display_name="Observable Command",
            description="Observable Command.",
            parameters={
                "string_value": Element(
                    identifier="StringValue", display_name="String Value", description="String Value.", data_type=String
                ),
                "integer_value": Element(
                    identifier="IntegerValue",
                    display_name="Integer Value",
                    description="Integer Value.",
                    data_type=Integer,
                ),
            },
        )

        # Serialize
        xml = Serializer.serialize(observable_command.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <Command>
              <Identifier>ObservableCommand</Identifier>
              <DisplayName>Observable Command</DisplayName>
              <Description>Observable Command.</Description>
              <Observable>Yes</Observable>
              <Parameter>
                <Identifier>StringValue</Identifier>
                <DisplayName>String Value</DisplayName>
                <Description>String Value.</Description>
                <DataType>
                  <Basic>String</Basic>
                </DataType>
              </Parameter>
              <Parameter>
                <Identifier>IntegerValue</Identifier>
                <DisplayName>Integer Value</DisplayName>
                <Description>Integer Value.</Description>
                <DataType>
                  <Basic>Integer</Basic>
                </DataType>
              </Parameter>
            </Command>
            """
        )

    async def test_should_serialize_responses(self):
        # Create command
        observable_command = ObservableCommand(
            identifier="ObservableCommand",
            display_name="Observable Command",
            description="Observable Command.",
            responses={
                "received_string": Element(
                    identifier="ReceivedString",
                    display_name="Received String",
                    description="Received String.",
                    data_type=String,
                ),
                "received_integer": Element(
                    identifier="ReceivedInteger",
                    display_name="Received Integer",
                    description="Received Integer.",
                    data_type=Integer,
                ),
            },
        )

        # Serialize
        xml = Serializer.serialize(observable_command.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <Command>
              <Identifier>ObservableCommand</Identifier>
              <DisplayName>Observable Command</DisplayName>
              <Description>Observable Command.</Description>
              <Observable>Yes</Observable>
              <Response>
                <Identifier>ReceivedString</Identifier>
                <DisplayName>Received String</DisplayName>
                <Description>Received String.</Description>
                <DataType>
                  <Basic>String</Basic>
                </DataType>
              </Response>
              <Response>
                <Identifier>ReceivedInteger</Identifier>
                <DisplayName>Received Integer</DisplayName>
                <Description>Received Integer.</Description>
                <DataType>
                  <Basic>Integer</Basic>
                </DataType>
              </Response>
            </Command>
            """
        )

    async def test_should_serialize_intermediate_responses(self):
        # Create command
        observable_command = ObservableCommand(
            identifier="ObservableCommand",
            display_name="Observable Command",
            description="Observable Command.",
            intermediate_responses={
                "intermediate_integer": Element(
                    identifier="IntermediateInteger",
                    display_name="Intermediate Integer",
                    description="Intermediate Integer.",
                    data_type=Integer,
                ),
            },
        )

        # Serialize
        xml = Serializer.serialize(observable_command.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <Command>
              <Identifier>ObservableCommand</Identifier>
              <DisplayName>Observable Command</DisplayName>
              <Description>Observable Command.</Description>
              <Observable>Yes</Observable>
              <IntermediateResponse>
                <Identifier>IntermediateInteger</Identifier>
                <DisplayName>Intermediate Integer</DisplayName>
                <Description>Intermediate Integer.</Description>
                <DataType>
                  <Basic>Integer</Basic>
                </DataType>
              </IntermediateResponse>
            </Command>
            """
        )

    async def test_should_serialize_errors(self):
        # Create command
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
        unobservable_command = UnobservableCommand(
            identifier="UnobservableCommand",
            display_name="Unobservable Command",
            description="Unobservable Command.",
            errors={error1.identifier: error1, error2.identifier: error2},
        )

        # Serialize
        xml = Serializer.serialize(unobservable_command.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <Command>
              <Identifier>UnobservableCommand</Identifier>
              <DisplayName>Unobservable Command</DisplayName>
              <Description>Unobservable Command.</Description>
              <Observable>No</Observable>
              <DefinedExecutionErrors>
                <Identifier>Error1</Identifier>
                <Identifier>Error2</Identifier>
              </DefinedExecutionErrors>
            </Command>
            """
        )

    async def test_should_serialize_observable_command(self):
        # Create command
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
        observable_command = ObservableCommand(
            identifier="ObservableCommand",
            display_name="Observable Command",
            description="Observable Command.",
            parameters={
                "string_value": Element(
                    identifier="StringValue", display_name="String Value", description="String Value.", data_type=String
                ),
                "integer_value": Element(
                    identifier="IntegerValue",
                    display_name="Integer Value",
                    description="Integer Value.",
                    data_type=Integer,
                ),
            },
            responses={
                "received_string": Element(
                    identifier="ReceivedString",
                    display_name="Received String",
                    description="Received String.",
                    data_type=String,
                ),
                "received_integer": Element(
                    identifier="ReceivedInteger",
                    display_name="Received Integer",
                    description="Received Integer.",
                    data_type=Integer,
                ),
            },
            intermediate_responses={
                "intermediate_integer": Element(
                    identifier="IntermediateInteger",
                    display_name="Intermediate Integer",
                    description="Intermediate Integer.",
                    data_type=Integer,
                ),
            },
            errors={error1.identifier: error1, error2.identifier: error2},
        )

        # Serialize
        xml = Serializer.serialize(observable_command.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <Command>
              <Identifier>ObservableCommand</Identifier>
              <DisplayName>Observable Command</DisplayName>
              <Description>Observable Command.</Description>
              <Observable>Yes</Observable>
              <Parameter>
                <Identifier>StringValue</Identifier>
                <DisplayName>String Value</DisplayName>
                <Description>String Value.</Description>
                <DataType>
                  <Basic>String</Basic>
                </DataType>
              </Parameter>
              <Parameter>
                <Identifier>IntegerValue</Identifier>
                <DisplayName>Integer Value</DisplayName>
                <Description>Integer Value.</Description>
                <DataType>
                  <Basic>Integer</Basic>
                </DataType>
              </Parameter>
              <Response>
                <Identifier>ReceivedString</Identifier>
                <DisplayName>Received String</DisplayName>
                <Description>Received String.</Description>
                <DataType>
                  <Basic>String</Basic>
                </DataType>
              </Response>
              <Response>
                <Identifier>ReceivedInteger</Identifier>
                <DisplayName>Received Integer</DisplayName>
                <Description>Received Integer.</Description>
                <DataType>
                  <Basic>Integer</Basic>
                </DataType>
              </Response>
              <IntermediateResponse>
                <Identifier>IntermediateInteger</Identifier>
                <DisplayName>Intermediate Integer</DisplayName>
                <Description>Intermediate Integer.</Description>
                <DataType>
                  <Basic>Integer</Basic>
                </DataType>
              </IntermediateResponse>
              <DefinedExecutionErrors>
                <Identifier>Error1</Identifier>
                <Identifier>Error2</Identifier>
              </DefinedExecutionErrors>
            </Command>
            """
        )


class TestDeserialize:
    async def test_should_deserialize_unobservable_command(self):
        # Create xml
        xml = """
        <Command>
          <Identifier>UnobservableCommand</Identifier>
          <DisplayName>Unobservable Command</DisplayName>
          <Description>Unobservable Command.</Description>
          <Observable>No</Observable>
        </Command>
        """

        # Deserialize
        unobservable_command = Deserializer.deserialize(
            xml,
            Command.deserialize,
            {
                "unobservable_command_factory": UnobservableCommand,
            },
        )

        # Assert that the method returns the correct value
        assert unobservable_command == UnobservableCommand(
            identifier="UnobservableCommand",
            display_name="Unobservable Command",
            description="Unobservable Command.",
        )

    async def test_should_deserialize_parameters(self):
        # Create xml
        xml = """
        <Command>
          <Identifier>ObservableCommand</Identifier>
          <DisplayName>Observable Command</DisplayName>
          <Description>Observable Command.</Description>
          <Observable>Yes</Observable>
          <Parameter>
            <Identifier>StringValue</Identifier>
            <DisplayName>String Value</DisplayName>
            <Description>String Value.</Description>
            <DataType>
              <Basic>String</Basic>
            </DataType>
          </Parameter>
          <Parameter>
            <Identifier>IntegerValue</Identifier>
            <DisplayName>Integer Value</DisplayName>
            <Description>Integer Value.</Description>
            <DataType>
              <Basic>Integer</Basic>
            </DataType>
          </Parameter>
        </Command>
        """

        # Deserialize
        observable_command = Deserializer.deserialize(
            xml,
            Command.deserialize,
            {
                "observable_command_factory": ObservableCommand,
            },
        )

        # Assert that the method returns the correct value
        assert observable_command == ObservableCommand(
            identifier="ObservableCommand",
            display_name="Observable Command",
            description="Observable Command.",
            parameters={
                "StringValue": Element(
                    identifier="StringValue", display_name="String Value", description="String Value.", data_type=String
                ),
                "IntegerValue": Element(
                    identifier="IntegerValue",
                    display_name="Integer Value",
                    description="Integer Value.",
                    data_type=Integer,
                ),
            },
        )

    async def test_should_deserialize_responses(self):
        # Create xml
        xml = """
            <Command>
              <Identifier>ObservableCommand</Identifier>
              <DisplayName>Observable Command</DisplayName>
              <Description>Observable Command.</Description>
              <Observable>Yes</Observable>
              <Response>
                <Identifier>ReceivedString</Identifier>
                <DisplayName>Received String</DisplayName>
                <Description>Received String.</Description>
                <DataType>
                  <Basic>String</Basic>
                </DataType>
              </Response>
              <Response>
                <Identifier>ReceivedInteger</Identifier>
                <DisplayName>Received Integer</DisplayName>
                <Description>Received Integer.</Description>
                <DataType>
                  <Basic>Integer</Basic>
                </DataType>
              </Response>
            </Command>
        """

        # Deserialize
        observable_command = Deserializer.deserialize(
            xml,
            Command.deserialize,
            {
                "observable_command_factory": ObservableCommand,
            },
        )

        # Assert that the method returns the correct value
        assert observable_command == ObservableCommand(
            identifier="ObservableCommand",
            display_name="Observable Command",
            description="Observable Command.",
            responses={
                "ReceivedString": Element(
                    identifier="ReceivedString",
                    display_name="Received String",
                    description="Received String.",
                    data_type=String,
                ),
                "ReceivedInteger": Element(
                    identifier="ReceivedInteger",
                    display_name="Received Integer",
                    description="Received Integer.",
                    data_type=Integer,
                ),
            },
        )

    async def test_should_deserialize_intermediate_responses(self):
        # Create xml
        xml = """
            <Command>
              <Identifier>ObservableCommand</Identifier>
              <DisplayName>Observable Command</DisplayName>
              <Description>Observable Command.</Description>
              <Observable>Yes</Observable>
              <IntermediateResponse>
                <Identifier>IntermediateInteger</Identifier>
                <DisplayName>Intermediate Integer</DisplayName>
                <Description>Intermediate Integer.</Description>
                <DataType>
                  <Basic>Integer</Basic>
                </DataType>
              </IntermediateResponse>
            </Command>
        """

        # Deserialize
        observable_command = Deserializer.deserialize(
            xml,
            Command.deserialize,
            {
                "observable_command_factory": ObservableCommand,
            },
        )

        # Assert that the method returns the correct value
        assert observable_command == ObservableCommand(
            identifier="ObservableCommand",
            display_name="Observable Command",
            description="Observable Command.",
            intermediate_responses={
                "IntermediateInteger": Element(
                    identifier="IntermediateInteger",
                    display_name="Intermediate Integer",
                    description="Intermediate Integer.",
                    data_type=Integer,
                ),
            },
        )

    async def test_should_deserialize_errors(self):
        # Create xml
        xml = """
        <Command>
          <Identifier>UnobservableCommand</Identifier>
          <DisplayName>Unobservable Command</DisplayName>
          <Description>Unobservable Command.</Description>
          <Observable>No</Observable>
          <DefinedExecutionErrors>
            <Identifier>Error1</Identifier>
            <Identifier>Error2</Identifier>
          </DefinedExecutionErrors>
        </Command>
        """

        # Deserialize
        unobservable_command = Deserializer.deserialize(
            xml,
            Command.deserialize,
            {
                "unobservable_command_factory": UnobservableCommand,
            },
        )

        # Assert that the method returns the correct value
        assert unobservable_command.errors.keys() == {"Error1", "Error2"}
        assert unobservable_command.errors["Error1"].identifier == "Error1"
        assert unobservable_command.errors["Error1"].display_name == "Error1"
        assert unobservable_command.errors["Error1"].description == ""
        assert unobservable_command.errors["Error2"].identifier == "Error2"
        assert unobservable_command.errors["Error2"].display_name == "Error2"
        assert unobservable_command.errors["Error2"].description == ""

    async def test_should_deserialize_observable_command(self):
        # Create xml
        xml = """
        <Command>
          <Identifier>ObservableCommand</Identifier>
          <DisplayName>Observable Command</DisplayName>
          <Description>Observable Command.</Description>
          <Observable>Yes</Observable>
          <Parameter>
            <Identifier>StringValue</Identifier>
            <DisplayName>String Value</DisplayName>
            <Description>String Value.</Description>
            <DataType>
              <Basic>String</Basic>
            </DataType>
          </Parameter>
          <Parameter>
            <Identifier>IntegerValue</Identifier>
            <DisplayName>Integer Value</DisplayName>
            <Description>Integer Value.</Description>
            <DataType>
              <Basic>Integer</Basic>
            </DataType>
          </Parameter>
          <Response>
            <Identifier>ReceivedString</Identifier>
            <DisplayName>Received String</DisplayName>
            <Description>Received String.</Description>
            <DataType>
              <Basic>String</Basic>
            </DataType>
          </Response>
          <Response>
            <Identifier>ReceivedInteger</Identifier>
            <DisplayName>Received Integer</DisplayName>
            <Description>Received Integer.</Description>
            <DataType>
              <Basic>Integer</Basic>
            </DataType>
          </Response>
          <IntermediateResponse>
            <Identifier>IntermediateInteger</Identifier>
            <DisplayName>Intermediate Integer</DisplayName>
            <Description>Intermediate Integer.</Description>
            <DataType>
              <Basic>Integer</Basic>
            </DataType>
          </IntermediateResponse>
          <DefinedExecutionErrors>
            <Identifier>Error1</Identifier>
            <Identifier>Error2</Identifier>
          </DefinedExecutionErrors>
        </Command>
        """

        # Deserialize
        observable_command = Deserializer.deserialize(
            xml,
            Command.deserialize,
            {
                "observable_command_factory": ObservableCommand,
            },
        )

        # Assert that the method returns the correct value
        assert observable_command.identifier == "ObservableCommand"
        assert observable_command.display_name == "Observable Command"
        assert observable_command.description == "Observable Command."
        assert observable_command.parameters == {
            "StringValue": Element(
                identifier="StringValue", display_name="String Value", description="String Value.", data_type=String
            ),
            "IntegerValue": Element(
                identifier="IntegerValue",
                display_name="Integer Value",
                description="Integer Value.",
                data_type=Integer,
            ),
        }
        assert observable_command.responses == {
            "ReceivedString": Element(
                identifier="ReceivedString",
                display_name="Received String",
                description="Received String.",
                data_type=String,
            ),
            "ReceivedInteger": Element(
                identifier="ReceivedInteger",
                display_name="Received Integer",
                description="Received Integer.",
                data_type=Integer,
            ),
        }
        assert observable_command.intermediate_responses == {
            "IntermediateInteger": Element(
                identifier="IntermediateInteger",
                display_name="Intermediate Integer",
                description="Intermediate Integer.",
                data_type=Integer,
            ),
        }
        assert observable_command.errors.keys() == {"Error1", "Error2"}
        assert observable_command.errors["Error1"].identifier == "Error1"
        assert observable_command.errors["Error1"].display_name == "Error1"
        assert observable_command.errors["Error1"].description == ""
        assert observable_command.errors["Error2"].identifier == "Error2"
        assert observable_command.errors["Error2"].display_name == "Error2"
        assert observable_command.errors["Error2"].description == ""

    async def test_should_raise_on_intermediate_responses_on_unobservable_command(self):
        # Create xml
        xml = """
        <Command>
          <Identifier>UnobservableCommand</Identifier>
          <DisplayName>Unobservable Command</DisplayName>
          <Description>Unobservable Command.</Description>
          <Observable>No</Observable>
          <IntermediateResponse>
            <Identifier>IntermediateInteger</Identifier>
            <DisplayName>Intermediate Integer</DisplayName>
            <Description>Intermediate Integer.</Description>
            <DataType>
              <Basic>Integer</Basic>
            </DataType>
          </IntermediateResponse>
        </Command>
        """

        # Deserialize
        with pytest.raises(
            ParseError, match=re.escape("IntermediateResponse can only be used with observable commands.")
        ):
            Deserializer.deserialize(
                xml,
                Command.deserialize,
                {
                    "unobservable_command_factory": UnobservableCommand,
                },
            )


class TestEquality:
    def test_should_be_true_on_equal_commands(self):
        # Create data type
        command_0 = Command(
            identifier="Command",
            display_name="Command",
            description="Command.",
        )
        command_1 = Command(
            identifier="Command",
            display_name="Command",
            description="Command.",
        )

        # Compare equality
        assert command_0 == command_1

    def test_should_be_false_on_unequal_commands(self):
        # Create data type
        command_0 = Command(
            identifier="Command1",
            display_name="Command1",
            description="Command1.",
        )
        command_1 = Command(
            identifier="Command2",
            display_name="Command2",
            description="Command2.",
        )

        # Compare equality
        assert command_0 != command_1

    def test_should_be_false_on_non_structure(self):
        # Create data type
        command = Command(
            identifier="Command1",
            display_name="Command1",
            description="Command1.",
        )

        # Compare equality
        assert command != unittest.mock.Mock()
