import re
import textwrap

import pytest

from sila.framework.command.command import Command
from sila.framework.command.observable_command import ObservableCommand
from sila.framework.command.unobservable_command import UnobservableCommand
from sila.framework.common.feature import Feature
from sila.framework.data_types.custom import Custom
from sila.framework.data_types.string import String
from sila.framework.errors.defined_execution_error import DefinedExecutionError
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.serializer import Serializer
from sila.framework.metadata.metadata import Metadata
from sila.framework.property.observable_property import ObservableProperty
from sila.framework.property.property import Property
from sila.framework.property.unobservable_property import UnobservableProperty


class TestInitialize:
    async def test_should_raise_on_invalid_identifier(self):
        # Create feature
        with pytest.raises(
            ValueError, match=re.escape("Identifier must start with an upper-case letter, received ''.")
        ):
            Feature(identifier="")

    async def test_should_raise_on_invalid_display_name(self):
        # Create feature
        with pytest.raises(ValueError, match=re.escape("Display name must not be empty, received ''.")):
            Feature(identifier="Feature", display_name="")

    async def test_should_add_command_to_feature(self):
        # Create feature
        command = Command(identifier="TestCommand", display_name="Test Command")
        feature = Feature(identifier="SiLAService", display_name="SiLA Service", commands={command.identifier: command})

        # Get fully qualified identifier
        assert command.feature == feature
        assert feature.commands["TestCommand"] == command

    async def test_should_add_property_to_feature(self):
        # Create feature
        property_ = Property(identifier="TestProperty", display_name="Test Property")
        feature = Feature(
            identifier="SiLAService", display_name="SiLA Service", properties={property_.identifier: property_}
        )

        # Get fully qualified identifier
        assert property_.feature == feature
        assert feature.properties["TestProperty"] == property_

    async def test_should_add_metadata_to_feature(self):
        # Create feature
        metadata = Metadata.create(identifier="TestMetadata", display_name="TestMetadata")
        feature = Feature(
            identifier="SiLAService", display_name="SiLA Service", metadata={metadata.identifier: metadata}
        )

        # Get fully qualified identifier
        assert metadata.feature == feature
        assert feature.metadata["TestMetadata"] == metadata


class TestFullyQualifiedIdentifier:
    async def test_should_get_fully_qualified_identifier(self):
        # Create feature
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")

        # Get fully qualified identifier
        assert feature.fully_qualified_identifier == "org.silastandard/none/SiLAService/v1"


class TestRpcPackage:
    async def test_should_get_rpc_package(self):
        # Create feature
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")

        # Get fully qualified identifier
        assert feature.rpc_package == "sila2.org.silastandard.none.silaservice.v1"


