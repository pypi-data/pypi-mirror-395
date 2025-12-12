import re
import textwrap
import unittest.mock

import pytest

from sila.framework.common.feature import Feature
from sila.framework.data_types.string import String
from sila.framework.errors.defined_execution_error import DefinedExecutionError
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.serializer import Serializer
from sila.framework.metadata.metadata import Metadata


class TestCreate:
    async def test_should_raise_on_invalid_identifier(self):
        # Create metadata
        with pytest.raises(
            ValueError, match=re.compile("Identifier must start with an upper-case letter, received ''.")
        ):
            Metadata.create(identifier="", display_name="Metadata")

    async def test_should_raise_on_invalid_display_name(self):
        # Create metadata
        with pytest.raises(ValueError, match=re.compile("Display name must not be empty, received ''.")):
            Metadata.create(identifier="Metadata", display_name="")

    async def test_should_add_to_feature(self):
        # Create metadata
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")
        metadata = Metadata.create(identifier="TestMetadata", display_name="Test Metadata", feature=feature)

        # Get fully qualified identifier
        assert metadata.feature == feature
        assert feature.metadata["TestMetadata"] == metadata


class TestFullyQualifiedIdentifier:
    async def test_should_raise_on_missing_feature(self):
        # Create metadata
        metadata = Metadata.create(identifier="TestMetadata", display_name="Test Metadata")

        # Get fully qualified identifier
        with pytest.raises(
            RuntimeError,
            match=re.compile(
                "Unable to get fully qualified identifier for Metadata 'TestMetadata' without feature association."
            ),
        ):
            assert metadata.fully_qualified_identifier() is None

    async def test_should_get_fully_qualified_identifier(self):
        # Create metadata
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")
        metadata = Metadata.create(identifier="TestMetadata", display_name="Test Metadata", feature=feature)

        # Get fully qualified identifier
        assert metadata.fully_qualified_identifier() == "org.silastandard/none/SiLAService/v1/Metadata/TestMetadata"


class TestRpcHeader:
    async def test_should_get_rpc_header(self):
        # Create metadata
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")
        metadata = Metadata.create(identifier="TestMetadata", display_name="Test Metadata", feature=feature)

        # Get fully qualified identifier
        assert metadata.rpc_header() == "sila-org.silastandard-none-silaservice-v1-metadata-testmetadata-bin"


class TestAddToFeature:
    async def test_should_add_to_feature(self):
        # Create metadata
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")
        metadata = Metadata.create(identifier="TestMetadata", display_name="Test Metadata")

        # Add to feature
        metadata.add_to_feature(feature)

        # Assert that the method returns the correct value
        assert metadata.feature == feature
        assert feature.metadata["TestMetadata"] == metadata


class TestSerialize:
    async def test_should_serialize_xml(self):
        # Create metadata
        metadata = Metadata.create(
            identifier="TestMetadata",
            display_name="Test Metadata",
            description="Test Metadata.",
            data_type=String,
        )

        # Serialize
        xml = Serializer.serialize(metadata.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <Metadata>
              <Identifier>TestMetadata</Identifier>
              <DisplayName>Test Metadata</DisplayName>
              <Description>Test Metadata.</Description>
              <DataType>
                <Basic>String</Basic>
              </DataType>
            </Metadata>
            """
        )

    async def test_should_serialize_errors(self):
        # Create metadata
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
        metadata = Metadata.create(
            identifier="TestMetadata",
            display_name="Test Metadata",
            description="Test Metadata.",
            data_type=String,
            errors={error1.identifier: error1, error2.identifier: error2},
        )

        # Serialize
        xml = Serializer.serialize(metadata.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <Metadata>
              <Identifier>TestMetadata</Identifier>
              <DisplayName>Test Metadata</DisplayName>
              <Description>Test Metadata.</Description>
              <DataType>
                <Basic>String</Basic>
              </DataType>
              <DefinedExecutionErrors>
                <Identifier>Error1</Identifier>
                <Identifier>Error2</Identifier>
              </DefinedExecutionErrors>
            </Metadata>
            """
        )


class TestDeserialize:
    async def test_should_deserialize_xml(self):
        # Create xml
        xml = """
        <Metadata>
          <Identifier>Testetadata</Identifier>
          <DisplayName>Test Metadata</DisplayName>
          <Description>Test Metadata.</Description>
          <DataType>
            <Basic>String</Basic>
          </DataType>
        </Metadata>
        """

        # Deserialize
        metadata = Deserializer.deserialize(
            xml,
            Metadata.deserialize,
            {
                "metadata_factory": Metadata,
            },
        )

        # Assert that the method returns the correct value
        assert metadata.identifier == "Testetadata"
        assert metadata.display_name == "Test Metadata"
        assert metadata.description == "Test Metadata."
        assert metadata.data_type == String

    async def test_should_deserialize_errors(self):
        # Create xml
        xml = """
        <Metadata>
          <Identifier>Testetadata</Identifier>
          <DisplayName>Test Metadata</DisplayName>
          <Description>Test Metadata.</Description>
          <DataType>
            <Basic>String</Basic>
          </DataType>
          <DefinedExecutionErrors>
            <Identifier>Error1</Identifier>
            <Identifier>Error2</Identifier>
          </DefinedExecutionErrors>
        </Metadata>
        """

        # Deserialize
        metadata = Deserializer.deserialize(
            xml,
            Metadata.deserialize,
            {
                "metadata_factory": Metadata,
            },
        )

        assert metadata.errors.keys() == {"Error1", "Error2"}
        assert metadata.errors["Error1"].identifier == "Error1"
        assert metadata.errors["Error1"].display_name == "Error1"
        assert metadata.errors["Error1"].description == ""
        assert metadata.errors["Error2"].identifier == "Error2"
        assert metadata.errors["Error2"].display_name == "Error2"
        assert metadata.errors["Error2"].description == ""


class TestEquality:
    def test_should_be_true_on_equal_metadata(self):
        # Create data type
        metadata_0 = Metadata.create(
            identifier="Metadata",
            display_name="Metadata",
            description="Metadata.",
            data_type=String,
        )(String("Hello, World!"))
        metadata_1 = Metadata.create(
            identifier="Metadata",
            display_name="Metadata",
            description="Metadata.",
            data_type=String,
        )(String("Hello, World!"))

        # Compare equality
        assert metadata_0 == metadata_1

    def test_should_be_false_on_unequal_metadata(self):
        # Create data type
        metadata_0 = Metadata.create(
            identifier="Metadata",
            display_name="Metadata",
            description="Metadata.",
            data_type=String,
        )(String("1: Hello, World!"))
        metadata_1 = Metadata.create(
            identifier="Metadata",
            display_name="Metadata",
            description="Metadata.",
            data_type=String,
        )(String("2: Hello, World!"))

        # Compare equality
        assert metadata_0 != metadata_1

    def test_should_be_false_on_non_metadata(self):
        # Create data type
        metadata = Metadata.create(
            identifier="Metadata1",
            display_name="Metadata1",
            description="Metadata1.",
            data_type=String,
        )(String("2: Hello, World!"))

        # Compare equality
        assert metadata != unittest.mock.Mock()