class TestSerialize:
    async def test_should_serialize_feature(self):
        # Create feature
        feature = Feature(
            identifier="SomeFeature",
            display_name="Some Feature",
            description="Some Feature.",
        )

        # Serialize
        xml = Serializer.serialize(feature.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <?xml version="1.0" encoding="utf-8" ?>
            <Feature SiLA2Version="1.1" FeatureVersion="1.0" Originator="org.silastandard"
                     xmlns="http://www.sila-standard.org"
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                     xsi:schemaLocation="http://www.sila-standard.org https://gitlab.com/SiLA2/sila_base/raw/master/schema/FeatureDefinition.xsd">
              <Identifier>SomeFeature</Identifier>
              <DisplayName>Some Feature</DisplayName>
              <Description>Some Feature.</Description>
            </Feature>
            """
        )

    async def test_should_serialize_locale(self):
        # Create feature
        feature = Feature(
            identifier="SomeFeature",
            display_name="Some Feature",
            description="Some Feature.",
            locale="de-de",
        )

        # Serialize
        xml = Serializer.serialize(feature.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <?xml version="1.0" encoding="utf-8" ?>
            <Feature Locale="de-de" SiLA2Version="1.1" FeatureVersion="1.0" Originator="org.silastandard"
                     xmlns="http://www.sila-standard.org"
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                     xsi:schemaLocation="http://www.sila-standard.org https://gitlab.com/SiLA2/sila_base/raw/master/schema/FeatureDefinition.xsd">
              <Identifier>SomeFeature</Identifier>
              <DisplayName>Some Feature</DisplayName>
              <Description>Some Feature.</Description>
            </Feature>
            """
        )

    async def test_should_serialize_maturity_level(self):
        # Create feature
        feature = Feature(
            identifier="SomeFeature",
            display_name="Some Feature",
            description="Some Feature.",
            maturity_level="Verified",
        )

        # Serialize
        xml = Serializer.serialize(feature.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <?xml version="1.0" encoding="utf-8" ?>
            <Feature SiLA2Version="1.1" FeatureVersion="1.0" MaturityLevel="Verified" Originator="org.silastandard"
                     xmlns="http://www.sila-standard.org"
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                     xsi:schemaLocation="http://www.sila-standard.org https://gitlab.com/SiLA2/sila_base/raw/master/schema/FeatureDefinition.xsd">
              <Identifier>SomeFeature</Identifier>
              <DisplayName>Some Feature</DisplayName>
              <Description>Some Feature.</Description>
            </Feature>
            """
        )

    async def test_should_serialize_category(self):
        # Create feature
        feature = Feature(
            identifier="SomeFeature",
            display_name="Some Feature",
            description="Some Feature.",
            category="some.category",
        )

        # Serialize
        xml = Serializer.serialize(feature.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <?xml version="1.0" encoding="utf-8" ?>
            <Feature SiLA2Version="1.1" FeatureVersion="1.0" Originator="org.silastandard" Category="some.category"
                     xmlns="http://www.sila-standard.org"
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                     xsi:schemaLocation="http://www.sila-standard.org https://gitlab.com/SiLA2/sila_base/raw/master/schema/FeatureDefinition.xsd">
              <Identifier>SomeFeature</Identifier>
              <DisplayName>Some Feature</DisplayName>
              <Description>Some Feature.</Description>
            </Feature>
            """
        )

    async def test_should_serialize_originator(self):
        # Create feature
        feature = Feature(
            identifier="SomeFeature",
            display_name="Some Feature",
            description="Some Feature.",
            originator="io.unitelabs",
        )

        # Serialize
        xml = Serializer.serialize(feature.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <?xml version="1.0" encoding="utf-8" ?>
            <Feature SiLA2Version="1.1" FeatureVersion="1.0" Originator="io.unitelabs"
                     xmlns="http://www.sila-standard.org"
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                     xsi:schemaLocation="http://www.sila-standard.org https://gitlab.com/SiLA2/sila_base/raw/master/schema/FeatureDefinition.xsd">
              <Identifier>SomeFeature</Identifier>
              <DisplayName>Some Feature</DisplayName>
              <Description>Some Feature.</Description>
            </Feature>
            """
        )

    async def test_should_serialize_command(self):
        # Create feature
        feature = Feature(
            identifier="SomeFeature",
            display_name="Some Feature",
            description="Some Feature.",
        )
        Command(
            identifier="UnobservableCommand",
            display_name="Unobservable Command",
            description="Unobservable Command.",
            feature=feature,
        )

        # Serialize
        xml = Serializer.serialize(feature.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <?xml version="1.0" encoding="utf-8" ?>
            <Feature SiLA2Version="1.1" FeatureVersion="1.0" Originator="org.silastandard"
                     xmlns="http://www.sila-standard.org"
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                     xsi:schemaLocation="http://www.sila-standard.org https://gitlab.com/SiLA2/sila_base/raw/master/schema/FeatureDefinition.xsd">
              <Identifier>SomeFeature</Identifier>
              <DisplayName>Some Feature</DisplayName>
              <Description>Some Feature.</Description>
              <Command>
                <Identifier>UnobservableCommand</Identifier>
                <DisplayName>Unobservable Command</DisplayName>
                <Description>Unobservable Command.</Description>
                <Observable>No</Observable>
              </Command>
            </Feature>
            """
        )

    async def test_should_serialize_property(self):
        # Create feature
        feature = Feature(
            identifier="SomeFeature",
            display_name="Some Feature",
            description="Some Feature.",
        )
        Property(
            identifier="UnobservableProperty",
            display_name="Unobservable Property",
            description="Unobservable Property.",
            data_type=String,
            feature=feature,
        )

        # Serialize
        xml = Serializer.serialize(feature.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <?xml version="1.0" encoding="utf-8" ?>
            <Feature SiLA2Version="1.1" FeatureVersion="1.0" Originator="org.silastandard"
                     xmlns="http://www.sila-standard.org"
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                     xsi:schemaLocation="http://www.sila-standard.org https://gitlab.com/SiLA2/sila_base/raw/master/schema/FeatureDefinition.xsd">
              <Identifier>SomeFeature</Identifier>
              <DisplayName>Some Feature</DisplayName>
              <Description>Some Feature.</Description>
              <Property>
                <Identifier>UnobservableProperty</Identifier>
                <DisplayName>Unobservable Property</DisplayName>
                <Description>Unobservable Property.</Description>
                <Observable>No</Observable>
                <DataType>
                  <Basic>String</Basic>
                </DataType>
              </Property>
            </Feature>
            """
        )

    async def test_should_serialize_metadata(self):
        # Create feature
        feature = Feature(
            identifier="SomeFeature",
            display_name="Some Feature",
            description="Some Feature.",
        )
        Metadata.create(
            identifier="SomeMetadata",
            display_name="Some Metadata",
            description="Some Metadata.",
            data_type=String,
            feature=feature,
        )

        # Serialize
        xml = Serializer.serialize(feature.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <?xml version="1.0" encoding="utf-8" ?>
            <Feature SiLA2Version="1.1" FeatureVersion="1.0" Originator="org.silastandard"
                     xmlns="http://www.sila-standard.org"
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                     xsi:schemaLocation="http://www.sila-standard.org https://gitlab.com/SiLA2/sila_base/raw/master/schema/FeatureDefinition.xsd">
              <Identifier>SomeFeature</Identifier>
              <DisplayName>Some Feature</DisplayName>
              <Description>Some Feature.</Description>
              <Metadata>
                <Identifier>SomeMetadata</Identifier>
                <DisplayName>Some Metadata</DisplayName>
                <Description>Some Metadata.</Description>
                <DataType>
                  <Basic>String</Basic>
                </DataType>
              </Metadata>
            </Feature>
            """
        )

    async def test_should_serialize_error(self):
        # Create feature
        feature = Feature(
            identifier="SomeFeature",
            display_name="Some Feature",
            description="Some Feature.",
        )
        shared_error = DefinedExecutionError.create(
            identifier="SharedError",
            display_name="Shared Error",
            description="Shared Error.",
        )
        Command(
            identifier="UnobservableCommand",
            display_name="Unobservable Command",
            description="Unobservable Command.",
            errors={
                shared_error.identifier: shared_error,
                "UnobservableCommandError": DefinedExecutionError.create(
                    identifier="UnobservableCommandError",
                    display_name="Unobservable Command Error",
                    description="Unobservable Command Error.",
                ),
            },
            feature=feature,
        )
        Property(
            identifier="UnobservableProperty",
            display_name="Unobservable Property",
            description="Unobservable Property.",
            data_type=String,
            errors={
                shared_error.identifier: shared_error,
                "UnobservablePropertyError": DefinedExecutionError.create(
                    identifier="UnobservablePropertyError",
                    display_name="Unobservable Property Error",
                    description="Unobservable Property Error.",
                ),
            },
            feature=feature,
        )
        Metadata.create(
            identifier="SomeMetadata",
            display_name="Some Metadata",
            description="Some Metadata.",
            data_type=String,
            errors={
                shared_error.identifier: shared_error,
                "MetadataError": DefinedExecutionError.create(
                    identifier="MetadataError",
                    display_name="Metadata Error",
                    description="Metadata Error.",
                ),
            },
            feature=feature,
        )

        # Serialize
        xml = Serializer.serialize(feature.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <?xml version="1.0" encoding="utf-8" ?>
            <Feature SiLA2Version="1.1" FeatureVersion="1.0" Originator="org.silastandard"
                     xmlns="http://www.sila-standard.org"
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                     xsi:schemaLocation="http://www.sila-standard.org https://gitlab.com/SiLA2/sila_base/raw/master/schema/FeatureDefinition.xsd">
              <Identifier>SomeFeature</Identifier>
              <DisplayName>Some Feature</DisplayName>
              <Description>Some Feature.</Description>
              <Command>
                <Identifier>UnobservableCommand</Identifier>
                <DisplayName>Unobservable Command</DisplayName>
                <Description>Unobservable Command.</Description>
                <Observable>No</Observable>
                <DefinedExecutionErrors>
                  <Identifier>SharedError</Identifier>
                  <Identifier>UnobservableCommandError</Identifier>
                </DefinedExecutionErrors>
              </Command>
              <Property>
                <Identifier>UnobservableProperty</Identifier>
                <DisplayName>Unobservable Property</DisplayName>
                <Description>Unobservable Property.</Description>
                <Observable>No</Observable>
                <DataType>
                  <Basic>String</Basic>
                </DataType>
                <DefinedExecutionErrors>
                  <Identifier>SharedError</Identifier>
                  <Identifier>UnobservablePropertyError</Identifier>
                </DefinedExecutionErrors>
              </Property>
              <Metadata>
                <Identifier>SomeMetadata</Identifier>
                <DisplayName>Some Metadata</DisplayName>
                <Description>Some Metadata.</Description>
                <DataType>
                  <Basic>String</Basic>
                </DataType>
                <DefinedExecutionErrors>
                  <Identifier>SharedError</Identifier>
                  <Identifier>MetadataError</Identifier>
                </DefinedExecutionErrors>
              </Metadata>
              <DefinedExecutionError>
                <Identifier>SharedError</Identifier>
                <DisplayName>Shared Error</DisplayName>
                <Description>Shared Error.</Description>
              </DefinedExecutionError>
              <DefinedExecutionError>
                <Identifier>UnobservableCommandError</Identifier>
                <DisplayName>Unobservable Command Error</DisplayName>
                <Description>Unobservable Command Error.</Description>
              </DefinedExecutionError>
              <DefinedExecutionError>
                <Identifier>UnobservablePropertyError</Identifier>
                <DisplayName>Unobservable Property Error</DisplayName>
                <Description>Unobservable Property Error.</Description>
              </DefinedExecutionError>
              <DefinedExecutionError>
                <Identifier>MetadataError</Identifier>
                <DisplayName>Metadata Error</DisplayName>
                <Description>Metadata Error.</Description>
              </DefinedExecutionError>
            </Feature>
            """
        )

    async def test_should_serialize_data_type_definition(self):
        # Create feature
        feature = Feature(
            identifier="SomeFeature",
            display_name="Some Feature",
            description="Some Feature.",
        )
        Custom.create(
            identifier="DataTypeDefinition",
            display_name="Data Type Definition",
            description="Data Type Definition.",
            data_type=String,
            feature=feature,
        )

        # Serialize
        xml = Serializer.serialize(feature.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <?xml version="1.0" encoding="utf-8" ?>
            <Feature SiLA2Version="1.1" FeatureVersion="1.0" Originator="org.silastandard"
                     xmlns="http://www.sila-standard.org"
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                     xsi:schemaLocation="http://www.sila-standard.org https://gitlab.com/SiLA2/sila_base/raw/master/schema/FeatureDefinition.xsd">
              <Identifier>SomeFeature</Identifier>
              <DisplayName>Some Feature</DisplayName>
              <Description>Some Feature.</Description>
              <DataTypeDefinition>
                <Identifier>DataTypeDefinition</Identifier>
                <DisplayName>Data Type Definition</DisplayName>
                <Description>Data Type Definition.</Description>
                <DataType>
                  <Basic>String</Basic>
                </DataType>
              </DataTypeDefinition>
            </Feature>
            """
        )


class TestDeserialize:
    async def test_should_deserialize_unobservable_command(self):
        # Create xml
        xml = """
        <?xml version="1.0" encoding="utf-8" ?>
        <Feature SiLA2Version="1.1" FeatureVersion="1.0" Originator="org.silastandard"
                 xmlns="http://www.sila-standard.org"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://www.sila-standard.org https://gitlab.com/SiLA2/sila_base/raw/master/schema/FeatureDefinition.xsd">
          <Identifier>SomeFeature</Identifier>
          <DisplayName>Some Feature</DisplayName>
          <Description>Some Feature.</Description>
        </Feature>
        """

        # Deserialize
        feature = Deserializer.deserialize(xml, Feature.deserialize)

        # Assert that the method returns the correct value
        assert feature == Feature(
            identifier="SomeFeature",
            display_name="Some Feature",
            description="Some Feature.",
        )

    async def test_should_deserialize_locale(self):
        # Create xml
        xml = """
        <?xml version="1.0" encoding="utf-8" ?>
        <Feature Locale="de-de" SiLA2Version="1.1" FeatureVersion="1.0" Originator="org.silastandard"
                 xmlns="http://www.sila-standard.org"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://www.sila-standard.org https://gitlab.com/SiLA2/sila_base/raw/master/schema/FeatureDefinition.xsd">
          <Identifier>SomeFeature</Identifier>
          <DisplayName>Some Feature</DisplayName>
          <Description>Some Feature.</Description>
        </Feature>
        """

        # Deserialize
        feature = Deserializer.deserialize(xml, Feature.deserialize)

        # Assert that the method returns the correct value
        assert feature == Feature(
            identifier="SomeFeature",
            display_name="Some Feature",
            description="Some Feature.",
            locale="de-de",
        )

    async def test_should_deserialize_maturity_level(self):
        # Create xml
        xml = """
        <?xml version="1.0" encoding="utf-8" ?>
        <Feature SiLA2Version="1.1" FeatureVersion="1.0" MaturityLevel="Verified" Originator="org.silastandard"
                 xmlns="http://www.sila-standard.org"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://www.sila-standard.org https://gitlab.com/SiLA2/sila_base/raw/master/schema/FeatureDefinition.xsd">
          <Identifier>SomeFeature</Identifier>
          <DisplayName>Some Feature</DisplayName>
          <Description>Some Feature.</Description>
        </Feature>
        """

        # Deserialize
        feature = Deserializer.deserialize(xml, Feature.deserialize)

        # Assert that the method returns the correct value
        assert feature == Feature(
            identifier="SomeFeature",
            display_name="Some Feature",
            description="Some Feature.",
            maturity_level="Verified",
        )

    async def test_should_deserialize_category(self):
        # Create xml
        xml = """
        <?xml version="1.0" encoding="utf-8" ?>
        <Feature SiLA2Version="1.1" FeatureVersion="1.0" Originator="org.silastandard" Category="some.category"
                 xmlns="http://www.sila-standard.org"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://www.sila-standard.org https://gitlab.com/SiLA2/sila_base/raw/master/schema/FeatureDefinition.xsd">
          <Identifier>SomeFeature</Identifier>
          <DisplayName>Some Feature</DisplayName>
          <Description>Some Feature.</Description>
        </Feature>
        """

        # Deserialize
        feature = Deserializer.deserialize(xml, Feature.deserialize)

        # Assert that the method returns the correct value
        assert feature == Feature(
            identifier="SomeFeature", display_name="Some Feature", description="Some Feature.", category="some.category"
        )

    async def test_should_deserialize_originator(self):
        # Create xml
        xml = """
        <?xml version="1.0" encoding="utf-8" ?>
        <Feature SiLA2Version="1.1" FeatureVersion="1.0" Originator="io.unitelabs"
                 xmlns="http://www.sila-standard.org"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://www.sila-standard.org https://gitlab.com/SiLA2/sila_base/raw/master/schema/FeatureDefinition.xsd">
          <Identifier>SomeFeature</Identifier>
          <DisplayName>Some Feature</DisplayName>
          <Description>Some Feature.</Description>
        </Feature>
        """

        # Deserialize
        feature = Deserializer.deserialize(xml, Feature.deserialize)

        # Assert that the method returns the correct value
        assert feature == Feature(
            identifier="SomeFeature",
            display_name="Some Feature",
            description="Some Feature.",
            originator="io.unitelabs",
        )

    async def test_should_deserialize_command(self):
        # Create xml
        xml = """
        <?xml version="1.0" encoding="utf-8" ?>
        <Feature SiLA2Version="1.1" FeatureVersion="1.0" Originator="org.silastandard"
                 xmlns="http://www.sila-standard.org"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://www.sila-standard.org https://gitlab.com/SiLA2/sila_base/raw/master/schema/FeatureDefinition.xsd">
          <Identifier>SomeFeature</Identifier>
          <DisplayName>Some Feature</DisplayName>
          <Description>Some Feature.</Description>
          <Command>
            <Identifier>UnobservableCommand</Identifier>
            <DisplayName>Unobservable Command</DisplayName>
            <Description>Unobservable Command.</Description>
            <Observable>No</Observable>
          </Command>
        </Feature>
        """

        # Deserialize
        feature: Feature = Deserializer.deserialize(xml, Feature.deserialize, {"unobservable_command_factory": Command})

        # Assert that the method returns the correct value
        assert feature == Feature(identifier="SomeFeature", display_name="Some Feature", description="Some Feature.")
        assert feature.commands == {
            "UnobservableCommand": UnobservableCommand(
                identifier="UnobservableCommand",
                display_name="Unobservable Command",
                description="Unobservable Command.",
                feature=feature,
            )
        }

    async def test_should_deserialize_property(self):
        # Create xml
        xml = """
        <?xml version="1.0" encoding="utf-8" ?>
        <Feature SiLA2Version="1.1" FeatureVersion="1.0" Originator="org.silastandard"
                 xmlns="http://www.sila-standard.org"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://www.sila-standard.org https://gitlab.com/SiLA2/sila_base/raw/master/schema/FeatureDefinition.xsd">
          <Identifier>SomeFeature</Identifier>
          <DisplayName>Some Feature</DisplayName>
          <Description>Some Feature.</Description>
          <Property>
            <Identifier>UnobservableProperty</Identifier>
            <DisplayName>Unobservable Property</DisplayName>
            <Description>Unobservable Property.</Description>
            <Observable>No</Observable>
            <DataType>
              <Basic>String</Basic>
            </DataType>
          </Property>
        </Feature>
        """

        # Deserialize
        feature: Feature = Deserializer.deserialize(
            xml, Feature.deserialize, {"unobservable_property_factory": UnobservableProperty}
        )

        # Assert that the method returns the correct value
        assert feature == Feature(identifier="SomeFeature", display_name="Some Feature", description="Some Feature.")
        assert feature.properties == {
            "UnobservableProperty": UnobservableProperty(
                identifier="UnobservableProperty",
                display_name="Unobservable Property",
                description="Unobservable Property.",
                data_type=String,
                feature=feature,
            )
        }

    async def test_should_deserialize_metadata(self):
        # Create xml
        xml = """
        <?xml version="1.0" encoding="utf-8" ?>
        <Feature SiLA2Version="1.1" FeatureVersion="1.0" Originator="org.silastandard"
                 xmlns="http://www.sila-standard.org"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://www.sila-standard.org https://gitlab.com/SiLA2/sila_base/raw/master/schema/FeatureDefinition.xsd">
          <Identifier>SomeFeature</Identifier>
          <DisplayName>Some Feature</DisplayName>
          <Description>Some Feature.</Description>
          <Metadata>
            <Identifier>SomeMetadata</Identifier>
            <DisplayName>Some Metadata</DisplayName>
            <Description>Some Metadata.</Description>
            <DataType>
              <Basic>String</Basic>
            </DataType>
          </Metadata>
        </Feature>
        """

        # Deserialize
        feature: Feature = Deserializer.deserialize(xml, Feature.deserialize, {"metadata_factory": Metadata})

        # Assert that the method returns the correct value
        assert feature == Feature(identifier="SomeFeature", display_name="Some Feature", description="Some Feature.")
        assert list(feature.metadata.keys()) == ["SomeMetadata"]
        assert feature.metadata["SomeMetadata"].identifier == "SomeMetadata"
        assert feature.metadata["SomeMetadata"].display_name == "Some Metadata"
        assert feature.metadata["SomeMetadata"].description == "Some Metadata."
        assert feature.metadata["SomeMetadata"].data_type == String

    async def test_should_deserialize_error(self):
        # Create xml
        xml = """
        <?xml version="1.0" encoding="utf-8" ?>
        <Feature SiLA2Version="1.1" FeatureVersion="1.0" Originator="org.silastandard"
                 xmlns="http://www.sila-standard.org"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://www.sila-standard.org https://gitlab.com/SiLA2/sila_base/raw/master/schema/FeatureDefinition.xsd">
          <Identifier>SomeFeature</Identifier>
          <DisplayName>Some Feature</DisplayName>
          <Description>Some Feature.</Description>
          <Command>
            <Identifier>UnobservableCommand</Identifier>
            <DisplayName>Unobservable Command</DisplayName>
            <Description>Unobservable Command.</Description>
            <Observable>No</Observable>
            <DefinedExecutionErrors>
              <Identifier>SharedError</Identifier>
              <Identifier>UnobservableCommandError</Identifier>
            </DefinedExecutionErrors>
          </Command>
          <Property>
            <Identifier>UnobservableProperty</Identifier>
            <DisplayName>Unobservable Property</DisplayName>
            <Description>Unobservable Property.</Description>
            <Observable>No</Observable>
            <DataType>
              <Basic>String</Basic>
            </DataType>
            <DefinedExecutionErrors>
              <Identifier>SharedError</Identifier>
              <Identifier>UnobservablePropertyError</Identifier>
            </DefinedExecutionErrors>
          </Property>
          <Metadata>
            <Identifier>SomeMetadata</Identifier>
            <DisplayName>Some Metadata</DisplayName>
            <Description>Some Metadata.</Description>
            <DataType>
              <Basic>String</Basic>
            </DataType>
            <DefinedExecutionErrors>
              <Identifier>SharedError</Identifier>
              <Identifier>MetadataError</Identifier>
            </DefinedExecutionErrors>
          </Metadata>
          <DefinedExecutionError>
            <Identifier>SharedError</Identifier>
            <DisplayName>Shared Error</DisplayName>
            <Description>Shared Error.</Description>
          </DefinedExecutionError>
          <DefinedExecutionError>
            <Identifier>UnobservableCommandError</Identifier>
            <DisplayName>Unobservable Command Error</DisplayName>
            <Description>Unobservable Command Error.</Description>
          </DefinedExecutionError>
          <DefinedExecutionError>
            <Identifier>UnobservablePropertyError</Identifier>
            <DisplayName>Unobservable Property Error</DisplayName>
            <Description>Unobservable Property Error.</Description>
          </DefinedExecutionError>
          <DefinedExecutionError>
            <Identifier>MetadataError</Identifier>
            <DisplayName>Metadata Error</DisplayName>
            <Description>Metadata Error.</Description>
          </DefinedExecutionError>
        </Feature>
        """

        # Deserialize
        feature: Feature = Deserializer.deserialize(
            xml,
            Feature.deserialize,
            {
                "unobservable_property_factory": UnobservableProperty,
                "unobservable_command_factory": UnobservableCommand,
                "metadata_factory": Metadata,
                "error_definitions": {},
            },
        )

        # Assert that the method returns the correct value
        assert feature == Feature(identifier="SomeFeature", display_name="Some Feature", description="Some Feature.")

        assert list(feature.commands.keys()) == ["UnobservableCommand"]
        assert feature.commands["UnobservableCommand"].identifier == "UnobservableCommand"
        assert feature.commands["UnobservableCommand"].display_name == "Unobservable Command"
        assert feature.commands["UnobservableCommand"].description == "Unobservable Command."
        assert list(feature.commands["UnobservableCommand"].errors.keys()) == [
            "SharedError",
            "UnobservableCommandError",
        ]
        assert feature.commands["UnobservableCommand"].errors["SharedError"].identifier == "SharedError"
        assert feature.commands["UnobservableCommand"].errors["SharedError"].display_name == "Shared Error"
        assert feature.commands["UnobservableCommand"].errors["SharedError"].description == "Shared Error."
        assert (
            feature.commands["UnobservableCommand"].errors["UnobservableCommandError"].identifier
            == "UnobservableCommandError"
        )
        assert (
            feature.commands["UnobservableCommand"].errors["UnobservableCommandError"].display_name
            == "Unobservable Command Error"
        )
        assert (
            feature.commands["UnobservableCommand"].errors["UnobservableCommandError"].description
            == "Unobservable Command Error."
        )

        assert list(feature.properties.keys()) == ["UnobservableProperty"]
        assert feature.properties["UnobservableProperty"].identifier == "UnobservableProperty"
        assert feature.properties["UnobservableProperty"].display_name == "Unobservable Property"
        assert feature.properties["UnobservableProperty"].description == "Unobservable Property."
        assert feature.properties["UnobservableProperty"].data_type == String
        assert list(feature.properties["UnobservableProperty"].errors.keys()) == [
            "SharedError",
            "UnobservablePropertyError",
        ]
        assert feature.properties["UnobservableProperty"].errors["SharedError"].identifier == "SharedError"
        assert feature.properties["UnobservableProperty"].errors["SharedError"].display_name == "Shared Error"
        assert feature.properties["UnobservableProperty"].errors["SharedError"].description == "Shared Error."
        assert (
            feature.properties["UnobservableProperty"].errors["UnobservablePropertyError"].identifier
            == "UnobservablePropertyError"
        )
        assert (
            feature.properties["UnobservableProperty"].errors["UnobservablePropertyError"].display_name
            == "Unobservable Property Error"
        )
        assert (
            feature.properties["UnobservableProperty"].errors["UnobservablePropertyError"].description
            == "Unobservable Property Error."
        )

        assert list(feature.metadata.keys()) == ["SomeMetadata"]
        assert feature.metadata["SomeMetadata"].identifier == "SomeMetadata"
        assert feature.metadata["SomeMetadata"].display_name == "Some Metadata"
        assert feature.metadata["SomeMetadata"].description == "Some Metadata."
        assert feature.metadata["SomeMetadata"].data_type == String
        assert list(feature.metadata["SomeMetadata"].errors.keys()) == ["SharedError", "MetadataError"]
        assert feature.metadata["SomeMetadata"].errors["SharedError"].identifier == "SharedError"
        assert feature.metadata["SomeMetadata"].errors["SharedError"].display_name == "Shared Error"
        assert feature.metadata["SomeMetadata"].errors["SharedError"].description == "Shared Error."
        assert feature.metadata["SomeMetadata"].errors["MetadataError"].identifier == "MetadataError"
        assert feature.metadata["SomeMetadata"].errors["MetadataError"].display_name == "Metadata Error"
        assert feature.metadata["SomeMetadata"].errors["MetadataError"].description == "Metadata Error."

    async def test_should_deserialize_data_type_definition(self):
        # Create xml
        xml = """
        <?xml version="1.0" encoding="utf-8" ?>
        <Feature SiLA2Version="1.1" FeatureVersion="1.0" Originator="org.silastandard"
                 xmlns="http://www.sila-standard.org"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://www.sila-standard.org https://gitlab.com/SiLA2/sila_base/raw/master/schema/FeatureDefinition.xsd">
          <Identifier>SomeFeature</Identifier>
          <DisplayName>Some Feature</DisplayName>
          <Description>Some Feature.</Description>
          <Command>
            <Identifier>Command</Identifier>
            <DisplayName>Command</DisplayName>
            <Description>Command</Description>
            <Observable>Yes</Observable>
            <Parameter>
              <Identifier>Parameter</Identifier>
              <DisplayName>Parameter</DisplayName>
              <Description>Parameter</Description>
              <DataType>
                <DataTypeIdentifier>DataTypeDefinition</DataTypeIdentifier>
              </DataType>
            </Parameter>
            <Response>
              <Identifier>Response</Identifier>
              <DisplayName>Response</DisplayName>
              <Description>Response</Description>
              <DataType>
                <DataTypeIdentifier>DataTypeDefinition</DataTypeIdentifier>
              </DataType>
            </Response>
            <IntermediateResponse>
              <Identifier>IntermediateResponse</Identifier>
              <DisplayName>IntermediateResponse</DisplayName>
              <Description>IntermediateResponse</Description>
              <DataType>
                <DataTypeIdentifier>DataTypeDefinition</DataTypeIdentifier>
              </DataType>
            </IntermediateResponse>
          </Command>
          <Property>
            <Identifier>Property</Identifier>
            <DisplayName>Property</DisplayName>
            <Description>Property</Description>
            <Observable>Yes</Observable>
            <DataType>
              <DataTypeIdentifier>DataTypeDefinition</DataTypeIdentifier>
            </DataType>
          </Property>
          <Metadata>
            <Identifier>SomeMetadata</Identifier>
            <DisplayName>Some Metadata</DisplayName>
            <Description>Some Metadata.</Description>
            <DataType>
              <DataTypeIdentifier>DataTypeDefinition</DataTypeIdentifier>
            </DataType>
          </Metadata>
          <DataTypeDefinition>
            <Identifier>DataTypeDefinition</Identifier>
            <DisplayName>Data Type Definition</DisplayName>
            <Description>Data Type Definition.</Description>
            <DataType>
              <Basic>String</Basic>
            </DataType>
          </DataTypeDefinition>
        </Feature>
        """

        # Deserialize
        feature: Feature = Deserializer.deserialize(
            xml,
            Feature.deserialize,
            {
                "unobservable_property_factory": UnobservableProperty,
                "observable_property_factory": ObservableProperty,
                "unobservable_command_factory": UnobservableCommand,
                "observable_command_factory": ObservableCommand,
                "metadata_factory": Metadata,
                "data_type_definitions": {},
            },
        )

        # Assert that the method returns the correct value
        assert list(feature.data_type_definitions.keys()) == ["DataTypeDefinition"]
        assert feature.data_type_definitions["DataTypeDefinition"].identifier == "DataTypeDefinition"
        assert feature.data_type_definitions["DataTypeDefinition"].display_name == "Data Type Definition"
        assert feature.data_type_definitions["DataTypeDefinition"].description == "Data Type Definition."

        custom = feature.data_type_definitions["DataTypeDefinition"]

        assert feature.commands["Command"].parameters["Parameter"].data_type == custom
        assert feature.commands["Command"].responses["Response"].data_type == custom
        assert feature.commands["Command"].intermediate_responses["IntermediateResponse"].data_type == custom
        assert feature.properties["Property"].data_type == custom
        assert feature.metadata["SomeMetadata"].data_type == custom

    async def test_should_deserialize_unordered_elements(self):
        # Create xml
        xml = """
        <?xml version="1.0" encoding="utf-8" ?>
        <Feature SiLA2Version="1.1" FeatureVersion="1.0" Originator="org.silastandard"
                 xmlns="http://www.sila-standard.org"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://www.sila-standard.org https://gitlab.com/SiLA2/sila_base/raw/master/schema/FeatureDefinition.xsd">
          <Identifier>SomeFeature</Identifier>
          <DisplayName>Some Feature</DisplayName>
          <Description>Some Feature.</Description>
          <DefinedExecutionError>
            <Identifier>SharedError</Identifier>
            <DisplayName>Shared Error</DisplayName>
            <Description>Shared Error.</Description>
          </DefinedExecutionError>
          <DefinedExecutionError>
            <Identifier>UnobservableCommandError</Identifier>
            <DisplayName>Unobservable Command Error</DisplayName>
            <Description>Unobservable Command Error.</Description>
          </DefinedExecutionError>
          <DefinedExecutionError>
            <Identifier>UnobservablePropertyError</Identifier>
            <DisplayName>Unobservable Property Error</DisplayName>
            <Description>Unobservable Property Error.</Description>
          </DefinedExecutionError>
          <DefinedExecutionError>
            <Identifier>MetadataError</Identifier>
            <DisplayName>Metadata Error</DisplayName>
            <Description>Metadata Error.</Description>
          </DefinedExecutionError>
          <Command>
            <Identifier>UnobservableCommand</Identifier>
            <DisplayName>Unobservable Command</DisplayName>
            <Description>Unobservable Command.</Description>
            <Observable>No</Observable>
            <DefinedExecutionErrors>
              <Identifier>SharedError</Identifier>
              <Identifier>UnobservableCommandError</Identifier>
            </DefinedExecutionErrors>
          </Command>
          <Property>
            <Identifier>UnobservableProperty</Identifier>
            <DisplayName>Unobservable Property</DisplayName>
            <Description>Unobservable Property.</Description>
            <Observable>No</Observable>
            <DataType>
              <Basic>String</Basic>
            </DataType>
            <DefinedExecutionErrors>
              <Identifier>SharedError</Identifier>
              <Identifier>UnobservablePropertyError</Identifier>
            </DefinedExecutionErrors>
          </Property>
          <Metadata>
            <Identifier>SomeMetadata</Identifier>
            <DisplayName>Some Metadata</DisplayName>
            <Description>Some Metadata.</Description>
            <DataType>
              <Basic>String</Basic>
            </DataType>
            <DefinedExecutionErrors>
              <Identifier>SharedError</Identifier>
              <Identifier>MetadataError</Identifier>
            </DefinedExecutionErrors>
          </Metadata>
        </Feature>
        """

        # Deserialize
        feature: Feature = Deserializer.deserialize(
            xml,
            Feature.deserialize,
            {
                "unobservable_property_factory": UnobservableProperty,
                "unobservable_command_factory": UnobservableCommand,
                "metadata_factory": Metadata,
                "error_definitions": {},
            },
        )

        # Assert that the method returns the correct value
        assert feature == Feature(identifier="SomeFeature", display_name="Some Feature", description="Some Feature.")

        assert list(feature.commands.keys()) == ["UnobservableCommand"]
        assert feature.commands["UnobservableCommand"].identifier == "UnobservableCommand"
        assert feature.commands["UnobservableCommand"].display_name == "Unobservable Command"
        assert feature.commands["UnobservableCommand"].description == "Unobservable Command."
        assert list(feature.commands["UnobservableCommand"].errors.keys()) == [
            "SharedError",
            "UnobservableCommandError",
        ]
        assert feature.commands["UnobservableCommand"].errors["SharedError"].identifier == "SharedError"
        assert feature.commands["UnobservableCommand"].errors["SharedError"].display_name == "Shared Error"
        assert feature.commands["UnobservableCommand"].errors["SharedError"].description == "Shared Error."
        assert (
            feature.commands["UnobservableCommand"].errors["UnobservableCommandError"].identifier
            == "UnobservableCommandError"
        )
        assert (
            feature.commands["UnobservableCommand"].errors["UnobservableCommandError"].display_name
            == "Unobservable Command Error"
        )
        assert (
            feature.commands["UnobservableCommand"].errors["UnobservableCommandError"].description
            == "Unobservable Command Error."
        )

        assert list(feature.properties.keys()) == ["UnobservableProperty"]
        assert feature.properties["UnobservableProperty"].identifier == "UnobservableProperty"
        assert feature.properties["UnobservableProperty"].display_name == "Unobservable Property"
        assert feature.properties["UnobservableProperty"].description == "Unobservable Property."
        assert feature.properties["UnobservableProperty"].data_type == String
        assert list(feature.properties["UnobservableProperty"].errors.keys()) == [
            "SharedError",
            "UnobservablePropertyError",
        ]
        assert feature.properties["UnobservableProperty"].errors["SharedError"].identifier == "SharedError"
        assert feature.properties["UnobservableProperty"].errors["SharedError"].display_name == "Shared Error"
        assert feature.properties["UnobservableProperty"].errors["SharedError"].description == "Shared Error."
        assert (
            feature.properties["UnobservableProperty"].errors["UnobservablePropertyError"].identifier
            == "UnobservablePropertyError"
        )
        assert (
            feature.properties["UnobservableProperty"].errors["UnobservablePropertyError"].display_name
            == "Unobservable Property Error"
        )
        assert (
            feature.properties["UnobservableProperty"].errors["UnobservablePropertyError"].description
            == "Unobservable Property Error."
        )

        assert list(feature.metadata.keys()) == ["SomeMetadata"]
        assert feature.metadata["SomeMetadata"].identifier == "SomeMetadata"
        assert feature.metadata["SomeMetadata"].display_name == "Some Metadata"
        assert feature.metadata["SomeMetadata"].description == "Some Metadata."
        assert feature.metadata["SomeMetadata"].data_type == String
        assert list(feature.metadata["SomeMetadata"].errors.keys()) == ["SharedError", "MetadataError"]
        assert feature.metadata["SomeMetadata"].errors["SharedError"].identifier == "SharedError"
        assert feature.metadata["SomeMetadata"].errors["SharedError"].display_name == "Shared Error"
        assert feature.metadata["SomeMetadata"].errors["SharedError"].description == "Shared Error."
        assert feature.metadata["SomeMetadata"].errors["MetadataError"].identifier == "MetadataError"
        assert feature.metadata["SomeMetadata"].errors["MetadataError"].display_name == "Metadata Error"
        assert feature.metadata["SomeMetadata"].errors["MetadataError"].description == "Metadata Error."


class TestEquality:
    def test_should_be_true_on_equal_feature(self):
        # Create feature
        feature_0 = Feature(identifier="SiLAService", display_name="SiLA Service")
        feature_1 = Feature(identifier="SiLAService", display_name="SiLA Service")

        # Compare equality
        assert feature_0 == feature_1

    def test_should_be_true_on_different_casing(self):
        # Create feature
        feature_0 = Feature(identifier="SILASERVICE", display_name="SiLA Service")
        feature_1 = Feature(identifier="Silaservice", display_name="SiLA Service")

        # Compare equality
        assert feature_0 == feature_1

    def test_should_be_false_on_unequal_identifier(self):
        # Create feature
        feature_0 = Feature(identifier="SiLAService", display_name="SiLA Service")
        feature_1 = Feature(identifier="LockController", display_name="SiLA Service")

        # Compare equality
        assert feature_0 != feature_1

    def test_should_be_false_on_non_sila_feature(self):
        # Create feature
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")

        # Compare equality
        assert feature != object()
